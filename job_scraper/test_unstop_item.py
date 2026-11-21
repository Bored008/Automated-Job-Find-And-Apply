import urllib.request
import ssl
import json

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE
headers = {'User-Agent': 'Mozilla/5.0'}

url = 'https://unstop.com/api/public/opportunity/search-result?opportunity=internships&searchTerm=react&per_page=2'
req = urllib.request.Request(url, headers=headers)
with urllib.request.urlopen(req, context=ctx) as r:
    d = json.loads(r.read().decode())
    items = d.get('data', {}).get('data', [])
    if items:
        print("Sample item keys:", list(items[0].keys()))
        for k in ['id', 'title', 'regn_open', 'status', 'end_date', 'public_url', 'organisation']:
            print(f"{k}: {items[0].get(k)}")
