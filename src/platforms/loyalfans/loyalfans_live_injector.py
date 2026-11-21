"""
SIREN AI — Inyector en Vivo para Transmisión de Loyalfans dentro de StreamMonitor.
Flujo de automatización completo y resiliente:
1. Detecta la pestaña/webview de Loyalfans en StreamMonitor (puerto CDP).
2. Si está en /profile o inicio, navega a la sala de transmisión en vivo (/broadcast).
3. Cierra advertencias de adultos y popup de seguridad ("Mantente Seguro").
4. Inyecta el Room Topic idéntico al de Streamate en los Ajustes de la sala y pulsa GUARDAR.
5. Inyecta el Objetivo de Sala con los 3 niveles requeridos por Sam ($11, $22, $33) y pulsa CONFIRMAR.
6. Deja la sala lista con el botón 'INICIAR TRANSMISIÓN' visible.
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

    # Valores por defecto para el objetivo de Loyalfans
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

async function evalInTarget(wsUrl, expr) {
  const ws = new WebSocket(wsUrl);
  await new Promise(r => ws.on('open', r));
  return new Promise(resolve => {
    ws.send(JSON.stringify({
      id: 1,
      method: 'Runtime.evaluate',
      params: { expression: expr, returnByValue: true }
    }));
    ws.on('message', m => {
      try {
        const data = JSON.parse(m.toString());
        ws.close();
        resolve(data?.result?.result?.value);
      } catch(e) {
        ws.close();
        resolve(null);
      }
    });
  });
}

async function main() {
  let targets = await getTargets();
  let lf = targets.find(t => t.url.includes('loyalfans.com'));

  // Reintento si Loyalfans aún no ha montado
  for (let i = 0; i < 5 && !lf; i++) {
    await new Promise(r => setTimeout(r, 1000));
    targets = await getTargets();
    lf = targets.find(t => t.url.includes('loyalfans.com'));
  }

  if (!lf) {
    console.log(JSON.stringify({ success: false, error: 'No se encontró la página de Loyalfans en StreamMonitor' }));
    process.exit(1);
  }

  const wsUrl = lf.webSocketDebuggerUrl;

  // 1. Cerrar advertencias de cookies o contenido adulto si aparecen
  await evalInTarget(wsUrl, `(() => {
    const btn = Array.from(document.querySelectorAll('button')).find(b => (b.innerText || '').includes('ACEPTA TODO') || (b.innerText || '').includes('ACEPTAR'));
    if (btn) btn.click();
  })()`);
  await new Promise(r => setTimeout(r, 400));

  // 2. Si no está en /broadcast, navegar directamente
  const curUrl = await evalInTarget(wsUrl, 'window.location.href');
  if (!curUrl || !curUrl.includes('/broadcast')) {
    await evalInTarget(wsUrl, 'window.location.href = "https://www.loyalfans.com/broadcast"');
    await new Promise(r => setTimeout(r, 2500));
  }

  // 3. Cerrar popup de seguridad si aparece
  await evalInTarget(wsUrl, `(() => {
    const btn = Array.from(document.querySelectorAll('button')).find(b => (b.innerText || '').includes('CONFIRMAR'));
    if (btn) btn.click();
  })()`);
  await new Promise(r => setTimeout(r, 500));

  // 4. Inyectar Room Topic en Ajustes
  await evalInTarget(wsUrl, `(() => {
    const gear = document.querySelector('i.lf-settings');
    if (gear) {
      gear.click();
      if (gear.parentElement) gear.parentElement.click();
    }
  })()`);
  await new Promise(r => setTimeout(r, 600));

  const saveTopicRes = await evalInTarget(wsUrl, `(() => {
    const topicInp = document.querySelector('input[placeholder="Tema de chat"]');
    if (topicInp) {
      const setter = Object.getOwnPropertyDescriptor(window.HTMLInputElement.prototype, 'value').set;
      setter.call(topicInp, ${JSON.stringify(targetTopic)});
      topicInp.dispatchEvent(new Event('input', { bubbles: true }));
      topicInp.dispatchEvent(new Event('change', { bubbles: true }));

      let p = topicInp.parentElement;
      let saveBtn = null;
      for (let i = 0; i < 4 && p; i++) {
        saveBtn = Array.from(p.querySelectorAll('button')).find(b => (b.innerText || '').trim() === 'GUARDAR');
        if (saveBtn) break;
        p = p.parentElement;
      }
      if (saveBtn) {
        saveBtn.click();
      }

      // Cerrar modal de ajustes tras guardar
      setTimeout(() => {
        const closeBtn = document.querySelector('.mat-mdc-dialog-container .lf-close, [mat-dialog-close], .close-button');
        if (closeBtn) closeBtn.click();
        const backdrop = document.querySelector('.cdk-overlay-backdrop');
        if (backdrop) backdrop.click();
      }, 300);

      return { updated: true, saved: !!saveBtn };
    }
    return { updated: false };
  })()`);
  await new Promise(r => setTimeout(r, 600));

  // 5. Inyectar Objetivo 3 niveles ($11, $22, $33)
  await evalInTarget(wsUrl, `(() => {
    const btn = Array.from(document.querySelectorAll('button')).find(b => (b.innerText || '').includes('EDITAR OBJETIVO'));
    if (btn) btn.click();
  })()`);
  await new Promise(r => setTimeout(r, 800));

  const saveGoalRes = await evalInTarget(wsUrl, `(() => {
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

    if (inpL1) setInp(inpL1, ${JSON.stringify(goalL1)});
    if (inpL2) setInp(inpL2, ${JSON.stringify(goalL2)});
    if (inpL3) setInp(inpL3, ${JSON.stringify(goalL3)});

    // Precios: inputs numéricos de cada nivel ($11, $22, $33)
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

  console.log(JSON.stringify({
    success: true,
    message: 'Estrategia inyectada con éxito en Loyalfans Live (Tema y Objetivo 3 niveles $11/$22/$33)',
    topic: saveTopicRes,
    goal: saveGoalRes
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

    try:
        r = subprocess.run([NODE_PATH, str(temp_script)], capture_output=True, text=True, timeout=25)
        out = (r.stdout or "").strip()
        if out:
            try:
                return json.loads(out)
            except Exception:
                pass
        return {"success": False, "error": r.stderr or out or "Sin respuesta del inyector de Loyalfans"}
    except Exception as e:
        return {"success": False, "error": str(e)}
