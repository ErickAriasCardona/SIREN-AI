import re
from pathlib import Path

html_path = Path("index.html")
content = html_path.read_text(encoding="utf-8")

# 1. REBRAND VELVET -> SIREN AI in title and brand elements
print("--- 1. Applying SIREN AI Rebranding ---")

# Title
content = content.replace(
    "<title>VELVET AI - Command & Intelligence Center | Sam Barton</title>",
    "<title>SIREN AI — Webcam Intelligence & Multi-Platform Command | Sam Barton</title>"
)

# Header & Badge
content = content.replace("VELVET AI v2.5", "SIREN AI v2.5")
content = content.replace("VELVET AI V2.5", "SIREN AI V2.5")
content = content.replace("VELVET <span>COMMAND</span>", "SIREN <span>COMMAND</span>")
content = content.replace("VELVET Daemon Activo", "SIREN Daemon Activo")
content = content.replace("toggleVelvetTheme", "toggleSirenTheme")
content = content.replace("Servidor VELVET", "Servidor SIREN")
content = content.replace("Servidor Velvet", "Servidor SIREN")
content = content.replace("VELVET AI", "SIREN AI")
content = content.replace("Velvet AI", "SIREN AI")

# Fix theme and history storage to support both siren and legacy velvet
content = content.replace(
    "localStorage.getItem('velvet_theme')",
    "(localStorage.getItem('siren_theme') || localStorage.getItem('velvet_theme'))"
)
content = content.replace(
    "localStorage.setItem('velvet_theme'",
    "localStorage.setItem('siren_theme'"
)
content = content.replace(
    "localStorage.getItem('velvet_roxanne_chat_history')",
    "(localStorage.getItem('siren_roxanne_chat_history') || localStorage.getItem('velvet_roxanne_chat_history'))"
)
content = content.replace(
    "localStorage.setItem('velvet_roxanne_chat_history'",
    "localStorage.setItem('siren_roxanne_chat_history'"
)

# 2. ENHANCE switchSubTab IN JAVASCRIPT TO BE LOCALLY SCOPED
print("--- 2. Updating switchSubTab logic ---")
old_switch_subtab = """    function switchSubTab(prefix, platform, btnEl) {
      document.querySelectorAll('.subtab-btn').forEach(b => b.classList.remove('active'));
      btnEl.classList.add('active');

      document.querySelectorAll('.sub-tab-content').forEach(c => c.style.display = 'none');
      const target = document.getElementById(`${prefix}-${platform}`);
      if (target) target.style.display = 'block';
    }"""

new_switch_subtab = """    function switchSubTab(prefix, platform, btnEl) {
      const container = btnEl.closest('.tab-view') || document;
      container.querySelectorAll('.subtab-btn').forEach(b => b.classList.remove('active'));
      btnEl.classList.add('active');

      container.querySelectorAll('.sub-tab-content').forEach(c => c.style.display = 'none');
      const target = container.querySelector(`#${prefix}-${platform}`) || document.getElementById(`${prefix}-${platform}`);
      if (target) target.style.display = 'block';
    }"""

if old_switch_subtab in content:
    content = content.replace(old_switch_subtab, new_switch_subtab)
    print("Updated switchSubTab function to be scoped per tab-view.")

# 3. RESTRUCTURE tab-finanzas TO HAVE SUBTABS PER PLATFORM
print("--- 3. Adding platform subtabs to tab-finanzas ---")
finanzas_pattern = re.compile(
    r'(<section id="tab-finanzas" class="tab-view">)(.*?)(<!-- Barra de Control de Sincronización)',
    re.DOTALL
)

finanzas_subtabs_bar = """<section id="tab-finanzas" class="tab-view">
        <!-- Sub-Pestañas Plataformas en Finanzas -->
        <div class="subtabs-bar">
          <button class="subtab-btn active" onclick="switchSubTab('sub-finanzas', 'loyalfans', this)">
            <i data-lucide="gem"></i> LoyalFans (Directo • 100% Split)
          </button>
          <button class="subtab-btn" onclick="switchSubTab('sub-finanzas', 'streamate', this)">
            <i data-lucide="zap"></i> Streamate (Auditoría Estudio Centenario • Solo Consulta)
          </button>
          <button class="subtab-btn" onclick="switchSubTab('sub-finanzas', 'stripchat', this)">
            <i data-lucide="flame"></i> Stripchat & Lovense (Tokens & Menú de Sala)
          </button>
          <button class="subtab-btn" onclick="switchSubTab('sub-finanzas', 'matriz', this)">
            <i data-lucide="table"></i> Matriz Consolidada de Pagos
          </button>
        </div>

        <!-- 1. SUBTAB LOYALFANS FINANZAS -->
        <div id="sub-finanzas-loyalfans" class="sub-tab-content">
          <!-- Barra de Control de Sincronización"""

# Wrap existing finanzas content inside the subtabs
if "sub-finanzas-loyalfans" not in content:
    content = content.replace(
        '<section id="tab-finanzas" class="tab-view">\n        <!-- Barra de Control de Sincronización',
        finanzas_subtabs_bar
    )
    
    # Now find where the streamate audit split analysis begins in finanzas and split it into subtabs
    split_audit_anchor = '<!-- Auditoría Comparativa de Split de Ingresos -->'
    streamate_finanzas_content = """        </div>

        <!-- 2. SUBTAB STREAMATE FINANZAS (SOLO CONSULTA / AUDITORIA EXTERNA) -->
        <div id="sub-finanzas-streamate" class="sub-tab-content" style="display:none;">
          <div style="background: rgba(245, 158, 11, 0.08); border: 1px solid rgba(245, 158, 11, 0.3); border-radius: var(--radius-md); padding: 14px 20px; margin-bottom: 20px; display:flex; justify-content:space-between; align-items:center;">
            <div style="display:flex; align-items:center; gap:12px;">
              <span class="status-dot" style="background:#fbbf24; box-shadow:0 0 10px #fbbf24;"></span>
              <div>
                <strong style="color:#fbbf24; font-size:14px;">Streamate Models: Modo Solo Consulta (Centenario Studio)</strong>
                <div style="font-size:11px; color:var(--text-muted);">
                  Streamate es administrado por el estudio satélite externo. SIREN AI monitorea ingresos en tiempo real.
                </div>
              </div>
            </div>
            <a href="https://streamatemodels.com/reports/earnings" target="_blank" class="action-btn" style="text-decoration:none; font-size:11px;">
              <i data-lucide="external-link"></i> Ver Reportes en Portal
            </a>
          </div>

          <!-- KPIs de Tarifas y Ganancia Neta Sam en Streamate -->
          <div class="grid-4" style="margin-bottom: 20px;">
            <div class="kpi-card" style="border-left: 3px solid #fbbf24;">
              <div class="kpi-header">
                <span class="kpi-title">Tarifa Privado (Bruto)</span>
                <div class="kpi-icon"><i data-lucide="video" style="color:#fbbf24;"></i></div>
              </div>
              <div class="kpi-value" style="color:#fbbf24;">$2.99 / min</div>
              <div class="kpi-sub">Pago neto a Sam (50% del 35%): <strong>~$0.52 / min</strong></div>
            </div>

            <div class="kpi-card" style="border-left: 3px solid #f59e0b;">
              <div class="kpi-header">
                <span class="kpi-title">Tarifa Exclusivo (Bruto)</span>
                <div class="kpi-icon"><i data-lucide="crown" style="color:#f59e0b;"></i></div>
              </div>
              <div class="kpi-value" style="color:#f59e0b;">$3.99 / min</div>
              <div class="kpi-sub">Pago neto a Sam (50% del 35%): <strong>~$0.70 / min</strong></div>
            </div>

            <div class="kpi-card" style="border-left: 3px solid #10b981;">
              <div class="kpi-header">
                <span class="kpi-title">Ganancias Semana Actual</span>
                <div class="kpi-icon"><i data-lucide="dollar-sign" style="color:#10b981;"></i></div>
              </div>
              <div class="kpi-value" style="color:#10b981;">$0.00 USD</div>
              <div class="kpi-sub">Auditoría en vivo: 0 horas de transmisión esta semana</div>
            </div>

            <div class="kpi-card" style="border-left: 3px solid #ec4899;">
              <div class="kpi-header">
                <span class="kpi-title">Llamadas Directas</span>
                <div class="kpi-icon"><i data-lucide="phone-call" style="color:#ec4899;"></i></div>
              </div>
              <div class="kpi-value" style="color:#ec4899;">$3.99 / min</div>
              <div class="kpi-sub">Video: $3.99/min • Voz: $2.99/min</div>
            </div>
          </div>
        </div>

        <!-- 3. SUBTAB STRIPCHAT & LOVENSE FINANZAS -->
        <div id="sub-finanzas-stripchat" class="sub-tab-content" style="display:none;">
          <div style="background: rgba(244, 63, 94, 0.08); border: 1px solid rgba(244, 63, 94, 0.3); border-radius: var(--radius-md); padding: 14px 20px; margin-bottom: 20px; display:flex; justify-content:space-between; align-items:center;">
            <div style="display:flex; align-items:center; gap:12px;">
              <span class="status-dot" style="background:#f43f5e; box-shadow:0 0 10px #f43f5e;"></span>
              <div>
                <strong style="color:#f43f5e; font-size:14px;">Stripchat & Lovense: Monetización por Tokens Freemium</strong>
                <div style="font-size:11px; color:var(--text-muted);">
                  Tokens acumulados en sala pública, shows privados interactivos y metas Lovense.
                </div>
              </div>
            </div>
            <a href="https://stripchat.com/sam_barton" target="_blank" class="action-btn" style="text-decoration:none; font-size:11px;">
              <i data-lucide="external-link"></i> Abrir Sala Stripchat
            </a>
          </div>

          <div class="grid-4" style="margin-bottom: 20px;">
            <div class="kpi-card" style="border-left: 3px solid #f43f5e;">
              <div class="kpi-header">
                <span class="kpi-title">Valor del Token (Creador)</span>
                <div class="kpi-icon"><i data-lucide="coins" style="color:#f43f5e;"></i></div>
              </div>
              <div class="kpi-value" style="color:#f43f5e;">$0.05 USD / tk</div>
              <div class="kpi-sub">100 tokens = <strong>$5.00 USD netos</strong></div>
            </div>

            <div class="kpi-card" style="border-left: 3px solid #a855f7;">
              <div class="kpi-header">
                <span class="kpi-title">Show Privado</span>
                <div class="kpi-icon"><i data-lucide="lock" style="color:#a855f7;"></i></div>
              </div>
              <div class="kpi-value" style="color:#a855f7;">60 tokens / min</div>
              <div class="kpi-sub">Equivalente a: <strong>$3.00 USD netos / min</strong></div>
            </div>

            <div class="kpi-card" style="border-left: 3px solid #06b6d4;">
              <div class="kpi-header">
                <span class="kpi-title">Juguete Lovense</span>
                <div class="kpi-icon"><i data-lucide="bluetooth" style="color:#06b6d4;"></i></div>
              </div>
              <div class="kpi-value" style="color:#06b6d4;">5 Niveles</div>
              <div class="kpi-sub">Sincronizado con propinas de 1 a 100+ tokens</div>
            </div>

            <div class="kpi-card" style="border-left: 3px solid #10b981;">
              <div class="kpi-header">
                <span class="kpi-title">Fan Club Mensual</span>
                <div class="kpi-icon"><i data-lucide="heart" style="color:#10b981;"></i></div>
              </div>
              <div class="kpi-value" style="color:#10b981;">199 tokens</div>
              <div class="kpi-sub">Suscripción recurrente a muro VIP</div>
            </div>
          </div>
        </div>

        <!-- 4. SUBTAB MATRIZ CONSOLIDADA -->
        <div id="sub-finanzas-matriz" class="sub-tab-content" style="display:none;">
"""
    if split_audit_anchor in content:
        content = content.replace(split_audit_anchor, f"{streamate_finanzas_content}\n          {split_audit_anchor}")
        print("Inserted Streamate and Stripchat subtabs into tab-finanzas.")

# 4. RESTRUCTURE tab-posicionamiento TO HAVE SUBTABS PER PLATFORM
print("--- 4. Adding platform subtabs to tab-posicionamiento ---")
pos_subtabs_bar = """      <section id="tab-posicionamiento" class="tab-view">
        <!-- Sub-Pestañas Plataformas en Posicionamiento -->
        <div class="subtabs-bar">
          <button class="subtab-btn active" onclick="switchSubTab('sub-pos', 'loyalfans', this)">
            <i data-lucide="gem"></i> LoyalFans (Radar Recently Updated • Top 23%)
          </button>
          <button class="subtab-btn" onclick="switchSubTab('sub-pos', 'streamate', this)">
            <i data-lucide="zap"></i> Streamate (Algoritmo EPH • Ganancia por Hora)
          </button>
          <button class="subtab-btn" onclick="switchSubTab('sub-pos', 'stripchat', this)">
            <i data-lucide="flame"></i> Stripchat (Velocidad de Tokens & Carrusel)
          </button>
        </div>

        <!-- 1. SUBTAB LOYALFANS POSICIONAMIENTO -->
        <div id="sub-pos-loyalfans" class="sub-tab-content">
"""

if "sub-pos-loyalfans" not in content:
    content = content.replace(
        '<section id="tab-posicionamiento" class="tab-view">',
        pos_subtabs_bar
    )
    
    # Find the end of loyal fans radar and insert streamate and stripchat radar subtabs
    comparativa_anchor = '<!-- Comparativa de Posicionamiento Entre Plataformas -->'
    pos_extra_subtabs = """        </div>

        <!-- 2. SUBTAB STREAMATE POSICIONAMIENTO (EPH REVENUE RADAR) -->
        <div id="sub-pos-streamate" class="sub-tab-content" style="display:none;">
          <div class="card" style="border: 1px solid rgba(245, 158, 11, 0.3); background: radial-gradient(circle at top right, rgba(245, 158, 11, 0.1), rgba(18, 14, 28, 0.95)); margin-bottom: 20px;">
            <div class="card-title">
              <span style="color:#fbbf24;">⚡ Streamate: Algoritmo Revenue-Driven (EPH - Earnings Per Hour)</span>
              <span class="table-badge badge-warning">Auditoría Estudio Centenario • Solo Consulta</span>
            </div>
            <p style="font-size:12px; color:var(--text-muted); line-height:1.6; margin-bottom:16px;">
              El algoritmo de Streamate no posiciona por antigüedad ni por fans registrados; su ranking global se basa exclusivamente en <strong>EPH (Earnings Per Hour)</strong>:
            </p>
            <div class="grid-3" style="margin-bottom:16px;">
              <div class="kpi-card" style="border-left: 3px solid #fbbf24;">
                <div class="kpi-title">Regla de Oro en Free Chat</div>
                <div class="kpi-value" style="font-size:16px; color:#fbbf24;">Máx 10 Minutos</div>
                <div class="kpi-sub">Pasar tiempo en Free Chat sin cobrar hunde tu perfil a las páginas 10-20.</div>
              </div>
              <div class="kpi-card" style="border-left: 3px solid #10b981;">
                <div class="kpi-title">Salto a Página 1 & 2</div>
                <div class="kpi-value" style="font-size:16px; color:#10b981;">2 Privados Rápidos</div>
                <div class="kpi-sub">Cerrar privados rápidos en los primeros 10 min te posiciona en el top.</div>
              </div>
              <div class="kpi-card" style="border-left: 3px solid #38bdf8;">
                <div class="kpi-title">Estado de Cuenta Actual</div>
                <div class="kpi-value" style="font-size:16px; color:#38bdf8;">Rating 4.0 ★</div>
                <div class="kpi-sub">4 idiomas oficiales actualizados y en revisión por cumplimiento.</div>
              </div>
            </div>
            <div style="background:rgba(0,0,0,0.25); border:1px solid rgba(255,255,255,0.06); border-radius:8px; padding:14px; font-size:12px; color:var(--text-muted); line-height:1.7;">
              💡 <strong>Estrategia Recomendada por SIREN AI:</strong> Utiliza el gancho de ukelele y conversación tomboy directa para filtrar mirones y forzar la entrada a show Privado ($2.99/min) o Exclusivo ($3.99/min) antes del minuto 8.
            </div>
          </div>
        </div>

        <!-- 3. SUBTAB STRIPCHAT POSICIONAMIENTO (VELOCITY & CONCURSOS) -->
        <div id="sub-pos-stripchat" class="sub-tab-content" style="display:none;">
          <div class="card" style="border: 1px solid rgba(244, 63, 94, 0.3); background: radial-gradient(circle at top right, rgba(244, 63, 94, 0.1), rgba(18, 14, 28, 0.95)); margin-bottom: 20px;">
            <div class="card-title">
              <span style="color:#f43f5e;">🔥 Stripchat: Algoritmo Velocity-Driven (Velocidad de Tokens & Carrusel)</span>
              <span class="table-badge badge-info">Directo • Tokens & Lovense</span>
            </div>
            <p style="font-size:12px; color:var(--text-muted); line-height:1.6; margin-bottom:16px;">
              En Stripchat el motor de recomendación premia la frecuencia de interacción por segundo en sala pública:
            </p>
            <div class="grid-3" style="margin-bottom:16px;">
              <div class="kpi-card" style="border-left: 3px solid #f43f5e;">
                <div class="kpi-title">Disparador de Tráfico</div>
                <div class="kpi-value" style="font-size:16px; color:#f43f5e;">Lovense Vibe Spikes</div>
                <div class="kpi-sub">Cada propina que activa el juguete dispara tu sala al carrusel superior.</div>
              </div>
              <div class="kpi-card" style="border-left: 3px solid #a855f7;">
                <div class="kpi-title">Muro Social Stripchat</div>
                <div class="kpi-value" style="font-size:16px; color:#a855f7;">Notificaciones Push</div>
                <div class="kpi-sub">Publicar fotos 15 minutos antes del directo avisa a todos tus seguidores en línea.</div>
              </div>
              <div class="kpi-card" style="border-left: 3px solid #10b981;">
                <div class="kpi-title">Metas de Sala (Ticket Show)</div>
                <div class="kpi-value" style="font-size:16px; color:#10b981;">250 - 500 Tokens</div>
                <div class="kpi-sub">Dividir el show en metas grupales acelera la acumulación de tokens.</div>
              </div>
            </div>
          </div>
        </div>
"""
    if comparativa_anchor in content:
        content = content.replace(comparativa_anchor, f"{pos_extra_subtabs}\n        {comparativa_anchor}")
        print("Inserted Streamate and Stripchat radar subtabs into tab-posicionamiento.")

html_path.write_text(content, encoding="utf-8")
print("Saved index.html with SIREN AI branding and platform subtabs!")
