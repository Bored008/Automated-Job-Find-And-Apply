import urllib.request
import json
import ssl

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
    'Accept': 'application/json, text/plain, */*'
}

opp_id = '1820983'
api_url = f"https://unstop.com/api/public/competition/{opp_id}"
req = urllib.request.Request(api_url, headers=HEADERS)
try:
    with urllib.request.urlopen(req, context=ctx, timeout=8) as r:
        data = json.loads(r.read().decode('utf-8'))
        comp = data.get('data', {}).get('competition', {})
        print("Nexvora details:")
        print(" Title:", comp.get('title'))
        print(" Org:", comp.get('organisation', {}).get('name') if comp.get('organisation') else 'Nexvora')
        print(" Status:", comp.get('status'))
        print(" RegOpen:", comp.get('regn_open'))
        print(" End Date:", comp.get('end_date'))
        print(" Locations:", comp.get('locations'))
except Exception as e:
    print("Nexvora error:", e)
