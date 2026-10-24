import sys
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

with open('index.html', encoding='utf-8') as f:
    text = f.read()

import re

perfiles_match = re.search(r'<section id="tab-perfiles".*?</section>', text, re.DOTALL)
if perfiles_match:
    print("--- TAB PERFILES PREVIEW (first 1500 chars) ---")
    print(perfiles_match.group(0)[:1500])
    print(f"\nTotal length of tab-perfiles: {len(perfiles_match.group(0))} chars")

roxanne_match = re.search(r'<section id="tab-roxanne-copilot".*?</section>', text, re.DOTALL)
if roxanne_match:
    print("\n--- TAB ROXANNE COPILOT PREVIEW (first 1500 chars) ---")
    print(roxanne_match.group(0)[:1500])
    print(f"\nTotal length of tab-roxanne: {len(roxanne_match.group(0))} chars")

# Also let's check JavaScript for roxanne chat handling
chat_js_match = re.search(r'function sendChatMessage.*?function', text, re.DOTALL)
if not chat_js_match:
    chat_js_match = re.search(r'sendChatMessage.*?(?=\n\s*function|\n\s*const|\n\s*let)', text, re.DOTALL)
if chat_js_match:
    print("\n--- CHAT JS PREVIEW ---")
    print(chat_js_match.group(0)[:1200])
