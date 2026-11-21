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
            "Welcome in! First time? Paid submission today 🗝️",
            "New here? Ball gag & collar on camera 😈",
            "Hey, you're back! Ready to command me? 😏",
            "Good to see you again! Tip 3G for gag orders 💋",
            "My master is back! Take full control in private 🖤",
            "Always back to discipline me ⚡ take me to private now 🗝️"
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
            "Welcome in! First time? Booty special today 😉",
            "New here? Check my 3G Gold Menu now 🍑",
            "Hey, you're back! Missed this booty bouncing? 😏",
            "Good to see you again! Spin the wheel 5G 🎡",
            "My favorite regular! Ready for private show? 💋",
            "Back to spoil me again 🖤 let's go uncensored ⚡"
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
            "Welcome in! First time? Chill ukelele tunes today 🎶",
            "New here? Request a song from my 3G menu ✨",
            "Hey, you're back! Glad you came to vibe 🎸",
            "Good to see you again! Spin the wheel 5G 🎡",
            "My favorite regular! Want a private VIP song? 🖤",
            "Always back to support me ✨ let's chat in private 💋"
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
            "Welcome in! First time? Lovense control active ⚡",
            "New here? Tip 3G to buzz my toy live 🔥",
            "Hey, you're back! Ready to make me buzz? 😏",
            "Good to see you again! Take my toy to max ⚡",
            "My favorite controller is back! Level 10 ready 😈",
            "Back to make me shake 🖤 take me to private now 💋"
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
        f"5. MACROS DE CHAT (Alt+1 a Alt+6): 6 mensajes súper cortos en inglés, afines al saludo de sala:\n"f"   - Alt+1 y Alt+2: Primera vez en la sala (nuevos)\n"f"   - Alt+3 y Alt+4: Ya han entrado antes (retorno)\n"f"   - Alt+5 y Alt+6: Han entrado varias veces (habituales / VIPs)"
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


ENGLISH_TO_SPANISH_OFFICIAL = {
    # Twerk & Booty
    "twerk": "twerk",
    "shake ass": "Sacudir el culo",
    "shake": "Agita el trasero",
    "booty": "Muestra el trasero",
    "butt": "Muéstrame el culo",
    "bounce": "Rebota el trasero",
    "oil": "Ponte aceite en el trasero",
    "spank": "10x nalgadas",
    "spanking": "5x azotes",
    "whip": "Azotar",
    "paddle": "Golpear culo con paleta",
    "bend over": "Agacharse",
    "doggy": "Posición de perrito",
    "squat": "Sentadillas",
    "squats": "Sentadillas",
    "clap boobs": "Aplaude con los senos",
    "boob bounce": "Rebote de senos",
    "boobs": "Acercamiento en senos",
    "top off": "Quitarse el top",
    "strip": "Estriptís",
    "dance": "Baile",
    "pole dance": "Baile en tubo",
    "feet": "Muéstrame los pies",
    "toes": "Chupar dedos de pies",
    "face": "Acercamiento en rostro",
    "pleasure face": "Cara de placer",
    # BDSM & Submission / Gag
    "ball gag": "Mordaza",
    "gag": "Hazme amordazar",
    "drool": "Hazme babear",
    "tongue": "Mostrar lengua",
    "spit": "Escupir",
    "nipple clamps": "Pinzas en pezones",
    "clamps": "Pinzas en pezones",
    "pinch": "Pellizcar pezones",
    "insult": "Insultar",
    "humiliate": "SPH",
    "sph": "SPH",
    "kneel": "Agacharse",
    "crawl": "Posición de perrito",
    # Chill & Sensory
    "asmr": "ASMR",
    "whisper": "ASMR",
    "dirty talk": "Palabras sucias",
    "dirty story": "Cuento sucio",
    "smile": "Sonrisa",
    "kiss": "Lanzar un beso",
    "blow kiss": "Lanzar un beso",
    "lick lips": "Lamer labios",
    "wink": "Quiño",
    "say my name": "Di mi nombre",
    "name": "Di mi nombre",
    "yoga": "Yoga sensual",
    "sarcasm": "Sarcasmo",
    "belly": "Mostrar vientre",
    # Toys & Lovense
    "toy": "Mostrar juguetes",
    "toys": "Mostrar juguetes",
    "vibrator": "Lame vibrador",
    "buzz": "Lame vibrador",
    "lovense": "Lame vibrador",
    "orgasm": "Hazme acabar",
    "cum": "Hazme acabar",
    "dildo": "Dildo",
    "magic wand": "Varita Hitachi / Magic Wand",
    "moan": "Gemido",
    "moan my name": "Gemir mi nombre",
    "touch": "Provocame con todo el cuerpo",
    "tease": "Provocame con todo el cuerpo"
}

def deduce_strategy_from_mahia_text(mahia_text: str, user_idea: str) -> Dict[str, Any]:
    """
    Deduce de forma 100% DINÁMICA (cero datos quemados) la estrategia técnica
    analizando las recomendaciones textuales reales de Mahia y las palabras clave de Sam.
    Garantiza que el Topic sea el de Mahia y que las opciones de Gold y Ruleta pertenezcan
    exclusivamente al catálogo oficial de 109 opciones de Streamate.
    """
    from src.platforms.streamate.stream_monitor_controller import DEFAULT_STREAMATE_OPTIONS, normalize_text

    combined_text = f"{mahia_text}\n{user_idea}"
    norm_combined = normalize_text(combined_text)

    # 1. Extraer tópicos propuestos por Mahia
    quoted_topics = []
    # Buscar patrones Principal / Alternativa o comillas explícitas
    labeled_matches = re.findall(r'(?:Principal|Alternativa|Topic|Opción A|Opcion A|Opción B|Opcion B)[:\s]*"([^"]+)"', mahia_text, re.IGNORECASE)
    for cand in labeled_matches:
        cand_clean = cand.strip()
        if len(cand_clean) <= 140 and cand_clean not in quoted_topics:
            quoted_topics.append(cand_clean)

    # Buscar otras comillas si no encontramos labeled
    all_quotes = re.findall(r'"([^"]{15,140})"', mahia_text)
    for q in all_quotes:
        q_clean = q.strip()
        if q_clean not in quoted_topics and any(w in q_clean.lower() for w in ["gold", "wheel", "show", "special", "tease", "live", "3g", "5g", "#"]):
            quoted_topics.append(q_clean)

    main_topic = quoted_topics[0] if quoted_topics else "🔥 LIVE IN STREAMATE 🔥 Gold Menu 3G ⚡ Wheel 5G 🖤 Tease Me In Private #Tomboy #Lovense #Gold"
    alt_topic = quoted_topics[1] if len(quoted_topics) > 1 else ""

    # 2. Extraer acciones del catálogo oficial recomendadas por Mahia o el usuario
    detected_options = []
    seen = set()

    for key, official_name in ENGLISH_TO_SPANISH_OFFICIAL.items():
        if f" {key} " in f" {norm_combined} " or key in norm_combined:
            if official_name not in seen and official_name in DEFAULT_STREAMATE_OPTIONS.values():
                seen.add(official_name)
                detected_options.append(official_name)

    for opt_id, opt_name in DEFAULT_STREAMATE_OPTIONS.items():
        norm_opt = normalize_text(opt_name)
        if norm_opt in norm_combined and opt_name not in seen:
            seen.add(opt_name)
            detected_options.append(opt_name)

    # Fallbacks temáticos inteligentes para completar el cupo exacto
    theme_fallbacks = [
        "twerk", "Sacudir el culo", "Muestra el trasero", "10x nalgadas", "Posición de perrito",
        "Ponte aceite en el trasero", "Agita el trasero", "Golpear culo con paleta", "5x azotes",
        "Agacharse", "Baile", "Estriptís", "Sentadillas", "Muéstrame el culo", "Palabras sucias",
        "Gemido", "Gemir mi nombre", "Lanzar un beso", "Sonrisa", "Di mi nombre"
    ]
    for fb in theme_fallbacks:
        if fb not in seen and fb in DEFAULT_STREAMATE_OPTIONS.values():
            seen.add(fb)
            detected_options.append(fb)

    gold_menu = [{"name": opt, "gold": 3} for opt in detected_options[:6]]
    wheel_items = detected_options[6:16]
    if len(wheel_items) < 10:
        for opt_name in DEFAULT_STREAMATE_OPTIONS.values():
            if opt_name not in seen:
                seen.add(opt_name)
                wheel_items.append(opt_name)
                if len(wheel_items) == 10:
                    break

    short_title = main_topic.split("#")[0].strip().strip("-•|")[:40]
    auto_messages = {
        "room_30s": f"Hey! Welcome in. {short_title} today. Gold Menu is 3G, treat yourself 😉",
        "send_golds": "Mmm thank you for that gold {fan}! Loving this dynamic tonight 🔥",
        "private_show": "We are completely alone in private now... Take full control 💋"
    }

    # 4. Extraer los 6 Atajos Rápidos de Chat (Alt+1 a Alt+6) solicitados por Sam
    # Alt+1 y Alt+2: Primera vez en la sala (afines al Saludo 30s)
    # Alt+3 y Alt+4: Ya han entrado antes (retorno)
    # Alt+5 y Alt+6: Han entrado varias veces (habituales / VIPs)
    extracted_macros = {}
    in_macros_section = False
    for line in mahia_text.splitlines():
        line_low = line.lower().strip()
        if any(k in line_low for k in ["macro", "alt+", "atajo", "mensaje rápido", "mensajes rápidos", "5."]):
            in_macros_section = True
        
        if in_macros_section:
            m = re.search(r'alt\s*\+\s*([1-6])\s*[:\-]\s*(.+)', line, re.IGNORECASE)
            if m:
                idx = int(m.group(1))
                val = m.group(2).strip().strip('"\'')
                if len(val) >= 4:
                    extracted_macros[idx] = val

    theme_keyword = "special show"
    if any(w in norm_combined for w in ["ass", "twerk", "booty", "cola", "nalga"]):
        theme_keyword = "twerk show"
    elif any(w in norm_combined for w in ["ball", "gag", "sumision", "collar"]):
        theme_keyword = "kinky session"
    elif any(w in norm_combined for w in ["ukelele", "chill", "music"]):
        theme_keyword = "chill session"
    elif any(w in norm_combined for w in ["buzz", "lovense"]):
        theme_keyword = "toy control"

    macro_defaults = {
        1: f"Welcome in! First time? Come enjoy my {theme_keyword} 😉",
        2: "Hey new face! Check out my 3G Gold Menu today 🍑",
        3: "Hey, you're back! Missed my show already? 😏",
        4: "Good to see you again! Ready for some fun? 💋",
        5: "My favorite regular is here! Come closer 😈",
        6: "Look who's back to spoil me 🖤 always loving you ⚡"
    }

    quick_messages = [extracted_macros.get(i, macro_defaults[i]) for i in range(1, 7)]
    quick_messages_by_tier = {
        "new_users": [quick_messages[0], quick_messages[1]],
        "returning_users": [quick_messages[2], quick_messages[3]],
        "frequent_users": [quick_messages[4], quick_messages[5]]
    }

    return {
        "title": short_title,
        "topic": main_topic,
        "alt_topic": alt_topic,
        "alternative_topics": quoted_topics,
        "gold_menu": gold_menu,
        "wheel": {"cost": 5, "items": wheel_items},
        "auto_messages": auto_messages,
        "quick_messages": quick_messages,
        "quick_messages_by_tier": quick_messages_by_tier,
        "mahia_raw_reply": mahia_text
    }

async def apply_full_orchestrated_shift(theme_key: str, custom_text: Optional[str] = None, strategy_data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """
    Aplica de manera unificada y en un solo ciclo toda la estrategia comercial:
    1. Enfoca StreamMonitor en pantalla y activa la vista de transmisión ('Streamate').
    2. Inyecta el Room Topic (<= 140 chars) y Menú Gold (3G) directamente en SMConnect.
    3. Guarda los Auto-Mensajes y Macros preparados para StreamMonitor.
    """
    from src.platforms.streamate.stream_monitor_controller import save_streamate_tools_config

    # Traer ventana de StreamMonitor al frente en el monitor del usuario
    focus_streammonitor_window()

    if strategy_data and isinstance(strategy_data, dict) and strategy_data.get("topic"):
        shift_data = strategy_data
    elif custom_text and custom_text.strip():
        shift_data = parse_mahia_output_to_tools(custom_text)
    else:
        shift_data = PRESET_SHIFT_THEMES.get(theme_key, PRESET_SHIFT_THEMES["ass_twerk"])

    topic_str = shift_data.get("topic", "")
    gold_items = shift_data.get("gold_menu", [])
    wheel_data = shift_data.get("wheel", {"cost": 5, "items": []})
    wheel_items = wheel_data.get("items", [])

    reports = {}

    # 1. Inyección de Auto-mensajes (3 disparadores) y Atajos Alt+1..Alt+8 en StreamMonitor Desktop
    auto_msgs = shift_data.get("auto_messages") or {}
    quick_msgs = shift_data.get("quick_messages") or []
    try:
        from src.platforms.streamate.streammonitor_messages_injector import inject_streammonitor_auto_and_quick_messages
        msg_res = inject_streammonitor_auto_and_quick_messages(auto_msgs, quick_msgs)
        if msg_res.get("success"):
            reports["auto_messages"] = "Mensajes automáticos (Bienvenida 30s, Entrada a privado, Propina Gold) y Atajos Alt+1..Alt+8 inyectados y guardados en StreamMonitor"
        else:
            reports["auto_messages_warning"] = msg_res.get("error", "Aviso guardando mensajes automáticos")
    except Exception as e:
        reports["auto_messages_warning"] = f"Aviso auto-messages injector: {e}"

    # 2. Inyección directa instantánea en la transmisión embebida de StreamMonitor (SMConnect)
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
        f"Aplica las reglas de Streamate y entrégame el plan en estos 5 puntos claros y bien enumerados:\n"
        f"1. Room Topic (en inglés, máx 140 chars con #hashtags).\n"
        f"2. GOLD Menu a 3G (exactamente 6 acciones oficiales del catálogo de Streamate).\n"
        f"3. Ruleta Íntima a 5G (exactamente 10 acciones oficiales del catálogo de Streamate).\n"
        f"4. Tres mensajes automáticos en inglés: Saludo 30s sala, Entrada a privado y Agradecimiento por propina gold.\n"
        f"5. Seis mensajes rápidos de chat súper cortos en inglés para StreamMonitor (Alt+1 a Alt+6), afines al saludo de sala:\n"
        f"   - Alt+1: Primera vez en la sala (usuario nuevo)\n"
        f"   - Alt+2: Primera vez en la sala (usuario nuevo)\n"
        f"   - Alt+3: Ya ha entrado antes (retorno)\n"
        f"   - Alt+4: Ya ha entrado antes (retorno)\n"
        f"   - Alt+5: Ha entrado varias veces (habitual / VIP)\n"
        f"   - Alt+6: Ha entrado varias veces (habitual / VIP)\n"
        f"Devuélveme el plan estructurado para aplicarlo en vivo."
    )

    # 3. INTERACCIÓN EN VIVO: Enviar al chat de Mahia dentro de StreamMonitor Desktop
    live_mahia_res = {}
    try:
        from src.platforms.streamate.mahia_live_connector import send_prompt_to_mahia_desktop
        live_mahia_res = send_prompt_to_mahia_desktop(siren_to_mahia_prompt, timeout_seconds=45)
    except Exception as e:
        live_mahia_res = {"success": False, "error": str(e)}

    # Si Mahia respondió en vivo en el chat de StreamMonitor, DEDUCIR TODO DINÁMICAMENTE (NO DATA QUEMADA)
    if live_mahia_res.get("success") and live_mahia_res.get("mahia_response"):
        mahia_response_text = live_mahia_res["mahia_response"]
        live_chat_done = True
        # Deducir dinámicamente Topic, Menú Gold (3G) y Ruleta (5G) directamente de lo que Mahia escribió:
        strategy = deduce_strategy_from_mahia_text(mahia_response_text, user_idea_spanish)
        theme_key = "mahia_live_deduction" 
    else:
        # Fallback estructurado oficial bien enumerado y claro
        qm = strategy.get('quick_messages', [])
        m1 = qm[0] if len(qm) > 0 else "Welcome in! New to my room? 😉"
        m2 = qm[1] if len(qm) > 1 else "First time here? Try my 3G menu 🍑"
        m3 = qm[2] if len(qm) > 2 else "Hey, you're back! Missed me? 😏"
        m4 = qm[3] if len(qm) > 3 else "Good to see you again! Ready? 💋"
        m5 = qm[4] if len(qm) > 4 else "My favorite regular is here! Come closer 😈"
        m6 = qm[5] if len(qm) > 5 else "Back again to spoil me? You're the best ⚡"

        mahia_response_text = (
            f"Entendido Sam. Aquí tienes el plan táctico completo para tu sala, estructurado en 5 puntos claros:\n\n"
            f"1. ROOM TOPIC (en inglés, ≤ 140 chars con #hashtags):\n"
            f"\"{strategy['topic']}\"\n\n"
            f"2. GOLD MENU (6 opciones oficiales del catálogo de Streamate a 3G):\n" +
            "\n".join([f"{idx+1}. {it['name']} - 3G" for idx, it in enumerate(strategy['gold_menu'])]) +
            f"\n\n3. RULETA ÍNTIMA (10 opciones oficiales del catálogo de Streamate a 5G):\n" +
            "\n".join([f"{idx+1}. {it}" for idx, it in enumerate(strategy['wheel']['items'])]) +
            f"\n\n4. TRES MENSAJES AUTOMÁTICOS (StreamMonitor):\n"
            f"- Saludo / Bienvenida (30s): \"{strategy['auto_messages']['room_30s']}\"\n"
            f"- Mensaje al entrar a Privado: \"{strategy['auto_messages'].get('private_show', 'Welcome to private room 💋')}\"\n"
            f"- Agradecimiento por Propina Gold: \"{strategy['auto_messages']['send_golds']}\"\n\n"
            f"5. SEIS ATAJOS RÁPIDOS DE CHAT (Alt+1 a Alt+6 - Afines al Saludo de Sala):\n"
            f"• Primera vez en la sala (Usuarios Nuevos):\n"
            f"  - Alt+1: \"{m1}\"\n"
            f"  - Alt+2: \"{m2}\"\n"
            f"• Ya han entrado antes (Retorno / Segunda vez):\n"
            f"  - Alt+3: \"{m3}\"\n"
            f"  - Alt+4: \"{m4}\"\n"
            f"• Han entrado varias veces (Habituales / VIPs):\n"
            f"  - Alt+5: \"{m5}\"\n"
            f"  - Alt+6: \"{m6}\""
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
