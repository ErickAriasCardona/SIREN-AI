"""
SIREN AI — Conector en Vivo con Mahia (StreamMonitor Desktop)
Controla la interfaz de StreamMonitor vía Chrome DevTools Protocol (CDP):
1. Asegura que StreamMonitor Desktop esté ejecutándose y visible en la pantalla del usuario.
2. Abre y enfoca el panel de chat de Mahia: button[aria-label="Mahia"].
3. PRESERVA SIEMPRE EL HISTORIAL EXISTENTE (continúa en el hilo activo).
4. Cuenta las respuestas previas para detectar con exactitud la nueva respuesta generada.
5. Escribe la consulta o comando táctico usando el setter de React y despacha eventos 'input' y 'change'.
6. Presiona el botón 'Enviar' (button[aria-label="Enviar"]).
7. Monitorea el streaming hasta su estabilización y retorna la respuesta en tiempo real.
"""

import os
import sys
import json
import time
import subprocess
import urllib.request
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
                port = int(lines[0].strip())
                # Validar rápidamente si el socket está escuchando
                try:
                    with urllib.request.urlopen(f"http://127.0.0.1:{port}/json", timeout=1.0) as r:
                        if r.status == 200:
                            return port
                except Exception:
                    pass
    except Exception:
        pass
    return None

def ensure_streammonitor_running(max_wait_seconds: int = 15) -> Optional[int]:
    """Verifica si StreamMonitor está corriendo; si está cerrado, lo lanza automáticamente y espera su puerto CDP."""
    port = get_devtools_active_port()
    if port:
        try:
            from src.platforms.streamate.stream_monitor_orchestrator import focus_streammonitor_window
            focus_streammonitor_window()
        except Exception:
            pass
        return port

    # Iniciar StreamMonitor
    exe_candidates = [
        Path("C:/Users/MI PC/AppData/Local/Programs/streammonitor/streammonitor.exe"),
        Path(os.environ.get("LOCALAPPDATA", "C:/Users/MI PC/AppData/Local")) / "Programs" / "streammonitor" / "streammonitor.exe",
        Path(__file__).resolve().parent.parent.parent.parent / "run_streammonitor.bat"
    ]

    started = False
    for candidate in exe_candidates:
        if candidate.exists():
            try:
                if candidate.suffix == ".bat":
                    subprocess.Popen(["cmd.exe", "/c", str(candidate)], shell=False)
                else:
                    subprocess.Popen([str(candidate)], shell=False)
                started = True
                print(f"[Mahia Connector]: Iniciando StreamMonitor desde {candidate}...")
                break
            except Exception as e:
                print(f"[Mahia Connector Launch Error]: {e}")

    if not started:
        print("[Mahia Connector]: No se encontró el ejecutable de StreamMonitor.")
        return None

    # Esperar a que el puerto se active
    start_t = time.time()
    while time.time() - start_t < max_wait_seconds:
        time.sleep(1.0)
        port = get_devtools_active_port()
        if port:
            try:
                from src.platforms.streamate.stream_monitor_orchestrator import focus_streammonitor_window
                focus_streammonitor_window()
            except Exception:
                pass
            print(f"[Mahia Connector]: StreamMonitor conectado exitosamente en puerto {port}.")
            return port

    return None

def send_prompt_to_mahia_desktop(prompt_text: str, timeout_seconds: int = 50) -> Dict[str, Any]:
    """
    Envía un prompt a Mahia directamente en el chat con historial continuo en StreamMonitor Desktop
    y retorna la respuesta recibida en tiempo real.
    """
    port = ensure_streammonitor_running(max_wait_seconds=12)
    if not port:
        return {
            "success": False,
            "error": "No se pudo conectar a StreamMonitor. Asegúrate de que la aplicación esté instalada."
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

  // 1. Cerrar solo modales emergentes superpuestas (no botones de menú ni iconos)
  await send('Runtime.evaluate', {
    expression: `(() => {
      const modalClose = document.querySelector('div[role="dialog"] button[aria-label="Close"], div[role="dialog"] button[aria-label="Cerrar"]');
      if (modalClose) modalClose.click();
    })()`
  });
  await sleep(300);

  // 2. Asegurar vista de Mahia pulsando el icono lateral de Mahia si no está ya montado su textarea
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
    if (st && st.status === 'ready' && st.text && st.length > 50) {
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

  if (!finalResponse && latestText && latestText.length > 40) {
    finalResponse = latestText;
  }

  if (finalResponse) {
    console.log(JSON.stringify({
      success: true,
      mahia_response: finalResponse,
      response: finalResponse,
      reply: finalResponse,
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
                if data.get("mahia_response") and not data.get("response"):
                    data["response"] = data["mahia_response"]
                if data.get("mahia_response") and not data.get("reply"):
                    data["reply"] = data["mahia_response"]
                return data
            except Exception:
                pass
        return {"success": False, "error": res.stderr or output or "No output from Mahia connector"}
    except Exception as e:
        return {"success": False, "error": str(e)}
