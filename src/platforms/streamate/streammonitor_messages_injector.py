"""
SIREN AI — Inyector de Mensajes Automáticos y Atajos en StreamMonitor Desktop.
Inyecta directamente en la sección 'Mensajes' de StreamMonitor:
1. Saludo a usuarios nuevos (Bienvenida 30s)
2. Mensaje al entrar a privado
3. Propina al recibir golds
4. Mensajes rápidos (Alt+1 a Alt+6) segmentados por tipo de fan
5. Pulsa 'Guardar ajustes' en cada sección para persistir en StreamMonitor.
6. Regresa de inmediato a la vista de transmisión activa ('Plataformas') para ver Streamate y Loyalfans.
"""

import os
import json
import subprocess
from pathlib import Path
from typing import Dict, List, Any, Optional

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

def inject_streammonitor_auto_and_quick_messages(auto_messages: Dict[str, str], quick_messages: Optional[List[str]] = None) -> Dict[str, Any]:
    port = get_devtools_active_port()
    if not port:
        return {"success": False, "error": "StreamMonitor no tiene DevToolsActivePort activo."}

    welcome_msg = auto_messages.get("room_30s") or auto_messages.get("welcome") or ""
    private_msg = auto_messages.get("private_show") or auto_messages.get("private") or ""
    tip_msg = auto_messages.get("send_golds") or auto_messages.get("tip") or ""
    q_msgs = quick_messages or []

    # Construimos el script de Node.js
    js_template = r"""
const http = require('http');
const WebSocket = require('ws');

const port = PORT_PLACEHOLDER;
const welcomeText = WELCOME_PLACEHOLDER;
const privateText = PRIVATE_PLACEHOLDER;
const tipText = TIP_PLACEHOLDER;
const quickList = QUICK_PLACEHOLDER;

function getTargets() {
  return new Promise((resolve, reject) => {
    http.get('http://127.0.0.1:' + port + '/json', res => {
      let d = ''; res.on('data', c => d += c);
      res.on('end', () => { try { resolve(JSON.parse(d)); } catch(e) { reject(e); } });
    }).on('error', reject);
  });
}

async function main() {
  const targets = await getTargets();
  const page = targets.find(t => t.url && t.url.includes('renderer/index.html')) || targets[0];
  if (!page) {
    console.log(JSON.stringify({ success: false, error: 'No se encontró la página principal de StreamMonitor' }));
    process.exit(1);
  }

  const ws = new WebSocket(page.webSocketDebuggerUrl);
  await new Promise(r => ws.on('open', r));

  let msgId = 1;
  const send = (method, params = {}) => new Promise(resolve => {
    const curId = msgId++;
    const h = (buf) => {
      try {
        const msg = JSON.parse(buf.toString());
        if (msg.id === curId) {
          ws.removeListener('message', h);
          resolve(msg);
        }
      } catch (e) {}
    };
    ws.on('message', h);
    ws.send(JSON.stringify({ id: curId, method, params }));
  });

  // 1. Comprobar si los textareas de Mensajes ya están montados
  const checkInitial = await send('Runtime.evaluate', {
    expression: 'document.querySelectorAll("textarea").length >= 3',
    returnByValue: true
  });

  if (!checkInitial?.result?.result?.value) {
    // Abrir haciendo clic en Mensajes UNA sola vez
    await send('Runtime.evaluate', {
      expression: '(() => { const b = document.querySelector("button[aria-label=Mensajes]"); if (b) b.click(); })()'
    });
    // Esperar a que se monte
    for (let i = 0; i < 12; i++) {
      await new Promise(r => setTimeout(r, 350));
      const chk = await send('Runtime.evaluate', {
        expression: 'document.querySelectorAll("textarea").length >= 3',
        returnByValue: true
      });
      if (chk?.result?.result?.value) break;
    }
  }

  // 2. Inyectar valores y guardar
  const evalRes = await send('Runtime.evaluate', {
    expression: `(() => {
      const allTas = Array.from(document.querySelectorAll('textarea'));
      const norm = s => (s || '').toLowerCase().normalize("NFD").replace(/[\\u0300-\\u036f]/g, "");
      const taWelcome = allTas.find(t => norm(t.placeholder).includes('bienvenid') && norm(t.placeholder).includes('sala'));
      const taPrivate = allTas.find(t => norm(t.placeholder).includes('privado'));
      const taTip = allTas.find(t => norm(t.placeholder).includes('propina'));

      const setVal = (ta, val) => {
        if (!ta || !val) return false;
        const s = Object.getOwnPropertyDescriptor(window.HTMLTextAreaElement.prototype, 'value').set;
        s.call(ta, val);
        ta.dispatchEvent(new Event('input', { bubbles: true }));
        ta.dispatchEvent(new Event('change', { bubbles: true }));
        return true;
      };

      if (taWelcome) setVal(taWelcome, ${JSON.stringify(welcomeText)});
      if (taPrivate) setVal(taPrivate, ${JSON.stringify(privateText)});
      if (taTip) setVal(taTip, ${JSON.stringify(tipText)});

      // Rellenar mensajes rápidos (Alt+1 a Alt+8) segmentados sin emojis
      const qList = ${JSON.stringify(quickList)};
      let quickUpdatedCount = 0;
      if (qList && qList.length > 0) {
        for (let idx = 0; idx < Math.min(qList.length, 8); idx++) {
          const numStr = String(idx + 1);
          let taQ = allTas.find(t => norm(t.placeholder).includes('rapido ' + numStr));
          if (!taQ && allTas[idx]) taQ = allTas[idx];
          if (taQ) {
            setVal(taQ, qList[idx]);
            quickUpdatedCount++;
          }
        }
      }

      // Localizar botones de 'Guardar ajustes' en cada sección
      const allBtns = Array.from(document.querySelectorAll('button'));
      const saveBtns = allBtns.filter(b => (b.innerText || '').includes('Guardar ajustes'));

      let quickSaved = false;
      let autoSaved = false;
      let customSaved = false;

      // saveBtns[0]: Guardar Mensajes Rápidos (Alt+1 a Alt+8)
      if (saveBtns[0]) {
        saveBtns[0].click();
        quickSaved = true;
      }

      // saveBtns[1]: Guardar Mensajes Automáticos (Saludo 30s, Privado, Propina)
      if (saveBtns[1]) {
        saveBtns[1].click();
        autoSaved = true;
      }

      // Limpiar emojis de mensajes personalizados periódicos si existen (textareas 11+)
      for (let idx = 11; idx < allTas.length; idx++) {
        const taCustom = allTas[idx];
        if (taCustom && taCustom.value) {
          const cleanText = taCustom.value.replace(/[\u{1F300}-\u{1F9FF}\u{2600}-\u{26FF}\u{2700}-\u{27BF}\u{1F1E0}-\u{1F1FF}]/gu, '').trim();
          if (cleanText !== taCustom.value) {
            setVal(taCustom, cleanText);
          }
        }
      }
      if (saveBtns[2]) {
        saveBtns[2].click();
        customSaved = true;
      }

      return {
        success: true,
        welcomeUpdated: !!taWelcome,
        privateUpdated: !!taPrivate,
        tipUpdated: !!taTip,
        quickUpdatedCount,
        autoSaved,
        quickSaved,
        customSaved
      };
    })()`,
    returnByValue: true
  });

  const res = evalRes?.result?.result?.value || { success: false };

  // 3. Regresar de inmediato a la vista de transmisión activa ('Plataformas' / split multi-streaming)
  await new Promise(r => setTimeout(r, 600));
  await send('Runtime.evaluate', {
    expression: `(() => {
      const platBtn = document.querySelector('button[aria-label="Plataformas"]');
      if (platBtn) { platBtn.click(); return 'Switched to Plataformas'; }
      const inicioBtn = document.querySelector('button[aria-label="Inicio"]');
      if (inicioBtn) { inicioBtn.click(); return 'Switched to Inicio'; }
      return 'None';
    })()`
  });
  await new Promise(r => setTimeout(r, 400));

  console.log(JSON.stringify(res));
  ws.close();
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
        .replace("WELCOME_PLACEHOLDER", json.dumps(welcome_msg, ensure_ascii=False))
        .replace("PRIVATE_PLACEHOLDER", json.dumps(private_msg, ensure_ascii=False))
        .replace("TIP_PLACEHOLDER", json.dumps(tip_msg, ensure_ascii=False))
        .replace("QUICK_PLACEHOLDER", json.dumps(q_msgs, ensure_ascii=False))
    )

    temp_script = Path(__file__).resolve().parent.parent.parent.parent / "scratch" / "run_inject_messages.js"
    temp_script.parent.mkdir(parents=True, exist_ok=True)
    temp_script.write_text(js_script, encoding="utf-8")

    project_root = Path(__file__).resolve().parent.parent.parent.parent
    custom_env = dict(os.environ)
    custom_env["NODE_PATH"] = str(project_root / "node_modules")

    try:
        r = subprocess.run([NODE_PATH, str(temp_script)], cwd=str(project_root), env=custom_env, capture_output=True, text=True, timeout=20)
        out = (r.stdout or "").strip()
        if out:
            try:
                return json.loads(out)
            except Exception:
                pass
        return {"success": False, "error": r.stderr or out or "Sin respuesta del inyector de mensajes"}
    except Exception as e:
        return {"success": False, "error": str(e)}
