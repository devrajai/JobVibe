#!/usr/bin/env python3
"""Fetch real government vacancies from the National Career Service portal.

NCS (ncs.gov.in) is run by the Ministry of Labour & Employment and publishes a
public table of current government vacancies with the official notification PDF
link for each one. That table is the source here — we never invent a vacancy,
a last date or a pay figure.

What this writes: data/govt-live.json
Every record carries `url` (the official notification), `source`, `date_posted`
and `vacancies`. `last_date` is left null because it is inside the PDF — the
site says "check the notice for the last date" rather than guessing.

Run:  python3 pipeline/fetch_ncs.py && python3 build.py
"""
import json
import re
import urllib.request
from datetime import date, datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "data" / "govt-live.json"
URL = "https://ncs.gov.in/latest-update"
UA = "JobVibeBot/1.0 (+https://github.com/devrajai/JobVibe)"

# organisation / title keyword -> (category, education level)
MAP = [
    (r"nurs|nursing", "Nursing", "grad"),
    (r"pharmac|medical|hospital|aiims|esic|nhm|health", "Paramedical", "dip"),
    (r"apprentice|technician|diploma", "Engineering", "dip"),
    (r"iti|fitter|welder|electrician|wireman", "Engineering", "iti"),
    (r"sweeper|safai|chowkidar|mts|peon|attendant|helper", "Gig & Local", "10"),
    (r"professor|faculty|lecturer|research fellow|jrf|scientist", "Teaching", "pg"),
    (r"engineer|software|project|data|computer|cdac|programmer", "IT & Data", "grad"),
    (r"clerk|assistant|steno|typist|udc|ldc", "Government", "12"),
    (r"constable|police|guard|coast", "Defence & Police", "12"),
    (r"teacher|instructor|trainer", "Teaching", "grad"),
]


def classify(org, title):
    blob = f"{org} {title}".lower()
    for pattern, cat, el in MAP:
        if re.search(pattern, blob):
            return cat, el
    return "Government", "grad"


def get(url):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=40) as r:
        return r.read().decode("utf-8", "ignore")


def main():
    html = get(URL)
    rows = re.findall(r"<tr[^>]*>(.*?)</tr>", html, re.S | re.I)
    jobs = []
    today = date.today()

    for row in rows:
        cells = [re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", c)).strip()
                 for c in re.findall(r"<t[dh][^>]*>(.*?)</t[dh]>", row, re.S | re.I)]
        links = re.findall(r'href="([^"]+)"', row)
        if len(cells) < 6 or not re.match(r"^\d+$", cells[0] or ""):
            continue
        if not links:
            continue

        org, title, posted, vacancy, kind = cells[1], cells[2], cells[3], cells[4], cells[5]
        title = (title.replace("&amp;", "&").replace("&nbsp;", " ").strip())
        org = org.replace("&amp;", "&").strip()
        if not org or not title:
            continue

        try:
            d = datetime.strptime(posted, "%Y-%m-%d").date()
            days = max(0, (today - d).days)
        except ValueError:
            d, days = None, 0

        try:
            vac = int(re.sub(r"[^0-9]", "", vacancy) or 0)
        except ValueError:
            vac = 0

        cat, el = classify(org, title)
        jobs.append({
            "t": title, "o": org, "cat": cat, "city": "All India",
            "type": "Government", "mode": "On-site", "el": el,
            "sal": 0, "salTxt": "Government pay level — see notice",
            "exp": 0, "days": days, "sk": [kind or "Government", "Notification PDF"],
            "safe": 0, "ver": 0, "govt": 1,
            "url": links[0],
            "date_posted": posted if d else None,
            "last_date": None,            # inside the PDF; never guessed
            "vacancies": vac,
            "source": "National Career Service (ncs.gov.in)",
        })

    # de-duplicate on title + organisation
    seen, unique = set(), []
    for j in jobs:
        key = (j["t"].lower(), j["o"].lower())
        if key in seen:
            continue
        seen.add(key)
        unique.append(j)

    OUT.write_text(json.dumps({
        "fetched": datetime.now().strftime("%d %b %Y"),
        "source": "National Career Service, ncs.gov.in",
        "jobs": unique}, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"wrote data/govt-live.json — {len(unique)} government vacancies")


if __name__ == "__main__":
    main()
