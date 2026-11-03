#!/usr/bin/env python3
"""Live data pipeline — pulls real, currently-open postings from employer job
boards and writes data/live.json.

Every record written here carries the employer's own apply URL, so the button
on the site is a real redirect to a real application page. Nothing is invented.

Sources (public, keyless):
    Ashby        https://api.ashbyhq.com/posting-api/job-board/{org}
    Greenhouse   https://boards-api.greenhouse.io/v1/boards/{token}/jobs?content=true
    Lever        https://api.lever.co/v0/postings/{token}?mode=json

Edit pipeline/sources.json to choose boards. `"india": true` means "this is an
Indian employer, keep its remote roles too"; otherwise only postings whose
location mentions an Indian city are kept.

Run:  python3 pipeline/fetch_sources.py && python3 build.py
"""
import json
import re
import time
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LIVE = ROOT / "data" / "live.json"
SOURCES = ROOT / "pipeline" / "sources.json"
UA = "JobVibeBot/1.0 (+https://github.com/devrajai/JobVibe)"
TIMEOUT = 25

INDIA = re.compile(
    r"india|bengaluru|bangalore|mumbai|delhi|pune|hyderabad|chennai|gurgaon|"
    r"gurugram|noida|ahmedabad|kolkata|jaipur|kochi|indore|chandigarh|coimbatore",
    re.I,
)

# a location that means "anywhere", not a specific foreign city
GENERIC = re.compile(r"^(remote|anywhere|worldwide|global|india|distributed)\b", re.I)

RULES = [
    ("Nursing", r"\b(nurse|nursing|icu)\b"),
    ("Paramedical", r"\b(radiolog\w*|lab tech\w*|technician|phlebotom\w*|optom\w*|physiother\w*|dialysis)\b"),
    ("Pharmacy", r"\b(pharmac\w*|clinical research|drug safety)\b"),
    ("Medical", r"\b(mbbs|resident|physician|surgeon|medical officer)\b"),
    ("Music & Performing Arts", r"\b(music|guitar|piano|tabla|audio|sound engineer)\b"),
    ("Film & Media", r"\b(video|photograph\w*|content writer|journalis\w*|editor)\b"),
    ("Animation & Gaming", r"\b(animat\w*|vfx|3d|game)\b"),
    ("Design & Creative", r"\b(design\w*|ux|ui|figma|brand)\b"),
    ("Cyber Security", r"\b(security|infosec|pentest|appsec|trust)\b"),
    ("IT & Data", r"\b(engineer\w*|developer|software|data|analyst|python|devops|cloud|qa|platform|infra\w*)\b"),
    ("Teaching", r"\b(teacher|tutor|faculty|lecturer|instructor)\b"),
    ("Law", r"\b(legal|law|paralegal|counsel|compliance)\b"),
    ("Commerce & Accounts", r"\b(account\w*|finance|tax|audit|payroll)\b"),
    ("HR", r"\b(recruit\w*|people|talent|human resources)\b"),
    ("Sales & Marketing", r"\b(sales|marketing|growth|business development|account executive)\b"),
    ("BPO & Customer Support", r"\b(support|customer|success|community)\b"),
    ("Logistics & Supply Chain", r"\b(logistic\w*|warehouse|supply chain|operations)\b"),
    ("Hospitality & Travel", r"\b(hotel|chef|travel|front desk|housekeep\w*)\b"),
    ("Beauty & Wellness", r"\b(salon|spa|beauty)\b"),
    ("Sports & Fitness", r"\b(gym|fitness|coach|yoga)\b"),
    ("Event Management", r"\b(event|community manager)\b"),
    ("Agriculture", r"\b(agri\w*|farm)\b"),
    ("Architecture & Interior", r"\b(architect\w*|interior|civil)\b"),
    ("Aviation", r"\b(aviation|aircraft|airport)\b"),
    ("Veterinary", r"\b(veterinar\w*)\b"),
]


def categorise(title, department=""):
    blob = f"{title} {department}".lower()
    for name, pattern in RULES:
        if re.search(pattern, blob):
            return name
    return "IT & Data"


def days_since(value):
    if not value:
        return 0
    try:
        if isinstance(value, (int, float)):
            dt = datetime.fromtimestamp(value / 1000, tz=timezone.utc)
        else:
            dt = datetime.fromisoformat(str(value).replace("Z", "+00:00"))
        return max(0, (datetime.now(timezone.utc) - dt).days)
    except Exception:
        return 0


def get_json(url):
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "application/json"})
    with urllib.request.urlopen(req, timeout=TIMEOUT) as r:
        return json.loads(r.read().decode("utf-8"))


def record(title, org, city, url, when, department="", mode="On-site", pay=""):
    return {
        "t": title.strip(),
        "o": org.strip(),
        "cat": categorise(title, department),
        "city": (city or "India").strip(),
        "type": "Private",
        "mode": mode,
        "el": "grad",
        "sal": 0,
        "salTxt": pay or "Not disclosed",
        "exp": 0,
        "days": days_since(when),
        "sk": [s.strip() for s in re.split(r"[,/|–-]", title) if s.strip()][:3],
        "safe": 0,
        "ver": 1,
        "live": 1,
        "url": url,
    }


# ------------------------------------------------------------------- fetchers
def fetch_ashby(org, india=False):
    data = get_json(f"https://api.ashbyhq.com/posting-api/job-board/{org}?includeCompensation=true")
    out = []
    for j in data.get("jobs", []):
        loc = j.get("location", "") or ""
        sec = ", ".join(s.get("location", "") for s in (j.get("secondaryLocations") or []))
        blob = f"{loc} {sec}"
        remote = (j.get("workplaceType") == "Remote") or ("remote" in blob.lower())
        if not (INDIA.search(blob) or (india and remote and GENERIC.search(loc.strip()))):
            continue
        comp = j.get("compensation") or {}
        pay = comp.get("compensationTierSummary") or ""
        mode = {"Remote": "Remote", "Hybrid": "Hybrid"}.get(j.get("workplaceType", ""), "On-site")
        out.append(record(j.get("title", ""), org.title(), loc or sec,
                          j.get("jobUrl", ""), j.get("publishedAt"),
                          j.get("department", ""), mode, pay))
    return out


def fetch_greenhouse(token, india=False):
    data = get_json(f"https://boards-api.greenhouse.io/v1/boards/{token}/jobs?content=true")
    org = (data.get("meta") or {}).get("name") or token.title()
    out = []
    for j in data.get("jobs", []):
        loc = (j.get("location") or {}).get("name", "") or ""
        if not (INDIA.search(loc) or (india and GENERIC.search(loc.strip()))):
            continue
        out.append(record(j.get("title", ""), org, loc, j.get("absolute_url", ""),
                          j.get("updated_at"),
                          ", ".join(d.get("name", "") for d in j.get("departments", []))))
    return out


def fetch_lever(token, india=False):
    out, skip = [], 0
    while True:
        page = get_json(f"https://api.lever.co/v0/postings/{token}?mode=json&limit=100&skip={skip}")
        if not isinstance(page, list) or not page:
            break
        for j in page:
            cats = j.get("categories") or {}
            loc = cats.get("location", "") or ""
            remote = j.get("workplaceType") == "remote"
            if not (INDIA.search(loc) or (india and remote and GENERIC.search(loc.strip()))):
                continue
            mode = {"remote": "Remote", "hybrid": "Hybrid"}.get(j.get("workplaceType", ""), "On-site")
            out.append(record(j.get("text", ""), token.title(), loc, j.get("hostedUrl", ""),
                              j.get("createdAt"), cats.get("department", ""), mode))
        if len(page) < 100:
            break
        skip += 100
        time.sleep(1)  # Lever's robots.txt asks for a 1 second crawl delay
    return out


FETCHERS = {"ashby": fetch_ashby, "greenhouse": fetch_greenhouse, "lever": fetch_lever}


def main():
    sources = json.loads(SOURCES.read_text(encoding="utf-8"))
    jobs, seen = [], set()
    for s in sources:
        ats = s.get("ats")
        token = s.get("token") or s.get("org")
        fn = FETCHERS.get(ats)
        if not fn:
            print(f"  ! unknown source: {ats}")
            continue
        try:
            got = fn(token, bool(s.get("india")))
        except (urllib.error.HTTPError, urllib.error.URLError, TimeoutError, ValueError) as e:
            print(f"  ! {ats}:{token} — {type(e).__name__}: {e}")
            continue
        fresh = 0
        for rec in got:
            key = (rec["t"].lower(), rec["o"].lower())
            if key in seen:
                continue
            seen.add(key)
            rec["src"] = f"{ats}:{token}"
            jobs.append(rec)
            fresh += 1
        print(f"  {ats}:{token} -> {fresh} live postings")
        time.sleep(0.5)

    jobs.sort(key=lambda j: j["days"])
    payload = {"fetched": datetime.now(timezone.utc).strftime("%d %b %Y"),
               "jobs": jobs}
    LIVE.write_text(json.dumps(payload, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"wrote data/live.json — {len(jobs)} live postings")


if __name__ == "__main__":
    main()
