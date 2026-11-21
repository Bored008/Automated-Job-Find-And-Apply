import urllib.request
import urllib.parse
import json
import ssl
import re

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'application/json, text/plain, */*'
}

def fetch_url(url, headers=None):
    h = dict(HEADERS)
    if headers:
        h.update(headers)
    req = urllib.request.Request(url, headers=h)
    try:
        with urllib.request.urlopen(req, context=ctx, timeout=10) as resp:
            return resp.status, resp.read().decode('utf-8', errors='replace')
    except Exception as e:
        return 0, str(e)

# 1. Test micro1 jobs page
status, html = fetch_url('https://jobs.micro1.ai')
print('jobs.micro1.ai status:', status)
if status == 200:
    apis = re.findall(r'https?://[a-zA-Z0-9\.\-_/]+api[a-zA-Z0-9\.\-_/]*', html)
    print('Found API links in micro1 HTML:', set(apis)[:5])
    # check if next data is in html
    if '__NEXT_DATA__' in html:
        m = re.search(r'<script id="__NEXT_DATA__"[^>]*>(.*?)</script>', html, re.DOTALL)
        if m:
            data = json.loads(m.group(1))
            props = data.get('props', {}).get('pageProps', {})
            print('micro1 next data keys:', list(props.keys()))
            if 'jobs' in props:
                print('jobs count in pageProps:', len(props['jobs']))
            elif 'initialJobs' in props:
                print('initialJobs count:', len(props['initialJobs']))
            else:
                for k, v in props.items():
                    if isinstance(v, list):
                        print(f'List in props {k}: len {len(v)}')
                    elif isinstance(v, dict):
                        print(f'Dict in props {k}: keys {list(v.keys())[:5]}')

# 2. Test Ashby orgs
ashby_orgs = ['posthog', 'supabase', 'linear', 'resend', 'livekit', 'clerk', 'plane', 'signoz', 'perplexity', 'modal', 'cartesia']
for org in ashby_orgs:
    st, text = fetch_url(f'https://api.ashbyhq.com/posting-api/job-board/{org}')
    if st == 200:
        try:
            d = json.loads(text)
            print(f'Ashby {org}: {len(d.get("jobs", []))} jobs')
        except:
            print(f'Ashby {org}: invalid json')
    else:
        print(f'Ashby {org}: status {st}')

# 3. Test Greenhouse orgs
gh_orgs = ['vercel', 'figma', 'cloudflare', 'remote', 'gitlab', 'elastic', 'docker', 'brex', 'stripe', 'datadog']
for org in gh_orgs:
    st, text = fetch_url(f'https://boards-api.greenhouse.io/v1/boards/{org}/jobs')
    if st == 200:
        try:
            d = json.loads(text)
            print(f'Greenhouse {org}: {len(d.get("jobs", []))} jobs')
        except:
            print(f'Greenhouse {org}: invalid json')
    else:
        print(f'Greenhouse {org}: status {st}')

# 4. Test Lever orgs
lever_orgs = ['palantir', 'atlassian', 'netflix', 'spotify', 'affirm', 'leverdemo']
for org in lever_orgs:
    st, text = fetch_url(f'https://api.lever.co/v0/postings/{org}?mode=json')
    if st == 200:
        try:
            d = json.loads(text)
            print(f'Lever {org}: {len(d)} jobs')
        except:
            print(f'Lever {org}: invalid json')
    else:
        print(f'Lever {org}: status {st}')
