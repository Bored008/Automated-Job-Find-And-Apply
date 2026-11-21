import urllib.request
import ssl
import re
import json

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

for name, url in [
    ("Atlan", "https://jobs.ashbyhq.com/atlan/c6bb032c-6ac8-4b59-915c-d59b6f3a86f8"),
    ("ElevenLabs", "https://jobs.ashbyhq.com/ElevenLabs/e6924f60-c8cc-42b3-9d05-2442ec30e12d")
]:
    print(f"\n==================== {name} ====================")
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req, context=ctx) as r:
        html = r.read().decode('utf-8', errors='ignore')
        m = re.search(r'<script id="__NEXT_DATA__" type="application/json">(.*?)</script>', html)
        if m:
            nd = json.loads(m.group(1))
            props = nd.get('props', {}).get('pageProps', {})
            job = props.get('jobPosting', {}) or props.get('initialJobPosting', {})
            print(f"Job: {job.get('title')} | Location: {job.get('locationName')} | isListed: {job.get('isListed')}")
            form = props.get('applicationForm', {}) or job.get('applicationForm', {})
            fields = form.get('fields', [])
            print(f"Form Fields ({len(fields)}):")
            for f in fields:
                req_star = '*' if f.get('isRequired') else ''
                print(f" - {f.get('title')}{req_star} (type: {f.get('type')}, id: {f.get('id')})")
        else:
            print("No __NEXT_DATA__ found")
