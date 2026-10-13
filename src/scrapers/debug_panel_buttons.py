import asyncio
from pathlib import Path
from playwright.async_api import async_playwright

ROOT = Path(__file__).resolve().parent.parent.parent
PROFILE_DIR = ROOT / "data" / "browser_profiles" / "loyalfans_profile"

async def debug_panel():
    async with async_playwright() as p:
        ctx = await p.chromium.launch_persistent_context(
            user_data_dir=str(PROFILE_DIR),
            headless=True
        )
        page = await ctx.new_page()
        await page.goto("https://www.loyalfans.com/settings/messages/messages-automation", wait_until="networkidle")
        await page.wait_for_timeout(2000)

        await page.evaluate("() => { document.querySelectorAll('.chat-box, [class*=\"chat-box\"], .conversation-floating').forEach(e => e.remove()); }")

        # Clic en el primer header
        header = await page.query_selector("mat-expansion-panel-header")
        await header.click()
        await page.wait_for_timeout(1000)

        # Listar todos los botones dentro del mat-expansion-panel
        panel = await page.query_selector("mat-expansion-panel")
        btns = await panel.query_selector_all("button")
        print(f"Total botones en panel: {len(btns)}")
        for i, b in enumerate(btns):
            cls = await b.get_attribute("class")
            txt = await b.inner_text()
            print(f"  [{i}] class='{cls}' text='{txt}'")

        # Probar clic en el botón [1] del panel
        if len(btns) > 1:
            print("Probando clic en el botón de edición [1]...")
            await btns[1].click()
            await page.wait_for_timeout(2000)
            await page.screenshot(path=str(ROOT / "artifacts" / "btn_1_clicked_result.png"))

        await ctx.close()

if __name__ == "__main__":
    asyncio.run(debug_panel())
