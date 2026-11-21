import json
import urllib.request
import ssl
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

jobs = json.loads(Path('job_scraper/new_discovered_jobs.json').read_text(encoding='utf-8'))

candidates = []

for j in jobs:
    title = j['title']
    loc = j['location']
    source = j['source']
    company = j['company']
    raw_url = j['url']
    
    # Clean URL if unstop prefix doubled
    if 'unstop.com/o/https://' in raw_url:
        clean_url = raw_url.replace('https://unstop.com/o/', '')
    else:
        clean_url = raw_url
        
    loc_lower = loc.lower()
    if any(x in loc_lower for x in ['united states', 'canada', 'united kingdom', 'singapore', 'us remote', 'san fran']):
        continue
    if any(x in loc_lower for x in ['bangalore', 'bengaluru', 'pune', 'mumbai', 'hyderabad', 'chennai', 'kolkata']):
        continue
        
    t_lower = title.lower()
    fit_score = 60 # base
    if 'nextjs' in t_lower or 'next.js' in t_lower:
        fit_score += 35
    elif 'react' in t_lower:
        fit_score += 30
    elif 'frontend' in t_lower or 'front-end' in t_lower:
        fit_score += 25
    elif 'ui/ux' in t_lower or 'product designer' in t_lower or 'ui designer' in t_lower:
        fit_score += 25
    elif 'full stack' in t_lower or 'fullstack' in t_lower:
        fit_score += 20
        
    if 'junior' in t_lower or 'intern' in t_lower:
        fit_score += 10
    elif 'senior' in t_lower or 'staff' in t_lower or 'principal' in t_lower:
        fit_score -= 10
        
    candidates.append({
        'company': company,
        'title': title,
        'location': loc,
        'url': clean_url,
        'source': source,
        'fit_score': fit_score,
        'department': j.get('department', '')
    })

def check_url(cand):
    url = cand['url']
    try:
        req = urllib.request.Request(url, headers=HEADERS, method='GET')
        with urllib.request.urlopen(req, context=ctx, timeout=4) as r:
            if r.status < 400:
                return cand
    except urllib.error.HTTPError as e:
        if e.code in (401, 403): # ATS login walls or cloudflare challenges often return 403 for active jobs
            return cand
    except Exception:
        pass
    return None

print(f"Validating {len(candidates)} candidates concurrently...", flush=True)

verified = []
with ThreadPoolExecutor(max_workers=10) as executor:
    results = executor.map(check_url, candidates)
    for r in results:
        if r:
            verified.append(r)

verified.sort(key=lambda x: x['fit_score'], reverse=True)

print(f"\nTotal active verified candidates: {len(verified)}", flush=True)
for i, s in enumerate(verified[:12], 1):
    print(f"{i}. [{s['source']}] {s['company']} — {s['title']} (Fit: {s['fit_score']}%)", flush=True)
    print(f"   Location: {s['location']} | URL: {s['url']}", flush=True)

Path('job_scraper/ranked_eligible_jobs.json').write_text(json.dumps(verified, indent=2), encoding='utf-8')
