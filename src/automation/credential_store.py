import json
import base64
from pathlib import Path
from typing import Dict, Any, Optional

ROOT_DIR = Path(__file__).resolve().parent.parent.parent
CREDENTIALS_FILE = ROOT_DIR / "data" / "credentials.json"

def _simple_obfuscate(text: str) -> str:
    """Ofuscación simple local para evitar contraseñas en texto totalmente plano."""
    if not text:
        return ""
    return base64.b64encode(text.encode("utf-8")).decode("utf-8")

def _simple_deobfuscate(text: str) -> str:
    """Decodifica la ofuscación local."""
    if not text:
        return ""
    try:
        return base64.b64decode(text.encode("utf-8")).decode("utf-8")
    except Exception:
        return text

def load_all_credentials() -> Dict[str, Dict[str, str]]:
    """Carga todas las credenciales guardadas por plataforma."""
    if not CREDENTIALS_FILE.exists():
        return {}
    try:
        with open(CREDENTIALS_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            # Desofuscar contraseñas
            for plat, creds in data.items():
                if "password" in creds:
                    creds["password"] = _simple_deobfuscate(creds["password"])
            return data
    except Exception:
        return {}

def save_platform_credentials(platform_key: str, username: str, password: str):
    """Guarda o actualiza las credenciales de una plataforma específica."""
    platform_key = platform_key.lower().strip()
    data = load_all_credentials()
    
    # Actualizar datos
    data[platform_key] = {
        "username": username,
        "password": password
    }

    # Guardar ofuscado en disco
    data_to_save = {}
    for plat, creds in data.items():
        data_to_save[plat] = {
            "username": creds.get("username", ""),
            "password": _simple_obfuscate(creds.get("password", ""))
        }

    CREDENTIALS_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(CREDENTIALS_FILE, "w", encoding="utf-8") as f:
        json.dump(data_to_save, f, ensure_ascii=False, indent=2)

def get_platform_credentials(platform_key: str) -> Dict[str, str]:
    """Retorna las credenciales guardadas para una plataforma o strings vacíos si no existen."""
    platform_key = platform_key.lower().strip()
    creds = load_all_credentials()
    return creds.get(platform_key, {"username": "", "password": ""})
