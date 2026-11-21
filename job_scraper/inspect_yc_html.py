import re
from bs4 import BeautifulSoup

with open('job_scraper/test_yc_startup.py') as f:
    pass

import urllib.request
import ssl

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

req = urllib.request.Request('https://www.workatastartup.com/jobs', headers={'User-Agent': 'Mozilla/5.0'})
resp = urllib.request.urlopen(req, context=ctx)
html = resp.read().decode('utf-8', errors='replace')

soup = BeautifulSoup(html, 'html.parser')
# Find scripts
scripts = soup.find_all('script')
for s in scripts:
    if s.string and ('window.gon' in s.string or 'jobs' in s.string):
        print("Found script containing jobs or gon:", s.string[:200])
        
# Find job cards or listings
job_elements = soup.find_all('div', class_=re.compile(r'job|company|listing', re.I))
print(f"Found {len(job_elements)} matching job/company elements")
