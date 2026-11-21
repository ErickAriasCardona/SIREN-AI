"""
SIREN AI — Conector en Vivo con Mahia (StreamMonitor Desktop)
Controla la interfaz de StreamMonitor vía Chrome DevTools Protocol (CDP):
1. Cierra modales superpuestas (como Mensajes) si están abiertas.
2. Navega al Chat de Mahia mediante el icono lateral: button[aria-label="Mahia"].
3. PRESERVA SIEMPRE EL HISTORIAL EXISTENTE (NO abre chat nuevo).
4. Cuenta los mensajes previos para detectar con precisión la nueva respuesta generada en el mismo hilo.
5. Escribe la orden táctica usando el setter de React y despacha eventos 'input' y 'change'.
6. Presiona el botón 'Enviar' (button[aria-label="Enviar"]).
7. Monitorea la nueva respuesta streaming hasta su estabilización y la retorna.
"""

import os
import sys
import json
import time
import subprocess
from pathlib import Path
from typing import Dict, Any, Optional

NODE_PATH = "node"

def get_devtools_active_port() -> Optional[int]:
    """Obtiene el puerto CDP dinámico de StreamMonitor."""
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

def send_prompt_to_mahia_desktop(prompt_text: str, timeout_seconds: int = 50) -> Dict[str, Any]:
    """
    Envía un prompt a Mahia directamente en el chat con historial continuo en StreamMonitor Desktop
    y retorna la respuesta recibida en tiempo real.
    """
    port = get_devtools_active_port()
    if not port:
        return {
            "success": False,
            "error": "StreamMonitor no tiene DevToolsActivePort activo. Abre StreamMonitor primero."
        }

    js_template = """const http = require('http');
const WebSocket = require('ws');

const port = PORT_PLACEHOLDER;
const promptText = PROMPT_PLACEHOLDER;
const maxSeconds = TIMEOUT_PLACEHOLDER;

const sleep = ms => new Promise(r => setTimeout(r, ms));

function getTargets() {
  return new Promise((resolve, reject) => {
    http.get('http://127.0.0.1:' + port + '/json', (res) => {
      let d = ''; res.on('data', c => d += c);
      res.on('end', () => {
        try { resolve(JSON.parse(d)); } catch(e) { reject(e); }
      });
    }).on('error', reject);
  });
}

async function run() {
  let targets = [];
  try {
    targets = await getTargets();
  } catch(e) {
    console.log(JSON.stringify({ success: false, error: 'No se pudo conectar a CDP: ' + e.message }));
    process.exit(1);
  }

  const page = targets.find(t => t.type === 'page' && t.url.includes('renderer/index.html')) || targets.find(t => t.type === 'page');
  if (!page) {
    console.log(JSON.stringify({ success: false, error: 'No se encontró la página de StreamMonitor en CDP' }));
    process.exit(1);
  }

  const ws = new WebSocket(page.webSocketDebuggerUrl);
  await new Promise(r => ws.on('open', r));

  let msgId = 1;
  const send = (method, params = {}) => new Promise((resolve) => {
    const curId = msgId++;
    const h = (data) => {
      try {
        const msg = JSON.parse(data.toString());
        if (msg.id === curId) {
          ws.removeListener('message', h);
          resolve(msg);
        }
      } catch(e) {}
    };
    ws.on('message', h);
    ws.send(JSON.stringify({ id: curId, method, params }));
  });

  // 1. Si hay alguna modal abierta (como Mensajes), cerrarla para despejar la vista
  await send('Runtime.evaluate', {
    expression: `(() => {
      const closeBtns = Array.from(document.querySelectorAll('button')).filter(b => (b.innerText || '').trim() === '✕');
      closeBtns.forEach(b => b.click());
    })()`
  });
  await sleep(400);

  // 2. Asegurar vista de Mahia pulsando el icono lateral si no está ya montado su textarea
  await send('Runtime.evaluate', {
    expression: `(() => {
      const ta = document.querySelector('textarea[placeholder*="Pregunta por tus datos"]') || document.querySelector('textarea.chakra-textarea');
      const sendBtn = document.querySelector('button[aria-label="Enviar"]');
      if (!ta || !sendBtn) {
        const btn = document.querySelector('button[aria-label="Mahia"]');
        if (btn) btn.click();
      }
    })()`
  });
  await sleep(700);

  // 3. PRESERVAR HISTORIAL: Contar cuántas respuestas previas existen en el hilo ANTES de enviar el nuevo mensaje
  const prevCountRes = await send('Runtime.evaluate', {
    expression: `(() => {
      return document.querySelectorAll('button[aria-label="Copiar respuesta"]').length;
    })()`,
    returnByValue: true
  });
  const prevCount = prevCountRes?.result?.result?.value || 0;

  // 4. Pegar prompt en el textarea específico de Mahia (sin abrir chat nuevo)
  const pasteRes = await send('Runtime.evaluate', {
    expression: `(() => {
      const ta = document.querySelector('textarea[placeholder*="Pregunta por tus datos"]') || document.querySelector('textarea.chakra-textarea') || document.querySelector('textarea');
      if (!ta) return false;
      const setter = Object.getOwnPropertyDescriptor(window.HTMLTextAreaElement.prototype, "value").set;
      setter.call(ta, ${JSON.stringify(promptText)});
      ta.dispatchEvent(new Event('input', { bubbles: true }));
      ta.dispatchEvent(new Event('change', { bubbles: true }));
      ta.focus();
      return true;
    })()`,
    returnByValue: true
  });

  await sleep(500);

  // 5. Pulsar botón 'Enviar'
  await send('Runtime.evaluate', {
    expression: `(() => {
      const btn = document.querySelector('button[aria-label="Enviar"]');
      if (btn && !btn.disabled) {
        btn.click();
        return 'btn_clicked';
      }
      const ta = document.querySelector('textarea[placeholder*="Pregunta por tus datos"]') || document.querySelector('textarea.chakra-textarea');
      if (ta) {
        ta.dispatchEvent(new KeyboardEvent('keydown', { key: 'Enter', code: 'Enter', keyCode: 13, which: 13, bubbles: true }));
        return 'enter_dispatched';
      }
      return false;
    })()`,
    returnByValue: true
  });

  // 6. Monitorear streaming buscando la NUEVA respuesta generada en el historial
  let latestText = '';
  let stableCount = 0;
  let finalResponse = null;

  for (let t = 0; t < maxSeconds; t++) {
    await sleep(1000);
    const poll = await send('Runtime.evaluate', {
      expression: `(() => {
        const copyBtns = Array.from(document.querySelectorAll('button[aria-label="Copiar respuesta"]'));
        const targetCount = ${prevCount};

        // Si aún no se ha montado una nueva respuesta más allá de las que ya existían en el historial
        if (copyBtns.length <= targetCount) {
          const thinking = Array.from(document.querySelectorAll('*')).some(el => (el.innerText || '').includes('Pensando'));
          return { status: thinking ? 'thinking' : 'waiting' };
        }

        // El último botón de copiar respuesta corresponde exactamente a la NUEVA respuesta en el hilo
        const lastBtn = copyBtns[copyBtns.length - 1];
        let parent = lastBtn.parentElement;
        while (parent && parent.innerText.length < 50) {
          parent = parent.parentElement;
        }
        const txt = parent ? parent.innerText.replace(/Leer en voz alta|Copiar respuesta/g, '').trim() : '';
        const isThinking = txt.includes('Pensando') || txt.endsWith('...');
        return {
          status: isThinking ? 'thinking' : 'ready',
          text: txt,
          length: txt.length
        };
      })()`,
      returnByValue: true
    });

    const st = poll?.result?.result?.value;
    if (st && st.status === 'ready' && st.text && st.length > 80) {
      if (st.text === latestText) {
        stableCount++;
        if (stableCount >= 2) {
          finalResponse = st.text;
          break;
        }
      } else {
        latestText = st.text;
        stableCount = 0;
      }
    }
  }

  if (!finalResponse && latestText && latestText.length > 60) {
    finalResponse = latestText;
  }

  if (finalResponse) {
    console.log(JSON.stringify({
      success: true,
      mahia_response: finalResponse,
      live_chat: true,
      preserved_history: true,
      steps: ["Historial preservado", "Prompt entregado en hilo continuo", "Streaming monitoreado", "Respuesta final estabilizada"]
    }));
    ws.close();
    process.exit(0);
  } else {
    console.log(JSON.stringify({ success: false, error: 'Tiempo de espera agotado esperando nueva respuesta de Mahia en el historial' }));
    ws.close();
    process.exit(1);
  }
}

run().catch(err => {
  console.log(JSON.stringify({ success: false, error: err.message }));
  process.exit(1);
});
"""

    js_code = js_template.replace("PORT_PLACEHOLDER", str(port))
    js_code = js_code.replace("PROMPT_PLACEHOLDER", json.dumps(prompt_text, ensure_ascii=False))
    js_code = js_code.replace("TIMEOUT_PLACEHOLDER", str(timeout_seconds))

    temp_js = Path(__file__).resolve().parent.parent.parent.parent / "scratch" / "run_mahia_exchange.js"
    temp_js.parent.mkdir(parents=True, exist_ok=True)
    temp_js.write_text(js_code, encoding="utf-8")

    try:
        res = subprocess.run(
            [NODE_PATH, str(temp_js)],
            capture_output=True,
            encoding="utf-8",
            errors="replace",
            timeout=timeout_seconds + 10
        )
        output = (res.stdout or "").strip()
        if output:
            try:
                data = json.loads(output)
                return data
            except Exception:
                pass
        return {"success": False, "error": res.stderr or output or "No output from Mahia connector"}
    except Exception as e:
        return {"success": False, "error": str(e)}
