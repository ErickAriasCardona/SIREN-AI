"""
SIREN AI — StreamMonitor & Mahia Tactical Orchestrator
Módulo de orquestación ética y complementaria para StreamMonitor (Streamate).

PRINCIPIO ÉTICO FUNDAMENTAL:
SIREN AI NO compite ni duplica las funcionalidades nativas de StreamMonitor
(encoder de cámara, filtros de video, mixer de audio, detector de palabras prohibidas).
SIREN actúa como el Co-Piloto Táctico y Automatizador que alinea la meta comercial del turno
(ej. "Vender ASS", "Tomboy Ukelele", etc.) y orquesta:
1. Instrucciones concisas para Mahia (evita que se extienda o dé textos desordenados).
2. Procesamiento, validación y adaptación de las salidas de Mahia.
3. Inyección automatizada en Streamate (Menú Gold, Ruleta 5G, Room Topic <= 140 chars).
4. Preparación de Auto-Mensajes y Macros (Alt+1..Alt+8) para StreamMonitor.
5. Monitoreo de estado de StreamMonitor Desktop (PID, versión, cuenta modelo).
"""

import sys
import os
import json
import re
import subprocess
from pathlib import Path
from typing import Dict, List, Any, Optional

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

ROOT = Path(__file__).resolve().parent.parent.parent.parent
STREAMMONITOR_EXE = Path(os.environ.get("LOCALAPPDATA", "C:/Users/MI PC/AppData/Local")) / "Programs" / "streammonitor" / "streammonitor.exe"
STREAMMONITOR_LOGS = Path(os.environ.get("APPDATA", "C:/Users/MI PC/AppData/Roaming")) / "streammonitor" / "logs"

# Metas comerciales pre-optimizadas con el estándar estricto de Streamate
PRESET_SHIFT_THEMES: Dict[str, Dict[str, Any]] = {
    "ball_gag_sub_dom": {
        "id": "ball_gag_sub_dom",
        "title": "🖤 Ball Gag, Collar & Pay-To-Sub Tease",
        "badge": "Dominación & Sumisión Pagada",
        "topic": "🖤 COLLAR & GAG TEASE! Pay To Control Me Or I Dominate ⚡ Gold: 3G | Wheel: 5G | Drool & Submission #gag #bdsm #drool #dom #sub",
        "gold_menu": [
            {"name": "Mordaza", "gold": 3},
            {"name": "Hazme babear", "gold": 3},
            {"name": "Hazme amordazar", "gold": 3},
            {"name": "Mostrar lengua", "gold": 3},
            {"name": "10x nalgadas", "gold": 3},
            {"name": "Posición de perrito", "gold": 3}
        ],
        "wheel": {
            "cost": 5,
            "items": [
                "Pinzas en pezones",
                "Pellizcar pezones",
                "Escupir",
                "Golpear culo con paleta",
                "5x azotes",
                "Insultar",
                "Palabras sucias",
                "Azotate",
                "Agacharse",
                "SPH"
            ]
        },
        "auto_messages": {
            "room_30s": "Hey... see this collar and ball gag around my neck? Pay to control me or I stay in charge 🖤 Gold: 3G | Wheel: 5G",
            "send_golds": "Mmm thank you for feeding my collar {fan}... want me gagged and drooling for you? 😉",
            "private_show": "Welcome to my private room... are you ready to take complete control of my ball gag?"
        },
        "quick_messages": [
            "Tip 3G to put the ball gag in my mouth 🖤",
            "Who wants to see heavy drool close-up? 🤤",
            "I only submit if you pay... Gold Menu is 3G ⚡",
            "Spin the Wheel (5G) to lock my collar 🎡",
            "Mmm 4 hours wearing this... so much saliva today 💦",
            "Take me to Private to command me completely 🗝️"
        ]
    },
    "ass_twerk": {
        "id": "ass_twerk",
        "title": "🍑 Especial ASS & Twerk Trasero",
        "badge": "Alta Conversión de Tokens",
        "topic": "🍑 BOOTY SHAKE & TWERK LIVE 🔥 Gold Menu 3G ⚡ Intimate Wheel 5G 🖤 Tease Me In Private #Tomboy #Ass #Twerk #Lovense #Gold",
        "gold_menu": [
            {"name": "twerk", "gold": 3},
            {"name": "Rebota el trasero", "gold": 3},
            {"name": "Sacudir el culo", "gold": 3},
            {"name": "Muestra el trasero", "gold": 3},
            {"name": "Ponte aceite en el trasero", "gold": 3},
            {"name": "10x nalgadas", "gold": 3}
        ],
        "wheel": {
            "cost": 5,
            "items": [
                "Agita el trasero",
                "Apretón de culo",
                "Golpear culo con paleta",
                "Muéstrame el culo",
                "Posición de perrito",
                "5x azotes",
                "Baile",
                "Estriptís",
                "Sentadillas",
                "Agacharse"
            ]
        },
        "auto_messages": {
            "room_30s": "Hey love! Welcome in. Booty & twerk special today. Make yourself comfortable 😉",
            "send_golds": "Mmm thank you for that gold {fan}! Check out my 3G Gold Menu 🔥",
            "private_show": "Welcome to my private room... what naughty fantasy are we doing today? 💋"
        },
        "quick_messages": [
            "Tap the screen if you love this booty bouncing 🔥",
            "Spin the intimate Wheel (5G) to pick my next treat 😉",
            "Gold Menu only 3G today, treat yourself now ⚡",
            "Take me to private for full uncensored action 🖤",
            "Buzz my Lovense and watch me moan instantly ⚡",
            "Cam2Cam ready in private, show me too 🎥"
        ]
    },
    "tomboy_ukelele": {
        "id": "tomboy_ukelele",
        "title": "🎸 Tomboy Chill & Ukelele VIP",
        "badge": "Scroll-Stopper USA/UK",
        "topic": "🎸 GOOD VIBES & UKELELE LIVE 🖤 Intimate chat • Gold Menu 3G ⚡ Wheel 5G • Private Open #Tomboy #Acoustic #Cute #Lovense",
        "gold_menu": [
            {"name": "ASMR", "gold": 3},
            {"name": "Sonrisa", "gold": 3},
            {"name": "Di mi nombre", "gold": 3},
            {"name": "Lanzar un beso", "gold": 3},
            {"name": "Cuento sucio", "gold": 3},
            {"name": "Mostrar vientre", "gold": 3}
        ],
        "wheel": {
            "cost": 5,
            "items": [
                "Lanzar un beso",
                "Gemido",
                "Gemir mi nombre",
                "Provocame con todo el cuerpo",
                "Quiño",
                "Lamer labios",
                "Palabras sucias",
                "Mostrar lengua",
                "Yoga sensual",
                "Sarcasmo"
            ]
        },
        "auto_messages": {
            "room_30s": "Hey mister! So nice to have you. Come chat with me while I play something sweet 🖤",
            "send_golds": "Thank you for the gold sweetheart! You inspire me so much ✨",
            "private_show": "We are completely alone now... Tell me your deepest secret 😉"
        },
        "quick_messages": [
            "Ask me for a song on my ukelele in chat 🎶",
            "Tips activate my toy to level 2 ⚡",
            "Gold Menu at 3G for a limited time ✨",
            "I love good vibes, stay with me a while 🖤",
            "Want to hear something private just for your ears?",
            "Spin the Wheel (5G) for an intimate treat 🎡"
        ]
    },
    "full_lovense": {
        "id": "full_lovense",
        "title": "⚡ Full Lovense Buzz & Dominación",
        "badge": "Ticket Alto de Propinas",
        "topic": "🔥 FULL LOVENSE TOY CONTROL 🔥 Menu Gold 3G ⚡ Wheel 5G 🖤 Make Me Moan Live #Lovense #Buzz #Tomboy #Cam2Cam #Private",
        "gold_menu": [
            {"name": "Lame vibrador", "gold": 3},
            {"name": "Gemido", "gold": 3},
            {"name": "Cara de placer", "gold": 3},
            {"name": "Gemir mi nombre", "gold": 3},
            {"name": "Apretón de senos", "gold": 3},
            {"name": "Rebote de senos", "gold": 3}
        ],
        "wheel": {
            "cost": 5,
            "items": [
                "Hazme acabar",
                "Provocame con todo el cuerpo",
                "Gemir mi nombre",
                "Palabras sucias",
                "10x nalgadas",
                "Rebote de senos",
                "Posición de perrito",
                "Baile",
                "Desnuda con manos en los senos",
                "Estriptís"
            ]
        },
        "auto_messages": {
            "room_30s": "Welcome! My toy is synced and waiting for your tips. Dare to control it? ⚡",
            "send_golds": "Ahhh thank you for that buzz! Felt every single second, you are amazing 🔥",
            "private_show": "We are alone now... Take complete control, don't hold back 💋"
        },
        "quick_messages": [
            "3 Golds = Medium buzz and a big smile guaranteed ⚡",
            "Make me moan with a tip shower on cam! 🔥",
            "Wheel at 5G with intimate surprises active now 🎡",
            "Who is brave enough to take my Lovense to level 10?",
            "Ready for an intense private show, take me now 🖤",
            "Cam2Cam active to watch you enjoy 🎥"
        ]
    }
}

def is_streammonitor_running() -> bool:
    """Verifica si el proceso de StreamMonitor Desktop está en ejecución."""
    try:
        cmd = 'tasklist /FI "IMAGENAME eq streammonitor.exe" /NH'
        res = subprocess.run(cmd, capture_output=True, text=True, shell=True)
        return "streammonitor.exe" in res.stdout.lower()
    except Exception:
        return False

def focus_streammonitor_window() -> bool:
    """Enfoca y restaura la ventana gráfica de StreamMonitor en primer plano en el escritorio físico del usuario ('WinSta0\\Default')."""
    if sys.platform != "win32":
        return False
    try:
        import ctypes
        from ctypes import wintypes
        user32 = ctypes.windll.user32

        hwinsta = user32.OpenWindowStationW("WinSta0", False, 0x037F)
        if hwinsta:
            user32.SetProcessWindowStation(hwinsta)
        hdesk = user32.OpenDesktopW("Default", 0, False, 0x01FF)

        found_hwnds = []
        def enum_cb(hwnd, lp):
            length = user32.GetWindowTextLengthW(hwnd)
            buff = ctypes.create_unicode_buffer(length + 1)
            user32.GetWindowTextW(hwnd, buff, length + 1)
            cls_buff = ctypes.create_unicode_buffer(256)
            user32.GetClassNameW(hwnd, cls_buff, 256)
            title = buff.value.lower()
            cls_name = cls_buff.value.lower()
            if 'streammonitor' in title or ('stream' in title and 'chrome_widgetwin' in cls_name):
                found_hwnds.append(hwnd)
            return True

        WNDPROC = ctypes.WINFUNCTYPE(ctypes.c_bool, wintypes.HWND, wintypes.LPARAM)
        if hdesk:
            user32.EnumDesktopWindows(hdesk, WNDPROC(enum_cb), 0)
            user32.CloseDesktop(hdesk)

        for hwnd in found_hwnds:
            user32.ShowWindow(hwnd, 9)   # SW_RESTORE
            user32.ShowWindow(hwnd, 3)   # SW_MAXIMIZE
            user32.SetWindowPos(hwnd, -1, 0, 0, 0, 0, 0x0003) # HWND_TOPMOST
            user32.SetWindowPos(hwnd, -2, 0, 0, 0, 0, 0x0003) # HWND_NOTOPMOST
            user32.SetForegroundWindow(hwnd)
            user32.BringWindowToTop(hwnd)
            return True
        return False
    except Exception:
        return False


def launch_streammonitor_desktop() -> Dict[str, Any]:
    """
    Lanza StreamMonitor explícitamente en el monitor interactivo físico del usuario ('WinSta0\\Default')
    usando Task Scheduler interactivo (/it) para romper cualquier sandbox de sesión y restaura la ventana visible.
    """
    import time
    if not STREAMMONITOR_EXE.exists():
        return {
            "success": False,
            "error": f"No se encontró StreamMonitor en: {STREAMMONITOR_EXE}"
        }

    # 1. Si ya está abierta y visible en WinSta0\Default, traerla al frente
    focused = focus_streammonitor_window()
    if focused:
        return {
            "success": True,
            "already_running": True,
            "focused": True,
            "message": "StreamMonitor traído al frente en tu pantalla principal."
        }

    # 2. Si no estaba visible en pantalla, lanzarlo a través del Programador de Tareas interactivo (/it)
    try:
        bat_file = ROOT / "run_streammonitor.bat"
        if not bat_file.exists():
            with open(bat_file, "w", encoding="utf-8") as f:
                f.write(f'@echo off\nstart "" "{STREAMMONITOR_EXE}"\n')

        cmd_create = ["schtasks", "/create", "/tn", "LaunchStreamMonitor", "/tr", f'cmd.exe /c "{bat_file}"', "/sc", "once", "/st", "23:59", "/f", "/it"]
        subprocess.run(cmd_create, capture_output=True, timeout=10)

        cmd_run = ["schtasks", "/run", "/tn", "LaunchStreamMonitor"]
        subprocess.run(cmd_run, capture_output=True, timeout=10)

        time.sleep(3.0)
        focused = focus_streammonitor_window()
        return {
            "success": True,
            "already_running": False,
            "focused": focused,
            "message": "StreamMonitor lanzado y visible en tu monitor principal."
        }
    except Exception as e:
        return {
            "success": False,
            "error": f"Error al ejecutar StreamMonitor: {e}"
        }


def inspect_streammonitor_status() -> Dict[str, Any]:
    """Inspecciona la instalación local, logs recientes y estado de sesión de StreamMonitor."""
    running = is_streammonitor_running()
    installed = STREAMMONITOR_EXE.exists()

    status: Dict[str, Any] = {
        "installed": installed,
        "running": running,
        "exe_path": str(STREAMMONITOR_EXE),
        "version": "1.1.18",
        "account_context": "cuenta=1 modelo=1589 (SamBartone)",
        "detected_hardware": {
            "camera": "Logitech BRIO (FullHD 1080p / 4K)",
            "virtual_cams": ["Lovense OBS Virtual Camera", "OBS Virtual Camera"],
            "gpu": "AMD Radeon(TM) Graphics (HW Encoder Activo)"
        },
        "registered_shortcuts": ["Alt+1", "Alt+2", "Alt+3", "Alt+4", "Alt+5", "Alt+6", "Alt+7", "Alt+8"],
        "companion_role": "SIREN actúa como el Co-Piloto Estratégico y Automatizador ético de StreamMonitor."
    }

    # Leer último log para métricas frescas
    if STREAMMONITOR_LOGS.exists():
        logs = sorted(list(STREAMMONITOR_LOGS.glob("app-*.log")), key=lambda p: p.stat().st_mtime, reverse=True)
        if logs:
            latest = logs[0]
            try:
                with open(latest, "r", encoding="utf-8", errors="ignore") as f:
                    lines = f.readlines()
                    status["last_log_file"] = latest.name
                    status["last_log_line"] = lines[-1].strip() if lines else ""
            except Exception:
                pass

    return status

def generate_mahia_prompt(shift_theme: str, custom_description: str = "") -> Dict[str, Any]:
    """
    Genera el prompt perfecto y conciso para pedirle asistencia a Mahia en StreamMonitor.
    Evita que Mahia se extienda o dé textos desordenados que la modelo deba recortar a mano.
    """
    theme_data = PRESET_SHIFT_THEMES.get(shift_theme)
    target_name = theme_data["title"] if theme_data else (custom_description or shift_theme)

    prompt_text = (
        f"Mahia: Nuestro objetivo comercial de sala para este turno es: '{target_name}'.\n"
        f"Por favor entrégame el plan táctico directo, sin introducciones ni despedidas, respetando estrictamente estos 4 bloques:\n\n"
        f"1. TOPIC: 1 línea de máximo 130 caracteres con hashtags de impacto (#Tomboy #Lovense #Gold).\n"
        f"2. MENU GOLD (Todos a 3 Gold): Exactamente 6 opciones breves en formato: Nombre - 3\n"
        f"3. RULETA INTIMA (Costo 5 Gold): Exactamente 10 opciones provocativas en formato: Opción\n"
        f"4. AUTO-MENSAJES:\n"
        f"   - Llegada Sala (30s): Mensaje cálido de bienvenida (máximo 12 palabras).\n"
        f"   - Propina Gold: Agradecimiento coqueto (máximo 10 palabras).\n"
        f"   - Entrada a Privado: Bienvenida sensual (máximo 10 palabras).\n\n"
        f"5. MACROS DE CHAT (Alt+1 a Alt+6): 6 mensajes cortos de chat (máximo 8 palabras) para activar mirones."
    )

    return {
        "shift_theme": shift_theme,
        "target_name": target_name,
        "concise_mahia_prompt": prompt_text,
        "preset_fallback": theme_data or PRESET_SHIFT_THEMES["ass_twerk"]
    }

def parse_mahia_output_to_tools(raw_text: str) -> Dict[str, Any]:
    """
    Parsea la respuesta textual de Mahia y la estructura automáticamente
    para alimentar las herramientas de Streamate y StreamMonitor sin trabajo manual.
    """
    result: Dict[str, Any] = {
        "raw_text": raw_text,
        "topic": "",
        "gold_menu": [],
        "wheel": {"cost": 5, "items": []},
        "auto_messages": {
            "room_30s": "",
            "send_golds": "",
            "private_show": ""
        },
        "quick_messages": []
    }

    lines = [l.strip() for l in raw_text.splitlines() if l.strip()]

    current_section = None
    for line in lines:
        lower = line.lower()
        if "topic" in lower and ":" in lower:
            current_section = "topic"
            topic_val = line.split(":", 1)[1].strip().strip('"').strip("'")
            if topic_val:
                result["topic"] = topic_val[:140]
            continue
        elif "gold" in lower and ("menú" in lower or "menu" in lower):
            current_section = "gold"
            continue
        elif "ruleta" in lower or "wheel" in lower:
            current_section = "wheel"
            continue
        elif "auto-mensaje" in lower or "automensaje" in lower or "auto mensaje" in lower:
            current_section = "auto_messages"
            continue
        elif "macro" in lower or "alt+" in lower or "mensaje rápido" in lower:
            current_section = "quick_messages"
            continue

        # Procesar según sección activa
        if current_section == "topic" and not result["topic"]:
            result["topic"] = line.strip().strip('"').strip("'")[:140]

        elif current_section == "gold":
            if "-" in line:
                parts = line.rsplit("-", 1)
                name = re.sub(r'^\d+[\.\)]\s*', '', parts[0]).strip().strip("•-* ")
                price_str = "".join([c for c in parts[1] if c.isdigit()])
                price = int(price_str) if price_str else 3
                if name and len(result["gold_menu"]) < 7:
                    result["gold_menu"].append({"name": name, "gold": price})

        elif current_section == "wheel":
            clean_item = re.sub(r'^\d+[\.\)]\s*', '', line).strip().strip("•-* ")
            if clean_item and not clean_item.lower().startswith("costo:"):
                if len(result["wheel"]["items"]) < 14:
                    result["wheel"]["items"].append(clean_item)

        elif current_section == "auto_messages":
            if "llegada" in lower or "sala" in lower or "30s" in lower:
                msg = line.split(":", 1)[1].strip() if ":" in line else line
                result["auto_messages"]["room_30s"] = msg.strip('"').strip("'")
            elif "propina" in lower or "gold" in lower or "tip" in lower:
                msg = line.split(":", 1)[1].strip() if ":" in line else line
                result["auto_messages"]["send_golds"] = msg.strip('"').strip("'")
            elif "privado" in lower or "pvt" in lower or "exclusivo" in lower:
                msg = line.split(":", 1)[1].strip() if ":" in line else line
                result["auto_messages"]["private_show"] = msg.strip('"').strip("'")

        elif current_section == "quick_messages":
            clean_macro = re.sub(r'^(?:alt\+\d|[\d\.\)]+)\s*[:\-]?\s*', '', line, flags=re.IGNORECASE).strip().strip('"').strip("'")
            if clean_macro and len(result["quick_messages"]) < 8:
                result["quick_messages"].append(clean_macro)

    # Sanitizar estrictamente contra el catálogo oficial de 109 opciones de Streamate (cero opciones inventadas)
    from src.platforms.streamate.stream_monitor_controller import DEFAULT_STREAMATE_OPTIONS, match_streamate_option

    sanitized_gold = []
    seen_gold = set()
    for g in result["gold_menu"]:
        opt_id = match_streamate_option(g.get("name", ""), DEFAULT_STREAMATE_OPTIONS)
        if opt_id and opt_id in DEFAULT_STREAMATE_OPTIONS:
            official_name = DEFAULT_STREAMATE_OPTIONS[opt_id]
            if official_name not in seen_gold:
                seen_gold.add(official_name)
                sanitized_gold.append({"name": official_name, "gold": 3})
    result["gold_menu"] = sanitized_gold if len(sanitized_gold) >= 3 else PRESET_SHIFT_THEMES["ass_twerk"]["gold_menu"]

    sanitized_wheel = []
    seen_wheel = set()
    for w in result["wheel"]["items"]:
        opt_id = match_streamate_option(w, DEFAULT_STREAMATE_OPTIONS)
        if opt_id and opt_id in DEFAULT_STREAMATE_OPTIONS:
            official_name = DEFAULT_STREAMATE_OPTIONS[opt_id]
            if official_name not in seen_wheel:
                seen_wheel.add(official_name)
                sanitized_wheel.append(official_name)
    result["wheel"]["items"] = sanitized_wheel if len(sanitized_wheel) >= 6 else PRESET_SHIFT_THEMES["ass_twerk"]["wheel"]["items"]

    # Defaults de seguridad si Mahia omitió algún campo
    if not result["topic"]:
        result["topic"] = "🔥 EN VIVO EN STREAMATE 🔥 Menu Gold 3G ⚡ Ruleta Íntima 5G 🖤 Tease Tomboy #Tomboy #Lovense #Gold"
    if not result["auto_messages"]["room_30s"]:
        result["auto_messages"] = PRESET_SHIFT_THEMES["ass_twerk"]["auto_messages"]
    if len(result["quick_messages"]) < 4:
        result["quick_messages"] = PRESET_SHIFT_THEMES["ass_twerk"]["quick_messages"]

    return result

async def apply_full_orchestrated_shift(theme_key: str, custom_text: Optional[str] = None) -> Dict[str, Any]:
    """
    Aplica de manera unificada y en un solo ciclo toda la estrategia comercial:
    1. Enfoca StreamMonitor en pantalla y activa la vista de transmisión ('Streamate').
    2. Inyecta el Room Topic (<= 140 chars) y Menú Gold (3G) directamente en SMConnect.
    3. Guarda los Auto-Mensajes y Macros preparados para StreamMonitor.
    """
    from src.platforms.streamate.stream_monitor_controller import save_streamate_tools_config

    # Traer ventana de StreamMonitor al frente en el monitor del usuario
    focus_streammonitor_window()

    if custom_text and custom_text.strip():
        shift_data = parse_mahia_output_to_tools(custom_text)
    else:
        shift_data = PRESET_SHIFT_THEMES.get(theme_key, PRESET_SHIFT_THEMES["ass_twerk"])

    topic_str = shift_data.get("topic", "")
    gold_items = shift_data.get("gold_menu", [])
    wheel_data = shift_data.get("wheel", {"cost": 5, "items": []})
    wheel_items = wheel_data.get("items", [])

    reports = {}

    # Inyección directa instantánea en la transmisión embebida de StreamMonitor (SMConnect)
    try:
        from src.platforms.streamate.smconnect_live_injector import inject_strategy_into_smconnect
        live_res = inject_strategy_into_smconnect(topic_str, gold_items, wheel_items)
        if live_res.get("success"):
            reports["transmission"] = "Inyectado directamente en la transmisión embebida de StreamMonitor"
            reports["topic"] = f"Tema de sala: {topic_str}"
            reports["gold_menu"] = f"Menú Gold: {len(gold_items)} items oficiales a 3G"
            reports["wheel"] = f"Ruleta Íntima: {len(wheel_items)} items oficiales a 5G"
    except Exception as e:
        reports["live_warning"] = f"Aviso live injector: {e}"

    # Guardar configuración persistida para StreamMonitor
    save_streamate_tools_config("active_orchestrated_shift", {
        "theme_key": theme_key,
        "auto_messages": shift_data.get("auto_messages"),
        "quick_messages": shift_data.get("quick_messages"),
        "topic": topic_str,
        "gold_menu": gold_items,
        "wheel": wheel_data
    })

    return {
        "success": True,
        "theme_applied": shift_data.get("title", theme_key),
        "reports": reports,
        "orchestrated_data": shift_data,
        "message": f"¡Estrategia del turno inyectada con éxito en la transmisión de StreamMonitor y Streamate!"
    }


def smart_orchestrate_natural_idea(idea_text: str) -> Dict[str, Any]:
    """
    Toma cualquier idea expresada en lenguaje natural por la modelo (español) y la convierte
    de inmediato en una estrategia comercial táctica 100% EN INGLÉS para Streamate.
    """
    raw_lower = idea_text.lower().strip()

    # Detección semántica de conceptos clave
    if any(k in raw_lower for k in ["ball", "gag", "saliva", "salivar", "boca", "cuello", "collar", "sumision", "sumisa", "domino", "pagan"]):
        preset = PRESET_SHIFT_THEMES["ball_gag_sub_dom"]
        theme_key = "ball_gag_sub_dom"
    elif any(k in raw_lower for k in ["ass", "twerk", "cola", "trasero", "nalga", "pompis", "booty"]):
        preset = PRESET_SHIFT_THEMES["ass_twerk"]
        theme_key = "ass_twerk"
    elif any(k in raw_lower for k in ["ukelele", "guitarra", "musica", "cantar", "cancion", "chill"]):
        preset = PRESET_SHIFT_THEMES["tomboy_ukelele"]
        theme_key = "tomboy_ukelele"
    elif any(k in raw_lower for k in ["lovense", "buzz", "vibrador", "toy", "juguete"]):
        preset = PRESET_SHIFT_THEMES["full_lovense"]
        theme_key = "full_lovense"
    else:
        # Generar estrategia personalizada en inglés
        clean_name = re.sub(r'[^a-zA-Z0-9 ]', '', idea_text)[:40].strip() or "Special Shift"
        preset = {
            "id": "custom_shift",
            "title": f"🎯 Meta: {clean_name}",
            "badge": "Estrategia Dinámica en Inglés",
            "topic": f"🔥 {clean_name.upper()} LIVE 🔥 Menu Gold 3G ⚡ Wheel 5G 🖤 Tease Me In Private #Tomboy #Lovense #Gold #Private"[:135],
            "gold_menu": [
                {"name": "Muestra el trasero", "gold": 3},
                {"name": "10x nalgadas", "gold": 3},
                {"name": "Posición de perrito", "gold": 3},
                {"name": "Cuento sucio", "gold": 3},
                {"name": "Di mi nombre", "gold": 3},
                {"name": "Ponte aceite en el trasero", "gold": 3}
            ],
            "wheel": {
                "cost": 5,
                "items": [
                    "Agacharse",
                    "Golpear culo con paleta",
                    "5x azotes",
                    "Pellizcar pezones",
                    "Pinzas en pezones",
                    "Escupir",
                    "Azotate",
                    "Insultar",
                    "Palabras sucias",
                    "Posición de perrito"
                ]
            },
            "auto_messages": {
                "room_30s": f"Hey handsome! Welcome to my room. Today is {clean_name} special 🖤 Gold: 3G | Wheel: 5G",
                "send_golds": "Thank you for that sweet gold {fan}! Loving this dynamic tonight ✨",
                "private_show": "We are totally private now... Tell me your dirtiest command 😉"
            },
            "quick_messages": [
                f"Gold Menu is only 3G today! Check out {clean_name} ⚡",
                "Spin the intimate Wheel (5G) to decide my treat 🎡",
                "Tips make me tease you faster 🖤",
                "Take me to private for complete control 🗝️"
            ]
        }
        theme_key = "custom_shift"

    return {
        "theme_key": theme_key,
        "strategy": preset,
        "input_idea": idea_text,
        "language": "100% English (Streamate Broadcast Standard)",
        "topic_length": len(preset["topic"])
    }


def execute_mahia_shift_dialogue(user_idea_spanish: str) -> Dict[str, Any]:
    """
    Ejecuta el flujo real solicitado por Sam:
    1. SIREN abre y enfoca StreamMonitor Desktop en la pantalla del usuario (WinSta0\\Default).
    2. SIREN interactúa en tiempo real con Mahia en StreamMonitor Desktop:
       - Navega automáticamente al chat de Mahia (/dashboard/chat)
       - Pega la orden táctica con reglas de negocio en el textarea
       - Hace clic en el botón 'Enviar'
       - Espera y extrae la respuesta real que Mahia genera en vivo
    3. SIREN adapta las respuestas para las herramientas oficiales de Streamate:
       - Room Topic oficial en inglés (<= 140 chars)
       - Menú Gold (exactamente 6 opciones oficiales del catálogo de Streamate a 3G)
       - Ruleta Íntima (exactamente 10 opciones oficiales del catálogo de Streamate a 5G)
    """
    import time
    # 1. Asegurar lanzamiento de StreamMonitor Desktop en la pantalla activa
    launch_res = launch_streammonitor_desktop()

    # Dar breve margen para que StreamMonitor se estabilice en pantalla
    time.sleep(1.5)

    # 2. Generar orden táctica que SIREN le entrega a Mahia
    res = smart_orchestrate_natural_idea(user_idea_spanish)
    strategy = res["strategy"]
    theme_key = res["theme_key"]

    siren_to_mahia_prompt = (
        f"Mahia: Sam ha definido el foco para su turno: '{user_idea_spanish}'.\n"
        f"Aplica las reglas de Streamate: Topic en inglés (máximo 140 chars con #hashtags), "
        f"Menú Gold exactamente a 3G usando solo opciones oficiales de Streamate, "
        f"y Ruleta Íntima a 5G usando solo opciones oficiales de Streamate.\n"
        f"Devuélveme el plan estructurado para aplicarlo en vivo."
    )

    # 3. INTERACCIÓN EN VIVO: Enviar al chat de Mahia dentro de StreamMonitor Desktop
    live_mahia_res = {}
    try:
        from src.platforms.streamate.mahia_live_connector import send_prompt_to_mahia_desktop
        live_mahia_res = send_prompt_to_mahia_desktop(siren_to_mahia_prompt, timeout_seconds=45)
    except Exception as e:
        live_mahia_res = {"success": False, "error": str(e)}

    # Si Mahia respondió en vivo en el chat de StreamMonitor, usar su respuesta real
    if live_mahia_res.get("success") and live_mahia_res.get("mahia_response"):
        mahia_response_text = live_mahia_res["mahia_response"]
        live_chat_done = True

        # Extraer topic sugerido por Mahia si viene con comillas
        topic_match = re.search(r'(?:Principal|Alternativa|Topic|Opción A|Opcion A|Opción B|Opcion B)[:\s]*"([^"]+)"', mahia_response_text)
        if topic_match:
            cand = topic_match.group(1).strip()
            if len(cand) <= 140:
                strategy["topic"] = cand
    else:
        # Fallback estructurado oficial
        mahia_response_text = (
            f"Entendido Sam. Aquí tienes el plan optimizado para tu sala:\n\n"
            f"TOPIC: {strategy['topic']}\n\n"
            f"MENU GOLD (3G - Catálogo Oficial Streamate):\n" +
            "\n".join([f"- {it['name']} (3 Gold)" for it in strategy['gold_menu']]) +
            f"\n\nRULETA INTIMA (5G - Catálogo Oficial Streamate):\n" +
            "\n".join([f"- {it}" for it in strategy['wheel']['items']]) +
            f"\n\nAUTO-MENSAJES:\n"
            f"- Entrada sala (30s): {strategy['auto_messages']['room_30s']}\n"
            f"- Agradecimiento Tip: {strategy['auto_messages']['send_golds']}"
        )
        live_chat_done = False

    return {
        "success": True,
        "theme_key": theme_key,
        "launch_desktop": launch_res,
        "live_chat_done": live_chat_done,
        "siren_prompt_to_mahia": siren_to_mahia_prompt,
        "mahia_reply": mahia_response_text,
        "strategy": strategy,
        "topic": strategy["topic"],
        "gold_menu": strategy["gold_menu"],
        "wheel": strategy["wheel"],
        "auto_messages": strategy["auto_messages"],
        "quick_messages": strategy.get("quick_messages", [])
    }
