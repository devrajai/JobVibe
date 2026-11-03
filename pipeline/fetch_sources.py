#!/usr/bin/env python3
"""Data pipeline: pull live listings from free public sources and merge them
into data/site-data.json.

What this does
--------------
1. Reads pipeline/sources.json — a list of employer job boards to poll.
2. Fetches each board from a keyless public endpoint:
      Greenhouse  https://boards-api.greenhouse.io/v1/boards/{token}/jobs?content=true
      Lever       https://api.lever.co/v0/postings/{token}?mode=json
      Ashby       https://api.ashbyhq.com/posting-api/job-board/{org}
3. Normalises every posting into this site's schema.
4. Keeps all hand-written listings (anything without a "src" key) and replaces
   only the previously-sourced ones, so your manual data is never lost.
5. Writes data/site-data.json. Run build.py afterwards.

Rules of the road
-----------------
- Public board data only. Never scrape LinkedIn, Naukri or Indeed — their terms
  forbid it and they block it.
- Identify yourself in the User-Agent, honour robots.txt crawl delays (Lever
  asks for 1 second), and back off on HTTP 429.
- Store the job id so you can tell new postings from old ones. A job that
  disappears from a board is closed.
- Do not fetch more than a few times a day; boards rarely change faster.

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
DATA = ROOT / "data" / "site-data.json"
SOURCES = ROOT / "pipeline" / "sources.json"
UA = "JobVibeJobAggregator/1.0 (+contact: you@example.com)"  # <- put your email here
TIMEOUT = 30

# ---------------------------------------------------------------- categorising
# Order matters: first match wins. Extend freely.
RULES = [
    ("Nursing", r"nurse|nursing|icu|gnm"),
    ("Paramedical", r"radiolog|lab tech|technician.*(ot|lab|dialysis|ecg)|phlebotom|optom|physiother"),
    ("Pharmacy", r"pharmac|pharm\.?d|drug safety|clinical research"),
    ("Medical", r"mbbs|resident|medical officer|surgeon|physician"),
    ("Music & Performing Arts", r"music|guitar|piano|tabla|sound engineer|audio"),
    ("Film & Media", r"video|photograph|content writer|journalis|editor"),
    ("Animation & Gaming", r"animat|vfx|3d|game|unity"),
    ("Design & Creative", r"design|ux|ui|graphic|figma"),
    ("Cyber Security", r"security|soc|pentest|infosec"),
    ("IT & Data", r"engineer|developer|software|data|analyst|python|java|devops|cloud|qa|test"),
    ("Teaching", r"teacher|tutor|faculty|lecturer|professor|trainer"),
    ("Law", r"legal|law|paralegal|counsel|compliance"),
    ("Commerce & Accounts", r"account|finance|tax|gst|audit|payroll|bookkeep"),
    ("HR", r"recruit|human resource|talent|hr "),
    ("Sales & Marketing", r"sales|marketing|growth|business development|bd "),
    ("BPO & Customer Support", r"support|customer|call cent|bpo|success"),
    ("Logistics & Supply Chain", r"logistic|warehouse|supply chain|driver|fleet"),
    ("Hospitality & Travel", r"hotel|chef|hospitality|travel|tour|front desk|housekeep"),
    ("Beauty & Wellness", r"salon|spa|beauty|hair|barber|nail"),
    ("Sports & Fitness", r"gym|fitness|coach|yoga|swim|sport"),
    ("Event Management", r"event|wedding|planner"),
    ("Agriculture", r"agri|farm|agronom|horticult|dairy"),
    ("Architecture & Interior", r"architect|interior|autocad|civil"),
    ("Aviation", r"cabin crew|aviation|aircraft|airport|ame"),
    ("Veterinary", r"veterinar|vet "),
]


def categorise(title: str, department: str = "") -> str:
    blob = f"{title} {department}".lower()
    for name, pattern in RULES:
        if re.search(pattern, blob):
            return name
    return "IT & Data"  # safe default for ATS boards, which are mostly tech


def days_since(iso_or_ms):
    """Accept ISO strings or Unix ms; return whole days, floor 0."""
    if not iso_or_ms:
        return 0
    try:
        if isinstance(iso_or_ms, (int, float)):
            dt = datetime.fromtimestamp(iso_or_ms / 1000, tz=timezone.utc)
        else:
            dt = datetime.fromisoformat(str(iso_or_ms).replace("Z", "+00:00"))
        return max(0, (datetime.now(timezone.utc) - dt).days)
    except Exception:
        return 0


def get_json(url: str):
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "application/json"})
    with urllib.request.urlopen(req, timeout=TIMEOUT) as r:
        return json.loads(r.read().decode("utf-8"))


def norm(title, org, city, url, when, department="", mode="On-site", el="grad"):
    """One posting -> one record in the site's schema."""
    return {
        "t": title.strip(),
        "o": org.strip(),
        "cat": categorise(title, department),
        "city": (city or "Not specified").strip(),
        "type": "Private",
        "mode": mode,
        "el": el,
        "sal": 0,
        "salTxt": "Not disclosed",
        "exp": 0,
        "days": days_since(when),
        "sk": [s for s in re.split(r"[,/|–-]", title) if s.strip()][:3],
        "safe": 0,
        "ver": 1,
        "url": url,
    }


# ------------------------------------------------------------------- fetchers
def fetch_greenhouse(token: str):
    data = get_json(f"https://boards-api.greenhouse.io/v1/boards/{token}/jobs?content=true")
    org = (data.get("meta") or {}).get("name") or token
    out = []
    for j in data.get("jobs", []):
        out.append(norm(j.get("title", ""), org,
                        (j.get("location") or {}).get("name", ""),
                        j.get("absolute_url", ""), j.get("updated_at"),
                        ", ".join(d.get("name", "") for d in j.get("departments", []))))
    return out


def fetch_lever(token: str):
    out, skip = [], 0
    while True:
        page = get_json(f"https://api.lever.co/v0/postings/{token}?mode=json&limit=100&skip={skip}")
        if not isinstance(page, list) or not page:
            break
        for j in page:
            cats = j.get("categories") or {}
            mode = {"remote": "Remote", "hybrid": "Hybrid"}.get(j.get("workplaceType", ""), "On-site")
            out.append(norm(j.get("text", ""), token.title(), cats.get("location", ""),
                            j.get("hostedUrl", ""), j.get("createdAt"),
                            cats.get("department", ""), mode))
        if len(page) < 100:
            break
        skip += 100
        time.sleep(1)  # Lever's robots.txt asks for a 1 second crawl delay
    return out


def fetch_ashby(org: str):
    data = get_json(f"https://api.ashbyhq.com/posting-api/job-board/{org}?includeCompensation=true")
    out = []
    for j in data.get("jobs", []):
        mode = {"Remote": "Remote", "Hybrid": "Hybrid"}.get(j.get("workplaceType", ""), "On-site")
        out.append(norm(j.get("title", ""), org.title(),
                        j.get("location", "") or j.get("secondaryLocations", ""),
                        j.get("jobUrl", ""), j.get("publishedAt"),
                        j.get("department", ""), mode))
    return out


FETCHERS = {"greenhouse": fetch_greenhouse, "lever": fetch_lever, "ashby": fetch_ashby}


# ----------------------------------------------------------------------- main
def main():
    data = json.loads(DATA.read_text(encoding="utf-8"))
    manual = [j for j in data["jobs"] if not j.get("src")]
    sources = json.loads(SOURCES.read_text(encoding="utf-8")) if SOURCES.exists() else []

    sourced, seen = [], set()
    for s in sources:
        ats, token = s.get("ats"), s.get("token") or s.get("org")
        fn = FETCHERS.get(ats)
        if not fn:
            print(f"  ! unknown source type: {ats}")
            continue
        try:
            got = fn(token)
        except (urllib.error.HTTPError, urllib.error.URLError, TimeoutError, ValueError) as e:
            print(f"  ! {ats}:{token} failed — {e}")
            continue
        for rec in got:
            key = (rec["t"].lower(), rec["o"].lower())
            if key in seen:
                continue
            seen.add(key)
            rec["src"] = f"{ats}:{token}"
            sourced.append(rec)
        print(f"  {ats}:{token} -> {len(got)} postings")
        time.sleep(1)

    data["jobs"] = manual + sourced
    DATA.write_text(json.dumps(data, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"kept {len(manual)} hand-written, added {len(sourced)} sourced, total {len(data['jobs'])}")


if __name__ == "__main__":
    main()
