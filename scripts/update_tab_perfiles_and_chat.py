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

# Let's prepare the new tab-perfiles content
new_tab_perfiles = """      <section id="tab-perfiles" class="tab-view active">
        <!-- Sub-Pestañas Plataformas -->
        <div class="subtabs-bar">
          <button class="subtab-btn active" onclick="switchSubTab('sub-perfil', 'todas', this)">
            <i data-lucide="layers"></i> Resumen de Todas las Cuentas
          </button>
          <button class="subtab-btn" onclick="switchSubTab('sub-perfil', 'streamate', this)">
            <i data-lucide="zap"></i> Streamate (Auditoría & Cuenta Estudio)
          </button>
          <button class="subtab-btn" onclick="switchSubTab('sub-perfil', 'loyalfans', this)">
            <i data-lucide="gem"></i> LoyalFans (Directo)
          </button>
          <button class="subtab-btn" onclick="switchSubTab('sub-perfil', 'stripchat', this)">
            <i data-lucide="flame"></i> Stripchat (Tokens)
          </button>
        </div>

        <!-- VISTA RESUMEN DE TODAS LAS CUENTAS -->
        <div id="sub-perfil-todas" class="sub-tab-content">
          <div class="card" style="margin-bottom: 20px; border-left: 4px solid var(--primary-light);">
            <div class="card-title">
              <span>🔐 Acceso Centralizado a Cuentas y Credenciales de Sam Barton</span>
              <span class="badge" style="background: rgba(16, 185, 129, 0.2); color: #34d399;">4 Plataformas Registradas</span>
            </div>
            <p style="font-size: 13px; color: var(--text-muted); line-height: 1.5;">
              Visualización unificada de las cuentas oficiales de transmisión. Incluye los accesos auditados, contraseñas seguras desencriptadas localmente con visualizador de privacidad, enlaces directos de creador y perfil público con fotos reales.
            </p>
          </div>

          <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(320px, 1fr)); gap: 20px;">

            <!-- CARD STREAMATE -->
            <div class="platform-profile-card" style="border-top: 3px solid #f59e0b;">
              <div class="platform-header-row">
                <div class="platform-badge-tag tag-streamate" style="background: rgba(245, 158, 11, 0.15); color: #fbbf24; border: 1px solid rgba(245, 158, 11, 0.3);">
                  <i data-lucide="zap"></i> STREAMATE MODELS
                </div>
                <span class="table-badge badge-warning">✓ Cuenta Estudio (Verified)</span>
              </div>

              <div style="display: flex; gap: 14px; align-items: center;">
                <img src="/artifacts/streamate_audit/profile.png" alt="SamBartone Avatar" style="width: 58px; height: 58px; border-radius: 50%; object-fit: cover; border: 2px solid #fbbf24; box-shadow: 0 4px 12px rgba(245, 158, 11, 0.3);">
                <div>
                  <h3 style="font-size: 16px; color: var(--text-main); font-weight: 700;">SamBartone</h3>
                  <div style="font-size: 11px; color: var(--text-dim);">PID: <strong>144675665</strong> • Rating: <strong style="color: #fbbf24;">4.0 ★</strong></div>
                  <div style="font-size: 11px; color: var(--text-muted);">Estudio Administrador: <strong>Centenario Studio</strong></div>
                </div>
              </div>

              <div class="credential-box" style="background: rgba(0,0,0,0.25); border: 1px solid var(--border-color); border-radius: 8px; padding: 12px; display: flex; flex-direction: column; gap: 8px;">
                <div style="display:flex; justify-content:space-between; align-items:center; font-size:12px;">
                  <span style="color: var(--text-dim);">Usuario / Email:</span>
                  <div style="display:flex; align-items:center; gap:6px;">
                    <code style="color: var(--secondary); font-family: var(--font-mono); font-size: 11px;">efac05@yopmail.com</code>
                    <button class="action-btn" style="padding: 2px 6px; font-size: 10px;" onclick="copyToClipboard('efac05@yopmail.com', this)" title="Copiar usuario">
                      <i data-lucide="copy" style="width:11px; height:11px;"></i>
                    </button>
                  </div>
                </div>

                <div style="display:flex; justify-content:space-between; align-items:center; font-size:12px;">
                  <span style="color: var(--text-dim);">Contraseña:</span>
                  <div style="display:flex; align-items:center; gap:6px;">
                    <input type="password" id="pwd-sm" value="Centenario123@" readonly style="background: transparent; border: none; color: var(--primary-light); font-family: var(--font-mono); font-size: 11px; width: 110px; outline: none;">
                    <button class="action-btn" style="padding: 2px 6px; font-size: 10px;" onclick="togglePasswordVisibility('pwd-sm', this)" title="Ver / Ocultar">
                      <i data-lucide="eye" style="width:11px; height:11px;"></i>
                    </button>
                    <button class="action-btn" style="padding: 2px 6px; font-size: 10px;" onclick="copyToClipboard('Centenario123@', this)" title="Copiar contraseña">
                      <i data-lucide="copy" style="width:11px; height:11px;"></i>
                    </button>
                  </div>
                </div>
              </div>

              <div style="font-size: 11px; color: var(--text-muted); display:flex; flex-direction:column; gap:4px;">
                <div>Tarifas en Vivo: <strong>Privado $2.99 / Exclusivo $3.99 min</strong></div>
                <div>Geobloqueo: <strong style="color: #34d399;">Colombia Visible (Sin Bloqueo)</strong></div>
              </div>

              <div style="display: flex; gap: 8px; margin-top: auto;">
                <a href="https://streamatemodels.com/login" target="_blank" class="action-btn" style="flex:1; text-align:center; text-decoration:none; font-size:11px; justify-content:center;">
                  <i data-lucide="log-in" style="width:12px; height:12px;"></i> Portal Modelo
                </a>
                <a href="https://sambartone.cammodels.com" target="_blank" class="action-btn primary" style="flex:1; text-align:center; text-decoration:none; font-size:11px; justify-content:center;">
                  <i data-lucide="external-link" style="width:12px; height:12px;"></i> Ver en Vivo
                </a>
              </div>
            </div>

            <!-- CARD LOYALFANS -->
            <div class="platform-profile-card" style="border-top: 3px solid #9333ea;">
              <div class="platform-header-row">
                <div class="platform-badge-tag tag-loyalfans">
                  <i data-lucide="gem"></i> LOYALFANS
                </div>
                <span class="table-badge badge-success">✓ 100% Creadora Directa</span>
              </div>

              <div style="display: flex; gap: 14px; align-items: center;">
                <img src="/artifacts/test_public_profile_verified.png" alt="LoyalFans Avatar" style="width: 58px; height: 58px; border-radius: 50%; object-fit: cover; border: 2px solid #c084fc; box-shadow: 0 4px 12px rgba(147, 51, 234, 0.3);">
                <div>
                  <h3 style="font-size: 16px; color: var(--text-main); font-weight: 700;">Sam Barton</h3>
                  <div style="font-size: 11px; color: var(--primary-light);">@samm_bartonn • <strong style="color: #34d399;">Top 23%</strong></div>
                  <div style="font-size: 11px; color: var(--text-muted);">Comisión Neta: <strong>80% para Sam (Directo)</strong></div>
                </div>
              </div>

              <div class="credential-box" style="background: rgba(0,0,0,0.25); border: 1px solid var(--border-color); border-radius: 8px; padding: 12px; display: flex; flex-direction: column; gap: 8px;">
                <div style="display:flex; justify-content:space-between; align-items:center; font-size:12px;">
                  <span style="color: var(--text-dim);">Usuario / Email:</span>
                  <div style="display:flex; align-items:center; gap:6px;">
                    <code style="color: var(--secondary); font-family: var(--font-mono); font-size: 11px;">sambartonn23@gmail.com</code>
                    <button class="action-btn" style="padding: 2px 6px; font-size: 10px;" onclick="copyToClipboard('sambartonn23@gmail.com', this)">
                      <i data-lucide="copy" style="width:11px; height:11px;"></i>
                    </button>
                  </div>
                </div>

                <div style="display:flex; justify-content:space-between; align-items:center; font-size:12px;">
                  <span style="color: var(--text-dim);">Contraseña:</span>
                  <div style="display:flex; align-items:center; gap:6px;">
                    <input type="password" id="pwd-lf" value="Kjc20009*" readonly style="background: transparent; border: none; color: var(--primary-light); font-family: var(--font-mono); font-size: 11px; width: 110px; outline: none;">
                    <button class="action-btn" style="padding: 2px 6px; font-size: 10px;" onclick="togglePasswordVisibility('pwd-lf', this)">
                      <i data-lucide="eye" style="width:11px; height:11px;"></i>
                    </button>
                    <button class="action-btn" style="padding: 2px 6px; font-size: 10px;" onclick="copyToClipboard('Kjc20009*', this)">
                      <i data-lucide="copy" style="width:11px; height:11px;"></i>
                    </button>
                  </div>
                </div>
              </div>

              <div style="font-size: 11px; color: var(--text-muted); display:flex; flex-direction:column; gap:4px;">
                <div>Mensajería: <strong>$0.50 texto / $0.50 foto</strong></div>
                <div>Suscripción Fan Club: <strong>$10.00 / mes</strong></div>
              </div>

              <div style="display: flex; gap: 8px; margin-top: auto;">
                <a href="https://loyalfans.com/login" target="_blank" class="action-btn" style="flex:1; text-align:center; text-decoration:none; font-size:11px; justify-content:center;">
                  <i data-lucide="log-in" style="width:12px; height:12px;"></i> Iniciar Sesión
                </a>
                <a href="https://loyalfans.com/samm_bartonn" target="_blank" class="action-btn primary" style="flex:1; text-align:center; text-decoration:none; font-size:11px; justify-content:center;">
                  <i data-lucide="external-link" style="width:12px; height:12px;"></i> Perfil Fans
                </a>
              </div>
            </div>

            <!-- CARD STRIPCHAT -->
            <div class="platform-profile-card" style="border-top: 3px solid #f43f5e;">
              <div class="platform-header-row">
                <div class="platform-badge-tag" style="background: rgba(244, 63, 94, 0.15); color: #f43f5e; border: 1px solid rgba(244, 63, 94, 0.3);">
                  <i data-lucide="flame"></i> STRIPCHAT
                </div>
                <span class="table-badge badge-info">✓ Tokens & Lovense</span>
              </div>

              <div style="display: flex; gap: 14px; align-items: center;">
                <img src="/artifacts/stripchat_profile_updated_20261014_211003.png" alt="Stripchat Avatar" style="width: 58px; height: 58px; border-radius: 50%; object-fit: cover; border: 2px solid #f43f5e; box-shadow: 0 4px 12px rgba(244, 63, 94, 0.3);">
                <div>
                  <h3 style="font-size: 16px; color: var(--text-main); font-weight: 700;">Sam Barton</h3>
                  <div style="font-size: 11px; color: #f43f5e;">@sam_barton • <strong>Listo en Cola</strong></div>
                  <div style="font-size: 11px; color: var(--text-muted);">Integración: <strong>Lovense Interactive ON</strong></div>
                </div>
              </div>

              <div class="credential-box" style="background: rgba(0,0,0,0.25); border: 1px solid var(--border-color); border-radius: 8px; padding: 12px; display: flex; flex-direction: column; gap: 8px;">
                <div style="display:flex; justify-content:space-between; align-items:center; font-size:12px;">
                  <span style="color: var(--text-dim);">Usuario / Email:</span>
                  <div style="display:flex; align-items:center; gap:6px;">
                    <code style="color: var(--secondary); font-family: var(--font-mono); font-size: 11px;">sambartonn23@gmail.com</code>
                    <button class="action-btn" style="padding: 2px 6px; font-size: 10px;" onclick="copyToClipboard('sambartonn23@gmail.com', this)">
                      <i data-lucide="copy" style="width:11px; height:11px;"></i>
                    </button>
                  </div>
                </div>

                <div style="display:flex; justify-content:space-between; align-items:center; font-size:12px;">
                  <span style="color: var(--text-dim);">Contraseña:</span>
                  <div style="display:flex; align-items:center; gap:6px;">
                    <input type="password" id="pwd-sc" value="6L!3K3RUnEdPKPt" readonly style="background: transparent; border: none; color: var(--primary-light); font-family: var(--font-mono); font-size: 11px; width: 110px; outline: none;">
                    <button class="action-btn" style="padding: 2px 6px; font-size: 10px;" onclick="togglePasswordVisibility('pwd-sc', this)">
                      <i data-lucide="eye" style="width:11px; height:11px;"></i>
                    </button>
                    <button class="action-btn" style="padding: 2px 6px; font-size: 10px;" onclick="copyToClipboard('6L!3K3RUnEdPKPt', this)">
                      <i data-lucide="copy" style="width:11px; height:11px;"></i>
                    </button>
                  </div>
                </div>
              </div>

              <div style="font-size: 11px; color: var(--text-muted); display:flex; flex-direction:column; gap:4px;">
                <div>Valor Token: <strong>$0.05 USD / token</strong></div>
                <div>Arquetipo: <strong>Cute Tomboy Gamer • Lovense Interactive</strong></div>
              </div>

              <div style="display: flex; gap: 8px; margin-top: auto;">
                <a href="https://stripchat.com/login" target="_blank" class="action-btn" style="flex:1; text-align:center; text-decoration:none; font-size:11px; justify-content:center;">
                  <i data-lucide="log-in" style="width:12px; height:12px;"></i> Acceder Portal
                </a>
                <a href="https://stripchat.com/sam_barton" target="_blank" class="action-btn primary" style="flex:1; text-align:center; text-decoration:none; font-size:11px; justify-content:center;">
                  <i data-lucide="external-link" style="width:12px; height:12px;"></i> Sala Pública
                </a>
              </div>
            </div>

            <!-- CARD LOVENSE -->
            <div class="platform-profile-card" style="border-top: 3px solid #06b6d4;">
              <div class="platform-header-row">
                <div class="platform-badge-tag" style="background: rgba(6, 182, 212, 0.15); color: #38bdf8; border: 1px solid rgba(6, 182, 212, 0.3);">
                  <i data-lucide="radio"></i> LOVENSE INTERACTIVE
                </div>
                <span class="table-badge badge-info">✓ Bluetooth Sync</span>
              </div>

              <div style="display: flex; gap: 14px; align-items: center;">
                <img src="/artifacts/streamate_audit/12_smconnect_ajustes.png" alt="Lovense Connect" style="width: 58px; height: 58px; border-radius: 50%; object-fit: cover; border: 2px solid #06b6d4; box-shadow: 0 4px 12px rgba(6, 182, 212, 0.3);">
                <div>
                  <h3 style="font-size: 16px; color: var(--text-main); font-weight: 700;">Lovense Connect</h3>
                  <div style="font-size: 11px; color: #38bdf8;">Juguetes Hápticos • <strong>5 Niveles</strong></div>
                  <div style="font-size: 11px; color: var(--text-muted);">Sincronización: <strong>Stripchat + Streamate</strong></div>
                </div>
              </div>

              <div class="credential-box" style="background: rgba(0,0,0,0.25); border: 1px solid var(--border-color); border-radius: 8px; padding: 12px; display: flex; flex-direction: column; gap: 8px;">
                <div style="display:flex; justify-content:space-between; align-items:center; font-size:12px;">
                  <span style="color: var(--text-dim);">Cuenta Lovense:</span>
                  <div style="display:flex; align-items:center; gap:6px;">
                    <code style="color: var(--secondary); font-family: var(--font-mono); font-size: 11px;">sambartonn23@gmail.com</code>
                    <button class="action-btn" style="padding: 2px 6px; font-size: 10px;" onclick="copyToClipboard('sambartonn23@gmail.com', this)">
                      <i data-lucide="copy" style="width:11px; height:11px;"></i>
                    </button>
                  </div>
                </div>

                <div style="display:flex; justify-content:space-between; align-items:center; font-size:12px;">
                  <span style="color: var(--text-dim);">Contraseña:</span>
                  <div style="display:flex; align-items:center; gap:6px;">
                    <input type="password" id="pwd-lv" value="6L!3K3RUnEdPKPt" readonly style="background: transparent; border: none; color: var(--primary-light); font-family: var(--font-mono); font-size: 11px; width: 110px; outline: none;">
                    <button class="action-btn" style="padding: 2px 6px; font-size: 10px;" onclick="togglePasswordVisibility('pwd-lv', this)">
                      <i data-lucide="eye" style="width:11px; height:11px;"></i>
                    </button>
                    <button class="action-btn" style="padding: 2px 6px; font-size: 10px;" onclick="copyToClipboard('6L!3K3RUnEdPKPt', this)">
                      <i data-lucide="copy" style="width:11px; height:11px;"></i>
                    </button>
                  </div>
                </div>
              </div>

              <div style="font-size: 11px; color: var(--text-muted); display:flex; flex-direction:column; gap:4px;">
                <div>Protocolo: <strong>Lovense Connect App (PC / Móvil)</strong></div>
                <div>Niveles: <strong>Bajo, Medio, Altura media, Alto, Muy alto</strong></div>
              </div>

              <div style="display: flex; gap: 8px; margin-top: auto;">
                <a href="https://streamate.lovense.com" target="_blank" class="action-btn" style="flex:1; text-align:center; text-decoration:none; font-size:11px; justify-content:center;">
                  <i data-lucide="radio" style="width:12px; height:12px;"></i> Lovense Streamate
                </a>
              </div>
            </div>

          </div>
        </div>

        <!-- PERFIL DETALLADO STREAMATE -->
        <div id="sub-perfil-streamate" class="sub-tab-content" style="display:none;">
          <div class="grid-2">
            <div class="platform-profile-card">
              <div class="platform-header-row">
                <div class="platform-badge-tag tag-streamate">
                  <i data-lucide="zap"></i> STREAMATE — Perfil Oficial Narrativo en 4 Actos
                </div>
                <span class="table-badge badge-warning">✓ Cuenta Estudio Activa</span>
              </div>
              <div style="display:flex; gap:12px; align-items:center;">
                <img src="/artifacts/streamate_audit/profile.png" alt="Sam" style="width:50px; height:50px; border-radius:50%; object-fit:cover; border:2px solid #fbbf24;">
                <div>
                  <strong style="font-size: 15px; color: var(--text-main);">SamBartone</strong>
                  <div style="font-size: 12px; color: #fbbf24; margin-top: 2px;">
                    Chica tomboy versatil con energia propia e inteligente
                  </div>
                </div>
              </div>

              <div class="bio-preview-box" style="white-space: pre-wrap; font-size: 12px; line-height: 1.6;"><strong>Acto 1. Titular / Bio Corta:</strong>
Chica tomboy versatil con energia propia e inteligente. Curiosa y directa. Me gusta la buena charla, la picardia natural y conectar de verdad.

<strong>Acto 2. Sobre Mi / About Me:</strong>
Mi mundo se mueve entre la musica, la tecnologia, el deporte y esa pasion constante por explorar el deseo. Toco el ukelele, pero tambien disfruto explorar sensaciones intensas a solas. Tengo una piel sensible que reacciona rapido al calor del momento, una sonrisa picara que tienta y una entrega total cuando alguien sabe encenderme sin frenos.

<strong>Acto 3. Que Me Excita / Turn Ons:</strong>
Me enciende poder ver tus reacciones y poder sostener tu mirada fija donde no hacen falta palabras. Tambien me encienden las vibraciones inesperadas recorriendo mi piel, sentir como sube el calor despacio y esa complicidad donde ambos sabemos lo que queremos.

<strong>Acto 4. Mis Especialidades / Expertise:</strong>
Dejar que la curiosidad abra paso a momentos de intimidad, permitiendo experimentar y alternar el control, vivir fantasias y dejarnos llevar sin ataduras. Me gusta empezar suave, provocar con calma y luego acelerar el ritmo cuando el calor sube, hablando al oido y complaciendo caprichos mutuos donde ambos terminamos completamente satisfechos.</div>

              <div style="display:flex; justify-content:space-between; align-items:center; font-size:12px; color:var(--text-dim);">
                <span>Vello Púbico: <strong>Trimmed (Recortado)</strong></span>
                <span>Idiomas: <strong>EN, FR, ES, PT (Estudio)</strong></span>
                <span>Geobloqueo: <strong>Colombia Abierto</strong></span>
              </div>
            </div>

            <div class="card" style="margin-bottom: 0;">
              <div class="card-title">
                <span>📋 Resumen de Auditoría Estudio</span>
                <span class="badge" style="background: rgba(245, 158, 11, 0.2); color: #fbbf24;">Auditoría 24 Octubre</span>
              </div>
              <ul style="list-style: none; display: flex; flex-direction: column; gap: 12px; font-size: 12px; color: var(--text-muted);">
                <li style="display: flex; gap: 10px; align-items: flex-start;">
                  <i data-lucide="check-circle-2" style="color: var(--success); width: 16px; min-width: 16px; margin-top: 2px;"></i>
                  <span><strong>Usuario:</strong> <code>efac05@yopmail.com</code> | Clave: <code>Centenario123@</code></span>
                </li>
                <li style="display: flex; gap: 10px; align-items: flex-start;">
                  <i data-lucide="check-circle-2" style="color: var(--success); width: 16px; min-width: 16px; margin-top: 2px;"></i>
                  <span><strong>Estructura Tarifaria:</strong> Privado $2.99 / Exclusivo $3.99 por minuto. (Administrada por el estudio).</span>
                </li>
                <li style="display: flex; gap: 10px; align-items: flex-start;">
                  <i data-lucide="check-circle-2" style="color: var(--success); width: 16px; min-width: 16px; margin-top: 2px;"></i>
                  <span><strong>Reglas de Texto:</strong> 100% sin tildes, sin emojis y sin palabras de venta o shows mecánicos.</span>
                </li>
                <li style="display: flex; gap: 10px; align-items: flex-start;">
                  <i data-lucide="check-circle-2" style="color: var(--success); width: 16px; min-width: 16px; margin-top: 2px;"></i>
                  <span><strong>Consola Streamate:</strong> Administrada por software propio del estudio (VELVET AI se mantiene como auditor personal).</span>
                </li>
              </ul>
            </div>
          </div>
        </div>

        <!-- PERFIL DETALLADO LOYALFANS -->
        <div id="sub-perfil-loyalfans" class="sub-tab-content" style="display:none;">
          <div class="grid-2">
            <div class="platform-profile-card">
              <div class="platform-header-row">
                <div class="platform-badge-tag tag-loyalfans">
                  <i data-lucide="gem"></i> LOYALFANS — Perfil Oficial Actualizado en Vivo
                </div>
                <span class="table-badge badge-success">✓ EN VIVO (Verificado)</span>
              </div>
              <div style="display:flex; gap:12px; align-items:center;">
                <img src="/artifacts/test_public_profile_verified.png" alt="Sam" style="width:50px; height:50px; border-radius:50%; object-fit:cover; border:2px solid #c084fc;">
                <div>
                  <strong style="font-size: 15px; color: var(--text-main);">Sam Barton</strong>
                  <div style="font-size: 12px; color: var(--primary-light); margin-top: 2px;">
                    Software & AI Architect ⚡ Versatile Tomboy 🏍️
                  </div>
                </div>
              </div>
              <div class="bio-preview-box">🐺 Sam Barton | Software & AI Architect ⚡ Versatile Tomboy 🏍️

Smart by day, driven about my goals, and teasingly wicked by night.

Software & AI Architect by trade, but my real sanctuary is motorcycles, speed, and my beloved pack: my dogs and my 2 cats are my greatest blessings in this world 🐾🐈. Gym addict, soccer player, late-night sketcher, and an absolute InuYasha devotee 🍙. I also play the ukulele and sing straight from the heart (Billie Eilish, Radiohead, Lana Del Rey, Gorillaz, Mägo de Oz, Rels B... my playlist is a whole journey).

Obsessed with neon in the dark, skulls, and eerie October vibes 💀✨. Working hard every single day to buy my used car in December 🚗 and escape to Cancun 🌴.

Want my attention? Be respectful, intelligent, different, and abnormal. Generic, boring guys bore me to death. If you're a real man who knows how to treat a girl, I just might let you take the wheel... under my explicit permission. 😈⚡</div>
              <div>
                <label style="font-size: 11px; color: var(--text-dim); display: block; margin-bottom: 6px;">Tags Oficiales Registrados (Máx 3):</label>
                <div class="tags-container">
                  <span class="pill-tag" style="color: var(--primary-light); border-color: var(--primary);">#Tomboy</span>
                  <span class="pill-tag" style="color: var(--primary-light); border-color: var(--primary);">#Biker</span>
                  <span class="pill-tag" style="color: var(--primary-light); border-color: var(--primary);">#Tech</span>
                </div>
              </div>
            </div>

            <div class="card" style="margin-bottom: 0;">
              <div class="card-title">
                <span>🎯 Matriz Táctica: LoyalFans</span>
                <span class="badge">Fan Club & Clips</span>
              </div>
              <ul style="list-style: none; display: flex; flex-direction: column; gap: 12px; font-size: 12px; color: var(--text-muted);">
                <li style="display: flex; gap: 10px; align-items: flex-start;">
                  <i data-lucide="check-circle-2" style="color: var(--success); width: 16px; min-width: 16px; margin-top: 2px;"></i>
                  <span><strong>Monetización Pasiva:</strong> Venta directa de Clips en Video Store ($10 - $35) y audios exclusivos.</span>
                </li>
                <li style="display: flex; gap: 10px; align-items: flex-start;">
                  <i data-lucide="check-circle-2" style="color: var(--success); width: 16px; min-width: 16px; margin-top: 2px;"></i>
                  <span><strong>Pay-to-Message Activo:</strong> Seguidores pagan $0.50/mensaje y $0.50/multimedia. Cada respuesta genera ingresos netos.</span>
                </li>
                <li style="display: flex; gap: 10px; align-items: flex-start;">
                  <i data-lucide="check-circle-2" style="color: var(--success); width: 16px; min-width: 16px; margin-top: 2px;"></i>
                  <span><strong>Retención:</strong> El 80% de comisión neto queda para Sam Barton. Mínimo de retiro $50 USD.</span>
                </li>
              </ul>
            </div>
          </div>
        </div>

        <!-- PERFIL DETALLADO STRIPCHAT -->
        <div id="sub-perfil-stripchat" class="sub-tab-content" style="display:none;">
          <div class="grid-2">
            <div class="platform-profile-card">
              <div class="platform-header-row">
                <div class="platform-badge-tag tag-stripchat">
                  <i data-lucide="flame"></i> STRIPCHAT — Perfil Interactivo Lovense
                </div>
                <span class="table-badge badge-info">✓ Lovense Conectado</span>
              </div>
              <div style="display:flex; gap:12px; align-items:center;">
                <img src="/artifacts/stripchat_profile_updated_20261014_211003.png" alt="Sam" style="width:50px; height:50px; border-radius:50%; object-fit:cover; border:2px solid #f43f5e;">
                <div>
                  <strong style="font-size: 15px; color: var(--text-main);">Sam Barton</strong>
                  <div style="font-size: 12px; color: #f43f5e; margin-top: 2px;">
                    Cute Tomboy Gamer ⚡ Lovense Interactive 🎮
                  </div>
                </div>
              </div>
              <div class="bio-preview-box">🐺 Sam Barton | Cute Tomboy Gamer ⚡ Lovense Interactive 🏍️

Software & AI Architect by day, gaming tomboy & teasing companion by night.
Soccer player, motorcycle enthusiast, and devoted mom to my dogs & 2 cats 🐾.
InuYasha devotee 🍙, indie music lover & ukulele player 🎶.

Obsessed with neon in the dark, skulls, and Halloween vibes 💀✨.
Working hard every single day to buy my used car in December 🚗 and escape to Cancun 🌴!

💖 LOVENSE SYNCED:
My toys are active and connect directly to every tip! Send tokens to make me buzz, trigger reactions, or take me into Private / Exclusive for full control 😈🖤.

Be respectful, abnormal, and have fun. Tip to play 💋</div>
              <div>
                <label style="font-size: 11px; color: var(--text-dim); display: block; margin-bottom: 6px;">Tags Principales:</label>
                <div class="tags-container">
                  <span class="pill-tag" style="color: #f43f5e; border-color: #f43f5e;">#Tomboy</span>
                  <span class="pill-tag" style="color: #f43f5e; border-color: #f43f5e;">#Lovense</span>
                  <span class="pill-tag" style="color: #f43f5e; border-color: #f43f5e;">#Interactive</span>
                </div>
              </div>
            </div>

            <div class="card" style="margin-bottom: 0;">
              <div class="card-title">
                <span>🎯 Matriz Táctica: Stripchat</span>
                <span class="badge" style="background: rgba(244, 63, 94, 0.2); color: #f43f5e;">Tokens & Shows</span>
              </div>
              <ul style="list-style: none; display: flex; flex-direction: column; gap: 12px; font-size: 12px; color: var(--text-muted);">
                <li style="display: flex; gap: 10px; align-items: flex-start;">
                  <i data-lucide="check-circle-2" style="color: var(--success); width: 16px; min-width: 16px; margin-top: 2px;"></i>
                  <span><strong>Lovense Synced:</strong> Los juguetes reaccionan con vibración automática a cada tip desde 1 token.</span>
                </li>
                <li style="display: flex; gap: 10px; align-items: flex-start;">
                  <i data-lucide="check-circle-2" style="color: var(--success); width: 16px; min-width: 16px; margin-top: 2px;"></i>
                  <span><strong>Metas de Sala:</strong> Definir 3 niveles de propinas para mantener el flujo constante en transmisión.</span>
                </li>
              </ul>
            </div>
          </div>
        </div>
      </section>"""

# Replace old tab-perfiles
pattern = re.compile(r'<section id="tab-perfiles".*?</section>', re.DOTALL)
if pattern.search(html):
    html = pattern.sub(new_tab_perfiles, html, count=1)
    print("Replaced tab-perfiles with rich multi-platform cards and credentials.")
else:
    print("Error: Could not locate tab-perfiles.")

with open(INDEX_PATH, "w", encoding="utf-8") as f:
    f.write(html)

print("Step 2 saved!")
