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

    url = "http://localhost:8888/"
    print(f"Loading UI from {url}...")
    await page.goto(url)
    await page.wait_for_timeout(2000)

    # 1. Check Perfiles tab
    tab_title = await page.inner_text("#current-tab-title")
    print(f"Current Tab Title: {tab_title}")

    # Take screenshot of Editorial Dossier in Dark Mode
    await page.set_viewport_size({"width": 1400, "height": 1100})
    await page.screenshot(path="artifacts/test_ui_editorial_dossier_dark.png")
    print("Saved editorial dossier dark mode screenshot to artifacts/test_ui_editorial_dossier_dark.png")

    # 2. Check Theme Toggle
    print("\n--- Testing Light Theme Toggle ---")
    theme_btn = page.locator("#theme-toggle-btn")
    await theme_btn.click()
    await page.wait_for_timeout(500)
    has_light_class = await page.evaluate("() => document.body.classList.contains('light-theme')")
    print(f"Has 'light-theme' class after click: {has_light_class}")
    await page.screenshot(path="artifacts/test_ui_editorial_dossier_light.png")
    print("Saved editorial dossier light mode screenshot to artifacts/test_ui_editorial_dossier_light.png")

    # Toggle back to dark
    await theme_btn.click()
    await page.wait_for_timeout(500)

    # 3. Check Roxanne Copilot Tab
    print("\n--- Testing Roxanne Assistant Tab ---")
    await page.evaluate("() => switchMainTab('tab-roxanne-copilot')")
    await page.wait_for_timeout(1500)
    copilot_title = await page.inner_text("#current-tab-title")
    print(f"Switched to: {copilot_title}")

    # Check messages box
    chat_box_text = await page.inner_text("#chat-messages-box")
    print("Roxanne Chatbox greeting preview:\n", chat_box_text[:200])

    # Take screenshot of Reorganized Roxanne Tab (Dark Mode)
    await page.screenshot(path="artifacts/test_ui_roxanne_reorganized_dark.png")
    print("Saved roxanne tab dark screenshot to artifacts/test_ui_roxanne_reorganized_dark.png")

    # Test Light Mode for Roxanne Tab
    await theme_btn.click()
    await page.wait_for_timeout(500)
    await page.screenshot(path="artifacts/test_ui_roxanne_reorganized_light.png")
    print("Saved roxanne tab light screenshot to artifacts/test_ui_roxanne_reorganized_light.png")
    await theme_btn.click()
    await page.wait_for_timeout(500)

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
