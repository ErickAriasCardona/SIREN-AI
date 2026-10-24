import sys
import asyncio
from pathlib import Path
from playwright.async_api import async_playwright

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

async def test_ui():
    p = await async_playwright().start()
    browser = await p.chromium.launch(headless=True)
    page = await browser.new_page()

    errors = []
    page.on("pageerror", lambda err: errors.append(f"PAGE ERROR: {err}"))
    page.on("console", lambda msg: errors.append(f"CONSOLE: {msg.text}") if msg.type == "error" else None)

    file_url = f"file:///{Path('index.html').resolve()}".replace("\\", "/")
    print(f"Loading UI from {file_url}...")
    await page.goto(file_url)
    await page.wait_for_timeout(2000)

    # 1. Check Perfiles tab
    tab_title = await page.inner_text("#current-tab-title")
    print(f"Current Tab Title: {tab_title}")

    # Check cards
    cards_text = await page.evaluate('''() => {
        const cards = Array.from(document.querySelectorAll('.platform-profile-card'));
        return cards.map(c => c.innerText);
    }''')
    print(f"Rendered {len(cards_text)} platform profile cards.")
    for i, t in enumerate(cards_text[:4]):
        first_line = t.split('\n')[0] if t else ''
        print(f"  Card {i+1}: {first_line[:60]}")

    # 2. Check Theme Toggle
    print("\n--- Testing Light Theme Toggle ---")
    theme_btn = page.locator("#theme-toggle-btn")
    await theme_btn.click()
    await page.wait_for_timeout(500)
    has_light_class = await page.evaluate("() => document.body.classList.contains('light-theme')")
    print(f"Has 'light-theme' class after click: {has_light_class}")
    await page.screenshot(path="artifacts/test_ui_light_mode.png")
    print("Saved light mode screenshot to artifacts/test_ui_light_mode.png")

    # Toggle back
    await theme_btn.click()
    await page.wait_for_timeout(500)
    has_light_class_after = await page.evaluate("() => document.body.classList.contains('light-theme')")
    print(f"Has 'light-theme' class after second click: {has_light_class_after}")

    # 3. Check Roxanne Copilot Tab
    print("\n--- Testing Roxanne Assistant Tab ---")
    await page.evaluate("() => switchMainTab('tab-roxanne-copilot')")
    await page.wait_for_timeout(1000)
    copilot_title = await page.inner_text("#current-tab-title")
    print(f"Switched to: {copilot_title}")

    # Check messages box
    chat_box_text = await page.inner_text("#chat-messages-box")
    print("Roxanne Chatbox greeting preview:\n", chat_box_text[:300])

    await page.screenshot(path="artifacts/test_ui_roxanne_tab.png")
    print("Saved roxanne tab screenshot to artifacts/test_ui_roxanne_tab.png")

    if errors:
        print("\nErrors captured during UI test:")
        for err in errors:
            print(" ", err)
    else:
        print("\nSUCCESS: 0 console/page errors detected!")

    await browser.close()
    await p.stop()

if __name__ == "__main__":
    asyncio.run(test_ui())
