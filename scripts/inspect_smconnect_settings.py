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

async def inspect_smconnect_settings():
    p = await async_playwright().start()
    profile_dir = Path("data/browser_profiles/streamate_profile")
    ctx = await p.chromium.launch_persistent_context(
        user_data_dir=str(profile_dir),
        headless=True,
        args=["--disable-blink-features=AutomationControlled", "--start-maximized"]
    )
    page = ctx.pages[0] if ctx.pages else await ctx.new_page()

    await page.goto("https://performerclient.streamatemodels.com/client", timeout=30000)
    await page.wait_for_timeout(3500)

    # Click Ajustes
    print("--- Clicking Ajustes in SMConnect ---")
    try:
        ajustes_btn = page.locator('text=Ajustes').first
        if await ajustes_btn.count() > 0:
            await ajustes_btn.click()
            await page.wait_for_timeout(1500)
            await page.screenshot(path=str(AUDIT_DIR / "12_smconnect_ajustes.png"))
            modal_text = await page.evaluate('() => document.body.innerText')
            print("Ajustes modal text preview:\n", modal_text[:1000])
    except Exception as e:
        print("Error on Ajustes:", e)

    await ctx.close()
    await p.stop()

if __name__ == "__main__":
    asyncio.run(inspect_smconnect_settings())
