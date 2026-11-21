import urllib.request
import json
import ssl
from bs4 import BeautifulSoup

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

urls = [
    'https://unstop.com/jobs/frontend-developer-reactjs-kikbak-financial-1816010',
    'https://unstop.com/jobs/frontend-developer-techspar-solutions-1817946',
    'https://unstop.com/jobs/uiux-graphic-designer-ohmyfood-1814681'
]

for u in urls:
    req = urllib.request.Request(u, headers=HEADERS)
    try:
        resp = urllib.request.urlopen(req, context=ctx, timeout=8)
        html = resp.read().decode('utf-8', errors='replace')
        soup = BeautifulSoup(html, 'html.parser')
        title = soup.find('title')
        print("Page Title:", title.text if title else "No title")
        # Check for form fields or requirements
        desc = soup.find('div', {'id': 'overview'}) or soup.find('section')
        if desc:
            print("Desc snippet:", desc.text[:200].replace('\n', ' '))
    except Exception as e:
        print("Error fetching", u, ":", e)
