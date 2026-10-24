import sys
import json
import asyncio
from pathlib import Path
from playwright.async_api import async_playwright

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

AUDIT_DIR = Path("artifacts/streamate_audit")

async def extract_smconnect_tabs():
    p = await async_playwright().start()
    profile_dir = Path("data/browser_profiles/streamate_profile")
    ctx = await p.chromium.launch_persistent_context(
        user_data_dir=str(profile_dir),
        headless=True,
        args=["--disable-blink-features=AutomationControlled", "--start-maximized"]
    )
    page = ctx.pages[0] if ctx.pages else await ctx.new_page()

    await page.goto("https://performerclient.streamatemodels.com/client", timeout=30000)
    await page.wait_for_timeout(3000)

    # Click Ajustes
    await page.locator('text=Ajustes').first.click()
    await page.wait_for_timeout(1500)

    tabs = ["Preferencias", "Configuraciones De Chat", "GOLD Menu", "Juguetes Interactivos", "Gira La Rueda"]
    tab_data = {}

    for tab in tabs:
        try:
            btn = page.locator(f'button:has-text("{tab}"), div:has-text("{tab}")').last
            await btn.click()
            await page.wait_for_timeout(1000)
            shot = AUDIT_DIR / f"smconnect_tab_{tab.replace(' ', '_').lower()}.png"
            await page.screenshot(path=str(shot))
            txt = await page.evaluate('() => document.querySelector(".modal, [role=\'dialog\'], .modal-content, .MuiDialog-root") ? document.querySelector(".modal, [role=\'dialog\'], .modal-content, .MuiDialog-root").innerText : document.body.innerText')
            tab_data[tab] = txt
        except Exception as e:
            tab_data[tab] = f"Error: {e}"

    with open(AUDIT_DIR / "smconnect_tabs_data.json", "w", encoding="utf-8") as f:
        json.dump(tab_data, f, indent=2, ensure_ascii=False)

    await ctx.close()
    await p.stop()

if __name__ == "__main__":
    asyncio.run(extract_smconnect_tabs())
