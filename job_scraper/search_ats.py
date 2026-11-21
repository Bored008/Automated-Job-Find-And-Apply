import urllib.request
import urllib.parse
import json
import ssl
import time

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'application/json, text/plain, */*'
}

def fetch_json(url, method='GET', data=None, headers=None):
    h = dict(HEADERS)
    if headers:
        h.update(headers)
    req = urllib.request.Request(url, data=data, headers=h, method=method)
    try:
        with urllib.request.urlopen(req, context=ctx, timeout=10) as resp:
            return resp.status, json.loads(resp.read().decode('utf-8'))
    except urllib.error.HTTPError as e:
        return e.code, None
    except Exception as e:
        return 0, str(e)

def test_sources():
    print("Testing Ashby:")
    status, res = fetch_json('https://api.ashbyhq.com/posting-api/job-board/posthog')
    print(f"PostHog Ashby: status {status}, {len(res.get('jobs', [])) if res else 0} jobs")

    status, res = fetch_json('https://api.ashbyhq.com/posting-api/job-board/browserbase')
    print(f"Browserbase Ashby: status {status}, {len(res.get('jobs', [])) if res else 0} jobs")

    print("\nTesting Greenhouse:")
    status, res = fetch_json('https://boards-api.greenhouse.io/v1/boards/vercel/jobs')
    print(f"Vercel Greenhouse: status {status}, {len(res.get('jobs', [])) if res else 0} jobs")

    status, res = fetch_json('https://boards-api.greenhouse.io/v1/boards/razorpay/jobs')
    print(f"Razorpay Greenhouse: status {status}, {len(res.get('jobs', [])) if res else 0} jobs")

    print("\nTesting Lever:")
    status, res = fetch_json('https://api.lever.co/v0/postings/postman?mode=json')
    print(f"Postman Lever: status {status}, {len(res) if isinstance(res, list) else 0} jobs")

    status, res = fetch_json('https://api.lever.co/v0/postings/deliveroo?mode=json')
    print(f"Deliveroo Lever: status {status}, {len(res) if isinstance(res, list) else 0} jobs")

    print("\nTesting micro1:")
    status, res = fetch_json('https://prod-api.micro1.ai/api/job-posts')
    print(f"micro1 API: status {status}, {len(res) if isinstance(res, list) else (len(res.get('data', [])) if isinstance(res, dict) else 0)} jobs")

    print("\nTesting Unstop:")
    status, res = fetch_json('https://unstop.com/api/public/opportunity/search-result?opportunity=jobs&searchTerm=frontend')
    print(f"Unstop API: status {status}, {res.get('data', {}).get('total', 0) if isinstance(res, dict) and 'data' in res else 0} jobs")

    print("\nTesting HN:")
    status, res = fetch_json('https://hn.algolia.com/api/v1/search?tags=ask_hn&query=Who+is+hiring')
    print(f"HN API: status {status}, {len(res.get('hits', [])) if isinstance(res, dict) else 0} hits")

if __name__ == '__main__':
    test_sources()
