import os
import sys
from playwright.sync_api import sync_playwright

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

ARTIFACTS_DIR = r"C:\Users\MI PC\.gemini\antigravity\brain\4782b539-824e-4ebf-9a1f-b247d4f7399a"

def test_logo_and_footer():
    print("Testing new SIREN logo and sidebar footer version...")
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)

        # 1. Desktop Test (Light Theme by default)
        context = browser.new_context(viewport={"width": 1440, "height": 900})
        page = context.new_page()
        page.goto("http://localhost:8888/", wait_until="networkidle")
        page.wait_for_timeout(800)

        # Verify logo exists in sidebar header
        logo_el = page.locator("#siren-header-logo-wrap")
        assert logo_el.is_visible(), "Logo wrap must be visible in sidebar header"
        print("  ✓ Sidebar header logo wrap is visible")

        # Verify version pill in footer
        version_el = page.locator(".sidebar-version-pill")
        assert version_el.is_visible(), "Version pill must be visible in sidebar footer"
        version_text = version_el.inner_text().strip()
        assert "v1.0" in version_text, f"Expected v1.0 in footer, found: {version_text}"
        print(f"  ✓ Sidebar footer contains version: {version_text}")

        # Capture Desktop Sidebar (Light Mode)
        shot_desktop_light = os.path.join(ARTIFACTS_DIR, "desktop_sidebar_logo_light.png")
        page.screenshot(path=shot_desktop_light)
        print(f"  ✓ Saved screenshot: {shot_desktop_light}")

        # Open Logo Selector Modal
        logo_el.click()
        page.wait_for_timeout(500)
        modal = page.locator("#logoSelectorModal")
        assert modal.is_visible(), "Logo selector modal should open on logo click"
        print("  ✓ Logo selector modal opened showing 3 options")

        shot_modal = os.path.join(ARTIFACTS_DIR, "logo_selector_modal.png")
        page.screenshot(path=shot_modal)
        print(f"  ✓ Saved modal screenshot: {shot_modal}")

        # Close modal
        page.locator("#logoSelectorModal .close-modal").click()
        page.wait_for_timeout(300)

        # Switch to Dark Theme & capture
        page.locator("#theme-toggle-btn").click()
        page.wait_for_timeout(500)
        shot_desktop_dark = os.path.join(ARTIFACTS_DIR, "desktop_sidebar_logo_dark.png")
        page.screenshot(path=shot_desktop_dark)
        print(f"  ✓ Saved Dark Mode screenshot: {shot_desktop_dark}")

        context.close()

        # 2. Mobile Test (390x844)
        context_mobile = browser.new_context(
            viewport={"width": 390, "height": 844},
            is_mobile=True,
            has_touch=True
        )
        page_mobile = context_mobile.new_page()
        page_mobile.goto("http://localhost:8888/", wait_until="networkidle")
        page_mobile.wait_for_timeout(800)

        # Open mobile sidebar
        page_mobile.locator("#btn-open-sidebar").click()
        page_mobile.wait_for_timeout(500)

        # Check logo & version in mobile sidebar
        m_logo = page_mobile.locator("#siren-header-logo-wrap")
        assert m_logo.is_visible(), "Logo must be visible in mobile sidebar"
        m_version = page_mobile.locator(".sidebar-version-pill")
        assert m_version.is_visible(), "Version pill must be visible in mobile sidebar"

        shot_mobile_sidebar = os.path.join(ARTIFACTS_DIR, "mobile_sidebar_new_logo.png")
        page_mobile.screenshot(path=shot_mobile_sidebar)
        print(f"  ✓ Saved mobile sidebar screenshot: {shot_mobile_sidebar}")

        context_mobile.close()
        browser.close()

    print("\n🎉 ALL LOGO & SIDEBAR FOOTER TESTS PASSED!")

if __name__ == "__main__":
    test_logo_and_footer()
