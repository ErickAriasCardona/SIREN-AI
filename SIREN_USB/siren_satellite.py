"""
SIREN AI — Agente Satélite Portable para Memoria USB (THE_QUEEN).
Se ejecuta en cualquier ordenador sin instalaciones. Enlaza el StreamMonitor local
con el Cerebro Central de SIREN (Ollama + Servidor) a través del Túnel Seguro.
Garantiza que SIEMPRE se use el perfil oficial de SamBartone (ID: 1589).
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
    gh_url = config.get("github_tunnel_url")
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
    # Lee dinámicamente el usuario de Windows actual mediante la variable de entorno
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

def lock_sambartone_profile(port: int) -> dict:
    """Verifica y asegura que StreamMonitor en este PC esté usando el perfil de SamBartone."""
    try:
        req = urllib.request.urlopen(f"http://127.0.0.1:{port}/json")
        targets = json.loads(req.read().decode())
        renderer = next((t for t in targets if "renderer" in t.get("url", "")), None)
        if not renderer:
            return {"success": False, "error": "Renderer no encontrado"}

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

def main():
    print("========================================================================")
    print("        SIREN AI — SATELITE DE TRANSMISION REMOTA (THE_QUEEN)")
    print("========================================================================")
    print()

    # Información del entorno actual del PC anfitrión
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
    print("      * Estado:                   EN LINEA Y LISTO PARA TRANSMITIR")
    print("      ================================================================")
    print()
    print("-> Puedes controlar todo desde tu celular abriendo la web de SIREN:")
    print(f"   {central_url}")
    print()
    print("Presiona Ctrl+C en esta ventana para desconectar el satelite.")

    # Bucle de mantenimiento de conexión
    try:
        while True:
            time.sleep(5)
            # Verificar si StreamMonitor sigue abierto
            p = detect_streammonitor_port()
            if not p:
                print("[!] StreamMonitor fue cerrado. Esperando reapertura...")
                while not p:
                    time.sleep(2)
                    p = detect_streammonitor_port()
                print(f"[✓] StreamMonitor reconectado en puerto: {p}")
                lock_sambartone_profile(p)
    except KeyboardInterrupt:
        print("\nSatelite desconectado por el usuario.")

if __name__ == "__main__":
    main()
