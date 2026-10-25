from pathlib import Path

server_file = Path("src/server/velvet_app_server.py")
content = server_file.read_text(encoding="utf-8")

# 1. Imports
import_anchor = "from src.agents.roxanne_multimodel_copilot import ("
new_imports = """import asyncio
from src.platforms.streamate.stream_monitor_controller import (
    parse_gold_menu_text,
    parse_wheel_game_text,
    update_gold_menu_live,
    update_wheel_game_live,
    update_room_topic_live
)
from src.analytics.streamate_competitor_radar import scan_streamate_tomboy_competitors

from src.agents.roxanne_multimodel_copilot import ("""

if "from src.platforms.streamate.stream_monitor_controller import" not in content:
    content = content.replace(import_anchor, new_imports, 1)
    print("Added stream_monitor_controller and competitor radar imports!")

# 2. Add Routes in do_GET and do_POST
get_route_anchor = 'elif self.path.startswith("/api/positioning"):\n            self.handle_api_positioning()'
new_get_route = """elif self.path.startswith("/api/positioning"):
            self.handle_api_positioning()
        elif self.path.startswith("/api/streamate/analyze_tomboy_radar"):
            self.handle_api_streamate_analyze_tomboy_radar()"""

if "/api/streamate/analyze_tomboy_radar" not in content and get_route_anchor in content:
    content = content.replace(get_route_anchor, new_get_route, 1)
    print("Added GET route for /api/streamate/analyze_tomboy_radar")

post_route_anchor = 'elif self.path.startswith("/api/deploy_profile"):\n            self.handle_api_deploy_profile()'
new_post_route = """elif self.path.startswith("/api/deploy_profile"):
            self.handle_api_deploy_profile()
        elif self.path == "/api/streamate/update_gold_menu":
            self.handle_api_streamate_update_gold_menu()
        elif self.path == "/api/streamate/update_wheel":
            self.handle_api_streamate_update_wheel()
        elif self.path == "/api/streamate/update_topic":
            self.handle_api_streamate_update_topic()
        elif self.path == "/api/streamate/analyze_tomboy_radar":
            self.handle_api_streamate_analyze_tomboy_radar()"""

if "update_gold_menu" not in content and post_route_anchor in content:
    content = content.replace(post_route_anchor, new_post_route, 1)
    print("Added POST routes for stream monitor actions!")

# 3. Add Handler Methods to VelvetRequestHandler
handlers_code = """
    def handle_api_streamate_update_gold_menu(self):
        \"\"\"Actualiza el menú GOLD en SM Connect / Stream Monitor.\"\"\"
        try:
            content_length = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(content_length).decode("utf-8")
            data = json.loads(body) if body else {}

            raw_text = data.get("raw_text", "")
            items = data.get("items", [])

            if raw_text and not items:
                items = parse_gold_menu_text(raw_text)

            res = asyncio.run(update_gold_menu_live(items))
            self.send_response(200 if res.get("success") else 400)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.end_headers()
            self.wfile.write(json.dumps(res, ensure_ascii=False).encode("utf-8"))
        except Exception as e:
            self.send_response(500)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.end_headers()
            self.wfile.write(json.dumps({"success": False, "error": str(e)}).encode("utf-8"))

    def handle_api_streamate_update_wheel(self):
        \"\"\"Actualiza la Ruleta (Gira La Rueda) en SM Connect / Stream Monitor.\"\"\"
        try:
            content_length = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(content_length).decode("utf-8")
            data = json.loads(body) if body else {}

            raw_text = data.get("raw_text", "")
            cost = data.get("cost", 20)
            items = data.get("items", [])

            if raw_text and not items:
                parsed = parse_wheel_game_text(raw_text)
                cost = parsed["cost"]
                items = parsed["items"]

            res = asyncio.run(update_wheel_game_live(cost, items))
            self.send_response(200 if res.get("success") else 400)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.end_headers()
            self.wfile.write(json.dumps(res, ensure_ascii=False).encode("utf-8"))
        except Exception as e:
            self.send_response(500)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.end_headers()
            self.wfile.write(json.dumps({"success": False, "error": str(e)}).encode("utf-8"))

    def handle_api_streamate_update_topic(self):
        \"\"\"Actualiza el Tema de Habitación (Room Topic) en SM Connect.\"\"\"
        try:
            content_length = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(content_length).decode("utf-8")
            data = json.loads(body) if body else {}

            topic = data.get("topic", "").strip()
            res = asyncio.run(update_room_topic_live(topic))
            self.send_response(200 if res.get("success") else 400)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.end_headers()
            self.wfile.write(json.dumps(res, ensure_ascii=False).encode("utf-8"))
        except Exception as e:
            self.send_response(500)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.end_headers()
            self.wfile.write(json.dumps({"success": False, "error": str(e)}).encode("utf-8"))

    def handle_api_streamate_analyze_tomboy_radar(self):
        \"\"\"Ejecuta escaneo de competidoras tomboy en Streamate y devuelve métricas.\"\"\"
        try:
            res = asyncio.run(scan_streamate_tomboy_competitors(3))
            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.end_headers()
            self.wfile.write(json.dumps({"success": True, "radar": res}, ensure_ascii=False).encode("utf-8"))
        except Exception as e:
            self.send_response(500)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.end_headers()
            self.wfile.write(json.dumps({"success": False, "error": str(e)}).encode("utf-8"))
"""

chat_handler_anchor = "    def handle_api_chat(self):"
if "def handle_api_streamate_update_gold_menu" not in content and chat_handler_anchor in content:
    content = content.replace(chat_handler_anchor, f"{handlers_code}\n{chat_handler_anchor}", 1)
    print("Added Stream Monitor API handlers to server!")

# 4. Enhance handle_api_chat with Intent Recognition
chat_prepare_anchor = "lang = detect_language(message)\n\n            # Preparar mensajes para Ollama / LLM"
new_chat_prepare = """lang = detect_language(message)
            msg_lower = message.lower()

            # DETECCIÓN DE INTENCIÓN: RADAR COMPETENCIA TOMBOY
            if ("analiza" in msg_lower or "radar" in msg_lower or "competencia" in msg_lower or "tendencia" in msg_lower) and \\
               ("tomboy" in msg_lower or "streamate" in msg_lower or "streetmate" in msg_lower or "streaming" in msg_lower):
                try:
                    radar_data = asyncio.run(scan_streamate_tomboy_competitors(3))
                    radar_summary = json.dumps(radar_data, ensure_ascii=False)
                    chat_history.append({
                        "role": "system",
                        "content": f"[RADAR TOMBOY STREAMATE EN VIVO]: {radar_summary}. Presenta a Sam un desglose claro de modelos activas, temas de sala que están usando, tarifas promedio ($2.99 / $3.99) y recomendaciones clave para destacar hoy."
                    })
                except Exception as re:
                    print("[Radar Error]:", re)

            # DETECCIÓN DE INTENCIÓN: ACTUALIZAR MENÚ GOLD
            elif ("menú gold" in msg_lower or "menu gold" in msg_lower) and ("actualiza" in msg_lower or "cambia" in msg_lower or "-" in message):
                try:
                    parsed_items = parse_gold_menu_text(message)
                    if len(parsed_items) >= 3:
                        res_up = asyncio.run(update_gold_menu_live(parsed_items))
                        chat_history.append({
                            "role": "system",
                            "content": f"[ACCIÓN EN VIVO]: Menú GOLD inyectado en Stream Monitor: {json.dumps(res_up, ensure_ascii=False)}. Confírmale a Sam las opciones y precios que quedaron guardados."
                        })
                except Exception as ge:
                    print("[Gold Menu Update Error]:", ge)

            # DETECCIÓN DE INTENCIÓN: ACTUALIZAR RULETA
            elif ("ruleta" in msg_lower or "gira la rueda" in msg_lower or "rueda" in msg_lower) and ("actualiza" in msg_lower or "cambia" in msg_lower or "pon" in msg_lower):
                try:
                    parsed_wheel = parse_wheel_game_text(message)
                    if len(parsed_wheel["items"]) >= 8:
                        res_wh = asyncio.run(update_wheel_game_live(parsed_wheel["cost"], parsed_wheel["items"]))
                        chat_history.append({
                            "role": "system",
                            "content": f"[ACCIÓN EN VIVO]: Ruleta inyectada en Stream Monitor: {json.dumps(res_wh, ensure_ascii=False)}. Confírmale a Sam el costo en Gold y las opciones seleccionadas."
                        })
                except Exception as we:
                    print("[Wheel Update Error]:", we)

            # DETECCIÓN DE INTENCIÓN: ACTUALIZAR TEMA DE HABITACIÓN
            elif ("tema de sala" in msg_lower or "tema de habitación" in msg_lower or "room topic" in msg_lower) and ("actualiza" in msg_lower or "cambia" in msg_lower or "pon" in msg_lower):
                try:
                    clean_topic = message.split(":", 1)[-1].strip() if ":" in message else message
                    res_tp = asyncio.run(update_room_topic_live(clean_topic))
                    chat_history.append({
                        "role": "system",
                        "content": f"[ACCIÓN EN VIVO]: Tema de habitación actualizado en Stream Monitor: {json.dumps(res_tp, ensure_ascii=False)}. Confírmale a Sam el nuevo tema activo."
                    })
                except Exception as te:
                    print("[Topic Update Error]:", te)

            # Preparar mensajes para Ollama / LLM"""

if "DETECCIÓN DE INTENCIÓN: RADAR COMPETENCIA TOMBOY" not in content and chat_prepare_anchor in content:
    content = content.replace(chat_prepare_anchor, new_chat_prepare, 1)
    print("Enhanced handle_api_chat with intent recognition!")

server_file.write_text(content, encoding="utf-8")
print("Saved updated velvet_app_server.py!")
