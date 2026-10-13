import asyncio
import json
from pathlib import Path
from playwright.async_api import async_playwright

ROOT = Path(__file__).resolve().parent.parent.parent
PROFILE_DIR = ROOT / "data" / "browser_profiles" / "loyalfans_profile"

async def select_prev_month():
    async with async_playwright() as p:
        ctx = await p.chromium.launch_persistent_context(
            user_data_dir=str(PROFILE_DIR),
            headless=True
        )
        page = await ctx.new_page()
        captured_calls = []
        page.on("response", lambda r: captured_calls.append(r.url) if "funds" in r.url or "trans" in r.url else None)
        await page.goto("https://www.loyalfans.com/settings/earnings/statements", wait_until="networkidle")
        await page.wait_for_timeout(2000)

        # Eliminar chat
        await page.evaluate("() => { document.querySelectorAll('.chat-box, [class*=\"chat-box\"], .conversation-floating').forEach(e => e.remove()); }")

        # Clic en selector de mes
        select = await page.query_selector("mat-select")
        print("Select encontrado:", select)
        if select:
            await select.click()
            await page.wait_for_timeout(1000)

            options = await page.evaluate("""() => {
                return Array.from(document.querySelectorAll('mat-option')).map(o => o.innerText.trim());
            }""")
            print("Opciones de mes disponibles:", options)

            # Clic en septiembre
            sept_opt = await page.query_selector("mat-option:has-text('09'), mat-option:has-text('Septiembre'), mat-option:has-text('September'), mat-option:has-text('7.19')")
            print("Opción septiembre encontrada:", sept_opt)
            if sept_opt:
                captured_calls.clear()
                await sept_opt.click()
                await page.wait_for_timeout(3000)
                await page.screenshot(path=str(ROOT / "artifacts" / "september_statements_result.png"))
                print("Captura tomada de Septiembre 2026.")
                print("Llamadas disparadas:", captured_calls)

                # Extraer filas de transacciones
                tx_rows = await page.evaluate("""() => {
                    const rows = Array.from(document.querySelectorAll('table tr, .table tr, .transaction-row, [class*="item"]')).map(r => r.innerText.trim());
                    return {
                        bodyText: document.body.innerText.slice(0, 1500),
                        rows: rows
                    };
                }""")
                with open(ROOT / "artifacts" / "september_real_rows.json", "w", encoding="utf-8") as f:
                    json.dump(tx_rows, f, indent=2, ensure_ascii=False)

        await ctx.close()

if __name__ == "__main__":
    asyncio.run(select_prev_month())
