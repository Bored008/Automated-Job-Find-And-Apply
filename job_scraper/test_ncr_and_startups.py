import urllib.request
import json
import ssl
from concurrent.futures import ThreadPoolExecutor

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

HEADERS = {'User-Agent': 'Mozilla/5.0'}

def check_board(platform, company):
    url = ""
    if platform == 'greenhouse':
        url = f"https://boards-api.greenhouse.io/v1/boards/{company}/jobs"
    elif platform == 'lever':
        url = f"https://api.lever.co/v0/postings/{company}?mode=json"
    elif platform == 'ashby':
        url = f"https://api.ashbyhq.com/posting-api/job-board/{company}"
        
    req = urllib.request.Request(url, headers=HEADERS)
    try:
        with urllib.request.urlopen(req, context=ctx, timeout=4) as r:
            if r.status == 200:
                data = json.loads(r.read().decode('utf-8', errors='replace'))
                count = 0
                if platform == 'greenhouse':
                    count = len(data.get('jobs', []))
                elif platform == 'lever':
                    count = len(data) if isinstance(data, list) else 0
                elif platform == 'ashby':
                    count = len(data.get('jobs', []))
                return platform, company, count, data
    except Exception:
        pass
    return platform, company, 0, None

candidates = [
    # Greenhouse
    ('greenhouse', 'urbancompany'),
    ('greenhouse', 'shiprocket'),
    ('greenhouse', 'cars24'),
    ('greenhouse', 'sprinklr'),
    ('greenhouse', 'atlan'),
    ('greenhouse', 'devtron'),
    ('greenhouse', 'dyte'),
    ('greenhouse', 'harness'),
    ('greenhouse', 'groww'),
    ('greenhouse', 'cleartax'),
    ('greenhouse', 'browserstack'),
    ('greenhouse', 'airmeet'),
    ('greenhouse', 'cred'),
    ('greenhouse', 'swiggy'),
    ('greenhouse', 'meesho'),
    ('greenhouse', 'postman'),
    ('greenhouse', 'hasura'),
    ('greenhouse', 'inmobi'),
    ('greenhouse', 'zepto'),
    ('greenhouse', 'blinkit'),
    ('greenhouse', 'zomato'),
    ('greenhouse', 'moglix'),
    ('greenhouse', 'spinny'),
    
    # Lever
    ('lever', 'urbancompany'),
    ('lever', 'shiprocket'),
    ('lever', 'cars24'),
    ('lever', 'sprinklr'),
    ('lever', 'atlan'),
    ('lever', 'devtron'),
    ('lever', 'dyte'),
    ('lever', 'harness'),
    ('lever', 'postman'),
    ('lever', 'yellowai'),
    ('lever', 'toplyne'),
    ('lever', 'kula'),
    ('lever', 'questlabs'),
    ('lever', 'crux'),
    
    # Ashby
    ('ashby', 'atlan'),
    ('ashby', 'dyte'),
    ('ashby', 'devtron'),
    ('ashby', 'questlabs'),
    ('ashby', 'crux'),
    ('ashby', 'appwrite'),
    ('ashby', 'dhiwise'),
    ('ashby', 'cursor'),
    ('ashby', 'bolt-new'),
    ('ashby', 'stackblitz'),
    ('ashby', 'supermemory'),
    ('ashby', 'agentops'),
    ('ashby', 'phidata'),
    ('ashby', 'unkey')
]

print(f"Testing {len(candidates)} company career boards...", flush=True)

active_boards = []
with ThreadPoolExecutor(max_workers=15) as ex:
    results = ex.map(lambda c: check_board(c[0], c[1]), candidates)
    for plat, comp, count, data in results:
        if count > 0:
            active_boards.append((plat, comp, count, data))
            print(f"[{plat.upper()}] {comp}: {count} jobs active", flush=True)

print(f"\nTotal active boards found: {len(active_boards)}")
