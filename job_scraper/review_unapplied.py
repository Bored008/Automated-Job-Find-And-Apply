import json
import csv
from pathlib import Path

# Load tracker
tracker_urls = set()
tracker_comps = set()
with open("job_search_tracker.csv", "r", encoding="utf-8") as f:
    for row in csv.DictReader(f):
        if row.get("source"):
            tracker_urls.add(row["source"].rstrip("/"))
        if row.get("company"):
            tracker_comps.add(row["company"].lower().strip())

# Load seen
seen_data = json.load(open("job_scraper/seen_jobs.json", encoding="utf-8")).get("seen", {})
seen_urls = set()
for k, v in seen_data.items():
    if isinstance(v, dict) and v.get("url"):
        if v.get("status") in ("applied", "expired", "rejected"):
            seen_urls.add(v["url"].rstrip("/"))

# Load vetted
vetted = json.load(open("job_scraper/vetted_genuine_jobs.json", encoding="utf-8"))

unapplied = []
for j in vetted:
    url = j.get("url", "").rstrip("/")
    comp = j.get("company", "").lower().strip()
    if url in tracker_urls or url in seen_urls:
        continue
    unapplied.append(j)

print(f"Total unapplied vetted jobs: {len(unapplied)}")
for i, j in enumerate(unapplied[:15], 1):
    print(f"{i}. [{j.get('source')}] {j.get('company')} — {j.get('title')} ({j.get('location')}) [Fit: {j.get('fit_rating')}%]")
    print(f"   URL: {j.get('url')}")
    print(f"   Deadline: {j.get('deadline')}")
