import urllib.request
import urllib.parse
import json
import ssl
from datetime import datetime
from pathlib import Path

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

now = datetime.fromisoformat('2026-11-21T00:00:00+05:30')
terms = ['frontend', 'react', 'nextjs', 'ui ux', 'full stack', 'web development', 'figma', 'web designer', 'software developer']
categories = ['jobs', 'internships']

all_unstop = []
seen_ids = set()

for cat in categories:
    for t in terms:
        for page in [1, 2, 3]:
            url = f"https://unstop.com/api/public/opportunity/search-result?opportunity={cat}&searchTerm={urllib.parse.quote(t)}&per_page=25&page={page}"
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            try:
                with urllib.request.urlopen(req, context=ctx, timeout=4) as r:
                    d = json.loads(r.read().decode('utf-8'))
                    items = d.get('data', {}).get('data', [])
                    for it in items:
                        op_id = it.get('id')
                        if op_id in seen_ids:
                            continue
                        seen_ids.add(op_id)
                        if not it.get('regn_open') or it.get('status') != 'LIVE':
                            continue
                        end_date_str = it.get('end_date')
                        if end_date_str:
                            try:
                                ed = datetime.fromisoformat(end_date_str)
                                if ed < now:
                                    continue
                            except Exception:
                                pass
                        title = it.get('title', '')
                        t_low = title.lower()
                        # Positive filter
                        if not any(k in t_low for k in ['front', 'react', 'next', 'ui', 'ux', 'web dev', 'full stack', 'design', 'software']):
                            continue
                        # Negative filter
                        if any(neg in t_low for neg in [
                            'senior', 'sr.', 'lead', 'manager', 'sales', 'telecaller', 'bpo',
                            'marketing', 'hr intern', 'human resource', 'content writer', 'civil',
                            'mechanical', 'electrical engineer', 'hardware', 'embedded', 'finance', 'accounting'
                        ]):
                            continue
                        locs = it.get('locations', [])
                        is_ncr_or_remote = False
                        loc_names = []
                        if not locs:
                            is_ncr_or_remote = True
                            loc_str = 'Remote (All India)'
                        else:
                            for l in locs:
                                city = (l.get('city') or '').lower()
                                state = (l.get('state') or '').lower()
                                loc_names.append(f"{l.get('city')}, {l.get('state')}")
                                if any(x in city or x in state for x in ['delhi', 'ncr', 'gurgaon', 'gurugram', 'noida', 'sonipat', 'haryana', 'faridabad', 'ghaziabad', 'remote']):
                                    is_ncr_or_remote = True
                            loc_str = ', '.join(loc_names)
                        if not is_ncr_or_remote:
                            continue
                        org = it.get('organisation', {}).get('name') if it.get('organisation') else 'Unstop Hiring Partner'
                        all_unstop.append({
                            'id': op_id,
                            'title': title,
                            'company': org,
                            'category': cat,
                            'location': loc_str,
                            'url': f"https://unstop.com/{it.get('public_url')}",
                            'deadline': end_date_str
                        })
            except Exception:
                pass

print(f"Total Unstop matching positions: {len(all_unstop)}")
for idx, j in enumerate(all_unstop, 1):
    cat_lbl = j['category'].upper()
    print(f"{idx}. [{cat_lbl}] {j['company']} — {j['title']}")
    print(f"   Loc: {j['location']} | Deadline: {j['deadline']}")
    print(f"   URL: {j['url']}")

Path('job_scraper/unstop_deep_results.json').write_text(json.dumps(all_unstop, indent=2), encoding='utf-8')
