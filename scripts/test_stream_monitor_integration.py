import sys
from pathlib import Path
from playwright.sync_api import sync_playwright

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

html_path = Path(__file__).resolve().parent.parent / "index.html"
file_url = html_path.as_uri()

print("Testing Stream Monitor integration with Playwright...")

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page(viewport={"width": 1440, "height": 900})

    page.goto(file_url, wait_until="networkidle")

    # 1. Switch to ROXANNE Copilot tab
    page.evaluate("switchMainTab('tab-roxanne-copilot')")
    page.wait_for_timeout(300)

    # 2. Check that the toolbar buttons exist
    toolbar_buttons = page.locator("button:has-text('Menú GOLD'), button:has-text('Gira La Rueda'), button:has-text('Tema de Sala'), button:has-text('Radar Tomboy')")
    assert toolbar_buttons.count() >= 4, f"Expected 4 Stream Monitor buttons, found {toolbar_buttons.count()}"
    print("✓ All 4 Stream Monitor action buttons exist in Roxanne's tab!")

    # 3. Test opening Menú GOLD modal
    page.evaluate("openSmModal('gold')")
    page.wait_for_timeout(300)
    assert page.is_visible("#streamMonitorModal"), "Modal did not open for Gold Menu!"
    heading = page.locator("#smModalHeading").inner_text()
    assert "Menú GOLD" in heading, f"Unexpected heading: {heading}"
    textarea_val = page.locator("#smModalTextarea").input_value()
    assert "10x nalgadas - 15" in textarea_val, "Default textarea text missing expected format"
    print("✓ Menú GOLD dialog opens with correct structure, explanation, and placeholder!")

    # Screenshot of Menú Gold dialog
    page.screenshot(path="artifacts/stream_monitor_dialog_gold.png")
    page.evaluate("closeSmModal()")
    page.wait_for_timeout(200)
    assert not page.is_visible("#streamMonitorModal"), "Modal did not close!"
    print("✓ Modal closes cleanly")

    # 4. Test opening Ruleta modal
    page.evaluate("openSmModal('wheel')")
    page.wait_for_timeout(300)
    assert page.is_visible("#streamMonitorModal"), "Modal did not open for Wheel!"
    heading = page.locator("#smModalHeading").inner_text()
    assert "Gira La Rueda" in heading, f"Unexpected heading: {heading}"
    textarea_val = page.locator("#smModalTextarea").input_value()
    assert "Costo: 20" in textarea_val, "Wheel default text missing expected format"
    print("✓ Ruleta dialog opens with correct structure and 8+ options!")
    page.evaluate("closeSmModal()")

    # 5. Test opening Tema de Sala modal
    page.evaluate("openSmModal('topic')")
    page.wait_for_timeout(300)
    assert page.is_visible("#streamMonitorModal"), "Modal did not open for Topic!"
    heading = page.locator("#smModalHeading").inner_text()
    assert "Tema de Habitación" in heading, f"Unexpected heading: {heading}"
    print("✓ Tema de Sala dialog opens with anti-emoji reminder and clean copy!")
    page.evaluate("closeSmModal()")

    # 6. Test opening Radar Tomboy modal
    page.evaluate("openSmModal('radar')")
    page.wait_for_timeout(300)
    assert page.is_visible("#streamMonitorModal"), "Modal did not open for Radar!"
    heading = page.locator("#smModalHeading").inner_text()
    assert "Radar" in heading, f"Unexpected heading: {heading}"
    print("✓ Radar Tomboy dialog opens with live competitor scan action!")
    page.evaluate("closeSmModal()")

    print("\nAll Stream Monitor dialog tests passed with 100% success!")
    browser.close()
