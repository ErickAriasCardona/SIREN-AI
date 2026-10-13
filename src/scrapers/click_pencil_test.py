import asyncio
import json
from pathlib import Path
from playwright.async_api import async_playwright

ROOT = Path(__file__).resolve().parent.parent.parent
PROFILE_DIR = ROOT / "data" / "browser_profiles" / "loyalfans_profile"

async def test_pencil_click():
    async with async_playwright() as p:
        ctx = await p.chromium.launch_persistent_context(
            user_data_dir=str(PROFILE_DIR),
            headless=True
        )
        page = await ctx.new_page()
        
        # Escuchar peticiones para ver qué endpoint llama al editar/guardar
        page.on("request", lambda r: print(f"REQ: {r.method} {r.url}") if "api" in r.url else None)

        await page.goto("https://www.loyalfans.com/settings/messages/messages-automation", wait_until="networkidle")
        await page.wait_for_timeout(2000)

        # Quitar chat flotante
        await page.evaluate("() => { document.querySelectorAll('.chat-box, [class*=\"chat-box\"], .conversation-floating').forEach(e => e.remove()); }")

        # Clic en el primer .lf-pencil-edit
        pencils = await page.query_selector_all(".lf-pencil-edit")
        print(f"Total lápices encontrados: {len(pencils)}")

        if pencils:
            print("Haciendo clic en el primer lápiz...")
            await pencils[0].click(force=True)
            await page.wait_for_timeout(2000)

            await page.screenshot(path=str(ROOT / "artifacts" / "pencil_edit_clicked.png"))
            print("Screenshot guardada: artifacts/pencil_edit_clicked.png")

            modal_info = await page.evaluate("""() => {
                const modal = document.querySelector('mat-dialog-container, .modal-dialog, [role="dialog"], .cdk-overlay-pane');
                if (!modal) return { dialog_found: false };
                const textareas = Array.from(modal.querySelectorAll('textarea, input, [contenteditable="true"]')).map(el => ({
                    tag: el.tagName,
                    placeholder: el.placeholder,
                    value: el.value || el.innerText,
                    name: el.name,
                    classes: el.className
                }));
                const buttons = Array.from(modal.querySelectorAll('button')).map(b => b.innerText.trim());
                return {
                    dialog_found: true,
                    text: modal.innerText.slice(0, 500),
                    textareas: textareas,
                    buttons: buttons
                };
            }""")
            print("Modal Info:", modal_info)

        await ctx.close()

if __name__ == "__main__":
    asyncio.run(test_pencil_click())
