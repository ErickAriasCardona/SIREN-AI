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
        elif self.path == "/api/refresh_financials":
            self.handle_api_refresh_financials()
        elif self.path.startswith("/api/refresh_positioning"):
            self.handle_api_refresh_positioning()
        else:
            self.send_error(404, "Endpoint no encontrado")

    def handle_api_financials(self):
        """Devuelve el balance en vivo, desglose de octubre y transacciones recientes."""
        try:
            from src.analytics.financial_live_sync import parse_financials_dump
            data = parse_financials_dump()
        except Exception as e:
            data = {"error": str(e), "balance": 15.59, "current_month": 8.40}
        self.send_response(200)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.end_headers()
        self.wfile.write(json.dumps(data).encode("utf-8"))

    def handle_api_refresh_financials(self):
        """Consulta en vivo la sesión de LoyalFans y actualiza las métricas financieras."""
        try:
            from src.analytics.financial_live_sync import fetch_live_financials_now_sync
            data = fetch_live_financials_now_sync()
        except Exception as e:
            data = {"error": str(e), "balance": 15.59, "current_month": 8.40}
        self.send_response(200)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.end_headers()
        self.wfile.write(json.dumps(data).encode("utf-8"))

    def handle_api_positioning(self):
        """Devuelve el posicionamiento, percentil y estado de ventas en tiempo real."""
        try:
            from urllib.parse import urlparse, parse_qs
            from src.analytics.positioning_live_sync import get_realtime_positioning
            qs = parse_qs(urlparse(self.path).query)
            platform = qs.get("platform", ["loyalfans"])[0]
            data = get_realtime_positioning(platform)
        except Exception as e:
            data = {"error": str(e), "percentile": "Top 23%", "platform_key": "loyalfans"}
        self.send_response(200)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.end_headers()
        self.wfile.write(json.dumps(data).encode("utf-8"))

    def handle_api_refresh_positioning(self):
        """Fuerza actualización en vivo del posicionamiento y registra en SQLite."""
        try:
            from urllib.parse import urlparse, parse_qs
            from src.analytics.positioning_live_sync import refresh_positioning_live
            qs = parse_qs(urlparse(self.path).query)
            platform = qs.get("platform", ["loyalfans"])[0]
            data = refresh_positioning_live(platform)
        except Exception as e:
            data = {"error": str(e), "percentile": "Top 23%", "platform_key": "loyalfans"}
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

            # Guardar en SQLite
            log_interaction_to_db(message, reply, model_name, lang)

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
