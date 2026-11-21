"""
SIREN AI — Inyector y Autenticador en Vivo para la Transmisión de Streamate dentro de StreamMonitor.
Flujo de automatización completo y resiliente:
1. Activa la pestaña 'Streamate' en StreamMonitor.
2. Si aparece el botón 'Entrar a Streamate' (Listo para transmitir), le hace clic automáticamente.
3. Máquina de estados con polling (hasta 45s):
   - Si está en /login: llena credenciales (EFAC05@YOPMAIL.COM / Centenario123@) y envía.
   - Si está en dashboard-creator: pulsa el botón 'Stream' para abrir la consola de transmisión.
   - Si llega a performerclient (SMConnect): inyecta Room Topic y Menú Gold (3G), salvando ambos.
4. Deja la vista de transmisión activa y lista para transmitir en pantalla física.
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
  const norm = (s) => (s || '').toLowerCase().normalize("NFD").replace(/[\\u0300-\\u036f]/g, "").trim();
  const target = norm(name);
  for (const [id, val] of Object.entries(DEFAULT_OPTIONS)) {{
    if (norm(val) === target || target.includes(norm(val)) || norm(val).includes(target)) {{
      return id;
    }}
  }}
  return "0";
}}

const sleep = ms => new Promise(r => setTimeout(r, ms));

const getTargets = () => new Promise((res, rej) => http.get('http://127.0.0.1:' + port + '/json', r => {{
  let d = ''; r.on('data', c => d += c); r.on('end', () => {{ try {{ res(JSON.parse(d)); }} catch(e) {{ rej(e); }} }});
}}).on('error', rej));

async function sendCDP(wsUrl, method, params = {{}}) {{
  return new Promise((res, rej) => {{
    const ws = new WebSocket(wsUrl);
    ws.addEventListener('open', () => {{
      ws.send(JSON.stringify({{ id: 1, method, params }}));
    }});
    ws.addEventListener('message', m => {{
      try {{
        const data = JSON.parse(m.data);
        ws.close();
        res(data.result);
      }} catch(e) {{ ws.close(); rej(e); }}
    }});
    ws.addEventListener('error', err => {{ ws.close(); rej(err); }});
  }});
}}

async function evalInPage(wsUrl, expr) {{
  try {{
    const r = await sendCDP(wsUrl, 'Runtime.evaluate', {{ expression: expr, returnByValue: true }});
    return r?.result?.value;
  }} catch(e) {{
    return null;
  }}
}}

async function clickEntrarAStreamateIfPresent(rendererTarget) {{
  if (!rendererTarget) return;
  await evalInPage(rendererTarget.webSocketDebuggerUrl, `(() => {{
    const closeBtn = document.querySelector('button[aria-label=Cerrar]');
    if (closeBtn) closeBtn.click();
    const tabBtn = document.querySelector('button[aria-label=Streamate]');
    if (tabBtn) tabBtn.click();
    const enterBtn = Array.from(document.querySelectorAll('button, a, div[role=button]')).find(b => (b.innerText || '').includes('Entrar a Streamate'));
    if (enterBtn) enterBtn.click();
  }})()`);
}}

async function run() {{
  let targets = await getTargets();
  const mainTarget = targets.find(t => t.type === 'page' && t.url.includes('renderer/index.html'));
  if (mainTarget) {{
    await clickEntrarAStreamateIfPresent(mainTarget);
    await sleep(1500);
  }}

  const startTime = Date.now();
  const MAX_WAIT_MS = 45000;

  while (Date.now() - startTime < MAX_WAIT_MS) {{
    targets = await getTargets();
    const smTarget = targets.find(t => t.url.includes('performerclient') || t.url.includes('streamatemodels.com') || t.url.includes('streamatelinx') || t.title.includes('SMConnect'));

    if (!smTarget) {{
      if (mainTarget) await clickEntrarAStreamateIfPresent(mainTarget);
      await sleep(1200);
      continue;
    }}

    const curUrl = await evalInPage(smTarget.webSocketDebuggerUrl, `window.location.href`) || smTarget.url;

    // CASO 1: Pantalla de Login (/login)
    if (curUrl.includes('/login') || curUrl.includes('/signin')) {{
      await evalInPage(smTarget.webSocketDebuggerUrl, `(() => {{
        const userInp = document.querySelector('input[name="username"], input[name="email"], input[type="email"], #username, #email');
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
      }})()`);
      await sleep(2500);
      continue;
    }}

    // CASO 2: Dashboard Creator (pulsar botón Stream)
    if (curUrl.includes('dashboard-creator') || curUrl.includes('streamatelinx') || (curUrl.includes('streamatemodels.com') && !curUrl.includes('performerclient'))) {{
      const clicked = await evalInPage(smTarget.webSocketDebuggerUrl, `(() => {{
        const btn = Array.from(document.querySelectorAll('button, a')).find(b => {{
          const t = (b.innerText || '').trim().toLowerCase();
          return t === 'stream' || t.startsWith('stream');
        }});
        if (btn) {{
          btn.click();
          return true;
        }}
        return false;
      }})()`);
      await sleep(2500);
      continue;
    }}

    // CASO 3: Consola de Transmisión en Vivo (performerclient.streamatemodels.com/client)
    if (curUrl.includes('performerclient') || smTarget.title.includes('SMConnect')) {{
      // Verificar si los botones principales ya se renderizaron
      const isReady = await evalInPage(smTarget.webSocketDebuggerUrl, `(() => {{
        return Array.from(document.querySelectorAll('button')).some(b => (b.innerText || '').includes('Tema de sala') || (b.innerText || '').includes('Ajustes'));
      }})()`);

      if (!isReady) {{
        await sleep(1000);
        continue;
      }}

      // A. Inyectar Room Topic
      if (topic) {{
        await evalInPage(smTarget.webSocketDebuggerUrl, `(() => {{
          const btn = Array.from(document.querySelectorAll('button, a')).find(b => (b.innerText || '').includes('Tema de sala'));
          if (btn) btn.click();
        }})()`);
        await sleep(600);

        await evalInPage(smTarget.webSocketDebuggerUrl, `(() => {{
          const ta = document.querySelector('textarea[placeholder*="Tema de sala"]') || document.querySelector('textarea');
          if (ta) {{
            const setter = Object.getOwnPropertyDescriptor(window.HTMLTextAreaElement.prototype, "value").set;
            setter.call(ta, ${{JSON.stringify(topic)}});
            ta.dispatchEvent(new Event('input', {{ bubbles: true }}));
            ta.dispatchEvent(new Event('change', {{ bubbles: true }}));
          }}
          const saveBtn = Array.from(document.querySelectorAll('button')).find(b => (b.innerText || '').trim() === 'Salvar');
          if (saveBtn) saveBtn.click();
        }})()`);
        await sleep(600);
      }}

      // B. Inyectar Menú Gold en Ajustes
      if (goldMenu && goldMenu.length > 0) {{
        await evalInPage(smTarget.webSocketDebuggerUrl, `(() => {{
          const ajustesBtn = Array.from(document.querySelectorAll('button, a')).find(b => (b.innerText || '').trim() === 'Ajustes');
          if (ajustesBtn) ajustesBtn.click();
        }})()`);
        await sleep(600);

        await evalInPage(smTarget.webSocketDebuggerUrl, `(() => {{
          const goldBtn = Array.from(document.querySelectorAll('button')).find(b => (b.innerText || '').trim() === 'GOLD Menu');
          if (goldBtn) goldBtn.click();
        }})()`);
        await sleep(600);

        const itemIds = goldMenu.map(it => getOptionId(it.name || it));
        await evalInPage(smTarget.webSocketDebuggerUrl, `(() => {{
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
        }})()`);
        await sleep(600);

        await evalInPage(smTarget.webSocketDebuggerUrl, `(() => {{
          const closeBtn = document.querySelector('button[aria-label="close"]');
          if (closeBtn) closeBtn.click();
        }})()`);
      }}

      console.log(JSON.stringify({{ success: true, message: '¡Listo para transmitir! Sesión en vivo configurada en SMConnect.' }}));
      process.exit(0);
    }}

    await sleep(1000);
  }}

  console.log(JSON.stringify({{ success: false, error: 'Tiempo de espera agotado navegando a la consola de transmisión' }}));
  process.exit(1);
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
        res = subprocess.run([NODE_PATH, str(temp_runner)], capture_output=True, encoding="utf-8", errors="replace", timeout=50)
        out = (res.stdout or "").strip()
        if out:
            try:
                return json.loads(out)
            except Exception:
                pass
        return {"success": False, "error": res.stderr or out or "Sin respuesta del inyector SMConnect"}
    except Exception as e:
        return {"success": False, "error": str(e)}
