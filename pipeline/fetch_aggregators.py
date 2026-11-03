#!/usr/bin/env python3
"""Aggregator fetchers: Adzuna and Jooble.

Both need a free API key, so they only run when the keys exist as environment
variables (GitHub Actions secrets). Without keys this script prints what is
missing and exits 0 — it never breaks the daily build.

    ADZUNA_ID, ADZUNA_KEY   -> https://developer.adzuna.com  (free key, India = "in")
    JOOBLE_KEY              -> https://jooble.org/api/about  (free key on request)

What it does, in order:
    fetch  -> normalise to the site schema -> tag the course -> clean -> write

Cleaning drops a job if it mentions a fee, has no apply link, is older than 30
days, or duplicates another on (title, employer, city). Every kept record keeps
the aggregator's own URL and names the source, because both require attribution.

Rotation: pipeline/rotation.json lists (keyword, location) pairs. Free tiers are
small, so only ROTATION_SLICE pairs run per day; the cursor lives in
data/rotation-state.json so tomorrow continues where today stopped.

Run:  python3 pipeline/fetch_aggregators.py && python3 build.py
"""
import json
import os
import re
import time
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LIVE = ROOT / "data" / "live.json"
COURSEMAP = ROOT / "data" / "course-map.json"
ROTATION = ROOT / "pipeline" / "rotation.json"
CURSOR = ROOT / "data" / "rotation-state.json"
UA = "JobVibeBot/1.0 (+https://github.com/devrajai/JobVibe)"

SLICE = int(os.environ.get("ROTATION_SLICE", "25"))     # queries per day
MAX_AGE_DAYS = 30
TIMEOUT = 30

SCAM = re.compile(
    r"registration\s*fee|security\s*deposit|pay\s*to\s*join|joining\s*fee|"
    r"refundable\s*deposit|training\s*charge|deposit\s*amount|processing\s*fee",
    re.I,
)

# ------------------------------------------------------------------ course tag
def load_keyword_index():
    """keyword -> (category, education level), from the course map."""
    try:
        cm = json.loads(COURSEMAP.read_text(encoding="utf-8"))
    except Exception:
        return {}
    idx = {}
    for c in cm.get("courses", []):
        for kw in c.get("keywords", []) + c.get("titles", []):
            idx.setdefault(kw.lower(), (c["category"], c.get("education_min", "grad")))
    return idx


KEYWORDS = load_keyword_index()


def tag_course(title, description=""):
    blob = f"{title} {description}".lower()
    best = None
    for kw, meta in KEYWORDS.items():
        if len(kw) >= 4 and kw in blob:
            if best is None or len(kw) > best[0]:
                best = (len(kw), meta)
    return best[1] if best else ("IT & Data", "grad")


# -------------------------------------------------------------------- helpers
def days_old(value):
    if not value:
        return 0
    try:
        if isinstance(value, (int, float)):
            dt = datetime.fromtimestamp(value, tz=timezone.utc)
        else:
            dt = datetime.fromisoformat(str(value).replace("Z", "+00:00"))
        return max(0, (datetime.now(timezone.utc) - dt).days)
    except Exception:
        return 0


def get_json(url):
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "application/json"})
    with urllib.request.urlopen(req, timeout=TIMEOUT) as r:
        return json.loads(r.read().decode("utf-8", "ignore"))


def post_json(url, payload):
    req = urllib.request.Request(
        url, data=json.dumps(payload).encode(),
        headers={"User-Agent": UA, "Content-Type": "application/json", "Accept": "application/json"})
    with urllib.request.urlopen(req, timeout=TIMEOUT) as r:
        return json.loads(r.read().decode("utf-8", "ignore"))


def record(title, org, city, url, when, category, el, source, pay=""):
    return {
        "t": (title or "").strip()[:120], "o": (org or "Employer").strip()[:80],
        "cat": category, "city": (city or "India").strip()[:60],
        "type": "Private", "mode": "On-site", "el": el,
        "sal": 0, "salTxt": pay or "Not disclosed",
        "exp": 0, "days": days_old(when),
        "sk": [s.strip() for s in re.split(r"[,/|–-]", title or "") if s.strip()][:3],
        "safe": 0, "ver": 0, "live": 1,
        "url": url, "source": source,
    }


# ------------------------------------------------------------------- fetchers
def fetch_adzuna(app_id, app_key, keyword, location):
    url = ("https://api.adzuna.com/v1/api/jobs/in/search/1"
           f"?app_id={app_id}&app_key={app_key}&results_per_page=40"
           f"&what={urllib.parse.quote(keyword)}&where={urllib.parse.quote(location)}"
           "&content-type=application/json")
    data = get_json(url)
    out = []
    for j in data.get("results", []):
        cat, el = tag_course(j.get("title", ""), j.get("description", ""))
        pay = ""
        if j.get("salary_min"):
            pay = f"₹{int(j['salary_min']):,} – ₹{int(j.get('salary_max') or j['salary_min']):,} per year"
        out.append(record(j.get("title"), (j.get("company") or {}).get("display_name"),
                          (j.get("location") or {}).get("display_name"),
                          j.get("redirect_url"), j.get("created"), cat, el,
                          "Adzuna", pay))
    return out


def fetch_jooble(key, keyword, location):
    data = post_json(f"https://jooble.org/api/{key}",
                     {"keywords": keyword, "location": location})
    out = []
    for j in data.get("jobs", []):
        cat, el = tag_course(j.get("title", ""), j.get("snippet", ""))
        out.append(record(j.get("title"), j.get("company"), j.get("location"),
                          j.get("link"), j.get("updated"), cat, el,
                          "Jooble", j.get("salary") or ""))
    return out


# ---------------------------------------------------------------------- main
def load_cursor():
    if CURSOR.exists():
        try:
            return json.loads(CURSOR.read_text(encoding="utf-8")).get("index", 0)
        except Exception:
            pass
    return 0


def main():
    app_id, app_key = os.environ.get("ADZUNA_ID"), os.environ.get("ADZUNA_KEY")
    jooble = os.environ.get("JOOBLE_KEY")

    if not (app_id and app_key) and not jooble:
        print("no aggregator keys set (ADZUNA_ID/ADZUNA_KEY/JOOBLE_KEY) — skipping")
        return

    if not ROTATION.exists():
        print("pipeline/rotation.json missing — nothing to fetch")
        return
    queries = json.loads(ROTATION.read_text(encoding="utf-8"))
    start = load_cursor() % max(1, len(queries))
    today = [queries[(start + i) % len(queries)] for i in range(min(SLICE, len(queries)))]

    found, errors = [], 0
    for q in today:
        kw, loc = q.get("keyword", ""), q.get("location", "India")
        if app_id and app_key:
            try:
                found += fetch_adzuna(app_id, app_key, kw, loc)
            except (urllib.error.HTTPError, urllib.error.URLError, TimeoutError, ValueError) as e:
                errors += 1
                print(f"  ! adzuna {kw}/{loc}: {type(e).__name__}")
            time.sleep(0.4)
        if jooble:
            try:
                found += fetch_jooble(jooble, kw, loc)
            except (urllib.error.HTTPError, urllib.error.URLError, TimeoutError, ValueError) as e:
                errors += 1
                print(f"  ! jooble {kw}/{loc}: {type(e).__name__}")
            time.sleep(0.4)

    # ---- clean ----
    kept, seen, dropped = [], set(), {"fee": 0, "nolnk": 0, "old": 0, "dup": 0}
    for j in found:
        blob = f"{j['t']} {j['salTxt']}"
        if SCAM.search(blob):
            dropped["fee"] += 1
            continue
        if not j.get("url"):
            dropped["nolnk"] += 1
            continue
        if j["days"] > MAX_AGE_DAYS:
            dropped["old"] += 1
            continue
        key = (j["t"].lower(), j["o"].lower(), j["city"].lower())
        if key in seen:
            dropped["dup"] += 1
            continue
        seen.add(key)
        kept.append(j)

    # ---- merge: keep everything already in live.json that is not from an aggregator ----
    payload = json.loads(LIVE.read_text(encoding="utf-8")) if LIVE.exists() else {"jobs": []}
    manual = [j for j in payload.get("jobs", [])
              if (j.get("source") or "") not in ("Adzuna", "Jooble")]
    payload["jobs"] = manual + kept
    payload["fetched"] = datetime.now(timezone.utc).strftime("%d %b %Y")
    LIVE.write_text(json.dumps(payload, ensure_ascii=False, indent=1), encoding="utf-8")

    CURSOR.write_text(json.dumps({"index": (start + len(today)) % max(1, len(queries)),
                                  "updated": datetime.now(timezone.utc).isoformat()},
                                 indent=1), encoding="utf-8")

    print(f"aggregators: {len(found)} fetched, {len(kept)} kept, "
          f"dropped {dropped} , errors {errors}; next cursor {start + len(today)}")


if __name__ == "__main__":
    main()
