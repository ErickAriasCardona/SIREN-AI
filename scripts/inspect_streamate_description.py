import asyncio
from pathlib import Path
from playwright.async_api import async_playwright

async def inspect_description():
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

    # Click "Live Show Description"
    desc_opt = page.locator('text="Live Show Description"').first
    if await desc_opt.count() > 0:
        print("Clicking Live Show Description...")
        await desc_opt.click()
        await page.wait_for_timeout(4000)
        print("Landed on URL:", page.url)
        await page.screenshot(path='artifacts/streamate_audit/live_show_description_page.png', full_page=True)

        txt = await page.evaluate('() => document.body.innerText')
        Path('artifacts/streamate_audit/live_show_description_text.txt').write_text(txt, encoding='utf-8')
        print("Saved live show description text.")

        fields = await page.evaluate('''() => {
            const els = Array.from(document.querySelectorAll('input, textarea, select'));
            return els.map(f => ({
                id: f.id,
                name: f.name,
                placeholder: f.placeholder,
                value: f.value,
                maxlength: f.maxLength,
                tagName: f.tagName,
                outerHTML: f.outerHTML.substring(0, 200)
            }));
        }''')
        import json
        print("Fields in Live Show Description:", json.dumps(fields, indent=2))

    await ctx.close()
    await p.stop()

if __name__ == '__main__':
    asyncio.run(inspect_description())
