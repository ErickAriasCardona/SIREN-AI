"""
SIREN AI — Conector en Vivo con Mahia (StreamMonitor Desktop)
Controla la interfaz de StreamMonitor vía Chrome DevTools Protocol (CDP):
1. Navega automáticamente al Chat de Mahia mediante el icono lateral: button[aria-label="Mahia"].
2. Espera a que textarea.chakra-textarea esté montado y visible.
3. Escribe la orden táctica usando el setter de valor de React y despacha eventos 'input' y 'change'.
4. Presiona el botón 'Enviar' (button[aria-label="Enviar"]) o pulsa Enter.
5. Monitorea la respuesta streaming de Mahia hasta su estabilización.
6. Extrae y devuelve el texto completo generado por Mahia en vivo.
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

def send_prompt_to_mahia_desktop(prompt_text: str, timeout_seconds: int = 40) -> Dict[str, Any]:
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

    js_template = """const http = require('http');
const fs = require('fs');

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

  const page = targets.find(t => t.type === 'page' && t.url.includes('renderer/index.html')) || targets.find(t => t.type === 'page');
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
          resolve(msg);
        }
      };
      ws.addEventListener('message', h);
      ws.send(JSON.stringify({ id: curId, method, params }));
    });

    // 1. Verificar si ya estamos en la vista de Mahia (textarea ya visible)
    const checkAlready = await send('Runtime.evaluate', {
      expression: `!!(document.querySelector('textarea.chakra-textarea') || document.querySelector('textarea'))`,
      returnByValue: true
    });

    let textareaReady = !!checkAlready?.result?.result?.value;

    if (!textareaReady) {
      // Navegar a Mahia haciendo clic en el icono lateral (Paso 2 / Img 2)
      await send('Runtime.evaluate', {
        expression: `(() => {
          const btn = document.querySelector('button[aria-label="Mahia"]');
          if (btn) btn.click();
        })()`
      });

      // Esperar a que el textarea esté montado en el DOM
      for (let i = 0; i < 30; i++) {
        await new Promise(r => setTimeout(r, 150));
        const chk = await send('Runtime.evaluate', {
          expression: `!!(document.querySelector('textarea.chakra-textarea') || document.querySelector('textarea'))`,
          returnByValue: true
        });
        if (chk?.result?.result?.value) {
          textareaReady = true;
          break;
        }
      }
    }

    if (!textareaReady) {
      console.log(JSON.stringify({ success: false, error: 'Textarea de Mahia no apareció tras hacer clic' }));
      ws.close();
      process.exit(1);
    }

    // 3. Escribir orden táctica en el textarea (Paso 3 / Img 3)
    const pasteRes = await send('Runtime.evaluate', {
      expression: `(() => {
        const ta = document.querySelector('textarea.chakra-textarea') || document.querySelector('textarea');
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

    await new Promise(r => setTimeout(r, 500));

    // 4. Enviar prompt
    await send('Runtime.evaluate', {
      expression: `(() => {
        const btn = document.querySelector('button[aria-label="Enviar"]');
        if (btn && !btn.disabled) {
          btn.click();
          return true;
        }
        const ta = document.querySelector('textarea.chakra-textarea') || document.querySelector('textarea');
        if (ta) {
          ta.dispatchEvent(new KeyboardEvent('keydown', { key: 'Enter', code: 'Enter', keyCode: 13, which: 13, bubbles: true }));
          return true;
        }
        return false;
      })()`,
      returnByValue: true
    });

    // 5. Esperar streaming de Mahia (Paso 4 / Img 4)
    let lastSeenText = '';
    let stableCount = 0;
    let finalMahiaText = '';
    const maxTicks = TIMEOUT_PLACEHOLDER;

    for (let t = 0; t < maxTicks; t++) {
      await new Promise(r => setTimeout(r, 1000));
      const poll = await send('Runtime.evaluate', {
        expression: `(() => {
          const candidates = Array.from(document.querySelectorAll('div.css-1k66j02, div.css-1vunpsv, p.chakra-text'));
          const valid = candidates.map(el => (el.innerText || '').trim())
            .filter(txt => txt.length > 40 && !txt.includes('Modelo fuera de cámara') && !txt.includes('Sam ha definido el foco') && !txt.includes('Sam:'));
          if (valid.length === 0) return { status: 'waiting' };
          const latest = valid[valid.length - 1];
          const thinking = latest.includes('Pensando') || latest === '...';
          return { status: thinking ? 'thinking' : 'ready', text: latest, len: latest.length };
        })()`,
        returnByValue: true
      });

      const pdata = poll?.result?.result?.value;
      if (pdata && pdata.status === 'ready' && pdata.text && pdata.len > 80) {
        if (pdata.text === lastSeenText) {
          stableCount++;
          if (stableCount >= 2) {
            finalMahiaText = pdata.text;
            break;
          }
        } else {
          lastSeenText = pdata.text;
          stableCount = 0;
        }
      }
    }

    if (!finalMahiaText && lastSeenText && lastSeenText.length > 50) {
      finalMahiaText = lastSeenText;
    }

    if (finalMahiaText) {
      console.log(JSON.stringify({
        success: true,
        mahia_response: finalMahiaText,
        live_chat: true,
        steps: ["Img 1 (Inicio)", "Img 2 (Vista Mahia)", "Img 3 (Envío & Pensando)", "Img 4 (Respuesta en Vivo)"]
      }));
      ws.close();
      process.exit(0);
    } else {
      console.log(JSON.stringify({ success: false, error: 'Tiempo de espera agotado esperando a Mahia' }));
      ws.close();
      process.exit(1);
    }
  });
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
    with open(temp_js, "w", encoding="utf-8") as f:
        f.write(js_code)

    try:
        res = subprocess.run(
            [NODE_PATH, str(temp_js)],
            capture_output=True,
            encoding="utf-8",
            errors="replace",
            timeout=timeout_seconds + 5
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
