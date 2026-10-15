"""
VELVET AI — Asistente de Inicio de Sesión Asistido (Human-in-the-Loop)
Permite resolver retos de Cloudflare Turnstile, 2FA y validaciones iniciales
en Stripchat, LoyalFans o Flirt4Free, guardando de forma permanente la sesión
y las cookies de autorización en el perfil del navegador de VELVET AI.
"""

import sys
import os
import asyncio
import argparse
from pathlib import Path
from playwright.async_api import async_playwright

ROOT_DIR = Path(__file__).resolve().parent.parent.parent
sys.path.append(str(ROOT_DIR))

from src.config import DATA_DIR
from src.automation.broadcast_manager import get_webrtc_media_hook_script, setup_live_broadcast_room
from src.automation.platform_auth import (
    PLATFORM_CONFIG,
    PLATFORM_DESTINATIONS,
    PROFILES_DIR,
    clean_profile_crash_state,
    is_user_logged_in,
    handle_cookies_and_age_dialogs,
    wait_for_cloudflare_resolution
)

async def run_assisted_login(platform_key: str, redirect_target: str = "feed"):
    platform_key = platform_key.lower().strip()
    if platform_key not in PLATFORM_CONFIG:
        print(f"❌ Plataforma desconocida: '{platform_key}'. Opciones: {list(PLATFORM_CONFIG.keys())}")
        return False

    cfg = PLATFORM_CONFIG[platform_key]
    user_data_dir = PROFILES_DIR / f"{platform_key}_profile"
    user_data_dir.mkdir(parents=True, exist_ok=True)
    clean_profile_crash_state(user_data_dir)

    print("\n" + "="*70)
    print(f"  🔐 VELVET AI — INICIO DE SESIÓN ASISTIDO & RESOLUCIÓN CLOUDFLARE")
    print(f"  🌐 Plataforma: {cfg['name']}")
    print(f"  📁 Perfil persistente: {user_data_dir}")
    print("="*70)
    print("👉 Pasos a seguir:")
    print(" 1. Se abrirá una ventana de Chrome con protección anti-detección.")
    print(" 2. Si aparece la casilla de Cloudflare Turnstile ('Verifica que eres humano'), márcala.")
    print(" 3. Ingresa tu usuario y contraseña (o código 2FA si aplica).")
    print(" 4. Una vez dentro de tu cuenta, el sistema guardará la sesión automáticamente.")
    print("="*70 + "\n")

    playwright = await async_playwright().start()
    context = await playwright.chromium.launch_persistent_context(
        user_data_dir=str(user_data_dir),
        headless=False,
        no_viewport=True,
        permissions=["camera", "microphone"],
        ignore_default_args=["--enable-automation"],
        args=[
            "--start-maximized",
            "--disable-blink-features=AutomationControlled",
            "--disable-session-crashed-bubble",
            "--hide-crash-restore-bubble",
            "--no-first-run",
            "--no-default-browser-check",
            "--disable-infobars",
            "--use-fake-ui-for-media-stream",
            "--lang=es-ES,es,en-US,en"
        ]
    )

    # Inyección de stealth scripts
    await context.add_init_script("""
        Object.defineProperty(navigator, 'webdriver', { get: () => undefined });
        window.chrome = window.chrome || { runtime: {}, app: {}, csi: () => {}, loadTimes: () => {} };
        Object.defineProperty(navigator, 'plugins', { get: () => [1, 2, 3, 4, 5] });
        Object.defineProperty(navigator, 'languages', { get: () => ['es-ES', 'es', 'en-US', 'en'] });
    """)

    # Inyección de hook WebRTC para priorizar OBS Virtual Camera y Micrófono Logitech
    await context.add_init_script(get_webrtc_media_hook_script())

    page = context.pages[0] if context.pages else await context.new_page()

    print(f"⏳ Navegando a {cfg['name']} ({cfg['login_url']})...")
    await page.goto(cfg["login_url"], wait_until="domcontentloaded", timeout=60000)

    # Monitorear Cloudflare y cookies iniciales
    await wait_for_cloudflare_resolution(page, print, timeout_seconds=45)
    await handle_cookies_and_age_dialogs(page, print)

    # Verificar si ya está logueado
    if await is_user_logged_in(page, cfg):
        print(f"\n🎉 ¡SESIÓN PREVIAMENTE ACTIVA DETECTADA EN {cfg['name'].upper()}!")
        print("Tu perfil ya tiene las cookies y credenciales vigentes.")
    else:
        print("\n⏳ Esperando a que completes el inicio de sesión en el navegador...")
        print("(Monitoreando estado cada 2 segundos. Puedes tomarte el tiempo que necesites)")

        logged_in = False
        for _ in range(120):  # Hasta 4 minutos de espera
            await asyncio.sleep(2)
            try:
                if page.is_closed():
                    print("⚠️ Ventana cerrada por el usuario.")
                    break
                
                # Manejar Cloudflare si salta durante el login
                await wait_for_cloudflare_resolution(page, print, timeout_seconds=5)

                if await is_user_logged_in(page, cfg):
                    logged_in = True
                    break
            except Exception:
                pass

        if logged_in:
            print("\n" + "*"*70)
            print(f"  ✨ ¡ACCESO CONFIRMADO EXITOSAMENTE EN {cfg['name'].upper()}!")
            print(f"  💾 Todas las cookies de autorización y 'cf_clearance' han sido guardadas.")
            print(f"  🚀 A partir de ahora, VELVET AI podrá operar automáticamente sin bloqueos.")
            print("*"*70 + "\n")
        else:
            print("\n⚠️ No se confirmó el login en el tiempo límite, pero los datos introducidos se preservan en el perfil.")

    # Redirección automática al destino seleccionado si está logueado
    if (await is_user_logged_in(page, cfg)) and redirect_target and redirect_target.lower() != "home":
        target_key = redirect_target.lower().strip()
        dest_url = PLATFORM_DESTINATIONS.get(platform_key, {}).get(target_key)
        if dest_url:
            target_label = "Muro / Feed" if target_key == "feed" else ("Transmisión en Vivo" if target_key == "live" else target_key)
            print(f"🎯 Redireccionando automáticamente a [{target_label.upper()}]: {dest_url}...")
            try:
                await page.goto(dest_url, wait_until="domcontentloaded", timeout=30000)
                print(f"✨ ¡Redirección completada! Ahora estás en tu {target_label}.")

                # Si el destino es la Transmisión en Vivo, configurar OBS, micrófono Logitech, meta del día y tema @SAMBARTONN23
                if target_key == "live":
                    await asyncio.sleep(2)
                    await setup_live_broadcast_room(page, platform_key, print)
            except Exception as e:
                print(f"Nota en redirección / setup de transmisión: {e}")

    # Guardar estado de almacenamiento explícito
    storage_file = DATA_DIR / "sessions" / f"{platform_key}_storage_state.json"
    storage_file.parent.mkdir(parents=True, exist_ok=True)
    try:
        await context.storage_state(path=str(storage_file))
        print(f"💾 Snapshot de sesión exportado en: {storage_file.name}")
    except Exception as e:
        print(f"Nota en guardado de snapshot: {e}")

    input("\nPresiona ENTER cuando desees cerrar el navegador asistido...")
    await context.close()
    await playwright.stop()
    print("✓ Navegador cerrado. Perfil listo para su uso en VELVET AI.")
    return True

def main():
    parser = argparse.ArgumentParser(description="Asistente de login y superación de Cloudflare para VELVET AI")
    parser.add_argument("--platform", default="stripchat", choices=["stripchat", "loyalfans", "flirt4free", "streamate"], help="Plataforma a iniciar")
    parser.add_argument("--redirect", default="feed", choices=["feed", "live", "home"], help="Destino post-login (feed, live, home)")
    args = parser.parse_args()

    asyncio.run(run_assisted_login(args.platform, redirect_target=args.redirect))

if __name__ == "__main__":
    main()
