import urllib.request
import json
import ssl

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

APP_ID = "45BWZJ1SGC"
API_KEY = "M2QzY2UwOTcxOGY0MWQzOGNhNjk5M2IxNDMyYzRhZTc0NzJmMDY1OGMwMDMxYmQ3NmFjNjExZGFiMjMxYWUwMWFuYWx5dGljc1RhZ3M9d2FhcyZyZXN0cmljdEluZGljZXM9Sm9ic1NjaG9vbF9wcm9kdWN0aW9uJTJDSm9ic0VtcGxveWVyX3Byb2R1Y3Rpb24lMkNXYWFzSGlkZUZyb21Db21wYW55X3Byb2R1Y3Rpb24lMkNXYWFTUHVibGljQ29tcGFueUpvYl9wcm9kdWN0aW9uJTJDV2FhU1B1YmxpY0NvbXBhbnlKb2JfY3JlYXRlZF9hdF9kZXNjX3Byb2R1Y3Rpb24lMkNXYWFTUHVibGljQ29tcGFueUpvYl9jb21wYW55X21vc3RfYWN0aXZlX3Byb2R1Y3Rpb24lMkNXYWFTUHVibGljQ29tcGFueUpvYl9jb21wYW55X2NyZWF0ZWRfYXRfZGVzY19wcm9kdWN0aW9uJTJDV2FhU1B1YmxpY0NvbXBhbnlKb2JfY29tcGFueV9zaXplX2FzY19wcm9kdWN0aW9uJTJDV2FhU1B1YmxpY0NvbXBhbnlKb2JfY29tcGFueV9zaXplX2Rlc2NfcHJvZHVjdGlvbiZ0YWdGaWx0ZXJzPSU1QiU1QiUyMm5vbmUlMjIlNUQlNUQmdmFsaWRVbnRpbD0xNzk1MjkwNDQ3"

headers = {
    'Content-Type': 'application/json',
    'X-Algolia-Application-Id': APP_ID,
    'X-Algolia-API-Key': API_KEY,
    'User-Agent': 'Mozilla/5.0'
}

for idx in ["WaaSPublicCompanyJob_production", "WaaSPublicCompanyJob_created_at_desc_production"]:
    url = f"https://{APP_ID}-dsn.algolia.net/1/indexes/{idx}/query"
    payload = json.dumps({"params": "query=&hitsPerPage=5"}).encode('utf-8')
    req = urllib.request.Request(url, data=payload, headers=headers, method='POST')
    try:
        with urllib.request.urlopen(req, context=ctx, timeout=5) as r:
            d = json.loads(r.read().decode())
            print(f"Index {idx}: {d.get('nbHits', 0)} total hits, returned {len(d.get('hits', []))}")
            if d.get('hits'):
                print("First hit:", d['hits'][0].get('title'), "at", d['hits'][0].get('company_name'))
    except Exception as e:
        print(f"Index {idx} error: {e}")
