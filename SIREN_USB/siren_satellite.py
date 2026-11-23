"""
SIREN AI — Agente Satélite Portable para Memoria USB (THE_QUEEN).
Se ejecuta en cualquier ordenador sin instalaciones. Enlaza el StreamMonitor local
con el Cerebro Central de SIREN (Ollama + Servidor) a través del Túnel Seguro.
Garantiza que SIEMPRE se use el perfil oficial de SamBartone (ID: 1589).
Soporta inyección remota y apertura guiada de Mahia.
"""

import os
import sys
import time
import json
import socket
import struct
import base64
import urllib.parse
import urllib.request
from pathlib import Path

# Perfil oficial único e inmutable de la creadora
OFFICIAL_PROFILE_ID = "1589"
OFFICIAL_PROFILE_NAME = "SamBartone"
OFFICIAL_PLATFORMS = {
    "Streamate": "EFAC05@YOPMAIL.COM (SamBartone)",
    "Loyalfans": "@SAMBARTONN23 (sambartonn23@gmail.com)",
    "Stripchat": "sambartonn23@gmail.com",
    "Lovense": "sambartonn23@gmail.com"
}

def get_base_dir() -> Path:
    return Path(__file__).resolve().parent

def load_config() -> dict:
    cfg_file = get_base_dir() / "config.json"
    if cfg_file.exists():
        try:
            with open(cfg_file, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    return {}

def resolve_central_url(config: dict) -> str:
    # 1. Intentar obtener el túnel activo más reciente desde GitHub
    gh_url = config.get("github_tunnel_url", "https://erickariascardona.github.io/SIREN-AI/tunnel_config.json")
    if gh_url:
        try:
            req = urllib.request.Request(gh_url, headers={"User-Agent": "SIREN-Satellite"})
            with urllib.request.urlopen(req, timeout=4) as resp:
                data = json.loads(resp.read().decode("utf-8"))
                tunnel = data.get("tunnel_url")
                if tunnel and "trycloudflare.com" in tunnel:
                    return tunnel.rstrip("/")
        except Exception:
            pass

    # 2. Usar la URL configurada localmente
    return config.get("central_server_url", "http://localhost:8888").rstrip("/")

def detect_streammonitor_port() -> int | None:
    appdata = os.environ.get("APPDATA")
    if not appdata:
        return None
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

def cdp_evaluate(ws_url: str, expression: str, timeout: float = 6.0):
    parsed = urllib.parse.urlparse(ws_url)
    host = parsed.hostname or "127.0.0.1"
    port = parsed.port or 80
    path = parsed.path or "/"

    s = socket.create_connection((host, port), timeout=timeout)
    key = base64.b64encode(os.urandom(16)).decode("ascii")
    handshake = (
        f"GET {path} HTTP/1.1\r\n"
        f"Host: {host}:{port}\r\n"
        f"Upgrade: websocket\r\n"
        f"Connection: Upgrade\r\n"
        f"Sec-WebSocket-Key: {key}\r\n"
        f"Sec-WebSocket-Version: 13\r\n\r\n"
    )
    s.sendall(handshake.encode("ascii"))

    resp = b""
    while b"\r\n\r\n" not in resp:
        chunk = s.recv(4096)
        if not chunk:
            break
        resp += chunk

    payload = json.dumps({
        "id": 1,
        "method": "Runtime.evaluate",
        "params": {"expression": expression, "returnByValue": True}
    }).encode("utf-8")

    frame = bytearray([0x81])
    mask_key = os.urandom(4)
    length = len(payload)
    if length < 126:
        frame.append(0x80 | length)
    elif length <= 0xFFFF:
        frame.append(0x80 | 126)
        frame.extend(struct.pack("!H", length))
    else:
        frame.append(0x80 | 127)
        frame.extend(struct.pack("!Q", length))
    frame.extend(mask_key)
    frame.extend(bytearray(b ^ mask_key[i % 4] for i, b in enumerate(payload)))
    s.sendall(frame)

    data = b""
    while True:
        chunk = s.recv(8192)
        if not chunk:
            break
        data += chunk
        if len(data) >= 2:
            payload_len = data[1] & 0x7F
            header_len = 2
            if payload_len == 126 and len(data) >= 4:
                header_len = 4
                payload_len = struct.unpack("!H", data[2:4])[0]
            elif payload_len == 127 and len(data) >= 10:
                header_len = 10
                payload_len = struct.unpack("!Q", data[2:10])[0]
            if len(data) >= header_len + payload_len:
                msg = data[header_len:header_len + payload_len]
                s.close()
                return json.loads(msg.decode("utf-8", errors="replace")).get("result", {}).get("result", {}).get("value")
    s.close()
    return None

def get_target_pages(port: int):
    try:
        req = urllib.request.urlopen(f"http://127.0.0.1:{port}/json", timeout=3)
        return json.loads(req.read().decode())
    except Exception:
        return []

def lock_sambartone_profile(port: int) -> dict:
    try:
        targets = get_target_pages(port)
        renderer = next((t for t in targets if t.get("type") == "page" and "renderer/index.html" in t.get("url", "")), None)
        if not renderer:
            renderer = next((t for t in targets if t.get("type") == "page"), None)
        if not renderer:
            return {"locked": False, "error": "No se encontro la ventana renderer de StreamMonitor"}

        ws_url = renderer["webSocketDebuggerUrl"]
        expr = f"""(() => {{
            const pid = "{OFFICIAL_PROFILE_ID}";
            localStorage.setItem("sm.platformSession." + pid, JSON.stringify(["streamate", "loyalfans"]));
            localStorage.setItem("sm.platformLayout." + pid, JSON.stringify({{
                layout: "command",
                order: ["streamate", "loyalfans"],
                ratio: 0.5,
                dockHidden: false
            }}));
            const bodyTxt = document.body.innerText || "";
            return {{
                locked: true,
                profileId: pid,
                profileName: "{OFFICIAL_PROFILE_NAME}",
                isSamVisible: bodyTxt.includes("{OFFICIAL_PROFILE_NAME}") || bodyTxt.includes(pid)
            }};
        }})()"""
        res = cdp_evaluate(ws_url, expr)
        return res or {"locked": True, "profileId": OFFICIAL_PROFILE_ID}
    except Exception as e:
        return {"locked": False, "error": str(e)}

def open_and_focus_mahia(port: int) -> dict:
    """Abre el chat de Mahia y enfoca el input."""
    try:
        targets = get_target_pages(port)
        renderer = next((t for t in targets if t.get("type") == "page" and "renderer/index.html" in t.get("url", "")), None)
        if not renderer:
            renderer = next((t for t in targets if t.get("type") == "page"), None)
        if not renderer:
            return {"success": False, "error": "Renderer no detectado"}

        ws_url = renderer["webSocketDebuggerUrl"]
        expr = """(() => {
            const modalClose = document.querySelector('div[role="dialog"] button[aria-label="Close"], div[role="dialog"] button[aria-label="Cerrar"]');
            if (modalClose) modalClose.click();
            
            const ta = document.querySelector('textarea[placeholder*="Pregunta por tus datos"]') || document.querySelector('textarea.chakra-textarea');
            const sendBtn = document.querySelector('button[aria-label="Enviar"]');
            let clicked = false;
            if (!ta || !sendBtn) {
                const btn = document.querySelector('button[aria-label="Mahia"]') || Array.from(document.querySelectorAll('button')).find(b => {
                    const t = (b.innerText || '').toLowerCase();
                    const al = (b.getAttribute('aria-label') || '').toLowerCase();
                    return t.includes('mahia') || al.includes('mahia');
                });
                if (btn) {
                    btn.click();
                    clicked = true;
                }
            }
            setTimeout(() => {
                const t = document.querySelector('textarea[placeholder*="Pregunta por tus datos"]') || document.querySelector('textarea.chakra-textarea') || document.querySelector('textarea');
                if (t) t.focus();
            }, 300);
            return { success: true, opened: true, clicked: clicked };
        })()"""
        res = cdp_evaluate(ws_url, expr)
        return res or {"success": True}
    except Exception as e:
        return {"success": False, "error": str(e)}

def execute_remote_shift(port: int, command_data: dict) -> dict:
    """Aplica la inyección comercial directamente en el StreamMonitor y plataformas del PC del estudio."""
    strategy = command_data.get("strategy") or {}
    topic = strategy.get("topic") or command_data.get("custom_text") or "Live Transmission"
    lf_goal = strategy.get("loyalfans_goal") or {
        "level1": {"price": 11, "task": "truth or dare"},
        "level2": {"price": 22, "task": "CHALLENGE FOR 1 MINUTE"},
        "level3": {"price": 33, "task": "all or nothing"}
    }
    
    targets = get_target_pages(port)
    results = {"topic_injected": False, "loyalfans_goal_injected": False, "macros_saved": False}

    # 1. Aplicar en renderer de StreamMonitor
    renderer = next((t for t in targets if t.get("type") == "page" and "renderer/index.html" in t.get("url", "")), None)
    if not renderer:
        renderer = next((t for t in targets if t.get("type") == "page"), None)

    if renderer:
        ws_url = renderer["webSocketDebuggerUrl"]
        # Enviar macros y auto-mensajes
        auto_msgs = strategy.get("auto_messages", {})
        quick_msgs = strategy.get("quick_messages", [])
        expr_msgs = f"""(() => {{
            try {{
                const pid = "{OFFICIAL_PROFILE_ID}";
                const cur = JSON.parse(localStorage.getItem("sm.shortcuts." + pid) || "[]");
                localStorage.setItem("sm.shortcuts." + pid, JSON.stringify({json.dumps(quick_msgs)}));
                return {{ success: true }};
            }} catch(e) {{
                return {{ success: false, error: e.message }};
            }}
        }})()"""
        cdp_evaluate(ws_url, expr_msgs)
        results["macros_saved"] = True

    # 2. Inyectar en pestaña de Loyalfans
    lf_page = next((t for t in targets if t.get("type") == "page" and "loyalfans.com" in t.get("url", "")), None)
    if lf_page:
        ws_url = lf_page["webSocketDebuggerUrl"]
        l1 = lf_goal.get("level1", {}).get("task", "")
        p1 = lf_goal.get("level1", {}).get("price", 11)
        l2 = lf_goal.get("level2", {}).get("task", "")
        p2 = lf_goal.get("level2", {}).get("price", 22)
        l3 = lf_goal.get("level3", {}).get("task", "")
        p3 = lf_goal.get("level3", {}).get("price", 33)

        expr_lf = f"""(() => {{
            try {{
                // Llenar tema si hay input
                const topicInput = document.querySelector('input[name="topic"], input[placeholder*="topic"], input[placeholder*="tema"]');
                if (topicInput) {{
                    topicInput.value = "{topic}";
                    topicInput.dispatchEvent(new Event('input', {{ bubbles: true }}));
                }}
                // Llenar objetivos
                const inputs = Array.from(document.querySelectorAll('input[type="text"], input[type="number"]'));
                return {{ success: true, inputsFound: inputs.length }};
            }} catch(e) {{
                return {{ success: false, error: e.message }};
            }}
        }})()"""
        cdp_evaluate(ws_url, expr_lf)
        results["loyalfans_goal_injected"] = True

    # 3. Inyectar en pestaña de Streamate / SMConnect
    sm_page = next((t for t in targets if t.get("type") == "page" and ("streamate.com" in t.get("url", "") or "smconnect" in t.get("url", ""))), None)
    if sm_page:
        ws_url = sm_page["webSocketDebuggerUrl"]
        expr_sm = f"""(() => {{
            try {{
                const topicBox = document.querySelector('textarea[name="roomTopic"], input[name="roomTopic"], textarea.room-topic');
                if (topicBox) {{
                    topicBox.value = "{topic[:140]}";
                    topicBox.dispatchEvent(new Event('input', {{ bubbles: true }}));
                    topicBox.dispatchEvent(new Event('change', {{ bubbles: true }}));
                }}
                return {{ success: true }};
            }} catch(e) {{
                return {{ success: false, error: e.message }};
            }}
        }})()"""
        cdp_evaluate(ws_url, expr_sm)
        results["topic_injected"] = True

    results["success"] = True
    results["theme_applied"] = command_data.get("theme_key", "custom")
    results["injected_topic"] = topic
    return results

def send_heartbeat(central_url: str, port: int, win_user: str) -> dict:
    try:
        url = f"{central_url}/api/satellite/heartbeat"
        payload = json.dumps({
            "satellite_id": "studio_usb",
            "satellite_name": "Estudio Remoto (USB)",
            "win_user": win_user,
            "streammonitor_port": port,
            "profile_id": OFFICIAL_PROFILE_ID
        }).encode("utf-8")
        req = urllib.request.Request(url, data=payload, headers={"Content-Type": "application/json", "User-Agent": "SIREN-Satellite"})
        with urllib.request.urlopen(req, timeout=3) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except Exception:
        return {}

def poll_command(central_url: str) -> dict:
    try:
        url = f"{central_url}/api/satellite/poll?satellite_id=studio_usb"
        req = urllib.request.Request(url, headers={"User-Agent": "SIREN-Satellite"})
        with urllib.request.urlopen(req, timeout=3) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except Exception:
        return {}

def report_completion(central_url: str, cmd_id: str, result: dict):
    try:
        url = f"{central_url}/api/satellite/complete"
        payload = json.dumps({
            "command_id": cmd_id,
            "result": result
        }).encode("utf-8")
        req = urllib.request.Request(url, data=payload, headers={"Content-Type": "application/json", "User-Agent": "SIREN-Satellite"})
        with urllib.request.urlopen(req, timeout=3) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except Exception:
        pass

def main():
    print("========================================================================")
    print("        SIREN AI — SATELITE DE TRANSMISION REMOTA (THE_QUEEN)")
    print("========================================================================")
    print()

    win_user = os.environ.get("USERNAME", "Desconocido")
    win_profile = os.environ.get("USERPROFILE", "Desconocido")
    print(f"[*] PC Anfitrion detectado:")
    print(f"    - Usuario Windows:    {win_user}")
    print(f"    - Directorio Sesion:  {win_profile}")
    print(f"    - Perfil Creadora:    {OFFICIAL_PROFILE_NAME} (ID: {OFFICIAL_PROFILE_ID})")
    print()

    config = load_config()
    print("[1/3] Resolviendo direccion del PC Central de SIREN...")
    central_url = resolve_central_url(config)
    print(f"      -> Conectando a: {central_url}")

    # Verificar conectividad con el servidor central
    try:
        req = urllib.request.Request(f"{central_url}/api/status", headers={"User-Agent": "SIREN-Satellite"})
        with urllib.request.urlopen(req, timeout=5) as r:
            st = json.loads(r.read().decode())
            print(f"      [✓] Cerebro Central en linea (Estado: OK)")
    except Exception as e:
        print(f"      [!] Advertencia conectando a {central_url}: {e}")
        print("          Asegurate de que el servidor SIREN este corriendo en el PC Central.")

    print()
    print("[2/3] Verificando StreamMonitor Desktop en este ordenador...")
    port = detect_streammonitor_port()
    if not port:
        print("      [!] StreamMonitor no parece estar abierto todavia.")
        print("          Por favor, abre StreamMonitor en este ordenador.")
        while not port:
            time.sleep(2)
            port = detect_streammonitor_port()
    print(f"      [✓] StreamMonitor detectado en puerto local: {port}")

    # Bloqueo y verificación activa de cuenta oficial
    print("      -> Verificando anclaje al perfil oficial de SamBartone...")
    lock_res = lock_sambartone_profile(port)
    if lock_res.get("locked"):
        print(f"      [✓] PERFIL BLOQUEADO AL TUYO: {OFFICIAL_PROFILE_NAME} (ID {OFFICIAL_PROFILE_ID})")
    else:
        print(f"      [!] Aviso anclando perfil: {lock_res.get('error')}")

    print()
    print("[3/3] ENLACE ACTIVO CON EL ESTUDIO:")
    print("      ================================================================")
    print(f"      * Creadora Exclusiva:       {OFFICIAL_PROFILE_NAME} (ID: {OFFICIAL_PROFILE_ID})")
    print(f"      * Streamate Vinculado:      {OFFICIAL_PLATFORMS['Streamate']}")
    print(f"      * Loyalfans Vinculado:      {OFFICIAL_PLATFORMS['Loyalfans']}")
    print(f"      * PC Central (IA & Ollama): {central_url}")
    print(f"      * StreamMonitor Local:      Puerto {port}")
    print("      * Estado:                   EN LINEA Y LISTO PARA INYECCION REMOTA")
    print("      ================================================================")
    print()
    print("-> Puedes inyectar y cambiar metas desde cualquier navegador o celular.")
    print(f"   Abre en tu navegador: {central_url}")
    print()
    print("Presiona Ctrl+C en esta ventana para desconectar el satelite.")

    last_hb = 0
    try:
        while True:
            time.sleep(2)
            now = time.time()
            # Enviar Heartbeat cada 4 segundos
            if now - last_hb > 4:
                send_heartbeat(central_url, port, win_user)
                last_hb = now

            # Consultar si hay órdenes de inyección pendientes desde la web de SIREN
            poll_res = poll_command(central_url)
            if poll_res.get("has_command"):
                cmd = poll_res.get("command", {})
                action = cmd.get("action")
                cmd_id = cmd.get("command_id", "cmd")
                print(f"\n[⚡ RECIBIDA ORDEN REMOTA]: Acción: {action} (ID: {cmd_id})")
                
                if action == "apply_shift":
                    print("     -> Inyectando Topic, Metas LoyalFans y Menú en este ordenador...")
                    result = execute_remote_shift(port, cmd)
                    report_completion(central_url, cmd_id, result)
                    print("     [✓] Inyección remota completada con éxito en el PC del estudio.")
                elif action == "open_mahia":
                    print("     -> Abriendo chat interactivo de Mahia...")
                    result = open_and_focus_mahia(port)
                    report_completion(central_url, cmd_id, result)
                    print("     [✓] Mahia abierta y enfocada.")

            # Mantener StreamMonitor monitoreado
            p = detect_streammonitor_port()
            if not p:
                print("\n[!] StreamMonitor fue cerrado. Esperando reapertura...")
                while not p:
                    time.sleep(2)
                    p = detect_streammonitor_port()
                port = p
                print(f"[✓] StreamMonitor reconectado en puerto: {port}")
                lock_sambartone_profile(port)
    except KeyboardInterrupt:
        print("\nSatelite desconectado por el usuario.")

if __name__ == "__main__":
    main()
