import asyncio
from pathlib import Path
from playwright.async_api import async_playwright

ROOT = Path(__file__).resolve().parent.parent.parent
PROFILE_DIR = ROOT / "data" / "browser_profiles" / "loyalfans_profile"

async def find_save():
    async with async_playwright() as p:
        ctx = await p.chromium.launch_persistent_context(
            user_data_dir=str(PROFILE_DIR),
            headless=True
        )
        page = await ctx.new_page()
        page.on("request", lambda r: print(f"REQ: {r.method} {r.url}") if "/api/" in r.url else None)
        await page.goto("https://www.loyalfans.com/settings/messages/messages-automation", wait_until="networkidle")
        await page.wait_for_timeout(2000)

        # Eliminar chat
        await page.evaluate("() => { document.querySelectorAll('.chat-box, [class*=\"chat-box\"], .conversation-floating').forEach(e => e.remove()); }")

        # Clic en AÑADIR
        await page.click("button:has-text('AÑADIR')")
        await page.wait_for_timeout(1500)

        buttons = await page.evaluate("""() => {
            return Array.from(document.querySelectorAll('button')).map(b => ({
                text: b.innerText.trim(),
                class: b.className,
                type: b.type
            }));
        }""")
        print("Botones disponibles:")
        for b in buttons:
            print("  ->", b)

        # Hacer scroll para ver parte inferior
        await page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
        await page.wait_for_timeout(1000)
        await page.screenshot(path=str(ROOT / "artifacts" / "automation_form_bottom.png"))

        await ctx.close()

if __name__ == "__main__":
    asyncio.run(find_save())
