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

print("Testing Light Mode Default & Dark Toggle with Playwright...")

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page(viewport={"width": 1440, "height": 900})

    # Clear localStorage to test fresh user experience
    page.goto(file_url, wait_until="networkidle")
    page.evaluate("localStorage.clear()")
    page.reload(wait_until="networkidle")

    # 1. Verify Light Mode is default
    body_classes = page.locator("body").get_attribute("class") or ""
    assert "light-theme" in body_classes, f"Expected light-theme class by default, got: '{body_classes}'"
    print("✓ Body has 'light-theme' class by default!")

    # 2. Verify button label and icon
    btn_label = page.locator("#theme-label").inner_text()
    assert "Modo Oscuro" in btn_label, f"Expected button to propose 'Modo Oscuro', got: '{btn_label}'"
    print("✓ Theme toggle button is ready with 'Modo Oscuro'!")

    # Screenshot in default Light Mode
    page.screenshot(path="artifacts/siren_light_mode_default.png")

    # 3. Click toggle button to switch to Dark Mode
    page.locator("#theme-toggle-btn").click()
    page.wait_for_timeout(200)

    body_classes_dark = page.locator("body").get_attribute("class") or ""
    assert "light-theme" not in body_classes_dark, f"Expected dark mode (no light-theme), got: '{body_classes_dark}'"
    btn_label_dark = page.locator("#theme-label").inner_text()
    assert "Modo Claro" in btn_label_dark, f"Expected button to propose 'Modo Claro', got: '{btn_label_dark}'"
    print("✓ Successfully toggled to Dark Mode!")

    # Screenshot in Dark Mode
    page.screenshot(path="artifacts/siren_dark_mode_toggled.png")

    # 4. Click again to return to Light Mode
    page.locator("#theme-toggle-btn").click()
    page.wait_for_timeout(200)

    body_classes_restored = page.locator("body").get_attribute("class") or ""
    assert "light-theme" in body_classes_restored, "Expected return to Light Mode!"
    print("✓ Successfully toggled back to Light Mode!")

    print("\n🎉 ALL THEME TESTS PASSED: Light Mode default & toggle work perfectly!")
    browser.close()
