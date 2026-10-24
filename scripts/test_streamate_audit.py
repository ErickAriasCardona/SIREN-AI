import asyncio
from pathlib import Path
from playwright.async_api import async_playwright

async def test_streamate_login():
    p = await async_playwright().start()
    profile_dir = Path('data/browser_profiles/streamate_profile')
    profile_dir.mkdir(parents=True, exist_ok=True)
    
    ctx = await p.chromium.launch_persistent_context(
        user_data_dir=str(profile_dir),
        headless=True,
        args=['--disable-blink-features=AutomationControlled', '--start-maximized']
    )
    page = ctx.pages[0] if ctx.pages else await ctx.new_page()

    print('Navigating to https://streamatemodels.com/login...')
    await page.goto('https://streamatemodels.com/login', timeout=35000)
    await page.wait_for_timeout(2500)

    # Fill credentials
    await page.fill('#username', 'EFAC05@YOPMAIL.COM')
    await page.fill('#password', 'Centenario123@')
    print('Credentials filled. Clicking Log In...')
    await page.click('button[type="submit"]')

    # Wait for navigation
    await page.wait_for_timeout(6000)
    print('Current URL after login attempt:', page.url)
    print('Page title:', await page.title())

    # Check for text on page
    body_text = await page.evaluate('() => document.body.innerText')
    lines = [l.strip() for l in body_text.split('\n') if l.strip()]
    print('--- Page text (first 25 lines) ---')
    for l in lines[:25]:
        print('  ', l)

    # Take screenshot
    Path('artifacts').mkdir(exist_ok=True)
    await page.screenshot(path='artifacts/streamate_login_attempt.png')
    print('Screenshot saved to artifacts/streamate_login_attempt.png')

    await ctx.close()
    await p.stop()

if __name__ == '__main__':
    asyncio.run(test_streamate_login())
