import sys
from pathlib import Path

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

INDEX_PATH = Path("index.html")
with open(INDEX_PATH, "r", encoding="utf-8") as f:
    text = f.read()

# 1. Update initial greeting
old_msg = """            <!-- Mensaje Inicial de Bienvenida -->
            <div class="chat-msg sam">
              <div class="chat-msg-avatar">SB</div>
              <div class="chat-msg-body">
                <div class="chat-msg-meta">
                  <strong style="color: var(--primary-light);">Sam Barton (ROXANNE Copilot)</strong>
                  <span>• Ahora</span>
                  <span class="table-badge badge-purple" style="font-size: 9px; padding: 1px 6px;">Qwen 2.5 Activo</span>
                </div>
                <div class="chat-bubble">
                  ¡Hey! Soy el copiloto activo de Sam Barton (ROXANNE). Estoy conectado en vivo con Ollama en tu PC (<code>qwen2.5:7b-instruct</code>). 
                  Escribe cualquier mensaje de prueba o pega un DM de tus fans en LoyalFans o Streamate. Si me escribes en inglés, respondo en inglés; si me escribes en español, te hablo como la Sam más pícara y directa. 🏍️✨
                </div>
              </div>
            </div>"""

new_msg = """            <!-- Mensaje Inicial de Bienvenida -->
            <div class="chat-msg sam">
              <div class="chat-msg-avatar" style="background: linear-gradient(135deg, #9333ea, #06b6d4); font-weight:bold;">RX</div>
              <div class="chat-msg-body">
                <div class="chat-msg-meta">
                  <strong style="color: var(--primary-light);">ROXANNE (Tu Asistente de Modelo Webcam)</strong>
                  <span>• Lista</span>
                  <span class="table-badge badge-purple" style="font-size: 9px; padding: 1px 6px;">Co-Piloto Activa</span>
                </div>
                <div class="chat-bubble">
                  ¡Hola Sam! Aquí estoy lista para asistirte en todo lo que necesites para tus transmisiones, responder y entrenar cómo contestar a fans en LoyalFans, Stripchat o Streamate, planear metas de sala con Lovense o armar tus dinámicas. ¿En qué trabajamos hoy? 🐺✨
                </div>
              </div>
            </div>"""

if old_msg in text:
    text = text.replace(old_msg, new_msg)
    print("Replaced initial greeting with assistant greeting.")
else:
    # Try fuzzy replace if encoding differed
    import re
    text = re.sub(r'<!-- Mensaje Inicial de Bienvenida -->\s*<div class="chat-msg sam">.*?</div>\s*</div>\s*</div>', new_msg, text, count=1, flags=re.DOTALL)
    print("Fuzzy replaced initial greeting.")

# 2. Fix image paths to relative `artifacts/`
text = text.replace('src="/artifacts/', 'src="artifacts/')
print("Updated avatar image paths to relative artifacts/.")

with open(INDEX_PATH, "w", encoding="utf-8") as f:
    f.write(text)

print("All polish saved!")
