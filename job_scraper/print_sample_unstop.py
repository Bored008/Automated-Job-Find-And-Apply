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
for it in items[:5]:
    print("---")
    print("Title:", it.get('title'))
    print("Org:", it.get('organisation', {}).get('name') if it.get('organisation') else 'None')
    print("Public URL:", it.get('public_url'))
    print("Regn open:", it.get('regn_open'))
    print("Status:", it.get('status'))
    print("End date:", it.get('end_date'))
    print("Locations:", it.get('locations'))
    print("Skills:", [s.get('name') for s in it.get('required_skills', []) if isinstance(s, dict)])
