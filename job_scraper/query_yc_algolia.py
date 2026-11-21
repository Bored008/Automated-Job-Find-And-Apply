import urllib.request
import json
import ssl

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

APP_ID = "45BWZJ1SGC"
API_KEY = "M2QzY2UwOTcxOGY0MWQzOGNhNjk5M2IxNDMyYzRhZTc0NzJmMDY1OGMwMDMxYmQ3NmFjNjExZGFiMjMxYWUwMWFuYWx5dGljc1RhZ3M9d2FhcyZyZXN0cmljdEluZGljZXM9Sm9ic1NjaG9vbF9wcm9kdWN0aW9uJTJDSm9ic0VtcGxveWVyX3Byb2R1Y3Rpb24lMkNXYWFzSGlkZUZyb21Db21wYW55X3Byb2R1Y3Rpb24lMkNXYWFTUHVibGljQ29tcGFueUpvYl9wcm9kdWN0aW9uJTJDV2FhU1B1YmxpY0NvbXBhbnlKb2JfY3JlYXRlZF9hdF9kZXNjX3Byb2R1Y3Rpb24lMkNXYWFTUHVibGljQ29tcGFueUpvYl9jb21wYW55X21vc3RfYWN0aXZlX3Byb2R1Y3Rpb24lMkNXYWFTUHVibGljQ29tcGFueUpvYl9jb21wYW55X2NyZWF0ZWRfYXRfZGVzY19wcm9kdWN0aW9uJTJDV2FhU1B1YmxpY0NvbXBhbnlKb2JfY29tcGFueV9zaXplX2FzY19wcm9kdWN0aW9uJTJDV2FhU1B1YmxpY0NvbXBhbnlKb2JfY29tcGFueV9zaXplX2Rlc2NfcHJvZHVjdGlvbiZ0YWdGaWx0ZXJzPSU1QiU1QiUyMm5vbmUlMjIlNUQlNUQmdmFsaWRVbnRpbD0xNzk1MjkwNDQ3"

index_name = "WaaSPublicCompanyJob_created_at_desc_production"
url = f"https://{APP_ID}-dsn.algolia.net/1/indexes/{index_name}/query"

headers = {
    'Content-Type': 'application/json',
    'X-Algolia-Application-Id': APP_ID,
    'X-Algolia-API-Key': API_KEY,
    'User-Agent': 'Mozilla/5.0'
}

queries = ["frontend", "react", "full stack", "designer"]

all_hits = []
seen_ids = set()

for q in queries:
    payload = json.dumps({
        "query": q,
        "hitsPerPage": 40,
        "facetFilters": [
            #["remote:true", "location_names:India", "location_names:Delhi"]
        ]
    }).encode('utf-8')
    
    req = urllib.request.Request(url, data=payload, headers=headers, method='POST')
    try:
        with urllib.request.urlopen(req, context=ctx, timeout=6) as resp:
            data = json.loads(resp.read().decode('utf-8'))
            hits = data.get('hits', [])
            print(f"Query '{q}': {len(hits)} hits found")
            for h in hits:
                jid = h.get('objectID')
                if jid not in seen_ids:
                    seen_ids.add(jid)
                    all_hits.append(h)
    except Exception as e:
        print(f"Error querying '{q}': {e}")

print(f"\nTotal unique YC jobs retrieved: {len(all_hits)}")

# Inspect sample job structure
if all_hits:
    sample = all_hits[0]
    print("\nSample keys:", list(sample.keys()))
    print("Title:", sample.get('title'))
    print("Company:", sample.get('company_name'))
    print("Locations:", sample.get('location_names'), "Remote:", sample.get('remote'))
    print("Min Exp:", sample.get('min_experience'), "Max Exp:", sample.get('max_experience'))
    print("URL slug:", sample.get('job_slug'))

json.dump(all_hits, open('job_scraper/yc_raw_hits.json', 'w', encoding='utf-8'), indent=2)
