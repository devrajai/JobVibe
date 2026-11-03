#!/usr/bin/env python3
"""Fetch open vacancies from individual employer career pages.

Why this exists: job-board APIs (Ashby, Greenhouse, Lever) are almost entirely
tech companies, and government aggregators (NCS) carry mostly central/state
posts. Pharma and hospital employers publish nothing machine-readable — they
put a table on their own careers page and a PDF behind it. This module handles
that case, one employer at a time.

It appends into data/live.json, so run pipeline/fetch_sources.py first (that
overwrites the file) and this second (this appends).

Conservative by design:
  * a row is included only when an OPEN closing date is found on the page
  * if the page cannot be parsed, or no date is found, nothing is written and
    the script exits 0 — a silent no-op is better than publishing a dead job
  * every record keeps the employer's own URL and names the source

Currently supported: HLL Lifecare (Government of India enterprise — pharma,
diagnostics, healthcare services).

NOTE: the sandbox this was written in cannot reach lifecarehll.com, so the HTML
parse below has not been exercised against the live page. It fails safe: on the
first CI run, check the log line it prints.
"""
import json
import re
import urllib.request
from datetime import date, datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LIVE = ROOT / "data" / "live.json"
UA = "JobVibeBot/1.0 (+https://github.com/devrajai/JobVibe)"

EMPLOYERS = [
    {
        "name": "HLL Lifecare",
        "url": "https://www.lifecarehll.com/careers",
        "ref_pattern": r"HLL/HR/\d{3}/\d{4}",
        "source": "HLL Lifecare careers page",
        "default_category": "Pharmacy",
        "default_city": "Thiruvananthapuram",
    },
]


def get(url):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=40) as r:
        return r.read().decode("utf-8", "ignore")


def text_of(html):
    t = re.sub(r"<script.*?</script>|<style.*?</style>", " ", html, flags=re.S | re.I)
    t = re.sub(r"<[^>]+>", " | ", t)
    return re.sub(r"[ \t]+", " ", t)


def find_closing_date(blob):
    """Latest DD.MM.YYYY that looks like an application deadline on the page."""
    found = []
    for m in re.finditer(r"(?:extended to|last date[^0-9]{0,40}|closing date[^0-9]{0,40})"
                         r"(\d{1,2})[./-](\d{1,2})[./-](\d{4})", blob, re.I):
        d, mo, y = (int(x) for x in m.groups())
        try:
            found.append(date(y, mo, d))
        except ValueError:
            pass
    return max(found) if found else None


def classify(title):
    t = title.lower()
    if re.search(r"qa|qc|quality|production|pharmac", t):
        return "Pharmacy"
    if re.search(r"diagnostic|lab|biochem|radiolog|teleradiolog", t):
        return "Paramedical"
    if re.search(r"audit|business|operations|manager|training", t):
        return "Management"
    return "Pharmacy"


def fetch_hll(cfg):
    html = get(cfg["url"])
    blob = text_of(html)
    closing = find_closing_date(blob)

    rows = []
    # each posting row: position | ref | location | nature | vacancy
    for m in re.finditer(
        r"([A-Z][A-Za-z0-9 ()&/\-–,\.]{6,90}?)\s*\|\s*(" + cfg["ref_pattern"] + r")\s*\|"
        r"\s*([^|]{2,60})\|\s*([^|]{0,40})\|\s*([0-9]{1,3})\s*\|", blob):
        title, ref, location, _nature, vacancy = (x.strip() for x in m.groups())
        title = re.sub(r"^[0-9]+\s*\|\s*", "", title).strip()
        if len(title) < 6:
            continue
        rows.append({
            "t": title, "o": cfg["name"], "cat": classify(title),
            "city": location or cfg["default_city"],
            "type": "Government", "mode": "On-site", "el": "grad",
            "sal": 0, "salTxt": "As per company pay scale — see notice",
            "exp": 0, "days": 0, "sk": [ref, "Official careers page"],
            "safe": 0, "ver": 0, "live": 1,
            "url": cfg["url"], "source": cfg["source"],
            "last_date": closing.isoformat() if closing else None,
        })

    if not rows:
        print(f"  {cfg['name']}: no posting rows parsed — page layout may have changed")
        return []
    if closing is None:
        print(f"  {cfg['name']}: {len(rows)} rows found but no closing date — skipped (cannot confirm open)")
        return []
    if closing < date.today():
        print(f"  {cfg['name']}: advertisement closed {closing.isoformat()} — {len(rows)} rows dropped")
        return []
    print(f"  {cfg['name']}: {len(rows)} open postings, closes {closing.isoformat()}")
    return rows


def main():
    payload = json.loads(LIVE.read_text(encoding="utf-8")) if LIVE.exists() else {"jobs": []}
    existing = payload.get("jobs", [])
    have = {(j["t"].lower(), j["o"].lower()) for j in existing}

    added = []
    for cfg in EMPLOYERS:
        try:
            for rec in fetch_hll(cfg):
                key = (rec["t"].lower(), rec["o"].lower())
                if key in have:
                    continue
                have.add(key)
                added.append(rec)
        except Exception as e:                      # network, TLS, markup, anything
            print(f"  ! {cfg['name']}: {type(e).__name__}: {e}")

    if added:
        payload["jobs"] = existing + added
        LIVE.write_text(json.dumps(payload, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"employer pages: {len(added)} open postings added to data/live.json")


if __name__ == "__main__":
    main()
