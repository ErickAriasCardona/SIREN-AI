"""
SIREN AI — Inyector y Autenticador en Vivo para la Transmisión de Streamate dentro de StreamMonitor.
Flujo de automatización completo:
1. Activa la pestaña 'Streamate' en StreamMonitor.
2. Si aparece el botón 'Entrar a Streamate' (Listo para transmitir), le hace clic automáticamente.
3. Si requiere inicio de sesión (/login), ingresa las credenciales guardadas (EFAC05@YOPMAIL.COM / Centenario123@) y envía.
4. Si está en dashboard-creator, pulsa el botón 'Stream' para abrir la consola de transmisión.
5. Inyecta el Room Topic (<= 140 chars) y Menú Gold (3G) directamente en SMConnect.
"""

import os
import sys
import json
import subprocess
from pathlib import Path
from typing import Dict, List, Any

NODE_PATH = "node"

def get_devtools_active_port():
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

def inject_strategy_into_smconnect(topic: str, gold_menu: List[Dict[str, Any]], wheel_items: List[str] = None) -> Dict[str, Any]:
    port = get_devtools_active_port()
    if not port:
        return {"success": False, "error": "StreamMonitor no tiene DevToolsActivePort activo."}

    # Leer credenciales guardadas
    creds_file = Path(__file__).resolve().parent.parent.parent.parent / "data" / "credentials.json"
    username = "EFAC05@YOPMAIL.COM"
    password = "Centenario123@"
    if creds_file.exists():
        try:
            import base64
            with open(creds_file, "r", encoding="utf-8") as f:
                cdata = json.load(f)
                sm_c = cdata.get("streamate", {})
                if sm_c.get("username"):
                    username = sm_c["username"]
                if sm_c.get("password"):
                    try:
                        password = base64.b64decode(sm_c["password"]).decode("utf-8")
                    except Exception:
                        password = sm_c["password"]
        except Exception:
            pass

    js_runner = f"""
const http = require('http');
const fs = require('fs');

const topic = {json.dumps(topic, ensure_ascii=False)};
const goldMenu = {json.dumps(gold_menu, ensure_ascii=False)};
const port = {port};
const USERNAME = {json.dumps(username, ensure_ascii=False)};
const PASSWORD = {json.dumps(password, ensure_ascii=False)};

const DEFAULT_OPTIONS = {{
  "0": "10x nalgadas", "1": "5x azotes", "2": "Acercamiento en pies", "3": "Acercamiento en rostro",
  "4": "Acercamiento en senos", "5": "Agacharse", "6": "Agita el trasero", "7": "Aplaude con los senos",
  "8": "Apreciación de diosa", "9": "Apretón de culo", "10": "Apretón de senos", "11": "ASMR",
  "12": "Axila", "13": "Azotar", "14": "Azotate", "15": "Baila si sostén", "16": "Baile",
  "17": "Baile en tubo", "18": "Cambiar atuendo", "19": "Cambiar zapatos", "20": "Camiseta mojada",
  "21": "Cara de placer", "22": "Chupar dedo", "23": "Chupar dedos de pies", "24": "Coletas",
  "25": "Con tacones", "26": "Coquetear con hielos", "27": "Coquetear con loción", "28": "Coqueteo con aceite",
  "29": "Cuento sucio", "30": "Da vueltas sin sostén", "31": "De cabeza", "32": "Deseos de cumpleaños",
  "33": "Desnuda con manos en los senos", "34": "Di mi nombre", "35": "Dildo", "36": "Enséñame las tetas",
  "37": "Enviar video", "38": "Envía fotografía", "39": "Escupir", "40": "Estriptís",
  "41": "Flexionar", "42": "Flexiones", "43": "Frota mis bragas", "44": "Fumar un cigarro",
  "45": "Gemido", "46": "Gemir mi nombre", "47": "Giro rápido", "48": "Golpear culo con paleta",
  "49": "Golpes en el coño", "50": "Hazme acabar", "51": "Hazme amordazar", "52": "Hazme babear",
  "53": "Insultar", "54": "Juega tres en línea conmigo", "55": "Jugueteo de mamada", "56": "Lactar",
  "57": "Lame el pezón", "58": "Lame pezón", "59": "Lame vibrador", "60": "Lamer labios",
  "61": "Lanzar un beso", "62": "Lápiz labial", "63": "Mamada con juguete", "64": "Marcador",
  "65": "Masaje de senos", "66": "Masturbar con juguete", "67": "Masturbar con senos", "68": "Monta la almohada",
  "69": "Monte de Venus", "70": "Mordaza", "71": "Mostrar juguetes", "72": "Mostrar lengua",
  "73": "Mostrar vientre", "74": "Muestra el trasero", "75": "Muestra los tatuajes", "76": "Muéstrame el culo",
  "77": "Muéstrame los pies", "78": "Nombre en el cuerpo", "79": "Palabras sucias", "80": "Pellizcar pezones",
  "81": "Pinzas en pezones", "82": "Poner pantimedias (sin desnudo)", "83": "Ponete aceite en los senos",
  "84": "Ponte aceite en el trasero", "85": "Ponte de pie", "86": "Posición de perrito",
  "87": "Provocación con garganta profunda", "88": "Provocame con todo el cuerpo", "89": "Puntua tu verga",
  "90": "Quitar pantimedias (sin desnudo)", "91": "Quitarse el top", "92": "Quiño", "93": "Rebota el trasero",
  "94": "Rebote de senos", "95": "Sacar el dedo", "96": "Sacudir el culo", "97": "Saltar arriba y abajo",
  "98": "Sarcasmo", "99": "Sentadillas", "100": "Shake weight", "101": "Sonrisa", "102": "SPH",
  "103": "Thighmaster", "104": "Tipo", "105": "Tributo", "106": "twerk",
  "107": "Varita Hitachi / Magic Wand", "108": "Yoga sensual"
}};

function getOptionId(name) {{
  const norm = (s) => s.toLowerCase().normalize("NFD").replace(/[\\u0300-\\u036f]/g, "").trim();
  const target = norm(name);
  for (const [id, val] of Object.entries(DEFAULT_OPTIONS)) {{
    if (norm(val) === target || target.includes(norm(val)) || norm(val).includes(target)) {{
      return id;
    }}
  }}
  return "0";
}}

async function run() {{
  const getTargets = () => new Promise((res, rej) => http.get('http://127.0.0.1:' + port + '/json', r => {{
    let d = ''; r.on('data', c => d += c); r.on('end', () => {{ try {{ res(JSON.parse(d)); }} catch(e) {{ rej(e); }} }});
  }}).on('error', rej));

  let targets = await getTargets();

  // 1. Activar pestaña Streamate y pulsar 'Entrar a Streamate' si aparece
  const mainTarget = targets.find(t => t.type === 'page' && t.url.includes('renderer/index.html'));
  if (mainTarget) {{
    const wsMain = new WebSocket(mainTarget.webSocketDebuggerUrl);
    await new Promise(res => {{
      wsMain.addEventListener('open', async () => {{
        let msgId = 1;
        const send = (m, p = {{}}) => new Promise(r => {{
          const id = msgId++;
          const h = (evt) => {{ const msg = JSON.parse(evt.data); if (msg.id === id) {{ wsMain.removeEventListener('message', h); r(msg); }} }};
          wsMain.addEventListener('message', h);
          wsMain.send(JSON.stringify({{ id, method: m, params: p }}));
        }});

        await send('Runtime.evaluate', {{
          expression: `(() => {{
            const btn = document.querySelector('button[aria-label="Streamate"]');
            if (btn) btn.click();
          }})()`
        }});
        await new Promise(r => setTimeout(r, 400));

        await send('Runtime.evaluate', {{
          expression: `(() => {{
            const btn = Array.from(document.querySelectorAll('button')).find(b => (b.innerText || '').includes('Entrar a Streamate'));
            if (btn) btn.click();
          }})()`
        }});

        wsMain.close();
        res();
      }});
    }});
    await new Promise(r => setTimeout(r, 1500));
  }}

  // 2. Conectar a la vista de Streamate
  targets = await getTargets();
  const smTarget = targets.find(t => t.url.includes('streamatemodels.com') || t.title.includes('SMConnect'));
  if (!smTarget) {{
    console.log(JSON.stringify({{ success: false, error: 'No se encontró la vista de Streamate en StreamMonitor' }}));
    process.exit(1);
  }}

  const ws = new WebSocket(smTarget.webSocketDebuggerUrl);
  ws.addEventListener('open', async () => {{
    let msgId = 1;
    const send = (m, p = {{}}) => new Promise(r => {{
      const id = msgId++;
      const h = (evt) => {{ const msg = JSON.parse(evt.data); if (msg.id === id) {{ ws.removeEventListener('message', h); r(msg); }} }};
      ws.addEventListener('message', h);
      ws.send(JSON.stringify({{ id, method: m, params: p }}));
    }});

    // A. Si está en /login, llenar credenciales
    const info = await send('Runtime.evaluate', {{ expression: `window.location.href`, returnByValue: true }});
    const curUrl = info?.result?.result?.value || '';

    if (curUrl.includes('/login')) {{
      await send('Runtime.evaluate', {{
        expression: `(() => {{
          const userInp = document.querySelector('input[name="username"], input[name="email"], input[type="email"], #username');
          const passInp = document.querySelector('input[name="password"], input[type="password"], #password');
          if (userInp) {{
            const s1 = Object.getOwnPropertyDescriptor(window.HTMLInputElement.prototype, 'value').set;
            s1.call(userInp, ${{JSON.stringify(USERNAME)}});
            userInp.dispatchEvent(new Event('input', {{ bubbles: true }}));
            userInp.dispatchEvent(new Event('change', {{ bubbles: true }}));
          }}
          if (passInp) {{
            const s2 = Object.getOwnPropertyDescriptor(window.HTMLInputElement.prototype, 'value').set;
            s2.call(passInp, ${{JSON.stringify(PASSWORD)}});
            passInp.dispatchEvent(new Event('input', {{ bubbles: true }}));
            passInp.dispatchEvent(new Event('change', {{ bubbles: true }}));
          }}
          const submitBtn = document.querySelector('button[type="submit"], input[type="submit"]') || Array.from(document.querySelectorAll('button')).find(b => (b.innerText || '').toLowerCase().includes('login') || (b.innerText || '').toLowerCase().includes('entrar'));
          if (submitBtn) submitBtn.click();
        }})()`
      }});
      await new Promise(r => setTimeout(r, 3500));
    }}

    // B. Si está en dashboard-creator, hacer clic en 'Stream'
    await send('Runtime.evaluate', {{
      expression: `(() => {{
        if (window.location.href.includes('dashboard-creator')) {{
          const streamBtn = Array.from(document.querySelectorAll('button, a')).find(b => (b.innerText || '').trim().toLowerCase() === 'stream');
          if (streamBtn) streamBtn.click();
        }}
      }})()`
    }});
    await new Promise(r => setTimeout(r, 2000));

    // C. Inyectar Topic en SMConnect
    if (topic) {{
      await send('Runtime.evaluate', {{
        expression: `(() => {{
          const btn = Array.from(document.querySelectorAll('button, a')).find(b => (b.innerText || '').includes('Tema de sala'));
          if (btn) btn.click();
        }})()`
      }});
      await new Promise(r => setTimeout(r, 600));

      await send('Runtime.evaluate', {{
        expression: `(() => {{
          const ta = document.querySelector('textarea[placeholder*="Tema de sala"]') || document.querySelector('textarea');
          if (ta) {{
            const setter = Object.getOwnPropertyDescriptor(window.HTMLTextAreaElement.prototype, "value").set;
            setter.call(ta, ${{JSON.stringify(topic)}});
            ta.dispatchEvent(new Event('input', {{ bubbles: true }}));
            ta.dispatchEvent(new Event('change', {{ bubbles: true }}));
          }}
          const saveBtn = Array.from(document.querySelectorAll('button')).find(b => (b.innerText || '').trim() === 'Salvar');
          if (saveBtn) saveBtn.click();
        }})()`
      }});
      await new Promise(r => setTimeout(r, 600));
    }}

    // D. Inyectar Menú Gold en Ajustes
    if (goldMenu && goldMenu.length > 0) {{
      await send('Runtime.evaluate', {{
        expression: `(() => {{
          const ajustesBtn = Array.from(document.querySelectorAll('button, a')).find(b => (b.innerText || '').trim() === 'Ajustes');
          if (ajustesBtn) ajustesBtn.click();
        }})()`
      }});
      await new Promise(r => setTimeout(r, 600));

      await send('Runtime.evaluate', {{
        expression: `(() => {{
          const goldBtn = Array.from(document.querySelectorAll('button')).find(b => (b.innerText || '').trim() === 'GOLD Menu');
          if (goldBtn) goldBtn.click();
        }})()`
      }});
      await new Promise(r => setTimeout(r, 600));

      const itemIds = goldMenu.map(it => getOptionId(it.name || it));
      await send('Runtime.evaluate', {{
        expression: `(() => {{
          const selects = Array.from(document.querySelectorAll('select'));
          const targetIds = ${{JSON.stringify(itemIds)}};
          targetIds.forEach((tid, idx) => {{
            if (selects[idx]) {{
              selects[idx].value = tid;
              selects[idx].dispatchEvent(new Event('change', {{ bubbles: true }}));
            }}
            const inp = document.querySelector('input[name="goldInput' + idx + '"]');
            if (inp) {{
              inp.value = "3";
              inp.dispatchEvent(new Event('input', {{ bubbles: true }}));
              inp.dispatchEvent(new Event('change', {{ bubbles: true }}));
            }}
          }});
          const saveBtn = Array.from(document.querySelectorAll('button')).find(b => (b.innerText || '').trim() === 'Salvar');
          if (saveBtn) saveBtn.click();
        }})()`
      }});
      await new Promise(r => setTimeout(r, 800));

      await send('Runtime.evaluate', {{
        expression: `(() => {{
          const closeBtn = document.querySelector('button[aria-label="close"]');
          if (closeBtn) closeBtn.click();
        }})()`
      }});
    }}

    console.log(JSON.stringify({{ success: true, message: '¡Sesión iniciada y estrategia inyectada en la transmisión de StreamMonitor!' }}));
    ws.close();
    process.exit(0);
  }});
}}

run().catch(err => {{
  console.log(JSON.stringify({{ success: false, error: err.message }}));
  process.exit(1);
}});
"""

    temp_runner = Path(__file__).resolve().parent.parent.parent.parent / "scratch" / "run_smconnect_injection.js"
    temp_runner.parent.mkdir(parents=True, exist_ok=True)
    with open(temp_runner, "w", encoding="utf-8") as f:
        f.write(js_runner)

    try:
        res = subprocess.run([NODE_PATH, str(temp_runner)], capture_output=True, encoding="utf-8", errors="replace", timeout=20)
        out = (res.stdout or "").strip()
        if out:
            try:
                return json.loads(out)
            except Exception:
                pass
        return {"success": False, "error": res.stderr or out or "Sin respuesta del inyector SMConnect"}
    except Exception as e:
        return {"success": False, "error": str(e)}
