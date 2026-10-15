"""
VELVET AI — Stripchat Profile Updater
Actualiza automáticamente la biografía, arquetipo Tomboy Gamer, tags
y configuración interactiva de Lovense en Stripchat utilizando Playwright.
"""

import sys
import asyncio
from pathlib import Path
from typing import Dict, Any, List, Optional
from datetime import datetime
from playwright.async_api import async_playwright

ROOT_DIR = Path(__file__).resolve().parent.parent.parent.parent
sys.path.append(str(ROOT_DIR))

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

from src.config import ARTIFACTS_DIR, DATA_DIR
from src.automation.credential_store import load_all_credentials
from src.automation.platform_auth import (
    wait_for_cloudflare_resolution,
    handle_cookies_and_age_dialogs,
    clean_profile_crash_state,
    get_webrtc_media_hook_script
)

PROFILES_DIR = DATA_DIR / "browser_profiles"

DEFAULT_STRIPCHAT_PROFILE = {
    "display_name": "Sam Barton",
    "status_topic": "Cute Tomboy Gamer ⚡ Lovense ON • Goal: December Car 🚗💨",
    "bio_text": (
        "🐺 Sam Barton | Cute Tomboy Gamer ⚡ Lovense Interactive 🏍️\n\n"
        "Software & AI Architect by day, gaming tomboy & teasing companion by night.\n"
        "Soccer player, motorcycle enthusiast, and devoted mom to my dogs & 2 cats 🐾.\n"
        "InuYasha devotee 🍙, indie music lover & ukulele player 🎶.\n\n"
        "Obsessed with neon in the dark, skulls, and Halloween vibes 💀✨.\n"
        "Working hard every single day to buy my used car in December 🚗 and escape to Cancun 🌴!\n\n"
        "💖 LOVENSE SYNCED:\n"
        "My toys are active and connect directly to every tip! "
        "Send tokens to make me buzz, trigger reactions, or take me into Private / Exclusive for full control 😈🖤.\n\n"
        "Be respectful, abnormal, and have fun. Tip to play 💋"
    ),
    "tags": ["tomboy", "gamer", "lovense", "athletic", "sensual", "biker"]
}

async def update_stripchat_profile(
    bio_text: Optional[str] = None,
    status_topic: Optional[str] = None,
    headless: bool = False,
    status_callback = None
) -> Dict[str, Any]:
    """
    Inicia sesión asistida/persistente en Stripchat y actualiza la biografía
    y el tema de la sala de Sam Barton.
    """
    user_data_dir = PROFILES_DIR / "stripchat_profile"
    user_data_dir.mkdir(parents=True, exist_ok=True)
    clean_profile_crash_state(user_data_dir)

    bio_val = bio_text or DEFAULT_STRIPCHAT_PROFILE["bio_text"]
    topic_val = status_topic or DEFAULT_STRIPCHAT_PROFILE["status_topic"]

    def log(msg: str):
        print(f"[Stripchat Profile Updater] {msg}", flush=True)
        if status_callback:
            status_callback(msg)

    log(f"Iniciando navegador Chrome para Stripchat (headless={headless})...")
    playwright = await async_playwright().start()

    try:
        context = await playwright.chromium.launch_persistent_context(
            user_data_dir=str(user_data_dir),
            headless=headless,
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
                "--lang=es-ES,es,en-US,en"
            ]
        )

        # Inyectar scripts stealth para Turnstile / Cloudflare
        await context.add_init_script("""
            Object.defineProperty(navigator, 'webdriver', { get: () => undefined });
            window.chrome = window.chrome || { runtime: {}, app: {}, csi: () => {}, loadTimes: () => {} };
            Object.defineProperty(navigator, 'plugins', { get: () => [1, 2, 3, 4, 5] });
            Object.defineProperty(navigator, 'languages', { get: () => ['es-ES', 'es', 'en-US', 'en'] });
        """)
        await context.add_init_script(get_webrtc_media_hook_script())

        page = context.pages[0] if context.pages else await context.new_page()

        log("Navegando a la página de edición de perfil de Stripchat...")
        await page.goto("https://es.stripchat.com/user/edit-profile", wait_until="domcontentloaded", timeout=45000)

        # 1. Esperar Cloudflare si se presenta
        await wait_for_cloudflare_resolution(page, log, timeout_seconds=60)
        await handle_cookies_and_age_dialogs(page, log)

        # 2. Verificar si pide login
        is_login_page = "login" in page.url.lower() or await page.locator("input[name='login'], #login_login_or_email").first.is_visible(timeout=1500)
        if is_login_page:
            log("Requiere inicio de sesión. Cargando credenciales guardadas de Stripchat...")
            creds = load_all_credentials().get("stripchat", {})
            user = creds.get("username", "sambartonn23@gmail.com")
            pwd = creds.get("password", "")

            if user and pwd:
                log(f"Ingresando usuario: {user}...")
                for sel in ["#login_login_or_email", "input[name='login']", "input[type='email']", "input[autocomplete='username']"]:
                    try:
                        u_el = page.locator(sel).first
                        if await u_el.is_visible(timeout=1000):
                            await u_el.click()
                            await u_el.fill(user)
                            break
                    except Exception:
                        pass

                for sel in ["#login_password", "input[name='password']", "input[type='password']"]:
                    try:
                        p_el = page.locator(sel).first
                        if await p_el.is_visible(timeout=1000):
                            await p_el.click()
                            await p_el.fill(pwd)
                            break
                    except Exception:
                        pass

                for sel in ["button:has-text('Iniciar sesión')", "button:has-text('Log In')", "button[type='submit']"]:
                    try:
                        btn = page.locator(sel).first
                        if await btn.is_visible(timeout=1000):
                            await btn.click()
                            log("✓ Formulario enviado. Esperando verificación de sesión...")
                            break
                    except Exception:
                        pass

                await wait_for_cloudflare_resolution(page, log, timeout_seconds=45)
                await page.wait_for_timeout(3000)

        # 3. Navegar directamente al editor de perfil / bio
        log("Accediendo al editor de biografía y detalles de modelo...")
        await page.goto("https://es.stripchat.com/user/edit-profile", wait_until="domcontentloaded", timeout=30000)
        await page.wait_for_timeout(2000)
        await handle_cookies_and_age_dialogs(page, log)

        # Buscar textarea de biografía o información 'Sobre mí' / 'About me'
        bio_updated = False
        bio_selectors = [
            "textarea[name='aboutMe']",
            "textarea[name='bio']",
            "textarea[name='description']",
            "textarea[placeholder*='sobre']",
            "textarea[placeholder*='About']",
            "textarea"
        ]
        for sel in bio_selectors:
            try:
                area = page.locator(sel).first
                if await area.is_visible(timeout=1500):
                    log(f"Campo de biografía localizado: [{sel}]. Inyectando arquetipo Tomboy Gamer...")
                    await area.click()
                    await area.fill(bio_val)
                    bio_updated = True
                    log("✓ Biografía oficial inyectada.")
                    break
            except Exception:
                continue

        # Buscar botón guardar cambios
        if bio_updated:
            for s_btn in ["button:has-text('Guardar')", "button:has-text('Save')", "button:has-text('Actualizar')", "button[type='submit']"]:
                try:
                    save_el = page.locator(s_btn).first
                    if await save_el.is_visible(timeout=1000):
                        await save_el.click()
                        log("✓ Clic en guardar cambios.")
                        await page.wait_for_timeout(1500)
                        break
                except Exception:
                    pass

        # Captura de pantalla como comprobante forense
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        screenshot_path = ARTIFACTS_DIR / f"stripchat_profile_updated_{timestamp}.png"
        ARTIFACTS_DIR.mkdir(parents=True, exist_ok=True)
        try:
            await page.screenshot(path=str(screenshot_path), full_page=False)
            log(f"📸 Captura de verificación guardada en: {screenshot_path.name}")
        except Exception:
            pass

        log("🎉 ¡Proceso de perfil Stripchat finalizado con éxito! El navegador permanecerá abierto para tu show.")
        return {
            "success": True,
            "platform": "stripchat",
            "bio_updated": bio_updated,
            "screenshot": str(screenshot_path)
        }

    except Exception as e:
        log(f"Nota en actualización de Stripchat: {e}")
        return {"success": False, "error": str(e), "platform": "stripchat"}

def run_update_stripchat_sync():
    """Ejecutor síncrono para CLI o subprocesos."""
    return asyncio.run(update_stripchat_profile(headless=False))

if __name__ == "__main__":
    run_update_stripchat_sync()
