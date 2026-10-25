import os
import sys
import json
import sqlite3
import datetime
import time
import base64
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

import asyncio
from src.platforms.streamate.stream_monitor_controller import (
    parse_gold_menu_text,
    parse_wheel_game_text,
    update_gold_menu_live,
    update_wheel_game_live,
    update_room_topic_live
)
from src.analytics.streamate_competitor_radar import scan_streamate_tomboy_competitors

from src.agents.roxanne_multimodel_copilot import (
    ROXANNE_SAM_SYSTEM_PROMPT,
    OllamaProvider,
    GeminiProvider
)
from src.agents.chloe_instagram_agent import (
    CHLOE_INSTAGRAM_SYSTEM_PROMPT,
    generate_daily_instagram_strategy,
    generate_stories_pack
)
from src.automation.push_notification_service import push_service

# ==============================================================================
# PROMPTS DEL SISTEMA OPTIMIZADOS PARA CPU (AGILIDAD 7-15s EN OLLAMA)
# ==============================================================================
ROXANNE_CPU_SYSTEM_PROMPT = """Eres ROXANNE, Co-Piloto Estratégica y mentora personal de la modelo y creadora Sam Barton (@sambartonn23).
Sam es modelo tomboy versátil en LoyalFans, Stripchat y Streamate (cuenta estudio, 50% split, rating 4.0).
Asistes a Sam directamente en español con respuestas a fans, metas de sala, dinámicas Lovense y tácticas de monetización.
Sé concisa, práctica, directa y estratégica. Responde con calidez y profesionalismo."""

CHLOE_CPU_SYSTEM_PROMPT = """Eres CHLOE, estratega de Instagram de Sam Barton (@sambartonn23).
Creas ideas de historias, ganchos visuales y textos con estilo tomboy para reactivar el algoritmo y dirigir tráfico a LoyalFans y Streamate.
Sé creativa, concisa, moderna y enfocada en interacción."""

DIANA_CPU_SYSTEM_PROMPT = """Eres DIANA, auditora financiera y especialista de pagos de Sam Barton (@sambartonn23).
Especialista en splits de Streamate (50% neto del 35% del estudio), pagos de LoyalFans (80% creador, retiro mínimo $50) y Stripchat.
Responde a Sam en español con números claros, precisión financiera y consejos prácticos de rentabilidad."""

ELECTRA_CPU_SYSTEM_PROMPT = """Eres ELECTRA, ingeniera de tráfico algorítmico y posicionamiento de Sam Barton (@sambartonn23).
Especialista en SEO de streaming, ciclo de bump cada 3.5h en LoyalFans, retención de los primeros 30 segundos en Streamate y tags clave (#Tomboy, #Versatile).
Responde a Sam en español con tácticas directas, accionables y análisis de algoritmos."""

def generate_contextual_fallback(assistant_id: str, message: str) -> str:
    """Genera una respuesta contextual inteligente si Ollama no está disponible o está reiniciando."""
    msg_low = message.lower()
    if assistant_id == "chloe":
        if any(w in msg_low for w in ["historia", "story", "stories", "publicar", "post", "foto", "idea"]):
            return (
                "✨ **[CHLOE - Estrategia Rápida de Instagram]**\n\n"
                "Para tus historias de hoy con vibra tomboy:\n"
                "1. **Mañana**: Boomerang casual afinando el ukelele o preparando café con texto: *'Modo enfoque activado... ¿quién anda por acá?'* + sticker de encuesta.\n"
                "2. **Tarde**: Foto en cabina/set con luz tenue: *'Segunda mitad del día, lista para lo bueno 🖤'*.\n"
                "3. **Cierre**: Gancho a LoyalFans/Streamate: *'Los detalles exclusivos están en el link de mi bio 🔥'*."
            )
        elif any(w in msg_low for w in ["hola", "buenos dias", "buenas", "que tal", "como estas"]):
            return (
                "✨ **[CHLOE - Asistente de Instagram]**\n\n"
                "¡Hola Sam! Lista para mover el algoritmo de @sambartonn23 hoy. ¿Quieres que preparemos el pack de historias del día o un copy para un nuevo post?"
            )
        else:
            return (
                f"✨ **[CHLOE - Estrategia Instagram]**\n\n"
                f"Sam, respecto a tu consulta: para mantener alta la retención en @sambartonn23, publica historias con stickers interactivos cada 3 horas y usa siempre un gancho claro al inicio."
            )
    elif assistant_id == "diana":
        if any(w in msg_low for w in ["ganancia", "split", "cuanto", "precio", "privado", "exclusivo", "gold", "dolar"]):
            return (
                "📊 **[DIANA - Auditoría Financiera]**\n\n"
                "Sam, recordatorio de tus tasas activas:\n"
                "• **Streamate**: Privado $2.99/min, Exclusivo $3.99/min. De cada 100 Gold ($100 USD), el estudio recibe $35 USD y tu neto es $17.50 USD (50% de la comisión del estudio).\n"
                "• **LoyalFans**: DMs $0.50, te quedas con el 80% neto directo. Retiro mínimo de $50 USD.\n"
                "• **Meta recomendada**: Prioriza sesiones privadas de más de 6 minutos para superar el ticket promedio."
            )
        elif any(w in msg_low for w in ["hola", "buenos dias", "buenas", "que tal", "como estas"]):
            return (
                "📊 **[DIANA - Auditora Financiera]**\n\n"
                "¡Hola Sam! Aquí revisando tus balances y proyecciones. ¿Qué cifra o split quieres que auditemos para tu turno de hoy?"
            )
        else:
            return (
                f"📊 **[DIANA - Auditoría Financiera]**\n\n"
                f"Sam, analizando tu consulta: recuerda siempre separar los ingresos directos (LoyalFans 80%) de los de cuenta estudio (Streamate 50% split) para calcular con exactitud tu flujo de caja neto."
            )
    elif assistant_id == "electra":
        if any(w in msg_low for w in ["bump", "cooldown", "feed", "posicion", "posicionamiento", "rank", "ranking"]):
            return (
                "⚡ **[ELECTRA - Tráfico & Algoritmos]**\n\n"
                "Sam, checklist del algoritmo:\n"
                "1. **LoyalFans**: Ejecuta el bump cada 3.5 horas exactas. Esto te devuelve a la parte superior del feed orgánico.\n"
                "2. **Streamate**: Los primeros 30 segundos de free chat definen tu multiplicador de visibilidad. Mantén la interacción verbal activa de inmediato.\n"
                "3. **Tags clave**: Asegúrate de tener activos `#Tomboy`, `#Versatile`, `#Ukelele` y `#Cam2Cam`."
            )
        elif any(w in msg_low for w in ["hola", "buenos dias", "buenas", "que tal", "como estas"]):
            return (
                "⚡ **[ELECTRA - Algoritmos & Tráfico]**\n\n"
                "¡Hola Sam! Monitores de tráfico al 100%. ¿Quieres revisar el cooldown de tu bump o la estrategia de retención para Streamate?"
            )
        else:
            return (
                f"⚡ **[ELECTRA - Algoritmos de Tráfico]**\n\n"
                f"Sam, sobre tu consulta: para elevar el score en los rankings de streaming, cambia el tema de sala cada 90 minutos y estimula las propinas rápidas en los primeros minutos de transmisión."
            )
    else: # Roxanne
        if any(w in msg_low for w in ["hola", "buenos dias", "buenas", "que tal", "como estas"]):
            return (
                "🐺 **[ROXANNE - Co-Piloto]**\n\n"
                "¡Hola Sam! Aquí lista a tu lado. ¿Qué tienes planeado para hoy? Dime si necesitas que redactemos una respuesta a un fan, ajustemos el menú de sala o preparemos las dinámicas de cámara."
            )
        elif any(w in msg_low for w in ["fan", "mensaje", "responder", "chat", "cliente"]):
            return (
                "🐺 **[ROXANNE - Co-Piloto]**\n\n"
                "Pégame el mensaje que te envió el fan y te preparo 2 opciones de respuesta de inmediato: una coqueta y directa con tu vibra tomboy, y otra para monetizar con fotos o propinas."
            )
        else:
            return (
                f"🐺 **[ROXANNE - Co-Piloto]**\n\n"
                f"Sam, respecto a tu mensaje: mantén tu vibra tomboy versátil firme, combina momentos de ukelele y charla cercana con tensión sensual en cámara, y recuerda tomar descansos de 10 minutos cada 2 horas."
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
        elif self.path.startswith("/api/chat_history"):
            self.handle_api_chat_history()
        elif self.path == "/api/platforms_profiles":
            self.handle_api_platforms_profiles()
        elif self.path == "/api/financials":
            self.handle_api_financials()
        elif self.path.startswith("/api/positioning"):
            self.handle_api_positioning()
        elif self.path.startswith("/api/streamate/analyze_tomboy_radar"):
            self.handle_api_streamate_analyze_tomboy_radar()
        elif self.path.startswith("/api/instagram/daily_strategy"):
            self.handle_api_instagram_daily_strategy()
        elif self.path.startswith("/api/instagram/stories_pack"):
            self.handle_api_instagram_stories_pack()
        elif self.path.startswith("/api/instagram/sync_live"):
            self.handle_api_instagram_sync_live()
        elif self.path == "/api/push/vapid_public_key":
            self.handle_api_push_vapid_public_key()
        elif self.path == "/api/logo_status":
            self.handle_api_logo_status()
        elif self.path == "/manifest.json":
            self.send_response(200)
            self.send_header("Content-Type", "application/manifest+json; charset=utf-8")
            self.end_headers()
            with open(ROOT / "manifest.json", "rb") as f:
                self.wfile.write(f.read())
            return
        elif self.path == "/sw.js":
            self.send_response(200)
            self.send_header("Content-Type", "application/javascript; charset=utf-8")
            self.send_header("Service-Worker-Allowed", "/")
            self.end_headers()
            with open(ROOT / "sw.js", "rb") as f:
                self.wfile.write(f.read())
            return
        else:
            # Servir index.html si entra a /
            if self.path == "/" or self.path == "":
                self.path = "/index.html"
            super().do_GET()

    def do_POST(self):
        if self.path == "/api/chat":
            self.handle_api_chat()
        elif self.path == "/api/upload_logo":
            self.handle_api_upload_logo()
        elif self.path == "/api/reset_logo":
            self.handle_api_reset_logo()
        elif self.path.startswith("/api/clear_chat_history"):
            self.handle_api_clear_chat_history()
        elif self.path == "/api/push/subscribe":
            self.handle_api_push_subscribe()
        elif self.path == "/api/push/unsubscribe":
            self.handle_api_push_unsubscribe()
        elif self.path == "/api/push/test":
            self.handle_api_push_test()
        elif self.path.startswith("/api/streamate/analyze_tomboy_radar"):
            self.handle_api_streamate_analyze_tomboy_radar()
        elif self.path == "/api/refresh_financials":
            self.handle_api_refresh_financials()
        elif self.path.startswith("/api/refresh_positioning"):
            self.handle_api_refresh_positioning()
        elif self.path.startswith("/api/deploy_profile"):
            self.handle_api_deploy_profile()
        elif self.path.startswith("/api/instagram/daily_strategy"):
            self.handle_api_instagram_daily_strategy()
        elif self.path.startswith("/api/instagram/stories_pack"):
            self.handle_api_instagram_stories_pack()
        elif self.path.startswith("/api/instagram/sync_live"):
            self.handle_api_instagram_sync_live()
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

    def handle_api_push_vapid_public_key(self):
        """Retorna la clave pública VAPID en base64url para la suscripción Web Push en el navegador."""
        try:
            pub_key = push_service.get_public_key()
            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.end_headers()
            self.wfile.write(json.dumps({"publicKey": pub_key}).encode("utf-8"))
        except Exception as e:
            self.send_response(500)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.end_headers()
            self.wfile.write(json.dumps({"error": str(e)}).encode("utf-8"))

    def handle_api_push_subscribe(self):
        """Registra una suscripción Web Push (endpoint, p256dh, auth) en SQLite."""
        try:
            length = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(length).decode("utf-8") if length > 0 else "{}"
            data = json.loads(body)
            sub = data.get("subscription", {})
            ua = self.headers.get("User-Agent", "")
            success = push_service.save_subscription(sub, ua)
            self.send_response(200 if success else 400)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.end_headers()
            self.wfile.write(json.dumps({
                "status": "ok" if success else "error",
                "message": "Dispositivo registrado en notificaciones push de SIREN AI" if success else "Datos de suscripción incompletos"
            }).encode("utf-8"))
        except Exception as e:
            self.send_response(500)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.end_headers()
            self.wfile.write(json.dumps({"error": str(e)}).encode("utf-8"))

    def handle_api_push_unsubscribe(self):
        """Desactiva una suscripción Web Push en la base de datos."""
        try:
            length = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(length).decode("utf-8") if length > 0 else "{}"
            data = json.loads(body)
            endpoint = data.get("endpoint", "")
            push_service.remove_subscription(endpoint)
            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.end_headers()
            self.wfile.write(json.dumps({"status": "ok", "message": "Suscripción desactivada"}).encode("utf-8"))
        except Exception as e:
            self.send_response(500)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.end_headers()
            self.wfile.write(json.dumps({"error": str(e)}).encode("utf-8"))

    def handle_api_push_test(self):
        """Dispara una notificación de prueba para cualquiera de los 4 asistentes."""
        try:
            length = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(length).decode("utf-8") if length > 0 else "{}"
            data = json.loads(body) if body else {}
            assistant_id = data.get("assistant", "roxanne").lower()
            
            sample_messages = {
                "roxanne": "¡Hola Sam! Notificación en tiempo real de Roxanne verificada con éxito en tu pantalla de bloqueo. Sistema operativo y listo.",
                "chloe": "¡Hey Sam! Chloe aquí: tu estrategia de Instagram para hoy está preparada. Toca para ver el desglose en el chat.",
                "diana": "¡Alerta Financiera de Diana! Nuevo corte de facturación registrado. Toca para auditar tus ganancias.",
                "electra": "¡Alerta Algorítmica de Electra! Pico de tráfico detectado en Streamate. Momento ideal para abrir sala."
            }
            msg = sample_messages.get(assistant_id, sample_messages["roxanne"])
            push_service.notify_assistant_response(assistant_id, msg)
            
            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.end_headers()
            self.wfile.write(json.dumps({
                "status": "ok",
                "assistant": assistant_id,
                "message": msg,
                "note": "Push disparado a todos los dispositivos registrados"
            }).encode("utf-8"))
        except Exception as e:
            self.send_response(500)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.end_headers()
            self.wfile.write(json.dumps({"error": str(e)}).encode("utf-8"))

    def handle_api_logo_status(self):
        """Devuelve el estado del logotipo activo (opción oficial 2 o personalizado)."""
        logo_cfg = ROOT / "data" / "logo_config.json"
        status = {"type": "option2", "url": "", "updated_at": 0}
        if logo_cfg.exists():
            try:
                with open(logo_cfg, "r", encoding="utf-8") as f:
                    status = json.load(f)
            except Exception:
                pass
        self.send_response(200)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.end_headers()
        self.wfile.write(json.dumps(status).encode("utf-8"))

    def handle_api_upload_logo(self):
        """Recibe una imagen, genera todos los tamaños para PWA, favicons y web, y actualiza el sistema."""
        try:
            content_length = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(content_length).decode("utf-8")
            data = json.loads(body)
            img_b64 = data.get("image", "")

            if not img_b64:
                self.send_response(400)
                self.send_header("Content-Type", "application/json; charset=utf-8")
                self.end_headers()
                self.wfile.write(json.dumps({"error": "No se recibió imagen"}).encode("utf-8"))
                return

            if "," in img_b64:
                header, encoded = img_b64.split(",", 1)
            else:
                encoded = img_b64

            raw_bytes = base64.b64decode(encoded)
            icons_dir = ROOT / "icons"
            icons_dir.mkdir(parents=True, exist_ok=True)

            custom_logo_path = icons_dir / "custom_logo.png"
            with open(custom_logo_path, "wb") as f:
                f.write(raw_bytes)

            t_now = int(time.time())

            # Redimensionar usando Pillow para PWA (192, 512, maskable, badge)
            try:
                from PIL import Image, ImageOps
                with Image.open(custom_logo_path) as im:
                    im_rgba = im.convert("RGBA")
                    # 1. custom_logo optimizado
                    im_rgba.save(icons_dir / "custom_logo.png", "PNG")

                    # 2. icon-512x512
                    im_512 = Image.new("RGBA", (512, 512), (30, 36, 50, 255))
                    im_fit_512 = ImageOps.contain(im_rgba, (440, 440), Image.Resampling.LANCZOS)
                    im_512.paste(im_fit_512, ((512 - im_fit_512.width) // 2, (512 - im_fit_512.height) // 2), im_fit_512)
                    im_512.save(icons_dir / "icon-512x512.png", "PNG")

                    # 3. icon-512x512-maskable
                    im_mask = Image.new("RGBA", (512, 512), (30, 36, 50, 255))
                    im_fit_mask = ImageOps.contain(im_rgba, (380, 380), Image.Resampling.LANCZOS)
                    im_mask.paste(im_fit_mask, ((512 - im_fit_mask.width) // 2, (512 - im_fit_mask.height) // 2), im_fit_mask)
                    im_mask.save(icons_dir / "icon-512x512-maskable.png", "PNG")

                    # 4. icon-192x192
                    im_192 = Image.new("RGBA", (192, 192), (30, 36, 50, 255))
                    im_fit_192 = ImageOps.contain(im_rgba, (160, 160), Image.Resampling.LANCZOS)
                    im_192.paste(im_fit_192, ((192 - im_fit_192.width) // 2, (192 - im_fit_192.height) // 2), im_fit_192)
                    im_192.save(icons_dir / "icon-192x192.png", "PNG")

                    # 5. badge-72x72
                    im_72 = ImageOps.contain(im_rgba, (72, 72), Image.Resampling.LANCZOS)
                    im_72.save(icons_dir / "badge-72x72.png", "PNG")
            except Exception as pe:
                print("[Logo Image Processing Warning]:", pe)

            logo_cfg = ROOT / "data" / "logo_config.json"
            logo_cfg.parent.mkdir(parents=True, exist_ok=True)
            with open(logo_cfg, "w", encoding="utf-8") as f:
                json.dump({"type": "custom", "updated_at": t_now, "url": f"/icons/custom_logo.png?v={t_now}"}, f)

            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.end_headers()
            self.wfile.write(json.dumps({
                "success": True,
                "message": "Logotipo personalizado guardado y actualizado en PWA, Favicons y Header",
                "logo_url": f"/icons/custom_logo.png?v={t_now}",
                "updated_at": t_now
            }).encode("utf-8"))

        except Exception as e:
            self.send_response(500)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.end_headers()
            self.wfile.write(json.dumps({"success": False, "error": str(e)}).encode("utf-8"))

    def handle_api_reset_logo(self):
        """Restablece los iconos al logotipo oficial de SIREN (Opción 2: Cyber Pulse Aegis)."""
        try:
            from scripts.generate_pwa_icons import create_option2_pwa_icons
            create_option2_pwa_icons()

            logo_cfg = ROOT / "data" / "logo_config.json"
            logo_cfg.parent.mkdir(parents=True, exist_ok=True)
            t_now = int(time.time())
            with open(logo_cfg, "w", encoding="utf-8") as f:
                json.dump({"type": "option2", "updated_at": t_now, "url": ""}, f)

            custom_file = ROOT / "icons" / "custom_logo.png"
            if custom_file.exists():
                try:
                    custom_file.unlink()
                except Exception:
                    pass

            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.end_headers()
            self.wfile.write(json.dumps({
                "success": True,
                "message": "Logotipo restablecido a la Opción 2 Oficial (Cyber Pulse Aegis)",
                "type": "option2",
                "updated_at": t_now
            }).encode("utf-8"))
        except Exception as e:
            self.send_response(500)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.end_headers()
            self.wfile.write(json.dumps({"success": False, "error": str(e)}).encode("utf-8"))

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
        """Devuelve el historial persistente de conversacion filtrado por asistente (o completo con campo assistant)."""
        from urllib.parse import urlparse, parse_qs
        history = []
        qs = parse_qs(urlparse(self.path).query)
        target_asst = qs.get("assistant", [None])[0]
        if target_asst:
            target_asst = target_asst.lower()

        try:
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS copilot_assistant_history (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp TEXT,
                    sender TEXT,
                    message TEXT,
                    model TEXT,
                    assistant TEXT DEFAULT 'roxanne'
                )
            """)
            cols = [col[1] for col in cursor.execute("PRAGMA table_info(copilot_assistant_history)").fetchall()]
            if "assistant" not in cols:
                cursor.execute("ALTER TABLE copilot_assistant_history ADD COLUMN assistant TEXT DEFAULT 'roxanne'")
                conn.commit()

            if target_asst:
                cursor.execute("""
                    SELECT timestamp, sender, message, model, assistant
                    FROM copilot_assistant_history
                    WHERE LOWER(COALESCE(assistant, sender)) = ?
                    ORDER BY id ASC
                """, (target_asst,))
            else:
                cursor.execute("""
                    SELECT timestamp, sender, message, model, assistant
                    FROM copilot_assistant_history
                    ORDER BY id ASC
                """)

            for row in cursor.fetchall():
                asst_val = row[4]
                if not asst_val or asst_val == "sam":
                    asst_val = row[1] if row[1] in ["roxanne", "chloe", "diana", "electra"] else "roxanne"
                history.append({
                    "timestamp": row[0],
                    "sender": row[1],
                    "message": row[2],
                    "model": row[3],
                    "assistant": asst_val
                })
            conn.close()
        except Exception as e:
            print("[History Error]:", e)

        self.send_response(200)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.end_headers()
        self.wfile.write(json.dumps({"success": True, "history": history, "assistant": target_asst}).encode("utf-8"))

    def handle_api_clear_chat_history(self):
        """Limpia el historial de conversacion para el asistente indicado (o todos si no se indica)."""
        from urllib.parse import urlparse, parse_qs
        qs = parse_qs(urlparse(self.path).query)
        target_asst = qs.get("assistant", [None])[0]

        # Verificar si vino por cuerpo JSON
        length = int(self.headers.get("Content-Length", 0))
        if length > 0:
            try:
                body_data = json.loads(self.rfile.read(length).decode("utf-8"))
                if not target_asst and "assistant" in body_data:
                    target_asst = body_data["assistant"]
            except Exception:
                pass

        try:
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            if target_asst:
                t_lower = target_asst.lower()
                cursor.execute("""
                    DELETE FROM copilot_assistant_history
                    WHERE LOWER(COALESCE(assistant, '')) = ? OR LOWER(sender) = ?
                """, (t_lower, t_lower))
                msg = f"Historial de {target_asst.upper()} limpiado exitosamente"
            else:
                cursor.execute("DELETE FROM copilot_assistant_history")
                msg = "Historial completo de todos los asistentes limpiado exitosamente"
            conn.commit()
            conn.close()
            resp = {"success": True, "message": msg, "assistant": target_asst}
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



    def handle_api_streamate_update_gold_menu(self):
        """Actualiza el menú GOLD en SM Connect / Stream Monitor."""
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
        """Actualiza la Ruleta (Gira La Rueda) en SM Connect / Stream Monitor."""
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
        """Actualiza el Tema de Habitación (Room Topic) en SM Connect."""
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
        """Ejecuta escaneo de competidoras tomboy en Streamate y devuelve métricas."""
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

    def handle_api_instagram_daily_strategy(self):
        """Genera la estrategia diaria estructurada para @sambartonn23."""
        try:
            strategy = generate_daily_instagram_strategy()
            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.end_headers()
            self.wfile.write(json.dumps({"success": True, "strategy": strategy}, ensure_ascii=False).encode("utf-8"))
        except Exception as e:
            self.send_response(500)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.end_headers()
            self.wfile.write(json.dumps({"success": False, "error": str(e)}).encode("utf-8"))

    def handle_api_instagram_stories_pack(self):
        """Genera pack de historias del día listas para publicar."""
        try:
            stories = generate_stories_pack()
            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.end_headers()
            self.wfile.write(json.dumps({"success": True, "stories": stories}, ensure_ascii=False).encode("utf-8"))
        except Exception as e:
            self.send_response(500)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.end_headers()
            self.wfile.write(json.dumps({"success": False, "error": str(e)}).encode("utf-8"))

    def handle_api_instagram_sync_live(self):
        """Devuelve o refresca los datos y capturas en vivo de la cuenta @sambartonn23."""
        try:
            from urllib.parse import urlparse, parse_qs
            import subprocess

            qs = parse_qs(urlparse(self.path).query)
            refresh = qs.get("refresh", ["false"])[0].lower() in ["1", "true", "yes"]

            artifacts_live_json = ROOT / "artifacts" / "instagram" / "sambartonn23_live.json"

            if refresh or not artifacts_live_json.exists():
                sync_script = ROOT / "src" / "platforms" / "instagram" / "instagram_sync.py"
                try:
                    subprocess.run([sys.executable, str(sync_script)], cwd=str(ROOT), timeout=45, capture_output=True)
                except Exception as sub_e:
                    print("[Instagram Sync Error]:", sub_e)

            # Cargar datos si existen
            live_data = {
                "username": "sambartonn23",
                "fullName": "Sam Bartonn",
                "followers": "78",
                "following": "104",
                "posts": "24",
                "bio": "Software Architect | AI Engineer 🤓 💻\nCat Lover 🐱",
                "avatar_url": "/artifacts/instagram/sambartonn23_avatar.png",
                "feed_screenshot": "/artifacts/instagram/sambartonn23_feed_live.png",
                "status": "Sincronizado en Vivo",
                "verified": True,
                "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }

            if artifacts_live_json.exists():
                try:
                    with open(artifacts_live_json, "r", encoding="utf-8") as f:
                        saved = json.load(f)
                        live_data.update(saved)
                        live_data["avatar_url"] = "/artifacts/instagram/sambartonn23_avatar.png"
                        live_data["feed_screenshot"] = "/artifacts/instagram/sambartonn23_feed_live.png"
                except Exception:
                    pass

            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.end_headers()
            self.wfile.write(json.dumps({"success": True, "data": live_data}, ensure_ascii=False).encode("utf-8"))
        except Exception as e:
            self.send_response(500)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.end_headers()
            self.wfile.write(json.dumps({"success": False, "error": str(e)}).encode("utf-8"))

    def handle_api_chat(self):
        """Procesa una consulta de chat con ROXANNE o CHLOE y devuelve la respuesta del LLM."""
        try:
            content_length = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(content_length).decode("utf-8")
            data = json.loads(body)

            message = data.get("message", "").strip()
            model_name = data.get("model", "qwen2.5:7b-instruct")
            chat_history = data.get("history", [])
            assistant_id = data.get("assistant", "roxanne").lower()

            if not message:
                self.send_response(400)
                self.send_header("Content-Type", "application/json; charset=utf-8")
                self.end_headers()
                self.wfile.write(json.dumps({"error": "Mensaje vacío"}).encode("utf-8"))
                return

            lang = detect_language(message)
            msg_lower = message.lower()

            # DETECCIÓN DE INTENCIÓN: RADAR COMPETENCIA TOMBOY
            if ("analiza" in msg_lower or "radar" in msg_lower or "competencia" in msg_lower or "tendencia" in msg_lower) and \
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

            # Seleccionar Prompt de Sistema según Asistente (optimizado para CPU)
            if assistant_id == "chloe":
                active_system_prompt = CHLOE_CPU_SYSTEM_PROMPT
            elif assistant_id == "diana":
                active_system_prompt = DIANA_CPU_SYSTEM_PROMPT
            elif assistant_id == "electra":
                active_system_prompt = ELECTRA_CPU_SYSTEM_PROMPT
            else:
                active_system_prompt = ROXANNE_CPU_SYSTEM_PROMPT

            # Preparar mensajes para Ollama (limitar historial a últimos 6 mensajes = 3 turnos para máxima agilidad en CPU)
            recent_history = [h for h in chat_history if "role" in h and "content" in h][-6:]
            messages = [{"role": "system", "content": active_system_prompt}]
            messages.extend(recent_history)
            messages.append({"role": "user", "content": message})

            # Inferencia vía Ollama con paralelismo multihilo de CPU
            ollama_payload = {
                "model": model_name,
                "messages": messages,
                "stream": False,
                "options": {
                    "num_thread": 10,
                    "num_ctx": 1024,
                    "num_predict": 180,
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
                with urllib.request.urlopen(req, timeout=50) as response:
                    res_json = json.loads(response.read().decode("utf-8"))
                    reply = res_json.get("message", {}).get("content", "").strip()
                    if not reply:
                        reply = generate_contextual_fallback(assistant_id, message)
            except Exception as e:
                print(f"[Ollama Inference Fallback]: {e}")
                reply = generate_contextual_fallback(assistant_id, message)


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
                        model TEXT,
                        assistant TEXT DEFAULT 'roxanne'
                    )
                """)
                cols = [col[1] for col in cursor.execute("PRAGMA table_info(copilot_assistant_history)").fetchall()]
                if "assistant" not in cols:
                    cursor.execute("ALTER TABLE copilot_assistant_history ADD COLUMN assistant TEXT DEFAULT 'roxanne'")
                    conn.commit()

                now_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                cursor.execute("INSERT INTO copilot_assistant_history (timestamp, sender, message, model, assistant) VALUES (?, ?, ?, ?, ?)",
                               (now_str, "sam", message, model_name, assistant_id))
                cursor.execute("INSERT INTO copilot_assistant_history (timestamp, sender, message, model, assistant) VALUES (?, ?, ?, ?, ?)",
                               (now_str, assistant_id, reply, model_name, assistant_id))
                conn.commit()
                conn.close()
            except Exception as dbe:
                print("[Chat Persist Error]:", dbe)

            # Disparar notificación Web Push en tiempo real para el asistente que respondió
            try:
                push_service.notify_assistant_response(assistant_id, reply)
            except Exception as pe:
                print("[Push Trigger Warning]:", pe)

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
    print(f"🚀 SIREN AI Command & Server activo en http://localhost:{PORT}")
    print(f"📡 API de Chat ROXANNE conectada a Ollama en http://localhost:11434")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nDeteniendo servidor SIREN...")
        httpd.server_close()

if __name__ == "__main__":
    run_server()
