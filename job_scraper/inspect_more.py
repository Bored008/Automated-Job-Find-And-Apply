import json

jobs = json.load(open('job_scraper/top_unique_eligible_jobs.json', encoding='utf-8'))
for i, u in enumerate(jobs[15:35], 16):
    print(f"{i}. [{u['source']}] {u['company']} - {u['title']} (Fit: {u['fit_score']}) | {u['url']}")
