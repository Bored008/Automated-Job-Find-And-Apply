import urllib.request
import json
import ssl
from datetime import datetime

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

queries = ['frontend', 'react', 'nextjs', 'ui-ux']
now = datetime.fromisoformat('2026-11-21T00:00:00+05:30')

live_opportunities = []
seen_ids = set()

for q in queries:
    url = f"https://unstop.com/api/public/opportunity/search-result?opportunity=jobs&searchTerm={q}&per_page=20"
    req = urllib.request.Request(url, headers=HEADERS)
    try:
        resp = urllib.request.urlopen(req, context=ctx, timeout=8)
        data = json.loads(resp.read().decode())
        items = data.get('data', {}).get('data', [])
        for it in items:
            op_id = it.get('id')
            if op_id in seen_ids:
                continue
            seen_ids.add(op_id)
            
            regn_open = it.get('regn_open')
            status = it.get('status')
            end_date_str = it.get('end_date')
            
            if not regn_open or status != 'LIVE':
                continue
                
            if end_date_str:
                try:
                    # Parse end date
                    ed = datetime.fromisoformat(end_date_str)
                    if ed < now:
                        continue
                except:
                    pass
                    
            # Check locations
            locs = it.get('locations', [])
            loc_names = []
            is_ncr_or_remote = False
            if not locs:
                is_ncr_or_remote = True
                loc_names = ['Remote / All India']
            else:
                for loc_obj in locs:
                    city = (loc_obj.get('city') or '').lower()
                    state = (loc_obj.get('state') or '').lower()
                    loc_names.append(f"{loc_obj.get('city')}, {loc_obj.get('state')}")
                    if any(x in city or x in state for x in ['delhi', 'ncr', 'gurgaon', 'gurugram', 'noida', 'sonipat', 'haryana', 'remote']):
                        is_ncr_or_remote = True
                        
            if not is_ncr_or_remote:
                continue
                
            title = it.get('title')
            org = it.get('organisation', {}).get('name') if it.get('organisation') else 'Unstop Hiring Partner'
            pub_url = f"https://unstop.com/{it.get('public_url')}"
            
            live_opportunities.append({
                'id': op_id,
                'company': org,
                'title': title,
                'location': ', '.join(loc_names),
                'url': pub_url,
                'end_date': end_date_str,
                'regn_open': regn_open,
                'status': status
            })
    except Exception as e:
        print(f"Error querying {q}: {e}")

print(f"Found {len(live_opportunities)} strictly active, valid, live opportunities:")
for i, op in enumerate(live_opportunities, 1):
    print(f"{i}. [{op['company']}] {op['title']} | Loc: {op['location']} | Deadline: {op['end_date']}")
    print(f"   URL: {op['url']}")

json.dump(live_opportunities, open('job_scraper/strictly_live_unstop.json', 'w', encoding='utf-8'), indent=2)
