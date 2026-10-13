import asyncio
from playwright.async_api import async_playwright
import os

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page(viewport={"width": 1440, "height": 950})
        
        page.on("console", lambda msg: print(f"[Browser Console]: {msg.text}"))
        page.on("pageerror", lambda err: print(f"[Browser PageError]: {err}"))
        
        await page.goto("http://localhost:8888/index.html")
        await page.wait_for_timeout(1000)
        
        # Call switchMainTab
        res = await page.evaluate("""() => {
            switchMainTab('tab-roxanne-copilot');
            const sec = document.getElementById('tab-roxanne-copilot');
            const inp = document.getElementById('copilot-input');
            return {
                sectionExists: !!sec,
                sectionClass: sec ? sec.className : null,
                inputExists: !!inp,
                inputOffsetParent: inp ? !!inp.offsetParent : null
            };
        }""")
        print("Debug evaluation:", res)
        await page.wait_for_timeout(1000)
        
        # Scroll textarea into view and type
        await page.locator('#copilot-input').scroll_into_view_if_needed()
        await page.locator('#copilot-input').fill("Hola hermosa, que moto manejas?")
        await page.locator('#copilot-send-btn').click()
        
        print("Sent message, waiting for reply...")
        await page.wait_for_selector('.chat-msg.sam .copy-msg-btn', timeout=40000)
        await page.wait_for_timeout(2000)
        
        screenshot_path = os.path.abspath("artifacts/roxanne_live_chat_verified.png")
        await page.screenshot(path=screenshot_path, full_page=False)
        print("Saved screenshot to:", screenshot_path)
        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())
