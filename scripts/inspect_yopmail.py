import sys
import asyncio
from playwright.async_api import async_playwright

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

async def inspect_yopmail():
    p = await async_playwright().start()
    browser = await p.chromium.launch(headless=True)
    page = await browser.new_page()

    await page.goto("https://yopmail.com/es/", timeout=30000)
    await page.wait_for_timeout(2000)

    # Input login
    await page.fill("#login", "EFAC05")
    await page.keyboard.press("Enter")
    await page.wait_for_timeout(4000)

    print("Current URL:", page.url)

    inbox_frame = page.frame(name="ifinbox")
    mail_frame = page.frame(name="ifmail")

    if inbox_frame:
        print("=== INBOX MESSAGES ===")
        msg_elements = await inbox_frame.evaluate('''() => {
            return Array.from(document.querySelectorAll('.m, .mcall, button.lm, div.m')).map(el => ({
                from: el.querySelector('.lmf')?.innerText || '',
                subject: el.querySelector('.lms')?.innerText || '',
                date: el.querySelector('.lmh')?.innerText || '',
                allText: el.innerText
            }));
        }''')
        print(f"Total elements: {len(msg_elements)}")
        for i, m in enumerate(msg_elements):
            print(f"[{i}] From: {m['from']} | Subject: {m['subject']} | Full: {m['allText']}")
    else:
        print("No inbox frame found!")

    if mail_frame:
        print("\n=== LATEST MAIL CONTENT ===")
        content = await mail_frame.evaluate('() => document.body.innerText')
        for line in content.split('\n'):
            if line.strip():
                print("  ", line.strip())

    await browser.close()
    await p.stop()

if __name__ == "__main__":
    asyncio.run(inspect_yopmail())
