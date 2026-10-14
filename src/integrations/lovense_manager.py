"""
VELVET AI — Lovense & Stream Master Integration Manager
Controlador del ecosistema Lovense (Stream Master, Lovense Connect, Lovense OBS y API local).
Permite lanzar la suite de transmisión, consultar juguetes conectados por Bluetooth BLE
y mapear las propinas de Stripchat/LoyalFans a los niveles de vibración de Sam Barton.
"""

import sys
import os
import json
import base64
import subprocess
import urllib.request
import urllib.parse
from pathlib import Path
from typing import Dict, Any, List, Optional

ROOT_DIR = Path(__file__).resolve().parent.parent.parent
sys.path.append(str(ROOT_DIR))

from src.config import DATA_DIR

CREDENTIALS_FILE = DATA_DIR / "credentials.json"
LOCALAPPDATA = os.environ.get("LOCALAPPDATA", r"C:\Users\MI PC\AppData\Local")

STREAM_MASTER_DIR = Path(LOCALAPPDATA) / "Lovense" / "Stream Master"
STREAM_MASTER_EXE = STREAM_MASTER_DIR / "LovenseBrowser" / "Browser" / "chrome.exe"
STREAM_MASTER_DATA = Path(LOCALAPPDATA) / "Lovense" / "Chromium"

LOVENSE_OBS_EXE = STREAM_MASTER_DIR / "LovenseOBS" / "bin" / "64bit" / "lvs_obs64.exe"
LOVENSE_CONNECT_EXE = Path(LOCALAPPDATA) / "Lovense" / "Connect" / "Lovense_Connect.exe"

# 💎 MATRIZ DE REACCIÓN Y TIP TIERS — SAM BARTON
SAM_BARTON_TIP_MATRIX = [
    {
        "tier": "Level 1 — Piquete Eléctrico",
        "tokens_min": 1,
        "tokens_max": 9,
        "vibration_level": 3,
        "duration_sec": 2,
        "sam_reaction": "😏 'Hey, sentí eso... apenas calentando motores'",
        "style": "Discreto / Tomboy traviesa"
    },
    {
        "tier": "Level 2 — Aceleración Inicial",
        "tokens_min": 10,
        "tokens_max": 24,
        "vibration_level": 7,
        "duration_sec": 4,
        "sam_reaction": "🔥 'Mmm... eso ya tiene mejor cadencia. Me gusta el ritmo'",
        "style": "Pícaro y receptivo"
    },
    {
        "tier": "Level 3 — Modo Turbo (Alta Potencia)",
        "tokens_min": 25,
        "tokens_max": 49,
        "vibration_level": 12,
        "duration_sec": 6,
        "sam_reaction": "⚡ 'Uff... vibración profunda. No te detengas ahora'",
        "style": "Sensual y retador"
    },
    {
        "tier": "Level 4 — Terremoto & Onda Sísmica",
        "tokens_min": 50,
        "tokens_max": 99,
        "vibration_level": 16,
        "duration_sec": 9,
        "sam_reaction": "🏍️ '¡Santo cielo! Eso sacude como mi moto a 140km/h... ¡mírame temblar!'",
        "style": "Intensidad alta / Biker adrenalina"
    },
    {
        "tier": "Level 5 — Sobrecarga Máxima (Climax / Orgasm)",
        "tokens_min": 100,
        "tokens_max": 249,
        "vibration_level": 20,
        "duration_sec": 15,
        "sam_reaction": "👑 '¡AH! 20/20 continuo... Me tienes completamente a tu merced'",
        "style": "Máximo control del fan"
    },
    {
        "tier": "Level 6 — Meta Carro de Diciembre & Cancún",
        "tokens_min": 250,
        "tokens_max": 99999,
        "vibration_level": 20,
        "duration_sec": 30,
        "special_preset": "pulse_wave_fireworks",
        "sam_reaction": "🚗 '¡LO HICISTE! Cada token va directo a mi carro de diciembre. Eres oficialmente mi favorito'",
        "style": "Agradecimiento apasionado y complicidad total"
    }
]

def get_lovense_credentials() -> Dict[str, str]:
    """Obtiene las credenciales de Lovense almacenadas de forma cifrada/codificada."""
    if not CREDENTIALS_FILE.exists():
        return {"username": "", "password": ""}
    try:
        data = json.loads(CREDENTIALS_FILE.read_text(encoding="utf-8"))
        lov = data.get("lovense", {})
        pwd_b64 = lov.get("password", "")
        pwd = base64.b64decode(pwd_b64).decode("utf-8") if pwd_b64 else ""
        return {
            "username": lov.get("username", "sambartonn23@gmail.com"),
            "password": pwd
        }
    except Exception as e:
        print(f"Error al leer credenciales Lovense: {e}")
        return {"username": "", "password": ""}

def launch_stream_master() -> Dict[str, Any]:
    """Inicia la suite Lovense Stream Master (Chromium + Extensiones integradas)."""
    if not STREAM_MASTER_EXE.exists():
        return {
            "success": False,
            "error": f"No se encontró el ejecutable de Stream Master en: {STREAM_MASTER_EXE}"
        }

    STREAM_MASTER_DATA.mkdir(parents=True, exist_ok=True)
    cmd = [
        str(STREAM_MASTER_EXE),
        f'--user-data-dir={str(STREAM_MASTER_DATA)}'
    ]

    try:
        proc = subprocess.Popen(
            cmd,
            creationflags=subprocess.CREATE_NEW_PROCESS_GROUP if os.name == 'nt' else 0,
            close_fds=True
        )
        return {
            "success": True,
            "pid": proc.pid,
            "message": "Lovense Stream Master iniciado exitosamente en segundo plano."
        }
    except Exception as e:
        return {"success": False, "error": str(e)}

def launch_lovense_obs() -> Dict[str, Any]:
    """Inicia la versión especializada Lovense OBS Studio."""
    if not LOVENSE_OBS_EXE.exists():
        return {
            "success": False,
            "error": f"No se encontró Lovense OBS en: {LOVENSE_OBS_EXE}"
        }

    try:
        proc = subprocess.Popen(
            [str(LOVENSE_OBS_EXE)],
            cwd=str(LOVENSE_OBS_EXE.parent),
            creationflags=subprocess.CREATE_NEW_PROCESS_GROUP if os.name == 'nt' else 0,
            close_fds=True
        )
        return {
            "success": True,
            "pid": proc.pid,
            "message": "Lovense OBS Studio iniciado correctamente."
        }
    except Exception as e:
        return {"success": False, "error": str(e)}

def check_local_lovense_api(port: int = 20010) -> Dict[str, Any]:
    """
    Consulta la API local de Lovense Connect / Stream Master en el puerto loopback (default 20010).
    Retorna la lista de juguetes sincronizados (Lush, Nora, Domi, etc.), batería y estado.
    """
    url = f"http://127.0.0.1:{port}/GetToys"
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "VELVET-AI-Lovense-Client"})
        with urllib.request.urlopen(req, timeout=1.5) as response:
            if response.status == 200:
                body = response.read().decode("utf-8")
                data = json.loads(body)
                return {
                    "online": True,
                    "port": port,
                    "data": data,
                    "toys": data.get("data", {})
                }
    except Exception:
        pass

    # Probar puerto alternativo 30010
    if port != 30010:
        return check_local_lovense_api(port=30010)

    return {
        "online": False,
        "port": None,
        "message": "Servicio local de Lovense Connect no detectado en puertos 20010/30010."
    }

def send_toy_command(
    action: str = "Vibrate",
    value: int = 10,
    time_sec: int = 5,
    toy_id: Optional[str] = None,
    port: int = 20010
) -> Dict[str, Any]:
    """
    Envía un comando de activación a los juguetes Lovense vía HTTP Local API.
    Acciones soportadas: 'Vibrate', 'Rotate', 'Air:Auto', 'Preset'.
    """
    api_status = check_local_lovense_api(port)
    if not api_status.get("online"):
        return {"success": False, "error": "Lovense Connect / Stream Master no está activo en red local."}

    active_port = api_status["port"]
    params = {
        "v": min(max(value, 0), 20),
        "t": time_sec
    }
    if toy_id:
        params["toy"] = toy_id

    url = f"http://127.0.0.1:{active_port}/{action}?{urllib.parse.urlencode(params)}"
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "VELVET-AI-Lovense-Client"})
        with urllib.request.urlopen(req, timeout=3.0) as resp:
            raw = resp.read().decode("utf-8")
            return {"success": True, "response": raw, "action": action, "value": value}
    except Exception as e:
        return {"success": False, "error": str(e)}

def get_sam_barton_tip_reaction(tokens: int) -> Dict[str, Any]:
    """Calcula la respuesta de juguete y el parlamento en voz de Sam Barton para una propina recibida."""
    for tier in SAM_BARTON_TIP_MATRIX:
        if tier["tokens_min"] <= tokens <= tier["tokens_max"]:
            return {
                "tokens": tokens,
                "tier_name": tier["tier"],
                "vibration_level": tier["vibration_level"],
                "duration_sec": tier["duration_sec"],
                "sam_voice": tier["sam_reaction"],
                "aesthetic_style": tier["style"]
            }

    # Si supera la matriz máxima
    last = SAM_BARTON_TIP_MATRIX[-1]
    return {
        "tokens": tokens,
        "tier_name": last["tier"],
        "vibration_level": 20,
        "duration_sec": 30,
        "sam_voice": last["sam_reaction"],
        "aesthetic_style": last["style"]
    }
