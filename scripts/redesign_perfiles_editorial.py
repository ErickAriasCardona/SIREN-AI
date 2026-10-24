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

# 1. Add Editorial Showcase CSS styles
editorial_css = """
    /* ========================================== */
    /* 📸 EDITORIAL DOSSIER PROFILE CARD (ESTILO FOTO-PROMPT) */
    /* ========================================== */
    .editorial-card {
      background: #090d14;
      border: 1px solid rgba(255, 255, 255, 0.12);
      border-radius: 18px;
      overflow: hidden;
      box-shadow: 0 16px 40px rgba(0, 0, 0, 0.6);
      position: relative;
      margin-bottom: 25px;
      background-image: radial-gradient(circle at 85% 15%, rgba(6, 182, 212, 0.15) 0%, transparent 60%),
                        radial-gradient(circle at 15% 85%, rgba(147, 51, 234, 0.12) 0%, transparent 50%);
    }

    body.light-theme .editorial-card {
      background: #ffffff;
      border-color: #cbd5e1;
      box-shadow: 0 10px 30px rgba(0, 0, 0, 0.08);
      background-image: radial-gradient(circle at 85% 15%, rgba(6, 182, 212, 0.08) 0%, transparent 60%),
                        radial-gradient(circle at 15% 85%, rgba(147, 51, 234, 0.06) 0%, transparent 50%);
    }

    .editorial-hero-banner {
      display: flex;
      justify-content: space-between;
      align-items: center;
      padding: 16px 24px;
      border-bottom: 1px solid rgba(255, 255, 255, 0.08);
      background: rgba(0, 0, 0, 0.25);
    }

    body.light-theme .editorial-hero-banner {
      background: rgba(248, 250, 252, 0.9);
      border-bottom-color: #e2e8f0;
    }

    .editorial-badge {
      display: inline-flex;
      align-items: center;
      gap: 8px;
      font-size: 11px;
      font-weight: 700;
      letter-spacing: 1.5px;
      text-transform: uppercase;
      padding: 4px 12px;
      border-radius: 20px;
    }

    .editorial-body {
      display: grid;
      grid-template-columns: 360px 1fr;
      gap: 28px;
      padding: 28px;
    }

    @media (max-width: 1024px) {
      .editorial-body {
        grid-template-columns: 1fr;
      }
    }

    .editorial-left-col {
      display: flex;
      flex-direction: column;
      gap: 20px;
    }

    .editorial-right-col {
      display: flex;
      flex-direction: column;
      gap: 20px;
    }

    .editorial-portrait-frame {
      position: relative;
      border-radius: 14px;
      overflow: hidden;
      border: 1px solid rgba(255, 255, 255, 0.15);
      box-shadow: 0 12px 30px rgba(0,0,0,0.5);
      background: #000;
      aspect-ratio: 4 / 5;
      max-height: 440px;
    }

    .editorial-portrait-frame img {
      width: 100%;
      height: 100%;
      object-fit: cover;
      display: block;
      transition: transform 0.4s ease;
    }

    .editorial-portrait-frame:hover img {
      transform: scale(1.02);
    }

    .editorial-portrait-overlay {
      position: absolute;
      bottom: 0;
      left: 0;
      right: 0;
      padding: 20px 16px 14px;
      background: linear-gradient(180deg, transparent 0%, rgba(0,0,0,0.85) 100%);
      display: flex;
      flex-direction: column;
      gap: 4px;
    }

    .editorial-prompt-title {
      font-family: 'JetBrains Mono', monospace;
      font-size: 26px;
      font-weight: 800;
      color: #38bdf8;
      letter-spacing: -0.5px;
      display: flex;
      align-items: center;
      gap: 10px;
      margin-bottom: 12px;
    }

    .editorial-anchor-box {
      display: flex;
      align-items: center;
      gap: 14px;
      padding: 12px 14px;
      background: rgba(255, 255, 255, 0.03);
      border: 1px solid rgba(255, 255, 255, 0.1);
      border-radius: 12px;
    }

    body.light-theme .editorial-anchor-box {
      background: #f8fafc;
      border-color: #e2e8f0;
    }

    .editorial-anchor-thumb {
      width: 54px;
      height: 54px;
      border-radius: 10px;
      object-fit: cover;
      border: 2px solid #10b981;
      box-shadow: 0 0 12px rgba(16, 185, 129, 0.4);
    }

    .spec-block {
      background: rgba(255, 255, 255, 0.02);
      border: 1px solid rgba(255, 255, 255, 0.07);
      border-radius: 12px;
      padding: 16px 18px;
      font-size: 12px;
      line-height: 1.6;
    }

    body.light-theme .spec-block {
      background: #f8fafc;
      border-color: #e2e8f0;
      color: #1e293b;
    }

    .spec-label {
      font-family: 'JetBrains Mono', monospace;
      font-size: 11px;
      font-weight: 700;
      text-transform: uppercase;
      letter-spacing: 1px;
      color: #38bdf8;
      margin-bottom: 6px;
      display: flex;
      align-items: center;
      gap: 6px;
    }

    .spec-content {
      color: var(--text-main);
      font-size: 12px;
    }

    .act-card {
      background: rgba(0, 0, 0, 0.3);
      border-left: 3px solid var(--primary-light);
      border-radius: 0 8px 8px 0;
      padding: 12px 16px;
      margin-bottom: 10px;
    }

    body.light-theme .act-card {
      background: #f1f5f9;
      border-left-color: #9333ea;
    }

    .act-title {
      font-family: 'JetBrains Mono', monospace;
      font-size: 11px;
      font-weight: 700;
      color: #c084fc;
      margin-bottom: 4px;
      text-transform: uppercase;
    }

    body.light-theme .act-title {
      color: #7e22ce;
    }

    .act-text {
      font-size: 12px;
      color: var(--text-main);
      line-height: 1.5;
    }
"""

if "/* 📸 EDITORIAL DOSSIER PROFILE CARD" not in html:
    html = html.replace("    /* Scrollbars */", editorial_css + "\n    /* Scrollbars */")
    print("Added Editorial Dossier CSS.")

# Let's craft the new tab-perfiles matching the exact layout of the user's uploaded photo!
new_editorial_tab_perfiles = """      <section id="tab-perfiles" class="tab-view active">
        <!-- Sub-Pestañas Plataformas -->
        <div class="subtabs-bar">
          <button class="subtab-btn active" onclick="switchSubTab('sub-perfil', 'streamate', this)">
            <i data-lucide="zap"></i> Streamate (Dossier Editorial)
          </button>
          <button class="subtab-btn" onclick="switchSubTab('sub-perfil', 'loyalfans', this)">
            <i data-lucide="gem"></i> LoyalFans (Dossier Editorial)
          </button>
          <button class="subtab-btn" onclick="switchSubTab('sub-perfil', 'stripchat', this)">
            <i data-lucide="flame"></i> Stripchat (Dossier Editorial)
          </button>
          <button class="subtab-btn" onclick="switchSubTab('sub-perfil', 'credenciales-grid', this)">
            <i data-lucide="key"></i> Resumen de Todas las Credenciales
          </button>
        </div>

        <!-- 1. STREAMATE EDITORIAL DOSSIER CARD -->
        <div id="sub-perfil-streamate" class="sub-tab-content">
          <div class="editorial-card">
            <div class="editorial-hero-banner">
              <div style="display: flex; align-items: center; gap: 12px;">
                <span class="editorial-badge" style="background: rgba(245, 158, 11, 0.15); color: #fbbf24; border: 1px solid rgba(245, 158, 11, 0.4);">
                  <i data-lucide="zap" style="width:13px; height:13px;"></i> STREAMATE MODELS • LIVE DOSSIER
                </span>
                <span class="table-badge badge-success">✓ Verified & Compliance 2257 Approved</span>
              </div>
              <div style="display: flex; gap: 8px;">
                <a href="https://streamatemodels.com/login" target="_blank" class="action-btn" style="font-size: 11px; text-decoration:none;">
                  <i data-lucide="log-in" style="width:12px; height:12px;"></i> Portal Modelo
                </a>
                <a href="https://sambartone.cammodels.com" target="_blank" class="action-btn primary" style="font-size: 11px; text-decoration:none;">
                  <i data-lucide="external-link" style="width:12px; height:12px;"></i> Ver en Vivo
                </a>
              </div>
            </div>

            <div class="editorial-body">
              <!-- COLUMNA IZQUIERDA: HERO PORTRAIT & SPECS TÉCNICOS -->
              <div class="editorial-left-col">
                <div class="editorial-portrait-frame">
                  <img src="artifacts/streamate_audit/profile.png" alt="Sam Barton Editorial Portrait">
                  <div class="editorial-portrait-overlay">
                    <strong style="color: #fff; font-size: 18px; font-weight: 800;">SamBartone</strong>
                    <div style="font-size: 11px; color: #fbbf24; display: flex; align-items: center; gap: 6px;">
                      <span>PID: 144675665</span> • <span>Rating: 4.0 ★</span> • <span>Colombia | 22</span>
                    </div>
                  </div>
                </div>

                <!-- IDENTITY ANCHOR (COMO EN LA IMAGEN DE REFERENCIA) -->
                <div class="editorial-anchor-box">
                  <img src="artifacts/streamate_audit/profile.png" alt="Reference Thumbnail" class="editorial-anchor-thumb">
                  <div style="flex:1;">
                    <div style="font-family:'JetBrains Mono',monospace; font-size:10px; color:#10b981; font-weight:700;">IDENTITY ANCHOR (FOTO REAL SFW)</div>
                    <div style="font-size:11px; color:var(--text-main); font-weight:600;">Sam Barton • Tomboy Versátil</div>
                    <div style="font-size:10px; color:var(--text-muted);">Aprobada por Streamate Compliance • Chaqueta y corte tomboy</div>
                  </div>
                </div>

                <!-- CREDENCIALES ACCESO DIRECTO -->
                <div class="spec-block" style="border-left: 3px solid #fbbf24;">
                  <div class="spec-label"><i data-lucide="lock" style="width:12px; height:12px;"></i> ACCESO & CREDENCIALES (CENTENARIO STUDIO)</div>
                  
                  <div style="display:flex; justify-content:space-between; align-items:center; margin-top:8px; font-size:12px;">
                    <span style="color:var(--text-dim);">Usuario / Email:</span>
                    <div style="display:flex; align-items:center; gap:6px;">
                      <code style="color:var(--secondary); font-family:var(--font-mono); font-size:11px;">efac05@yopmail.com</code>
                      <button class="action-btn" style="padding:2px 6px; font-size:10px;" onclick="copyToClipboard('efac05@yopmail.com', this)">
                        <i data-lucide="copy" style="width:11px; height:11px;"></i>
                      </button>
                    </div>
                  </div>

                  <div style="display:flex; justify-content:space-between; align-items:center; margin-top:8px; font-size:12px;">
                    <span style="color:var(--text-dim);">Contraseña:</span>
                    <div style="display:flex; align-items:center; gap:6px;">
                      <input type="password" id="pwd-sm-card" value="Centenario123@" readonly style="background:transparent; border:none; color:var(--primary-light); font-family:var(--font-mono); font-size:11px; width:110px; outline:none;">
                      <button class="action-btn" style="padding:2px 6px; font-size:10px;" onclick="togglePasswordVisibility('pwd-sm-card', this)">
                        <i data-lucide="eye" style="width:11px; height:11px;"></i>
                      </button>
                      <button class="action-btn" style="padding:2px 6px; font-size:10px;" onclick="copyToClipboard('Centenario123@', this)">
                        <i data-lucide="copy" style="width:11px; height:11px;"></i>
                      </button>
                    </div>
                  </div>

                  <div style="display:grid; grid-template-columns: 1fr 1fr; gap:6px; margin-top:12px; padding-top:10px; border-top:1px solid rgba(255,255,255,0.06); font-size:11px;">
                    <div>Tarifa Privado: <strong style="color:#fbbf24;">$2.99 / min</strong></div>
                    <div>Tarifa Exclusivo: <strong style="color:#fbbf24;">$3.99 / min</strong></div>
                    <div>Geobloqueo: <strong style="color:#34d399;">Colombia Abierto</strong></div>
                    <div>Vello Púbico: <strong>Trimmed (Recortado)</strong></div>
                  </div>
                </div>
              </div>

              <!-- COLUMNA DERECHA: PROMPT NARRATIVO Y DIRECCIÓN EDITORIAL EN 4 ACTOS -->
              <div class="editorial-right-col">
                <div class="editorial-prompt-title">
                  <i data-lucide="terminal" style="width:24px; height:24px;"></i> Prompt & Narrative Architecture
                </div>

                <div class="spec-block">
                  <div class="spec-label">ROLE & AESTHETIC (ROL & IDENTIDAD CENTRAL)</div>
                  <div class="spec-content">
                    Chica tomboy versatil con energia propia, mirada directa e inteligente. Apasionada por la musica, el ukelele, la tecnologia, el deporte y esa curiosidad constante por explorar el deseo sin poses fingidas ni sumision forzada.
                  </div>
                </div>

                <!-- LOS 4 ACTOS NARRATIVOS (LISTOS PARA COPIAR CON UN BOTÓN) -->
                <div>
                  <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:10px;">
                    <div class="spec-label" style="margin-bottom:0;"><i data-lucide="book-open" style="width:12px; height:12px;"></i> NARRATIVA OFICIAL EN 4 ACTOS (SIN TILDES NI EMOJIS)</div>
                    <button class="action-btn" style="padding:3px 10px; font-size:11px;" onclick="copyAllActsStreamate(this)">
                      <i data-lucide="copy" style="width:12px; height:12px;"></i> Copiar los 4 Actos
                    </button>
                  </div>

                  <div class="act-card">
                    <div class="act-title">Acto 1. Titular / Bio Corta (El Gancho)</div>
                    <div class="act-text">Chica tomboy versatil con energia propia e inteligente. Curiosa y directa. Me gusta la buena charla, la picardia natural y conectar de verdad.</div>
                  </div>

                  <div class="act-card">
                    <div class="act-title">Acto 2. Sobre Mi / About Me (Música, Ukelele e Intimidad)</div>
                    <div class="act-text">Mi mundo se mueve entre la musica, la tecnologia, el deporte y esa pasion constante por explorar el deseo. Toco el ukelele, pero tambien disfruto explorar sensaciones intensas a solas. Tengo una piel sensible que reacciona rapido al calor del momento, una sonrisa picara que tienta y una entrega total cuando alguien sabe encenderme sin frenos.</div>
                  </div>

                  <div class="act-card">
                    <div class="act-title">Acto 3. Que Me Excita / Turn Ons (Tensión Visual & Vibraciones)</div>
                    <div class="act-text">Me enciende poder ver tus reacciones y poder sostener tu mirada fija donde no hacen falta palabras. Tambien me encienden las vibraciones inesperadas recorriendo mi piel, sentir como sube el calor despacio y esa complicidad donde ambos sabemos lo que queremos.</div>
                  </div>

                  <div class="act-card">
                    <div class="act-title">Acto 4. Mis Especialidades / Expertise (Momentos de Intimidad & Control)</div>
                    <div class="act-text">Dejar que la curiosidad abra paso a momentos de intimidad, permitiendo experimentar y alternar el control, vivir fantasias y dejarnos llevar sin ataduras. Me gusta empezar suave, provocar con calma y luego acelerar el ritmo cuando el calor sube, hablando al oido y complaciendo caprichos mutuos donde ambos terminamos completamente satisfechos.</div>
                  </div>
                </div>

                <!-- SPECS TÉCNICOS ADICIONALES (COMO LA IMAGEN) -->
                <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 14px;">
                  <div class="spec-block">
                    <div class="spec-label">EXPRESSION & CONNECTION</div>
                    <div style="font-size: 11px; color: var(--text-muted); line-height: 1.5;">
                      Mirada fija sosteniendo el lente, complicidad visual sin titubeos. Contacto de cámara mutua (Cam2Cam) sin mencionar encuentros personales.
                    </div>
                  </div>
                  <div class="spec-block">
                    <div class="spec-label">TECHNICAL HARDWARE</div>
                    <div style="font-size: 11px; color: var(--text-muted); line-height: 1.5;">
                      Cámara: OBS Virtual Cam • Micrófono: Logitech • Lovense: Sincronizado por Bluetooth con 5 niveles de vibración.
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- 2. LOYALFANS EDITORIAL DOSSIER CARD -->
        <div id="sub-perfil-loyalfans" class="sub-tab-content" style="display:none;">
          <div class="editorial-card">
            <div class="editorial-hero-banner">
              <div style="display: flex; align-items: center; gap: 12px;">
                <span class="editorial-badge" style="background: rgba(147, 51, 234, 0.15); color: #c084fc; border: 1px solid rgba(147, 51, 234, 0.4);">
                  <i data-lucide="gem" style="width:13px; height:13px;"></i> LOYALFANS • LIVE DOSSIER
                </span>
                <span class="table-badge badge-success">✓ 100% Creadora Directa (Top 23%)</span>
              </div>
              <div style="display: flex; gap: 8px;">
                <a href="https://loyalfans.com/login" target="_blank" class="action-btn" style="font-size: 11px; text-decoration:none;">
                  <i data-lucide="log-in" style="width:12px; height:12px;"></i> Iniciar Sesión
                </a>
                <a href="https://loyalfans.com/samm_bartonn" target="_blank" class="action-btn primary" style="font-size: 11px; text-decoration:none;">
                  <i data-lucide="external-link" style="width:12px; height:12px;"></i> Perfil Público
                </a>
              </div>
            </div>

            <div class="editorial-body">
              <div class="editorial-left-col">
                <div class="editorial-portrait-frame">
                  <img src="artifacts/test_public_profile_verified.png" alt="Sam Barton LoyalFans Portrait">
                  <div class="editorial-portrait-overlay">
                    <strong style="color: #fff; font-size: 18px; font-weight: 800;">Sam Barton</strong>
                    <div style="font-size: 11px; color: #c084fc;">@samm_bartonn • Top 23% Platform Rank</div>
                  </div>
                </div>

                <div class="spec-block" style="border-left: 3px solid #c084fc;">
                  <div class="spec-label"><i data-lucide="lock" style="width:12px; height:12px;"></i> ACCESO DIRECTO LOYALFANS</div>
                  <div style="display:flex; justify-content:space-between; align-items:center; margin-top:8px; font-size:12px;">
                    <span style="color:var(--text-dim);">Usuario:</span>
                    <code style="color:var(--secondary); font-family:var(--font-mono); font-size:11px;">sambartonn23@gmail.com</code>
                  </div>
                  <div style="display:flex; justify-content:space-between; align-items:center; margin-top:8px; font-size:12px;">
                    <span style="color:var(--text-dim);">Contraseña:</span>
                    <div style="display:flex; align-items:center; gap:6px;">
                      <input type="password" id="pwd-lf-card" value="Kjc20009*" readonly style="background:transparent; border:none; color:var(--primary-light); font-family:var(--font-mono); font-size:11px; width:90px; outline:none;">
                      <button class="action-btn" style="padding:2px 6px; font-size:10px;" onclick="togglePasswordVisibility('pwd-lf-card', this)">
                        <i data-lucide="eye" style="width:11px; height:11px;"></i>
                      </button>
                      <button class="action-btn" style="padding:2px 6px; font-size:10px;" onclick="copyToClipboard('Kjc20009*', this)">
                        <i data-lucide="copy" style="width:11px; height:11px;"></i>
                      </button>
                    </div>
                  </div>
                </div>
              </div>

              <div class="editorial-right-col">
                <div class="editorial-prompt-title" style="color: #c084fc;">
                  <i data-lucide="sparkles" style="width:24px; height:24px;"></i> LoyalFans Architectural Bio
                </div>
                <div class="spec-block">
                  <div class="spec-label">ENGLISH OUTBOUND OFFICIAL COPY</div>
                  <div class="act-card" style="border-left-color: #c084fc;">
                    <div class="act-text" style="white-space: pre-wrap; font-size:12px;">🐺 Sam Barton | Software & AI Architect ⚡ Versatile Tomboy 🏍️

Smart by day, driven about my goals, and teasingly wicked by night.

Software & AI Architect by trade, but my real sanctuary is motorcycles, speed, and my beloved pack: my dogs and my 2 cats are my greatest blessings in this world 🐾🐈. Gym addict, soccer player, late-night sketcher, and an absolute InuYasha devotee 🍙. I also play the ukulele and sing straight from the heart.

Obsessed with neon in the dark, skulls, and eerie October vibes 💀✨. Working hard every single day to buy my used car in December 🚗 and escape to Cancun 🌴.

Want my attention? Be respectful, intelligent, different, and abnormal. Generic, boring guys bore me to death. If you're a real man who knows how to treat a girl, I just might let you take the wheel... under my explicit permission. 😈⚡</div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- 3. STRIPCHAT EDITORIAL DOSSIER CARD -->
        <div id="sub-perfil-stripchat" class="sub-tab-content" style="display:none;">
          <div class="editorial-card">
            <div class="editorial-hero-banner">
              <div style="display: flex; align-items: center; gap: 12px;">
                <span class="editorial-badge" style="background: rgba(244, 63, 94, 0.15); color: #f43f5e; border: 1px solid rgba(244, 63, 94, 0.4);">
                  <i data-lucide="flame" style="width:13px; height:13px;"></i> STRIPCHAT • LIVE DOSSIER
                </span>
                <span class="table-badge badge-info">✓ Tokens & Lovense Synced</span>
              </div>
              <div style="display: flex; gap: 8px;">
                <a href="https://stripchat.com/login" target="_blank" class="action-btn" style="font-size: 11px; text-decoration:none;">
                  <i data-lucide="log-in" style="width:12px; height:12px;"></i> Acceder Portal
                </a>
                <a href="https://stripchat.com/sam_barton" target="_blank" class="action-btn primary" style="font-size: 11px; text-decoration:none;">
                  <i data-lucide="external-link" style="width:12px; height:12px;"></i> Sala Pública
                </a>
              </div>
            </div>

            <div class="editorial-body">
              <div class="editorial-left-col">
                <div class="editorial-portrait-frame">
                  <img src="artifacts/stripchat_profile_updated_20261014_211003.png" alt="Sam Barton Stripchat Portrait">
                  <div class="editorial-portrait-overlay">
                    <strong style="color: #fff; font-size: 18px; font-weight: 800;">Sam Barton</strong>
                    <div style="font-size: 11px; color: #f43f5e;">@sam_barton • Tokens & Interactive Toys</div>
                  </div>
                </div>

                <div class="spec-block" style="border-left: 3px solid #f43f5e;">
                  <div class="spec-label"><i data-lucide="lock" style="width:12px; height:12px;"></i> ACCESO DIRECTO STRIPCHAT</div>
                  <div style="display:flex; justify-content:space-between; align-items:center; margin-top:8px; font-size:12px;">
                    <span style="color:var(--text-dim);">Usuario:</span>
                    <code style="color:var(--secondary); font-family:var(--font-mono); font-size:11px;">sambartonn23@gmail.com</code>
                  </div>
                  <div style="display:flex; justify-content:space-between; align-items:center; margin-top:8px; font-size:12px;">
                    <span style="color:var(--text-dim);">Contraseña:</span>
                    <div style="display:flex; align-items:center; gap:6px;">
                      <input type="password" id="pwd-sc-card" value="6L!3K3RUnEdPKPt" readonly style="background:transparent; border:none; color:var(--primary-light); font-family:var(--font-mono); font-size:11px; width:90px; outline:none;">
                      <button class="action-btn" style="padding:2px 6px; font-size:10px;" onclick="togglePasswordVisibility('pwd-sc-card', this)">
                        <i data-lucide="eye" style="width:11px; height:11px;"></i>
                      </button>
                      <button class="action-btn" style="padding:2px 6px; font-size:10px;" onclick="copyToClipboard('6L!3K3RUnEdPKPt', this)">
                        <i data-lucide="copy" style="width:11px; height:11px;"></i>
                      </button>
                    </div>
                  </div>
                </div>
              </div>

              <div class="editorial-right-col">
                <div class="editorial-prompt-title" style="color: #f43f5e;">
                  <i data-lucide="flame" style="width:24px; height:24px;"></i> Stripchat Interactive Narrative
                </div>
                <div class="spec-block">
                  <div class="spec-label">TOPIC & LOVENSE LIVE PROMPT</div>
                  <div class="act-card" style="border-left-color: #f43f5e;">
                    <div class="act-text" style="white-space: pre-wrap; font-size:12px;">🐺 Sam Barton | Cute Tomboy Gamer ⚡ Lovense Interactive 🏍️

Software & AI Architect by day, gaming tomboy & teasing companion by night.
Soccer player, motorcycle enthusiast, and devoted mom to my dogs & 2 cats 🐾.
InuYasha devotee 🍙, indie music lover & ukulele player 🎶.

Obsessed with neon in the dark, skulls, and Halloween vibes 💀✨.
Working hard every single day to buy my used car in December 🚗 and escape to Cancun 🌴!

💖 LOVENSE SYNCED:
My toys are active and connect directly to every tip! Send tokens to make me buzz, trigger reactions, or take me into Private / Exclusive for full control 😈🖤.</div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- 4. GRID DE TODAS LAS CREDENCIALES COMPACTAS -->
        <div id="sub-perfil-credenciales-grid" class="sub-tab-content" style="display:none;">
          <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 18px;">
            <!-- STREAMATE -->
            <div class="platform-profile-card" style="border-top: 3px solid #f59e0b;">
              <div class="platform-header-row">
                <strong style="color:#fbbf24;">Streamate Models</strong>
                <span class="table-badge badge-warning">Estudio</span>
              </div>
              <div>Usuario: <code>efac05@yopmail.com</code></div>
              <div>Clave: <code>Centenario123@</code></div>
            </div>
            <!-- LOYALFANS -->
            <div class="platform-profile-card" style="border-top: 3px solid #9333ea;">
              <div class="platform-header-row">
                <strong style="color:#c084fc;">LoyalFans</strong>
                <span class="table-badge badge-success">Directo</span>
              </div>
              <div>Usuario: <code>sambartonn23@gmail.com</code></div>
              <div>Clave: <code>Kjc20009*</code></div>
            </div>
            <!-- STRIPCHAT -->
            <div class="platform-profile-card" style="border-top: 3px solid #f43f5e;">
              <div class="platform-header-row">
                <strong style="color:#f43f5e;">Stripchat</strong>
                <span class="table-badge badge-info">Tokens</span>
              </div>
              <div>Usuario: <code>sambartonn23@gmail.com</code></div>
              <div>Clave: <code>6L!3K3RUnEdPKPt</code></div>
            </div>
            <!-- LOVENSE -->
            <div class="platform-profile-card" style="border-top: 3px solid #06b6d4;">
              <div class="platform-header-row">
                <strong style="color:#38bdf8;">Lovense Connect</strong>
                <span class="table-badge badge-purple">Hardware</span>
              </div>
              <div>Usuario: <code>sambartonn23@gmail.com</code></div>
              <div>Clave: <code>6L!3K3RUnEdPKPt</code></div>
            </div>
          </div>
        </div>
      </section>"""

# Replace tab-perfiles
pattern = re.compile(r'<section id="tab-perfiles".*?</section>', re.DOTALL)
if pattern.search(html):
    html = pattern.sub(new_editorial_tab_perfiles, html, count=1)
    print("Replaced tab-perfiles with Editorial Dossier layout!")
else:
    print("Could not match tab-perfiles.")

# Helper JS function to copy all 4 acts for Streamate
copy_helper_js = """
    function copyAllActsStreamate(btn) {
      const actsText = `Acto 1. Titular / Bio Corta:
Chica tomboy versatil con energia propia e inteligente. Curiosa y directa. Me gusta la buena charla, la picardia natural y conectar de verdad.

Acto 2. Sobre Mi / About Me:
Mi mundo se mueve entre la musica, la tecnologia, el deporte y esa pasion constante por explorar el deseo. Toco el ukelele, pero tambien disfruto explorar sensaciones intensas a solas. Tengo una piel sensible que reacciona rapido al calor del momento, una sonrisa picara que tienta y una entrega total cuando alguien sabe encenderme sin frenos.

Acto 3. Que Me Excita / Turn Ons:
Me enciende poder ver tus reacciones y poder sostener tu mirada fija donde no hacen falta palabras. Tambien me encienden las vibraciones inesperadas recorriendo mi piel, sentir como sube el calor despacio y esa complicidad donde ambos sabemos lo que queremos.

Acto 4. Mis Especialidades / Expertise:
Dejar que la curiosidad abra paso a momentos de intimidad, permitiendo experimentar y alternar el control, vivir fantasias y dejarnos llevar sin ataduras. Me gusta empezar suave, provocar con calma y luego acelerar el ritmo cuando el calor sube, hablando al oido y complaciendo caprichos mutuos donde ambos terminamos completamente satisfechos.`;
      
      navigator.clipboard.writeText(actsText).then(() => {
        const oldHtml = btn.innerHTML;
        btn.innerHTML = '<span style=\"color:#10b981; font-weight:700;\">✓ ¡Copiados los 4 Actos!</span>';
        showToast('Los 4 Actos de Streamate copiados al portapapeles');
        setTimeout(() => {
          btn.innerHTML = oldHtml;
          lucide.createIcons();
        }, 2200);
      });
    }
"""

if "function copyAllActsStreamate" not in html:
    html = html.replace("    function copyToClipboard(text, btn) {", copy_helper_js + "\n    function copyToClipboard(text, btn) {")
    print("Added copyAllActsStreamate helper.")

with open(INDEX_PATH, "w", encoding="utf-8") as f:
    f.write(html)

print("Editorial redesign applied to index.html!")
