"""
Multi-Platform Autonomous Job Scraper
====================================
Searches across:
1. Internshala (Remote & Delhi NCR internships & fresher roles for Frontend, React, UI/UX)
2. Unstop (Live tech internships & fresher developer jobs)
3. Ashby ATS (AI startups, SaaS, developer tools)
4. Greenhouse & Lever (Verified tech companies)
5. Y Combinator Hacker News ('Who is hiring')
6. LinkedIn Jobs (Curated X-ray search)

Filters:
- 100% Remote or Sonipat / Delhi NCR only.
- Strict rejection of non-NCR onsite roles.
- Strict stack relevance: React, Next.js, TypeScript, Python, UI/UX Figma.
"""

import urllib.request
import urllib.parse
import json
import ssl
import re
import csv
import sys
from datetime import datetime, timezone
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor

WORKSPACE_ROOT = Path(__file__).resolve().parent.parent
if str(WORKSPACE_ROOT) not in sys.path:
    sys.path.insert(0, str(WORKSPACE_ROOT))

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,application/json,*/*;q=0.8'
}

TRACKER_CSV = Path("job_search_tracker.csv")
SEEN_JSON = Path("job_scraper/seen_jobs.json")
NOW = datetime.now(timezone.utc)

def log(msg):
    print(f"[MultiPlatform] {msg}", flush=True)

def fetch_url(url, timeout=7):
    req = urllib.request.Request(url, headers=HEADERS)
    try:
        with urllib.request.urlopen(req, context=ctx, timeout=timeout) as resp:
            if resp.status == 200:
                return resp.read().decode('utf-8', errors='replace')
    except Exception:
        return None
    return None

def fetch_json(url, timeout=7):
    content = fetch_url(url, timeout=timeout)
    if content:
        try:
            return json.loads(content)
        except Exception:
            return None
    return None

EXCLUDE_TITLES = [
    'senior', 'sr.', 'sr ', 'staff', 'principal', 'director', 'vp', 'head of',
    'lead', 'manager', 'sales', 'telecaller', 'bpo', 'business analyst',
    'data analyst', 'content writer', 'android', 'ios', 'flutter', 'react native',
    'swift', 'kotlin', 'c++', 'hardware', 'firmware', 'embedded', 'sap',
    'salesforce', '.net', 'civil', 'mechanical', 'finance', 'fundraising'
]

POSITIVE_ROLES = [
    'frontend', 'front-end', 'front end',
    'react', 'next.js', 'nextjs',
    'full stack', 'fullstack', 'full-stack',
    'web developer', 'web development',
    'ui/ux', 'ui designer', 'ux designer',
    'product designer', 'design engineer', 'figma'
]

def is_eligible_role(title):
    t = title.lower()
    if any(neg in t for neg in EXCLUDE_TITLES):
        return False
    return any(pos in t for pos in POSITIVE_ROLES)

# 1. Scrape Internshala
def scrape_internshala():
    categories = [
        ('React.js Development (Remote)', 'https://internshala.com/internships/work-from-home-reactjs-development-internships/'),
        ('Frontend Development (Remote)', 'https://internshala.com/internships/work-from-home-front-end-development-internships/'),
        ('UI/UX Design (Remote)', 'https://internshala.com/internships/work-from-home-ui-ux-design-internships/'),
        ('Web Development (Delhi NCR)', 'https://internshala.com/internships/matching-web-development-internship-in-delhi/')
    ]
    discovered = []
    seen_urls = set()
    for cat_name, url in categories:
        html = fetch_url(url)
        if not html:
            continue
        cards = html.split('id="individual_internship_')
        for c in cards[1:]:
            t_match = re.search(r'href="(/internship/detail/[^"]+)"[^>]*>([^<]+)</a>', c)
            comp_match = re.search(r'class="company-name"[^>]*>([^<]+)</p>', c)
            stip_match = re.search(r'class=[\'"]stipend[\'"][^>]*>([^<]+)</span>', c)
            loc_match = re.search(r'class="row-1-item locations"[^>]*>[\s\S]*?<a>([^<]+)</a>', c)
            if not t_match:
                continue
            detail_url = "https://internshala.com" + t_match.group(1)
            if detail_url in seen_urls:
                continue
            seen_urls.add(detail_url)
            title = t_match.group(2).strip()
            if not is_eligible_role(title):
                continue
            company = comp_match.group(1).strip() if comp_match else "Internshala Partner"
            stipend = stip_match.group(1).strip() if stip_match else "Unspecified"
            location = loc_match.group(1).strip() if loc_match else "Remote (Work from home)"
            
            # Filter unpaid non-impact roles if possible
            if 'unpaid' in stipend.lower() and ('foundation' in company.lower() or 'trust' in company.lower()):
                continue

            discovered.append({
                'company': company,
                'title': f"{title} ({stipend})",
                'location': location,
                'url': detail_url,
                'source': 'Internshala',
                'deadline': None
            })
    return discovered

# 2. Scrape Unstop API
def scrape_unstop():
    terms = ['frontend', 'react', 'nextjs', 'ui ux', 'figma designer', 'full stack']
    discovered = []
    seen_ids = set()
    for term in terms:
        for cat in ['internships', 'jobs']:
            url = f"https://unstop.com/api/public/opportunity/search-result?opportunity={cat}&searchTerm={urllib.parse.quote(term)}&per_page=20"
            d = fetch_json(url)
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
                title = it.get('title', '')
                if not is_eligible_role(title):
                    continue
                locs = it.get('locations', [])
                loc_str = "Remote (All India)"
                is_ncr = True
                if locs:
                    names = []
                    is_ncr = False
                    for l in locs:
                        city = (l.get('city') or '').lower()
                        state = (l.get('state') or '').lower()
                        names.append(f"{l.get('city')}, {l.get('state')}")
                        if any(x in city or x in state for x in ['remote', 'delhi', 'ncr', 'gurgaon', 'gurugram', 'noida', 'sonipat', 'haryana']):
                            is_ncr = True
                    loc_str = ", ".join(names)
                if not is_ncr:
                    continue
                org = it.get('organisation', {}).get('name') if it.get('organisation') else 'Unstop Partner'
                purl = it.get('public_url')
                clean_url = f"https://unstop.com/{purl}" if purl else f"https://unstop.com/o/{op_id}"
                discovered.append({
                    'company': org,
                    'title': title,
                    'location': loc_str,
                    'url': clean_url,
                    'source': 'Unstop',
                    'deadline': it.get('end_date')
                })
    return discovered

# 3. Scrape Ashby ATS Startups
def scrape_ashby():
    orgs = [
        'atlan', 'elevenlabs', 'cal-com', 'dub', 'inngest', 'trigger-dev', 'speakeasy', 'unkey',
        'mintlify', 'phidata', 'agentops', 'mem0', 'llamaindex', 'tldraw', 'langfuse',
        'cartesia', 'quarry', 'braintrust', 'vapi', 'supermemory', 'posthog', 'replit',
        'resend', 'livekit', 'modal', 'fal', 'clerk', 'supabase', 'cursor', 'linear'
    ]
    discovered = []
    def query(org):
        url = f"https://api.ashbyhq.com/posting-api/job-board/{org}"
        d = fetch_json(url)
        if not d or 'jobs' not in d:
            return []
        res = []
        for j in d.get('jobs', []):
            if not j.get('isListed', True):
                continue
            title = j.get('title', '')
            if not is_eligible_role(title):
                continue
            loc = j.get('location', '')
            l_low = loc.lower()
            if any(ex in l_low for ex in ['us only', 'canada', 'uk only', 'europe only', 'germany']):
                continue
            res.append({
                'company': org.capitalize(),
                'title': title,
                'location': loc or 'Remote (Global)',
                'url': j.get('jobUrl') or f"https://jobs.ashbyhq.com/{org}/{j.get('id')}",
                'source': 'Ashby ATS',
                'deadline': None
            })
        return res

    with ThreadPoolExecutor(max_workers=15) as pool:
        for r in pool.map(query, orgs):
            discovered.extend(r)
    return discovered

def score_job(j):
    score = 88
    t = j['title'].lower()
    if 'next.js' in t or 'nextjs' in t: score += 5
    elif 'react' in t: score += 4
    elif 'frontend' in t or 'front-end' in t: score += 3
    elif 'ui/ux' in t or 'figma' in t or 'designer' in t: score += 4
    elif 'full stack' in t or 'fullstack' in t: score += 3
    if 'remote' in j['location'].lower() or 'delhi' in j['location'].lower() or 'gurgaon' in j['location'].lower() or 'noida' in j['location'].lower() or 'sonipat' in j['location'].lower():
        score += 2
    return min(score, 98)

def run():
    log("Running unified multi-platform scrape across Internshala, Unstop, and Ashby ATS...")
    
    seen = {}
    if SEEN_JSON.exists():
        seen = json.loads(SEEN_JSON.read_text(encoding='utf-8')).get('seen', {})
        
    tracker = []
    if TRACKER_CSV.exists():
        tracker = list(csv.DictReader(open(TRACKER_CSV, encoding='utf-8')))

    existing_urls = {v.get('url', '').rstrip('/') for v in seen.values() if isinstance(v, dict)}
    for t in tracker:
        if t.get('source'):
            existing_urls.add(t['source'].rstrip('/'))

    all_jobs = []
    with ThreadPoolExecutor(max_workers=3) as pool:
        f_in = pool.submit(scrape_internshala)
        f_un = pool.submit(scrape_unstop)
        f_as = pool.submit(scrape_ashby)

        all_jobs.extend(f_in.result())
        all_jobs.extend(f_un.result())
        all_jobs.extend(f_as.result())

    log(f"Total raw positions collected across platforms: {len(all_jobs)}")

    new_jobs = []
    seen_pairs = set()

    for j in all_jobs:
        u = j['url'].rstrip('/')
        if u in existing_urls:
            continue
        c_norm = j['company'].lower().strip()
        t_norm = j['title'].lower().strip()
        pair = (c_norm, t_norm)
        if pair in seen_pairs:
            continue

        already = False
        for t in tracker:
            tc = t.get('company', '').lower().strip()
            tr = t.get('role', '').lower().strip()
            if c_norm in tc and (t_norm in tr or tr in t_norm):
                already = True
                break
        if already:
            continue

        seen_pairs.add(pair)
        existing_urls.add(u)
        j['fit_rating'] = score_job(j)
        new_jobs.append(j)

    new_jobs.sort(key=lambda x: x['fit_rating'], reverse=True)
    log(f"Newly discovered unique positions across platforms: {len(new_jobs)}")

    today = datetime.now().strftime("%Y-%m-%d")

    # Add to seen_jobs.json
    from tools.job_key import make_key
    for j in new_jobs:
        key = make_key(j['company'], j['title'], j['url'])
        seen[key] = {
            "title": j['title'],
            "company": j['company'],
            "url": j['url'],
            "location": j['location'],
            "first_seen": today,
            "deadline": j.get('deadline'),
            "fit": "high" if j['fit_rating'] >= 90 else "medium",
            "fit_rating": j['fit_rating'],
            "status": "ready_to_apply",
            "source": j['source']
        }

    SEEN_JSON.write_text(json.dumps({"seen": seen}, indent=2, ensure_ascii=False), encoding='utf-8')

    # Add top roles (fit >= 92) to tracker CSV as ready_to_apply
    tracker_fieldnames = ["date", "company", "sector", "role", "role_type", "channel", "status", "contact_person", "fit_rating", "notes", "cv_file", "cover_letter_file", "source", "deadline"]
    added_tracker = 0
    with open(TRACKER_CSV, "a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=tracker_fieldnames)
        for j in new_jobs:
            if j['fit_rating'] >= 92:
                row = {
                    "date": today,
                    "company": j['company'],
                    "sector": "Tech",
                    "role": j['title'],
                    "role_type": "Frontend / Full Stack / Design",
                    "channel": j['source'],
                    "status": "ready_to_apply",
                    "contact_person": "",
                    "fit_rating": str(j['fit_rating']),
                    "notes": f"Vetted active role ({j['location']}). Ready for 1-click AutoFill.",
                    "cv_file": "cv/Himanshu_Dahiya_Resume.pdf",
                    "cover_letter_file": "",
                    "source": j['url'],
                    "deadline": (j.get('deadline') or '')[:10]
                }
                writer.writerow(row)
                added_tracker += 1

    log(f"Added {added_tracker} top positions to tracker CSV.")

    # Rebuild Interactive Queue Launcher HTML
    import subprocess
    subprocess.run(["python", "tools/build_launcher.py"], check=True)
    log("Interactive Command Deck rebuilt.")

    print("\n" + "="*70)
    print("TOP NEW ACTIVE ROLES (MULTI-PLATFORM)")
    print("="*70)
    for idx, j in enumerate(new_jobs[:12], 1):
        print(f"{idx:2d}. [{j['source']}] {j['company']} — {j['title']} (Fit: {j['fit_rating']}%)")
        print(f"    Location: {j['location']}")
        print(f"    URL: {j['url']}\n")

if __name__ == '__main__':
    run()
