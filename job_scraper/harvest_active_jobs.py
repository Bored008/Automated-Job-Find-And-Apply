import urllib.request
import urllib.parse
import json
import ssl
import sys
import re
import csv
from pathlib import Path

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'application/json, text/plain, */*'
}

def log(msg):
    print(msg, flush=True)

def fetch_json(url, method='GET', data=None, timeout=5):
    req = urllib.request.Request(url, data=data, headers=HEADERS, method=method)
    try:
        with urllib.request.urlopen(req, context=ctx, timeout=timeout) as resp:
            return resp.status, json.loads(resp.read().decode('utf-8', errors='replace'))
    except urllib.error.HTTPError as e:
        return e.code, None
    except Exception as e:
        return 0, None

def load_seen():
    seen_path = Path('job_scraper/seen_jobs.json')
    if seen_path.exists():
        try:
            d = json.loads(seen_path.read_text(encoding='utf-8'))
            return d.get('seen', {})
        except Exception as e:
            log(f"Error reading seen_jobs.json: {e}")
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
        except Exception as e:
            log(f"Error reading tracker: {e}")
    return tracker_entries

def is_matching_role(title):
    t = title.lower()
    positive_keywords = [
        'frontend', 'front-end', 'front end',
        'full stack', 'fullstack', 'full-stack',
        'react', 'next.js', 'nextjs',
        'ui/ux', 'ui / ux', 'ui-ux', 'ui designer', 'ux designer', 'product designer',
        'web designer', 'design engineer', 'ui engineer'
    ]
    negative_keywords = [
        'sales', 'recruiter', 'marketing', 'legal', 'accounting', 'devops',
        'ios', 'android', 'hardware', 'embedded', 'staff security', 'director', 'vp'
    ]
    if any(neg in t for neg in negative_keywords):
        return False
    return any(pos in t for pos in positive_keywords)

def is_matching_location(loc_str):
    if not loc_str:
        return True # Many remote jobs have empty location or specify in title
    l = loc_str.lower()
    allowed = ['remote', 'india', 'delhi', 'ncr', 'gurugram', 'gurgaon', 'noida', 'sonipat', 'haryana', 'anywhere']
    prohibited = [
        'united states only', 'us only', 'usa only', 'us / canada only',
        'london only', 'uk only', 'san francisco only', 'new york only',
        'germany only', 'berlin', 'paris', 'sydney', 'bangalore only', 'bengaluru only',
        'mumbai only', 'pune only', 'hyderabad only', 'chennai only'
    ]
    if any(prohib in l for prohib in prohibited):
        return False
    return any(allow in l for allow in allowed)

def search_ashby():
    log("\n=== Searching Ashby ATS ===")
    orgs = [
        'supabase', 'posthog', 'linear', 'resend', 'livekit', 'clerk', 'plane',
        'signoz', 'perplexity', 'modal', 'cartesia', 'quarry', 'langfuse', 'tldraw',
        'cursor', 'anysphere', 'bolt-new', 'stackblitz'
    ]
    matches = []
    for org in orgs:
        url = f"https://api.ashbyhq.com/posting-api/job-board/{org}"
        status, data = fetch_json(url, timeout=5)
        if status != 200 or not data:
            continue
        jobs = data.get('jobs', [])
        for j in jobs:
            title = j.get('title', '')
            is_listed = j.get('isListed', True)
            loc = j.get('location', '')
            job_id = j.get('id', '')
            job_url = j.get('jobUrl') or f"https://jobs.ashbyhq.com/{org}/{job_id}"
            
            if not is_listed:
                continue
            if not is_matching_role(title):
                continue
            if not is_matching_location(loc):
                continue
                
            matches.append({
                'source': 'Ashby',
                'company': org.capitalize(),
                'title': title,
                'location': loc,
                'url': job_url,
                'id': job_id,
                'isListed': is_listed,
                'department': j.get('department', '')
            })
    log(f"Found {len(matches)} Ashby matches matching criteria")
    return matches

def search_greenhouse():
    log("\n=== Searching Greenhouse ATS ===")
    orgs = [
        'vercel', 'figma', 'cloudflare', 'remote', 'gitlab', 'docker', 'elastic',
        'brex', 'automattic', 'stripe', 'datadog', 'razorpay', 'airbnb'
    ]
    matches = []
    for org in orgs:
        url = f"https://boards-api.greenhouse.io/v1/boards/{org}/jobs"
        status, data = fetch_json(url, timeout=5)
        if status != 200 or not data:
            continue
        jobs = data.get('jobs', [])
        for j in jobs:
            title = j.get('title', '')
            loc = j.get('location', {}).get('name', '') if isinstance(j.get('location'), dict) else str(j.get('location', ''))
            job_id = str(j.get('id', ''))
            job_url = j.get('absolute_url') or f"https://boards.greenhouse.io/{org}/jobs/{job_id}"
            
            if not is_matching_role(title):
                continue
            if not is_matching_location(loc):
                continue
                
            matches.append({
                'source': 'Greenhouse',
                'company': org.capitalize(),
                'title': title,
                'location': loc,
                'url': job_url,
                'id': job_id,
                'isListed': True,
                'department': j.get('departments', [{}])[0].get('name', '') if j.get('departments') else ''
            })
    log(f"Found {len(matches)} Greenhouse matches matching criteria")
    return matches

def search_lever():
    log("\n=== Searching Lever ATS ===")
    orgs = ['palantir', 'atlassian', 'netflix', 'spotify', 'affirm', 'leverdemo']
    matches = []
    for org in orgs:
        url = f"https://api.lever.co/v0/postings/{org}?mode=json"
        status, data = fetch_json(url, timeout=5)
        if status != 200 or not data or not isinstance(data, list):
            continue
        for j in data:
            title = j.get('text', '')
            cats = j.get('categories', {})
            loc = cats.get('location', '') or cats.get('workplaceType', '')
            job_id = j.get('id', '')
            job_url = j.get('hostedUrl') or f"https://jobs.lever.co/{org}/{job_id}"
            
            if not is_matching_role(title):
                continue
            if not is_matching_location(loc):
                continue
                
            matches.append({
                'source': 'Lever',
                'company': org.capitalize(),
                'title': title,
                'location': loc,
                'url': job_url,
                'id': job_id,
                'isListed': True,
                'department': cats.get('department', '')
            })
    log(f"Found {len(matches)} Lever matches matching criteria")
    return matches

def search_unstop():
    log("\n=== Searching Unstop Opportunities ===")
    terms = ['frontend', 'react', 'ui-ux', 'nextjs']
    matches = []
    seen_unstop_ids = set()
    for t in terms:
        url = f"https://unstop.com/api/public/opportunity/search-result?opportunity=jobs&searchTerm={t}&per_page=15"
        status, data = fetch_json(url, timeout=6)
        if status != 200 or not data or 'data' not in data:
            continue
        opps = data.get('data', {}).get('data', [])
        for op in opps:
            op_id = op.get('id')
            if op_id in seen_unstop_ids:
                continue
            seen_unstop_ids.add(op_id)
            title = op.get('title', '')
            org = op.get('organisation', {}).get('name', 'Unstop Partner') if isinstance(op.get('organisation'), dict) else 'Unstop Partner'
            loc = op.get('job_location', '') or 'India / Remote'
            slug = op.get('seo_url', '')
            op_url = f"https://unstop.com/o/{slug}" if slug else f"https://unstop.com/jobs/{op_id}"
            
            if not is_matching_role(title):
                continue
            if not is_matching_location(loc):
                continue
                
            matches.append({
                'source': 'Unstop',
                'company': org,
                'title': title,
                'location': loc,
                'url': op_url,
                'id': str(op_id),
                'isListed': True,
                'department': 'Engineering/Design'
            })
    log(f"Found {len(matches)} Unstop matches matching criteria")
    return matches

def search_hn():
    log("\n=== Searching Hacker News Who is Hiring ===")
    url = "https://hn.algolia.com/api/v1/search?tags=ask_hn&query=Who+is+hiring&hitsPerPage=1"
    status, data = fetch_json(url, timeout=5)
    matches = []
    if status == 200 and data and 'hits' in data and data['hits']:
        story_id = data['hits'][0].get('objectID')
        log(f"Latest 'Who is hiring' thread ID: {story_id} ({data['hits'][0].get('title')})")
        # Search comments in this story
        com_url = f"https://hn.algolia.com/api/v1/search?tags=comment,story_{story_id}&query=frontend+OR+react+OR+remote&hitsPerPage=20"
        st_com, d_com = fetch_json(com_url, timeout=5)
        if st_com == 200 and d_com:
            for c in d_com.get('hits', []):
                text = c.get('comment_text', '')
                if not text:
                    continue
                # Simple extraction of company and role
                first_line = text.split('\n')[0].replace('<p>', '').replace('</p>', '')
                c_id = c.get('objectID')
                c_url = f"https://news.ycombinator.com/item?id={c_id}"
                if ('remote' in text.lower() or 'india' in text.lower()) and ('react' in text.lower() or 'frontend' in text.lower() or 'full stack' in text.lower()):
                    matches.append({
                        'source': 'Hacker News',
                        'company': first_line[:40],
                        'title': 'Frontend / Full Stack Engineer',
                        'location': 'Remote',
                        'url': c_url,
                        'id': c_id,
                        'isListed': True,
                        'department': 'Engineering'
                    })
    log(f"Found {len(matches)} Hacker News matches matching criteria")
    return matches

def main():
    seen = load_seen()
    tracker = load_tracker()
    
    seen_urls = {v.get('url', '').rstrip('/') for v in seen.values() if isinstance(v, dict)}
    tracker_urls = {r.get('source', '').rstrip('/') for r in tracker if r.get('source')}
    all_seen_urls = seen_urls.union(tracker_urls)
    
    log(f"Total existing seen/tracked URLs: {len(all_seen_urls)}")
    
    all_matches = []
    all_matches.extend(search_ashby())
    all_matches.extend(search_greenhouse())
    all_matches.extend(search_lever())
    all_matches.extend(search_unstop())
    all_matches.extend(search_hn())
    
    log(f"\nTotal raw discovered opportunities: {len(all_matches)}")
    
    # Filter against seen and tracker
    new_jobs = []
    for job in all_matches:
        u = job['url'].rstrip('/')
        if u in all_seen_urls:
            continue
        # Also check company + title similarity in tracker
        comp_norm = job['company'].lower().strip()
        title_norm = job['title'].lower().strip()
        already_applied = False
        for t in tracker:
            if comp_norm in t.get('company', '').lower() and (title_norm in t.get('role', '').lower() or t.get('role', '').lower() in title_norm):
                already_applied = True
                break
        if already_applied:
            continue
            
        new_jobs.append(job)
        all_seen_urls.add(u)
        
    log(f"\n=== New Unseen, Verified Active Positions: {len(new_jobs)} ===")
    for i, j in enumerate(new_jobs, 1):
        log(f"{i}. [{j['source']}] {j['company']} — {j['title']} ({j['location']})")
        log(f"   URL: {j['url']}")
        
    # Save output to JSON for subsequent application processing
    output_path = Path('job_scraper/new_discovered_jobs.json')
    output_path.write_text(json.dumps(new_jobs, indent=2), encoding='utf-8')
    log(f"\nSaved new jobs to {output_path}")

if __name__ == '__main__':
    main()
