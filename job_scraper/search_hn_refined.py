import urllib.request
import json
import ssl
import re

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

HEADERS = {'User-Agent': 'Mozilla/5.0'}

def get_hn_who_is_hiring():
    # Find latest 3 "Who is hiring" threads
    url = "https://hn.algolia.com/api/v1/search?tags=ask_hn&query=Who+is+hiring&hitsPerPage=3"
    req = urllib.request.Request(url, headers=HEADERS)
    resp = urllib.request.urlopen(req, context=ctx, timeout=5)
    threads = json.loads(resp.read().decode('utf-8')).get('hits', [])
    
    matches = []
    for t in threads:
        story_id = t.get('objectID')
        thread_title = t.get('title')
        print(f"Searching thread: {thread_title} ({story_id})...")
        
        # Search comments in this story
        com_url = f"https://hn.algolia.com/api/v1/search?tags=comment,story_{story_id}&query=frontend+OR+react+OR+designer+OR+fullstack&hitsPerPage=50"
        req_com = urllib.request.Request(com_url, headers=HEADERS)
        r_com = urllib.request.urlopen(req_com, context=ctx, timeout=5)
        comments = json.loads(r_com.read().decode('utf-8')).get('hits', [])
        
        for c in comments:
            text = c.get('comment_text', '')
            t_low = text.lower()
            
            # Must be Remote or India / Delhi
            if not ('remote' in t_low or 'india' in t_low or 'delhi' in t_low):
                continue
            # Must not be US only
            if 'us only' in t_low or 'usa only' in t_low or 'must be in the us' in t_low or 'us citizens only' in t_low:
                continue
                
            # Must match tech stack
            if not ('react' in t_low or 'next.js' in t_low or 'frontend' in t_low or 'ui/ux' in t_low or 'product designer' in t_low):
                continue
                
            first_line = text.split('<p>')[0].replace('<b>', '').replace('</b>', '').strip()
            # Extract links
            urls = re.findall(r'href="([^"]+)"', text)
            clean_text = re.sub(r'<[^>]+>', ' ', text)[:300]
            
            matches.append({
                'thread': thread_title,
                'header': first_line[:60],
                'summary': clean_text,
                'links': urls[:2],
                'hn_url': f"https://news.ycombinator.com/item?id={c.get('objectID')}"
            })
            
    return matches

found = get_hn_who_is_hiring()
print(f"\nFound {len(found)} vetted HN opportunities matching criteria:")
for i, f in enumerate(found[:10], 1):
    print(f"\n{i}. {f['header']}")
    print(f"   Links: {f['links']}")
    print(f"   HN URL: {f['hn_url']}")
    print(f"   Snippet: {f['summary'][:180]}...")
