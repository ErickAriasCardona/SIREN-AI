import asyncio
from pathlib import Path
from playwright.async_api import async_playwright

ROOT = Path(__file__).resolve().parent.parent.parent
PROFILE_DIR = ROOT / "data" / "browser_profiles" / "loyalfans_profile"

async def click_pencil_proper():
    async with async_playwright() as p:
        ctx = await p.chromium.launch_persistent_context(
            user_data_dir=str(PROFILE_DIR),
            headless=True
        )
        page = await ctx.new_page()
        page.on("request", lambda r: print(f"REQ: {r.method} {r.url}") if "automations" in r.url else None)
        await page.goto("https://www.loyalfans.com/settings/messages/messages-automation", wait_until="networkidle")
        await page.wait_for_timeout(2000)

        # Quitar chats
        await page.evaluate("() => { document.querySelectorAll('.chat-box, [class*=\"chat-box\"], .conversation-floating').forEach(e => e.remove()); }")

        # Buscar el contenedor del primer botón de editar
        pencil = await page.query_selector(".lf-pencil-edit")
        parent_btn = await pencil.query_selector("xpath=..")
        tag_info = await parent_btn.evaluate("el => el.tagName + '.' + el.className")
        print("Pencil parent tag:", tag_info)

        # Clic
        await parent_btn.click(force=True)
        await page.wait_for_timeout(2000)

        await page.screenshot(path=str(ROOT / "artifacts" / "parent_btn_clicked.png"))
        print("Screenshot guardada: artifacts/parent_btn_clicked.png")

        # Comprobar si se abrió algo
        state = await page.evaluate("""() => {
            return {
                url: window.location.href,
                has_modal: !!document.querySelector('.modal, mat-dialog-container, .cdk-overlay-pane, form'),
                open_forms: Array.from(document.querySelectorAll('form, .cdk-overlay-pane, mat-dialog-container')).map(f => f.innerText.slice(0, 300))
            };
        }""")
        print("Estado tras clic:", state)

        await ctx.close()

if __name__ == "__main__":
    asyncio.run(click_pencil_proper())
