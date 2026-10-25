from pathlib import Path

html_path = Path("index.html")
content = html_path.read_text(encoding="utf-8")

print("--- 1. Subtabs para tab-algoritmos ---")
algoritmos_start = '<section id="tab-algoritmos" class="tab-view">'
algoritmos_subtabs_header = """<section id="tab-algoritmos" class="tab-view">
        <!-- Sub-Pestañas Plataformas en Algoritmos -->
        <div class="subtabs-bar">
          <button class="subtab-btn active" onclick="switchSubTab('sub-algo', 'comparativa', this)">
            <i data-lucide="layers"></i> Matriz Comparativa Algorítmica
          </button>
          <button class="subtab-btn" onclick="switchSubTab('sub-algo', 'streamate', this)">
            <i data-lucide="zap"></i> Streamate (EPH • Solo Consulta Estudio)
          </button>
          <button class="subtab-btn" onclick="switchSubTab('sub-algo', 'loyalfans', this)">
            <i data-lucide="gem"></i> LoyalFans (Cooldown 4h • Tips Multiplier)
          </button>
          <button class="subtab-btn" onclick="switchSubTab('sub-algo', 'stripchat', this)">
            <i data-lucide="flame"></i> Stripchat (Token Velocity & Lovense Spikes)
          </button>
        </div>

        <!-- 1. SUBTAB COMPARATIVA ALGORITMOS -->
        <div id="sub-algo-comparativa" class="sub-tab-content">"""

extra_algo_subtabs = """        </div>

        <!-- 2. SUBTAB ALGORITMO STREAMATE (EPH & REVENUE-DRIVEN) -->
        <div id="sub-algo-streamate" class="sub-tab-content" style="display:none;">
          <div class="card" style="border: 1px solid rgba(245, 158, 11, 0.3); background: radial-gradient(circle at top right, rgba(245, 158, 11, 0.1), rgba(18, 14, 28, 0.95));">
            <div class="card-title">
              <span style="color: #fbbf24;">⚡ Algoritmo Streamate: EPH (Earnings Per Hour) & Auditoría Centenario</span>
              <span class="table-badge badge-warning">Modo Solo Consulta • Estudio Satélite</span>
            </div>
            <p style="font-size: 12px; color: var(--text-muted); line-height: 1.6; margin-bottom: 18px;">
              Streamate está administrado externamente por Centenario Studio. En SIREN AI auditamos su comportamiento algorítmico para sincronizar los directos de Sam:
            </p>

            <div class="grid-3" style="margin-bottom: 20px;">
              <div class="kpi-card" style="border-left: 3px solid #fbbf24;">
                <div class="kpi-title">Métrica Cardinal</div>
                <div class="kpi-value" style="font-size: 16px; color: #fbbf24;">EPH ($ / Hora)</div>
                <div class="kpi-sub">Total de dinero generado dividido por las horas acumuladas de transmisión.</div>
              </div>
              <div class="kpi-card" style="border-left: 3px solid #10b981;">
                <div class="kpi-title">Ventana de Oro</div>
                <div class="kpi-value" style="font-size: 16px; color: #10b981;">Primeros 8 Min</div>
                <div class="kpi-sub">Convertir mirones a Privado ($2.99/min) o Exclusivo ($3.99/min) de inmediato.</div>
              </div>
              <div class="kpi-card" style="border-left: 3px solid #f43f5e;">
                <div class="kpi-title">Penalización Algorítmica</div>
                <div class="kpi-value" style="font-size: 16px; color: #f43f5e;">Free Chat Idle</div>
                <div class="kpi-sub">Estar más de 12 minutos en Free Chat sin cobrar hunde a páginas 15+.</div>
              </div>
            </div>

            <div class="grid-2">
              <div style="background: rgba(255,255,255,0.02); padding: 16px; border-radius: 8px; border: 1px solid var(--border-color);">
                <h4 style="color:#fbbf24; font-size:13px; margin-bottom:8px;"><i data-lucide="shield-alert"></i> Reglas del Estudio Centenario</h4>
                <p style="font-size:12px; color:var(--text-muted); line-height:1.6;">
                  • Geobloqueo en Colombia activo desde la matriz del estudio.<br>
                  • Tarifas fijadas en $2.99 (Privado) y $3.99 (Exclusivo).<br>
                  • Perfil oficial en 4 idiomas verificado y listo en cumplimiento.<br>
                  • SIREN AI audita sin interferir en los accesos maestros del estudio.
                </p>
              </div>
              <div style="background: rgba(255,255,255,0.02); padding: 16px; border-radius: 8px; border: 1px solid var(--border-color);">
                <h4 style="color:#10b981; font-size:13px; margin-bottom:8px;"><i data-lucide="sparkles"></i> Tácticas para Sam Barton</h4>
                <p style="font-size:12px; color:var(--text-muted); line-height:1.6;">
                  • Tocar acordes en el ukelele para enganchar usuarios gringos.<br>
                  • No tolerar usuarios vulgares; aplicar actitud tomboy firme y directa.<br>
                  • Invitar a los usuarios VIP de calidad a su club personal de LoyalFans.
                </p>
              </div>
            </div>
          </div>
        </div>

        <!-- 3. SUBTAB ALGORITMO LOYALFANS (EVENT-DRIVEN & TIPS WEIGHT) -->
        <div id="sub-algo-loyalfans" class="sub-tab-content" style="display:none;">
          <div class="card" style="border: 1px solid rgba(147, 51, 234, 0.3); background: radial-gradient(circle at top right, rgba(147, 51, 234, 0.1), rgba(18, 14, 28, 0.95));">
            <div class="card-title">
              <span style="color: var(--primary-light);">💎 Algoritmo LoyalFans: Cooldown 4 Horas & Multiplicador de Propinas</span>
              <span class="table-badge badge-purple">Directo • 80% Split Neto</span>
            </div>
            <p style="font-size: 12px; color: var(--text-muted); line-height: 1.6; margin-bottom: 18px;">
              LoyalFans no clasifica por horas estáticas, sino por <strong>eventos de publicación</strong> en Timeline y Video Store:
            </p>

            <div class="grid-3" style="margin-bottom: 20px;">
              <div class="kpi-card" style="border-left: 3px solid #a855f7;">
                <div class="kpi-title">Ciclo de Bump</div>
                <div class="kpi-value" style="font-size: 16px; color: #a855f7;">Cada 4 Horas</div>
                <div class="kpi-sub">Publicar con menos de 4h de diferencia no resetea la posición #1 en Recently Updated.</div>
              </div>
              <div class="kpi-card" style="border-left: 3px solid #10b981;">
                <div class="kpi-title">Double Bump Hack</div>
                <div class="kpi-value" style="font-size: 16px; color: #10b981;">Store + Timeline</div>
                <div class="kpi-sub">Publicar clip en Video Store marcando "Post to Timeline" da doble exposición instantánea.</div>
              </div>
              <div class="kpi-card" style="border-left: 3px solid #06b6d4;">
                <div class="kpi-title">Peso del Tip</div>
                <div class="kpi-value" style="font-size: 16px; color: #06b6d4;">10x Factor</div>
                <div class="kpi-sub">Cada propina recibida en un post lo catapulta a la pestaña global Explore.</div>
              </div>
            </div>
          </div>
        </div>

        <!-- 4. SUBTAB ALGORITMO STRIPCHAT (TOKEN VELOCITY & CAROUSEL) -->
        <div id="sub-algo-stripchat" class="sub-tab-content" style="display:none;">
          <div class="card" style="border: 1px solid rgba(244, 63, 94, 0.3); background: radial-gradient(circle at top right, rgba(244, 63, 94, 0.1), rgba(18, 14, 28, 0.95));">
            <div class="card-title">
              <span style="color: #f43f5e;">🔥 Algoritmo Stripchat: Token Velocity & Integración Lovense</span>
              <span class="table-badge badge-info">Directo • Tokens $0.05 USD</span>
            </div>
            <p style="font-size: 12px; color: var(--text-muted); line-height: 1.6; margin-bottom: 18px;">
              Stripchat opera como un motor freemium de alta velocidad donde cada vibración de Lovense alimenta el ranking:
            </p>

            <div class="grid-3" style="margin-bottom: 20px;">
              <div class="kpi-card" style="border-left: 3px solid #f43f5e;">
                <div class="kpi-title">Velocidad de Tokens</div>
                <div class="kpi-value" style="font-size: 16px; color: #f43f5e;">Tokens / Seg</div>
                <div class="kpi-sub">Ráfagas continuas de propinas activan el algoritmo de "Trending Model".</div>
              </div>
              <div class="kpi-card" style="border-left: 3px solid #ec4899;">
                <div class="kpi-title">Lovense Interactive</div>
                <div class="kpi-value" style="font-size: 16px; color: #ec4899;">Vibe Spikes</div>
                <div class="kpi-sub">Niveles 1 a 5 conectados al menú de propinas en tiempo real.</div>
              </div>
              <div class="kpi-card" style="border-left: 3px solid #a855f7;">
                <div class="kpi-title">Ticket Show & Metas</div>
                <div class="kpi-value" style="font-size: 16px; color: #a855f7;">250 - 500 TK</div>
                <div class="kpi-sub">Metas grupales de sala para desatar privados colectivos rentables.</div>
              </div>
            </div>
          </div>
        </div>"""

algo_boundary = """            </div>
          </div>
        </div>
      </section>

      <!-- ========================================== -->
      <!-- PESTAÑA 5: CONTROL DE ACTUALIZACIONES (TAREAS) -->"""

if algoritmos_start in content and 'id="sub-algo-comparativa"' not in content:
    content = content.replace(algoritmos_start, algoritmos_subtabs_header, 1)
    new_algo_boundary = f"""            </div>
          </div>
{extra_algo_subtabs}
      </section>

      <!-- ========================================== -->
      <!-- PESTAÑA 5: CONTROL DE ACTUALIZACIONES (TAREAS) -->"""
    content = content.replace(algo_boundary, new_algo_boundary, 1)
    print("Done tab-algoritmos!")

print("--- 2. Subtabs para tab-actualizaciones ---")
act_start = '<section id="tab-actualizaciones" class="tab-view">'
act_subtabs_header = """<section id="tab-actualizaciones" class="tab-view">
        <!-- Sub-Pestañas Plataformas en Actualizaciones -->
        <div class="subtabs-bar">
          <button class="subtab-btn active" onclick="switchSubTab('sub-act', 'matriz', this)">
            <i data-lucide="check-square"></i> Matriz de Control General
          </button>
          <button class="subtab-btn" onclick="switchSubTab('sub-act', 'streamate', this)">
            <i data-lucide="zap"></i> Streamate (En Revisión • 4 Idiomas)
          </button>
          <button class="subtab-btn" onclick="switchSubTab('sub-act', 'loyalfans', this)">
            <i data-lucide="gem"></i> LoyalFans (Verificado & Activo)
          </button>
          <button class="subtab-btn" onclick="switchSubTab('sub-act', 'stripchat', this)">
            <i data-lucide="flame"></i> Stripchat (Listo en Cola)
          </button>
        </div>

        <!-- 1. SUBTAB MATRIZ GENERAL ACTUALIZACIONES -->
        <div id="sub-act-matriz" class="sub-tab-content">"""

extra_act_subtabs = """        </div>

        <!-- 2. SUBTAB STREAMATE ACTUALIZACIONES (EN REVISION CUMPLIMIENTO) -->
        <div id="sub-act-streamate" class="sub-tab-content" style="display:none;">
          <div class="card" style="border: 1px solid rgba(245, 158, 11, 0.3);">
            <div class="card-title">
              <span style="color: #fbbf24;">⚡ Streamate: Perfil Oficial Actualizado en 4 Idiomas</span>
              <span class="table-badge badge-warning">En Revisión de Cumplimiento (*) • Centenario Studio</span>
            </div>
            <p style="font-size: 12px; color: var(--text-muted); line-height: 1.6; margin-bottom: 16px;">
              El script automatizado <code>scripts/execute_streamate_profile_update.py</code> inyectó con éxito los 4 actos narrativos en los 4 idiomas oficiales de Streamate Models. Sin emojis, sin tildes, respetando estrictamente los límites de caracteres:
            </p>

            <div class="grid-4" style="margin-bottom: 16px;">
              <div class="kpi-card" style="border-left: 3px solid #38bdf8;">
                <div class="kpi-title">Español (ES)</div>
                <div class="kpi-value" style="font-size: 15px; color: #38bdf8;">✓ Actualizado</div>
                <div class="kpi-sub">Headline: 64 c • Show: 245 c • Turn Ons: 214 c • Exp: 213 c</div>
              </div>
              <div class="kpi-card" style="border-left: 3px solid #10b981;">
                <div class="kpi-title">Inglés (EN)</div>
                <div class="kpi-value" style="font-size: 15px; color: #10b981;">✓ Actualizado</div>
                <div class="kpi-sub">Headline: 61 c • Show: 245 c • Turn Ons: 210 c • Exp: 213 c</div>
              </div>
              <div class="kpi-card" style="border-left: 3px solid #a855f7;">
                <div class="kpi-title">Francés (FR)</div>
                <div class="kpi-value" style="font-size: 15px; color: #a855f7;">✓ Actualizado</div>
                <div class="kpi-sub">Headline: 64 c • Show: 222 c • Turn Ons: 201 c • Exp: 204 c</div>
              </div>
              <div class="kpi-card" style="border-left: 3px solid #f43f5e;">
                <div class="kpi-title">Portugués (PT)</div>
                <div class="kpi-value" style="font-size: 15px; color: #f43f5e;">✓ Actualizado</div>
                <div class="kpi-sub">Headline: 62 c • Show: 212 c • Turn Ons: 198 c • Exp: 199 c</div>
              </div>
            </div>

            <div style="background: rgba(16, 185, 129, 0.08); border: 1px solid rgba(16, 185, 129, 0.25); border-radius: 8px; padding: 14px; font-size: 12px; color: #34d399; margin-bottom: 14px;">
              ✓ <strong>Evidencia Almacenada:</strong> Capturas de pantalla de verificación guardadas en <code>artifacts/streamate_update_evidence/</code> (ES, EN, FR, PT) y resumen JSON listo.
            </div>

            <div style="font-size: 12px; color: var(--text-muted); background: rgba(0,0,0,0.25); padding: 14px; border-radius: 8px; border: 1px solid var(--border-color);">
              ⚠️ <strong>Nota de Seguridad:</strong> El estudio Centenario mantiene el control administrativo de la cuenta. Los cambios entraron a cola de revisión (*) de Streamate Compliance sin generar alertas de seguridad ni bloqueos.
            </div>
          </div>
        </div>

        <!-- 3. SUBTAB LOYALFANS ACTUALIZACIONES -->
        <div id="sub-act-loyalfans" class="sub-tab-content" style="display:none;">
          <div class="card" style="border: 1px solid rgba(147, 51, 234, 0.3);">
            <div class="card-title">
              <span style="color: var(--primary-light);">💎 LoyalFans: Perfil Tomboy Verificado & En Producción</span>
              <span class="table-badge badge-success">✓ 100% Verificado</span>
            </div>
            <p style="font-size: 12px; color: var(--text-muted); line-height: 1.6; margin-bottom: 16px;">
              Biografía oficial inyectada con éxito mediante Playwright en sesión autenticada:
            </p>
            <div style="background: rgba(0,0,0,0.3); border: 1px solid var(--border-color); border-radius: 8px; padding: 16px; font-size: 12px; line-height: 1.7; color: var(--text-main); margin-bottom: 16px;">
              <strong>Software & AI Architect ⚡ Tomboy</strong><br>
              A direct mind who loves tech, good humor, and deep conversations. I create without masks and connect with those who know what they want.
            </div>
            <div class="grid-3">
              <div class="kpi-card" style="border-left: 3px solid #10b981;">
                <div class="kpi-title">Tarifa Mensual</div>
                <div class="kpi-value" style="font-size: 15px; color: #10b981;">$15.00 USD</div>
                <div class="kpi-sub">80% neto directo para Sam ($12.00)</div>
              </div>
              <div class="kpi-card" style="border-left: 3px solid #06b6d4;">
                <div class="kpi-title">Pay-To-Message</div>
                <div class="kpi-value" style="font-size: 15px; color: #06b6d4;">$0.50 USD</div>
                <div class="kpi-sub">Filtro de DMs activos</div>
              </div>
              <div class="kpi-card" style="border-left: 3px solid #a855f7;">
                <div class="kpi-title">Estado Playwright</div>
                <div class="kpi-value" style="font-size: 15px; color: #a855f7;">Sesión Activa</div>
                <div class="kpi-sub">Actualización en 1 clic disponible</div>
              </div>
            </div>
          </div>
        </div>

        <!-- 4. SUBTAB STRIPCHAT ACTUALIZACIONES -->
        <div id="sub-act-stripchat" class="sub-tab-content" style="display:none;">
          <div class="card" style="border: 1px solid rgba(244, 63, 94, 0.3);">
            <div class="card-title">
              <span style="color: #f43f5e;">🔥 Stripchat: Perfil Preparado para Inyección</span>
              <span class="table-badge badge-warning">⏳ En Espera de Lanzamiento</span>
            </div>
            <p style="font-size: 12px; color: var(--text-muted); line-height: 1.6; margin-bottom: 16px;">
              Script <code>src/platforms/stripchat/profile_updater.py</code> configurado y en espera de confirmación:
            </p>
            <div style="background: rgba(0,0,0,0.3); border: 1px solid var(--border-color); border-radius: 8px; padding: 16px; font-size: 12px; line-height: 1.7; color: var(--text-main); margin-bottom: 16px;">
              <strong>Cute Tomboy • Lovense Interactive 🎮</strong><br>
              Direct, witty and always curious. My toys react to your tips and my music sets the mood.
            </div>
            <button class="action-btn primary" onclick="openUpdateModal('stripchat')">
              <i data-lucide="play"></i> Desplegar en Stripchat Ahora
            </button>
          </div>
        </div>"""

act_boundary = """            </div>
          </div>
        </div>
      </section>

      <!-- ========================================== -->
      <!-- PESTAÑA 6: PLAN DE TRABAJO & FLUJOS RECOMENDADOS -->"""

if act_start in content and 'id="sub-act-matriz"' not in content:
    content = content.replace(act_start, act_subtabs_header, 1)
    new_act_boundary = f"""            </div>
          </div>
{extra_act_subtabs}
      </section>

      <!-- ========================================== -->
      <!-- PESTAÑA 6: PLAN DE TRABAJO & FLUJOS RECOMENDADOS -->"""
    content = content.replace(act_boundary, new_act_boundary, 1)
    print("Done tab-actualizaciones!")

print("--- 3. Subtabs para tab-flujos ---")
flujos_start = '<section id="tab-flujos" class="tab-view">'
flujos_subtabs_header = """<section id="tab-flujos" class="tab-view">
        <!-- Sub-Pestañas Plataformas en Flujos -->
        <div class="subtabs-bar">
          <button class="subtab-btn active" onclick="switchSubTab('sub-flujo', 'hibrido', this)">
            <i data-lucide="git-merge"></i> Flujo Híbrido Consolidado (Sam 24/7)
          </button>
          <button class="subtab-btn" onclick="switchSubTab('sub-flujo', 'streamate', this)">
            <i data-lucide="zap"></i> Flujo Streamate (Shows Privados & EPH)
          </button>
          <button class="subtab-btn" onclick="switchSubTab('sub-flujo', 'loyalfans', this)">
            <i data-lucide="gem"></i> Flujo LoyalFans (Embudo 80% & DMs Masivos)
          </button>
          <button class="subtab-btn" onclick="switchSubTab('sub-flujo', 'stripchat', this)">
            <i data-lucide="flame"></i> Flujo Stripchat (Sala Lovense & Metas de Sala)
          </button>
        </div>

        <!-- 1. SUBTAB FLUJO HIBRIDO CONSOLIDADO -->
        <div id="sub-flujo-hibrido" class="sub-tab-content">"""

extra_flujos_subtabs = """        </div>

        <!-- 2. SUBTAB FLUJO STREAMATE -->
        <div id="sub-flujo-streamate" class="sub-tab-content" style="display:none;">
          <div class="card" style="border: 1px solid rgba(245, 158, 11, 0.3);">
            <div class="card-title">
              <span style="color:#fbbf24;">⚡ Flujo Operativo en Streamate: Maximizar EPH en 2 Horas</span>
              <span class="table-badge badge-warning">Auditoría Estudio Centenario • Solo Consulta</span>
            </div>
            <p style="font-size: 12px; color: var(--text-muted); line-height: 1.6; margin-bottom: 16px;">
              En Streamate las horas prolongadas en Free Chat destruyen el ranking. El flujo operativo debe ser quirúrgico:
            </p>
            <div class="grid-3" style="margin-bottom: 16px;">
              <div class="kpi-card" style="border-left: 3px solid #fbbf24;">
                <strong style="color:#fbbf24; display:block; font-size:13px; margin-bottom:6px;">1. Entrada en Free Chat (0-8 min)</strong>
                <p style="font-size:11px; color:var(--text-muted); line-height:1.5;">
                  Tocar acordes en el ukelele, saludar con voz baja al oído en inglés. Filtrar inmediatamente a los que piden cosas gratis.
                </p>
              </div>
              <div class="kpi-card" style="border-left: 3px solid #10b981;">
                <strong style="color:#10b981; display:block; font-size:13px; margin-bottom:6px;">2. Cierre Privado ($2.99/min)</strong>
                <p style="font-size:11px; color:var(--text-muted); line-height:1.5;">
                  Proponer privado con complicidad: "Vamos donde podamos hablar sin ruido". Buscar shows de mínimo 10 minutos.
                </p>
              </div>
              <div class="kpi-card" style="border-left: 3px solid #38bdf8;">
                <strong style="color:#38bdf8; display:block; font-size:13px; margin-bottom:6px;">3. Salida Inmediata o Upsell</strong>
                <p style="font-size:11px; color:var(--text-muted); line-height:1.5;">
                  Al terminar el privado, si en 5 minutos no hay otro cliente, pausar la transmisión para proteger el EPH.
                </p>
              </div>
            </div>
          </div>
        </div>

        <!-- 3. SUBTAB FLUJO LOYALFANS -->
        <div id="sub-flujo-loyalfans" class="sub-tab-content" style="display:none;">
          <div class="card" style="border: 1px solid rgba(147, 51, 234, 0.3);">
            <div class="card-title">
              <span style="color:var(--primary-light);">💎 Flujo Operativo en LoyalFans: Máquina de Ingresos Pasivos</span>
              <span class="table-badge badge-purple">80% Neto Directo</span>
            </div>
            <p style="font-size: 12px; color: var(--text-muted); line-height: 1.6; margin-bottom: 16px;">
              LoyalFans no requiere estar sentada frente a la cámara todo el día. Funciona con cadencia programada:
            </p>
            <div class="grid-3" style="margin-bottom: 16px;">
              <div class="kpi-card" style="border-left: 3px solid #a855f7;">
                <strong style="color:var(--primary-light); display:block; font-size:13px; margin-bottom:6px;">Cadencia de Cooldown 4h</strong>
                <p style="font-size:11px; color:var(--text-muted); line-height:1.5;">
                  10:00 AM Video Store • 02:00 PM Foto Sub • 06:00 PM Teaser noche. Garantiza primer lugar continuo en el feed.
                </p>
              </div>
              <div class="kpi-card" style="border-left: 3px solid #06b6d4;">
                <strong style="color:#38bdf8; display:block; font-size:13px; margin-bottom:6px;">DMs Masivos Estratégicos</strong>
                <p style="font-size:11px; color:var(--text-muted); line-height:1.5;">
                  Enviar 1 PPV masivo al día ($12-$15) a los 599 fans. Tasa de lectura del 22.5% produce $50-$70 USD por envío.
                </p>
              </div>
              <div class="kpi-card" style="border-left: 3px solid #10b981;">
                <strong style="color:#10b981; display:block; font-size:13px; margin-bottom:6px;">Pay-To-Message ($0.50)</strong>
                <p style="font-size:11px; color:var(--text-muted); line-height:1.5;">
                  Cada fan paga 50 centavos por iniciar conversación. Filtro automático de acosadores y monetización de atención.
                </p>
              </div>
            </div>
          </div>
        </div>

        <!-- 4. SUBTAB FLUJO STRIPCHAT -->
        <div id="sub-flujo-stripchat" class="sub-tab-content" style="display:none;">
          <div class="card" style="border: 1px solid rgba(244, 63, 94, 0.3);">
            <div class="card-title">
              <span style="color:#f43f5e;">🔥 Flujo Operativo en Stripchat: Dinámica de Sala & Lovense</span>
              <span class="table-badge badge-info">Tokens Freemium</span>
            </div>
            <p style="font-size: 12px; color: var(--text-muted); line-height: 1.6; margin-bottom: 16px;">
              En Stripchat el espectáculo se construye comunitariamente mediante metas acumulativas:
            </p>
            <div class="grid-3" style="margin-bottom: 16px;">
              <div class="kpi-card" style="border-left: 3px solid #f43f5e;">
                <strong style="color:#f43f5e; display:block; font-size:13px; margin-bottom:6px;">Metas Escalonadas</strong>
                <p style="font-size:11px; color:var(--text-muted); line-height:1.5;">
                  Fijar metas de 100, 250 y 500 tokens. La psicología de sala hace que varios usuarios aporten para ver el objetivo.
                </p>
              </div>
              <div class="kpi-card" style="border-left: 3px solid #a855f7;">
                <strong style="color:#a855f7; display:block; font-size:13px; margin-bottom:6px;">Lovense Vibe Levels</strong>
                <p style="font-size:11px; color:var(--text-muted); line-height:1.5;">
                  Configurar vibraciones progresivas. Propinas de 10-25 tokens para toques sutiles, 100+ para intensidad alta.
                </p>
              </div>
              <div class="kpi-card" style="border-left: 3px solid #10b981;">
                <strong style="color:#10b981; display:block; font-size:13px; margin-bottom:6px;">Fan Club VIP</strong>
                <p style="font-size:11px; color:var(--text-muted); line-height:1.5;">
                  Convertir a los mayores donadores en miembros del Fan Club mensual con álbumes privados exclusivos.
                </p>
              </div>
            </div>
          </div>
        </div>"""

flujos_boundary = """              </div>
            </div>
          </div>
        </div>
      </section>

      <!-- ========================================== -->
      <!-- PESTAÑA 7: ENDPOINTS & SCRAPERS (CATÁLOGO) -->"""

if flujos_start in content and 'id="sub-flujo-hibrido"' not in content:
    content = content.replace(flujos_start, flujos_subtabs_header, 1)
    new_flujos_boundary = f"""              </div>
            </div>
          </div>
{extra_flujos_subtabs}
        </div>
      </section>

      <!-- ========================================== -->
      <!-- PESTAÑA 7: ENDPOINTS & SCRAPERS (CATÁLOGO) -->"""
    content = content.replace(flujos_boundary, new_flujos_boundary, 1)
    print("Done tab-flujos!")

html_path.write_text(content, encoding="utf-8")
print("All remaining subtabs successfully written to index.html!")
