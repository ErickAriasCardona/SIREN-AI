"""
SIREN AI — Inyector de Mensajes Automáticos y Atajos en StreamMonitor Desktop.
Inyecta directamente en la sección 'Mensajes' de StreamMonitor:
1. Saludo a usuarios nuevos (Bienvenida 30s)
2. Mensaje al entrar a privado
3. Propina al recibir golds
4. Mensajes rápidos (Alt+1 a Alt+6) segmentados por tipo de fan
5. Pulsa 'Guardar ajustes' en cada sección para persistir en StreamMonitor.
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

    js_script = f"""
const http = require('http');
const WebSocket = require('ws');

const port = {port};
const welcomeText = {json.dumps(welcome_msg, ensure_ascii=False)};
const privateText = {json.dumps(private_msg, ensure_ascii=False)};
const tipText = {json.dumps(tip_msg, ensure_ascii=False)};
const quickList = {json.dumps(q_msgs, ensure_ascii=False)};

function getTargets() {{
  return new Promise((resolve, reject) => {{
    http.get('http://127.0.0.1:' + port + '/json', res => {{
      let d = ''; res.on('data', c => d += c);
      res.on('end', () => {{ try {{ resolve(JSON.parse(d)); }} catch(e) {{ reject(e); }} }});
    }}).on('error', reject);
  }});
}}

async function main() {{
  const targets = await getTargets();
  const page = targets.find(t => t.url.includes('renderer/index.html')) || targets[0];
  if (!page) {{
    console.log(JSON.stringify({{ success: false, error: 'No se encontró la página principal de StreamMonitor' }}));
    process.exit(1);
  }}

  const ws = new WebSocket(page.webSocketDebuggerUrl);
  await new Promise(r => ws.on('open', r));

  let msgId = 1;
  const send = (method, params = {{}}) => new Promise(resolve => {{
    const curId = msgId++;
    const h = (buf) => {{
      try {{
        const msg = JSON.parse(buf.toString());
        if (msg.id === curId) {{
          ws.removeListener('message', h);
          resolve(msg);
        }}
      }} catch (e) {{}}
    }};
    ws.on('message', h);
    ws.send(JSON.stringify({{ id: curId, method, params }}));
  }});

  // 1. Asegurar que la modal de Mensajes esté visible y montada
  let modalMounted = false;
  for (let attempt = 0; attempt < 5; attempt++) {{
    const chk = await send('Runtime.evaluate', {{
      expression: 'Array.from(document.querySelectorAll("textarea")).some(t => (t.placeholder || "").includes("bienvenid"))',
      returnByValue: true
    }});
    if (chk?.result?.result?.value) {{
      modalMounted = true;
      break;
    }}
    // Si no está montada, hacer clic en el botón Mensajes del sidebar
    await send('Runtime.evaluate', {{
      expression: '(() => {{ const b = document.querySelector("button[aria-label=\\"Mensajes\\"]"); if (b) b.click(); }})()'
    }});
    await new Promise(r => setTimeout(r, 600));
  }}

  if (!modalMounted) {{
    console.log(JSON.stringify({{ success: false, error: 'No se pudo abrir la modal de Mensajes en StreamMonitor' }}));
    ws.close();
    process.exit(1);
  }}

  // 2. Inyectar valores y guardar
  const evalRes = await send('Runtime.evaluate', {{
    expression: `(() => {{
      const allTas = Array.from(document.querySelectorAll('textarea'));
      const taWelcome = allTas.find(t => (t.placeholder || '').includes('bienvenid@ a la sala'));
      const taPrivate = allTas.find(t => (t.placeholder || '').includes('Bienvenid@ al privado'));
      const taTip = allTas.find(t => (t.placeholder || '').includes('Gracias por la propina'));

      const setVal = (ta, val) => {{
        if (!ta || !val) return false;
        const s = Object.getOwnPropertyDescriptor(window.HTMLTextAreaElement.prototype, 'value').set;
        s.call(ta, val);
        ta.dispatchEvent(new Event('input', {{ bubbles: true }}));
        ta.dispatchEvent(new Event('change', {{ bubbles: true }}));
        return true;
      }};

      if (taWelcome) setVal(taWelcome, ${{JSON.stringify(welcomeText)}});
      if (taPrivate) setVal(taPrivate, ${{JSON.stringify(privateText)}});
      if (taTip) setVal(taTip, ${{JSON.stringify(tipText)}});

      // Guardar sección de Mensajes automáticos
      let saveAutoBtn = null;
      if (taTip) {{
        let p = taTip.parentElement;
        for (let i = 0; i < 8 && p; i++) {{
          const b = Array.from(p.querySelectorAll('button')).find(btn => (btn.innerText || '').includes('Guardar ajustes'));
          if (b) {{ saveAutoBtn = b; break; }}
          p = p.parentElement;
        }}
      }}
      if (saveAutoBtn) {{
        saveAutoBtn.click();
      }}

      // Rellenar mensajes rápidos (Alt+1 a Alt+6) segmentados
      const qList = ${{JSON.stringify(quickList)}};
      let saveQuickBtn = null;
      if (qList && qList.length > 0) {{
        for (let idx = 0; idx < Math.min(qList.length, 6); idx++) {{
          const phNeed = 'Mensaje rápido ' + (idx + 1);
          const taQ = allTas.find(t => (t.placeholder || '').includes(phNeed));
          if (taQ) setVal(taQ, qList[idx]);
        }}

        const taQ1 = allTas.find(t => (t.placeholder || '').includes('Mensaje rápido 1'));
        if (taQ1) {{
          let pQ = taQ1.parentElement;
          for (let i = 0; i < 8 && pQ; i++) {{
            const bQ = Array.from(pQ.querySelectorAll('button')).find(btn => (btn.innerText || '').includes('Guardar ajustes'));
            if (bQ) {{ saveQuickBtn = bQ; break; }}
            pQ = pQ.parentElement;
          }}
        }}
        if (saveQuickBtn) {{
          saveQuickBtn.click();
        }}
      }}

      return {{
        success: true,
        welcomeUpdated: !!taWelcome,
        privateUpdated: !!taPrivate,
        tipUpdated: !!taTip,
        autoSaved: !!saveAutoBtn,
        quickSaved: !!saveQuickBtn
      }};
    }})()`,
    returnByValue: true
  }});

  const res = evalRes?.result?.result?.value || {{ success: false }};
  console.log(JSON.stringify(res));
  ws.close();
  process.exit(0);
}}

main().catch(err => {{
  console.log(JSON.stringify({{ success: false, error: err.message }}));
  process.exit(1);
}});
"""

    temp_script = Path(__file__).resolve().parent.parent.parent.parent / "scratch" / "run_inject_messages.js"
    temp_script.parent.mkdir(parents=True, exist_ok=True)
    temp_script.write_text(js_script, encoding="utf-8")

    try:
        r = subprocess.run([NODE_PATH, str(temp_script)], capture_output=True, encoding="utf-8", errors="replace", timeout=15)
        out = (r.stdout or "").strip()
        if out:
            try:
                return json.loads(out)
            except Exception:
                pass
        return {"success": False, "error": r.stderr or out or "Sin respuesta del inyector de mensajes"}
    except Exception as e:
        return {"success": False, "error": str(e)}
