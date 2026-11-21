import urllib.request
import json
import ssl
from pathlib import Path

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
}

candidates = [
    {
        "company": "Atlan",
        "title": "AI Native Builder/Architect",
        "url": "https://jobs.ashbyhq.com/atlan/c6bb032c-6ac8-4b59-915c-d59b6f3a86f8",
        "source": "Ashby ATS",
        "portal": "ashby"
    },
    {
        "company": "ElevenLabs",
        "title": "Full-Stack Engineer (Frontend Leaning) - Studio",
        "url": "https://jobs.ashbyhq.com/ElevenLabs/e6924f60-c8cc-42b3-9d05-2442ec30e12d",
        "source": "Ashby ATS",
        "portal": "ashby"
    },
    {
        "company": "Zenotalent",
        "title": "Full Stack Developer Internship",
        "url": "https://unstop.com/internships/full-stack-developer-internship-zenotalent-1791205",
        "source": "Unstop",
        "portal": "unstop",
        "opp_id": "1791205"
    },
    {
        "company": "Mystical Views Private Limited",
        "title": "Full Stack Developer Internship",
        "url": "https://unstop.com/internships/full-stack-developer-internship-mystical-views-private-limited-1806812",
        "source": "Unstop",
        "portal": "unstop",
        "opp_id": "1806812"
    },
    {
        "company": "Webmobril Technologies",
        "title": "Full Stack Developer Internship",
        "url": "https://unstop.com/internships/full-stack-developer-internship-webmobril-technologies-1818984",
        "source": "Unstop",
        "portal": "unstop",
        "opp_id": "1818984"
    },
    {
        "company": "Accesco Living",
        "title": "Frontend and Backend Internship",
        "url": "https://unstop.com/internships/frontend-and-backend-internship-accesco-living-1804646",
        "source": "Unstop",
        "portal": "unstop",
        "opp_id": "1804646"
    },
    {
        "company": "Frontend Arena",
        "title": "Frontend Developer Internship",
        "url": "https://unstop.com/internships/frontend-developer-internship-frontend-arena-1803735",
        "source": "Unstop",
        "portal": "unstop",
        "opp_id": "1803735"
    },
    {
        "company": "Rewyoo.com",
        "title": "UI/UX Design Internship",
        "url": "https://unstop.com/internships/uiux-design-internship-rewyoocom-1806024",
        "source": "Unstop",
        "portal": "unstop",
        "opp_id": "1806024"
    }
]

print("Validating Candidate Positions...")
for c in candidates:
    if c['portal'] == 'ashby':
        req = urllib.request.Request(c['url'], headers=headers)
        try:
            with urllib.request.urlopen(req, context=ctx, timeout=6) as r:
                print(f"[Ashby] {c['company']} - {c['title']}: HTTP {r.status} (Active)")
                c['status'] = 'active' if r.status == 200 else 'inactive'
        except Exception as e:
            print(f"[Ashby] {c['company']} - {c['title']}: Error {e}")
            c['status'] = 'inactive'
    elif c['portal'] == 'unstop':
        api_url = f"https://unstop.com/api/public/opportunity/{c['opp_id']}"
        req = urllib.request.Request(api_url, headers=headers)
        try:
            with urllib.request.urlopen(req, context=ctx, timeout=6) as r:
                d = json.loads(r.read().decode('utf-8'))
                opp = d.get('data', {})
                regn_open = opp.get('regn_open')
                live_status = opp.get('status')
                end_date = opp.get('end_date')
                print(f"[Unstop] {c['company']} - {c['title']}: status={live_status}, regn_open={regn_open}, deadline={end_date}")
                if regn_open and live_status == 'LIVE':
                    c['status'] = 'active'
                else:
                    c['status'] = 'closed'
                c['deadline'] = end_date
        except Exception as e:
            print(f"[Unstop] {c['company']} - {c['title']}: Error {e}")
            c['status'] = 'error'
