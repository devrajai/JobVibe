#!/usr/bin/env python3
"""Build index.html from template.html + data/site-data.json.

Edit data/site-data.json (or add to pipeline/new_entries.py and re-run
pipeline/merge.py), then run:  python3 build.py
"""
import json, pathlib, sys

root = pathlib.Path(__file__).parent
data = json.loads((root / "data/site-data.json").read_text(encoding="utf-8"))
tpl = (root / "template.html").read_text(encoding="utf-8")

if "/*__SITE_DATA__*/" not in tpl:
    sys.exit("template.html is missing the /*__SITE_DATA__*/ placeholder")

pairs = [("JOBS", "jobs"), ("GOVT", "govt"), ("WORKERS", "workers"),
         ("COURSES", "courses"), ("REVIEWS", "reviews")]
block = "\n".join(f"const {name} = {json.dumps(data[key], ensure_ascii=False)};" for name, key in pairs)

out = tpl.replace("/*__SITE_DATA__*/", block)
(root / "index.html").write_text(out, encoding="utf-8")

cats = sorted({j["cat"] for j in data["jobs"]})
print(f"built index.html — {len(data['jobs'])} jobs, {len(cats)} fields, "
      f"{len(data['workers'])} workers, {len(data['courses'])} courses, {len(data['reviews'])} reviews")
