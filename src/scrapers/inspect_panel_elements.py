import asyncio
import json
from pathlib import Path
from playwright.async_api import async_playwright

ROOT = Path(__file__).resolve().parent.parent.parent
PROFILE_DIR = ROOT / "data" / "browser_profiles" / "loyalfans_profile"

async def check_body_btns():
    async with async_playwright() as p:
        ctx = await p.chromium.launch_persistent_context(
            user_data_dir=str(PROFILE_DIR),
            headless=True
        )
        page = await ctx.new_page()
        await page.goto("https://www.loyalfans.com/settings/messages/messages-automation", wait_until="networkidle")
        await page.wait_for_timeout(2000)

        # Quitar chat flotante
        await page.evaluate("() => { document.querySelectorAll('.chat-box, [class*=\"chat-box\"], .conversation-floating').forEach(e => e.remove()); }")

        # Clic en primera fila para expandir
        panel = await page.query_selector("mat-expansion-panel")
        if panel:
            header = await panel.query_selector("mat-expansion-panel-header")
            await header.click()
            await page.wait_for_timeout(1000)

        # Buscar elementos dentro del panel expandido
        info = await page.evaluate("""() => {
            const first = document.querySelector('mat-expansion-panel');
            if (!first) return 'No panel';
            const els = Array.from(first.querySelectorAll('button, span, i, .lf-pencil, [class*="edit"], [class*="trash"], [class*="pencil"]')).map(el => ({
                tag: el.tagName,
                class: el.className,
                text: el.innerText.trim(),
                html: el.outerHTML.slice(0, 150)
            }));
            return els;
        }""")

        with open(ROOT / "artifacts" / "automation_panel_elements.json", "w", encoding="utf-8") as f:
            json.dump(info, f, indent=2, ensure_ascii=False)
        print(f"Encontrados {len(info)} elementos. Guardado en artifacts/automation_panel_elements.json")

        await ctx.close()

if __name__ == "__main__":
    asyncio.run(check_body_btns())
