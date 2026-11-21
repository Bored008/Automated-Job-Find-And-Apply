import urllib.request
import ssl
import re

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

url = 'https://jobs.ashbyhq.com/atlan/c6bb032c-6ac8-4b59-915c-d59b6f3a86f8/application'
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
with urllib.request.urlopen(req, context=ctx, timeout=5) as r:
    html = r.read().decode('utf-8')

scripts = re.findall(r'src="([^"]+\.js)"', html)
print('Found scripts:', len(scripts))
for s in scripts:
    if not s.startswith('http'):
        s = 'https://jobs.ashbyhq.com' + s
    print('Checking script:', s)
    try:
        req_js = urllib.request.Request(s, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req_js, context=ctx, timeout=5) as r_js:
            js_text = r_js.read().decode('utf-8', errors='ignore')
            mutations = re.findall(r'mutation\s+([A-Za-z0-9_]+)', js_text)
            if mutations:
                print('  Found mutations in', s.split('/')[-1], ':', set(mutations))
            if 'submitApplication' in js_text:
                print('  Contains submitApplication!')
            if 'apply' in js_text.lower():
                print('  Contains apply!')
    except Exception as e:
        print('  Error reading', s, e)
