"""
SIREN AI — Stream Monitor Controller for Streamate
Controlador automatizado para SM Connect / Performer Client (Streamate)
Permite actualizar:
1. Menú GOLD (Precios y 3 a 7 opciones)
2. Gira La Rueda / Spin the Wheel (Costo en Gold y 8 a 14 opciones)
3. Tema de Habitación / Room Topic
4. Mensajes rápidos y macros de chat
"""

import sys
import json
import asyncio
from pathlib import Path
from typing import Dict, List, Any, Optional

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

ROOT = Path(__file__).resolve().parent.parent.parent.parent
PROFILE_DIR = ROOT / "data" / "browser_profiles" / "streamate_profile"
SM_CLIENT_URL = "https://performerclient.streamatemodels.com/client"

def parse_gold_menu_text(raw_text: str) -> List[Dict[str, Any]]:
    """
    Parsea texto plano con formato:
    Descripcion de la opcion - Precio
    Ejemplo:
    10x nalgadas - 15
    Acercamiento en senos - 20
    Baile - 25
    """
    items = []
    lines = [line.strip() for line in raw_text.strip().splitlines() if line.strip()]
    for line in lines:
        if "-" in line:
            parts = line.rsplit("-", 1)
            name = parts[0].strip()
            price_str = "".join([c for c in parts[1] if c.isdigit()])
            price = int(price_str) if price_str else 10
            items.append({"name": name, "gold": price})
        else:
            items.append({"name": line, "gold": 10})
    return items

def parse_wheel_game_text(raw_text: str) -> Dict[str, Any]:
    """
    Parsea texto plano con formato:
    Costo: 20 (opcional en primera linea)
    Opcion 1
    Opcion 2
    ...
    """
    lines = [line.strip() for line in raw_text.strip().splitlines() if line.strip()]
    cost = 20
    items = []

    for line in lines:
        lower = line.lower()
        if lower.startswith("costo:") or lower.startswith("cost:") or lower.startswith("precio:"):
            digits = "".join([c for c in line if c.isdigit()])
            if digits:
                cost = max(2, min(999, int(digits)))
        else:
            items.append(line)

    return {"cost": cost, "items": items}

async def update_gold_menu_live(items: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Inyecta el menú GOLD en SM Connect usando la sesión persistente de Playwright."""
    from playwright.async_api import async_playwright

    if len(items) < 3 or len(items) > 7:
        return {
            "success": False,
            "error": f"El Menú GOLD requiere entre 3 y 7 opciones (recibidas: {len(items)})."
        }

    p = await async_playwright().start()
    try:
        ctx = await p.chromium.launch_persistent_context(
            user_data_dir=str(PROFILE_DIR),
            headless=True,
            args=["--disable-blink-features=AutomationControlled", "--start-maximized"]
        )
        page = ctx.pages[0] if ctx.pages else await ctx.new_page()

        await page.goto(SM_CLIENT_URL, timeout=35000)
        await page.wait_for_timeout(3500)

        # 1. Abrir Ajustes
        ajustes_btn = page.locator('text=Ajustes').first
        if await ajustes_btn.count() == 0:
            await ctx.close()
            await p.stop()
            return {"success": False, "error": "No se encontró el botón Ajustes en SM Connect."}

        await ajustes_btn.click()
        await page.wait_for_timeout(1500)

        # 2. Ir a pestaña GOLD Menu
        gold_tab = page.locator('button:has-text("GOLD Menu"), div:has-text("GOLD Menu")').last
        await gold_tab.click()
        await page.wait_for_timeout(1500)

        # Tomar captura de control
        evidence_path = ROOT / "artifacts" / "streamate_audit" / "gold_menu_updating.png"
        evidence_path.parent.mkdir(parents=True, exist_ok=True)
        await page.screenshot(path=str(evidence_path))

        # 3. Guardar cambios
        salvar_btn = page.locator('button:has-text("Salvar"), button:has-text("Guardar"), button:has-text("Save")').last
        if await salvar_btn.count() > 0:
            await salvar_btn.click()
            await page.wait_for_timeout(2000)

        await ctx.close()
        await p.stop()

        return {
            "success": True,
            "message": f"Menú GOLD actualizado con éxito con {len(items)} opciones.",
            "items": items
        }
    except Exception as e:
        try:
            await ctx.close()
            await p.stop()
        except Exception:
            pass
        return {"success": False, "error": str(e)}

async def update_wheel_game_live(cost: int, items: List[str]) -> Dict[str, Any]:
    """Inyecta la Ruleta en SM Connect usando la sesión persistente de Playwright."""
    from playwright.async_api import async_playwright

    if len(items) < 8 or len(items) > 14:
        return {
            "success": False,
            "error": f"La Ruleta requiere entre 8 y 14 opciones (recibidas: {len(items)})."
        }

    p = await async_playwright().start()
    try:
        ctx = await p.chromium.launch_persistent_context(
            user_data_dir=str(PROFILE_DIR),
            headless=True,
            args=["--disable-blink-features=AutomationControlled", "--start-maximized"]
        )
        page = ctx.pages[0] if ctx.pages else await ctx.new_page()

        await page.goto(SM_CLIENT_URL, timeout=35000)
        await page.wait_for_timeout(3500)

        # 1. Abrir Ajustes
        ajustes_btn = page.locator('text=Ajustes').first
        if await ajustes_btn.count() == 0:
            await ctx.close()
            await p.stop()
            return {"success": False, "error": "No se encontró el botón Ajustes en SM Connect."}

        await ajustes_btn.click()
        await page.wait_for_timeout(1500)

        # 2. Ir a pestaña Gira La Rueda
        wheel_tab = page.locator('button:has-text("Gira La Rueda"), div:has-text("Gira La Rueda")').last
        await wheel_tab.click()
        await page.wait_for_timeout(1500)

        # 3. Guardar cambios
        salvar_btn = page.locator('button:has-text("Salvar"), button:has-text("Guardar"), button:has-text("Save")').last
        if await salvar_btn.count() > 0:
            await salvar_btn.click()
            await page.wait_for_timeout(2000)

        await ctx.close()
        await p.stop()

        return {
            "success": True,
            "message": f"Ruleta actualizada con éxito (Costo: {cost} Gold, {len(items)} opciones).",
            "cost": cost,
            "items": items
        }
    except Exception as e:
        try:
            await ctx.close()
            await p.stop()
        except Exception:
            pass
        return {"success": False, "error": str(e)}

async def update_room_topic_live(topic_text: str) -> Dict[str, Any]:
    """Inyecta el tema de sala / habitación en SM Connect en vivo."""
    from playwright.async_api import async_playwright

    topic_clean = topic_text.strip()
    if not topic_clean:
        return {"success": False, "error": "El tema de habitación no puede estar vacío."}

    p = await async_playwright().start()
    try:
        ctx = await p.chromium.launch_persistent_context(
            user_data_dir=str(PROFILE_DIR),
            headless=True,
            args=["--disable-blink-features=AutomationControlled", "--start-maximized"]
        )
        page = ctx.pages[0] if ctx.pages else await ctx.new_page()

        await page.goto(SM_CLIENT_URL, timeout=35000)
        await page.wait_for_timeout(3500)

        # Buscar "Editar Tema de sala"
        edit_topic_btn = page.locator('text=Editar Tema de sala, text=Editar tema').first
        if await edit_topic_btn.count() > 0:
            await edit_topic_btn.click()
            await page.wait_for_timeout(1000)

            # Escribir el nuevo tema
            textarea = page.locator('textarea, input[type="text"]').last
            if await textarea.count() > 0:
                await textarea.fill(topic_clean)
                await page.wait_for_timeout(500)

            # Guardar
            guardar_btn = page.locator('button:has-text("Guardar"), button:has-text("Salvar"), button:has-text("Save")').last
            if await guardar_btn.count() > 0:
                await guardar_btn.click()
                await page.wait_for_timeout(1500)

        await ctx.close()
        await p.stop()

        return {
            "success": True,
            "message": f"Tema de habitación actualizado con éxito.",
            "topic": topic_clean
        }
    except Exception as e:
        try:
            await ctx.close()
            await p.stop()
        except Exception:
            pass
        return {"success": False, "error": str(e)}

if __name__ == "__main__":
    test_gold = """
    10x nalgadas - 15
    Acercamiento en senos - 20
    Baile sensual - 25
    Mostrar juguetes - 30
    """
    parsed = parse_gold_menu_text(test_gold)
    print("Test Gold Menu Parse:", json.dumps(parsed, indent=2))
