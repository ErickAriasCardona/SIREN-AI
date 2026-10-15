"""
VELVET AI — Streamate Profile Updater
Actualiza la biografía y tags de Sam Barton en Streamate (Fit Tomboy / Fast PVTs).
"""

import sys
import asyncio
from pathlib import Path
from typing import Dict, Any, Optional
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
from src.automation.platform_auth import clean_profile_crash_state, get_webrtc_media_hook_script

PROFILES_DIR = DATA_DIR / "browser_profiles"

DEFAULT_STREAMATE_PROFILE = {
    "display_name": "Sam Barton",
    "headline": "Fit Tomboy • Adrenaline & Fast PVTs ⚡",
    "bio_text": (
        "🐺 Sam Barton | Fit Tomboy • High Energy & Fast PVTs 🏍️\n\n"
        "Software Architect by trade, adrenaline & fitness addict by passion.\n"
        "Soccer player, motorcycle lover, dog & cat mom 🐾, InuYasha fan 🍙.\n\n"
        "I don't waste your time in Free Chat. Step into Private or Exclusive "
        "if you want real chemistry, teasing banter, and full personal attention. 😈💋"
    )
}

async def update_streamate_profile(headless: bool = False, status_callback = None) -> Dict[str, Any]:
    user_data_dir = PROFILES_DIR / "streamate_profile"
    user_data_dir.mkdir(parents=True, exist_ok=True)
    clean_profile_crash_state(user_data_dir)

    def log(msg: str):
        print(f"[Streamate Profile Updater] {msg}", flush=True)
        if status_callback: status_callback(msg)

    log(f"Iniciando navegador para Streamate (headless={headless})...")
    playwright = await async_playwright().start()
    try:
        context = await playwright.chromium.launch_persistent_context(
            user_data_dir=str(user_data_dir),
            headless=headless,
            no_viewport=True,
            permissions=["camera", "microphone"],
            ignore_default_args=["--enable-automation"],
            args=["--start-maximized", "--disable-blink-features=AutomationControlled"]
        )
        await context.add_init_script(get_webrtc_media_hook_script())
        page = context.pages[0] if context.pages else await context.new_page()

        log("Navegando a Streamate CamModel Portal...")
        await page.goto("https://streamate.com/cammodel/profile", timeout=45000)
        await page.wait_for_timeout(3000)
        log("Ventana abierta para gestión de perfil.")
        return {"success": True, "platform": "streamate"}
    except Exception as e:
        log(f"Nota en Streamate: {e}")
        return {"success": False, "error": str(e), "platform": "streamate"}

if __name__ == "__main__":
    asyncio.run(update_streamate_profile(headless=False))
