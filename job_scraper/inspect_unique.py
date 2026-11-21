import json

jobs = json.load(open('job_scraper/ranked_eligible_jobs.json', encoding='utf-8'))
seen_comps = set()
unique_jobs = []
for j in jobs:
    k = (j['company'].lower().strip(), j['title'].lower().strip()[:20])
    if k not in seen_comps:
        seen_comps.add(k)
        unique_jobs.append(j)

print(f'Unique top jobs: {len(unique_jobs)}')
for i, u in enumerate(unique_jobs[:15], 1):
    print(f"{i}. [{u['source']}] {u['company']} - {u['title']} (Fit: {u['fit_score']}) | {u['url']}")

json.dump(unique_jobs, open('job_scraper/top_unique_eligible_jobs.json', 'w', encoding='utf-8'), indent=2)
