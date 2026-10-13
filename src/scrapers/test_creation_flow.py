import asyncio
from pathlib import Path
from playwright.async_api import async_playwright

ROOT = Path(__file__).resolve().parent.parent.parent
PROFILE_DIR = ROOT / "data" / "browser_profiles" / "loyalfans_profile"

async def test_creation_flow():
    async with async_playwright() as p:
        ctx = await p.chromium.launch_persistent_context(
            user_data_dir=str(PROFILE_DIR),
            headless=True
        )
        page = await ctx.new_page()
        captured = []
        page.on("request", lambda r: captured.append({"url": r.url, "method": r.method, "post_data": r.post_data}) if "api" in r.url else None)

        await page.goto("https://www.loyalfans.com/settings/messages/messages-automation", wait_until="networkidle")
        await page.wait_for_timeout(2000)

        # Quitar chat
        await page.evaluate("() => { document.querySelectorAll('.chat-box, [class*=\"chat-box\"], .conversation-floating').forEach(e => e.remove()); }")

        # Clic en AÑADIR
        await page.click("button:has-text('AÑADIR')")
        await page.wait_for_timeout(1500)

        # Seleccionar Tipo de fan (mat-select)
        mat_selects = await page.query_selector_all("mat-select")
        print(f"Total mat-selects: {len(mat_selects)}")

        if len(mat_selects) >= 2:
            # 1. Tipo de fan: SUBSCRIBER
            await mat_selects[0].click()
            await page.wait_for_timeout(800)
            # Opciones
            options = await page.query_selector_all("mat-option")
            print(f"Opciones tipo fan: {len(options)}")
            for opt in options:
                txt = await opt.inner_text()
                print("  Opt:", txt)
            # Seleccionar la primera
            if options:
                await options[0].click()
                await page.wait_for_timeout(800)

            # 2. Accion
            await mat_selects[1].click()
            await page.wait_for_timeout(800)
            action_opts = await page.query_selector_all("mat-option")
            print(f"Opciones acción: {len(action_opts)}")
            for opt in action_opts:
                txt = await opt.inner_text()
                print("  Action Opt:", txt)
            if action_opts:
                await action_opts[0].click()
                await page.wait_for_timeout(800)

        # 3. Escribir mensaje en textarea
        textarea = await page.query_selector("textarea, [contenteditable='true'], input[placeholder*='mensaje']")
        print("Textarea encontrado:", textarea)
        if textarea:
            await textarea.fill("Hey there! Testing automated message setup.")
            await page.wait_for_timeout(500)

        # Ver qué petición se dispara si pulsamos GUARDAR
        save_btn = await page.query_selector("button:has-text('GUARDAR')")
        print("Botón GUARDAR:", save_btn)
        
        # Limpiar captured calls para ver la que sale al guardar
        captured.clear()
        if save_btn:
            print("Pulsando GUARDAR...")
            await save_btn.click()
            await page.wait_for_timeout(3000)
            print("Peticiones POST/PUT capturadas al guardar:")
            for c in captured:
                if c["method"] in ["POST", "PUT", "PATCH"]:
                    print(f"  -> {c['method']} {c['url']}")
                    print(f"     Payload: {c['post_data']}")

        await page.screenshot(path=str(ROOT / "artifacts" / "after_save_automation.png"))
        await ctx.close()

if __name__ == "__main__":
    asyncio.run(test_creation_flow())
