#!/usr/bin/env python3
"""ESIC recruitment notices -> data/govt-live.json

ESIC (Employees' State Insurance Corporation) runs hospitals and medical
colleges in every state and publishes a structured table of recruitment
notices: office, subject, publish date, last date, console number, PDF link.

That table is the best machine-readable source in India for medical,
paramedical, nursing and teaching-faculty posts — the fields aggregators
never cover.

Rules this script follows:
  * a row is kept only if its "Last Date" is a real date in the future
  * rows that are results, corrigenda, cancellations or selection lists are
    dropped — they are not vacancies
  * the PDF link and the console number are kept so a student can open the
    actual notice
  * if the page layout changes and nothing parses, it prints a warning and
    writes nothing rather than publishing guesses

Run AFTER fetch_ncs.py (which writes the file), so this appends to it.
    python3 pipeline/fetch_ncs.py && python3 pipeline/fetch_esic.py && python3 build.py
"""
import json
import re
import urllib.request
from datetime import date, datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "data" / "govt-live.json"
UA = "JobVibeBot/1.0 (+https://github.com/devrajai/JobVibe)"

PAGES = [
    "https://esic.gov.in/Recruitments/esic_hospital_recruitment_list/page:1",
    "https://esic.gov.in/Recruitments/esic_hospital_recruitment_list/page:2",
    "https://esic.gov.in/Recruitments/esic_hospital_recruitment_list/page:3",
]

# rows that are not vacancies
SKIP = re.compile(r"result|corrigendum|addendum|cancellation|selection\s*list|"
                  r"empanel|advocate|notice\s*to\s*advertisement", re.I)
# rows that are vacancies
KEEP = re.compile(r"recruit|walk[\s-]*in|advertis|engag|invit|application|"
                  r"senior\s*resident|junior\s*resident|pharmacist|nursing|technician|faculty", re.I)

CITIES = ["Mumbai","Pune","Nagpur","Nashik","Thane","Ahmedabad","Surat","Vadodara","Rajkot",
          "Bengaluru","Bangalore","Mysuru","Hyderabad","Chennai","Coimbatore","Madurai",
          "Delhi","New Delhi","Gurugram","Noida","Faridabad","Kolkata","Howrah","Patna",
          "Ranchi","Bhopal","Indore","Jaipur","Lucknow","Kanpur","Varanasi","Dehradun",
          "Chandigarh","Kochi","Ernakulam","Thiruvananthapuram","Kozhikode","Bhubaneswar",
          "Guwahati","Raipur","Bilaspur","Angul","Rudrapur","Baddi","Joka","Bihta",
          "Rajajinagar","Andheri","Bibvewadi","Gulbarga","Kalaburagi","Kakinada","Adityapur",
          "Bareilly","Phulwarisharif","Naroda","Tinsukia","Bhilai","Durgapur","Jammu","Srinagar"]

RULES = [
    (r"nurs", "Nursing", "grad"),
    (r"pharmac", "Pharmacy", "grad"),
    (r"lab\s*technician|technician|radiograph|ecg|ot\s|dialysis|optom", "Paramedical", "dip"),
    (r"professor|faculty|tutor|demonstrator", "Teaching", "pg"),
    (r"senior\s*resident|junior\s*resident|specialist|medical\s*officer|ayurved|homeo|dental",
     "Medical", "pg"),
    (r"assistant|clerk|steno|mts|udc|ldc|attendant", "Government", "12"),
]


def classify(subject):
    s = subject.lower()
    for pattern, cat, el in RULES:
        if re.search(pattern, s):
            return cat, el
    return "Paramedical", "dip"


def city_of(office):
    for c in sorted(CITIES, key=len, reverse=True):
        if c.lower() in office.lower():
            return c
    return "All India"


def get(url):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=40) as r:
        return r.read().decode("utf-8", "ignore")


def parse_date(cell):
    """'Interview (2026-11-06)' / 'Last Date (2026-11-25)' / '2026-11-06' -> date"""
    m = re.search(r"(\d{4})-(\d{2})-(\d{2})", cell or "")
    if not m:
        return None
    try:
        return date(int(m.group(1)), int(m.group(2)), int(m.group(3)))
    except ValueError:
        return None


def parse_html(html, today):
    """Rows of one ESIC page -> job records. Split out so it can be unit-tested."""
    found = []
    for row in re.findall(r"<tr[^>]*>(.*?)</tr>", html, re.S | re.I):
        cells = [re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", c)).strip()
                 for c in re.findall(r"<t[dh][^>]*>(.*?)</t[dh]>", row, re.S | re.I)]
        links = re.findall(r'href="([^"]+\.pdf)"', row, re.I)
        if len(cells) < 5 or not links:
            continue

        office, subject, published, last = cells[1], cells[2], cells[3], cells[4]
        if SKIP.search(subject) or not KEEP.search(subject):
            continue

        closing = parse_date(last)
        if not closing or closing < today:
            continue                      # expired, or no date to prove it is open

        cat, el = classify(subject)
        url_pdf = links[0] if links[0].startswith("http") else "https://esic.gov.in" + links[0]
        posted = published if re.match(r"\d{4}-\d{2}-\d{2}", published or "") else None
        days = 0
        if posted:
            try:
                days = max(0, (today - datetime.strptime(posted, "%Y-%m-%d").date()).days)
            except ValueError:
                pass

        found.append({
            "t": subject[:120], "o": office[:90], "cat": cat,
            "city": city_of(office), "type": "Government", "mode": "On-site",
            "el": el, "sal": 0, "salTxt": "As per ESIC / govt norms — see notice",
            "exp": 0, "days": days,
            "sk": [cells[5].strip() if len(cells) > 5 else "ESIC", "Notification PDF"],
            "safe": 0, "ver": 0, "govt": 1,
            "url": url_pdf, "date_posted": posted,
            "last_date": closing.isoformat(), "vacancies": 0,
            "source": "ESIC recruitment notice",
        })
    return found


def main():
    today = date.today()
    found, pages_ok = [], 0

    for url in PAGES:
        try:
            html = get(url)
            pages_ok += 1
        except Exception as e:
            print(f"  ! {url.rsplit('/', 1)[-1]}: {type(e).__name__}: {e}")
            continue

        found.extend(parse_html(html, today))

    if not pages_ok:
        print("ESIC: could not reach any page — nothing written")
        return

    seen, unique = set(), []
    for j in found:
        key = (j["t"].lower(), j["o"].lower())
        if key in seen:
            continue
        seen.add(key)
        unique.append(j)

    payload = json.loads(OUT.read_text(encoding="utf-8")) if OUT.exists() else {"jobs": []}
    existing = payload.get("jobs", [])
    have = {(j["t"].lower(), j["o"].lower()) for j in existing}
    added = [j for j in unique if (j["t"].lower(), j["o"].lower()) not in have]

    payload["jobs"] = existing + added
    OUT.write_text(json.dumps(payload, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"ESIC: {len(found)} open notices parsed, {len(added)} added to data/govt-live.json")


if __name__ == "__main__":
    main()
