import asyncio
import json
from pathlib import Path
from playwright.async_api import async_playwright

ROOT = Path(__file__).resolve().parent.parent.parent
PROFILE_DIR = ROOT / "data" / "browser_profiles" / "loyalfans_profile"

async def capture_update():
    async with async_playwright() as p:
        ctx = await p.chromium.launch_persistent_context(
            user_data_dir=str(PROFILE_DIR),
            headless=True
        )
        page = await ctx.new_page()
        
        captured_calls = []
        page.on("request", lambda r: captured_calls.append({
            "url": r.url,
            "method": r.method,
            "post_data": r.post_data
        }) if "automations" in r.url else None)

        await page.goto("https://www.loyalfans.com/settings/messages/messages-automation", wait_until="networkidle")
        await page.wait_for_timeout(2000)

        # Quitar chat
        await page.evaluate("() => { document.querySelectorAll('.chat-box, [class*=\"chat-box\"], .conversation-floating').forEach(e => e.remove()); }")

        # Clic en primera fila
        row = await page.query_selector("text='Cuando un no seguidor empieza a seguir'")
        if row:
            await row.click()
            await page.wait_for_timeout(1000)

        header_btns = await page.query_selector_all("mat-expansion-panel-header button")
        print(f"Header buttons count: {len(header_btns)}")
        if len(header_btns) >= 2:
            print("Clic en botón lápiz...")
            await header_btns[1].click()
            await page.wait_for_timeout(2000)

            await page.screenshot(path=str(ROOT / "artifacts" / "modal_edit_automation_opened.png"))
            print("Screenshot del modal guardada.")

            modal_info = await page.evaluate("""() => {
                const dialog = document.querySelector('mat-dialog-container, [role="dialog"], .modal-content');
                if (!dialog) return { found: false };
                const textareas = Array.from(dialog.querySelectorAll('textarea, input[type="text"], [contenteditable="true"]')).map(t => {
                    return { tag: t.tagName, value: t.value || t.innerText, placeholder: t.placeholder };
                });
                const btns = Array.from(dialog.querySelectorAll('button')).map(b => b.innerText.trim()).filter(Boolean);
                return {
                    found: true,
                    textareas: textareas,
                    buttons: btns
                };
            }""")
            print("Modal DOM Info:", modal_info)

        await ctx.close()

if __name__ == "__main__":
    asyncio.run(capture_update())
