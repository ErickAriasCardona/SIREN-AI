import os
import re

html_path = r"C:\Users\MI PC\Desktop\Sam\SIREN AI\index.html"

with open(html_path, "r", encoding="utf-8") as f:
    content = f.read()

# 1. Update CSS
css_pattern = re.compile(
    r"/\* STREAMMONITOR & MAHIA ORCHESTRATOR MODAL \*/.*?(?=/\* CODE BOXES \*/)",
    re.DOTALL
)

new_css = """/* STREAMMONITOR & MAHIA ORCHESTRATOR MODAL (ALMA TECH DESIGN SYSTEM) */
    #streamMonitorOrchestratorModal .modal-card {
      background: var(--bg-surface) !important;
      border: 1px solid var(--border-accent) !important;
      border-radius: var(--radius-lg) !important;
      box-shadow: 0 24px 60px rgba(0, 0, 0, 0.7) !important;
      color: var(--text-main) !important;
    }
    #streamMonitorOrchestratorModal .smo-status-bar {
      background: rgba(0, 229, 191, 0.06);
      border: 1px solid rgba(0, 229, 191, 0.22);
      border-radius: 12px;
      padding: 10px 14px;
      margin-bottom: 14px;
      display: flex;
      justify-content: space-between;
      align-items: center;
      flex-wrap: wrap;
      gap: 10px;
    }
    #streamMonitorOrchestratorModal .smo-preset-chip {
      padding: 6px 12px;
      border-radius: 8px;
      font-size: 11px;
      font-weight: 700;
      cursor: pointer;
      border: 1px solid rgba(0, 229, 191, 0.3);
      background: rgba(0, 229, 191, 0.08);
      color: #00E5BF;
      transition: all 0.2s ease;
      display: inline-flex;
      align-items: center;
      gap: 6px;
    }
    #streamMonitorOrchestratorModal .smo-preset-chip:hover {
      background: rgba(0, 229, 191, 0.2);
      border-color: #00A88F;
      color: #ffffff;
    }
    #streamMonitorOrchestratorModal .smo-preset-chip.active {
      background: linear-gradient(135deg, #00A88F 0%, #00E5BF 100%) !important;
      border: none !important;
      color: #062822 !important;
      font-weight: 800 !important;
      box-shadow: 0 2px 12px rgba(0, 229, 191, 0.4);
    }
    #streamMonitorOrchestratorModal .smo-card {
      background: rgba(18, 40, 36, 0.5);
      border: 1px solid rgba(0, 229, 191, 0.18);
      border-radius: 12px;
      padding: 14px 16px;
    }
    #streamMonitorOrchestratorModal .smo-subcard {
      background: rgba(10, 26, 23, 0.7);
      border: 1px solid rgba(0, 229, 191, 0.2);
      border-radius: 10px;
      padding: 10px 12px;
    }
    #streamMonitorOrchestratorModal .smo-terminal-box {
      background: rgba(6, 20, 18, 0.88);
      border: 1px solid rgba(0, 229, 191, 0.25);
      border-radius: 10px;
      padding: 14px;
      display: flex;
      flex-direction: column;
      gap: 12px;
    }
    #streamMonitorOrchestratorModal .smo-order-preview {
      background: rgba(0, 229, 191, 0.08);
      border-left: 3px solid #00E5BF;
      border-radius: 8px;
      padding: 10px 12px;
    }
    #streamMonitorOrchestratorModal .smo-reply-preview {
      background: rgba(0, 168, 143, 0.08);
      border-left: 3px solid #00A88F;
      border-radius: 8px;
      padding: 12px 14px;
      flex: 1;
      display: flex;
      flex-direction: column;
    }
    #streamMonitorOrchestratorModal .smo-item-pill {
      font-size: 11px;
      padding: 6px 10px;
      border-radius: 6px;
      background: rgba(6, 20, 18, 0.7);
      border: 1px solid rgba(0, 229, 191, 0.16);
      color: var(--text-main);
      display: flex;
      justify-content: space-between;
      align-items: center;
    }
    #streamMonitorOrchestratorModal .smo-trigger-item {
      background: rgba(6, 20, 18, 0.7);
      border-radius: 8px;
      padding: 8px 10px;
      border: 1px solid rgba(0, 229, 191, 0.18);
    }
    #streamMonitorOrchestratorModal .smo-tier-block {
      background: rgba(0, 229, 191, 0.05);
      border-left: 3px solid #00E5BF;
      border-radius: 8px;
      padding: 7px 10px;
    }
    #streamMonitorOrchestratorModal .smo-macro-item {
      background: rgba(6, 20, 18, 0.8);
      padding: 5px 8px;
      border-radius: 6px;
      border: 1px solid rgba(0, 229, 191, 0.2);
      white-space: nowrap;
      overflow: hidden;
      text-overflow: ellipsis;
    }
    #streamMonitorOrchestratorModal .smo-macro-text {
      color: var(--text-main);
      font-weight: 500;
    }
    #streamMonitorOrchestratorModal .smo-topic-chip {
      font-size: 11px;
      text-align: left;
      padding: 7px 11px;
      white-space: normal;
      word-break: break-word;
      border-radius: 8px;
      cursor: pointer;
      background: rgba(0, 229, 191, 0.08);
      border: 1px solid rgba(0, 229, 191, 0.3);
      color: #00E5BF;
      transition: all 0.2s ease;
      font-weight: 500;
      line-height: 1.4;
    }
    #streamMonitorOrchestratorModal .smo-topic-chip:hover {
      background: rgba(0, 229, 191, 0.18);
      border-color: #00A88F;
      color: #ffffff;
    }
    #streamMonitorOrchestratorModal .smo-idea-textarea {
      width: 100%;
      font-size: 12px;
      padding: 10px 12px;
      border-radius: 8px;
      border: 1px solid rgba(0, 229, 191, 0.3);
      background: rgba(6, 20, 18, 0.7);
      color: var(--text-main);
      resize: vertical;
      outline: none;
      line-height: 1.45;
    }
    #streamMonitorOrchestratorModal .smo-primary-btn {
      background: linear-gradient(135deg, #00A88F 0%, #00E5BF 100%) !important;
      color: #062822 !important;
      font-weight: 800 !important;
      border: none !important;
      box-shadow: 0 4px 18px rgba(0, 229, 191, 0.4) !important;
      cursor: pointer;
      border-radius: 8px;
      transition: transform 0.15s ease, box-shadow 0.15s ease;
      display: inline-flex;
      align-items: center;
      gap: 8px;
    }
    #streamMonitorOrchestratorModal .smo-primary-btn:hover {
      transform: translateY(-1px);
      box-shadow: 0 6px 22px rgba(0, 229, 191, 0.55) !important;
    }

    /* LIGHT THEME: ALMA TECH SOFT CLOUD EMERALD */
    body.light-theme #streamMonitorOrchestratorModal .modal-card {
      background: #ffffff !important;
      border: 1px solid rgba(0, 168, 143, 0.25) !important;
      color: #0B2520 !important;
      box-shadow: 0 24px 60px rgba(0, 168, 143, 0.14) !important;
    }
    body.light-theme #streamMonitorOrchestratorModal .smo-status-bar {
      background: #F0FBF8 !important;
      border-color: rgba(0, 168, 143, 0.25) !important;
    }
    body.light-theme #streamMonitorOrchestratorModal .smo-card {
      background: #F8FDFA !important;
      border-color: rgba(0, 168, 143, 0.22) !important;
      box-shadow: 0 2px 8px rgba(0, 168, 143, 0.04);
    }
    body.light-theme #streamMonitorOrchestratorModal .smo-subcard {
      background: #ffffff !important;
      border-color: rgba(0, 168, 143, 0.22) !important;
      box-shadow: 0 2px 8px rgba(0, 168, 143, 0.05) !important;
    }
    body.light-theme #streamMonitorOrchestratorModal .smo-terminal-box {
      background: #F4FAF8 !important;
      border-color: rgba(0, 168, 143, 0.25) !important;
      box-shadow: inset 0 1px 3px rgba(0, 168, 143, 0.05);
    }
    body.light-theme #streamMonitorOrchestratorModal .smo-order-preview {
      background: #E6F7F3 !important;
      border-left-color: #00A88F !important;
    }
    body.light-theme #streamMonitorOrchestratorModal .smo-order-preview div,
    body.light-theme #streamMonitorOrchestratorModal .smo-order-preview span {
      color: #0B2520 !important;
    }
    body.light-theme #streamMonitorOrchestratorModal .smo-reply-preview {
      background: #ffffff !important;
      border-left-color: #00A88F !important;
      box-shadow: 0 2px 8px rgba(0, 168, 143, 0.06);
    }
    body.light-theme #streamMonitorOrchestratorModal #smo-mahia-reply-preview {
      color: #0B2520 !important;
    }
    body.light-theme #streamMonitorOrchestratorModal .smo-item-pill {
      background: #F8FDFA !important;
      border-color: rgba(0, 168, 143, 0.2) !important;
      color: #0B2520 !important;
    }
    body.light-theme #streamMonitorOrchestratorModal .smo-trigger-item {
      background: #F8FDFA !important;
      border-color: rgba(0, 168, 143, 0.22) !important;
      box-shadow: 0 1px 3px rgba(0, 168, 143, 0.04);
    }
    body.light-theme #streamMonitorOrchestratorModal .smo-trigger-item span {
      color: #234942 !important;
    }
    body.light-theme #streamMonitorOrchestratorModal .smo-tier-block {
      background: #F0FBF8 !important;
      border-left-color: #00A88F !important;
    }
    body.light-theme #streamMonitorOrchestratorModal .smo-macro-item {
      background: #ffffff !important;
      border-color: rgba(0, 168, 143, 0.25) !important;
      box-shadow: 0 1px 3px rgba(0, 168, 143, 0.05);
    }
    body.light-theme #streamMonitorOrchestratorModal .smo-macro-text {
      color: #0B2520 !important;
    }
    body.light-theme #streamMonitorOrchestratorModal .smo-preset-chip {
      background: #EAF8F5 !important;
      border-color: rgba(0, 168, 143, 0.3) !important;
      color: #044338 !important;
    }
    body.light-theme #streamMonitorOrchestratorModal .smo-preset-chip:hover {
      background: rgba(0, 168, 143, 0.15) !important;
      color: #00A88F !important;
    }
    body.light-theme #streamMonitorOrchestratorModal .smo-preset-chip.active {
      background: linear-gradient(135deg, #00A88F 0%, #00E5BF 100%) !important;
      color: #062822 !important;
      border: none !important;
    }
    body.light-theme #streamMonitorOrchestratorModal .smo-topic-chip {
      background: #EAF8F5 !important;
      border-color: rgba(0, 168, 143, 0.35) !important;
      color: #044338 !important;
      font-weight: 600;
    }
    body.light-theme #streamMonitorOrchestratorModal .smo-topic-chip:hover {
      background: #D8F3ED !important;
      border-color: #00A88F !important;
      color: #023129 !important;
    }
    body.light-theme #streamMonitorOrchestratorModal .smo-idea-textarea,
    body.light-theme #streamMonitorOrchestratorModal textarea,
    body.light-theme #streamMonitorOrchestratorModal input {
      background: #ffffff !important;
      color: #0B2520 !important;
      border-color: rgba(0, 168, 143, 0.3) !important;
      box-shadow: inset 0 1px 3px rgba(0, 0, 0, 0.03);
    }
    
    """

if not css_pattern.search(content):
    print("ERROR: CSS pattern not found!")
    exit(1)

content = css_pattern.sub(new_css, content)
print("CSS updated successfully!")

# 2. Update HTML of #streamMonitorOrchestratorModal
modal_pattern = re.compile(
    r'<div id="streamMonitorOrchestratorModal" class="modal-overlay">.*?</div>\s*</div>\s*<!-- MODAL DE CONFIGURACIÓN',
    re.DOTALL
)

new_modal_html = """<div id="streamMonitorOrchestratorModal" class="modal-overlay" style="z-index: 100000;">
    <div class="modal-card" style="max-width: 1260px; width: 95%; max-height: 94vh; display: flex; flex-direction: column; padding: 22px;">
      
      <!-- Encabezado del Modal -->
      <div class="modal-header" style="padding-bottom: 12px; border-bottom: 1px solid var(--border-color); margin-bottom: 14px;">
        <div style="display: flex; align-items: center; gap: 12px;">
          <div style="width: 44px; height: 44px; border-radius: 12px; background: linear-gradient(135deg, rgba(0, 229, 191,0.25), rgba(0, 168, 143, 0.2)); display: flex; align-items: center; justify-content: center; border: 1px solid rgba(0, 229, 191,0.4); color: #00E5BF;">
            <i data-lucide="sparkles" style="width: 24px; height: 24px;"></i>
          </div>
          <div>
            <h3 style="margin: 0; font-size: 18px; font-weight: 800; display: flex; align-items: center; gap: 8px;">
               Co-Piloto Táctico StreamMonitor & Streamate
              <span class="table-badge badge-success" style="font-size: 9.5px; padding: 2px 7px;">Paso a Paso en Vivo</span>
            </h3>
            <div style="font-size: 11.5px; color: var(--text-dim); margin-top: 2px;">
              Planifica tu turno con tus palabras, genera la estrategia 100% en inglés y automatízala en 1 clic.
            </div>
          </div>
        </div>
        <button class="close-modal" onclick="closeStreamMonitorOrchestratorModal()" style="font-size: 22px; line-height: 1;">&times;</button>
      </div>

      <!-- Barra de Estado de StreamMonitor Desktop -->
      <div class="smo-status-bar">
        <div style="display: flex; align-items: center; gap: 12px; font-size: 11.5px;">
          <div style="display: flex; align-items: center; gap: 6px;">
            <span id="smo-status-indicator" style="display: inline-block; width: 9px; height: 9px; border-radius: 50%; background: var(--primary);"></span>
            <span id="smo-status-text" style="font-weight: 700; color: var(--primary);">StreamMonitor Detectado (v1.1.18)</span>
          </div>
          <span style="color: var(--text-dim);">|</span>
          <span style="color: var(--text-muted);"><strong style="color: var(--text-main);">Perfil:</strong> <span id="smo-account-text">SamBartone (ID 1589)</span></span>
          <span style="color: var(--text-dim);">|</span>
          <span style="color: var(--text-muted);"><strong style="color: var(--text-main);">Cámara:</strong> Logitech BRIO 4K</span>
          <span style="color: var(--text-dim);">|</span>
          <span style="color: var(--text-muted);"><strong style="color: var(--text-main);">Atajos:</strong> Alt+1 .. Alt+8</span>
        </div>
        <button class="action-btn" onclick="launchStreamMonitorDesktopApp()" style="font-size: 11px; padding: 5px 12px; border-color: rgba(0, 168, 143, 0.4); color: var(--primary); display: inline-flex; align-items: center; gap: 6px;">
          <i data-lucide="play" style="width: 12px; height: 12px;"></i> Abrir StreamMonitor en PC
        </button>
      </div>

      <!-- CUERPO PRINCIPAL CON SCROLL: PASO A PASO GUIADO -->
      <div style="flex: 1; overflow-y: auto; padding-right: 6px; display: flex; flex-direction: column; gap: 14px;">

        <!-- ========================================== -->
        <!-- PASO 1: TU IDEA O FANTASÍA DEL TURNO -->
        <!-- ========================================== -->
        <div class="smo-card" style="border-left: 4px solid var(--primary);">
          <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
            <div style="font-size: 13px; font-weight: 800; color: var(--primary); display: flex; align-items: center; gap: 7px;">
              <span style="background: var(--primary); color: #ffffff; width: 22px; height: 22px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 12px; font-weight: 900;">1</span>
              <span>¿Qué fantasía o meta comercial tienes hoy para el turno?</span>
            </div>
            <span class="table-badge badge-success" style="font-size: 9px; padding: 2px 7px;">Escribe en Español Natural</span>
          </div>

          <div style="font-size: 11px; color: var(--text-dim); margin-bottom: 8px; line-height: 1.4;">
            Escríbelo exactamente como lo piensas. SIREN lo analiza, deduce la psicología de sala y lo convierte en configuración técnica <strong>100% en inglés</strong> para los donadores de Streamate:
          </div>

          <textarea id="smo-natural-idea-input" class="smo-idea-textarea" rows="3" placeholder="Ej: hoy quiero vender la ball que va en mi boca y cuando esta mucho tiempo me produce mucha saliva, pienso que podria tenerla en el cuello en transmision el primer bloque de tiempo 4 o 5h para verla, y con esto seria un bloque de sumision pero ojo no sumision absoluta: domino o si sumisa es porque pagan..."></textarea>

          <!-- Ideas Rápidas en 1 Clic -->
          <div style="margin-top: 10px; display: flex; align-items: center; gap: 8px; flex-wrap: wrap;">
            <span style="font-size: 10.5px; font-weight: 700; color: var(--text-dim); text-transform: uppercase;">O prueba una idea rápida:</span>
            <button class="smo-preset-chip active" id="smo-chip-ball_gag_sub_dom" onclick="applyQuickIdea('ball_gag_sub_dom')">
               Ball Gag & Collar (Sumisión Pagada)
            </button>
            <button class="smo-preset-chip" id="smo-chip-ass_twerk" onclick="applyQuickIdea('ass_twerk')">
               Especial ASS & Twerk (3G)
            </button>
            <button class="smo-preset-chip" id="smo-chip-tomboy_ukelele" onclick="applyQuickIdea('tomboy_ukelele')">
               Chill Ukelele & Charla VIP
            </button>
            <button class="smo-preset-chip" id="smo-chip-full_lovense" onclick="applyQuickIdea('full_lovense')">
               Full Lovense Buzz (Control)
            </button>
          </div>

          <!-- Botón de Generación Paso 1 -->
          <div style="margin-top: 12px; display: flex; justify-content: flex-end;">
            <button class="action-btn smo-primary-btn" id="smo-orchestrate-btn" onclick="executeNaturalShiftOrchestration()" style="padding: 10px 22px; font-size: 12px;">
              <i data-lucide="bot" style="width: 16px; height: 16px;"></i>
              <span> 1. Abrir StreamMonitor y Enviar Orden a Mahia </span>
            </button>
          </div>

          <!-- Consola en Vivo de Progreso -->
          <div id="smo-live-console" class="smo-terminal-box" style="display: none; margin-top: 12px; font-family: var(--font-mono); font-size: 11px; max-height: 140px; overflow-y: auto; line-height: 1.5;">
          </div>
        </div>

        
        <!-- ============================================================ -->
        <!-- PASO 2: RESPUESTA EN VIVO DE MAHIA (IZQ) vs ESTRATEGIA DEDUCIDA POR SIREN (DER) -->
        <!-- ============================================================ -->
        <div style="display: grid; grid-template-columns: 1.05fr 1fr; gap: 16px; align-items: stretch; margin-top: 4px;">

          <!-- ========================================== -->
          <!-- COLUMNA IZQUIERDA: RESPUESTA EN TIEMPO REAL DE MAHIA -->
          <!-- ========================================== -->
          <div class="smo-card" style="border-left: 4px solid var(--primary-light); display: flex; flex-direction: column; padding: 16px;">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px; padding-bottom: 8px; border-bottom: 1px solid var(--border-color);">
              <div style="font-size: 13.5px; font-weight: 800; color: var(--primary); display: flex; align-items: center; gap: 8px;">
                <span style="background: var(--primary); color: #fff; width: 24px; height: 24px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 12px; font-weight: 900;">2A</span>
                <span> Respuesta en Tiempo Real de Mahia</span>
              </div>
              <span id="smo-mahia-live-badge" class="table-badge badge-success" style="font-size: 9.5px; padding: 3px 8px; font-weight: 700;">StreamMonitor Desktop</span>
            </div>

            <div style="font-size: 11px; color: var(--text-dim); margin-bottom: 10px; line-height: 1.4;">
              Diálogo capturado en vivo directamente del chat de Mahia en tu pantalla:
            </div>

            <!-- Contenedor Conversación con Mahia -->
            <div class="smo-terminal-box" style="flex: 1; min-height: 420px; max-height: 520px; overflow-y: auto;">
              
              <!-- Orden que SIREN envió a Mahia -->
              <div class="smo-order-preview">
                <div style="font-size: 10.5px; font-weight: 800; color: var(--primary); margin-bottom: 4px; display: flex; align-items: center; gap: 6px;">
                  <i data-lucide="send" style="width: 12px; height: 12px;"></i> SIREN entregó a Mahia en StreamMonitor:
                </div>
                <div id="smo-siren-to-mahia-preview" style="font-size: 11px; color: var(--text-main); font-family: var(--font-mono); line-height: 1.45; word-break: break-word;">
                  Esperando envío de tu idea...
                </div>
              </div>

              <!-- Respuesta Textual Completa de Mahia -->
              <div class="smo-reply-preview">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
                  <div style="font-size: 11px; font-weight: 800; color: var(--primary); display: flex; align-items: center; gap: 6px;">
                    <i data-lucide="bot" style="width: 13px; height: 13px;"></i> Respuesta textual de Mahia:
                  </div>
                  <button class="action-btn" onclick="copySmoMahiaReplyText()" style="font-size: 9.5px; padding: 2px 8px; border-color: rgba(0, 168, 143, 0.4); color: var(--primary); cursor: pointer;">
                     Copiar Texto
                  </button>
                </div>
                <div id="smo-mahia-reply-preview" style="font-size: 11.5px; line-height: 1.55; white-space: pre-wrap; word-break: break-word; min-height: 260px; max-height: 480px; overflow-y: auto; font-family: var(--font-sans);">
                  Mahia responderá aquí con sus sugerencias de Topic en inglés, Menú Gold oficial a 3G y Ruleta a 5G...
                </div>
              </div>

              <!-- Tópicos Sugeridos por Mahia (Chips Interactivos) -->
              <div id="smo-mahia-topics-selector" style="display: none; padding-top: 8px; border-top: 1px dashed var(--border-accent);">
                <div style="font-size: 10.5px; font-weight: 800; color: var(--primary); margin-bottom: 6px;">
                   Tópicos detectados en la respuesta de Mahia (Haz clic para usar en tu sala):
                </div>
                <div id="smo-mahia-topics-chips" style="display: flex; flex-direction: column; gap: 6px;">
                </div>
              </div>

            </div>
          </div>

          <!-- ========================================== -->
          <!-- COLUMNA DERECHA: CONFIGURACIÓN DEDUCIDA POR SIREN (NO DATA QUEMADA) -->
          <!-- ========================================== -->
          <div class="smo-card" style="border-left: 4px solid var(--primary); display: flex; flex-direction: column; padding: 16px;">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px; padding-bottom: 8px; border-bottom: 1px solid var(--border-color);">
              <div style="font-size: 13.5px; font-weight: 800; color: var(--primary); display: flex; align-items: center; gap: 8px;">
                <span style="background: var(--primary); color: #ffffff; width: 24px; height: 24px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 12px; font-weight: 900;">2B</span>
                <span> Opciones Deducidas por SIREN (Streamate)</span>
              </div>
              <span class="table-badge badge-success" style="font-size: 9.5px; padding: 3px 8px; font-weight: 700;">100% Catálogo Oficial</span>
            </div>

            <div style="font-size: 11px; color: var(--text-dim); margin-bottom: 10px; line-height: 1.4;">
              Opciones deducidas en vivo según las sugerencias de Mahia (cero datos quemados):
            </div>

            <div style="display: flex; flex-direction: column; gap: 12px; flex: 1;">
              
              <!-- 1. Topic de Sala Deducido -->
              <div class="smo-subcard">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 6px;">
                  <span style="font-size: 11px; font-weight: 800; color: var(--primary);">
                     Topic Oficial Deducido de Mahia:
                  </span>
                  <span style="font-size: 11px; font-weight: 800; color: var(--primary);">
                    <span id="smo-topic-counter">0/140</span> chars (&le; 140)
                  </span>
                </div>
                <input type="text" id="smo-topic-input" maxlength="140" oninput="updateSmoTopicCounter()" class="smo-idea-textarea" style="font-weight: 600; padding: 8px 10px;">
              </div>

              <!-- 2. Grids de Menú Gold (3G) y Ruleta (5G) -->
              <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 10px;">
                <!-- Menú Gold 3G -->
                <div class="smo-subcard">
                  <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
                    <span style="font-size: 11px; font-weight: 800; color: var(--primary);"> Menú GOLD (3G)</span>
                    <span class="table-badge badge-warning" style="font-size: 9px; padding: 1px 6px;">6 Ítems</span>
                  </div>
                  <div id="smo-gold-list" style="display: flex; flex-direction: column; gap: 5px; max-height: 165px; overflow-y: auto;">
                    <!-- Dinámico -->
                  </div>
                </div>

                <!-- Ruleta Íntima 5G -->
                <div class="smo-subcard">
                  <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
                    <span style="font-size: 11px; font-weight: 800; color: var(--primary);"> Ruleta Íntima (5G)</span>
                    <span class="table-badge badge-warning" style="font-size: 9px; padding: 1px 6px;">10 Ítems</span>
                  </div>
                  <div id="smo-wheel-list" style="display: flex; flex-direction: column; gap: 5px; max-height: 165px; overflow-y: auto;">
                    <!-- Dinámico -->
                  </div>
                </div>
              </div>

              <!-- 3. Los 3 Mensajes Automáticos de StreamMonitor (Deducidos de Mahia) -->
              <div class="smo-subcard">
                <div style="font-size: 11px; font-weight: 800; color: var(--text-main); margin-bottom: 6px; display: flex; justify-content: space-between; align-items: center;">
                  <span style="display: flex; align-items: center; gap: 6px;">
                    <i data-lucide="message-square" style="width: 13px; height: 13px; color: var(--primary);"></i>
                    <span> 3 Disparadores Automáticos (StreamMonitor):</span>
                  </span>
                  <span class="table-badge badge-success" style="font-size: 8.5px; padding: 1px 6px;">Auto-Sync</span>
                </div>
                <div style="display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 8px; font-size: 10.5px;">
                  <div class="smo-trigger-item">
                    <strong style="color: var(--primary); display: block; font-size: 10px; margin-bottom: 2px;"> Saludo / 30s:</strong>
                    <span id="smo-auto-welcome" style="line-height: 1.35; display: block;">...</span>
                  </div>
                  <div class="smo-trigger-item">
                    <strong style="color: var(--primary); display: block; font-size: 10px; margin-bottom: 2px;"> Entrar a Privado:</strong>
                    <span id="smo-auto-private" style="line-height: 1.35; display: block;">...</span>
                  </div>
                  <div class="smo-trigger-item">
                    <strong style="color: var(--primary); display: block; font-size: 10px; margin-bottom: 2px;"> Propina Gold:</strong>
                    <span id="smo-auto-tip" style="line-height: 1.35; display: block;">...</span>
                  </div>
                </div>
              </div>

              <!-- 4. Seis Atajos Rápidos de Chat (Alt+1 a Alt+6) Deducidos de Mahia -->
              <div class="smo-subcard">
                <div style="font-size: 11px; font-weight: 800; color: var(--primary); margin-bottom: 8px; display: flex; justify-content: space-between; align-items: center;">
                  <span style="display: flex; align-items: center; gap: 6px;">
                    <i data-lucide="zap" style="width: 14px; height: 14px;"></i>
                    <span> 6 Atajos Rápidos (Alt + #) Segmentados [StreamMonitor]:</span>
                  </span>
                  <span class="table-badge badge-success" style="font-size: 8.5px; padding: 1px 6px;">Deducidos de Mahia</span>
                </div>
                
                <div style="display: flex; flex-direction: column; gap: 6px;">
                  <!-- Tier 1: Nuevos / Primera vez en sala (Alt+1 y Alt+2) -->
                  <div class="smo-tier-block">
                    <div style="font-size: 9.5px; font-weight: 800; color: var(--primary); margin-bottom: 3px; display: flex; justify-content: space-between;">
                      <span> PRIMERA VEZ EN LA SALA (Nuevos):</span>
                      <span style="color: var(--text-dim); font-size: 8.5px;">Afín con Saludo 30s</span>
                    </div>
                    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 5px; font-size: 10.5px;">
                      <div class="smo-macro-item">
                        <strong style="color: var(--primary);">Alt+1:</strong> <span id="smo-macro-1" class="smo-macro-text" title="...">...</span>
                      </div>
                      <div class="smo-macro-item">
                        <strong style="color: var(--primary);">Alt+2:</strong> <span id="smo-macro-2" class="smo-macro-text" title="...">...</span>
                      </div>
                    </div>
                  </div>

                  <!-- Tier 2: Ya han entrado antes (Retorno) (Alt+3 y Alt+4) -->
                  <div class="smo-tier-block">
                    <div style="font-size: 9.5px; font-weight: 800; color: var(--primary); margin-bottom: 3px; display: flex; justify-content: space-between;">
                      <span> YA HAN ENTRADO ANTES (Retorno):</span>
                      <span style="color: var(--text-dim); font-size: 8.5px;">Re-enganche cálido</span>
                    </div>
                    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 5px; font-size: 10.5px;">
                      <div class="smo-macro-item">
                        <strong style="color: var(--primary);">Alt+3:</strong> <span id="smo-macro-3" class="smo-macro-text" title="...">...</span>
                      </div>
                      <div class="smo-macro-item">
                        <strong style="color: var(--primary);">Alt+4:</strong> <span id="smo-macro-4" class="smo-macro-text" title="...">...</span>
                      </div>
                    </div>
                  </div>

                  <!-- Tier 3: Varias veces / Habituales / VIPs (Alt+5 y Alt+6) -->
                  <div class="smo-tier-block">
                    <div style="font-size: 9.5px; font-weight: 800; color: var(--primary); margin-bottom: 3px; display: flex; justify-content: space-between;">
                      <span> HAN ENTRADO VARIAS VECES (Habituales / VIPs):</span>
                      <span style="color: var(--text-dim); font-size: 8.5px;">Fidelización & Privado</span>
                    </div>
                    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 5px; font-size: 10.5px;">
                      <div class="smo-macro-item">
                        <strong style="color: var(--primary);">Alt+5:</strong> <span id="smo-macro-5" class="smo-macro-text" title="...">...</span>
                      </div>
                      <div class="smo-macro-item">
                        <strong style="color: var(--primary);">Alt+6:</strong> <span id="smo-macro-6" class="smo-macro-text" title="...">...</span>
                      </div>
                    </div>
                  </div>
                </div>
              </div>

            </div>
          </div>

        </div>

        <!-- ========================================== -->
        <!-- SECCIÓN PLEGABLE EDUCATIVA: ORDEN PARA MAHIA -->
        <!-- ========================================== -->
        <div class="smo-card" style="border: 1px dashed var(--border-accent);">
          <div style="display: flex; justify-content: space-between; align-items: center; cursor: pointer;" onclick="toggleMahiaSection()">
            <div style="font-size: 12px; font-weight: 700; color: var(--primary); display: flex; align-items: center; gap: 8px;">
              <i data-lucide="help-circle" style="width: 15px; height: 15px;"></i>
              <span>¿Para qué sirve la "Orden Táctica para Mahia" y cómo usarla en StreamMonitor?</span>
            </div>
            <span id="smo-mahia-toggle-text" style="font-size: 11px; color: var(--text-dim); text-decoration: underline;">Mostrar detalles ▼</span>
          </div>

          <div id="smo-mahia-foldable-content" style="display: none; margin-top: 10px; font-size: 11.5px; color: var(--text-muted); line-height: 1.5;">
            <p style="margin: 0 0 8px 0;">
              <strong>¿Por qué existe esta orden?</strong> Mahia es la IA conversacional que Devin Systems integró dentro de la ventana de StreamMonitor. Si le preguntas a Mahia cosas abiertas, suele escribir párrafos largos o no respetar el límite de 140 caracteres de Streamate.
            </p>
            <p style="margin: 0 0 10px 0;">
              SIREN actúa como el co-piloto estratégico que formula la orden estricta. Si deseas que Mahia te asista durante la transmisión dentro de StreamMonitor, solo copia este texto y pégalo en su chat:
            </p>
            <div style="display: flex; gap: 8px; align-items: flex-start;">
              <textarea id="smo-mahia-prompt-box" rows="4" readonly class="smo-idea-textarea" style="flex: 1; font-family: var(--font-mono); font-size: 10.5px; line-height: 1.4;"></textarea>
              <button class="action-btn" onclick="copySmoMahiaPrompt()" style="font-size: 11px; padding: 8px 12px; border-color: rgba(0, 168, 143, 0.4); color: var(--primary); display: inline-flex; align-items: center; gap: 5px; height: 40px;">
                <i data-lucide="copy" style="width: 13px; height: 13px;"></i> Copiar
              </button>
            </div>
          </div>
        </div>

      </div>

      <!-- ========================================== -->
      <!-- PASO 3: BOTÓN DE ACCIÓN MAESTRO (FOOTER) -->
      <!-- ========================================== -->
      <div style="padding-top: 14px; border-top: 1px solid var(--border-color); margin-top: 14px; display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 10px;">
        <div style="font-size: 11px; color: var(--text-dim); display: flex; align-items: center; gap: 6px;">
          <i data-lucide="shield-check" style="width: 14px; height: 14px; color: var(--primary);"></i>
          <span>Cumplimiento ético: SIREN no modifica el encoder de video ni drivers de cámara de StreamMonitor.</span>
        </div>
        <div style="display: flex; gap: 10px;">
          <button class="action-btn" onclick="closeStreamMonitorOrchestratorModal()" style="font-size: 12px; padding: 8px 16px;">
            Cerrar
          </button>
          <button class="action-btn smo-primary-btn" id="smo-apply-btn" onclick="applySmoShiftStrategy()" style="font-size: 12.5px; padding: 9px 22px;">
            <i data-lucide="zap" style="width: 16px; height: 16px;"></i>
            <span> Inyectar Estrategia Completa a Streamate & Loyalfans (1-Click)</span>
          </button>
        </div>
      </div>

    </div>
  </div>

  <!-- MODAL DE CONFIGURACIÓN"""

if not modal_pattern.search(content):
    print("ERROR: Modal HTML pattern not found!")
    exit(1)

content = modal_pattern.sub(new_modal_html, content)
print("Modal HTML updated successfully!")

# 3. Update JS in renderSmoStrategy()
old_js = """          altTopics.forEach((t, idx) => {
            const btn = document.createElement('button');
            btn.className = 'action-btn';
            btn.style.fontSize = '10px';
            btn.style.textAlign = 'left';
            btn.style.padding = '4px 8px';
            btn.style.whiteSpace = 'normal';
            btn.style.wordBreak = 'break-word';
            btn.style.borderColor = idx === 0 ? 'rgba(26,229,139,0.5)' : 'rgba(0, 229, 191,0.4)';
            btn.style.color = idx === 0 ? '#1AE589' : '#00E5BF';
            btn.innerHTML = `<strong>${idx === 0 ? 'Principal' : 'Alternativa'}:</strong> "${t}"`;
            btn.onclick = () => selectSmoTopic(t);
            topicsChips.appendChild(btn);
          });"""

new_js = """          altTopics.forEach((t, idx) => {
            const btn = document.createElement('button');
            btn.className = 'smo-topic-chip';
            btn.innerHTML = `<strong>${idx === 0 ? 'Principal' : 'Alternativa'}:</strong> "${t}"`;
            btn.onclick = () => selectSmoTopic(t);
            topicsChips.appendChild(btn);
          });"""

if old_js not in content:
    print("ERROR: old_js not found in content!")
    exit(1)

content = content.replace(old_js, new_js)
print("JS updated successfully!")

# Write back
with open(html_path, "w", encoding="utf-8") as f:
    f.write(content)

print("index.html completely refactored successfully!")
