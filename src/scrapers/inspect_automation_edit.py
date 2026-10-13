import asyncio
import json
from pathlib import Path
from playwright.async_api import async_playwright

ROOT = Path(__file__).resolve().parent.parent.parent
PROFILE_DIR = ROOT / "data" / "browser_profiles" / "loyalfans_profile"

async def inspect_edit():
    async with async_playwright() as p:
        ctx = await p.chromium.launch_persistent_context(
            user_data_dir=str(PROFILE_DIR),
            headless=True,
            viewport={"width": 1400, "height": 900}
        )
        page = await ctx.new_page()
        await page.goto("https://www.loyalfans.com/settings/messages/messages-automation", wait_until="networkidle")
        await page.wait_for_timeout(2000)

        # Quitar chat flotante
        await page.evaluate("""() => {
            document.querySelectorAll('.chat-box, [class*="chat-box"], .conversation-floating').forEach(e => e.remove());
        }""")

        # Abrir la fila
        row = await page.query_selector("text='Cuando un no seguidor empieza a seguir'")
        if row:
            await row.click()
            await page.wait_for_timeout(1000)

        # Buscar el boton de editar (icono lápiz)
        pencil_buttons = await page.query_selector_all("button:has(mat-icon), button:has(i), [class*='edit'], .bi-pencil, mat-icon:has-text('edit')")
        print(f"Botones candidatos: {len(pencil_buttons)}")

        # Intentar clic en el botón de editar cerca de la fila abierta
        edit_btn = await page.query_selector("mat-expansion-panel [class*='edit'], .mat-expansion-panel-header [class*='edit'], [aria-label*='edit'], [aria-label*='editar'], button:has(.fa-pencil), button:has(.fa-edit), button:has-text('edit')")
        if not edit_btn:
            # Buscar el segundo boton dentro de la cabecera (trash, pencil, toggle)
            header_btns = await page.query_selector_all("mat-expansion-panel-header button, .mat-expansion-panel-header button")
            print(f"Header buttons: {len(header_btns)}")
            if len(header_btns) >= 2:
                edit_btn = header_btns[1] # El lápiz es el del medio
        
        if edit_btn:
            await edit_btn.click()
            await page.wait_for_timeout(1500)
            await page.screenshot(path=str(ROOT / "artifacts" / "automation_edit_modal.png"))
            print("Clic en lápiz ejecutado.")

        modal_data = await page.evaluate("""() => {
            const textareas = Array.from(document.querySelectorAll('textarea, input[type="text"], .ql-editor, [contenteditable="true"]')).map(t => {
                return {
                    tag: t.tagName,
                    placeholder: t.getAttribute('placeholder'),
                    value: t.value || t.innerText || '',
                    classes: t.className
                };
            });
            const buttons = Array.from(document.querySelectorAll('button, mat-dialog-container button, .modal button')).map(b => b.innerText.trim()).filter(Boolean);
            return {
                textareas: textareas,
                buttons: buttons,
                dialog_open: !!document.querySelector('mat-dialog-container, .modal, .cdk-overlay-pane')
            };
        }""")
        print("Datos del modal:", modal_data)
        await ctx.close()

if __name__ == "__main__":
    asyncio.run(inspect_edit())
