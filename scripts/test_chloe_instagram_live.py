import sys
import time
from playwright.sync_api import sync_playwright

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

def test_chloe_instagram():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        # Test mobile viewport
        context = browser.new_context(
            viewport={'width': 390, 'height': 844},
            user_agent='Mozilla/5.0 (iPhone; CPU iPhone OS 16_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.5 Mobile/15E148 Safari/604.1'
        )
        page = context.new_page()
        page.goto("http://localhost:8888", wait_until="domcontentloaded")
        page.wait_for_timeout(2000)

        # Navigate to tab-asistentes
        page.evaluate("() => switchMainTab('tab-asistentes')")
        page.wait_for_timeout(1000)

        # 1. Check overflow
        scroll_w = page.evaluate("() => document.documentElement.scrollWidth")
        print(f"Mobile scrollWidth: {scroll_w}px (max allowed: 390px)")
        assert scroll_w <= 390, f"Overflow detected: {scroll_w} > 390"

        # 2. Select Chloe
        chloe_card = page.locator("#card-assistant-chloe")
        if chloe_card.is_visible():
            chloe_card.click()
            page.wait_for_timeout(1000)
            print("✓ Card Chloe clickeada")

        # 3. Verify Chloe tools panel
        chloe_panel = page.locator("#panel-tools-chloe")
        assert chloe_panel.is_visible(), "El panel de Chloe no está visible"
        print("✓ Panel de herramientas de Chloe visible")

        # 4. Check feed container visibility
        feed_container = page.locator("#insta-view-feed-container")
        assert feed_container.is_visible(), "El contenedor de Captura en Vivo no está visible"
        print("✓ Captura en Vivo visible")

        # Take mobile screenshot of Chloe panel
        page.screenshot(path="artifacts/test_chloe_live_mobile_feed.png")
        print("✓ Captura guardada: artifacts/test_chloe_live_mobile_feed.png")

        # 5. Switch to grid view
        btn_grid = page.locator("#btn-insta-view-grid")
        btn_grid.click()
        page.wait_for_timeout(500)
        grid_container = page.locator("#insta-view-grid-container")
        assert grid_container.is_visible(), "El contenedor de Grid no está visible tras hacer click"
        print("✓ Perfil Interactivo visible tras switch")

        # Take screenshot of grid view
        page.screenshot(path="artifacts/test_chloe_live_mobile_grid.png")
        print("✓ Captura guardada: artifacts/test_chloe_live_mobile_grid.png")

        # Verify stats elements exist
        followers_text = page.locator("#insta-live-followers").inner_text()
        following_text = page.locator("#insta-live-following").inner_text()
        posts_text = page.locator("#insta-live-posts").inner_text()
        print(f"✓ Métricas en pantalla: {posts_text} posts, {followers_text} seguidores, {following_text} seguidos")

        # Check overflow again with panel open
        scroll_w_open = page.evaluate("() => document.documentElement.scrollWidth")
        print(f"Mobile scrollWidth con panel Chloe: {scroll_w_open}px")
        assert scroll_w_open <= 390, f"Overflow detected con Chloe: {scroll_w_open} > 390"

        # 6. Test on desktop viewport
        page.set_viewport_size({"width": 1440, "height": 900})
        page.wait_for_timeout(1000)
        page.screenshot(path="artifacts/test_chloe_live_desktop.png")
        print("✓ Captura Desktop guardada: artifacts/test_chloe_live_desktop.png")

        browser.close()
        print("🎉 TODOS LOS TESTS DE INTEGRACIÓN DE INSTAGRAM EN VIVO PASARON EXITOSAMENTE!")

if __name__ == "__main__":
    test_chloe_instagram()
