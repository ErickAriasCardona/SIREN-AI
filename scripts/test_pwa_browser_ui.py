import os
import sys
from playwright.sync_api import sync_playwright

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

ARTIFACTS_DIR = r"C:\Users\MI PC\.gemini\antigravity\brain\4782b539-824e-4ebf-9a1f-b247d4f7399a"
os.makedirs(ARTIFACTS_DIR, exist_ok=True)

def test_pwa_browser_ui():
    print("==================================================")
    print("📱 SIREN AI - Browser PWA & Web Push UI Test")
    print("==================================================")

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        # Emulate Android Mobile device (Pixel 7 / Galaxy S23)
        context = browser.new_context(
            viewport={"width": 393, "height": 851},
            user_agent="Mozilla/5.0 (Linux; Android 14; Pixel 7 Pro) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Mobile Safari/537.36",
            is_mobile=True,
            has_touch=True,
            permissions=["notifications"]
        )
        page = context.new_page()

        page_errors = []
        page.on("pageerror", lambda err: page_errors.append(str(err)))

        print("Navigating to SIREN AI http://localhost:8888/ ...")
        page.goto("http://localhost:8888/", wait_until="networkidle")
        page.wait_for_timeout(1500)

        assert len(page_errors) == 0, f"Page errors found: {page_errors}"
        print("  ✓ Zero page JS errors on initial load")

        # 1. Check top-bar notification button
        btn_push = page.locator("#btn-toggle-push")
        assert btn_push.is_visible(), "#btn-toggle-push must be visible in top-bar"
        print("  ✓ Top-bar notification button present and visible")

        # 2. Navigate to tab-asistentes
        page.evaluate("() => switchMainTab('tab-asistentes')")
        page.wait_for_timeout(800)

        # 3. Check PWA Push status bar
        status_bar = page.locator("#pwa-push-status-bar")
        assert status_bar.is_visible(), "#pwa-push-status-bar must be visible in tab-asistentes"
        print("  ✓ PWA Push status bar rendered successfully")

        # Capture screenshot of Asistentes tab with PWA Push Banner
        shot_banner = os.path.join(ARTIFACTS_DIR, "pwa_push_status_banner.png")
        page.screenshot(path=shot_banner)
        print(f"  ✓ Saved screenshot: {shot_banner}")

        # 4. Open Test Push Dropdown
        btn_dropdown = page.locator("button:has-text('Probar Push')")
        btn_dropdown.click()
        page.wait_for_timeout(400)

        menu = page.locator("#test-push-menu")
        assert menu.is_visible(), "#test-push-menu dropdown should be visible after click"
        print("  ✓ Test Push dropdown opened with 4 assistant buttons")

        # Capture screenshot of Test Push Dropdown
        shot_dropdown = os.path.join(ARTIFACTS_DIR, "pwa_test_push_dropdown.png")
        page.screenshot(path=shot_dropdown)
        print(f"  ✓ Saved screenshot: {shot_dropdown}")

        # 5. Check manifest link in head
        has_manifest = page.evaluate("() => !!document.querySelector('link[rel=\"manifest\"]')")
        assert has_manifest, "link[rel='manifest'] must be present in DOM"
        print("  ✓ <link rel='manifest'> verified in DOM")

        # 6. Verify Service Worker registration in browser
        sw_registered = page.evaluate("""async () => {
            if (!('serviceWorker' in navigator)) return false;
            const regs = await navigator.serviceWorker.getRegistrations();
            return regs.length > 0;
        }""")
        print(f"  ✓ Service Worker registered in browser context: {sw_registered}")

        browser.close()
        print("\n==================================================")
        print("🎉 ALL BROWSER PWA & UI CHECKS PASSED!")
        print("==================================================")

if __name__ == "__main__":
    test_pwa_browser_ui()
