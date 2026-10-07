import urllib.request
import re

def get_unsplash_info(photo_id):
    # Unsplash search API or page
    url = f'https://unsplash.com/napi/photos/{photo_id}'
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
    try:
        with urllib.request.urlopen(req) as resp:
            data = resp.read().decode('utf-8', errors='ignore')
            import json
            j = json.loads(data)
            print(f"ID: {photo_id}")
            print(f"  Description: {j.get('description')}")
            print(f"  Alt: {j.get('alt_description')}")
            tags = [t.get('title') for t in j.get('tags', [])[:5]]
            print(f"  Tags: {tags}")
    except Exception as e:
        # Fallback to page scraping
        try:
            url2 = f'https://unsplash.com/photos/{photo_id}'
            req2 = urllib.request.Request(url2, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req2) as resp2:
                html = resp2.read().decode('utf-8', errors='ignore')
                title_m = re.search(r'<title>(.*?)</title>', html)
                print(f"ID: {photo_id} (Page): {title_m.group(1) if title_m else 'No title'}")
        except Exception as e2:
            print(f"ID: {photo_id} Error: {e2}")

photos = [
    '1518709268805-4e9042af9f23', # candidate blacksmith
    '1534447677768-be436bb09401', # candidate blacksmith 2
    '1578749556568-bc2c40e68b61', # candidate pottery
    '1590736969955-71cc94801759', # candidate pottery 2
    '1562259949-e8e7689d7828', # candidate painting
    '1589939705384-5185137a7f0f'  # current painting
]

for p in photos:
    get_unsplash_info(p)
