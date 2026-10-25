"""
SIREN AI — Túnel Remoto Seguro (Cloudflare Tunnel)
Conecta tu PC de casa con el estudio de transmisión de forma cifrada (HTTPS).
"""
import os
import sys
import time
import re
import urllib.request
import subprocess
import threading
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

PORT = 8888
BIN_PATH = ROOT / "bin" / "cloudflared.exe"
TXT_OUT = ROOT / "ENLACE_SIREN_ESTUDIO.txt"

import socket

def is_server_running() -> bool:
    """Verifica si el servidor SIREN en el puerto 8888 está activo."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(0.5)
        return s.connect_ex(('127.0.0.1', PORT)) == 0

def start_local_server_thread():
    """Inicia el servidor SIREN si no está activo."""
    if not is_server_running():
        print("⚡ Servidor local no detectado en el puerto 8888. Iniciando servidor en segundo plano...", flush=True)
        from src.server.velvet_app_server import run_server
        server_thread = threading.Thread(target=run_server, daemon=True)
        server_thread.start()
        # Esperar a que responda
        for _ in range(15):
            time.sleep(0.3)
            if is_server_running():
                print("✓ Servidor local en línea en http://localhost:8888", flush=True)
                break
    else:
        print("✓ Servidor local ya está activo en http://localhost:8888", flush=True)

def copy_to_clipboard(text: str):
    """Copia el enlace al portapapeles de Windows."""
    if sys.platform == "win32":
        try:
            cmd = f'Set-Clipboard -Value "{text}"'
            subprocess.run(["powershell", "-NoProfile", "-Command", cmd], capture_output=True, timeout=3)
        except Exception:
            pass

def run_tunnel():
    if not BIN_PATH.exists():
        print(f"❌ Error: No se encontró el binario en {BIN_PATH}", flush=True)
        sys.exit(1)

    start_local_server_thread()

    print("\n🌐 Conectando Túnel Seguro con Cloudflare...", flush=True)
    cmd = [str(BIN_PATH), "tunnel", "--url", f"http://localhost:{PORT}"]

    proc = subprocess.Popen(
        cmd,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.PIPE,
        text=True,
        encoding="utf-8",
        errors="replace"
    )

    tunnel_url = None
    buffer = ""
    start_time = time.time()

    # Lectura carácter por carácter sin bloqueo de búfer
    while proc.poll() is None:
        char = proc.stderr.read(1)
        if not char:
            time.sleep(0.05)
            continue
        buffer += char
        m = re.search(r"https://[a-zA-Z0-9-]+\.trycloudflare\.com", buffer)
        if m:
            tunnel_url = m.group(0)
            break
        if time.time() - start_time > 25:
            print("⚠️ Tiempo de espera agotado buscando la URL del túnel.", flush=True)
            break

    if not tunnel_url:
        print("❌ No se pudo obtener la URL pública de Cloudflare.", flush=True)
        proc.terminate()
        sys.exit(1)

    # Guardar en archivo de texto para fácil acceso
    try:
        TXT_OUT.write_text(tunnel_url.strip(), encoding="utf-8")
    except Exception as e:
        print(f"Nota guardando TXT: {e}", flush=True)

    copy_to_clipboard(tunnel_url.strip())

    print("\n" + "=" * 76, flush=True)
    print("✨ SIREN AI — CONEXIÓN REMOTA ACTIVA PARA EL ESTUDIO", flush=True)
    print("=" * 76, flush=True)
    print(f"\n🔗 TU ENLACE PÚBLICO SEGURO:", flush=True)
    print(f"   👉  {tunnel_url}\n", flush=True)
    print(f"📋 ¡El enlace ha sido COPIADO a tu portapapeles automáticamente!", flush=True)
    print(f"📁 También quedó guardado en el archivo del escritorio / carpeta:", flush=True)
    print(f"   {TXT_OUT.name}\n", flush=True)
    print("💡 INSTRUCCIONES PARA TU TURNO EN EL ESTUDIO:", flush=True)
    print("   1. Deja este PC de casa ENCENDIDO con esta ventana abierta.", flush=True)
    print("   2. En el estudio (o desde tu celular), entra a ese enlace en Google Chrome.", flush=True)
    print("   3. Tendrás acceso total a Roxanne, la IA Qwen 2.5 y las herramientas de Streamate.", flush=True)
    print("=" * 76, flush=True)
    print("\n(El túnel y el servidor permanecerán activos mientras dejes esta ventana abierta)", flush=True)
    print("(Presiona Ctrl + C en cualquier momento para desconectar)\n", flush=True)

    try:
        proc.wait()
    except KeyboardInterrupt:
        print("\nCerrando túnel seguro...", flush=True)
        proc.terminate()
        proc.wait(timeout=3)
        print("✓ Túnel cerrado correctamente.", flush=True)

if __name__ == "__main__":
    run_tunnel()
