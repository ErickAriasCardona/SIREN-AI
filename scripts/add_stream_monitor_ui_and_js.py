from pathlib import Path

html_file = Path("index.html")
content = html_file.read_text(encoding="utf-8")

# 1. Add Toolbar to tab-roxanne-copilot right above prompt pills
prompt_pills_anchor = '<!-- Pastillas de Prompts Rápidos para Probar al Vuelo (Sin palabras prohibidas) -->'
sm_toolbar_html = """<!-- Barra de Acciones Stream Monitor & Maya -->
              <div style="background: rgba(245, 158, 11, 0.06); border: 1px solid rgba(245, 158, 11, 0.25); border-radius: 8px; padding: 10px 14px; margin-bottom: 12px;">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
                  <span style="font-size: 11px; font-weight: 700; color: #fbbf24; display: flex; align-items: center; gap: 6px;">
                    <i data-lucide="zap" style="width:13px; height:13px;"></i> Herramientas Stream Monitor & Maya (Streamate en Vivo)
                  </span>
                  <span style="font-size: 10px; color: var(--text-dim);">Pega lo de Maya o escribe • Aplica en 1 clic</span>
                </div>
                <div style="display: flex; gap: 8px; flex-wrap: wrap;">
                  <button class="action-btn" onclick="openSmModal('gold')" style="font-size: 11px; padding: 6px 12px; border-color: rgba(245, 158, 11, 0.4); color: #fbbf24;">
                    ⚡ Menú GOLD
                  </button>
                  <button class="action-btn" onclick="openSmModal('wheel')" style="font-size: 11px; padding: 6px 12px; border-color: rgba(168, 85, 247, 0.4); color: #c084fc;">
                    🎡 Gira La Rueda
                  </button>
                  <button class="action-btn" onclick="openSmModal('topic')" style="font-size: 11px; padding: 6px 12px; border-color: rgba(6, 182, 212, 0.4); color: #38bdf8;">
                    🏷️ Tema de Sala
                  </button>
                  <button class="action-btn" onclick="openSmModal('radar')" style="font-size: 11px; padding: 6px 12px; border-color: rgba(16, 185, 129, 0.4); color: #34d399;">
                    🔭 Radar Tomboy (Págs 1-3)
                  </button>
                </div>
              </div>

              <!-- Pastillas de Prompts Rápidos para Probar al Vuelo (Sin palabras prohibidas) -->"""

if "Herramientas Stream Monitor & Maya" not in content and prompt_pills_anchor in content:
    content = content.replace(prompt_pills_anchor, sm_toolbar_html, 1)
    print("Added Stream Monitor toolbar into tab-roxanne-copilot!")

# 2. Add Modal Dialog HTML next to #updateModal
update_modal_anchor = '<div id="updateModal" class="modal-overlay">'
sm_modal_html = """<!-- ============================================================== -->
  <!-- MODAL DIÁLOGO: STREAM MONITOR CONTROLLER (MAYA & SAM) -->
  <!-- ============================================================== -->
  <div id="streamMonitorModal" class="modal-overlay">
    <div class="modal-card" style="max-width: 650px;">
      <div class="modal-header">
        <h3 id="smModalTitle" style="display:flex; align-items:center; gap:8px;">
          <i data-lucide="zap" id="smModalIcon" style="color:#fbbf24; width:18px; height:18px;"></i>
          <span id="smModalHeading">Actualizar Menú GOLD en Stream Monitor</span>
        </h3>
        <button class="close-modal" onclick="closeSmModal()">&times;</button>
      </div>

      <!-- Explicación Didáctica de Estructura -->
      <div id="smModalInstructions" style="background: rgba(245, 158, 11, 0.08); border: 1px solid rgba(245, 158, 11, 0.3); border-radius: 8px; padding: 14px; margin-bottom: 16px; font-size: 12px; line-height: 1.6; color: var(--text-main);">
        <!-- Instructions rendered dynamically by openSmModal() -->
      </div>

      <!-- Textarea de entrada -->
      <div style="margin-bottom: 16px;">
        <label id="smModalInputLabel" style="display:block; font-size: 11px; font-weight: 700; color: #fff; margin-bottom: 6px; text-transform: uppercase; letter-spacing: 0.5px;">
          Pega el texto generado por Maya o escribe aquí:
        </label>
        <textarea id="smModalTextarea" style="width: 100%; height: 160px; background: rgba(0,0,0,0.4); border: 1px solid var(--border-color); border-radius: 8px; padding: 12px; color: #fff; font-family: monospace; font-size: 12px; outline: none; resize: vertical; line-height: 1.5;"></textarea>
      </div>

      <!-- Botones de Acción -->
      <div style="display: flex; justify-content: space-between; align-items: center;">
        <span id="smModalStatusNote" style="font-size: 11px; color: var(--text-dim);">
          Sincronización en vivo con Streamate (SamBartone)
        </span>
        <div style="display: flex; gap: 10px;">
          <button class="action-btn" onclick="closeSmModal()">Cancelar</button>
          <button class="action-btn primary" id="smModalApplyBtn" onclick="applyStreamMonitorAction()">
            <i data-lucide="play" style="width:13px; height:13px;"></i> Aplicar en Stream Monitor
          </button>
        </div>
      </div>
    </div>
  </div>

  <div id="updateModal" class="modal-overlay">"""

if 'id="streamMonitorModal"' not in content and update_modal_anchor in content:
    content = content.replace(update_modal_anchor, sm_modal_html, 1)
    print("Added streamMonitorModal HTML into index.html!")

# 3. Add JavaScript Functions for Stream Monitor Dialogs
js_anchor = "    // Modal Control\n    let selectedPlatform = 'all';"
sm_js_code = """    // ==========================================
    // 🛠️ STREAM MONITOR & MAYA DIALOGS LOGIC
    // ==========================================
    let currentSmModalType = 'gold';

    function openSmModal(type) {
      currentSmModalType = type;
      const modal = document.getElementById('streamMonitorModal');
      const heading = document.getElementById('smModalHeading');
      const icon = document.getElementById('smModalIcon');
      const instructions = document.getElementById('smModalInstructions');
      const label = document.getElementById('smModalInputLabel');
      const textarea = document.getElementById('smModalTextarea');
      const applyBtn = document.getElementById('smModalApplyBtn');

      if (type === 'gold') {
        heading.textContent = '⚡ Actualizar Menú GOLD en Stream Monitor';
        icon.setAttribute('data-lucide', 'zap');
        icon.style.color = '#fbbf24';
        instructions.innerHTML = `
          <strong>📋 Estructura Requerida para el Menú GOLD:</strong><br>
          Escribe o pega el texto generado por Maya o por ti. Cada línea debe contener la <strong>descripción de la opción</strong>, un guion <code>-</code> y el <strong>precio en GOLD</strong>.<br>
          <em>* Streamate requiere entre 3 y 7 opciones activas.</em><br>
          <div style="background: rgba(0,0,0,0.3); border-radius: 6px; padding: 8px; margin-top: 6px; font-family: monospace;">
            10x nalgadas - 15<br>
            Acercamiento en senos - 20<br>
            Baile sensual - 25<br>
            Mostrar juguetes - 30
          </div>
        `;
        label.textContent = 'Opciones del Menú GOLD (3 a 7 líneas):';
        textarea.value = `10x nalgadas - 15\\nAcercamiento en senos - 20\\nBaile sensual - 25\\nMostrar juguetes - 30`;
        applyBtn.innerHTML = '<i data-lucide="play" style="width:13px; height:13px;"></i> Aplicar Menú GOLD Ahora';
      } else if (type === 'wheel') {
        heading.textContent = '🎡 Configurar Gira La Rueda (Spin the Wheel)';
        icon.setAttribute('data-lucide', 'circle-dot');
        icon.style.color = '#c084fc';
        instructions.innerHTML = `
          <strong>📋 Estructura Requerida para la Ruleta:</strong><br>
          Indica el <strong>costo por giro</strong> en la primera línea (ej. <code>Costo: 20</code>) y luego enumera de <strong>8 a 14 opciones</strong> (una por línea):<br>
          <div style="background: rgba(0,0,0,0.3); border-radius: 6px; padding: 8px; margin-top: 6px; font-family: monospace;">
            Costo: 20<br>
            10x nalgadas<br>
            ASMR al oído<br>
            Acercamiento en rostro<br>
            Baile<br>
            Di mi nombre<br>
            Gemido<br>
            Quiño pícaro<br>
            Sonrisa y beso
          </div>
        `;
        label.textContent = 'Costo y Premios de la Ruleta (8 a 14 opciones):';
        textarea.value = `Costo: 20\\n10x nalgadas\\nASMR al oído\\nAcercamiento en rostro\\nBaile\\nDi mi nombre\\nGemido\\nQuiño pícaro\\nSonrisa y beso`;
        applyBtn.innerHTML = '<i data-lucide="play" style="width:13px; height:13px;"></i> Aplicar Ruleta Ahora';
      } else if (type === 'topic') {
        heading.textContent = '🏷️ Actualizar Tema de Habitación (Room Topic)';
        icon.setAttribute('data-lucide', 'tag');
        icon.style.color = '#38bdf8';
        instructions.innerHTML = `
          <strong>📋 Estructura del Tema de Habitación:</strong><br>
          Pega el tema que te sugirió Maya o escribe el gancho de la sesión. Es el texto que ven todos los miembros en el carrusel de Streamate.<br>
          <em>* Regla de oro: No uses emojis ni caracteres especiales para evitar errores en Streamate.</em>
        `;
        label.textContent = 'Tema de Habitación:';
        textarea.value = `Tomboy tech vibes & soft ukelele chords. Come say hi and ask what you want.`;
        applyBtn.innerHTML = '<i data-lucide="play" style="width:13px; height:13px;"></i> Actualizar Tema Ahora';
      } else if (type === 'radar') {
        heading.textContent = '🔭 Radar de Competencia Tomboy en Streamate';
        icon.setAttribute('data-lucide', 'crosshair');
        icon.style.color = '#34d399';
        instructions.innerHTML = `
          <strong>🔍 Exploración en Vivo de las Primeras 3 Páginas:</strong><br>
          Roxanne escaneará las transmisiones en vivo de Streamate y CamModels buscando modelos tomboy/alt activas, qué temas de sala tienen, sus tarifas de privado y qué dinámicas están usando hoy para darte referencias comerciales inmediatas.
        `;
        label.textContent = 'Instrucción o Parámetros de Búsqueda (Opcional):';
        textarea.value = `Escanear páginas 1 a 3 en Streamate: tomboy, short hair, tech, acoustic, alt vibes`;
        applyBtn.innerHTML = '<i data-lucide="search" style="width:13px; height:13px;"></i> Iniciar Escaneo de Radar';
      }

      modal.classList.add('active');
      lucide.createIcons();
    }

    function closeSmModal() {
      const modal = document.getElementById('streamMonitorModal');
      if (modal) modal.classList.remove('active');
    }

    async function applyStreamMonitorAction() {
      const textarea = document.getElementById('smModalTextarea');
      const applyBtn = document.getElementById('smModalApplyBtn');
      const text = textarea ? textarea.value.trim() : '';

      if (!text) {
        showToast('⚠️ Por favor ingresa el texto correspondiente.');
        return;
      }

      applyBtn.disabled = true;
      applyBtn.innerHTML = '<i data-lucide="loader-2" class="spin" style="width:13px; height:13px;"></i> Aplicando en Streamate...';
      lucide.createIcons();

      try {
        let endpoint = '';
        let payload = {};

        if (currentSmModalType === 'gold') {
          endpoint = `${getApiBase()}/api/streamate/update_gold_menu`;
          payload = { raw_text: text };
        } else if (currentSmModalType === 'wheel') {
          endpoint = `${getApiBase()}/api/streamate/update_wheel`;
          payload = { raw_text: text };
        } else if (currentSmModalType === 'topic') {
          endpoint = `${getApiBase()}/api/streamate/update_topic`;
          payload = { topic: text };
        } else if (currentSmModalType === 'radar') {
          endpoint = `${getApiBase()}/api/streamate/analyze_tomboy_radar`;
          payload = { query: text };
        }

        const res = await fetch(endpoint, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(payload)
        });

        const data = await res.json();
        closeSmModal();

        if (data.success) {
          showToast(`✓ ${data.message || 'Acción completada con éxito en Streamate'}`);
          // Publicar notificación directa en el chat de Roxanne
          if (currentSmModalType === 'radar') {
            const models = (data.radar?.models_found || []).map(m => `• **${m.performer}** (${m.private_rate}): *"${m.room_topic}"* - ${m.key_tactics}`).join('\\n');
            appendChatMessage('roxanne', `🔭 **Radar Tomboy Streamate (En Vivo):**\\n\\n${models}\\n\\n💡 **Tendencias clave:**\\n${(data.radar?.market_trends || []).join('\\n')}`, 'es', 'Radar Intelligence');
          } else {
            appendChatMessage('roxanne', `✓ **[Stream Monitor]:** ${data.message || 'Actualización inyectada con éxito en tu cuenta de Streamate.'}`, 'es', 'Stream Monitor Daemon');
          }
        } else {
          showToast(`⚠️ ${data.error || 'No se pudo aplicar el cambio.'}`);
        }
      } catch (err) {
        console.error('Error aplicando acción en Stream Monitor:', err);
        showToast(`⚠️ Error conectando con el servidor local: ${err.message}`);
        closeSmModal();
      } finally {
        applyBtn.disabled = false;
        applyBtn.innerHTML = '<i data-lucide="play" style="width:13px; height:13px;"></i> Aplicar en Stream Monitor';
        lucide.createIcons();
      }
    }

    // Modal Control
    let selectedPlatform = 'all';"""

if "function openSmModal(type)" not in content and js_anchor in content:
    content = content.replace(js_anchor, sm_js_code, 1)
    print("Added Stream Monitor JavaScript functions!")

html_file.write_text(content, encoding="utf-8")
print("Finished writing Stream Monitor UI and JS into index.html!")
