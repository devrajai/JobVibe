#!/usr/bin/env python3
"""Build index.html from template.html + data/site-data.json + data/live.json.

    python3 pipeline/fetch_sources.py   # refresh live postings (optional)
    python3 build.py                    # regenerate the site

Live postings are listed first and carry the employer's own apply URL.
"""
import json
import pathlib
import sys

root = pathlib.Path(__file__).parent
data = json.loads((root / "data" / "site-data.json").read_text(encoding="utf-8"))

govt_path = root / "data" / "govt-live.json"
if govt_path.exists():
    govt_live = json.loads(govt_path.read_text(encoding="utf-8"))
else:
    govt_live = {"fetched": "", "jobs": []}

live_path = root / "data" / "live.json"
if live_path.exists():
    live = json.loads(live_path.read_text(encoding="utf-8"))
else:
    live = {"fetched": "", "jobs": []}
live_jobs = live.get("jobs", [])
fetched = live.get("fetched") or "not yet fetched"

tpl = (root / "template.html").read_text(encoding="utf-8")
if "/*__SITE_DATA__*/" not in tpl:
    sys.exit("template.html is missing the /*__SITE_DATA__*/ placeholder")

jobs = live_jobs + govt_live.get("jobs", []) + data["jobs"]
pairs = [("JOBS", jobs), ("GOVT", data["govt"]), ("WORKERS", data["workers"]),
         ("COURSES", data["courses"]), ("REVIEWS", data["reviews"])]

block = "\n".join(
    f"const {name} = {json.dumps(value, ensure_ascii=False)};" for name, value in pairs
)
cs_path = root / "data" / "city-state.json"
citystate = json.loads(cs_path.read_text(encoding="utf-8")) if cs_path.exists() else {"cities": {}, "aliases": {}, "special": {}}
block += f"\nconst LIVE = {json.dumps(live_jobs, ensure_ascii=False)};"
ss_path = root / "data" / "state-sources.json"
state_sources = json.loads(ss_path.read_text(encoding="utf-8")) if ss_path.exists() else {"states": []}
block += f"\nconst STATE_SOURCES = {json.dumps(state_sources.get('states', []), ensure_ascii=False)};"
block += f"\nconst CITYSTATE = {json.dumps({'cities': citystate.get('cities', {}), 'aliases': citystate.get('aliases', {})}, ensure_ascii=False)};"
block += f"\nconst LIVE_DATE = {json.dumps(fetched)};"

(root / "index.html").write_text(tpl.replace("/*__SITE_DATA__*/", block), encoding="utf-8")

fields = sorted({j["cat"] for j in jobs})
print(f"built index.html — {len(jobs)} listings ({len(live_jobs)} live, "
      f"{len(govt_live.get('jobs', []))} government) across "
      f"{len(fields)} fields, {len(data['workers'])} workers, "
      f"{len(data['courses'])} courses, {len(data['reviews'])} reviews")
