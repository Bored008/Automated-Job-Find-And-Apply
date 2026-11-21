import urllib.request
import json
import ssl

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

HEADERS = {'User-Agent': 'Mozilla/5.0'}

ashby_orgs = [
    'supabase', 'plane', 'signoz', 'posthog', 'linear', 'resend', 'livekit',
    'clerk', 'perplexity', 'modal', 'cartesia', 'langfuse', 'tldraw',
    'cursor', 'groq', 'scaleapi', 'together', 'character', 'retool', 'quarry',
    'sentry', 'replit', 'vapi', 'elevenlabs', 'deepgram', 'braintrust'
]

results = []

for org in ashby_orgs:
    url = f"https://api.ashbyhq.com/posting-api/job-board/{org}"
    req = urllib.request.Request(url, headers=HEADERS)
    try:
        resp = urllib.request.urlopen(req, context=ctx, timeout=4)
        data = json.loads(resp.read().decode())
        jobs = data.get('jobs', [])
        for j in jobs:
            t = j.get('title', '')
            t_lower = t.lower()
            if any(k in t_lower for k in ['frontend', 'react', 'next.js', 'ui/ux', 'product designer', 'design engineer', 'web designer']):
                loc = j.get('location', '')
                loc_lower = loc.lower()
                # Check if remote or India
                if 'india' in loc_lower or 'remote' in loc_lower or not loc:
                    results.append({
                        'company': org.capitalize(),
                        'title': t,
                        'location': loc,
                        'url': j.get('jobUrl'),
                        'publishedAt': j.get('publishedAt')
                    })
    except Exception:
        pass

print(f"Total live matching Ashby jobs across top startups: {len(results)}")
for r in results:
    print(f"[{r['company']}] {r['title']} ({r['location']}) - {r['url']}")
