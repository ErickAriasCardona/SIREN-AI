import asyncio
from pathlib import Path
from playwright.async_api import async_playwright

async def inspect_tabs():
    p = await async_playwright().start()
    ctx = await p.chromium.launch_persistent_context(
        user_data_dir='data/browser_profiles/streamate_profile',
        headless=True,
        args=['--disable-blink-features=AutomationControlled']
    )
    page = ctx.pages[0] if ctx.pages else await ctx.new_page()
    await page.goto('https://streamatemodels.com/profile/show-information', timeout=35000)
    await page.wait_for_timeout(3000)

    # Find the language buttons/tabs
    lang_btns = await page.evaluate('''() => {
        return Array.from(document.querySelectorAll('button, [role=\"tab\"], label')).map(el => ({
            tag: el.tagName,
            text: (el.innerText || '').trim(),
            role: el.getAttribute('role') || '',
            id: el.id,
            className: el.className
        })).filter(x => ['EN', 'ES', 'FR', 'PT', 'Save', 'Cancel'].includes(x.text) || x.text.includes('English') || x.text.includes('Español') || x.text.includes('Française') || x.text.includes('Portugues'));
    }''')
    import json
    print("Language/Action buttons:", json.dumps(lang_btns, indent=2))

    await ctx.close()
    await p.stop()

if __name__ == '__main__':
    asyncio.run(inspect_tabs())
