import sys
import re
from pathlib import Path

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

INDEX_PATH = Path("index.html")
with open(INDEX_PATH, "r", encoding="utf-8") as f:
    html = f.read()

# 1. Update tab-roxanne-copilot title and quick prompts
old_chat_console_header = """        <!-- CONSOLA INTERACTIVA: CHAT EN VIVO CON ROXANNE COPILOT -->
        <div class="card chat-console">
          <div class="card-title" style="flex-wrap: wrap; gap: 10px;">
            <div style="display:flex; align-items:center; gap: 10px;">
              <i data-lucide="bot" style="color: var(--primary-light);"></i>
              <span>Consola en Vivo: Chat Interactivo con ROXANNE Copilot</span>
            </div>"""

new_chat_console_header = """        <!-- CONSOLA INTERACTIVA: ROXANNE ASISTENTE PERSONAL DE MODELO WEBCAM -->
        <div class="card chat-console">
          <div class="card-title" style="flex-wrap: wrap; gap: 10px;">
            <div style="display:flex; align-items:center; gap: 10px;">
              <i data-lucide="bot" style="color: var(--primary-light);"></i>
              <div>
                <span style="font-size:15px; font-weight:700;">ROXANNE — Tu Asistente Personal de Modelo Webcam</span>
                <div style="font-size:11px; color:var(--text-dim); font-weight:400;">Entrenada exclusivamente para tus transmisiones en LoyalFans, Stripchat y Streamate</div>
              </div>
            </div>"""

if old_chat_console_header in html:
    html = html.replace(old_chat_console_header, new_chat_console_header)
    print("Updated Roxanne chat console header.")

# 2. Update quick prompt pills
old_quick_prompts = """          <div class="quick-prompts-bar">
            <span style="font-size: 11px; color: var(--text-dim); display: flex; align-items: center; gap: 4px;">
              <i data-lucide="sparkles" style="width: 12px; height: 12px;"></i> Pruebas Rápidas:
            </span>
            <button class="quick-pill" onclick="useQuickPrompt('Hey Sam! Loved your bike picture, what model is it?')">Fan EN: Pregunta Moto</button>
            <button class="quick-pill" onclick="useQuickPrompt('Hola hermosa, qué rica te ves. ¿Haces videollamadas privadas?')">Fan ES: Propuesta Privado</button>
            <button class="quick-pill" onclick="useQuickPrompt('Hey what is your minimum tip for custom video?')">Fan EN: Pregunta Precios</button>
            <button class="quick-pill" onclick="useQuickPrompt('Hola reina, mándame una foto gratis para ver si compro')">Fan ES: Pide Contenido Gratis</button>
          </div>"""

new_quick_prompts = """          <div class="quick-prompts-bar">
            <span style="font-size: 11px; color: var(--text-dim); display: flex; align-items: center; gap: 4px;">
              <i data-lucide="sparkles" style="width: 12px; height: 12px;"></i> Consultas Frecuentes a tu Asistente:
            </span>
            <button class="quick-pill" onclick="useQuickPrompt('¿Cómo le respondo a un fan en Streamate que me pide descuento en show privado?')">Fan pide descuento</button>
            <button class="quick-pill" onclick="useQuickPrompt('Sugiéreme un tema de sala para hoy con @SAMBARTONN23 y metas en 3 niveles')">Tema de sala & Metas</button>
            <button class="quick-pill" onclick="useQuickPrompt('Escríbeme un mensaje de bienvenida coqueteando para nuevos seguidores en LoyalFans')">Bienvenida LoyalFans</button>
            <button class="quick-pill" onclick="useQuickPrompt('¿Qué dinámica con el ukelele y música podemos hacer en vivo?')">Dinámica Ukelele en vivo</button>
          </div>"""

if old_quick_prompts in html:
    html = html.replace(old_quick_prompts, new_quick_prompts)
    print("Updated quick prompts to assistant queries.")

# 3. Update JavaScript functions: appendChatMessage, clearCopilotChat, sendCopilotMessage, loadCopilotChatHistory, toggleVelvetTheme, togglePasswordVisibility, copyToClipboard
js_helpers = """
    // ==========================================
    // ☀️ CONTROL DE TEMA CLARO / OSCURO
    // ==========================================
    function toggleVelvetTheme() {
      const isLight = document.body.classList.toggle('light-theme');
      localStorage.setItem('velvet_theme', isLight ? 'light' : 'dark');
      updateThemeButtonUI(isLight);
      showToast(isLight ? 'Modo Claro activado' : 'Modo Oscuro activado');
    }

    function updateThemeButtonUI(isLight) {
      const icon = document.getElementById('theme-icon');
      const label = document.getElementById('theme-label');
      if (icon && label) {
        if (isLight) {
          icon.setAttribute('data-lucide', 'moon');
          label.textContent = 'Modo Oscuro';
        } else {
          icon.setAttribute('data-lucide', 'sun');
          label.textContent = 'Modo Claro';
        }
        lucide.createIcons();
      }
    }

    function initThemeFromStorage() {
      const saved = localStorage.getItem('velvet_theme');
      if (saved === 'light') {
        document.body.classList.add('light-theme');
        updateThemeButtonUI(true);
      }
    }

    // ==========================================
    // 👁️ VISUALIZADOR Y COPIADO DE CREDENCIALES
    // ==========================================
    function togglePasswordVisibility(inputId, btn) {
      const input = document.getElementById(inputId);
      if (!input) return;
      const isPassword = input.type === 'password';
      input.type = isPassword ? 'text' : 'password';
      const icon = btn.querySelector('i');
      if (icon) {
        icon.setAttribute('data-lucide', isPassword ? 'eye-off' : 'eye');
        lucide.createIcons();
      }
    }

    function copyToClipboard(text, btn) {
      navigator.clipboard.writeText(text).then(() => {
        const oldHtml = btn.innerHTML;
        btn.innerHTML = '<span style=\"color:#10b981; font-weight:700;\">✓</span>';
        showToast('Copiado al portapapeles: ' + text);
        setTimeout(() => {
          btn.innerHTML = oldHtml;
          lucide.createIcons();
        }, 1800);
      }).catch(err => {
        showToast('Error copiando: ' + err);
      });
    }

    // ==========================================
    // 💬 HISTORIAL Y CHAT PERSISTENTE CON ROXANNE
    // ==========================================
    let copilotChatHistory = [];

    async function loadCopilotChatHistory() {
      const box = document.getElementById('chat-messages-box');
      if (!box) return;

      // Intentar cargar desde el backend SQLite
      try {
        const res = await fetch('http://localhost:8888/api/chat_history');
        if (res.ok) {
          const data = await res.json();
          if (data.history && data.history.length > 0) {
            box.innerHTML = '';
            copilotChatHistory = [];
            data.history.forEach(item => {
              appendChatMessage(item.sender, item.message, 'es', item.model, item.timestamp, false);
              copilotChatHistory.push({
                role: item.sender === 'sam' ? 'user' : 'assistant',
                content: item.message
              });
            });
            box.scrollTop = box.scrollHeight;
            return;
          }
        }
      } catch (e) {
        console.log('Error conectando con endpoint de historial backend, usando localStorage:', e);
      }

      // Fallback a localStorage
      const localSaved = localStorage.getItem('velvet_roxanne_chat_history');
      if (localSaved) {
        try {
          const parsed = JSON.parse(localSaved);
          if (parsed && parsed.length > 0) {
            box.innerHTML = '';
            copilotChatHistory = [];
            parsed.forEach(item => {
              appendChatMessage(item.sender, item.message, 'es', item.model, item.timestamp, false);
              copilotChatHistory.push({
                role: item.sender === 'sam' ? 'user' : 'assistant',
                content: item.message
              });
            });
            box.scrollTop = box.scrollHeight;
            return;
          }
        } catch (e) {
          console.error('Error parseando localStorage:', e);
        }
      }

      // Mensaje de bienvenida inicial si no hay historial
      box.innerHTML = `
        <div class="chat-msg sam">
          <div class="chat-msg-avatar" style="background: linear-gradient(135deg, #9333ea, #06b6d4); font-weight:bold;">RX</div>
          <div class="chat-msg-body">
            <div class="chat-msg-meta">
              <strong style="color: var(--primary-light);">ROXANNE (Tu Asistente de Modelo Webcam)</strong>
              <span>• Lista</span>
              <span class="table-badge badge-purple" style="font-size: 9px; padding: 1px 6px;">Co-Piloto Activa</span>
            </div>
            <div class="chat-bubble">
              ¡Hola Sam! Aquí estoy lista para asistirte en todo lo que necesites para tus transmisiones, estrategias de sala, respuestas a fans en LoyalFans, Stripchat y Streamate, o configuración de juguetes Lovense. ¿En qué trabajamos hoy? 🐺✨
            </div>
          </div>
        </div>
      `;
      lucide.createIcons();
    }

    function appendChatMessage(sender, text, lang = 'es', model = '', timeStr = null, saveLocal = true) {
      const box = document.getElementById('chat-messages-box');
      if (!box) return;
      const msgDiv = document.createElement('div');
      msgDiv.className = `chat-msg ${sender === 'sam' ? 'fan' : 'sam'}`;
      
      const currentTime = timeStr || new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
      const escapedText = text.replace(/</g, "&lt;").replace(/>/g, "&gt;");

      if (sender === 'sam') {
        msgDiv.innerHTML = `
          <div class="chat-msg-avatar" style="background: #3b82f6; font-weight:bold;">SB</div>
          <div class="chat-msg-body">
            <div class="chat-msg-meta">
              <span class="table-badge badge-info" style="font-size:9px; padding:1px 6px;">Sam Barton</span>
              <span>• ${currentTime}</span>
              <strong style="color: var(--secondary);">Tú</strong>
            </div>
            <div class="chat-bubble" style="background: rgba(59, 130, 246, 0.15); border: 1px solid rgba(59, 130, 246, 0.3);">${escapedText}</div>
          </div>
        `;
      } else {
        msgDiv.innerHTML = `
          <div class="chat-msg-avatar" style="background: linear-gradient(135deg, #9333ea, #06b6d4); font-weight:bold;">RX</div>
          <div class="chat-msg-body">
            <div class="chat-msg-meta">
              <strong style="color: var(--primary-light);">ROXANNE (Tu Asistente de Modelo)</strong>
              <span>• ${currentTime}</span>
              <span class="table-badge badge-purple" style="font-size:9px; padding:1px 6px;">IA Local</span>
            </div>
            <div class="chat-bubble">
              ${escapedText}
              <div style="margin-top: 8px;">
                <button class="copy-msg-btn" onclick="copyMsgText(this)">
                  <i data-lucide="copy" style="width:10px; height:10px;"></i> Copiar respuesta lista
                </button>
              </div>
            </div>
          </div>
        `;
      }

      box.appendChild(msgDiv);
      box.scrollTop = box.scrollHeight;
      lucide.createIcons();

      if (saveLocal) {
        saveChatToLocalStorage(sender, text, currentTime, model);
      }
    }

    function saveChatToLocalStorage(sender, text, timestamp, model) {
      try {
        let history = JSON.parse(localStorage.getItem('velvet_roxanne_chat_history') || '[]');
        history.push({ sender, message: text, timestamp, model });
        if (history.length > 100) history = history.slice(-100);
        localStorage.setItem('velvet_roxanne_chat_history', JSON.stringify(history));
      } catch (e) {
        console.error('Error guardando en localStorage:', e);
      }
    }

    async function clearCopilotChat() {
      copilotChatHistory = [];
      localStorage.removeItem('velvet_roxanne_chat_history');

      try {
        await fetch('http://localhost:8888/api/clear_chat_history', { method: 'POST' });
      } catch (e) {
        console.log('Error llamando clear en backend:', e);
      }

      const box = document.getElementById('chat-messages-box');
      if (!box) return;
      box.innerHTML = `
        <div class="chat-msg sam">
          <div class="chat-msg-avatar" style="background: linear-gradient(135deg, #9333ea, #06b6d4); font-weight:bold;">RX</div>
          <div class="chat-msg-body">
            <div class="chat-msg-meta">
              <strong style="color: var(--primary-light);">ROXANNE (Tu Asistente de Modelo Webcam)</strong>
              <span>• Ahora</span>
              <span class="table-badge badge-purple" style="font-size: 9px; padding: 1px 6px;">Historial Reiniciado</span>
            </div>
            <div class="chat-bubble">
              Historial de conversación reiniciado. Estoy lista para asistirte con tus transmisiones, estrategias y respuestas a fans. 🐺✨
            </div>
          </div>
        </div>
      `;
      lucide.createIcons();
      showToast('Historial de chat reiniciado');
    }

    async function sendCopilotMessage() {
      const inputEl = document.getElementById('copilot-input');
      if (!inputEl) return;
      const text = inputEl.value.trim();
      if (!text) return;

      const modelSelect = document.getElementById('chat-model-select');
      const model = modelSelect ? modelSelect.value : 'qwen2.5:7b-instruct';

      appendChatMessage('sam', text, 'es', model);
      inputEl.value = '';
      
      const indicator = document.getElementById('chat-typing-indicator');
      const sendBtn = document.getElementById('copilot-send-btn');
      if (indicator) indicator.style.display = 'flex';
      if (sendBtn) sendBtn.disabled = true;

      try {
        const res = await fetch('http://localhost:8888/api/chat', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            message: text,
            model: model,
            history: copilotChatHistory
          })
        });

        if (!res.ok) throw new Error('HTTP ' + res.status);
        const data = await res.json();
        if (indicator) indicator.style.display = 'none';
        if (sendBtn) sendBtn.disabled = false;

        appendChatMessage('roxanne', data.reply, data.detected_lang, data.model);
        copilotChatHistory.push({ role: 'user', content: text });
        copilotChatHistory.push({ role: 'assistant', content: data.reply });
      } catch (err) {
        // Direct Ollama fallback
        try {
          const directOllama = await fetch('http://localhost:11434/api/chat', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
              model: model,
              messages: [
                { role: 'system', content: `Eres ROXANNE, la Asistente Personal y Estratega exclusiva de la modelo webcam Sam Barton (@sambartonn23). Le hablas directamente a Sam con respeto, calidez, complicidad y profesionalismo en español, ayudándola a responder a fans, planear transmisiones y optimizar sus ingresos.` },
                ...copilotChatHistory,
                { role: 'user', content: text }
              ],
              stream: false
            })
          });
          const odata = await directOllama.json();
          if (indicator) indicator.style.display = 'none';
          if (sendBtn) sendBtn.disabled = false;
          const reply = odata.message?.content || 'Sin respuesta';
          appendChatMessage('roxanne', reply, 'es', 'Direct Ollama');
          copilotChatHistory.push({ role: 'user', content: text });
          copilotChatHistory.push({ role: 'assistant', content: reply });
        } catch (ollamaErr) {
          if (indicator) indicator.style.display = 'none';
          if (sendBtn) sendBtn.disabled = false;
          appendChatMessage('roxanne', `[Aviso ROXANNE]: Error conectando con el motor (${err.message}). Recuerda que el servidor debe estar activo: python src/server/velvet_app_server.py`, 'es');
        }
      }
    }
"""

# Let's find where appendChatMessage starts and replace until the end of sendCopilotMessage
pattern_chat_js = re.compile(r'function appendChatMessage\(sender, text.*?\n    function getApiBase\(\)', re.DOTALL)
if pattern_chat_js.search(html):
    html = pattern_chat_js.sub(js_helpers + "\n    function getApiBase()", html, count=1)
    print("Replaced chat JS functions with persistent history, light theme and credentials helpers.")
else:
    print("Could not match chat JS pattern, appending to end of script block.")

# Make sure initThemeFromStorage and loadCopilotChatHistory are called on DOMContentLoaded
init_call = """    document.addEventListener('DOMContentLoaded', () => {
      initThemeFromStorage();
      loadCopilotChatHistory();
    });
"""
if "initThemeFromStorage();" not in html:
    html = html.replace("window.addEventListener('load', () => {", init_call + "\n    window.addEventListener('load', () => {")
    print("Added initThemeFromStorage and loadCopilotChatHistory to startup.")

with open(INDEX_PATH, "w", encoding="utf-8") as f:
    f.write(html)

print("Step 3 applied successfully!")
