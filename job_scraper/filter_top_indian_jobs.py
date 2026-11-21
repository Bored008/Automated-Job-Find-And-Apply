import urllib.request
import json
import ssl

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

HEADERS = {'User-Agent': 'Mozilla/5.0'}

def get_json(url):
    try:
        req = urllib.request.Request(url, headers=HEADERS)
        with urllib.request.urlopen(req, context=ctx, timeout=5) as r:
            return json.loads(r.read().decode('utf-8', errors='replace'))
    except Exception:
        return None

results = []

# 1. Sarvam AI (Ashby)
sarvam = get_json('https://api.ashbyhq.com/posting-api/job-board/sarvam')
if sarvam:
    for j in sarvam.get('jobs', []):
        t = j.get('title', '')
        loc = j.get('location', '')
        if any(k in t.lower() for k in ['frontend', 'react', 'design', 'ui', 'ux', 'web', 'full stack', 'fullstack', 'software engineer']):
            results.append({
                'company': 'Sarvam AI',
                'title': t,
                'location': loc,
                'url': j.get('jobUrl'),
                'source': 'Ashby ATS'
            })

# 2. CRED (Lever)
cred = get_json('https://api.lever.co/v0/postings/cred?mode=json')
if cred and isinstance(cred, list):
    for j in cred:
        t = j.get('text', '')
        cats = j.get('categories', {})
        loc = cats.get('location', '')
        if any(k in t.lower() for k in ['frontend', 'react', 'design', 'ui', 'ux', 'web', 'full stack', 'fullstack', 'software engineer']):
            results.append({
                'company': 'CRED',
                'title': t,
                'location': loc,
                'url': j.get('hostedUrl'),
                'source': 'Lever ATS'
            })

# 3. Slice (Greenhouse)
slice_data = get_json('https://boards-api.greenhouse.io/v1/boards/slice/jobs')
if slice_data:
    for j in slice_data.get('jobs', []):
        t = j.get('title', '')
        loc = j.get('location', {}).get('name', '') if isinstance(j.get('location'), dict) else str(j.get('location', ''))
        if any(k in t.lower() for k in ['frontend', 'react', 'design', 'ui', 'ux', 'web', 'full stack', 'fullstack', 'software engineer']):
            results.append({
                'company': 'Slice',
                'title': t,
                'location': loc,
                'url': j.get('absolute_url'),
                'source': 'Greenhouse ATS'
            })

# 4. InMobi / Glance (Greenhouse)
inmobi = get_json('https://boards-api.greenhouse.io/v1/boards/inmobi/jobs')
if inmobi:
    for j in inmobi.get('jobs', []):
        t = j.get('title', '')
        loc = j.get('location', {}).get('name', '') if isinstance(j.get('location'), dict) else str(j.get('location', ''))
        if any(k in t.lower() for k in ['frontend', 'react', 'design', 'ui', 'ux', 'web', 'full stack', 'fullstack']):
            results.append({
                'company': 'InMobi',
                'title': t,
                'location': loc,
                'url': j.get('absolute_url'),
                'source': 'Greenhouse ATS'
            })

print(f"Total matching positions: {len(results)}")
for r in results:
    print(f"[{r['source']}] {r['company']} - {r['title']} | Loc: {r['location']} | {r['url']}")
