import asyncio
import json
from pathlib import Path
from playwright.async_api import async_playwright

ROOT = Path(__file__).resolve().parent.parent.parent
PROFILE_DIR = ROOT / "data" / "browser_profiles" / "loyalfans_profile"

async def inspect_interaction():
    async with async_playwright() as p:
        ctx = await p.chromium.launch_persistent_context(
            user_data_dir=str(PROFILE_DIR),
            headless=True,
            viewport={"width": 1400, "height": 900}
        )
        page = await ctx.new_page()
        await page.goto("https://www.loyalfans.com/settings/messages/messages-automation", wait_until="networkidle")
        await page.wait_for_timeout(2000)

        # Quitar chat flotante que estorba
        await page.evaluate("""() => {
            document.querySelectorAll('.chat-box, [class*="chat-box"], .conversation-floating').forEach(e => e.remove());
        }""")

        # Clic en el primer trigger
        print("Haciendo clic en la primera fila...")
        rows = await page.query_selector_all("text='Cuando un no seguidor empieza a seguir'")
        if rows:
            await rows[0].click()
            await page.wait_for_timeout(1500)
            await page.screenshot(path=str(ROOT / "artifacts" / "automation_row_clicked.png"))
            print("Captura tomada de la fila abierta.")

        # Extraer elementos dentro del panel abierto
        inner_data = await page.evaluate("""() => {
            const inputs = Array.from(document.querySelectorAll('textarea, input[type="text"], [contenteditable="true"]')).map(i => {
                return {
                    tag: i.tagName,
                    placeholder: i.getAttribute('placeholder'),
                    value: i.value || i.innerText || '',
                    name: i.getAttribute('name'),
                    classes: i.className
                };
            });
            const buttons = Array.from(document.querySelectorAll('button')).map(b => b.innerText.trim()).filter(Boolean);
            return {
                inputs: inputs,
                buttons: buttons
            };
        }""")
        print("Elementos abiertos:", inner_data)
        await ctx.close()

if __name__ == "__main__":
    asyncio.run(inspect_interaction())
