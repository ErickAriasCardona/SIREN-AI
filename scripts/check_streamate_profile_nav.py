import asyncio
from pathlib import Path
from playwright.async_api import async_playwright

async def check():
    p = await async_playwright().start()
    ctx = await p.chromium.launch_persistent_context(
        user_data_dir='data/browser_profiles/streamate_profile',
        headless=True,
        args=['--disable-blink-features=AutomationControlled']
    )
    page = ctx.pages[0] if ctx.pages else await ctx.new_page()
    await page.goto('https://streamatemodels.com/dashboard-creator', timeout=35000)
    await page.wait_for_timeout(3000)

    # Click account button
    acc_btn = page.locator('#header_account_button, header button:has(svg)').last
    await acc_btn.click()
    await page.wait_for_timeout(1000)

    # Click on "Streamate Profile"
    prof_opt = page.locator('text="Streamate Profile"').first
    if await prof_opt.count() > 0:
        print("Found Streamate Profile menu option. Clicking...")
        await prof_opt.click()
        await page.wait_for_timeout(2000)
        await page.screenshot(path='artifacts/streamate_audit/profile_menu_clicked.png')
        print("URL after click:", page.url)
        
        # Check if there are subitems or if it navigated
        body_text = await page.evaluate('() => document.body.innerText')
        print("Page text snippet:\n", body_text[:600])

    await ctx.close()
    await p.stop()

if __name__ == '__main__':
    asyncio.run(check())
