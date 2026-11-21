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

# 1. Atlan
atlan_data = get_json('https://api.ashbyhq.com/posting-api/job-board/atlan')
if atlan_data:
    for j in atlan_data.get('jobs', []):
        print(f"Atlan: {j.get('title')} | Loc: {j.get('location')} | URL: {j.get('jobUrl')}")

# 2. Crux
crux_data = get_json('https://api.ashbyhq.com/posting-api/job-board/crux')
if crux_data:
    for j in crux_data.get('jobs', []):
        t = j.get('title', '')
        if any(k in t.lower() for k in ['frontend', 'react', 'design', 'full', 'software', 'ui', 'ux']):
            print(f"Crux: {t} | Loc: {j.get('location')} | URL: {j.get('jobUrl')}")

# 3. Cursor
cursor_data = get_json('https://api.ashbyhq.com/posting-api/job-board/cursor')
if cursor_data:
    for j in cursor_data.get('jobs', []):
        t = j.get('title', '')
        if any(k in t.lower() for k in ['frontend', 'design', 'ui', 'ux', 'product', 'web', 'full']):
            print(f"Cursor: {t} | Loc: {j.get('location')} | URL: {j.get('jobUrl')}")

# 4. Groww
groww_data = get_json('https://boards-api.greenhouse.io/v1/boards/groww/jobs')
if groww_data:
    for j in groww_data.get('jobs', []):
        print(f"Groww: {j.get('title')} | Loc: {j.get('location', {}).get('name')}")
