# Job portal — course-first job search (name TBD)

A free, single-page job portal for Indian students and workers: every course
and every skill, from MBBS and DMLT to ITI trades, music teachers, gig
workers and government recruitment. No build tools, no framework, no server —
one HTML file that works offline and deploys free.

**Pick the name first, then rename the repo.** The site currently shows
"JobVibe" in three places: the `<title>`, the logo block, and the footer in
`template.html`. Change it there and re-run `python3 build.py`.

---

## What is in the box

```
index.html                  the whole site — generated, do not edit by hand
template.html               the site with /*__SITE_DATA__*/ where data goes
build.py                    template + data -> index.html
data/site-data.json         every listing, worker, course and review
data/live.json              real postings pulled from employer boards today
data/course-map.json        105 courses -> job-title keywords (the course-first edge)
data/city-state.json        city -> state lookup, 125 cities + aliases
data/base.json              the original hand-written seed data
pipeline/new_entries.py     the v2 listings, in a compact pipe format
pipeline/merge.py           merges new_entries.py into site-data.json
pipeline/fetch_sources.py   pulls live boards -> data/live.json (real apply links)
pipeline/sources.json       which employer boards to poll
.github/workflows/          daily refresh on GitHub Actions
```

Current contents: **219 listings across 44 fields**, of which **7 are live postings** fetched from employer boards with the employer's own apply URL, 18 worker profiles,
16 free-course platforms, 9 workplace reviews, 12 official government portals.

## The two ways to change data

**Small edit (one job, one worker).** Edit `data/site-data.json` directly, then:

```bash
python3 build.py
```

**Bulk add.** Append lines to `pipeline/new_entries.py` in the pipe format
documented at the top of that file, then:

```bash
python3 pipeline/merge.py && python3 build.py
```

`merge.py` de-duplicates on title + employer, so re-running it is safe.

## The pipeline

```
employer job boards ──┐
                      ├─> fetch_sources.py ─> normalise ─> site-data.json ─> build.py ─> index.html
your manual listings ─┘                                         ▲
                                                                │
                                        government portals, colleges, local shops
                                        (added by hand — there is no API for these)
```

`fetch_sources.py` polls public, keyless endpoints only:

| ATS | Endpoint | Key needed |
|---|---|---|
| Greenhouse | `boards-api.greenhouse.io/v1/boards/{token}/jobs?content=true` | no |
| Lever | `api.lever.co/v0/postings/{token}?mode=json` | no |
| Ashby | `api.ashbyhq.com/posting-api/job-board/{org}` | no |

It keeps every hand-written listing (anything without a `src` field) and
replaces only previously-sourced ones, so your own data is never overwritten.

**What this pipeline will and will not give you.** These boards are almost
entirely IT, product and startup roles. For nursing, paramedical, ITI trades,
music teaching and government posts — the fields that make this site different —
there is no API. Those come from a human reading notification PDFs on AIIMS,
ESIC, state NHM and district collectorate sites. That manual work is the
product; the pipeline only keeps the tech half fresh.

**Do not scrape LinkedIn, Naukri or Indeed.** Their terms forbid it and they
block it. Adzuna and Jooble have free keys, but their terms restrict how you
may present and monetise the listings, and Adzuna forbids contacting the
employer directly — read the licence before you build on either.

## Deploy free

Pick one; all three are free and give you a subdomain.

**Netlify Drop** — put `index.html` in a folder, drag the folder onto
<https://app.netlify.com/drop>. Live in seconds, no signup to start.

**Cloudflare Pages** — Dashboard → Workers & Pages → Create → Pages →
Upload assets → drag the folder.

**GitHub Pages** — push this repo, then Settings → Pages → Source: `main` /
root. Live at `https://<user>.github.io/<repo>/`.

Then, optionally, in the Actions tab run "Refresh job data" once to confirm
the pipeline works.

A custom domain is the only cost: roughly ₹700–1,200 a year.

## Before you show this to real users

1. **Replace the sample listings with real ones.** Sample data is fine for a
   demo and dangerous for a live site — a student who travels to a fake
   interview has lost real money.
2. **Build the moderation queue.** `data/site-data.json` needs an `approved`
   flag and a simple admin screen before anyone can post. Every job portal
   attracts scammers who charge a "registration fee"; approve employers by
   hand and put the warning on every page.
3. **Make the badges mean something.** `safe` and `ver` are placeholders right
   now. Only set `ver: 1` after you have actually spoken to the employer, and
   only set `safe: 1` after checking that no unresolved harassment or
   wage-theft reports exist.
4. **Add a real backend** when you want employer self-posting: Supabase free
   tier gives Postgres + auth + row-level security, which is enough for a few
   thousand students.
5. **Write in the user's language.** The interface is English; a Hindi or
   regional-language toggle matters a lot for 10th/12th-pass and gig workers.

## Honest status

- Listings: realistic samples, not live vacancies.
- Government links: real, official portals (`*.gov.in` / `*.nic.in`).
- Free-course links: real platforms; the fee notes reflect what those
  platforms generally charge and should be re-checked before you promise
  anything.
- Reviews: illustrative. Publishing real reviews needs moderation and a
  right-of-reply, or you will be on the wrong side of a defamation complaint.
