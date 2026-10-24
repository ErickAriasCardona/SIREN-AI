with open('index.html', encoding='utf-8') as f:
    text = f.read()

import re
print("Length of index.html:", len(text))

# Search for sidebar items
sidebar_match = re.search(r'<div class="sidebar-menu".*?</div>\s*</div>', text, re.DOTALL)
if not sidebar_match:
    sidebar_match = re.search(r'<nav.*?</nav>', text, re.DOTALL)

if sidebar_match:
    print("Found nav:\n", sidebar_match.group(0)[:1500])
else:
    # search for sidebar
    for m in re.finditer(r'<aside id="sidebar"[^>]*>.*?</aside>', text, re.DOTALL):
        print("Found aside:\n", m.group(0)[:1500])
        break

# Search for views / tab panels
print("\n--- Views / Sections ---")
views = re.findall(r'<div[^>]*id="view-[^"]*"[^>]*>', text)
print("Views with id='view-*':", views)
sections = re.findall(r'<section[^>]*id="[^"]*"[^>]*>', text)
print("Sections with id:", sections[:10])

# Search for Roxanne / Chat
print("\n--- Roxanne chat elements ---")
for m in re.finditer(r'(id="chat-[^"]*"|id="roxanne[^"]*")', text):
    print(m.group(0))
