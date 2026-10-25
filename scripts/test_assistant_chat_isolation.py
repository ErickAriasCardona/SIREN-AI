import os
import sys
import time
from playwright.sync_api import sync_playwright

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

ARTIFACTS_DIR = r"C:\Users\MI PC\.gemini\antigravity\brain\4782b539-824e-4ebf-9a1f-b247d4f7399a"
os.makedirs(ARTIFACTS_DIR, exist_ok=True)

def test_chat_isolation():
    print("==================================================")
    print("🧪 Verificación de Aislamiento de Chat por Asistente")
    print("==================================================")

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(viewport={'width': 412, 'height': 915})
        page = context.new_page()

        # 1. Cargar la app
        page.goto("http://localhost:8888/", wait_until="networkidle")
        page.wait_for_timeout(1000)

        # 2. Navegar a Asistentes
        page.evaluate("() => switchMainTab('tab-asistentes')")
        page.wait_for_timeout(500)

        # 3. Seleccionar a CHLOE
        print("1. Seleccionando a CHLOE...")
        page.evaluate("() => selectAssistant('chloe')")
        page.wait_for_timeout(500)

        # 4. Enviar un mensaje de prueba específico para Chloe
        test_msg_chloe = "Chloe, prueba de aislamiento para Instagram @sambartonn23"
        print(f"2. Enviando mensaje a Chloe: '{test_msg_chloe}'...")
        
        # Simular envío a través del helper o la función appendChatMessage
        page.evaluate(f"""() => {{
            appendChatMessage('sam', '{test_msg_chloe}', 'es', 'test');
            appendChatMessage('chloe', '¡Hola Sam! Recibido en Chloe para Instagram. Esta respuesta pertenece exclusivamente a Chloe.', 'es', 'qwen2.5:7b-instruct');
        }}""")
        page.wait_for_timeout(500)

        # 5. Capturar pantalla de Chloe con el mensaje
        shot_chloe_before = os.path.join(ARTIFACTS_DIR, "test_chloe_chat_before_reload.png")
        page.screenshot(path=shot_chloe_before)
        print(f"  ✓ Captura guardada: {shot_chloe_before}")

        # 6. RECARGAR LA PÁGINA (el caso que reportó el usuario)
        print("3. Recargando la página...")
        page.reload(wait_until="networkidle")
        page.wait_for_timeout(1500)

        # Ir a la pestaña de asistentes si no estaba activa por defecto
        page.evaluate("() => switchMainTab('tab-asistentes')")
        page.wait_for_timeout(800)

        # 7. Verificar qué asistente está activo tras la recarga
        active_asst = page.evaluate("() => activeAssistant")
        print(f"4. Asistente activo tras recarga: {active_asst}")
        assert active_asst == "chloe", f"Se esperaba que Chloe siguiera activa, pero está: {active_asst}"
        print("  ✓ Chloe se mantiene como asistente activa tras la recarga")

        # 8. Verificar que el mensaje de Chloe sigue en el chat de Chloe
        chloe_chat_text = page.locator("#chat-messages-box").inner_text()
        assert test_msg_chloe in chloe_chat_text, "El mensaje de Chloe NO está en el chat de Chloe tras recargar"
        assert "Recibido en Chloe para Instagram" in chloe_chat_text, "La respuesta de Chloe no está en su chat"
        print("  ✓ Mensaje y respuesta intactos en el chat de Chloe tras la recarga")

        shot_chloe_after = os.path.join(ARTIFACTS_DIR, "test_chloe_chat_after_reload.png")
        page.screenshot(path=shot_chloe_after)

        # 9. Cambiar a ROXANNE y verificar que NO tiene el mensaje de Chloe
        print("5. Cambiando a ROXANNE...")
        page.evaluate("() => selectAssistant('roxanne')")
        page.wait_for_timeout(500)

        roxanne_chat_text = page.locator("#chat-messages-box").inner_text()
        assert test_msg_chloe not in roxanne_chat_text, f"ERROR: El mensaje de Chloe se filtró a Roxanne!"
        assert "Recibido en Chloe para Instagram" not in roxanne_chat_text, f"ERROR: La respuesta de Chloe se filtró a Roxanne!"
        print("  ✓ El chat de Roxanne está 100% libre de los mensajes de Chloe")

        shot_roxanne = os.path.join(ARTIFACTS_DIR, "test_roxanne_chat_isolated.png")
        page.screenshot(path=shot_roxanne)

        # 10. Cambiar a DIANA y ELECTRA para verificar aislamiento total
        page.evaluate("() => selectAssistant('diana')")
        page.wait_for_timeout(400)
        diana_chat_text = page.locator("#chat-messages-box").inner_text()
        assert test_msg_chloe not in diana_chat_text
        print("  ✓ El chat de Diana está 100% aislado")

        page.evaluate("() => selectAssistant('electra')")
        page.wait_for_timeout(400)
        electra_chat_text = page.locator("#chat-messages-box").inner_text()
        assert test_msg_chloe not in electra_chat_text
        print("  ✓ El chat de Electra está 100% aislado")

        browser.close()
        print("\n==================================================")
        print("🎉 AISLAMIENTO DE CHAT VALIDADO CON ÉXITO")
        print("==================================================")

if __name__ == "__main__":
    test_chat_isolation()
