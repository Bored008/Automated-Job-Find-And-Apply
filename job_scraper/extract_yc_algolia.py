import urllib.request
import ssl
import re
import json

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

req = urllib.request.Request('https://www.workatastartup.com/jobs', headers={'User-Agent': 'Mozilla/5.0'})
resp = urllib.request.urlopen(req, context=ctx)
html = resp.read().decode('utf-8', errors='replace')

m = re.search(r'window\.AlgoliaOpts\s*=\s*(\{.*?\});', html)
if m:
    opts = json.loads(m.group(1))
    print("AlgoliaOpts:", json.dumps(opts, indent=2))
else:
    print("Not found via regex")
