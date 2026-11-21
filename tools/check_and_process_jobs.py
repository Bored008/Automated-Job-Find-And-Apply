import urllib.request
import json
import ssl
from datetime import datetime

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
    'Accept': 'application/json, text/plain, */*'
}

unstop_ids = [
    ('Zenotalent', '1791205', 'https://unstop.com/internships/full-stack-developer-internship-zenotalent-1791205'),
    ('Frontend Arena', '1803735', 'https://unstop.com/internships/frontend-developer-internship-frontend-arena-1803735'),
    ('Rewyoo.com', '1806024', 'https://unstop.com/internships/uiux-design-internship-rewyoocom-1806024'),
]

print("Checking Unstop positions:")
for name, opp_id, url in unstop_ids:
    api_url = f"https://unstop.com/api/public/competition/{opp_id}"
    req = urllib.request.Request(api_url, headers=HEADERS)
    try:
        with urllib.request.urlopen(req, context=ctx, timeout=8) as r:
            data = json.loads(r.read().decode('utf-8'))
            comp = data.get('data', {}).get('competition', {})
            title = comp.get('title')
            status = comp.get('status')
            regn_open = comp.get('regn_open')
            end_date = comp.get('end_date')
            print(f"[{name}] Title: {title} | Status: {status} | RegOpen: {regn_open} | End: {end_date}")
    except Exception as e:
        print(f"[{name}] Error: {e}")

print("\nChecking newly discovered jobs in job_scraper/new_active_discovered.json:")
try:
    with open('job_scraper/new_active_discovered.json', 'r', encoding='utf-8') as f:
        new_jobs = json.load(f)
    print(f"Total new active jobs in file: {len(new_jobs)}")
    for j in new_jobs:
        print(f" - [{j.get('source')}] {j.get('company')} — {j.get('title')} ({j.get('location')}) Fit: {j.get('fit_rating')}% | {j.get('url')}")
except Exception as e:
    print(f"Error reading new jobs: {e}")
