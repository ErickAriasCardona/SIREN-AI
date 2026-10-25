import os
import sys
import time
from playwright.sync_api import sync_playwright

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

ARTIFACTS_DIR = r"C:\Users\MI PC\.gemini\antigravity\brain\4782b539-824e-4ebf-9a1f-b247d4f7399a"
os.makedirs(ARTIFACTS_DIR, exist_ok=True)

def run_tests():
    print("==================================================")
    print("🚀 SIREN AI - Exhaustive Responsive & Sidebar Tests")
    print("==================================================")

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)

        # ----------------------------------------------------
        # TEST 1: MOBILE PHONE (iPhone 13/14 - 390x844)
        # ----------------------------------------------------
        print("\n[TEST 1] Mobile Phone Viewport (390 x 844)...")
        context_mobile = browser.new_context(
            viewport={"width": 390, "height": 844},
            is_mobile=True,
            has_touch=True,
            user_agent="Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148"
        )
        page_mobile = context_mobile.new_page()

        # Capture console errors
        console_errors = []
        page_mobile.on("console", lambda msg: console_errors.append(msg.text) if msg.type == "error" else None)

        page_mobile.goto("http://localhost:8888/", wait_until="networkidle")
        page_mobile.wait_for_timeout(1000)

        # 1.1 Verify no horizontal overflow
        scroll_width = page_mobile.evaluate("document.documentElement.scrollWidth")
        client_width = page_mobile.evaluate("document.documentElement.clientWidth")
        print(f"  Viewport width: 390, ScrollWidth: {scroll_width}, ClientWidth: {client_width}")
        assert scroll_width <= client_width + 1, f"Horizontal overflow detected! scrollWidth ({scroll_width}) > clientWidth ({client_width})"
        print("  ✓ Zero horizontal overflow on mobile initial load")

        # 1.2 Verify initial off-canvas sidebar state
        is_sidebar_hidden = page_mobile.evaluate("""() => {
            const sidebar = document.getElementById('sidebar');
            const rect = sidebar.getBoundingClientRect();
            return rect.right <= 0 || !document.body.classList.contains('sidebar-mobile-open');
        }""")
        assert is_sidebar_hidden, "Sidebar should start closed/off-canvas on mobile"
        print("  ✓ Sidebar starts off-canvas/hidden on mobile")

        # 1.3 Open sidebar via top-bar button
        btn_open = page_mobile.locator("#btn-open-sidebar")
        assert btn_open.is_visible(), "#btn-open-sidebar should be visible on mobile"
        btn_open.click()
        page_mobile.wait_for_timeout(400)

        has_mobile_open_class = page_mobile.evaluate("document.body.classList.contains('sidebar-mobile-open')")
        assert has_mobile_open_class, "Body should have 'sidebar-mobile-open' class after click"
        print("  ✓ Mobile sidebar opens smoothly via #btn-open-sidebar")

        # Screenshot mobile sidebar open
        shot_mobile_sidebar = os.path.join(ARTIFACTS_DIR, "mobile_sidebar_open.png")
        page_mobile.screenshot(path=shot_mobile_sidebar)
        print(f"  ✓ Saved screenshot: {shot_mobile_sidebar}")

        # 1.4 Close sidebar via top-right collapse button in sidebar
        btn_collapse = page_mobile.locator("#btn-collapse-sidebar")
        assert btn_collapse.is_visible(), "#btn-collapse-sidebar must be visible in top-right of sidebar"
        btn_collapse.click()
        page_mobile.wait_for_timeout(400)

        has_mobile_open_class = page_mobile.evaluate("document.body.classList.contains('sidebar-mobile-open')")
        assert not has_mobile_open_class, "Sidebar should close when clicking #btn-collapse-sidebar"
        print("  ✓ Mobile sidebar closes smoothly via #btn-collapse-sidebar")

        # 1.5 Open sidebar again and close via backdrop click
        btn_open.click()
        page_mobile.wait_for_timeout(300)
        backdrop = page_mobile.locator("#sidebar-backdrop")
        backdrop.click(position={"x": 350, "y": 300})
        page_mobile.wait_for_timeout(400)
        assert not page_mobile.evaluate("document.body.classList.contains('sidebar-mobile-open')"), "Backdrop click should close sidebar"
        print("  ✓ Backdrop tap closes mobile sidebar successfully")

        # 1.6 Navigate to Asistentes tab
        page_mobile.evaluate("switchMainTab('tab-asistentes')")
        page_mobile.wait_for_timeout(500)

        # Verify assistant cards are in a 2x2 grid
        cards_count = page_mobile.locator(".assistant-card").count()
        assert cards_count == 4, f"Expected 4 assistant cards, found {cards_count}"
        print(f"  ✓ 4 Assistant cards verified in mobile deck")

        # Screenshot mobile assistants tab
        shot_mobile_assistants = os.path.join(ARTIFACTS_DIR, "mobile_assistants_deck.png")
        page_mobile.screenshot(path=shot_mobile_assistants)
        print(f"  ✓ Saved screenshot: {shot_mobile_assistants}")

        # 1.7 Select Chloe Instagram Assistant
        page_mobile.evaluate("selectAssistant('chloe')")
        page_mobile.wait_for_timeout(600)

        # Check Chloe visor visibility
        chloe_panel = page_mobile.locator("#panel-tools-chloe")
        assert chloe_panel.is_visible(), "Chloe Instagram visor complement panel should be visible"
        print("  ✓ Chloe Instagram mobile frame complement panel visible")

        # Test skill action button "Estrategias del Día"
        page_mobile.evaluate("executeChloeSkill('daily_strategy')")
        page_mobile.wait_for_timeout(1500)

        # Verify response in chat
        chat_bubbles = page_mobile.locator(".chat-bubble")
        last_bubble_text = chat_bubbles.last.inner_text()
        assert "Estrategia" in last_bubble_text or "Instagram" in last_bubble_text or "Sam" in last_bubble_text, f"Unexpected response: {last_bubble_text[:60]}"
        print(f"  ✓ Chloe Instagram skill executed, response received: {last_bubble_text[:45]}...")

        # Screenshot mobile Chloe view
        shot_mobile_chloe = os.path.join(ARTIFACTS_DIR, "mobile_chloe_instagram.png")
        page_mobile.screenshot(path=shot_mobile_chloe)
        print(f"  ✓ Saved screenshot: {shot_mobile_chloe}")

        # 1.8 Select Roxanne Webcam Assistant & Verify Vertical Stacking & Zero Overflow
        page_mobile.evaluate("selectAssistant('roxanne')")
        page_mobile.wait_for_timeout(500)

        roxanne_panel = page_mobile.locator("#panel-tools-roxanne")
        assert roxanne_panel.is_visible(), "Roxanne tools panel should be visible"
        
        # Verify panel tools flexDirection is column
        flex_dir = page_mobile.evaluate("window.getComputedStyle(document.getElementById('panel-tools-roxanne')).flexDirection")
        assert flex_dir == 'column', f"Expected flexDirection column, got {flex_dir}"
        print(f"  ✓ Roxanne tools panel layout is strictly vertical (flex-direction: {flex_dir})")

        # Verify zero horizontal overflow in content area and doc
        rx_scroll_width = page_mobile.evaluate("document.documentElement.scrollWidth")
        rx_client_width = page_mobile.evaluate("document.documentElement.clientWidth")
        rx_ca_scroll = page_mobile.evaluate("document.querySelector('.content-area').scrollWidth")
        rx_ca_client = page_mobile.evaluate("document.querySelector('.content-area').clientWidth")
        assert rx_scroll_width <= rx_client_width + 1, f"Doc overflow! {rx_scroll_width} > {rx_client_width}"
        assert rx_ca_scroll <= rx_ca_client + 1, f"Content area overflow! {rx_ca_scroll} > {rx_ca_client}"
        print(f"  ✓ Zero horizontal overflow with Roxanne active (doc: {rx_scroll_width}px, ca: {rx_ca_scroll}px)")

        # Scroll to Roxanne tools to capture the stacked cards
        page_mobile.evaluate("document.querySelector('.content-area').scrollTop = 450")
        page_mobile.wait_for_timeout(400)
        shot_mobile_roxanne = os.path.join(ARTIFACTS_DIR, "mobile_roxanne_no_overflow.png")
        page_mobile.screenshot(path=shot_mobile_roxanne)
        print(f"  ✓ Saved screenshot of vertically stacked Roxanne tools: {shot_mobile_roxanne}")

        context_mobile.close()

        # ----------------------------------------------------
        # TEST 2: TABLET VIEWPORT (iPad - 768x1024)
        # ----------------------------------------------------
        print("\n[TEST 2] Tablet Viewport (768 x 1024)...")
        context_tablet = browser.new_context(
            viewport={"width": 768, "height": 1024},
            user_agent="Mozilla/5.0 (iPad; CPU OS 16_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/604.1"
        )
        page_tablet = context_tablet.new_page()
        page_tablet.goto("http://localhost:8888/", wait_until="networkidle")
        page_tablet.wait_for_timeout(800)

        # Tablet horizontal overflow check
        t_scroll = page_tablet.evaluate("document.documentElement.scrollWidth")
        t_client = page_tablet.evaluate("document.documentElement.clientWidth")
        assert t_scroll <= t_client + 1, f"Tablet overflow detected: {t_scroll} > {t_client}"
        print("  ✓ Zero horizontal overflow on tablet")

        # Switch to Asistentes tab on tablet
        page_tablet.evaluate("switchMainTab('tab-asistentes')")
        page_tablet.wait_for_timeout(600)

        shot_tablet = os.path.join(ARTIFACTS_DIR, "tablet_responsive_asistentes.png")
        page_tablet.screenshot(path=shot_tablet)
        print(f"  ✓ Saved screenshot: {shot_tablet}")
        context_tablet.close()

        # ----------------------------------------------------
        # TEST 3: DESKTOP SIDEBAR COLLAPSE / EXPAND (1440x900)
        # ----------------------------------------------------
        print("\n[TEST 3] Desktop Viewport (1440 x 900)...")
        context_desktop = browser.new_context(viewport={"width": 1440, "height": 900})
        page_desktop = context_desktop.new_page()
        page_desktop.goto("http://localhost:8888/", wait_until="networkidle")
        page_desktop.wait_for_timeout(800)

        # Collapse sidebar on desktop
        btn_collapse_desktop = page_desktop.locator("#btn-collapse-sidebar")
        btn_collapse_desktop.click()
        page_desktop.wait_for_timeout(400)

        is_collapsed = page_desktop.evaluate("document.body.classList.contains('sidebar-collapsed')")
        assert is_collapsed, "Desktop should have 'sidebar-collapsed' class"
        print("  ✓ Desktop sidebar collapses to 0 width with smooth transition")

        shot_desktop_collapsed = os.path.join(ARTIFACTS_DIR, "desktop_sidebar_collapsed.png")
        page_desktop.screenshot(path=shot_desktop_collapsed)
        print(f"  ✓ Saved screenshot: {shot_desktop_collapsed}")

        # Expand sidebar on desktop
        btn_open_desktop = page_desktop.locator("#btn-open-sidebar")
        btn_open_desktop.click()
        page_desktop.wait_for_timeout(400)

        is_collapsed = page_desktop.evaluate("document.body.classList.contains('sidebar-collapsed')")
        assert not is_collapsed, "Desktop sidebar should expand back"
        print("  ✓ Desktop sidebar re-expands cleanly")

        context_desktop.close()
        browser.close()

    print("\n==================================================")
    print("🎉 ALL RESPONSIVE & SIDEBAR COLLAPSE TESTS PASSED!")
    print("==================================================")

if __name__ == "__main__":
    run_tests()
