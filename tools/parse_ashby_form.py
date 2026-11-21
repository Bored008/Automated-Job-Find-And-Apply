import urllib.request
import ssl
import re
import json

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

url = 'https://jobs.ashbyhq.com/atlan/c6bb032c-6ac8-4b59-915c-d59b6f3a86f8/application'
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
with urllib.request.urlopen(req, context=ctx, timeout=5) as r:
    html = r.read().decode('utf-8')
    m = re.search(r'<script id="__NEXT_DATA__" type="application/json">(.*?)</script>', html)
    if m:
        data = json.loads(m.group(1))
        props = data.get('props', {}).get('pageProps', {})
        print('pageProps keys:', list(props.keys()))
        app_form = props.get('applicationForm', {})
        if isinstance(app_form, dict):
            for sec in app_form.get('sections', []):
                print('Section:', sec.get('title'))
                for f in sec.get('fields', []):
                    title = f.get('title')
                    ftype = f.get('type')
                    fid = f.get('id')
                    freq = f.get('isRequired')
                    print(f"  Field: {title} | Type: {ftype} | Required: {freq} | ID: {fid}")
        else:
            print('applicationForm is:', type(app_form))
