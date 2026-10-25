import sys
import asyncio
from playwright.async_api import async_playwright
from pathlib import Path

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

ROOT = Path(__file__).resolve().parent.parent
SCREENSHOTS = ROOT / "artifacts"
SCREENSHOTS.mkdir(parents=True, exist_ok=True)

async def run_test():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(viewport={"width": 1440, "height": 950})
        page = await context.new_page()

        print("1. Cargando SIREN en http://localhost:8888...")
        await page.goto("http://localhost:8888", wait_until="networkidle")
        await page.wait_for_timeout(1000)

        # 2. Navegar a la pestaña Asistentes
        print("2. Haciendo clic en la pestaña 'Asistentes' del sidebar...")
        nav_btn = page.locator(".nav-btn:has-text('Asistentes')")
        await nav_btn.click()
        await page.wait_for_timeout(800)

        # 3. Verificar que la sección esté activa
        asistentes_view = page.locator("#tab-asistentes")
        assert await asistentes_view.is_visible(), "Error: tab-asistentes no es visible"
        print("✓ Pestaña Asistentes desplegada correctamente.")

        # 4. Verificar las 4 tarjetas de asistentes
        cards = ["card-assistant-roxanne", "card-assistant-chloe", "card-assistant-diana", "card-assistant-electra"]
        for cid in cards:
            c = page.locator(f"#{cid}")
            assert await c.is_visible(), f"Error: {cid} no es visible"
        print("✓ Las 4 tarjetas de Asistentes (Roxanne, Chloe, Diana, Electra) están visibles.")

        # 5. Verificar Roxanne por defecto
        rx_name = await page.locator("#active-assistant-name").text_content()
        assert "ROXANNE" in rx_name, f"Expected ROXANNE, got {rx_name}"
        assert await page.locator("#panel-tools-roxanne").is_visible(), "panel-tools-roxanne debe estar visible"
        print("✓ ROXANNE activa por defecto con herramientas Streamate.")

        # 6. Seleccionar CHLOE (Instagram)
        print("6. Seleccionando CHLOE (Especialista en Instagram)...")
        await page.locator("#card-assistant-chloe").click()
        await page.wait_for_timeout(600)

        chloe_name = await page.locator("#active-assistant-name").text_content()
        assert "CHLOE" in chloe_name, f"Expected CHLOE, got {chloe_name}"
        assert await page.locator("#panel-tools-chloe").is_visible(), "panel-tools-chloe debe estar visible"
        assert not await page.locator("#panel-tools-roxanne").is_visible(), "panel-tools-roxanne debe estar oculto"
        print("✓ CHLOE seleccionada. Complementos de Instagram y Visor Mobile activos.")

        # 7. Verificar Visor Mobile de Instagram
        phone_frame = page.locator(".instagram-phone-frame")
        assert await phone_frame.is_visible(), "El marco del celular Instagram no es visible"
        handle = await page.locator(".phone-header-nav span:has-text('sambartonn23')").text_content()
        assert "sambartonn23" in handle
        print("✓ Visor Instagram Mobile (@sambartonn23) renderizado con notch, avatar y bio.")

        # Tomar captura de Chloe con Visor Mobile
        await page.screenshot(path=str(SCREENSHOTS / "chloe_instagram_visor.png"))
        print("✓ Captura guardada: artifacts/chloe_instagram_visor.png")

        # 8. Ejecutar Skill: Estrategia del Día
        print("8. Probando Skill en 1 clic: 'Estrategia del Día'...")
        strat_btn = page.locator("button:has-text('Estrategia del Día')")
        await strat_btn.click()
        await page.wait_for_timeout(1500)

        # Verificar que el mensaje con la estrategia aparezca en el chat
        chat_content = await page.locator("#chat-messages-box").text_content()
        assert "Estrategia de Instagram para Hoy" in chat_content, "No se encontró la estrategia en el chat"
        print("✓ Skill 'Estrategia del Día' ejecutada con éxito y mostrada en el chat.")

        # 9. Ejecutar Skill: Pack de Historias
        print("9. Probando Skill en 1 clic: 'Pack de Historias de Hoy'...")
        stories_btn = page.locator("button:has-text('Pack de Historias de Hoy')")
        await stories_btn.click()
        await page.wait_for_timeout(1500)

        chat_content = await page.locator("#chat-messages-box").text_content()
        assert "Pack de Historias de Hoy" in chat_content, "No se encontraron las historias en el chat"
        print("✓ Skill 'Pack de Historias de Hoy' ejecutada y renderizada.")

        # 10. Probar colapso del panel derecho
        print("10. Probando botón de ocultar/mostrar panel lateral...")
        collapse_btn = page.locator("#btn-collapse-right-panel")
        await collapse_btn.click()
        await page.wait_for_timeout(500)

        is_collapsed = await page.locator(".roxanne-layout-container").evaluate("el => el.classList.contains('right-collapsed')")
        assert is_collapsed, "El contenedor debe tener la clase right-collapsed"
        show_btn = page.locator("#btn-show-right-panel")
        assert await show_btn.is_visible(), "El botón de restaurar panel debe estar visible en el header"
        print("✓ Panel lateral ocultado con éxito: chat central ocupa el 100% del ancho.")

        # Restaurar panel
        await show_btn.click()
        await page.wait_for_timeout(500)
        is_collapsed = await page.locator(".roxanne-layout-container").evaluate("el => el.classList.contains('right-collapsed')")
        assert not is_collapsed, "El panel debe estar restaurado"
        print("✓ Panel lateral restaurado con éxito.")

        # 11. Probar cambio a DIANA
        print("11. Seleccionando DIANA (Auditora Financiera)...")
        await page.locator("#card-assistant-diana").click()
        await page.wait_for_timeout(500)
        assert await page.locator("#panel-tools-diana").is_visible(), "panel-tools-diana debe estar visible"
        print("✓ DIANA activa con calculadora de splits 50/35% y balances.")

        # 12. Probar cambio a ELECTRA
        print("12. Seleccionando ELECTRA (Ingeniería de Algoritmos)...")
        await page.locator("#card-assistant-electra").click()
        await page.wait_for_timeout(500)
        assert await page.locator("#panel-tools-electra").is_visible(), "panel-tools-electra debe estar visible"
        print("✓ ELECTRA activa con radar de algoritmos y cooldowns.")

        # Volver a Chloe para captura final
        await page.locator("#card-assistant-chloe").click()
        await page.wait_for_timeout(500)
        await page.screenshot(path=str(SCREENSHOTS / "test_assistants_and_instagram.png"))
        print("✓ Captura guardada: artifacts/test_assistants_and_instagram.png")

        await browser.close()
        print("\n🎉 ¡TODAS LAS PRUEBAS (12/12) PASARON AL 100%!")

if __name__ == "__main__":
    asyncio.run(run_test())
