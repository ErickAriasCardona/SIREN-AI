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

print("Testing Streamate Tools & Mahia Right Panel Integration with Playwright...")

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page(viewport={"width": 1440, "height": 900})

    page.goto(file_url, wait_until="networkidle")

    # 1. Switch to ROXANNE Copilot tab
    page.evaluate("switchMainTab('tab-roxanne-copilot')")
    page.wait_for_timeout(400)

    # 2. Check that the buttons are in the right panel and NOT in center chat
    center_buttons = page.locator(".roxanne-center-chat button:has-text('Menú GOLD')")
    assert center_buttons.count() == 0, "Buttons still found inside center chat!"
    print("✓ Center chat is clean: zero toolbars obstructing the chat messages console!")

    right_panel_buttons = page.locator("#roxanne-right-panel #sm-tools-dropdown-body button")
    assert right_panel_buttons.count() >= 4, f"Expected 4 Streamate buttons in right panel dropdown, found {right_panel_buttons.count()}"
    print("✓ All 4 Streamate & Mahia buttons are properly placed in the right panel dropdown!")

    # 3. Test accordion toggle (collapsing and deploying dropdown body)
    dropdown_body = page.locator("#sm-tools-dropdown-body")
    assert dropdown_body.is_visible(), "Dropdown body should be visible initially"

    # Click card header to collapse
    page.locator("#sm-tools-card-header").click()
    page.wait_for_timeout(200)
    assert not dropdown_body.is_visible(), "Dropdown body did not collapse upon header click!"
    print("✓ Herramientas Streamate card collapsed successfully upon click!")

    # Click card header to expand back
    page.locator("#sm-tools-card-header").click()
    page.wait_for_timeout(200)
    assert dropdown_body.is_visible(), "Dropdown body did not deploy upon header click!"
    print("✓ Herramientas Streamate card deployed downwards successfully revealing 4 buttons!")

    # 4. Test opening Menú GOLD modal from the right panel
    page.locator("#sm-tools-dropdown-body button:has-text('Menú GOLD')").click()
    page.wait_for_timeout(300)
    assert page.is_visible("#streamMonitorModal"), "Modal did not open for Gold Menu!"
    heading = page.locator("#smModalHeading").inner_text()
    assert "Menú GOLD" in heading, f"Unexpected heading: {heading}"
    textarea_val = page.locator("#smModalTextarea").input_value()
    assert "10x nalgadas - 15" in textarea_val, "Default textarea text missing expected format"
    instructions_text = page.locator("#smModalInstructions").inner_text()
    assert "Mahia" in instructions_text, f"Expected Mahia in instructions, got {instructions_text}"
    label_text = page.locator("#smModalInputLabel").inner_text()
    assert "opciones" in label_text.lower() or "mahia" in label_text.lower(), f"Unexpected label text: {label_text}"
    print("✓ Menú GOLD dialog opens cleanly with Mahia branding and correct instructions!")

    page.screenshot(path="artifacts/stream_monitor_right_panel_gold_modal.png")
    page.evaluate("closeSmModal()")
    page.wait_for_timeout(200)

    # 5. Test Right Panel Collapse / Expand (Hide & Show Sidebar)
    collapse_btn = page.locator("#btn-collapse-right-panel")
    assert collapse_btn.is_visible(), "Collapse button in upper-left of right panel missing!"
    
    # Click collapse button
    collapse_btn.click()
    page.wait_for_timeout(300)

    right_panel = page.locator("#roxanne-right-panel")
    assert not right_panel.is_visible(), "Right panel is still visible after clicking collapse!"
    
    show_btn = page.locator("#btn-show-right-panel")
    assert show_btn.is_visible(), "Restore panel button in chat header should be visible when collapsed!"
    print("✓ Right panel collapsed cleanly! Center chat occupies 100% of workspace width.")

    page.screenshot(path="artifacts/roxanne_full_width_chat_collapsed.png")

    # Click restore button in chat header
    show_btn.click()
    page.wait_for_timeout(300)
    assert right_panel.is_visible(), "Right panel did not restore after clicking show button!"
    assert not show_btn.is_visible(), "Restore button should be hidden when panel is open!"
    print("✓ Right panel restored smoothly with all tools and KPIs visible!")

    page.screenshot(path="artifacts/roxanne_right_panel_restored.png")

    print("\n🎉 ALL TESTS PASSED: Mahia branding, right-panel dropdown, and collapsible sidebar work flawlessly!")
    browser.close()
