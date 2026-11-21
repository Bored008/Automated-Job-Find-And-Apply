import urllib.request
import json
import ssl

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

HEADERS = {'User-Agent': 'Mozilla/5.0'}

ashby_boards = [
    'ElevenLabs', 'dub', 'speakeasy', 'cal-com', 'mintlify', 'posthog',
    'tldraw', 'langfuse', 'modal', 'cartesia', 'unkey', 'inngest',
    'trigger-dev', 'mem0', 'llamaindex', 'vapi', 'supermemory', 'resend',
    'perplexity-ai', 'cursor', 'linear', 'raycast', 'shadcn', 'val-town'
]

print("=== Scanning Ashby Boards ===")
for b in ashby_boards:
    try:
        url = f'https://api.ashbyhq.com/posting-api/job-board/{b}'
        req = urllib.request.Request(url, headers=HEADERS)
        with urllib.request.urlopen(req, context=ctx, timeout=4) as r:
            d = json.loads(r.read().decode('utf-8'))
            for j in d.get('jobs', []):
                t = j.get('title', '').lower()
                if any(k in t for k in ['frontend', 'react', 'full stack', 'fullstack', 'designer', 'ui/ux', 'web developer']):
                    loc = j.get('location', '')
                    print(f"[{b}] {j.get('title')} | Loc: {loc} | URL: {j.get('jobUrl')}")
    except Exception:
        pass

greenhouse_boards = [
    'hasura', 'browserstack', 'postman', 'sprinklr', 'hackerrank', 'vercel',
    'cloudflare', 'notion', 'figma', 'airtable', 'zapier', 'buffer', 'slice'
]

print("\n=== Scanning Greenhouse Boards ===")
for b in greenhouse_boards:
    try:
        url = f'https://boards-api.greenhouse.io/v1/boards/{b}/jobs'
        req = urllib.request.Request(url, headers=HEADERS)
        with urllib.request.urlopen(req, context=ctx, timeout=4) as r:
            d = json.loads(r.read().decode('utf-8'))
            for j in d.get('jobs', []):
                t = j.get('title', '').lower()
                if any(k in t for k in ['frontend', 'react', 'full stack', 'fullstack', 'designer', 'ui/ux', 'web developer']):
                    loc = j.get('location', {}).get('name', '') if isinstance(j.get('location'), dict) else str(j.get('location', ''))
                    print(f"[{b}] {j.get('title')} | Loc: {loc} | ID: {j.get('id')}")
    except Exception:
        pass

lever_boards = [
    'cred', 'zerodha', 'groww', 'razorpay', 'urbancompany', 'zepto',
    'invideo', 'classplus', 'cuemath', 'unacademy', 'physicswallah',
    'loconav', 'swiggy', 'zomato'
]

print("\n=== Scanning Lever Boards ===")
for b in lever_boards:
    try:
        url = f'https://api.lever.co/v0/postings/{b}?mode=json'
        req = urllib.request.Request(url, headers=HEADERS)
        with urllib.request.urlopen(req, context=ctx, timeout=4) as r:
            d = json.loads(r.read().decode('utf-8'))
            if isinstance(d, list):
                for j in d:
                    t = j.get('text', '').lower()
                    if any(k in t for k in ['frontend', 'react', 'full stack', 'fullstack', 'designer', 'ui/ux', 'web developer']):
                        cats = j.get('categories', {})
                        loc = cats.get('location', '')
                        print(f"[{b}] {j.get('text')} | Loc: {loc} | URL: {j.get('hostedUrl')}")
    except Exception:
        pass
