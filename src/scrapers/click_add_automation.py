import asyncio
from pathlib import Path
from playwright.async_api import async_playwright

ROOT = Path(__file__).resolve().parent.parent.parent
PROFILE_DIR = ROOT / "data" / "browser_profiles" / "loyalfans_profile"

async def test_add():
    async with async_playwright() as p:
        ctx = await p.chromium.launch_persistent_context(
            user_data_dir=str(PROFILE_DIR),
            headless=True
        )
        page = await ctx.new_page()
        page.on("request", lambda r: print(f"REQ: {r.method} {r.url}") if "/api/" in r.url else None)
        await page.goto("https://www.loyalfans.com/settings/messages/messages-automation", wait_until="networkidle")
        await page.wait_for_timeout(2000)

        # Quitar chat
        await page.evaluate("() => { document.querySelectorAll('.chat-box, [class*=\"chat-box\"], .conversation-floating').forEach(e => e.remove()); }")

        # Clic en + AÑADIR
        add_btn = await page.query_selector("button:has-text('AÑADIR'), .btn:has-text('AÑADIR')")
        print("Botón AÑADIR:", add_btn)
        if add_btn:
            await add_btn.click()
            await page.wait_for_timeout(2000)
            await page.screenshot(path=str(ROOT / "artifacts" / "add_automation_clicked.png"))
            print("Captura tomada tras clic en AÑADIR.")

            # Extraer contenido de la pantalla o modal
            modal_text = await page.evaluate("""() => {
                const el = document.querySelector('mat-dialog-container, .modal, .cdk-overlay-pane, form');
                return el ? el.innerText : 'No dialog';
            }""")
            print("Modal content:", modal_text)

        await ctx.close()

if __name__ == "__main__":
    asyncio.run(test_add())
