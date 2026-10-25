"""
SIREN AI — Multi-Platform Command & Intelligence Server
Servidor local de alta velocidad con soporte para Roxanne Copilot (Ollama/Gemini)
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.server.velvet_app_server import run_server

if __name__ == "__main__":
    run_server()
