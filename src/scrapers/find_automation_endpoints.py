import urllib.request
import re

url = 'https://cdn-static.loyalfans.com/main-6R6YP2S6.js'
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
with urllib.request.urlopen(req) as resp:
    content = resp.read().decode('utf-8', errors='ignore')

matches = set(re.findall(r'/api/v\d+/messages/[a-zA-Z0-9_\-/]+', content))
print("Endpoints /api/v*/messages/ en bundle:")
for m in sorted(matches):
    print("  ->", m)

matches_auto = set(re.findall(r'/api/v\d+/[a-zA-Z0-9_\-/]*automation[a-zA-Z0-9_\-/]*', content))
print("\nEndpoints con automation:")
for m in sorted(matches_auto):
    print("  ->", m)
