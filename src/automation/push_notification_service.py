"""
SIREN AI — Web Push Notification Service
Envío de notificaciones Web Push en tiempo real para los 4 asistentes IA de Sam Barton.
Compatible con PWA en Chrome para Android, pantalla de bloqueo, sonido y vibración.
"""
import os
import sys
import json
import sqlite3
import base64
import logging
import threading
from pathlib import Path
from py_vapid import Vapid
from cryptography.hazmat.primitives.serialization import Encoding, PublicFormat
import pywebpush

ROOT = Path(__file__).resolve().parent.parent.parent
DB_PATH = ROOT / "data" / "velvet_data.db"
VAPID_JSON_PATH = ROOT / "data" / "vapid_keys.json"
VAPID_PEM_PATH = ROOT / "data" / "private_key.pem"

os.makedirs(ROOT / "data", exist_ok=True)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("SIREN_PUSH")

# Configuración y Metadatos de los 4 Asistentes
ASSISTANT_CONFIG = {
    "roxanne": {
        "name": "ROXANNE",
        "title": "ROXANNE (Directora General)",
        "tag": "siren-asst-roxanne",
        "icon": "/icons/assistant-roxanne.png",
        "sound": "default"
    },
    "chloe": {
        "name": "CHLOE",
        "title": "CHLOE (Instagram & Redes)",
        "tag": "siren-asst-chloe",
        "icon": "/icons/assistant-chloe.png",
        "sound": "default"
    },
    "diana": {
        "name": "DIANA",
        "title": "DIANA (Auditora Financiera)",
        "tag": "siren-asst-diana",
        "icon": "/icons/assistant-diana.png",
        "sound": "default"
    },
    "electra": {
        "name": "ELECTRA",
        "title": "ELECTRA (Ingeniera de Algoritmos)",
        "tag": "siren-asst-electra",
        "icon": "/icons/assistant-electra.png",
        "sound": "default"
    }
}

class PushNotificationService:
    def __init__(self):
        self._init_db()
        self.vapid = self._init_vapid()

    def _init_db(self):
        """Inicializa la tabla de suscripciones en SQLite."""
        try:
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS push_subscriptions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    endpoint TEXT UNIQUE,
                    p256dh TEXT,
                    auth TEXT,
                    user_agent TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    is_active INTEGER DEFAULT 1
                )
            """)
            conn.commit()
            conn.close()
        except Exception as e:
            logger.error(f"Error inicializando base de datos de push: {e}")

    def _init_vapid(self) -> Vapid:
        """Carga o genera las claves VAPID persistentes."""
        vapid = Vapid()
        if VAPID_PEM_PATH.exists() and VAPID_JSON_PATH.exists():
            try:
                vapid = Vapid.from_file(str(VAPID_PEM_PATH))
                logger.info("✓ Claves VAPID existentes cargadas correctamente.")
                return vapid
            except Exception as e:
                logger.warning(f"Error cargando PEM existente ({e}). Regenerando claves VAPID...")

        # Generar nuevas claves VAPID
        vapid.generate_keys()
        vapid.save_key(str(VAPID_PEM_PATH))

        pub_bytes = vapid.public_key.public_bytes(
            encoding=Encoding.X962,
            format=PublicFormat.UncompressedPoint
        )
        pub_b64 = base64.urlsafe_b64encode(pub_bytes).decode('utf-8').rstrip('=')

        with open(VAPID_JSON_PATH, "w", encoding="utf-8") as f:
            json.dump({
                "publicKey": pub_b64,
                "subject": "mailto:admin@siren.ai"
            }, f, indent=2)

        logger.info(f"✓ Nuevas claves VAPID creadas. Clave pública: {pub_b64[:16]}...")
        return vapid

    def get_public_key(self) -> str:
        """Retorna la clave pública en base64url para el frontend."""
        pub_bytes = self.vapid.public_key.public_bytes(
            encoding=Encoding.X962,
            format=PublicFormat.UncompressedPoint
        )
        return base64.urlsafe_b64encode(pub_bytes).decode('utf-8').rstrip('=')

    def save_subscription(self, sub_data: dict, user_agent: str = "") -> bool:
        """Guarda o actualiza una suscripción Push recibida desde el navegador."""
        endpoint = sub_data.get("endpoint")
        keys = sub_data.get("keys", {})
        p256dh = keys.get("p256dh")
        auth = keys.get("auth")

        if not endpoint or not p256dh or not auth:
            logger.warning("Suscripción Push inválida o incompleta")
            return False

        try:
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO push_subscriptions (endpoint, p256dh, auth, user_agent, is_active)
                VALUES (?, ?, ?, ?, 1)
                ON CONFLICT(endpoint) DO UPDATE SET
                    p256dh = excluded.p256dh,
                    auth = excluded.auth,
                    user_agent = excluded.user_agent,
                    is_active = 1
            """, (endpoint, p256dh, auth, user_agent))
            conn.commit()
            conn.close()
            logger.info(f"✓ Suscripción Push guardada para {endpoint[:45]}...")
            return True
        except Exception as e:
            logger.error(f"Error guardando suscripción push: {e}")
            return False

    def remove_subscription(self, endpoint: str):
        """Marca como inactiva una suscripción dada de baja."""
        try:
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            cursor.execute("UPDATE push_subscriptions SET is_active = 0 WHERE endpoint = ?", (endpoint,))
            conn.commit()
            conn.close()
            logger.info(f"Suscripción Push desactivada: {endpoint[:45]}...")
        except Exception as e:
            logger.error(f"Error desactivando suscripción push: {e}")

    def get_active_subscriptions(self) -> list:
        """Obtiene todas las suscripciones activas."""
        try:
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            cursor.execute("SELECT id, endpoint, p256dh, auth FROM push_subscriptions WHERE is_active = 1")
            rows = cursor.fetchall()
            conn.close()
            return [
                {
                    "id": r[0],
                    "endpoint": r[1],
                    "keys": {
                        "p256dh": r[2],
                        "auth": r[3]
                    }
                }
                for r in rows
            ]
        except Exception as e:
            logger.error(f"Error consultando suscripciones: {e}")
            return []

    def send_push_to_all(self, payload: dict) -> dict:
        """Envía el payload push a todos los dispositivos suscritos."""
        subs = self.get_active_subscriptions()
        if not subs:
            logger.info("No hay dispositivos móviles suscritos actualmente.")
            return {"sent": 0, "failed": 0, "total": 0, "msg": "No hay suscripciones activas"}

        sent_count = 0
        failed_count = 0
        payload_str = json.dumps(payload)

        vapid_claims = {
            "sub": "mailto:admin@siren.ai"
        }

        for sub in subs:
            try:
                pywebpush.webpush(
                    subscription_info=sub,
                    data=payload_str,
                    vapid_private_key=str(VAPID_PEM_PATH),
                    vapid_claims=vapid_claims,
                    ttl=86400  # 24 horas de retención en FCM
                )
                sent_count += 1
            except pywebpush.WebPushException as ex:
                logger.warning(f"Error enviando Web Push a dispositivo: {ex}")
                # Si el endpoint ya expiró o fue revocado en Android (404 o 410)
                if ex.response and ex.response.status_code in [404, 410]:
                    self.remove_subscription(sub["endpoint"])
                failed_count += 1
            except Exception as e:
                logger.error(f"Fallo general enviando push: {e}")
                failed_count += 1

        logger.info(f"Push enviado: {sent_count} exitosos, {failed_count} fallidos de {len(subs)} suscripciones.")
        return {"sent": sent_count, "failed": failed_count, "total": len(subs)}

    def notify_assistant_response(self, assistant_id: str, message_text: str):
        """
        Dispara una notificación en segundo plano cuando un asistente completa su respuesta.
        Llamado asíncronamente desde el servidor.
        """
        asst = ASSISTANT_CONFIG.get(assistant_id.lower(), ASSISTANT_CONFIG["roxanne"])
        
        # Limpiar texto para preview en pantalla de bloqueo (máx 140 chars)
        clean_text = message_text.strip()
        if len(clean_text) > 140:
            preview_body = clean_text[:137] + "..."
        else:
            preview_body = clean_text

        payload = {
            "title": f"💬 {asst['title']}",
            "body": preview_body,
            "assistant": assistant_id.lower(),
            "tag": asst["tag"], # Control de duplicados por asistente
            "url": f"./?tab=tab-asistentes&assistant={assistant_id.lower()}",
            "icon": asst["icon"],
            "timestamp": int(json.loads(json.dumps(threading.get_native_id())) + 1000) if hasattr(threading, 'get_native_id') else 0
        }

        # Ejecutar en hilo desacoplado para no bloquear el retorno HTTP
        def _send():
            self.send_push_to_all(payload)

        t = threading.Thread(target=_send, daemon=True)
        t.start()

# Instancia global Singleton
push_service = PushNotificationService()
