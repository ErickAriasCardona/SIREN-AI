import asyncio
import json
import sys
from pathlib import Path
from playwright.async_api import async_playwright

ROOT = Path(__file__).resolve().parent.parent.parent
PROFILE_DIR = ROOT / "data" / "browser_profiles" / "loyalfans_profile"

async def inspect():
    async with async_playwright() as p:
        ctx = await p.chromium.launch_persistent_context(
            user_data_dir=str(PROFILE_DIR),
            headless=True,
            viewport={"width": 1400, "height": 900}
        )
        page = await ctx.new_page()
        print("Navegando a /settings/messages/messages-automation...")
        await page.goto("https://www.loyalfans.com/settings/messages/messages-automation", wait_until="networkidle")
        await page.wait_for_timeout(3000)

        # Capturar screenshot
        screenshot_path = ROOT / "artifacts" / "automation_messages_dom_inspect.png"
        await page.screenshot(path=str(screenshot_path))
        print(f"Screenshot guardada: {screenshot_path}")

        # Extraer estructura
        details = await page.evaluate("""() => {
            const sections = [];
            // Buscar bloques de automatizacion
            const rows = document.querySelectorAll('.card, .row, .item, [class*="automation"], mat-expansion-panel, .form-group');
            const allText = document.body.innerText;
            
            const toggles = Array.from(document.querySelectorAll('mat-slide-toggle, input[type="checkbox"]')).map(t => {
                return {
                    id: t.id,
                    name: t.getAttribute('name'),
                    text: t.innerText || t.parentElement?.innerText || '',
                    checked: t.classList.contains('mat-mdc-slide-toggle-checked') || t.querySelector('input')?.checked
                };
            });

            const inputs = Array.from(document.querySelectorAll('input, textarea, [contenteditable="true"]')).map(i => {
                return {
                    tag: i.tagName,
                    placeholder: i.getAttribute('placeholder'),
                    value: i.value || i.innerText || '',
                    name: i.getAttribute('name')
                };
            });

            return {
                title: document.title,
                toggles_count: toggles.length,
                toggles: toggles,
                inputs: inputs,
                body_sample: allText.slice(0, 3000)
            };
        }""")

        with open(ROOT / "artifacts" / "automation_messages_dom.json", "w", encoding="utf-8") as f:
            json.dump(details, f, indent=2, ensure_ascii=False)
        print("Detalles extraídos con éxito.")
        await ctx.close()

if __name__ == "__main__":
    asyncio.run(inspect())
