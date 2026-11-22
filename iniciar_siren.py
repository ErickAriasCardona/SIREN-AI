"""
Lanzador oficial de SIREN AI (by ALMA TECH)
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

if __name__ == "__main__":
    from src.server.start_tunnel import run_server_and_tunnel
    try:
        from src.server.velvet_app_server import run_server
        run_server()
    except Exception as e:
        print(f"Error al iniciar servidor SIREN: {e}")
