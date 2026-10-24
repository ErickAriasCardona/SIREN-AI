import re
from pathlib import Path

html_path = Path("index.html")
content = html_path.read_text(encoding="utf-8")

# 1. Add CSS for Roxanne 2-column layout
css_to_add = """
    /* ROXANNE COPILOT 2-COLUMN LAYOUT (CHAT EN EL CENTRO, PANEL INICIAL A LA DERECHA) */
    .roxanne-layout-container {
      display: grid;
      grid-template-columns: minmax(0, 1.45fr) minmax(340px, 380px);
      gap: 20px;
      align-items: stretch;
    }
    @media (max-width: 1150px) {
      .roxanne-layout-container {
        grid-template-columns: 1fr;
      }
    }
    .roxanne-center-chat {
      display: flex;
      flex-direction: column;
      min-width: 0;
    }
    .roxanne-center-chat .chat-console {
      height: 100%;
      display: flex;
      flex-direction: column;
    }
    .roxanne-center-chat .chat-messages-container {
      flex: 1;
      min-height: 520px;
      max-height: calc(100vh - 350px);
      height: 540px;
    }
    .roxanne-right-panel {
      display: flex;
      flex-direction: column;
      gap: 14px;
    }
    .roxanne-kpi-stack {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 12px;
    }
    .roxanne-kpi-mini {
      background: var(--bg-card);
      border: 1px solid var(--border-color);
      border-radius: var(--radius-md);
      padding: 12px 14px;
      display: flex;
      flex-direction: column;
      gap: 4px;
    }
    .roxanne-kpi-mini .title {
      font-size: 10px;
      text-transform: uppercase;
      letter-spacing: 0.8px;
      color: var(--text-muted);
      font-weight: 700;
    }
    .roxanne-kpi-mini .val {
      font-size: 15px;
      font-weight: 800;
      color: #fff;
    }
    .roxanne-kpi-mini .sub {
      font-size: 10px;
      color: var(--text-dim);
    }
    body.light-theme .roxanne-kpi-mini {
      background: #ffffff;
      border-color: #e2e8f0;
      box-shadow: 0 2px 6px rgba(0,0,0,0.03);
    }
    body.light-theme .roxanne-kpi-mini .val {
      color: #0f172a;
    }
"""

if ".roxanne-layout-container" not in content:
    content = content.replace("</style>", f"{css_to_add}\n  </style>")
    print("Added Roxanne 2-column layout CSS.")

# 2. Build the new HTML for tab-roxanne-copilot
new_tab_html = """      <!-- ========================================== -->
      <!-- PESTAÑA 10: ROXANNE COPILOT & SELECTOR MULTI-MODELO -->
      <!-- ========================================== -->
      <section id="tab-roxanne-copilot" class="tab-view">
        <div class="roxanne-layout-container">

          <!-- ========================================== -->
          <!-- COLUMNA PRINCIPAL / CENTRO: CONSOLA DE CHAT ROXANNE -->
          <!-- ========================================== -->
          <div class="roxanne-center-chat">
            <div class="card chat-console">
              <div class="card-title" style="flex-wrap: wrap; gap: 10px; padding-bottom: 12px; border-bottom: 1px solid var(--border-color);">
                <div style="display:flex; align-items:center; gap: 10px;">
                  <div class="chat-msg-avatar" style="background: linear-gradient(135deg, #9333ea, #06b6d4); font-weight:bold; width:36px; height:36px; min-width:36px;">RX</div>
                  <div>
                    <div style="font-size:15px; font-weight:800; color:#fff; display:flex; align-items:center; gap:8px;">
                      ROXANNE
                      <span class="table-badge badge-purple" style="font-size: 10px; padding: 2px 8px;">Asistente de Modelo Webcam</span>
                    </div>
                    <div style="font-size:11px; color:var(--text-dim); font-weight:400;">Entrenada exclusivamente para Sam Barton (@sambartonn23) • LoyalFans, Stripchat, Streamate</div>
                  </div>
                </div>
                <div style="display:flex; align-items:center; gap: 10px; flex-wrap: wrap;">
                  <span id="chat-engine-status" class="table-badge badge-success" style="font-size: 11px; padding: 4px 9px;">
                    🟢 Servidor VELVET Activo (localhost:8888)
                  </span>
                  <select id="chat-model-select" onchange="syncModelSelectWithRadio(this.value)" style="background: var(--bg-card); border: 1px solid var(--border-color); color: #fff; padding: 5px 10px; border-radius: 6px; font-size: 11px; outline: none; cursor: pointer;">
                    <option value="qwen2.5:7b-instruct" selected>qwen2.5:7b-instruct (Local Offline)</option>
                    <option value="qwen2.5:14b-instruct">qwen2.5:14b-instruct (Local)</option>
                    <option value="gemini-2.5-pro">Gemini 2.5 Pro (Cloud SDK)</option>
                    <option value="gemini-2.5-flash">Gemini 2.5 Flash (Cloud)</option>
                  </select>
                  <button class="action-btn" onclick="clearCopilotChat()" style="padding: 5px 12px; font-size: 11px;">
                    <i data-lucide="trash-2" style="width:12px; height:12px;"></i> Limpiar
                  </button>
                </div>
              </div>

              <!-- Ventana de mensajes del chat con altura amplia en el centro -->
              <div id="chat-messages-box" class="chat-messages-container">
                <!-- Mensaje Inicial de Bienvenida -->
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
                </div>
              </div>

              <!-- Indicador de tipeo / pensando -->
              <div id="chat-typing-indicator" style="display: none; font-size: 11px; color: var(--secondary); align-items: center; gap: 8px; padding-left: 10px;">
                <i data-lucide="loader-2" class="spin" style="width: 14px; height: 14px;"></i>
                <span>ROXANNE está pensando la mejor estrategia con Qwen 2.5...</span>
              </div>

              <!-- Pastillas de Prompts Rápidos para Probar al Vuelo (Sin palabras prohibidas) -->
              <div style="display:flex; flex-direction:column; gap:6px;">
                <span style="font-size: 10px; font-weight: 700; text-transform: uppercase; color: var(--text-dim); letter-spacing: 0.8px;">
                  Estrategias Rápidas (Haz clic para enviar al instante):
                </span>
                <div class="prompt-pills-wrap">
                  <button class="prompt-pill" onclick="useQuickPrompt('¿Cómo respondo a un fan que me pide rebaja para ir a privado en Streamate?')">
                    💬 <em>"Fan pide rebaja para privado en Streamate"</em>
                  </button>
                  <button class="prompt-pill" onclick="useQuickPrompt('Ayúdame a planear las metas de propinas con Lovense para el show de hoy en Stripchat')">
                    🎯 <em>"Metas Lovense para show de hoy en Stripchat"</em>
                  </button>
                  <button class="prompt-pill" onclick="useQuickPrompt('Hey Sam! What motorcycle do you ride?')">
                    🏍️ <em>"What motorcycle do you ride?" (EN)</em>
                  </button>
                  <button class="prompt-pill" onclick="useQuickPrompt('Hola hermosa, qué linda estás. ¿Haces videollamadas privadas?')">
                    📹 <em>"Hola hermosa, ¿haces videollamadas?" (ES)</em>
                  </button>
                  <button class="prompt-pill" onclick="useQuickPrompt('¿Cómo sugerirle a un fan que toco ukelele en privado para motivarlo a entrar?')">
                    🎸 <em>"Sugerir toque de ukelele para motivar privado"</em>
                  </button>
                </div>
              </div>

              <!-- Barra de entrada de texto -->
              <div class="chat-input-bar">
                <textarea id="copilot-input" class="chat-textarea" placeholder="Escribe a Roxanne o pega un mensaje de un fan aquí... (Enter para enviar, Shift+Enter para salto de línea)" rows="2" onkeydown="handleChatInputKeyDown(event)"></textarea>
                <button id="copilot-send-btn" class="chat-send-btn" onclick="sendCopilotMessage()">
                  <i data-lucide="send" style="width:14px; height:14px;"></i> Enviar
                </button>
              </div>

              <div style="font-size: 11px; color: var(--text-dim); display:flex; justify-content: space-between; align-items:center;">
                <span>⚡ <strong>Regla Inviolable:</strong> Si el fan escribe en español, Sam responde en español. De lo contrario, 100% inglés.</span>
                <span>💾 Base de datos: <code>velvet_analytics.db</code> (Historial Persistente)</span>
              </div>
            </div>
          </div>

          <!-- ========================================== -->
          <!-- COLUMNA DERECHA: SECCIÓN INICIAL (KPIS + SELECTOR DE MOTORES + ASISTENTE SPECS) -->
          <!-- ========================================== -->
          <div class="roxanne-right-panel">

            <!-- 1. KPIs Compactos de Estado -->
            <div class="roxanne-kpi-stack">
              <div class="roxanne-kpi-mini">
                <div class="title">Motor Activo</div>
                <div class="val" style="color: var(--primary-light);">Qwen 2.5 (7B)</div>
                <div class="sub">100% Local & Gratis</div>
              </div>

              <div class="roxanne-kpi-mini">
                <div class="title">Servidor Ollama</div>
                <div class="val" style="color: var(--success);">localhost:11434</div>
                <div class="sub">100% GPU Activo</div>
              </div>

              <div class="roxanne-kpi-mini">
                <div class="title">Servidor VELVET</div>
                <div class="val" id="server-kpi-status" style="color: #38bdf8;">Puerto 8888</div>
                <div class="sub">API Server Activo</div>
              </div>

              <div class="roxanne-kpi-mini">
                <div class="title">Regla Idioma</div>
                <div class="val" style="color: var(--secondary);">EN Def / ES In</div>
                <div class="sub">Bilingüe Automático</div>
              </div>
            </div>

            <!-- 2. Panel Selector de Motor LLM -->
            <div class="card" style="padding: 16px;">
              <div style="font-size: 13px; font-weight: 800; color: #fff; margin-bottom: 12px; display:flex; align-items:center; gap:8px;">
                <i data-lucide="cpu" style="width:16px; height:16px; color:var(--primary-light);"></i>
                Selector de Motor de IA
              </div>

              <!-- Motores Locales -->
              <div style="background: rgba(255,255,255,0.02); border: 1px solid var(--border-color); padding: 12px; border-radius: 8px; margin-bottom: 12px;">
                <div style="font-size: 11px; font-weight: 700; color: var(--primary-light); margin-bottom: 8px; display:flex; align-items:center; gap:6px;">
                  <i data-lucide="hard-drive" style="width:12px; height:12px;"></i> Local (Ollama • Gratis & Privado)
                </div>
                <div style="display:flex; flex-direction:column; gap:8px;">
                  <label style="display:flex; align-items:center; gap:8px; font-size:11px; cursor:pointer;">
                    <input type="radio" name="ai-engine" value="qwen2.5:7b-instruct" checked onchange="syncRadioWithModelSelect(this.value)">
                    <strong>qwen2.5:7b-instruct</strong>
                    <span class="table-badge badge-success" style="font-size:9px; padding:1px 5px; margin-left:auto;">Activo</span>
                  </label>
                  <label style="display:flex; align-items:center; gap:8px; font-size:11px; color:var(--text-dim); cursor:pointer;">
                    <input type="radio" name="ai-engine" value="qwen2.5:14b-instruct" onchange="syncRadioWithModelSelect(this.value)">
                    <span>qwen2.5:14b-instruct</span>
                    <span class="table-badge badge-warning" style="font-size:9px; padding:1px 5px; margin-left:auto;">Descargable</span>
                  </label>
                </div>
              </div>

              <!-- Motores en la Nube -->
              <div style="background: rgba(255,255,255,0.02); border: 1px solid var(--border-color); padding: 12px; border-radius: 8px;">
                <div style="font-size: 11px; font-weight: 700; color: var(--secondary); margin-bottom: 8px; display:flex; align-items:center; gap:6px;">
                  <i data-lucide="cloud" style="width:12px; height:12px;"></i> Cloud (Google AGY SDK)
                </div>
                <div style="display:flex; flex-direction:column; gap:8px;">
                  <label style="display:flex; align-items:center; gap:8px; font-size:11px; cursor:pointer;">
                    <input type="radio" name="ai-engine" value="gemini-2.5-pro" onchange="syncRadioWithModelSelect(this.value)">
                    <span>Gemini 2.5 Pro</span>
                    <span class="table-badge badge-info" style="font-size:9px; padding:1px 5px; margin-left:auto;">Cloud</span>
                  </label>
                  <label style="display:flex; align-items:center; gap:8px; font-size:11px; color:var(--text-dim); cursor:pointer;">
                    <input type="radio" name="ai-engine" value="gemini-2.5-flash" onchange="syncRadioWithModelSelect(this.value)">
                    <span>Gemini 2.5 Flash</span>
                    <span class="table-badge badge-purple" style="font-size:9px; padding:1px 5px; margin-left:auto;">Rápido</span>
                  </label>
                </div>
              </div>
            </div>

            <!-- 3. Tarjeta Informativa de Asistente de Modelo Webcam -->
            <div class="card" style="padding: 16px; background: rgba(147, 51, 234, 0.05); border-color: rgba(147, 51, 234, 0.3);">
              <div style="font-size: 12px; font-weight: 800; color: #d8b4fe; margin-bottom: 8px; display:flex; align-items:center; gap:6px;">
                <i data-lucide="shield-check" style="width:14px; height:14px; color:#c084fc;"></i>
                Tu Asistente & Estratega Personal
              </div>
              <p style="font-size: 11px; color: var(--text-muted); line-height: 1.5; margin-bottom: 10px;">
                Roxanne está configurada para orientarte en cómo cerrar privados rápidos en Streamate, dinamizar propinas de Lovense en Stripchat y vender contenido en LoyalFans, manteniendo siempre tu identidad de tomboy inteligente y versátil.
              </p>
              <div style="display:flex; flex-direction:column; gap:5px; font-size:11px; color:var(--text-dim);">
                <div>• <strong>Streamate:</strong> Impulsar EPH ($2.99 / $3.99 min).</div>
                <div>• <strong>Stripchat:</strong> Velocidad de tokens y vibraciones.</div>
                <div>• <strong>LoyalFans:</strong> Bumps cada 3.5h y DMs exclusivos.</div>
              </div>
            </div>

          </div>

        </div>
      </section>"""

# Replace the existing tab-roxanne-copilot section
tab_pattern = re.compile(
    r'<!-- ==========================================\s*-->\s*<!-- PESTAÑA 10: ROXANNE COPILOT.*?<!-- ==========================================\s*-->',
    re.DOTALL
)

# If not matching the next section header, match until </section>
tab_pattern2 = re.compile(
    r'<section id="tab-roxanne-copilot" class="tab-view">.*?</section>',
    re.DOTALL
)

if tab_pattern2.search(content):
    content = tab_pattern2.sub(new_tab_html.strip(), content)
    print("Replaced tab-roxanne-copilot with 2-column layout (Chat in center, panel on right)!")
else:
    print("Could not find tab-roxanne-copilot in index.html!")

# 3. Add helper JS functions for syncing model select and radio buttons, and checking server health
js_helpers = """
    function syncRadioWithModelSelect(val) {
      const sel = document.getElementById('chat-model-select');
      if (sel) sel.value = val;
    }

    function syncModelSelectWithRadio(val) {
      const radio = document.querySelector(`input[name="ai-engine"][value="${val}"]`);
      if (radio) radio.checked = true;
    }

    async function checkServerHealth() {
      const statusBadge = document.getElementById('chat-engine-status');
      const kpiStatus = document.getElementById('server-kpi-status');
      try {
        const res = await fetch('http://localhost:8888/api/status', { cache: 'no-store' });
        if (res.ok) {
          const data = await res.json();
          if (statusBadge) {
            statusBadge.className = 'table-badge badge-success';
            statusBadge.innerHTML = '🟢 Servidor VELVET Activo (localhost:8888)';
          }
          if (kpiStatus) {
            kpiStatus.textContent = 'Activo (8888)';
            kpiStatus.style.color = 'var(--success)';
          }
        } else {
          throw new Error('HTTP ' + res.status);
        }
      } catch (err) {
        if (statusBadge) {
          statusBadge.className = 'table-badge badge-danger';
          statusBadge.style.background = 'rgba(239, 68, 68, 0.2)';
          statusBadge.style.color = '#f87171';
          statusBadge.style.border = '1px solid rgba(239, 68, 68, 0.4)';
          statusBadge.innerHTML = '⚠️ Servidor Offline (python src/server/velvet_app_server.py)';
        }
        if (kpiStatus) {
          kpiStatus.textContent = 'Desconectado';
          kpiStatus.style.color = '#f87171';
        }
      }
    }
    // Check server health on load and every 15s
    setInterval(checkServerHealth, 15000);
    setTimeout(checkServerHealth, 1000);
"""

if "function checkServerHealth()" not in content:
    # Insert right before </script>
    last_script_idx = content.rfind("</script>")
    if last_script_idx != -1:
        content = content[:last_script_idx] + js_helpers + "\n  " + content[last_script_idx:]
        print("Added checkServerHealth and model sync JS helpers.")

html_path.write_text(content, encoding="utf-8")
print("Updated index.html successfully!")
