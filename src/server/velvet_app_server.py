import os
import sys
import json
import sqlite3
import datetime
import urllib.request
import urllib.error
from pathlib import Path
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer

# Agregar raíz al sys.path
ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.append(str(ROOT))

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

from src.agents.roxanne_multimodel_copilot import (
    ROXANNE_SAM_SYSTEM_PROMPT,
    OllamaProvider,
    GeminiProvider
)

DB_PATH = ROOT / "data" / "velvet_analytics.db"
PORT = 8888

def detect_language(text: str) -> str:
    """Detecta si el mensaje entrante está en español o en inglés/otro."""
    text_lower = text.lower()
    spanish_indicators = [
        "hola", "buenos dias", "buenas tardes", "buenas noches", "hermosa", "linda", 
        "guapa", "bella", "que tal", "como estas", "cómo estás", "de donde eres", 
        "cuantos años", "cuánto", "haces", "hacer", "quiero", "foto", "videollamada", 
        "amor", "bebe", "papi", "chula", "te ves", "dios", "besos", "saludos", "gracias",
        "por favor", "precio", "cuanto cobras", "donde vives"
    ]
    for word in spanish_indicators:
        if word in text_lower:
            return "es"
    return "en"

def log_interaction_to_db(fan_message: str, reply: str, model_name: str, lang: str):
    """Registra la interacción en la base de datos velvet_analytics.db para análisis."""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS copilot_chat_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT,
                model_name TEXT,
                language TEXT,
                fan_message TEXT,
                sam_reply TEXT
            )
        """)
        cursor.execute("""
            INSERT INTO copilot_chat_logs 
            (timestamp, model_name, language, fan_message, sam_reply)
            VALUES (?, ?, ?, ?, ?)
        """, (
            datetime.datetime.now().isoformat(),
            model_name,
            lang,
            fan_message,
            reply
        ))
        conn.commit()
        conn.close()
    except Exception as e:
        print(f"[DB Warning]: No se pudo registrar en SQLite: {e}")

class VelvetRequestHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        # Servir archivos desde la raíz de VELVET AI
        super().__init__(*args, directory=str(ROOT), **kwargs)

    def end_headers(self):
        # Headers CORS universales
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type, Authorization")
        self.send_header("Cache-Control", "no-cache, no-store, must-revalidate")
        super().end_headers()

    def do_OPTIONS(self):
        self.send_response(204)
        self.end_headers()

    def do_GET(self):
        if self.path == "/api/status":
            self.handle_api_status()
        elif self.path == "/api/history":
            self.handle_api_history()
        elif self.path == "/api/chat_history":
            self.handle_api_chat_history()
        elif self.path == "/api/platforms_profiles":
            self.handle_api_platforms_profiles()
        elif self.path == "/api/financials":
            self.handle_api_financials()
        elif self.path.startswith("/api/positioning"):
            self.handle_api_positioning()
        else:
            # Servir index.html si entra a /
            if self.path == "/" or self.path == "":
                self.path = "/index.html"
            super().do_GET()

    def do_POST(self):
        if self.path == "/api/chat":
            self.handle_api_chat()
        elif self.path == "/api/clear_chat_history":
            self.handle_api_clear_chat_history()
        elif self.path == "/api/refresh_financials":
            self.handle_api_refresh_financials()
        elif self.path.startswith("/api/refresh_positioning"):
            self.handle_api_refresh_positioning()
        elif self.path.startswith("/api/deploy_profile"):
            self.handle_api_deploy_profile()
        else:
            self.send_error(404, "Endpoint no encontrado")


    def handle_api_deploy_profile(self):
        """Ejecuta el script de despliegue y actualización de perfil en segundo plano."""
        try:
            from urllib.parse import urlparse, parse_qs
            import threading
            import subprocess

            qs = parse_qs(urlparse(self.path).query)
            platform = qs.get("platform", ["stripchat"])[0].lower()

            script_map = {
                "loyalfans": "src/platforms/loyalfans/profile_updater.py",
                "stripchat": "src/platforms/stripchat/profile_updater.py",
                "streamate": "src/platforms/streamate/profile_updater.py",
                "flirt4free": "src/platforms/flirt4free/profile_updater.py"
            }

            target_script = script_map.get(platform, "src/platforms/stripchat/profile_updater.py")
            full_script_path = ROOT / target_script

            def run_worker():
                try:
                    subprocess.Popen([sys.executable, str(full_script_path)], cwd=str(ROOT))
                except Exception as e:
                    print(f"Error lanzando actualizador de {platform}: {e}")

            threading.Thread(target=run_worker, daemon=True).start()

            resp = {
                "success": True,
                "status": "launched",
                "platform": platform,
                "script": target_script,
                "message": f"🚀 Despliegue de {platform.upper()} puesto en marcha en ventana visible."
            }
        except Exception as e:
            resp = {"success": False, "error": str(e)}

        self.send_response(200)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.end_headers()
        self.wfile.write(json.dumps(resp).encode("utf-8"))

    def handle_api_financials(self):
        """Devuelve el balance en vivo, desglose de octubre y transacciones recientes."""
        try:
            import importlib
            import src.analytics.financial_live_sync as fls
            importlib.reload(fls)
            data = fls.parse_financials_dump()
        except Exception as e:
            data = {"error": str(e), "balance": 27.19, "current_month": 20.00}
        self.send_response(200)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.end_headers()
        self.wfile.write(json.dumps(data).encode("utf-8"))

    def handle_api_refresh_financials(self):
        """Consulta en vivo la sesión de LoyalFans y actualiza las métricas financieras."""
        try:
            import importlib
            import src.analytics.financial_live_sync as fls
            importlib.reload(fls)
            data = fls.fetch_live_financials_now_sync()
        except Exception as e:
            data = {"error": str(e), "balance": 27.19, "current_month": 20.00}
        self.send_response(200)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.end_headers()
        self.wfile.write(json.dumps(data).encode("utf-8"))

    def handle_api_positioning(self):
        """Devuelve el posicionamiento, percentil y estado de ventas en tiempo real."""
        try:
            from urllib.parse import urlparse, parse_qs
            import importlib
            import src.analytics.positioning_live_sync as pls
            importlib.reload(pls)
            qs = parse_qs(urlparse(self.path).query)
            platform = qs.get("platform", ["loyalfans"])[0]
            data = pls.get_realtime_positioning(platform)
        except Exception as e:
            data = {"error": str(e), "percentile": "Top 18%", "platform_key": "loyalfans"}
        self.send_response(200)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.end_headers()
        self.wfile.write(json.dumps(data).encode("utf-8"))

    def handle_api_refresh_positioning(self):
        """Fuerza actualización en vivo del posicionamiento y registra en SQLite."""
        try:
            from urllib.parse import urlparse, parse_qs
            import importlib
            import src.analytics.positioning_live_sync as pls
            importlib.reload(pls)
            qs = parse_qs(urlparse(self.path).query)
            platform = qs.get("platform", ["loyalfans"])[0]
            data = pls.refresh_positioning_live(platform)
        except Exception as e:
            data = {"error": str(e), "percentile": "Top 18%", "platform_key": "loyalfans"}
        self.send_response(200)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.end_headers()
        self.wfile.write(json.dumps(data).encode("utf-8"))

    def handle_api_status(self):
        """Verifica la conectividad con Ollama y la base de datos."""
        ollama_online = False
        available_models = []
        try:
            req = urllib.request.Request("http://localhost:11434/api/tags")
            with urllib.request.urlopen(req, timeout=3) as resp:
                data = json.loads(resp.read().decode())
                ollama_online = True
                available_models = [m.get("name") for m in data.get("models", [])]
        except Exception:
            ollama_online = False

        status_data = {
            "server": "VELVET AI Daemon",
            "port": PORT,
            "ollama_online": ollama_online,
            "ollama_host": "http://localhost:11434",
            "models": available_models,
            "active_default": "qwen2.5:7b-instruct",
            "database": str(DB_PATH.exists())
        }
        self.send_response(200)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.end_headers()
        self.wfile.write(json.dumps(status_data).encode("utf-8"))

    def handle_api_history(self):
        """Devuelve las últimas 10 interacciones registradas."""
        history = []
        try:
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            cursor.execute("""
                SELECT message_text, reply_text, reply_timestamp 
                FROM message_interactions 
                WHERE reply_text IS NOT NULL 
                ORDER BY id DESC LIMIT 10
            """)
            for row in cursor.fetchall():
                history.append({
                    "fan": row[0],
                    "sam": row[1],
                    "timestamp": row[2]
                })
            conn.close()
        except Exception:
            pass

        self.send_response(200)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.end_headers()
        self.wfile.write(json.dumps({"history": history}).encode("utf-8"))

    def handle_api_chat_history(self):
        """Devuelve el historial persistente de la conversacion entre Sam y Roxanne."""
        history = []
        try:
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS copilot_assistant_history (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp TEXT,
                    sender TEXT,
                    message TEXT,
                    model TEXT
                )
            """)
            cursor.execute("""
                SELECT timestamp, sender, message, model
                FROM copilot_assistant_history
                ORDER BY id ASC
            """)
            for row in cursor.fetchall():
                history.append({
                    "timestamp": row[0],
                    "sender": row[1],
                    "message": row[2],
                    "model": row[3]
                })
            conn.close()
        except Exception as e:
            print("[History Error]:", e)

        self.send_response(200)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.end_headers()
        self.wfile.write(json.dumps({"success": True, "history": history}).encode("utf-8"))

    def handle_api_clear_chat_history(self):
        """Limpia todo el historial de conversacion de Roxanne en la base de datos."""
        try:
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            cursor.execute("DROP TABLE IF EXISTS copilot_assistant_history")
            cursor.execute("""
                CREATE TABLE copilot_assistant_history (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp TEXT,
                    sender TEXT,
                    message TEXT,
                    model TEXT
                )
            """)
            conn.commit()
            conn.close()
            resp = {"success": True, "message": "Historial limpiado exitosamente"}
        except Exception as e:
            resp = {"success": False, "error": str(e)}

        self.send_response(200)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.end_headers()
        self.wfile.write(json.dumps(resp).encode("utf-8"))

    def handle_api_platforms_profiles(self):
        """Devuelve los perfiles oficiales y credenciales de acceso para cada plataforma."""
        try:
            from src.automation.credential_store import load_all_credentials
            creds = load_all_credentials()

            profiles = [
                {
                    "key": "streamate",
                    "name": "Streamate",
                    "model_handle": "SamBartone",
                    "performer_id": "144675665",
                    "rating": "4.0 ★ (Verificado)",
                    "status": "Verified (Activa)",
                    "account_type": "Cuenta Estudio Satelite (Centenario Studio)",
                    "login_url": "https://streamatemodels.com/login",
                    "public_url": "https://sambartone.cammodels.com",
                    "avatar_url": "/artifacts/streamate_audit/profile.png",
                    "username": creds.get("streamate", {}).get("username", "efac05@yopmail.com"),
                    "password": creds.get("streamate", {}).get("password", "Centenario123@"),
                    "rates": {
                        "private": "$2.99 / min",
                        "exclusive": "$3.99 / min",
                        "dynamic_enabled": "Activado ($2.99 - $6.99)"
                    },
                    "headline": "Chica tomboy versatil con energia propia e inteligente.",
                    "bio": "Mi mundo se mueve entre la musica, la tecnologia, el deporte y esa pasion constante por explorar el deseo. Toco el ukelele, pero tambien disfruto explorar sensaciones intensas a solas...",
                    "tags": ["Tomboy", "Ukelele", "Versatile", "Cam2Cam", "Roleplay"],
                    "geoblock": "Colombia visible (Sin bloqueo territorial)"
                },
                {
                    "key": "loyalfans",
                    "name": "LoyalFans",
                    "model_handle": "@samm_bartonn",
                    "performer_id": "samm_bartonn",
                    "rating": "Top 23% (Percentil Global)",
                    "status": "Verified (100% Directo)",
                    "account_type": "Independiente / Creadora Directa",
                    "login_url": "https://loyalfans.com/login",
                    "public_url": "https://loyalfans.com/samm_bartonn",
                    "avatar_url": "/artifacts/test_public_profile_verified.png",
                    "username": creds.get("loyalfans", {}).get("username", "sambartonn23@gmail.com"),
                    "password": creds.get("loyalfans", {}).get("password", "Kjc20009*"),
                    "rates": {
                        "message_text": "$0.50 / msg",
                        "message_media": "$0.50 / foto",
                        "fan_club": "$10.00 / mes"
                    },
                    "headline": "Software & AI Architect ⚡ Versatile Tomboy 🏍️",
                    "bio": "Smart by day, driven about my goals, and teasingly wicked by night. Software & AI Architect by trade, but my real sanctuary is motorcycles, speed, and my beloved pack...",
                    "tags": ["Tomboy", "Biker", "Tech"],
                    "geoblock": "Sin bloqueo territorial"
                },
                {
                    "key": "stripchat",
                    "name": "Stripchat",
                    "model_handle": "@sam_barton",
                    "performer_id": "sam_barton",
                    "rating": "En Espera (Listo en Cola)",
                    "status": "Verified (Verificado)",
                    "account_type": "Independiente / Directo",
                    "login_url": "https://stripchat.com/login",
                    "public_url": "https://stripchat.com/sam_barton",
                    "avatar_url": "/artifacts/stripchat_profile_updated_20261014_211003.png",
                    "username": creds.get("stripchat", {}).get("username", "sambartonn23@gmail.com"),
                    "password": creds.get("stripchat", {}).get("password", "6L!3K3RUnEdPKPt"),
                    "rates": {
                        "token_price": "$0.05 / token",
                        "private_show": "60 tokens / min",
                        "interactive_lovense": "Activo"
                    },
                    "headline": "Cute Tomboy Gamer • Lovense Interactive 🎮",
                    "bio": "Software & AI Architect by day, gaming tomboy & teasing companion by night. Soccer player, motorcycle enthusiast, and devoted mom to my dogs & 2 cats...",
                    "tags": ["tomboy", "gamer", "lovense", "athletic", "sensual", "biker"],
                    "geoblock": "Sin bloqueo territorial"
                },
                {
                    "key": "lovense",
                    "name": "Lovense Interactive",
                    "model_handle": "Lovense Connect",
                    "performer_id": "Bluetooth Link",
                    "rating": "Sincronizado",
                    "status": "Activo",
                    "account_type": "Herramienta Interactiva",
                    "login_url": "https://streamate.lovense.com",
                    "public_url": "",
                    "avatar_url": "/artifacts/smconnect_tab_juguetes_interactivos.png",
                    "username": creds.get("lovense", {}).get("username", "sambartonn23@gmail.com"),
                    "password": creds.get("lovense", {}).get("password", "6L!3K3RUnEdPKPt"),
                    "rates": {
                        "niveles": "5 niveles de vibracion configurados"
                    },
                    "headline": "Juguetes interactivos sincronizados con propinas en vivo.",
                    "bio": "Sincronizacion Bluetooth activa para reaccionar a propinas en Stripchat y Streamate.",
                    "tags": ["Lovense", "Bluetooth", "Tipping"],
                    "geoblock": "N/A"
                }
            ]
            resp = {"success": True, "profiles": profiles}
        except Exception as e:
            resp = {"success": False, "error": str(e)}

        self.send_response(200)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.end_headers()
        self.wfile.write(json.dumps(resp).encode("utf-8"))


    def handle_api_chat(self):
        """Procesa una consulta de chat con ROXANNE y devuelve la respuesta del LLM."""
        try:
            content_length = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(content_length).decode("utf-8")
            data = json.loads(body)

            message = data.get("message", "").strip()
            model_name = data.get("model", "qwen2.5:7b-instruct")
            chat_history = data.get("history", [])

            if not message:
                self.send_response(400)
                self.send_header("Content-Type", "application/json; charset=utf-8")
                self.end_headers()
                self.wfile.write(json.dumps({"error": "Mensaje vacío"}).encode("utf-8"))
                return

            lang = detect_language(message)

            # Preparar mensajes para Ollama / LLM
            messages = [{"role": "system", "content": ROXANNE_SAM_SYSTEM_PROMPT}]
            for h in chat_history:
                if "role" in h and "content" in h:
                    messages.append({"role": h["role"], "content": h["content"]})
            messages.append({"role": "user", "content": message})

            # Inferencia vía Ollama
            ollama_payload = {
                "model": model_name,
                "messages": messages,
                "stream": False,
                "options": {
                    "temperature": 0.7,
                    "top_p": 0.9
                }
            }

            req = urllib.request.Request(
                "http://localhost:11434/api/chat",
                data=json.dumps(ollama_payload).encode("utf-8"),
                headers={"Content-Type": "application/json"}
            )

            try:
                with urllib.request.urlopen(req, timeout=90) as response:
                    res_json = json.loads(response.read().decode("utf-8"))
                    reply = res_json.get("message", {}).get("content", "").strip()
            except Exception as e:
                reply = f"[Aviso ROXANNE]: Error conectando con el motor de inferencia ({model_name}): {e}. Asegúrate de que Ollama esté ejecutándose en localhost:11434."

            # Guardar en SQLite (Auditoría general y asistente persistente)
            log_interaction_to_db(message, reply, model_name, lang)
            try:
                conn = sqlite3.connect(DB_PATH)
                cursor = conn.cursor()
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS copilot_assistant_history (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        timestamp TEXT,
                        sender TEXT,
                        message TEXT,
                        model TEXT
                    )
                """)
                now_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                cursor.execute("INSERT INTO copilot_assistant_history (timestamp, sender, message, model) VALUES (?, ?, ?, ?)",
                               (now_str, "sam", message, model_name))
                cursor.execute("INSERT INTO copilot_assistant_history (timestamp, sender, message, model) VALUES (?, ?, ?, ?)",
                               (now_str, "roxanne", reply, model_name))
                conn.commit()
                conn.close()
            except Exception as dbe:
                print("[Chat Persist Error]:", dbe)


            response_data = {
                "reply": reply,
                "model": model_name,
                "detected_lang": lang,
                "rule_applied": "100% Spanish" if lang == "es" else "100% English (Default)",
                "timestamp": datetime.datetime.now().strftime("%H:%M:%S")
            }

            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.end_headers()
            self.wfile.write(json.dumps(response_data).encode("utf-8"))

        except Exception as err:
            self.send_response(500)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.end_headers()
            self.wfile.write(json.dumps({"error": str(err)}).encode("utf-8"))

def run_server():
    server_address = ("", PORT)
    httpd = ThreadingHTTPServer(server_address, VelvetRequestHandler)
    print(f"🚀 VELVET AI Command & Server activo en http://localhost:{PORT}")
    print(f"📡 API de Chat ROXANNE conectada a Ollama en http://localhost:11434")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nDeteniendo servidor...")
        httpd.server_close()

if __name__ == "__main__":
    run_server()
