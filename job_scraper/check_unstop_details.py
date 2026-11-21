import urllib.request
import json
import ssl
from bs4 import BeautifulSoup

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

jobs_to_check = [
    ("VegaStack (PeerXP)", "Junior NextJS Developer", "https://unstop.com/jobs/junior-nextjs-developer-vegastack-peerxp-1596466", "1596466"),
    ("Ekfrazo Technologies", "NextJs Developer", "https://unstop.com/jobs/nextjs-developer-ekfrazo-technologies-1496784", "1496784"),
    ("Kikbak Financial", "Frontend Developer (React.js)", "https://unstop.com/jobs/frontend-developer-reactjs-kikbak-financial-1816010", "1816010"),
    ("Persist Ventures", "Frontend Engineer", "https://unstop.com/jobs/frontend-engineer-persist-ventures-1727498", "1727498"),
    ("OhMyFood", "UI/UX & Graphic Designer", "https://unstop.com/jobs/uiux-graphic-designer-ohmyfood-1814681", "1814681"),
    ("Rexomi Technologies", "UI/UX Designer", "https://unstop.com/jobs/uiux-designer-rexomi-technologies-1782901", "1782901")
]

for comp, role, url, jid in jobs_to_check:
    api_url = f"https://unstop.com/api/public/opportunity/{jid}"
    req = urllib.request.Request(api_url, headers=HEADERS)
    try:
        with urllib.request.urlopen(req, context=ctx, timeout=5) as r:
            data = json.loads(r.read().decode('utf-8'))
            op = data.get('data', {})
            title = op.get('title')
            loc = op.get('job_location', 'Remote')
            org = op.get('organisation', {}).get('name') if op.get('organisation') else comp
            start_date = op.get('start_date')
            end_date = op.get('end_date')
            is_active = op.get('is_active')
            print(f"[{org}] {title} | Location: {loc} | Active: {is_active} | End Date: {end_date}")
    except Exception as e:
        print(f"[{comp}] Error fetching API: {e}")
