import sys
import asyncio
from pathlib import Path
from typing import Dict, Any, List, Optional
from datetime import datetime
from playwright.async_api import async_playwright

# Asegurar raíz en sys.path
ROOT_DIR = Path(__file__).resolve().parent.parent.parent.parent
sys.path.append(str(ROOT_DIR))

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

from src.config import ARTIFACTS_DIR
PROFILES_DIR = ROOT_DIR / "data" / "browser_profiles"

# Perfil oficial de Sam Barton v1.1.0 (en inglés para la plataforma)
DEFAULT_ENGLISH_PROFILE = {
    "display_name": "Sam Barton",
    "artist_type": "Software & AI Architect ⚡ Versatile Tomboy 🏍️",
    "bio_text": (
        "🐺 Sam Barton | Software & AI Architect ⚡ Versatile Tomboy 🏍️\n\n"
        "Smart by day, driven about my goals, and teasingly wicked by night.\n\n"
        "Software & AI Architect by trade, but my real sanctuary is motorcycles, speed, and my beloved pack: "
        "my dogs and my 2 cats are my greatest blessings in this world 🐾🐈. "
        "Gym addict, soccer player, late-night sketcher, and an absolute InuYasha devotee 🍙. "
        "I also play the ukulele and sing straight from the heart (Billie Eilish, Radiohead, Lana Del Rey, Gorillaz, Mägo de Oz, Rels B... my playlist is a whole journey).\n\n"
        "Obsessed with neon in the dark, skulls, and eerie October vibes 💀✨. "
        "Working hard every single day to buy my used car in December 🚗 and escape to Cancun 🌴.\n\n"
        "Want my attention? Be respectful, intelligent, different, and abnormal. Generic, boring guys bore me to death. "
        "Treat me right, be thoughtful with genuine acts of service (flowers, letters, chocolates, good food), "
        "and maybe—just maybe—I’ll grant you the privilege to take control 😈🖤.\n\n"
        "Unlock my exclusive world below or slide into my DMs. I’m reading you 💋"
    ),
    "desired_tags": [
        "Tomboy",
        "Biker",
        "Tech"
    ]
}

COOKIE_SELECTORS = [
    "button:has-text('ACEPTA TODO')",
    "button:has-text('ACEPTO')",
    "button:has-text('Aceptar todas')",
    "button:has-text('Aceptar')",
    "button:has-text('Accept all')",
    "button:has-text('Accept All')",
    "button:has-text('I Agree')",
    "button:has-text('Confirmar')",
    "button:has-text('Enter')"
]

def clean_profile_crash_state(user_data_dir: Path):
    """Evita el diálogo de recuperación por cierre inesperado de Chrome."""
    for sub in ["Default", ""]:
        pref_file = (user_data_dir / sub / "Preferences") if sub else (user_data_dir / "Preferences")
        if pref_file.exists():
            try:
                content = pref_file.read_text(encoding="utf-8", errors="ignore")
                content = content.replace('"exit_type":"Crashed"', '"exit_type":"Normal"')
                content = content.replace('"exit_type":"SessionCrashed"', '"exit_type":"Normal"')
                content = content.replace('"exited_cleanly":false', '"exited_cleanly":true')
                pref_file.write_text(content, encoding="utf-8")
            except Exception:
                pass

async def update_loyalfans_profile(
    display_name: Optional[str] = None,
    artist_type: Optional[str] = None,
    bio_text: Optional[str] = None,
    desired_tags: Optional[List[str]] = None,
    headless: bool = True,
    status_callback = None
) -> Dict[str, Any]:
    """Actualiza en vivo los datos del perfil de LoyalFans usando Playwright persistent context."""
    user_data_dir = PROFILES_DIR / "loyalfans_profile"
    user_data_dir.mkdir(parents=True, exist_ok=True)
    clean_profile_crash_state(user_data_dir)

    name_val = display_name or DEFAULT_ENGLISH_PROFILE["display_name"]
    type_val = artist_type or DEFAULT_ENGLISH_PROFILE["artist_type"]
    bio_val = bio_text or DEFAULT_ENGLISH_PROFILE["bio_text"]
    tags_val = desired_tags or DEFAULT_ENGLISH_PROFILE["desired_tags"]

    def log(msg: str):
        print(f"[LoyalFans Profile Updater] {msg}", flush=True)
        if status_callback:
            status_callback(msg)

    log(f"Iniciando Playwright (headless={headless}) para actualizar perfil...")
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    screenshot_path = ARTIFACTS_DIR / f"loyalfans_profile_updated_{timestamp}.png"
    public_screenshot_path = ARTIFACTS_DIR / f"loyalfans_public_verified_{timestamp}.png"

    async with async_playwright() as p:
        context = await p.chromium.launch_persistent_context(
            user_data_dir=str(user_data_dir),
            headless=headless,
            viewport={"width": 1400, "height": 900},
            args=[
                "--start-maximized",
                "--disable-blink-features=AutomationControlled",
                "--disable-session-crashed-bubble",
                "--hide-crash-restore-bubble",
                "--no-first-run",
                "--no-default-browser-check"
            ],
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
        )
        page = context.pages[0] if context.pages else await context.new_page()

        try:
            log("Navegando a https://www.loyalfans.com/settings/profile...")
            await page.goto("https://www.loyalfans.com/settings/profile", wait_until="networkidle", timeout=45000)
            await page.wait_for_timeout(2000)

            # 0. Aceptar cookies y cerrar overlays de chat emergentes
            for c_sel in COOKIE_SELECTORS:
                try:
                    c_btn = page.locator(c_sel).first
                    if await c_btn.is_visible(timeout=800):
                        await c_btn.click(force=True)
                        break
                except Exception:
                    pass

            await page.evaluate("""() => {
                document.querySelectorAll('.chat-box, [class*="chat"], .conversation-floating').forEach(el => el.remove());
            }""")

            # 1. Actualizar Nombre para mostrar (Display Name)
            name_input = page.locator("input#name, input[name='name']").first
            if await name_input.is_visible():
                await name_input.scroll_into_view_if_needed()
                await name_input.click(force=True)
                await page.keyboard.press("Control+A")
                await page.keyboard.press("Backspace")
                await name_input.press_sequentially(name_val, delay=5)
                await name_input.dispatch_event("input")
                await name_input.dispatch_event("change")
                log(f"✓ Nombre para mostrar actualizado: '{name_val}'")

            # 2. Actualizar Tipo de Creador (Artist Type)
            type_input = page.locator("input#type, input[name='artist_type']").first
            if await type_input.is_visible():
                await type_input.scroll_into_view_if_needed()
                await type_input.click(force=True)
                await page.keyboard.press("Control+A")
                await page.keyboard.press("Backspace")
                await type_input.press_sequentially(type_val, delay=5)
                await type_input.dispatch_event("input")
                await type_input.dispatch_event("change")
                log(f"✓ Tipo de creador actualizado: '{type_val}'")

            # 3. Actualizar Biografía en Quill Editor
            editor = page.locator(".ql-editor[contenteditable='true']").first
            if await editor.is_visible():
                await editor.scroll_into_view_if_needed()
                await editor.click(force=True)
                await page.keyboard.press("Control+A")
                await page.keyboard.press("Backspace")
                await page.wait_for_timeout(400)
                await page.keyboard.insert_text(bio_val)
                await editor.dispatch_event("input")
                log("✓ Biografía completa en inglés inyectada en editor Quill.")

            # 4. Actualizar Palabras Claves (Tags)
            for old_tag in ["femdom", "findom"]:
                await page.evaluate(f"""(term) => {{
                    const kws = Array.from(document.querySelectorAll('.keywords_wrapper .keyword'));
                    for (const kw of kws) {{
                        if (kw.innerText.toLowerCase().includes(term)) {{
                            const btn = kw.querySelector('button.lf-close');
                            if (btn) btn.click();
                        }}
                    }}
                }}""", old_tag)
                await page.wait_for_timeout(400)

            tag_input = page.locator("textarea[placeholder*='palabra']").first
            for tag in tags_val:
                if await tag_input.is_enabled():
                    await tag_input.click(force=True)
                    await tag_input.fill(tag)
                    await page.wait_for_timeout(200)
                    await page.keyboard.press("Enter")
                    await page.wait_for_timeout(600)
                    log(f"  + Tag agregado: #{tag}")

            # 5. Guardar Cambios (Botón GUARDAR / SAVE)
            await page.evaluate("""() => {
                document.querySelectorAll('.chat-box, [class*="chat"], .conversation-floating').forEach(el => el.remove());
            }""")
            save_button = page.locator("button.save-button, button:has-text('GUARDAR')").first
            if await save_button.is_visible():
                await save_button.scroll_into_view_if_needed()
                await page.wait_for_timeout(600)
                log("💾 Guardando cambios en LoyalFans...")
                await save_button.click(force=True)
                await page.wait_for_timeout(4000)
                log("✓ ¡Perfil guardado y persistido con éxito en la plataforma!")

            # 6. Captura de evidencia en ajustes
            await page.screenshot(path=str(screenshot_path), full_page=False)
            log(f"📸 Captura de evidencia guardada: {screenshot_path.name}")

            # 7. Verificación en perfil público
            log("Navegando a perfil público para verificación visual...")
            await page.goto("https://www.loyalfans.com/sambarton23", wait_until="networkidle")
            await page.wait_for_timeout(2500)
            await page.evaluate("""() => {
                document.querySelectorAll('.chat-box, [class*="chat"], .conversation-floating').forEach(el => el.remove());
            }""")
            await page.screenshot(path=str(public_screenshot_path), full_page=False)
            log(f"📸 Verificación pública guardada: {public_screenshot_path.name}")

            return {
                "success": True,
                "screenshot_settings": str(screenshot_path),
                "screenshot_public": str(public_screenshot_path),
                "display_name": name_val,
                "artist_type": type_val,
                "tags": tags_val
            }

        except Exception as e:
            err = f"Error al actualizar perfil de LoyalFans: {str(e)}"
            log(f"❌ {err}")
            return {"success": False, "error": err}
        finally:
            await context.close()

if __name__ == "__main__":
    async def main():
        print("--- INICIANDO EJECUCIÓN PROFILE UPDATER ---", flush=True)
        res = await update_loyalfans_profile(headless=True)
        print("Resultado final:", res, flush=True)

    asyncio.run(main())

