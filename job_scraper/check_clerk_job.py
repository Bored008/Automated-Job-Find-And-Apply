import urllib.request
import json
import ssl

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

req = urllib.request.Request(
    'https://api.ashbyhq.com/posting-api/job-board/Clerk',
    headers={'User-Agent': 'Mozilla/5.0'}
)
resp = urllib.request.urlopen(req, context=ctx)
data = json.loads(resp.read().decode())
for j in data.get('jobs', []):
    if 'product designer' in j.get('title', '').lower():
        print(json.dumps(j, indent=2))
