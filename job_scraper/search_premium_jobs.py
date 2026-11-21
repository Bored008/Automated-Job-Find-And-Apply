import urllib.request
import urllib.parse
import json
import ssl
import csv
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'application/json, text/plain, */*'
}

def log(msg):
    print(msg, flush=True)

def fetch_json(url, timeout=5):
    req = urllib.request.Request(url, headers=HEADERS)
    try:
        with urllib.request.urlopen(req, context=ctx, timeout=timeout) as resp:
            if resp.status == 200:
                return json.loads(resp.read().decode('utf-8', errors='replace'))
    except Exception:
        pass
    return None

def load_seen():
    seen_path = Path('job_scraper/seen_jobs.json')
    if seen_path.exists():
        try:
            d = json.loads(seen_path.read_text(encoding='utf-8'))
            return d.get('seen', {})
        except Exception:
            pass
    return {}

def load_tracker():
    tracker_path = Path('job_search_tracker.csv')
    tracker_entries = []
    if tracker_path.exists():
        try:
            with open(tracker_path, mode='r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for r in reader:
                    tracker_entries.append(r)
        except Exception:
            pass
    return tracker_entries

# Quality filters
POSITIVE_KEYWORDS = [
    'frontend', 'front-end', 'front end',
    'full stack', 'fullstack', 'full-stack',
    'react', 'next.js', 'nextjs',
    'ui/ux', 'ui designer', 'ux designer', 'product designer',
    'web designer', 'design engineer', 'ui engineer'
]

EXCLUDE_TITLES = [
    'staff', 'principal', 'lead', 'director', 'vp', 'head', 'architect',
    'sales', 'account executive', 'recruiter', 'marketing', 'legal',
    'devops', 'sre', 'ios', 'android', 'hardware', 'security engineer'
]

ALLOWED_LOCATIONS = [
    'remote', 'india', 'delhi', 'ncr', 'gurugram', 'gurgaon', 'noida', 'sonipat', 'haryana', 'anywhere', 'worldwide', 'global'
]

RESTRICTED_LOCATIONS = [
    'united states only', 'us only', 'usa only', 'us / canada', 'us/canada',
    'san francisco only', 'new york only', 'london only', 'uk only', 'germany only',
    'bangalore only', 'bengaluru only', 'pune only', 'mumbai only', 'hyderabad only', 'chennai only'
]

def is_matching_role(title):
    t = title.lower()
    if any(ex in t for ex in EXCLUDE_TITLES):
        return False
    return any(pos in t for pos in POSITIVE_KEYWORDS)

def is_matching_location(loc_str):
    if not loc_str:
        return True # Default to true for remote-first startups
    l = loc_str.lower()
    if any(r in l for r in RESTRICTED_LOCATIONS):
        return False
    return any(a in l for a in ALLOWED_LOCATIONS)

# 1. Broad list of high-tier startups & tech companies on Ashby
ASHBY_ORGS = [
    'posthog', 'supabase', 'linear', 'resend', 'livekit', 'clerk', 'plane',
    'signoz', 'perplexity', 'modal', 'cartesia', 'langfuse', 'tldraw',
    'cursor', 'groq', 'together', 'retool', 'quarry', 'sentry', 'replit',
    'vapi', 'elevenlabs', 'deepgram', 'braintrust', 'mintlify', 'inngest',
    'speakeasy', 'cal-com', 'dub', 'raycast', 'warp', 'zed', 'trigger-dev',
    'axiom', 'fal-ai', 'midjourney', 'reworkd', 'browserbase'
]

def check_ashby_org(org):
    url = f"https://api.ashbyhq.com/posting-api/job-board/{org}"
    data = fetch_json(url)
    if not data or 'jobs' not in data:
        return []
    matches = []
    for j in data.get('jobs', []):
        if not j.get('isListed', True):
            continue
        title = j.get('title', '')
        loc = j.get('location', '')
        if not is_matching_role(title):
            continue
        if not is_matching_location(loc):
            continue
        matches.append({
            'company': org.capitalize(),
            'title': title,
            'location': loc or 'Remote (Global)',
            'url': j.get('jobUrl') or f"https://jobs.ashbyhq.com/{org}/{j.get('id')}",
            'source': 'Ashby ATS',
            'department': j.get('department', '')
        })
    return matches

# 2. Top Indian tech companies and global remote tech on Greenhouse
GH_ORGS = [
    'vercel', 'cloudflare', 'remote', 'razorpay', 'browserstack', 'sprinklr',
    'hasura', 'postman', 'cred', 'swiggy', 'meesho', 'urbancompany',
    'cleartax', 'hackerrank', 'airmeet', 'gitlab', 'docker', 'elastic', 'brex'
]

def check_gh_org(org):
    url = f"https://boards-api.greenhouse.io/v1/boards/{org}/jobs"
    data = fetch_json(url)
    if not data or 'jobs' not in data:
        return []
    matches = []
    for j in data.get('jobs', []):
        title = j.get('title', '')
        loc = j.get('location', {}).get('name', '') if isinstance(j.get('location'), dict) else str(j.get('location', ''))
        if not is_matching_role(title):
            continue
        if not is_matching_location(loc):
            continue
        matches.append({
            'company': org.capitalize(),
            'title': title,
            'location': loc or 'Remote',
            'url': j.get('absolute_url') or f"https://boards.greenhouse.io/{org}/jobs/{j.get('id')}",
            'source': 'Greenhouse ATS',
            'department': j.get('departments', [{}])[0].get('name', '') if j.get('departments') else ''
        })
    return matches

# 3. Top remote companies on Lever
LEVER_ORGS = [
    'postman', 'sourcegraph', 'buffer', 'canonical', 'duckduckgo', 'atlassian',
    'affirm', 'deliveroo', 'kraken'
]

def check_lever_org(org):
    url = f"https://api.lever.co/v0/postings/{org}?mode=json"
    data = fetch_json(url)
    if not data or not isinstance(data, list):
        return []
    matches = []
    for j in data:
        title = j.get('text', '')
        cats = j.get('categories', {})
        loc = cats.get('location', '') or cats.get('workplaceType', '')
        if not is_matching_role(title):
            continue
        if not is_matching_location(loc):
            continue
        matches.append({
            'company': org.capitalize(),
            'title': title,
            'location': loc or 'Remote',
            'url': j.get('hostedUrl') or f"https://jobs.lever.co/{org}/{j.get('id')}",
            'source': 'Lever ATS',
            'department': cats.get('department', '')
        })
    return matches

def search_all_concurrent():
    seen = load_seen()
    tracker = load_tracker()
    
    seen_urls = {v.get('url', '').rstrip('/') for v in seen.values() if isinstance(v, dict)}
    tracker_urls = {r.get('source', '').rstrip('/') for r in tracker if r.get('source')}
    existing_urls = seen_urls.union(tracker_urls)
    
    log(f"Starting concurrent multi-platform search across {len(ASHBY_ORGS)} Ashby orgs, {len(GH_ORGS)} Greenhouse orgs, and {len(LEVER_ORGS)} Lever orgs...")
    
    all_results = []
    with ThreadPoolExecutor(max_workers=15) as executor:
        # Ashby
        ashby_futures = executor.map(check_ashby_org, ASHBY_ORGS)
        for res in ashby_futures:
            all_results.extend(res)
            
        # Greenhouse
        gh_futures = executor.map(check_gh_org, GH_ORGS)
        for res in gh_futures:
            all_results.extend(res)
            
        # Lever
        lever_futures = executor.map(check_lever_org, LEVER_ORGS)
        for res in lever_futures:
            all_results.extend(res)
            
    log(f"Total raw matching jobs found across tier-1 platforms: {len(all_results)}")
    
    # Deduplicate against seen and tracker
    unique_new_jobs = []
    seen_keys = set()
    
    for j in all_results:
        u = j['url'].rstrip('/')
        if u in existing_urls:
            continue
        comp_key = j['company'].lower().strip()
        title_key = j['title'].lower().strip()
        k = (comp_key, title_key[:25])
        if k in seen_keys:
            continue
            
        # Check tracker similarity
        already_applied = False
        for t in tracker:
            if comp_key in t.get('company', '').lower() and (title_key in t.get('role', '').lower() or t.get('role', '').lower() in title_key):
                already_applied = True
                break
        if already_applied:
            continue
            
        seen_keys.add(k)
        existing_urls.add(u)
        
        # Scoring
        score = 80
        t_low = title_key.lower()
        if 'nextjs' in t_low or 'next.js' in t_low: score += 15
        elif 'react' in t_low: score += 12
        elif 'frontend' in t_low or 'front-end' in t_low: score += 10
        elif 'ui/ux' in t_low or 'product designer' in t_low: score += 10
        elif 'full stack' in t_low or 'fullstack' in t_low: score += 8
        
        j['fit_score'] = score
        unique_new_jobs.append(j)
        
    unique_new_jobs.sort(key=lambda x: x['fit_score'], reverse=True)
    
    log(f"\n=== Found {len(unique_new_jobs)} Unseen, High-Quality, Genuine Jobs ===")
    for i, j in enumerate(unique_new_jobs, 1):
        log(f"{i}. [{j['source']}] {j['company']} — {j['title']} (Fit: {j['fit_score']}%)")
        log(f"   Location: {j['location']} | URL: {j['url']}")
        
    Path('job_scraper/high_quality_discovered_jobs.json').write_text(json.dumps(unique_new_jobs, indent=2), encoding='utf-8')

if __name__ == '__main__':
    search_all_concurrent()
