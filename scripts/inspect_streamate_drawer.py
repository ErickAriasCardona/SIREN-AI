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

    # Click on the hamburger menu
    btn = page.locator('header button').first
    await btn.click()
    await page.wait_for_timeout(1500)
    await page.screenshot(path='artifacts/streamate_audit/menu_opened.png')

    items = await page.evaluate('''() => {
        const els = Array.from(document.querySelectorAll('nav a, nav button, [role="dialog"] a, [role="dialog"] button, [role="menu"] a, [role="menu"] button, .MuiDrawer-root a, .MuiDrawer-root button'));
        return els.map(el => ({
            tag: el.tagName,
            text: (el.innerText || '').trim().replace(/\\n/g, ' '),
            href: el.getAttribute('href') || ''
        }));
    }''')
    for item in items:
        print(f"{item['tag']} | {item['text']} | {item['href']}")

    await ctx.close()
    await p.stop()

if __name__ == '__main__':
    asyncio.run(check())
