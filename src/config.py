import os
from pathlib import Path
from dotenv import load_dotenv

# Cargar variables de entorno desde .env si existe
ROOT_DIR = Path(__file__).resolve().parent.parent
load_dotenv(ROOT_DIR / ".env")

# Directorios principales
BRAIN_DIR = ROOT_DIR / "brain"
DATA_DIR = ROOT_DIR / "data"
ARTIFACTS_DIR = ROOT_DIR / "artifacts"
SRC_DIR = ROOT_DIR / "src"

# Asegurar que existan los directorios clave
DATA_DIR.mkdir(parents=True, exist_ok=True)
ARTIFACTS_DIR.mkdir(parents=True, exist_ok=True)

# Configuraciones de scraping y agentes
STREAMATE_BASE_URL = os.getenv("STREAMATE_BASE_URL", "https://streamate.com")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "")
