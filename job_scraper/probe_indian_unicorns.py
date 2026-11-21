import urllib.request
import json
import ssl
from concurrent.futures import ThreadPoolExecutor

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

HEADERS = {'User-Agent': 'Mozilla/5.0'}

companies = [
    'tata1mg', '1mg', 'pharmeasy', 'practo', 'cultfit', 'curefit', 'healthifyme',
    'smallcase', 'zerodha', 'groww', 'cred', 'slice', 'onecard', 'jupiter',
    'scaler', 'interviewbit', 'unacademy', 'upgrad', 'eruditus',
    'inshorts', 'dailyhunt', 'sharechat', 'loco', 'dream11', 'mpl',
    'urbancompany', 'cars24', 'spinny', 'car-dekho', 'cardekho', 'lenskart',
    'shiprocket', 'delhivery', 'shadowfax', 'porter', 'rapido',
    'sarvam', 'sarvamai', 'krutrim', 'glance', 'inmobi',
    'hasura', 'appwrite', 'dhiwise', 'yellowai', 'darwinbox',
    'browserstack', 'postman', 'sprinklr', 'cleartax'
]

def probe_company(comp):
    found = []
    # Test Greenhouse
    gh_url = f"https://boards-api.greenhouse.io/v1/boards/{comp}/jobs"
    try:
        req = urllib.request.Request(gh_url, headers=HEADERS)
        with urllib.request.urlopen(req, context=ctx, timeout=3) as r:
            if r.status == 200:
                d = json.loads(r.read().decode('utf-8', errors='replace'))
                jobs = d.get('jobs', [])
                if jobs:
                    found.append(('greenhouse', comp, len(jobs), jobs))
    except Exception:
        pass
        
    # Test Lever
    lev_url = f"https://api.lever.co/v0/postings/{comp}?mode=json"
    try:
        req = urllib.request.Request(lev_url, headers=HEADERS)
        with urllib.request.urlopen(req, context=ctx, timeout=3) as r:
            if r.status == 200:
                d = json.loads(r.read().decode('utf-8', errors='replace'))
                if isinstance(d, list) and len(d) > 0:
                    found.append(('lever', comp, len(d), d))
    except Exception:
        pass
        
    # Test Ashby
    ash_url = f"https://api.ashbyhq.com/posting-api/job-board/{comp}"
    try:
        req = urllib.request.Request(ash_url, headers=HEADERS)
        with urllib.request.urlopen(req, context=ctx, timeout=3) as r:
            if r.status == 200:
                d = json.loads(r.read().decode('utf-8', errors='replace'))
                jobs = d.get('jobs', [])
                if jobs:
                    found.append(('ashby', comp, len(jobs), jobs))
    except Exception:
        pass
        
    return found

print(f"Probing {len(companies)} top Indian tech companies...", flush=True)

all_found = []
with ThreadPoolExecutor(max_workers=20) as ex:
    results = ex.map(probe_company, companies)
    for res in results:
        for item in res:
            all_found.append(item)
            print(f"[{item[0].upper()}] {item[1]}: {item[2]} active jobs", flush=True)

print(f"\nTotal active boards discovered: {len(all_found)}")
