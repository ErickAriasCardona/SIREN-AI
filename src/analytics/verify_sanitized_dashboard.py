import asyncio
from playwright.async_api import async_playwright
import os

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page(viewport={"width": 1440, "height": 900})
        file_path = os.path.abspath("index.html")
        await page.goto(f"file:///{file_path.replace(os.sep, '/')}")
        await page.wait_for_timeout(1000)
        
        # Click on Finanzas tab
        finanzas_btn = page.locator('button[onclick*="tab-finanzas"]')
        await finanzas_btn.click()
        await page.wait_for_timeout(1500)
        
        # Screenshot
        screenshot_path = os.path.abspath("artifacts/sanitized_finanzas_dashboard.png")
        await page.screenshot(path=screenshot_path, full_page=False)
        print(f"Screenshot saved to {screenshot_path}")
        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())
