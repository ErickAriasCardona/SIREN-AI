with open('index.html', encoding='utf-8') as f:
    text = f.read()

pos = text.find('id="chat-messages-box"')
if pos != -1:
    line = text[:pos].count('\n') + 1
    print(f"Found id='chat-messages-box' at line {line}:")
    print(text[pos:pos+900])
