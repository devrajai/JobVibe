import json, re, sys, os
sys.path.insert(0, os.path.dirname(__file__))
from new_entries import NEW, NEW_WORKERS, NEW_COURSES, NEW_REVIEWS

base = json.load(open('data/base.json'))

def rows(txt):
    return [l.strip() for l in txt.strip().splitlines() if l.strip() and not l.strip().startswith('#')]

jobs = list(base['jobs'])
seen = {(j['t'], j['o']) for j in jobs}
added = 0
for line in rows(NEW):
    f = [x.strip() for x in line.split('|')]
    if len(f) < 14: raise SystemExit('bad job line: ' + line[:60])
    j = {"t":f[0],"o":f[1],"cat":f[2],"city":f[3],"type":f[4],"mode":f[5],"el":f[6],
         "sal":int(f[7]),"salTxt":f[8],"exp":int(f[9]),"days":int(f[10]),
         "sk":[s.strip() for s in f[11].split(';') if s.strip()],
         "safe":int(f[12]),"ver":int(f[13])}
    if len(f) > 14 and f[14]: j['url'] = f[14]
    if len(f) > 15 and f[15]: j['intern'] = f[15]
    if (j['t'], j['o']) in seen: continue
    seen.add((j['t'], j['o'])); jobs.append(j); added += 1

workers = list(base['workers'])
wseen = {w['n'] for w in workers}
for line in rows(NEW_WORKERS):
    f = [x.strip() for x in line.split('|')]
    if f[0] in wseen: continue
    workers.append({"n":f[0],"tr":f[1],"area":f[2],"exp":int(f[3]),"rate":f[4],"pd":int(f[5]),
                    "cat":[s.strip() for s in f[6].split(';') if s.strip()],
                    "r":float(f[7]),"jobs":int(f[8]),"ph":f[9]}); wseen.add(f[0])

courses = list(base['courses'])
cseen = {c['n'] for c in courses}
for line in rows(NEW_COURSES):
    f = [x.strip() for x in line.split('|')]
    if f[0] in cseen: continue
    courses.append({"n":f[0],"d":f[1],"free":f[2],"u":f[3],"tag":f[4]}); cseen.add(f[0])

reviews = list(base['reviews'])
rseen = {r['org'] for r in reviews}
for line in rows(NEW_REVIEWS):
    f = [x.strip() for x in line.split('|')]
    if f[0] in rseen: continue
    reviews.append({"org":f[0],"role":f[1],"r":float(f[2]),"yrs":f[3],"good":f[4],"bad":f[5],
                    "safe":int(f[6])}); rseen.add(f[0])

jobs.sort(key=lambda j: (j['cat'], j['days']))
out = {"jobs":jobs,"govt":base['govt'],"workers":workers,"courses":courses,"reviews":reviews}
json.dump(out, open('data/site-data.json','w'), ensure_ascii=False, indent=1)

cats = {}
for j in jobs: cats[j['cat']] = cats.get(j['cat'],0)+1
print('jobs added', added, '| total jobs', len(jobs))
print('fields', len(cats))
for k,v in sorted(cats.items(), key=lambda x:-x[1]): print(f'  {k}: {v}')
print('workers', len(workers), '| courses', len(courses), '| reviews', len(reviews))
