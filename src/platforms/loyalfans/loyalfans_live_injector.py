"""
SIREN AI — Inyector Ultra-Rápido en Vivo para Loyalfans dentro de StreamMonitor.
Optimizado para ejecución en < 1.5 segundos con selectores directos y paralelismo.
"""

import os
import json
import subprocess
from pathlib import Path
from typing import Dict, Any, Optional

NODE_PATH = "node"

def get_devtools_active_port() -> Optional[int]:
    appdata = os.environ.get("APPDATA", "C:/Users/MI PC/AppData/Roaming")
    port_file = Path(appdata) / "streammonitor" / "DevToolsActivePort"
    if not port_file.exists():
        return None
    try:
        with open(port_file, "r", encoding="utf-8") as f:
            lines = f.read().strip().splitlines()
            if lines and lines[0].strip().isdigit():
                return int(lines[0].strip())
    except Exception:
        pass
    return None

def inject_strategy_into_loyalfans(topic: str, goal_data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    port = get_devtools_active_port()
    if not port:
        return {"success": False, "error": "StreamMonitor no tiene DevToolsActivePort activo."}

    goal = goal_data or {}
    l1_task = goal.get("level1", {}).get("task") or "truth or dare"
    l2_task = goal.get("level2", {}).get("task") or "CHALLENGE FOR 1 MINUTE"
    l3_task = goal.get("level3", {}).get("task") or "all or nothing"

    js_template = """
const http = require('http');
const WebSocket = require('ws');

const port = PORT_PLACEHOLDER;
const targetTopic = TOPIC_PLACEHOLDER;
const goalL1 = GOAL_L1_PLACEHOLDER;
const goalL2 = GOAL_L2_PLACEHOLDER;
const goalL3 = GOAL_L3_PLACEHOLDER;

function getTargets() {
  return new Promise((resolve, reject) => {
    http.get('http://127.0.0.1:' + port + '/json', res => {
      let d = ''; res.on('data', c => d += c);
      res.on('end', () => { try { resolve(JSON.parse(d)); } catch(e) { reject(e); } });
    }).on('error', reject);
  });
}

async function evalInTarget(ws, expr) {
  return new Promise(resolve => {
    const id = Math.floor(Math.random() * 1000000);
    const handler = (m) => {
      try {
        const data = JSON.parse(m.toString());
        if (data.id === id) {
          ws.removeListener('message', handler);
          resolve(data?.result?.result?.value);
        }
      } catch(e) {
        ws.removeListener('message', handler);
        resolve(null);
      }
    };
    ws.on('message', handler);
    ws.send(JSON.stringify({
      id,
      method: 'Runtime.evaluate',
      params: { expression: expr, returnByValue: true }
    }));
  });
}

const sleep = ms => new Promise(r => setTimeout(r, ms));

async function main() {
  const startTime = Date.now();
  let targets = await getTargets();
  let lf = targets.find(t => t.url.includes('loyalfans.com'));

  for (let i = 0; i < 3 && !lf; i++) {
    await sleep(250);
    targets = await getTargets();
    lf = targets.find(t => t.url.includes('loyalfans.com'));
  }

  if (!lf) {
    console.log(JSON.stringify({ success: false, error: 'No se encontró la página de Loyalfans en StreamMonitor' }));
    process.exit(1);
  }

  const ws = new WebSocket(lf.webSocketDebuggerUrl);
  await new Promise(r => ws.on('open', r));

  // 1. Limpieza rápida de advertencias de cookies o contenido adulto si aparecen
  await evalInTarget(ws, `(() => {
    const cookieBtn = Array.from(document.querySelectorAll('button')).find(b => (b.innerText || '').includes('ACEPTA TODO'));
    if (cookieBtn) cookieBtn.click();
    const secBtn = Array.from(document.querySelectorAll('button')).find(b => (b.innerText || '').trim() === 'CONFIRMAR' && b.closest('.broadcast-alert, .modal, .dialog'));
    if (secBtn) secBtn.click();
  })()`);

  // 2. Si no está en /broadcast, navegar directamente
  const curUrl = await evalInTarget(ws, 'window.location.href');
  if (!curUrl || !curUrl.includes('/broadcast')) {
    await evalInTarget(ws, 'window.location.href = "https://www.loyalfans.com/broadcast"');
    await sleep(1200);
  }

  // 3. INYECCIÓN DEL TEMA DE SALA (Room Topic)
  await evalInTarget(ws, `(() => {
    let inp = document.querySelector('input[placeholder="Tema de chat"]');
    if (inp) return true;
    const updBtn = document.querySelector('span.topic-btn[data-translateevent="updateTopic"]');
    if (updBtn) { updBtn.click(); return true; }
    const gear = document.querySelector('i.lf-settings');
    if (gear) { gear.click(); if (gear.parentElement) gear.parentElement.click(); return true; }
    return false;
  })()`);

  // Esperar activamente que aparezca el input del tema (máx 1.2s)
  for (let i = 0; i < 8; i++) {
    const hasInp = await evalInTarget(ws, `!!document.querySelector('input[placeholder="Tema de chat"]')`);
    if (hasInp) break;
    await sleep(120);
  }

  // Escribir tema y guardar
  const topicRes = await evalInTarget(ws, `(() => {
    const topicInp = document.querySelector('input[placeholder="Tema de chat"]');
    if (!topicInp) return { updated: false, error: 'Input de tema no encontrado' };

    const setter = Object.getOwnPropertyDescriptor(window.HTMLInputElement.prototype, 'value').set;
    setter.call(topicInp, ${JSON.stringify(targetTopic)});
    topicInp.dispatchEvent(new Event('input', { bubbles: true }));
    topicInp.dispatchEvent(new Event('change', { bubbles: true }));

    // Buscar el botón GUARDAR correspondiente a este input
    let p = topicInp.parentElement;
    let saveBtn = null;
    for (let i = 0; i < 5 && p; i++) {
      saveBtn = Array.from(p.querySelectorAll('button')).find(b => (b.innerText || '').trim() === 'GUARDAR');
      if (saveBtn) break;
      p = p.parentElement;
    }
    if (!saveBtn) {
      saveBtn = Array.from(document.querySelectorAll('.mat-mdc-dialog-container button, button')).find(b => (b.innerText || '').trim() === 'GUARDAR');
    }
    if (saveBtn) saveBtn.click();

    // Cerrar modal de ajustes tras guardar
    setTimeout(() => {
      const closeBtn = document.querySelector('.mat-mdc-dialog-container .lf-close, [mat-dialog-close], .close-button');
      if (closeBtn) closeBtn.click();
      const backdrop = document.querySelector('.cdk-overlay-backdrop');
      if (backdrop) backdrop.click();
    }, 150);

    return { updated: true, saved: !!saveBtn };
  })()`);

  // Esperar a que el backdrop anterior se cierre
  for (let i = 0; i < 8; i++) {
    const hasBackdrop = await evalInTarget(ws, `!!document.querySelector('.cdk-overlay-backdrop')`);
    if (!hasBackdrop) break;
    await sleep(100);
  }

  // 4. INYECCIÓN DEL OBJETIVO 3 NIVELES ($11, $22, $33)
  await evalInTarget(ws, `(() => {
    const editGoalBtn = Array.from(document.querySelectorAll('button')).find(b => (b.innerText || '').includes('EDITAR OBJETIVO'));
    if (editGoalBtn) editGoalBtn.click();
  })()`);

  // Esperar activamente que monte el modal de objetivos
  for (let i = 0; i < 10; i++) {
    const hasGoalInp = await evalInTarget(ws, `!!document.querySelector('input[placeholder*="nivel 1"]')`);
    if (hasGoalInp) break;
    await sleep(100);
  }

  const goalRes = await evalInTarget(ws, `(() => {
    const setInp = (inp, val) => {
      if (!inp) return;
      const s = Object.getOwnPropertyDescriptor(window.HTMLInputElement.prototype, 'value').set;
      s.call(inp, val);
      inp.dispatchEvent(new Event('input', { bubbles: true }));
      inp.dispatchEvent(new Event('change', { bubbles: true }));
    };

    const inpL1 = document.querySelector('input[placeholder*="nivel 1"]');
    const inpL2 = document.querySelector('input[placeholder*="nivel 2"]');
    const inpL3 = document.querySelector('input[placeholder*="nivel 3"]');

    if (inpL1) setInp(inpL1, goalL1);
    if (inpL2) setInp(inpL2, goalL2);
    if (inpL3) setInp(inpL3, goalL3);

    // Precios: inputs de tipo number en el modal
    const numInputs = Array.from(document.querySelectorAll('.mat-mdc-dialog-container input[type="number"]'));
    if (numInputs[0]) setInp(numInputs[0], '11');
    if (numInputs[1]) setInp(numInputs[1], '22');
    if (numInputs[2]) setInp(numInputs[2], '33');

    const confirmBtn = Array.from(document.querySelectorAll('.mat-mdc-dialog-container button')).find(b => (b.innerText || '').trim() === 'CONFIRMAR');
    if (confirmBtn) {
      confirmBtn.click();
    }

    return {
      updatedL1: !!inpL1,
      updatedL2: !!inpL2,
      updatedL3: !!inpL3,
      confirmed: !!confirmBtn
    };
  })()`);

  ws.close();
  const totalDurationMs = Date.now() - startTime;

  console.log(JSON.stringify({
    success: true,
    duration_ms: totalDurationMs,
    message: 'Estrategia inyectada con éxito en Loyalfans Live (Tema y Objetivo 3 niveles $11/$22/$33)',
    topic: topicRes,
    goal: goalRes
  }));
  process.exit(0);
}

main().catch(err => {
  console.log(JSON.stringify({ success: false, error: err.message }));
  process.exit(1);
});
"""

    js_script = (
        js_template
        .replace("PORT_PLACEHOLDER", str(port))
        .replace("TOPIC_PLACEHOLDER", json.dumps(topic, ensure_ascii=False))
        .replace("GOAL_L1_PLACEHOLDER", json.dumps(l1_task, ensure_ascii=False))
        .replace("GOAL_L2_PLACEHOLDER", json.dumps(l2_task, ensure_ascii=False))
        .replace("GOAL_L3_PLACEHOLDER", json.dumps(l3_task, ensure_ascii=False))
    )

    temp_script = Path(__file__).resolve().parent.parent.parent.parent / "scratch" / "run_inject_loyalfans.js"
    temp_script.parent.mkdir(parents=True, exist_ok=True)
    temp_script.write_text(js_script, encoding="utf-8")

    project_root = Path(__file__).resolve().parent.parent.parent.parent
    try:
        r = subprocess.run([NODE_PATH, str(temp_script)], cwd=str(project_root), capture_output=True, text=True, timeout=10)
        out = (r.stdout or "").strip()
        if out:
            try:
                return json.loads(out)
            except Exception:
                pass
        return {"success": False, "error": r.stderr or out or "Sin respuesta del inyector de Loyalfans"}
    except Exception as e:
        return {"success": False, "error": str(e)}
