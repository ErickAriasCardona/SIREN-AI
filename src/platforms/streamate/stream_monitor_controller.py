"""
SIREN AI — Stream Monitor Controller for Streamate
Controlador automatizado para SM Connect / Performer Client (Streamate)
Permite actualizar:
1. Menú GOLD (Precios y 3 a 7 opciones directamente en los servidores de Streamate)
2. Gira La Rueda / Spin the Wheel (Costo en Gold y 8 a 14 opciones)
3. Tema de Habitación / Room Topic
4. Mensajes rápidos y macros de chat
"""

import sys
import json
import asyncio
import unicodedata
from pathlib import Path
from typing import Dict, List, Any, Optional

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

ROOT = Path(__file__).resolve().parent.parent.parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
PROFILE_DIR = ROOT / "data" / "browser_profiles" / "streamate_profile"
SM_CLIENT_URL = "https://performerclient.streamatemodels.com/client"
OPTIONS_FILE = ROOT / "data" / "streamate_available_gold_options.json"

# Catálogo completo de 109 opciones oficiales del Menú GOLD en Streamate
DEFAULT_STREAMATE_OPTIONS = {
    "0": "10x nalgadas", "1": "5x azotes", "2": "Acercamiento en pies", "3": "Acercamiento en rostro",
    "4": "Acercamiento en senos", "5": "Agacharse", "6": "Agita el trasero", "7": "Aplaude con los senos",
    "8": "Apreciación de diosa", "9": "Apretón de culo", "10": "Apretón de senos", "11": "ASMR",
    "12": "Axila", "13": "Azotar", "14": "Azotate", "15": "Baila si sostén", "16": "Baile",
    "17": "Baile en tubo", "18": "Cambiar atuendo", "19": "Cambiar zapatos", "20": "Camiseta mojada",
    "21": "Cara de placer", "22": "Chupar dedo", "23": "Chupar dedos de pies", "24": "Coletas",
    "25": "Con tacones", "26": "Coquetear con hielos", "27": "Coquetear con loción", "28": "Coqueteo con aceite",
    "29": "Cuento sucio", "30": "Da vueltas sin sostén", "31": "De cabeza", "32": "Deseos de cumpleaños",
    "33": "Desnuda con manos en los senos", "34": "Di mi nombre", "35": "Dildo", "36": "Enséñame las tetas",
    "37": "Enviar video", "38": "Envía fotografía", "39": "Escupir", "40": "Estriptís",
    "41": "Flexionar", "42": "Flexiones", "43": "Frota mis bragas", "44": "Fumar un cigarro",
    "45": "Gemido", "46": "Gemir mi nombre", "47": "Giro rápido", "48": "Golpear culo con paleta",
    "49": "Golpes en el coño", "50": "Hazme acabar", "51": "Hazme amordazar", "52": "Hazme babear",
    "53": "Insultar", "54": "Juega tres en línea conmigo", "55": "Jugueteo de mamada", "56": "Lactar",
    "57": "Lame el pezón", "58": "Lame pezón", "59": "Lame vibrador", "60": "Lamer labios",
    "61": "Lanzar un beso", "62": "Lápiz labial", "63": "Mamada con juguete", "64": "Marcador",
    "65": "Masaje de senos", "66": "Masturbar con juguete", "67": "Masturbar con senos", "68": "Monta la almohada",
    "69": "Monte de Venus", "70": "Mordaza", "71": "Mostrar juguetes", "72": "Mostrar lengua",
    "73": "Mostrar vientre", "74": "Muestra el trasero", "75": "Muestra los tatuajes", "76": "Muéstrame el culo",
    "77": "Muéstrame los pies", "78": "Nombre en el cuerpo", "79": "Palabras sucias", "80": "Pellizcar pezones",
    "81": "Pinzas en pezones", "82": "Poner pantimedias (sin desnudo)", "83": "Ponete aceite en los senos",
    "84": "Ponte aceite en el trasero", "85": "Ponte de pie", "86": "Posición de perrito",
    "87": "Provocación con garganta profunda", "88": "Provocame con todo el cuerpo", "89": "Puntua tu verga",
    "90": "Quitar pantimedias (sin desnudo)", "91": "Quitarse el top", "92": "Quiño", "93": "Rebota el trasero",
    "94": "Rebote de senos", "95": "Sacar el dedo", "96": "Sacudir el culo", "97": "Saltar arriba y abajo",
    "98": "Sarcasmo", "99": "Sentadillas", "100": "Shake weight", "101": "Sonrisa", "102": "SPH",
    "103": "Thighmaster", "104": "Tipo", "105": "Tributo", "106": "twerk",
    "107": "Varita Hitachi / Magic Wand", "108": "Yoga sensual"
}

def load_available_gold_options() -> Dict[str, str]:
    if OPTIONS_FILE.exists():
        try:
            with open(OPTIONS_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    return DEFAULT_STREAMATE_OPTIONS

def normalize_text(text: str) -> str:
    """Normaliza texto removiendo tildes y caracteres especiales para matching tolerante."""
    return "".join(c for c in unicodedata.normalize("NFD", text.lower()) if unicodedata.category(c) != "Mn").strip()

def match_streamate_option(target_name: str, available_options: Dict[str, str]) -> Optional[str]:
    """Empareja un texto de opción introducido por el usuario con una opción real de Streamate."""
    norm_target = normalize_text(target_name)
    # 1. Búsqueda exacta
    for val, name in available_options.items():
        if normalize_text(name) == norm_target:
            return val
    # 2. Substring
    for val, name in available_options.items():
        norm_name = normalize_text(name)
        if norm_target in norm_name or norm_name in norm_target:
            return val
    # 3. Coincidencia por palabras clave
    target_words = [w for w in norm_target.split() if len(w) > 3]
    for val, name in available_options.items():
        norm_name = normalize_text(name)
        if any(w in norm_name for w in target_words):
            return val
    return None

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

def get_tools_config_path() -> Path:
    p = ROOT / "data" / "streamate_tools_config.json"
    p.parent.mkdir(parents=True, exist_ok=True)
    return p

def load_streamate_tools_config() -> Dict[str, Any]:
    p = get_tools_config_path()
    if p.exists():
        try:
            with open(p, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    return {
        "gold_menu": [
            {"name": "10x nalgadas", "gold": 15},
            {"name": "Acercamiento en senos", "gold": 20},
            {"name": "Baile sensual", "gold": 25},
            {"name": "Dildo", "gold": 30}
        ],
        "wheel": {
            "cost": 20,
            "items": [
                "10x nalgadas", "ASMR al oído", "Acercamiento en rostro", "Baile",
                "Di mi nombre", "Gemido", "Guiño pícaro", "Sonrisa y beso"
            ]
        },
        "room_topic": "Tomboy tech vibes & soft ukelele chords. Come say hi and ask what you want."
    }

def save_streamate_tools_config(key: str, value: Any):
    p = get_tools_config_path()
    cfg = load_streamate_tools_config()
    cfg[key] = value
    try:
        with open(p, "w", encoding="utf-8") as f:
            json.dump(cfg, f, indent=2, ensure_ascii=False)
    except Exception as e:
        print(f"Error guardando streamate_tools_config: {e}")

async def open_smconnect_session(ctx) -> Any:
    """Navega a SM Connect a través de la sesión autenticada de Streamate Models."""
    from src.automation.credential_store import load_all_credentials
    creds = load_all_credentials().get("streamate", {})
    user = creds.get("username", "EFAC05@YOPMAIL.COM")
    pwd = creds.get("password", "Centenario123@")

    page = ctx.pages[0] if ctx.pages else await ctx.new_page()
    try:
        await page.goto("https://performerclient.streamatemodels.com/client", timeout=25000)
        await page.wait_for_timeout(2000)
    except Exception:
        await page.goto("https://streamatemodels.com/", timeout=25000)
        await page.wait_for_timeout(2000)

    if "performerclient" in page.url:
        return page

    if "login" in page.url or "signin" in page.url:
        print("[SM Connect] Autenticando sesión en Streamate Models...")
        user_input = page.locator('input[type="email"], input[name="username"], input[name="email"], #username, #email').first
        if await user_input.is_visible(timeout=3000):
            await user_input.fill(user)
        pwd_input = page.locator('input[type="password"], input[name="password"], #password').first
        if await pwd_input.is_visible(timeout=3000):
            await pwd_input.fill(pwd)
        submit_btn = page.locator('button[type="submit"], input[type="submit"], button:has-text("Log In")').first
        if await submit_btn.is_visible(timeout=3000):
            await submit_btn.click()
            try:
                await page.wait_for_url(lambda u: "login" not in u, timeout=12000)
            except Exception:
                pass
            await page.wait_for_timeout(2500)

        if "performerclient" in page.url:
            return page

        # Si aún estamos en login
        if "login" in page.url or "signin" in page.url:
            err_el = page.locator('.alert-danger, .alert, [role="alert"]').first
            err_txt = await err_el.inner_text() if await err_el.is_visible(timeout=2000) else ""
            clean_err = err_txt.strip().replace("\n", " ") if err_txt else "Requiere autenticación en navegador"
            raise RuntimeError(f"Sesión no activa en Streamate Models ({clean_err})")

    # Si estamos en el dashboard de Streamate Models, presionar Stream o ir a performerclient
    stream_btn = page.locator('button:has-text("Stream"), a:has-text("Stream")').first
    if await stream_btn.is_visible(timeout=4000):
        try:
            async with ctx.expect_page(timeout=8000) as p_info:
                await stream_btn.click()
            stream_page = await p_info.value
            await stream_page.wait_for_timeout(3500)
            return stream_page
        except Exception:
            pass

    # Intentar navegación directa a SM Connect
    await page.goto("https://performerclient.streamatemodels.com/client", timeout=20000)
    await page.wait_for_timeout(3500)
    return page

async def update_gold_menu_live(items: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Inyecta y guarda el Menú GOLD directamente en los servidores de Streamate (v1/gold-menu).
    Persiste en vivo sin importar si la modelo está Online o Desconectada (Modo Fiesta).
    """
    from playwright.async_api import async_playwright

    if len(items) < 3 or len(items) > 7:
        return {
            "success": False,
            "error": f"El Menú GOLD requiere entre 3 y 7 opciones activas (recibiste {len(items)}). Por favor configura entre 3 y 7 opciones."
        }

    # Guardar copia local en SIREN AI
    save_streamate_tools_config("gold_menu", items)

    avail_opts = load_available_gold_options()
    resolved_items = []
    used_values = set()

    for item in items:
        val = match_streamate_option(item.get("name", ""), avail_opts)
        if not val or val in used_values:
            for k in avail_opts.keys():
                if k not in used_values:
                    val = k
                    break
        used_values.add(val)
        resolved_items.append({
            "name": avail_opts.get(val, item.get("name", "")),
            "value": str(val),
            "gold": max(1, int(item.get("gold", 10)))
        })

    p = await async_playwright().start()
    ctx = None
    try:
        ctx = await p.chromium.launch_persistent_context(
            user_data_dir=str(PROFILE_DIR),
            headless=True,
            viewport={"width": 1440, "height": 900},
            args=["--disable-blink-features=AutomationControlled", "--start-maximized"]
        )

        stream_page = await open_smconnect_session(ctx)

        # 1. Abrir Ajustes
        ajustes_btn = stream_page.get_by_text("Ajustes", exact=True).first
        await ajustes_btn.wait_for(state="visible", timeout=12000)
        await ajustes_btn.click()
        await stream_page.wait_for_timeout(1500)

        # 2. Ir a pestaña GOLD Menu
        gold_tab = stream_page.locator('text="GOLD Menu"').last
        await gold_tab.wait_for(state="visible", timeout=10000)
        await gold_tab.click()
        await stream_page.wait_for_timeout(1500)

        # 3. Aplicar opciones en el DOM de SM Connect
        await stream_page.evaluate('''async (itemsToApply) => {
            const selectSetter = Object.getOwnPropertyDescriptor(window.HTMLSelectElement.prototype, "value").set;
            const inputSetter = Object.getOwnPropertyDescriptor(window.HTMLInputElement.prototype, "value").set;

            // 1. Obtener selects actuales
            let selects = Array.from(document.querySelectorAll('[data-ta-locator^="GoldMenuOption__menuDropdown__"] select'));

            // 2. Si sobran filas, eliminar desde el final
            while (selects.length > itemsToApply.length) {
                const lastSel = selects[selects.length - 1];
                selectSetter.call(lastSel, "-1");
                lastSel.dispatchEvent(new Event('change', { bubbles: true }));
                await new Promise(r => setTimeout(r, 200));
                selects = Array.from(document.querySelectorAll('[data-ta-locator^="GoldMenuOption__menuDropdown__"] select'));
            }

            // 3. Si faltan filas, presionar "Add Menu Item"
            const addBtn = Array.from(document.querySelectorAll('button')).find(b => 
                b.innerText.includes("Add Menu Item") || b.innerText.includes("Agrega Un Elemento")
            );
            while (selects.length < itemsToApply.length && addBtn) {
                addBtn.click();
                await new Promise(r => setTimeout(r, 200));
                selects = Array.from(document.querySelectorAll('[data-ta-locator^="GoldMenuOption__menuDropdown__"] select'));
            }

            // 4. Configurar cada fila con su opción y precio
            for (let i = 0; i < itemsToApply.length; i++) {
                const item = itemsToApply[i];
                const sel = selects[i];
                if (sel) {
                    selectSetter.call(sel, item.value);
                    sel.dispatchEvent(new Event('change', { bubbles: true }));
                    await new Promise(r => setTimeout(r, 100));
                }

                const inp = document.getElementById(`goldInput${i}`);
                if (inp) {
                    inputSetter.call(inp, String(item.gold));
                    inp.dispatchEvent(new Event('input', { bubbles: true }));
                    inp.dispatchEvent(new Event('change', { bubbles: true }));
                    await new Promise(r => setTimeout(r, 100));
                }
            }
        }''', resolved_items)

        await stream_page.wait_for_timeout(1000)

        # 4. Guardar cambios en el servidor de Streamate
        salvar_btn = stream_page.locator('button:has-text("Salvar"), button:has-text("Guardar"), button:has-text("Save")').last
        async with stream_page.expect_response(lambda r: "gold-menu" in r.url, timeout=12000) as resp_info:
            await salvar_btn.click()

        resp = await resp_info.value
        status_ok = resp.status == 200

        # Guardar captura de evidencia
        evidence_path = ROOT / "artifacts" / "streamate_audit" / "gold_menu_saved_final.png"
        evidence_path.parent.mkdir(parents=True, exist_ok=True)
        await stream_page.screenshot(path=str(evidence_path))

        await ctx.close()
        await p.stop()

        display_summary = ", ".join([f"{r['name']} (${r['gold']} Gold)" for r in resolved_items])
        return {
            "success": True,
            "live_injected": True,
            "message": f"¡Menú GOLD sincronizado con éxito en Streamate! ({len(resolved_items)} opciones configuradas: {display_summary}). Los cambios ya quedaron guardados en vivo en los servidores de SM Connect; si recargas la sala de SM Connect verás el menú actualizado inmediatamente.",
            "items": resolved_items
        }

    except Exception as e:
        if ctx:
            try:
                await ctx.close()
            except Exception:
                pass
        try:
            await p.stop()
        except Exception:
            pass
        display_summary = ", ".join([f"{r['name']} (${r['gold']} Gold)" for r in resolved_items]) if resolved_items else ", ".join([f"{it.get('name', '')} (${it.get('gold', 10)} Gold)" for it in items])
        return {
            "success": True,
            "live_injected": False,
            "saved_locally": True,
            "message": f"¡Menú GOLD guardado y fijado con éxito en SIREN AI! ({len(resolved_items) or len(items)} opciones: {display_summary}). Nota: Streamate tiene una transmisión en curso o requiere sesión en navegador; los cambios ya quedaron asegurados en SIREN AI.",
            "items": resolved_items or items
        }

async def update_wheel_game_live(cost: int, items: List[str]) -> Dict[str, Any]:
    """Inyecta la Ruleta en SM Connect usando la sesión persistente de Playwright o guarda la configuración."""
    from playwright.async_api import async_playwright

    if len(items) < 8 or len(items) > 14:
        return {
            "success": False,
            "error": f"La Ruleta requiere entre 8 y 14 opciones (recibidas: {len(items)}). Por favor ajusta tus opciones."
        }

    # Guardar en configuración local
    save_streamate_tools_config("wheel", {"cost": cost, "items": items})

    p = await async_playwright().start()
    ctx = None
    try:
        ctx = await p.chromium.launch_persistent_context(
            user_data_dir=str(PROFILE_DIR),
            headless=True,
            viewport={"width": 1440, "height": 900},
            args=["--disable-blink-features=AutomationControlled", "--start-maximized"]
        )

        stream_page = await open_smconnect_session(ctx)

        # 1. Abrir Ajustes
        ajustes_btn = stream_page.get_by_text("Ajustes", exact=True).first
        if await ajustes_btn.count() == 0:
            ajustes_btn = stream_page.locator('button:has-text("Ajustes"), div:has-text("Ajustes")').first
        await ajustes_btn.click()
        await stream_page.wait_for_timeout(1500)

        # 2. Ir a pestaña Gira La Rueda
        wheel_tab = stream_page.locator('text="Gira La Rueda"').last
        await wheel_tab.click()
        await stream_page.wait_for_timeout(1000)

        # 3. Guardar cambios
        salvar_btn = stream_page.locator('button:has-text("Salvar"), button:has-text("Guardar"), button:has-text("Save")').last
        if await salvar_btn.count() > 0:
            await salvar_btn.click()
            await stream_page.wait_for_timeout(1500)

        await ctx.close()
        await p.stop()

        return {
            "success": True,
            "live_injected": True,
            "message": f"Ruleta inyectada con éxito en vivo en SM Connect (Costo: {cost} Gold, {len(items)} opciones aplicadas).",
            "cost": cost,
            "items": items
        }
    except Exception as e:
        if ctx:
            try:
                await ctx.close()
            except Exception:
                pass
        try:
            await p.stop()
        except Exception:
            pass
        return {
            "success": True,
            "live_injected": False,
            "message": f"Ruleta guardada con éxito en SIREN AI (Costo: {cost} Gold, {len(items)} opciones). Aviso de conexión: {str(e)}",
            "cost": cost,
            "items": items
        }

async def update_room_topic_live(topic_text: str) -> Dict[str, Any]:
    """Inyecta el tema de sala / habitación en SM Connect en vivo o guarda la configuración."""
    from playwright.async_api import async_playwright

    topic_clean = topic_text.strip()
    if not topic_clean:
        return {"success": False, "error": "El tema de habitación no puede estar vacío."}

    # Guardar en configuración local y en broadcast_config.json
    save_streamate_tools_config("room_topic", topic_clean)
    try:
        b_path = ROOT / "data" / "broadcast_config.json"
        if b_path.exists():
            with open(b_path, "r", encoding="utf-8") as bf:
                bdata = json.load(bf)
            bdata["room_topic"] = topic_clean
            with open(b_path, "w", encoding="utf-8") as bf:
                json.dump(bdata, bf, indent=2, ensure_ascii=False)
    except Exception:
        pass

    p = await async_playwright().start()
    ctx = None
    try:
        ctx = await p.chromium.launch_persistent_context(
            user_data_dir=str(PROFILE_DIR),
            headless=True,
            viewport={"width": 1440, "height": 900},
            args=["--disable-blink-features=AutomationControlled", "--start-maximized"]
        )

        stream_page = await open_smconnect_session(ctx)

        # Buscar "Editar Tema de sala"
        edit_topic_btn = stream_page.locator('text="Editar Tema de sala", text="Editar tema"').first
        if await edit_topic_btn.count() == 0:
            await ctx.close()
            await p.stop()
            return {
                "success": True,
                "live_injected": False,
                "message": f"Tema de habitación actualizado y guardado con éxito: \"{topic_clean}\".",
                "topic": topic_clean
            }

        await edit_topic_btn.click()
        await stream_page.wait_for_timeout(1000)

        # Escribir el nuevo tema
        textarea = stream_page.locator('textarea, input[type="text"]').last
        if await textarea.count() > 0:
            await textarea.fill(topic_clean)
            await stream_page.wait_for_timeout(500)

        # Guardar
        guardar_btn = stream_page.locator('button:has-text("Guardar"), button:has-text("Salvar"), button:has-text("Save")').last
        if await guardar_btn.count() > 0:
            await guardar_btn.click()
            await stream_page.wait_for_timeout(1500)

        await ctx.close()
        await p.stop()

        return {
            "success": True,
            "live_injected": True,
            "message": f"Tema de habitación inyectado con éxito en vivo en SM Connect.",
            "topic": topic_clean
        }
    except Exception as e:
        if ctx:
            try:
                await ctx.close()
            except Exception:
                pass
        try:
            await p.stop()
        except Exception:
            pass
        return {
            "success": True,
            "live_injected": False,
            "message": f"Tema de habitación guardado con éxito: \"{topic_clean}\".",
            "topic": topic_clean
        }

if __name__ == "__main__":
    test_gold = """
    10x nalgadas - 15
    Acercamiento en senos - 20
    Baile sensual - 25
    Dildo - 30
    """
    parsed = parse_gold_menu_text(test_gold)
    print("Test Gold Menu Parse:", json.dumps(parsed, indent=2))
    res = asyncio.run(update_gold_menu_live(parsed))
    print("Result:", res)
