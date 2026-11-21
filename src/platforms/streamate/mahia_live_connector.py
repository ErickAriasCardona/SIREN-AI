"""
SIREN AI — Conector en Vivo con Mahia (StreamMonitor Desktop)
Controla la interfaz de StreamMonitor vía Chrome DevTools Protocol (CDP):
1. Navega automáticamente al Chat de Mahia (/dashboard/chat).
2. Pega la orden táctica en el textarea de Mahia.
3. Presiona el botón 'Enviar'.
4. Espera a que Mahia termine de generar la respuesta y la extrae.
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

def send_prompt_to_mahia_desktop(prompt_text: str, timeout_seconds: int = 35) -> Dict[str, Any]:
    """
    Envía un prompt a Mahia directamente en la ventana de StreamMonitor Desktop
    y retorna la respuesta recibida en tiempo real.
    """
    port = get_devtools_active_port()
    if not port:
        return {
            "success": False,
            "error": "StreamMonitor no tiene DevToolsActivePort activo. Abre StreamMonitor primero."
        }

    js_code = """
const http = require('http');

async function run() {
  const port = PORT_PLACEHOLDER;
  const promptText = PROMPT_PLACEHOLDER;

  let targets = [];
  try {
    targets = await new Promise((resolve, reject) => {
      http.get('http://127.0.0.1:' + port + '/json', (res) => {
        let d = ''; res.on('data', c => d += c);
        res.on('end', () => {
          try { resolve(JSON.parse(d)); } catch(e) { reject(e); }
        });
      }).on('error', reject);
    });
  } catch(e) {
    console.log(JSON.stringify({ success: false, error: 'No se pudo conectar a CDP: ' + e.message }));
    process.exit(1);
  }

  const page = targets.find(t => t.type === 'page');
  if (!page) {
    console.log(JSON.stringify({ success: false, error: 'No se encontró la página de StreamMonitor en CDP' }));
    process.exit(1);
  }

  const ws = new WebSocket(page.webSocketDebuggerUrl);

  ws.addEventListener('open', async () => {
    let msgId = 1;
    const send = (method, params = {}) => new Promise((resolve) => {
      const curId = msgId++;
      const h = (evt) => {
        const msg = JSON.parse(evt.data);
        if (msg.id === curId) {
          ws.removeEventListener('message', h);
          resolve(msg.result);
        }
      };
      ws.addEventListener('message', h);
      ws.send(JSON.stringify({ id: curId, method, params }));
    });

    // 1. Navegar o enfocar Mahia
    await send('Runtime.evaluate', {
      expression: `
        (() => {
          // Si estamos en otra pestaña, navegar al chat
          if (!window.location.href.includes('/dashboard/chat')) {
            const chatLink = Array.from(document.querySelectorAll('a, button')).find(el => (el.innerText || '').toLowerCase().includes('chat'));
            if (chatLink) chatLink.click();
          }
          // Hacer clic en Mahia
          const mahiaBtn = Array.from(document.querySelectorAll('button')).find(b => (b.innerText || '').includes('Mahia'));
          if (mahiaBtn) mahiaBtn.click();
        })()
      `
    });

    await new Promise(r => setTimeout(r, 600));

    // 2. Contar burbujas actuales de Mahia
    const countRes = await send('Runtime.evaluate', {
      expression: 'document.querySelectorAll(\\'[class*="rounded-bl-md"]\\').length',
      returnByValue: true
    });
    const initialCount = countRes?.result?.value || 0;

    // 3. Pegar prompt en el textarea
    const pasteRes = await send('Runtime.evaluate', {
      expression: `
        (() => {
          const ta = document.querySelector('textarea[placeholder*="Pregúntame"]') || document.querySelector('textarea');
          if (!ta) return { ok: false, error: 'Textarea no encontrado' };

          const setter = Object.getOwnPropertyDescriptor(window.HTMLTextAreaElement.prototype, "value").set;
          setter.call(ta, ${JSON.stringify(promptText)});
          ta.dispatchEvent(new Event('input', { bubbles: true }));
          ta.dispatchEvent(new Event('change', { bubbles: true }));

          // Dar foco
          ta.focus();
          return { ok: true };
        })()
      `,
      returnByValue: true
    });

    if (!pasteRes?.result?.value?.ok) {
      console.log(JSON.stringify({ success: false, error: 'No se pudo escribir en el chat de Mahia' }));
      ws.close();
      process.exit(1);
    }

    await new Promise(r => setTimeout(r, 400));

    // 4. Hacer clic en Enviar
    await send('Runtime.evaluate', {
      expression: `
        (() => {
          const sendBtn = document.querySelector('button[aria-label="Enviar"]');
          if (sendBtn) {
            sendBtn.click();
            return { clicked: true };
          }
          // Fallback disparar Enter en el textarea
          const ta = document.querySelector('textarea');
          if (ta) {
            ta.dispatchEvent(new KeyboardEvent('keydown', { key: 'Enter', code: 'Enter', keyCode: 13, which: 13, bubbles: true }));
            return { enterSent: true };
          }}
          return { error: 'No se encontró botón enviar' };
        })()
      `
    });

    // 5. Esperar respuesta de Mahia
    let lastText = '';
    let stableCount = 0;
    const maxWait = TIMEOUT_PLACEHOLDER * 2;

    for (let step = 0; step < maxWait; step++) {
      await new Promise(r => setTimeout(r, 500));

      const pollRes = await send('Runtime.evaluate', {
        expression: `
          (() => {
            const bubbles = Array.from(document.querySelectorAll('[class*="rounded-bl-md"]'));
            if (bubbles.length > ${initialCount}) {
              const latest = bubbles[bubbles.length - 1];
              const txt = (latest.innerText || '').trim();
              return { hasNew: true, text: txt };
            }
            return { hasNew: false };
          })()
        `,
        returnByValue: true
      });

      const val = pollRes?.result?.value;
      if (val && val.hasNew && val.text) {
        if (val.text === lastText && val.text.length > 20) {
          stableCount++;
          if (stableCount >= 3) {
            // Respuesta terminada de streamear
            console.log(JSON.stringify({ success: true, mahia_response: val.text, live_chat: true }));
            ws.close();
            process.exit(0);
          }
        } else {
          lastText = val.text;
          stableCount = 0;
        }
      }
    }

    if (lastText && lastText.length > 20) {
      console.log(JSON.stringify({ success: true, mahia_response: lastText, live_chat: true, partial: true }));
      ws.close();
      process.exit(0);
    }

    console.log(JSON.stringify({ success: false, error: 'Tiempo de espera agotado esperando a Mahia' }));
    ws.close();
    process.exit(1);
  });
}

run().catch(err => {
  console.log(JSON.stringify({ success: false, error: err.message }));
  process.exit(1);
});
"""

    js_code = js_code.replace("PORT_PLACEHOLDER", str(port))
    js_code = js_code.replace("PROMPT_PLACEHOLDER", json.dumps(prompt_text, ensure_ascii=False))
    js_code = js_code.replace("TIMEOUT_PLACEHOLDER", str(timeout_seconds))

    temp_js = Path(__file__).resolve().parent.parent.parent.parent / "scratch" / "run_mahia_exchange.js"
    temp_js.parent.mkdir(parents=True, exist_ok=True)
    with open(temp_js, "w", encoding="utf-8") as f:
        f.write(js_code)

    try:
        res = subprocess.run([NODE_PATH, str(temp_js)], capture_output=True, text=True, timeout=timeout_seconds + 5)
        output = res.stdout.strip()
        if output:
            try:
                data = json.loads(output)
                return data
            except Exception:
                pass
        return {"success": False, "error": res.stderr or output or "No output from Mahia connector"}
    except Exception as e:
        return {"success": False, "error": str(e)}
