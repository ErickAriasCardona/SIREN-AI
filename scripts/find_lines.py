with open('index.html', encoding='utf-8') as f:
    lines = f.readlines()

for i, l in enumerate(lines):
    if 'id="tab-perfiles"' in l:
        print(f"tab-perfiles starts at line {i+1}")
    if 'id="tab-finanzas"' in l:
        print(f"tab-finanzas starts at line {i+1}")
    if 'id="tab-roxanne-copilot"' in l:
        print(f"tab-roxanne-copilot starts at line {i+1}")
    if 'function switchMainTab' in l:
        print(f"switchMainTab at line {i+1}")
    if 'function sendChatMessage' in l:
        print(f"sendChatMessage at line {i+1}")
