from pathlib import Path

html_path = Path("index.html")
content = html_path.read_text(encoding="utf-8")

# Streamate Finanzas Subtab
streamate_finanzas_html = """
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
          <div class="card">
            <div class="card-title">
              <span>💳 Matriz Consolidada de Métodos de Pago, Fechas y Estados por Plataforma</span>
              <span class="badge">Datos de Auditoría SIREN</span>
            </div>

            <table class="custom-table">
              <thead>
                <tr>
                  <th>Plataforma</th>
                  <th>Moneda Base</th>
                  <th>Comisión Modelo</th>
                  <th>Frecuencia de Pago</th>
                  <th>Días de Corte / Pago</th>
                  <th>Mínimo Retiro</th>
                  <th>Métodos Soportados</th>
                  <th>Estado Cuenta</th>
                </tr>
              </thead>
              <tbody>
                <tr>
                  <td><strong><i data-lucide="gem" style="width:12px; vertical-align:middle; color:var(--primary-light);"></i> LoyalFans</strong></td>
                  <td>USD ($) Directo</td>
                  <td><span class="table-badge badge-success">80% Neto</span></td>
                  <td>Quincenal (Bi-monthly)</td>
                  <td>1ro y 16 de cada mes</td>
                  <td>$50.00 USD</td>
                  <td>Paxum, Wire, ACH Direct</td>
                  <td><span class="table-badge badge-warning" style="background: rgba(239, 68, 68, 0.15); color: #f87171; border: 1px solid rgba(239, 68, 68, 0.3);">⚠️ Sin Configurar (Requiere Setup)</span></td>
                </tr>
                <tr>
                  <td><strong><i data-lucide="zap" style="width:12px; vertical-align:middle; color:#fbbf24;"></i> Streamate</strong></td>
                  <td>Gold / USD</td>
                  <td><span class="table-badge badge-warning">~30% - 35%</span></td>
                  <td>Semanal / Quincenal</td>
                  <td>Cada Miércoles / Quincena</td>
                  <td>$100.00 USD</td>
                  <td>Paxum, Wire, Cheque Electrónico</td>
                  <td><span class="table-badge badge-purple">Listo para Configurar</span></td>
                </tr>
                <tr>
                  <td><strong><i data-lucide="flame" style="width:12px; vertical-align:middle; color:#fb7185;"></i> Stripchat</strong></td>
                  <td>Tokens ($0.05 / tk)</td>
                  <td><span class="table-badge badge-info">~50% Nominal</span></td>
                  <td>Semanal</td>
                  <td>Todos los Martes</td>
                  <td>$20.00 - $50.00 USD</td>
                  <td>Paxum, Cripto (USDT/BTC), Wire</td>
                  <td><span class="table-badge badge-purple">Listo para Configurar</span></td>
                </tr>
                <tr>
                  <td><strong><i data-lucide="sparkle" style="width:12px; vertical-align:middle; color:#38bdf8;"></i> Flirt4Free</strong></td>
                  <td>Créditos VIP</td>
                  <td><span class="table-badge badge-warning">~30% - 40%</span></td>
                  <td>Quincenal / Mensual</td>
                  <td>15 y 30 de cada mes</td>
                  <td>$100.00 USD</td>
                  <td>Paxum, ACH, Wire Internacional</td>
                  <td><span class="table-badge badge-purple">Listo para Configurar</span></td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
"""

finanzas_end_anchor = """            </table>
          </div>
        </div>
      </section>"""

if "sub-finanzas-streamate" not in content and finanzas_end_anchor in content:
    replacement = f"""            </table>
          </div>
        </div>
        </div> <!-- Fin de sub-finanzas-loyalfans -->
{streamate_finanzas_html}
      </section>"""
    content = content.replace(finanzas_end_anchor, replacement, 1)
    html_path.write_text(content, encoding="utf-8")
    print("Successfully fixed tab-finanzas with all subtabs!")
else:
    print("Could not match finanzas_end_anchor or already present.")
