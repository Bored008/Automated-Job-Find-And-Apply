import urllib.request
import urllib.parse
import json
import ssl
import csv
import sys
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'application/json, text/plain, */*'
}

def get_json(url, timeout=6):
    try:
        req = urllib.request.Request(url, headers=HEADERS)
        with urllib.request.urlopen(req, context=ctx, timeout=timeout) as r:
            if r.status == 200:
                return json.loads(r.read().decode('utf-8', errors='replace'))
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

# Negative keywords for Senior / Irrelevant roles
EXCLUDE_TITLES = [
    'senior', 'sr.', 'sr ', 'staff', 'principal', 'director', 'vp', 'head of',
    'lead', 'manager', 'architect', 'sales', 'account executive', 'recruiter',
    'marketing', 'legal', 'devops', 'sre', 'qa automation', 'telecaller',
    'customer support', 'bpo', 'business analyst', 'data analyst', 'content writer',
    'android', 'ios', 'flutter', 'react native', 'swift', 'kotlin', 'c++', 'hardware',
    'firmware', 'embedded', 'sap', 'salesforce', 'net developer', 'java developer'
]

POSITIVE_ROLES = [
    'frontend', 'front-end', 'front end',
    'react', 'next.js', 'nextjs',
    'full stack', 'fullstack', 'full-stack',
    'web developer', 'ui/ux', 'ui designer', 'ux designer',
    'product designer', 'design engineer', 'web designer'
]

EXCLUDE_LOCATIONS = [
    'us only', 'usa only', 'united states only', 'europe only', 'uk only', 'canada only',
    'germany only', 'france only', 'australia only', 'latin america only', 'emea only'
]

STRICT_ONSITE_EXCLUDE = [
    'bangalore', 'bengaluru', 'pune', 'mumbai', 'hyderabad', 'chennai', 'kolkata', 'ahmedabad'
]

NCR_KEYWORDS = [
    'remote', 'anywhere', 'work from home', 'delhi', 'ncr', 'gurgaon', 'gurugram', 'noida',
    'greater noida', 'sonipat', 'haryana', 'faridabad', 'ghaziabad', 'india'
]

def is_eligible_role(title):
    t = title.lower()
    # Check negatives
    if any(neg in t for neg in EXCLUDE_TITLES):
        return False
    # Check positives
    if not any(pos in t for pos in POSITIVE_ROLES):
        return False
    return True

def is_eligible_location(loc_str):
    if not loc_str:
        return True # Default remote / unassigned
    l = loc_str.lower()
    # Check strict foreign exclusions
    if any(ex in l for ex in EXCLUDE_LOCATIONS):
        return False
    
    # If explicitly remote or anywhere, accept unless foreign restricted
    if 'remote' in l or 'anywhere' in l or 'work from home' in l:
        return True
        
    # If it specifies an on-site Indian location outside NCR without Remote
    if any(city in l for city in STRICT_ONSITE_EXCLUDE):
        return False
        
    # Check NCR or India general
    if any(ncr in l for ncr in NCR_KEYWORDS):
        return True
        
    return False

# --- 1. Ashby ATS Boards ---
ashby_targets = [
    'atlan', 'cal-com', 'dub', 'inngest', 'trigger-dev', 'speakeasy', 'unkey',
    'mintlify', 'phidata', 'agentops', 'mem0', 'llamaindex', 'tldraw', 'langfuse',
    'cartesia', 'quarry', 'braintrust', 'vapi', 'supermemory', 'posthog', 'replit',
    'resend', 'livekit', 'modal', 'fal', 'clerk', 'supabase', 'elevenlabs',
    'perplexity-ai', 'cursor', 'linear', 'raycast', 'anysphere', 'outerbase',
    'warp', 'dust', 'cohere', 'together-ai', 'scale', 'cognition', 'midjourney',
    'sentry', 'shadcn', 'zed', 'val-town'
]

def check_ashby(org):
    url = f"https://api.ashbyhq.com/posting-api/job-board/{org}"
    d = get_json(url)
    if not d or 'jobs' not in d:
        return []
    matches = []
    for j in d.get('jobs', []):
        if not j.get('isListed', True):
            continue
        title = j.get('title', '')
        if not is_eligible_role(title):
            continue
        loc = j.get('location', '')
        if not is_eligible_location(loc):
            continue
        matches.append({
            'company': org.capitalize(),
            'title': title,
            'location': loc or 'Remote (Global)',
            'url': j.get('jobUrl') or f"https://jobs.ashbyhq.com/{org}/{j.get('id')}",
            'source': 'Ashby ATS',
            'department': j.get('departmentName', 'Engineering'),
            'compensation': j.get('compensation', {}).get('summary', '') if isinstance(j.get('compensation'), dict) else ''
        })
    return matches

# --- 2. Greenhouse ATS Boards ---
gh_targets = [
    'hasura', 'browserstack', 'postman', 'sprinklr', 'airmeet', 'cleartax',
    'hackerrank', 'vercel', 'cloudflare', 'remote', 'gitlab', 'slice',
    'figma', 'canva', 'notion', 'airtable', 'zapier', 'buffer', 'elastic',
    'datadog', 'mongodb', 'duckduckgo', 'automattic', 'canonical', 'hashicorp'
]

def check_gh(org):
    url = f"https://boards-api.greenhouse.io/v1/boards/{org}/jobs"
    d = get_json(url)
    if not d or 'jobs' not in d:
        return []
    matches = []
    for j in d.get('jobs', []):
        title = j.get('title', '')
        if not is_eligible_role(title):
            continue
        loc = j.get('location', {}).get('name', '') if isinstance(j.get('location'), dict) else str(j.get('location', ''))
        if not is_eligible_location(loc):
            continue
        matches.append({
            'company': org.capitalize(),
            'title': title,
            'location': loc or 'Remote',
            'url': j.get('absolute_url') or f"https://boards.greenhouse.io/{org}/jobs/{j.get('id')}",
            'source': 'Greenhouse ATS',
            'department': 'Engineering'
        })
    return matches

# --- 3. Lever ATS Boards ---
lever_targets = [
    'cred', 'zerodha', 'groww', 'razorpay', 'urbancompany', 'zepto',
    'invideo', 'classplus', 'cuemath', 'unacademy', 'physicswallah',
    'loconav', 'plaid', 'kraken', 'swiggy', 'zomato'
]

def check_lever(org):
    url = f"https://api.lever.co/v0/postings/{org}?mode=json"
    d = get_json(url)
    if not d or not isinstance(d, list):
        return []
    matches = []
    for j in d:
        title = j.get('text', '')
        if not is_eligible_role(title):
            continue
        cats = j.get('categories', {})
        loc = cats.get('location', '') or (cats.get('allLocations', [''])[0] if cats.get('allLocations') else '')
        if not is_eligible_location(loc):
            continue
        matches.append({
            'company': org.upper() if len(org) <= 4 else org.capitalize(),
            'title': title,
            'location': loc or 'Remote',
            'url': j.get('hostedUrl') or f"https://jobs.lever.co/{org}/{j.get('id')}",
            'source': 'Lever ATS',
            'department': cats.get('team', 'Engineering')
        })
    return matches

# --- 4. Unstop Jobs API ---
def check_unstop():
    now = datetime.fromisoformat('2026-11-21T00:00:00+05:30')
    search_queries = ['frontend', 'react', 'nextjs', 'ui-ux', 'ui designer', 'full stack', 'web development']
    matches = []
    seen_ids = set()
    for q in search_queries:
        url = f"https://unstop.com/api/public/opportunity/search-result?opportunity=jobs&searchTerm={urllib.parse.quote(q)}&per_page=25"
        d = get_json(url)
        if not d or 'data' not in d:
            continue
        items = d.get('data', {}).get('data', [])
        for it in items:
            op_id = it.get('id')
            if op_id in seen_ids:
                continue
            seen_ids.add(op_id)
            if not it.get('regn_open') or it.get('status') != 'LIVE':
                continue
            end_date_str = it.get('end_date')
            if end_date_str:
                try:
                    ed = datetime.fromisoformat(end_date_str)
                    if ed < now:
                        continue
                except Exception:
                    pass
            title = it.get('title', '')
            if not is_eligible_role(title):
                continue
            locs = it.get('locations', [])
            is_valid_loc = False
            loc_str = "Remote"
            if not locs:
                is_valid_loc = True
                loc_str = "Remote (All India)"
            else:
                loc_names = []
                for l in locs:
                    city = (l.get('city') or '').lower()
                    state = (l.get('state') or '').lower()
                    loc_names.append(f"{l.get('city')}, {l.get('state')}")
                    if is_eligible_location(f"{city} {state}"):
                        is_valid_loc = True
                loc_str = ", ".join(loc_names)
                
            if not is_valid_loc:
                continue
                
            org = it.get('organisation', {}).get('name') if it.get('organisation') else 'Unstop Hiring Partner'
            matches.append({
                'company': org,
                'title': title,
                'location': loc_str,
                'url': f"https://unstop.com/{it.get('public_url')}",
                'source': 'Unstop Jobs',
                'deadline': end_date_str
            })
    return matches

# --- 5. Remotive Remote Jobs ---
def check_remotive():
    urls = [
        'https://remotive.com/api/remote-jobs?category=software-dev&limit=40',
        'https://remotive.com/api/remote-jobs?category=design&limit=25'
    ]
    matches = []
    for u in urls:
        d = get_json(u)
        if not d or 'jobs' not in d:
            continue
        for j in d.get('jobs', []):
            title = j.get('title', '')
            if not is_eligible_role(title):
                continue
            geo = j.get('candidate_required_location', '')
            if not is_eligible_location(geo):
                continue
            matches.append({
                'company': j.get('company_name', 'Tech Startup'),
                'title': title,
                'location': geo or 'Worldwide Remote',
                'url': j.get('url'),
                'source': 'Remotive Remote',
                'compensation': j.get('salary', '')
            })
    return matches

# --- 6. Jobicy Remote Jobs ---
def check_jobicy():
    url = 'https://jobicy.com/api/v2/remote-jobs?count=50'
    d = get_json(url)
    if not d or 'jobs' not in d:
        return []
    matches = []
    for j in d.get('jobs', []):
        title = j.get('jobTitle', '')
        if not is_eligible_role(title):
            continue
        geo = j.get('jobGeo', '')
        if not is_eligible_location(geo):
            continue
        matches.append({
            'company': j.get('companyName', 'Remote Tech'),
            'title': title,
            'location': geo or 'Worldwide Remote',
            'url': j.get('url'),
            'source': 'Jobicy Remote'
        })
    return matches

def main():
    print("=================================================================", flush=True)
    print("  Deep Concurrent Search for Genuine, High-Quality Positions", flush=True)
    print("  Candidate: Himanshu Dahiya | Roles: Frontend, React, UI/UX, Full Stack", flush=True)
    print("  Strict Location: Remote or Delhi NCR / Sonipat Only", flush=True)
    print("=================================================================", flush=True)
    
    all_raw = []
    
    with ThreadPoolExecutor(max_workers=25) as ex:
        print("[1/6] Querying Ashby ATS Boards...", flush=True)
        ashby_res = list(ex.map(check_ashby, ashby_targets))
        for r in ashby_res:
            all_raw.extend(r)
            
        print("[2/6] Querying Greenhouse ATS Boards...", flush=True)
        gh_res = list(ex.map(check_gh, gh_targets))
        for r in gh_res:
            all_raw.extend(r)
            
        print("[3/6] Querying Lever ATS Boards...", flush=True)
        lever_res = list(ex.map(check_lever, lever_targets))
        for r in lever_res:
            all_raw.extend(r)
            
    print("[4/6] Querying Unstop Verified Live Jobs...", flush=True)
    all_raw.extend(check_unstop())
    
    print("[5/6] Querying Remotive Remote API...", flush=True)
    all_raw.extend(check_remotive())
    
    print("[6/6] Querying Jobicy Remote API...", flush=True)
    all_raw.extend(check_jobicy())
    
    print(f"\nTotal raw matches retrieved: {len(all_raw)}", flush=True)
    
    # Deduplicate against tracker and seen
    seen = load_seen()
    tracker = load_tracker()
    
    existing_urls = set()
    for v in seen.values():
        if isinstance(v, dict) and v.get('url'):
            existing_urls.add(v.get('url').rstrip('/'))
    for t in tracker:
        if t.get('source'):
            existing_urls.add(t['source'].rstrip('/'))
            
    filtered = []
    seen_unique = set()
    
    for j in all_raw:
        u = j['url'].rstrip('/')
        if u in existing_urls:
            continue
        comp_norm = j['company'].lower().strip()
        title_norm = j['title'].lower().strip()
        pair_key = (comp_norm, title_norm)
        if pair_key in seen_unique:
            continue
            
        already_tracked = False
        for t in tracker:
            t_comp = t.get('company', '').lower().strip()
            t_role = t.get('role', '').lower().strip()
            if comp_norm in t_comp and (title_norm in t_role or t_role in title_norm):
                already_tracked = True
                break
        if already_tracked:
            continue
            
        seen_unique.add(pair_key)
        existing_urls.add(u)
        
        # Calculate fit rating (85-98) based on direct keywords
        score = 88
        t_low = title_norm
        if 'react' in t_low:
            score += 4
        if 'frontend' in t_low or 'front-end' in t_low:
            score += 3
        if 'next.js' in t_low or 'nextjs' in t_low:
            score += 4
        if 'ui/ux' in t_low or 'product designer' in t_low or 'design engineer' in t_low:
            score += 4
        if 'remote' in j['location'].lower():
            score += 2
        score = min(score, 98)
        
        j['fit_rating'] = score
        filtered.append(j)
        
    filtered.sort(key=lambda x: x['fit_rating'], reverse=True)
    
    print(f"\n=================================================================", flush=True)
    print(f"  Vetted Genuine Opportunities (Total: {len(filtered)})", flush=True)
    print(f"=================================================================", flush=True)
    
    for idx, job in enumerate(filtered, 1):
        print(f"\n{idx}. [{job['source']}] {job['company']} — {job['title']} (Fit: {job['fit_rating']}%)")
        print(f"   Location: {job['location']}")
        print(f"   URL: {job['url']}")
        if job.get('deadline'):
            print(f"   Deadline: {job['deadline']}")
        if job.get('compensation'):
            print(f"   Compensation: {job['compensation']}")
            
    out_file = Path('job_scraper/vetted_genuine_jobs.json')
    out_file.write_text(json.dumps(filtered, indent=2, ensure_ascii=False), encoding='utf-8')
    print(f"\nResults successfully saved to {out_file}", flush=True)

if __name__ == '__main__':
    main()
