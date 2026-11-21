import urllib.request
import json
import ssl
from pathlib import Path

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

cookie_file = Path("tools/.unstop_cookies.txt")
cookies = cookie_file.read_text(encoding='utf-8').strip()

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    "Accept": "application/json, text/plain, */*",
    "Content-Type": "application/json",
    "Origin": "https://unstop.com",
    "Referer": "https://unstop.com/internships/full-stack-developer-nexvora-1820983",
    "Cookie": cookies
}

# Extract XSRF token from cookies
import re
xsrf_match = re.search(r'XSRF-TOKEN=([^;]+)', cookies)
if xsrf_match:
    import urllib.parse
    headers['X-XSRF-TOKEN'] = urllib.parse.unquote(xsrf_match.group(1))

opp_id = '1820983'

# 1. Test GET /api/competition/1820983/register
print("Testing GET /api/competition/1820983/register...")
try:
    req = urllib.request.Request(f"https://unstop.com/api/competition/{opp_id}/register", headers=headers, method="GET")
    with urllib.request.urlopen(req, context=ctx, timeout=8) as r:
        print(f"GET Status: {r.status}")
        print(r.read().decode('utf-8')[:500])
except urllib.error.HTTPError as e:
    print(f"GET HTTPError {e.code}: {e.read().decode('utf-8')[:500]}")
except Exception as e:
    print(f"GET Error: {e}")

# 2. Test PUT /api/competition/1820983/register
print("\nTesting PUT /api/competition/1820983/register...")
try:
    payload = json.dumps({"opportunity_id": int(opp_id)}).encode('utf-8')
    req = urllib.request.Request(f"https://unstop.com/api/competition/{opp_id}/register", data=payload, headers=headers, method="PUT")
    with urllib.request.urlopen(req, context=ctx, timeout=8) as r:
        print(f"PUT Status: {r.status}")
        print(r.read().decode('utf-8')[:500])
except urllib.error.HTTPError as e:
    print(f"PUT HTTPError {e.code}: {e.read().decode('utf-8')[:500]}")
except Exception as e:
    print(f"PUT Error: {e}")
