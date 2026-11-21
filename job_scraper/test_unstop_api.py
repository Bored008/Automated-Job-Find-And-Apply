import urllib.request
import ssl
import re

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}

url = 'https://unstop.com/internships/full-stack-developer-internship-zenotalent-1791205'
req = urllib.request.Request(url, headers=headers)
with urllib.request.urlopen(req, context=ctx) as r:
    html = r.read().decode('utf-8', errors='ignore')
    for idx, s in enumerate(re.findall(r'<script[^>]*>(.*?)</script>', html, re.DOTALL)):
        print(f"--- Script {idx} ({len(s)} chars) ---")
        print(s[:300].strip())
