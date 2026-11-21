import urllib.request
import json
import ssl
import re

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

req = urllib.request.Request('https://www.workatastartup.com/jobs', headers=HEADERS)
try:
    with urllib.request.urlopen(req, context=ctx, timeout=8) as r:
        html = r.read().decode('utf-8', errors='replace')
        print(f"workatastartup.com status {r.status}, length {len(html)}")
        if '__NEXT_DATA__' in html:
            m = re.search(r'<script id="__NEXT_DATA__"[^>]*>(.*?)</script>', html, re.DOTALL)
            if m:
                data = json.loads(m.group(1))
                print("Keys in Next data:", list(data.keys()))
                props = data.get('props', {}).get('pageProps', {})
                print("Keys in pageProps:", list(props.keys()))
except Exception as e:
    print("Error:", e)
