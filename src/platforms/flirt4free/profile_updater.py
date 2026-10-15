"""
VELVET AI — Flirt4Free Profile Updater
Actualiza la biografía y tags de Sam Barton en Flirt4Free (High-End Tomboy / VIP Credits).
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

DEFAULT_FLIRT4FREE_PROFILE = {
    "display_name": "Sam Barton",
    "headline": "High-End Tomboy • Intelligent & Sensual VIP ✨",
    "bio_text": (
        "👑 Sam Barton | High-End Tomboy • Intelligent VIP ✨\n\n"
        "Software & AI Architect by trade, sensual athlete and biker by lifestyle.\n"
        "Soccer player, motorcycle traveler, pack leader of dogs & cats 🐾.\n\n"
        "Exclusive True Private & VIP Party Chat experience. "
        "Intelligent conversation, dominant charm, and complete dedication for clients who appreciate genuine distinction. 😈🖤"
    )
}

async def update_flirt4free_profile(headless: bool = False, status_callback = None) -> Dict[str, Any]:
    user_data_dir = PROFILES_DIR / "flirt4free_profile"
    user_data_dir.mkdir(parents=True, exist_ok=True)
    clean_profile_crash_state(user_data_dir)

    def log(msg: str):
        print(f"[Flirt4Free Profile Updater] {msg}", flush=True)
        if status_callback: status_callback(msg)

    log(f"Iniciando navegador para Flirt4Free (headless={headless})...")
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

        log("Navegando a Flirt4Free Model Admin...")
        await page.goto("https://www.flirt4free.com/myaccount/", timeout=45000)
        await page.wait_for_timeout(3000)
        log("Ventana abierta para gestión de perfil.")
        return {"success": True, "platform": "flirt4free"}
    except Exception as e:
        log(f"Nota en Flirt4Free: {e}")
        return {"success": False, "error": str(e), "platform": "flirt4free"}

if __name__ == "__main__":
    asyncio.run(update_flirt4free_profile(headless=False))
