import asyncio
from pathlib import Path
from playwright.async_api import async_playwright

async def inspect_profile():
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

    # Click "Streamate Profile"
    await page.locator('text="Streamate Profile"').first.click()
    await page.wait_for_timeout(1000)

    # Click "Profile Information"
    prof_info = page.locator('text="Profile Information"').first
    if await prof_info.count() > 0:
        print("Clicking Profile Information...")
        await prof_info.click()
        await page.wait_for_timeout(4000)
        print("Landed on URL:", page.url)
        await page.screenshot(path='artifacts/streamate_audit/profile_information_page.png', full_page=True)

        inputs = await page.evaluate('''() => {
            const fields = Array.from(document.querySelectorAll('input, textarea, select'));
            return fields.map(f => ({
                id: f.id,
                name: f.name,
                placeholder: f.placeholder,
                value: f.value,
                type: f.type,
                maxlength: f.maxLength,
                tagName: f.tagName
            }));
        }''')
        import json
        print("Form Fields:", json.dumps(inputs, indent=2))

        # Check full text of the page
        txt = await page.evaluate('() => document.body.innerText')
        Path('artifacts/streamate_audit/profile_information_text.txt').write_text(txt, encoding='utf-8')
        print("Saved profile information page text.")

    await ctx.close()
    await p.stop()

if __name__ == '__main__':
    asyncio.run(inspect_profile())
