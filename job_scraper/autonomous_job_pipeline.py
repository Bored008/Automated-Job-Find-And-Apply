import urllib.request
import urllib.parse
import json
import ssl
import csv
import sys
import re
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

TRACKER_CSV = Path("job_search_tracker.csv")
SEEN_JSON = Path("job_scraper/seen_jobs.json")

# Candidate profile details
CANDIDATE = {
    "first_name": "Himanshu",
    "last_name": "Dahiya",
    "full_name": "Himanshu Dahiya",
    "email": "dahiyahimanshu80@gmail.com",
    "phone": "+91 9671757885",
    "raw_phone": "9671757885",
    "location": "Sonipat, Haryana, India",
    "city": "Sonipat",
    "state": "Haryana",
    "country": "India",
    "college": "Deenbandhu Chhotu Ram University of Science and Technology (DCRUST), Murthal, Sonipat",
    "degree": "B.Tech ECE (2024-2028)",
    "employer": "Softech Media",
    "designation": "Software Engineer Intern",
    "experience": "1 year",
    "linkedin": "https://www.linkedin.com/in/himanshuakabored/",
    "github": "https://github.com/Himanshu-Dahiya-24",
    "portfolio": "https://himanshudahiya.vercel.app/",
    "resume": "c:/Project/ai-job-search/cv/Himanshu_Dahiya_Resume.pdf"
}

def log(msg):
    print(f"[Pipeline] {msg}", flush=True)

def fetch_json(url, method='GET', data=None, timeout=6):
    req = urllib.request.Request(url, data=data, headers=HEADERS, method=method)
    try:
        with urllib.request.urlopen(req, context=ctx, timeout=timeout) as resp:
            if resp.status == 200:
                return resp.status, json.loads(resp.read().decode('utf-8', errors='replace'))
    except Exception as e:
        return 0, None
    return 0, None

def load_seen():
    if SEEN_JSON.exists():
        try:
            d = json.loads(SEEN_JSON.read_text(encoding='utf-8'))
            return d.get('seen', {})
        except Exception:
            pass
    return {}

def load_tracker():
    tracker_entries = []
    if TRACKER_CSV.exists():
        try:
            with open(TRACKER_CSV, mode='r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for r in reader:
                    tracker_entries.append(r)
        except Exception:
            pass
    return tracker_entries

EXCLUDE_TITLES = [
    'senior', 'sr.', 'sr ', 'staff', 'principal', 'director', 'vp', 'head of',
    'lead', 'manager', 'architect', 'sales', 'account executive', 'recruiter',
    'marketing', 'legal', 'devops', 'sre', 'qa automation', 'telecaller',
    'customer support', 'bpo', 'business analyst', 'data analyst', 'content writer',
    'android', 'ios', 'flutter', 'react native', 'swift', 'kotlin', 'c++', 'hardware',
    'firmware', 'embedded', 'sap', 'salesforce', '.net', 'java developer'
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
    if any(neg in t for neg in EXCLUDE_TITLES):
        return False
    return any(pos in t for pos in POSITIVE_ROLES)

def is_eligible_location(loc_str):
    if not loc_str:
        return True
    l = loc_str.lower()
    if any(ex in l for ex in EXCLUDE_LOCATIONS):
        return False
    if 'remote' in l or 'anywhere' in l or 'work from home' in l:
        return True
    if any(city in l for city in STRICT_ONSITE_EXCLUDE):
        return False
    return any(ncr in l for ncr in NCR_KEYWORDS)

# 1. Ashby ATS
ashby_orgs = [
    'atlan', 'elevenlabs', 'cal-com', 'dub', 'inngest', 'trigger-dev', 'speakeasy', 'unkey',
    'mintlify', 'phidata', 'agentops', 'mem0', 'llamaindex', 'tldraw', 'langfuse',
    'cartesia', 'quarry', 'braintrust', 'vapi', 'supermemory', 'posthog', 'replit',
    'resend', 'livekit', 'modal', 'fal', 'clerk', 'supabase',
    'perplexity-ai', 'cursor', 'linear', 'raycast', 'anysphere', 'outerbase',
    'warp', 'dust', 'cohere', 'together-ai', 'scale', 'cognition',
    'sentry', 'shadcn', 'zed', 'val-town'
]

def search_ashby(org):
    url = f"https://api.ashbyhq.com/posting-api/job-board/{org}"
    status, d = fetch_json(url)
    if status != 200 or not d or 'jobs' not in d:
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
            'deadline': None
        })
    return matches

# 2. Greenhouse ATS
gh_orgs = [
    'hasura', 'browserstack', 'postman', 'sprinklr', 'airmeet', 'cleartax',
    'hackerrank', 'vercel', 'cloudflare', 'remote', 'gitlab', 'slice',
    'figma', 'canva', 'notion', 'airtable', 'zapier', 'buffer', 'elastic',
    'datadog', 'mongodb', 'duckduckgo', 'automattic', 'canonical', 'hashicorp'
]

def search_greenhouse(org):
    url = f"https://boards-api.greenhouse.io/v1/boards/{org}/jobs"
    status, d = fetch_json(url)
    if status != 200 or not d or 'jobs' not in d:
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
            'department': 'Engineering',
            'deadline': None
        })
    return matches

# 3. Lever ATS
lever_orgs = [
    'cred', 'zerodha', 'groww', 'razorpay', 'urbancompany', 'zepto',
    'invideo', 'classplus', 'cuemath', 'unacademy', 'physicswallah',
    'loconav', 'plaid', 'kraken', 'swiggy', 'zomato'
]

def search_lever(org):
    url = f"https://api.lever.co/v0/postings/{org}?mode=json"
    status, d = fetch_json(url)
    if status != 200 or not d or not isinstance(d, list):
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
            'department': cats.get('team', 'Engineering'),
            'deadline': None
        })
    return matches

# 4. Y Combinator Hacker News ("Who is hiring")
def search_hn():
    url = "https://hn.algolia.com/api/v1/search?tags=ask_hn&query=Who+is+hiring&hitsPerPage=2"
    status, d = fetch_json(url)
    if status != 200 or not d:
        return []
    threads = d.get('hits', [])
    matches = []
    for t in threads:
        story_id = t.get('objectID')
        com_url = f"https://hn.algolia.com/api/v1/search?tags=comment,story_{story_id}&query=frontend+OR+react+OR+designer+OR+fullstack&hitsPerPage=30"
        s_com, d_com = fetch_json(com_url)
        if s_com != 200 or not d_com:
            continue
        for c in d_com.get('hits', []):
            text = c.get('comment_text', '')
            t_low = text.lower()
            if not ('remote' in t_low or 'india' in t_low or 'delhi' in t_low):
                continue
            if 'us only' in t_low or 'usa only' in t_low or 'must be in the us' in t_low:
                continue
            if not ('react' in t_low or 'next.js' in t_low or 'frontend' in t_low or 'ui/ux' in t_low or 'product designer' in t_low):
                continue
            first_line = text.split('<p>')[0].replace('<b>', '').replace('</b>', '').strip()
            urls = re.findall(r'href="([^"]+)"', text)
            hn_item_url = f"https://news.ycombinator.com/item?id={c.get('objectID')}"
            company = first_line.split('|')[0].strip() if '|' in first_line else first_line[:30].strip()
            role = first_line.split('|')[1].strip() if '|' in first_line and len(first_line.split('|')) > 1 else 'Frontend / Full Stack Engineer'
            matches.append({
                'company': company or 'YC Startup',
                'title': role,
                'location': 'Remote / Flexible',
                'url': urls[0] if urls else hn_item_url,
                'source': 'YC Hacker News',
                'department': 'Engineering',
                'deadline': None
            })
    return matches

# 5. Unstop API
def search_unstop():
    now = datetime.now()
    search_terms = ['frontend', 'react', 'nextjs', 'ui-ux', 'figma designer', 'full stack']
    matches = []
    seen_ids = set()
    for term in search_terms:
        for opp_type in ['jobs', 'internships']:
            url = f"https://unstop.com/api/public/opportunity/search-result?opportunity={opp_type}&searchTerm={urllib.parse.quote(term)}&per_page=20"
            status, d = fetch_json(url)
            if status != 200 or not d or 'data' not in d:
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
                        # parse ISO deadline
                        clean_end = end_date_str.split('+')[0]
                        ed = datetime.fromisoformat(clean_end)
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
                    'source': f'Unstop ({opp_type.capitalize()})',
                    'department': 'Engineering / Design',
                    'deadline': end_date_str
                })
    return matches

def main():
    log("Starting Search across Ashby, Greenhouse, Lever, YC HN, Unstop, micro1...")
    
    seen = load_seen()
    tracker = load_tracker()
    
    existing_urls = set()
    for v in seen.values():
        if isinstance(v, dict) and v.get('url'):
            existing_urls.add(v.get('url').rstrip('/'))
    for t in tracker:
        if t.get('source'):
            existing_urls.add(t['source'].rstrip('/'))
            
    all_raw = []
    
    with ThreadPoolExecutor(max_workers=20) as ex:
        log("1. Querying Ashby ATS endpoints...")
        ashby_results = list(ex.map(search_ashby, ashby_orgs))
        for r in ashby_results:
            all_raw.extend(r)
            
        log("2. Querying Greenhouse ATS endpoints...")
        gh_results = list(ex.map(search_greenhouse, gh_orgs))
        for r in gh_results:
            all_raw.extend(r)
            
        log("3. Querying Lever ATS endpoints...")
        lever_results = list(ex.map(search_lever, lever_orgs))
        for r in lever_results:
            all_raw.extend(r)
            
    log("4. Querying Y Combinator Hacker News 'Who is hiring'...")
    all_raw.extend(search_hn())
    
    log("5. Querying Unstop active live postings...")
    all_raw.extend(search_unstop())
    
    log(f"Raw positions collected: {len(all_raw)}")
    
    # Filter against seen and tracker
    new_active_positions = []
    seen_pairs = set()
    
    for j in all_raw:
        u = j['url'].rstrip('/')
        if u in existing_urls:
            continue
        comp_norm = j['company'].lower().strip()
        title_norm = j['title'].lower().strip()
        pair_key = (comp_norm, title_norm)
        if pair_key in seen_pairs:
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
            
        seen_pairs.add(pair_key)
        existing_urls.add(u)
        
        # Scoring
        score = 88
        t_low = title_norm
        if 'react' in t_low: score += 4
        if 'frontend' in t_low or 'front-end' in t_low: score += 3
        if 'next.js' in t_low or 'nextjs' in t_low: score += 4
        if 'ui/ux' in t_low or 'figma' in t_low or 'designer' in t_low: score += 4
        if 'remote' in j['location'].lower(): score += 2
        score = min(score, 98)
        j['fit_rating'] = score
        
        new_active_positions.append(j)
        
    new_active_positions.sort(key=lambda x: x['fit_rating'], reverse=True)
    
    log(f"Total newly discovered active & eligible positions: {len(new_active_positions)}")
    for idx, p in enumerate(new_active_positions[:12], 1):
        log(f"{idx}. [{p['source']}] {p['company']} — {p['title']} ({p['location']}) [Fit: {p['fit_rating']}%]")
        log(f"   URL: {p['url']}")
        
    # Save newly discovered jobs
    out_file = Path("job_scraper/new_active_discovered.json")
    out_file.write_text(json.dumps(new_active_positions, indent=2, ensure_ascii=False), encoding='utf-8')
    log(f"Saved {len(new_active_positions)} new positions to {out_file}")

if __name__ == '__main__':
    main()
