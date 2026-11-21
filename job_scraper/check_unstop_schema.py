import urllib.request
import json
import ssl

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

req = urllib.request.Request(
    'https://unstop.com/api/public/opportunity/search-result?opportunity=jobs&searchTerm=react',
    headers=HEADERS
)
resp = urllib.request.urlopen(req, context=ctx)
data = json.loads(resp.read().decode())
items = data.get('data', {}).get('data', [])
if items:
    print('Keys:', list(items[0].keys()))
    print('Sample item:')
    sample = {k: items[0][k] for k in ['id', 'title', 'seo_url', 'job_location', 'organisation', 'status', 'regn_end_date', 'filters']}
    print(json.dumps(sample, indent=2))
