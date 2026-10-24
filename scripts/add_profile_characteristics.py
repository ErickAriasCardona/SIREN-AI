import re
from pathlib import Path

html_path = Path("index.html")
content = html_path.read_text(encoding="utf-8")

# 1. Add CSS for specs-grid-table and light theme
css_specs = """
    /* SPECS GRID TABLE FOR EDITORIAL DOSSIER */
    .specs-grid-table {
      display: grid;
      grid-template-columns: repeat(2, 1fr);
      gap: 6px 14px;
      font-size: 11px;
    }
    .spec-item {
      display: flex;
      justify-content: space-between;
      align-items: center;
      padding: 3px 0;
      border-bottom: 1px solid rgba(255, 255, 255, 0.06);
    }
    .spec-item .label {
      color: var(--text-dim);
      font-size: 10.5px;
    }
    .spec-item .value {
      color: #fff;
      font-weight: 600;
      font-size: 11px;
      text-align: right;
    }
    .spec-section-divider {
      font-size: 10px;
      font-weight: 800;
      text-transform: uppercase;
      letter-spacing: 0.8px;
      color: #fbbf24;
      margin: 10px 0 6px 0;
      display: flex;
      align-items: center;
      gap: 5px;
      border-top: 1px solid rgba(255, 255, 255, 0.08);
      padding-top: 8px;
    }
    body.light-theme .spec-item {
      border-bottom-color: #e2e8f0;
    }
    body.light-theme .spec-item .value {
      color: #0f172a;
    }
    body.light-theme .spec-section-divider {
      border-top-color: #e2e8f0;
      color: #b45309;
    }
"""

if ".specs-grid-table" not in content:
    content = content.replace("</style>", f"{css_specs}\n  </style>")
    print("Added specs-grid-table CSS.")

# 2. Complete characteristics block for Streamate
streamate_specs_html = """                <!-- CREDENCIALES Y TODAS LAS CARACTERÍSTICAS DEL PERFIL STREAMATE -->
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

                  <!-- TARIFAS Y PARÁMETROS COMERCIALES -->
                  <div class="spec-section-divider">
                    <i data-lucide="dollar-sign" style="width:11px; height:11px;"></i> Tarifas & Parámetros Comerciales
                  </div>
                  <div class="specs-grid-table">
                    <div class="spec-item">
                      <span class="label">Tarifa Privado:</span>
                      <span class="value" style="color:#fbbf24;">$2.99 / min</span>
                    </div>
                    <div class="spec-item">
                      <span class="label">Tarifa Exclusivo:</span>
                      <span class="value" style="color:#fbbf24;">$3.99 / min</span>
                    </div>
                    <div class="spec-item">
                      <span class="label">Rango Dinámico:</span>
                      <span class="value">$2.99 - $6.99</span>
                    </div>
                    <div class="spec-item">
                      <span class="label">Llamada Video/Voz:</span>
                      <span class="value">$3.99 / $2.99</span>
                    </div>
                    <div class="spec-item">
                      <span class="label">Geobloqueo:</span>
                      <span class="value" style="color:#34d399;">Colombia Abierto</span>
                    </div>
                    <div class="spec-item">
                      <span class="label">Rating / Estado:</span>
                      <span class="value">4.0 ★ (Verificado)</span>
                    </div>
                  </div>

                  <!-- CARACTERÍSTICAS FÍSICAS Y BIOMETRÍA -->
                  <div class="spec-section-divider">
                    <i data-lucide="user" style="width:11px; height:11px;"></i> Características Físicas & Biometría
                  </div>
                  <div class="specs-grid-table">
                    <div class="spec-item">
                      <span class="label">Estatura:</span>
                      <span class="value">1.60 m (5'3")</span>
                    </div>
                    <div class="spec-item">
                      <span class="label">Peso:</span>
                      <span class="value">55 kg (121 lbs)</span>
                    </div>
                    <div class="spec-item">
                      <span class="label">Medidas:</span>
                      <span class="value">89 - 61 - 94 cm</span>
                    </div>
                    <div class="spec-item">
                      <span class="label">Copa / Busto:</span>
                      <span class="value">B (Natural)</span>
                    </div>
                    <div class="spec-item">
                      <span class="label">Color de Ojos:</span>
                      <span class="value">Brown (Castaños)</span>
                    </div>
                    <div class="spec-item">
                      <span class="label">Color de Cabello:</span>
                      <span class="value">Black (Negro)</span>
                    </div>
                    <div class="spec-item">
                      <span class="label">Complexión:</span>
                      <span class="value">Average (Proporcionada)</span>
                    </div>
                    <div class="spec-item">
                      <span class="label">Etnicidad:</span>
                      <span class="value">White / Latina</span>
                    </div>
                    <div class="spec-item" style="grid-column: span 2;">
                      <span class="label">Vello Púbico:</span>
                      <span class="value" style="color:#38bdf8;">Trimmed (Recortado) • <em>Auditado en portal: Hairy</em></span>
                    </div>
                  </div>

                  <!-- IDENTIDAD, IDIOMAS Y ATRIBUTOS -->
                  <div class="spec-section-divider">
                    <i data-lucide="sparkles" style="width:11px; height:11px;"></i> Identidad, Idiomas & Preferencias
                  </div>
                  <div class="specs-grid-table">
                    <div class="spec-item">
                      <span class="label">Edad Oficial:</span>
                      <span class="value">22 años</span>
                    </div>
                    <div class="spec-item">
                      <span class="label">Signo Zodiacal:</span>
                      <span class="value">Taurus (Tauro) ♉</span>
                    </div>
                    <div class="spec-item">
                      <span class="label">Orientación:</span>
                      <span class="value">Bisexual</span>
                    </div>
                    <div class="spec-item">
                      <span class="label">Género:</span>
                      <span class="value">Female (Mujer)</span>
                    </div>
                    <div class="spec-item" style="grid-column: span 2;">
                      <span class="label">Idiomas:</span>
                      <span class="value">English, Spanish, French, Portuguese</span>
                    </div>
                  </div>

                  <!-- ATRIBUTOS KINKY & PRÁCTICAS CONFIGURADAS EN STREAMATE -->
                  <div class="spec-section-divider">
                    <i data-lucide="tag" style="width:11px; height:11px;"></i> Tags & Atributos Registrados
                  </div>
                  <div style="display:flex; flex-wrap:wrap; gap:5px; margin-top:6px;">
                    <span class="table-badge badge-warning" style="font-size:10px;">Roleplay</span>
                    <span class="table-badge badge-info" style="font-size:10px;">Interactive Vibrator</span>
                    <span class="table-badge badge-purple" style="font-size:10px;">Cam2Cam</span>
                    <span class="table-badge badge-success" style="font-size:10px;">Tomboy</span>
                    <span class="table-badge" style="font-size:10px; background:rgba(255,255,255,0.06); color:var(--text-muted);">Submissive</span>
                    <span class="table-badge" style="font-size:10px; background:rgba(255,255,255,0.06); color:var(--text-muted);">Anal</span>
                    <span class="table-badge" style="font-size:10px; background:rgba(255,255,255,0.06); color:var(--text-muted);">Deepthroat</span>
                  </div>

                </div>"""

# Find the credentials block in sub-perfil-streamate and replace it
old_block_pattern = re.compile(
    r'<!-- CREDENCIALES ACCESO DIRECTO -->\s*<div class="spec-block" style="border-left: 3px solid #fbbf24;">.*?</div>\s*</div>\s*</div>\s*<!-- COLUMNA DERECHA',
    re.DOTALL
)

if old_block_pattern.search(content):
    content = old_block_pattern.sub(f"{streamate_specs_html}\n              </div>\n\n              <!-- COLUMNA DERECHA", content)
    print("Replaced Streamate specs block with full characteristics sheet!")
else:
    # Try alternate match
    alt_pattern = re.compile(
        r'<div class="spec-block" style="border-left: 3px solid #fbbf24;">.*?Tarifa Privado:.*?</div>\s*</div>\s*</div>\s*<!-- COLUMNA DERECHA',
        re.DOTALL
    )
    if alt_pattern.search(content):
        content = alt_pattern.sub(f"{streamate_specs_html}\n              </div>\n\n              <!-- COLUMNA DERECHA", content)
        print("Replaced Streamate specs block via alt pattern!")
    else:
        print("Could not find the Streamate specs block in index.html!")

html_path.write_text(content, encoding="utf-8")
print("Saved index.html successfully!")
