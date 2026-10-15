"""
VELVET AI — Gestor de Transmisión en Vivo (Live Broadcast Room Manager)
Controlador automatizado para salas de transmisión en LoyalFans, Stripchat, Flirt4Free y Streamate.
Configura y asegura de forma automática:
  1. Cámara fijada en 'OBS Virtual Camera'.
  2. Micrófono confirmado en 'Micrófono (Logitech BRIO)'.
  3. Objetivo del día dinámico con 3 niveles (Calentamiento, Intensidad, Clímax).
  4. Tema de la sala con etiqueta obligatoria '@SAMBARTONN23'.
"""

import json
from pathlib import Path
from typing import Dict, Any, Optional

ROOT_DIR = Path(__file__).resolve().parent.parent.parent
CONFIG_PATH = ROOT_DIR / "data" / "broadcast_config.json"

DEFAULT_BROADCAST_CONFIG = {
    "preferred_camera": "OBS Virtual Camera",
    "preferred_microphone": "Logitech",
    "creator_tag": "@SAMBARTONN23",
    "room_topic": "🖤 @SAMBARTONN23 | Dominante & Analítica 😈 Goal 3 Niveles Activo | Haz vibrar mi Lovense 🔥",
    "topic_presets": [
        "🖤 @SAMBARTONN23 | Dominante & Analítica 😈 Goal 3 Niveles Activo | Haz vibrar mi Lovense 🔥",
        "⚽ Athletic & Sensual @SAMBARTONN23 | Desafíame si puedes... Nivel 3 sin censura 💥",
        "💻 Dev de día, tu tentación de noche 🖤 @SAMBARTONN23 | Cumpliendo metas paso a paso 😈",
        "🔥 Sala VIP @SAMBARTONN23 | 3 Niveles de Intensidad + Lovense Conectado 🫦 ¿Listo para obedecer?",
        "✨ Atardecer íntimo con @SAMBARTONN23 | Ukelele, lencería y control total 🖤"
    ],
    "goals": {
        "level_1": {
            "name": "Nivel 1: Calentamiento & Conexión",
            "tokens": 250,
            "usd": 25.0,
            "desc": "Poses fitness/lencería deportiva, charla VIP interactiva y test suave Lovense"
        },
        "level_2": {
            "name": "Nivel 2: Intensidad & Sensualidad",
            "tokens": 750,
            "usd": 75.0,
            "desc": "Cambio a lencería exclusiva, baile sugerente y vibración media interactiva"
        },
        "level_3": {
            "name": "Nivel 3: Clímax & Dominación Total",
            "tokens": 1500,
            "usd": 150.0,
            "desc": "Show dominante completo, Lovense al 100%, flash show y clip VIP por DM"
        }
    }
}

def load_broadcast_config() -> Dict[str, Any]:
    """Carga la configuración persistente para transmisiones en vivo."""
    if CONFIG_PATH.exists():
        try:
            with open(CONFIG_PATH, "r", encoding="utf-8") as f:
                data = json.load(f)
                # Asegurar que @SAMBARTONN23 siempre esté presente
                if not data.get("creator_tag"):
                    data["creator_tag"] = "@SAMBARTONN23"
                if "@SAMBARTONN23" not in data.get("room_topic", ""):
                    data["room_topic"] = f"{data.get('room_topic', '')} @SAMBARTONN23".strip()
                return data
        except Exception:
            pass
    
    save_broadcast_config(DEFAULT_BROADCAST_CONFIG)
    return DEFAULT_BROADCAST_CONFIG.copy()

def save_broadcast_config(config: Dict[str, Any]) -> bool:
    """Guarda la configuración persistente para transmisiones en vivo."""
    try:
        CONFIG_PATH.parent.mkdir(parents=True, exist_ok=True)
        # Regla inquebrantable: siempre debe contener @SAMBARTONN23
        creator_tag = config.get("creator_tag") or "@SAMBARTONN23"
        topic = config.get("room_topic", "")
        if creator_tag.upper() not in topic.upper():
            topic = f"{topic} {creator_tag}".strip()
            config["room_topic"] = topic
        config["creator_tag"] = creator_tag

        with open(CONFIG_PATH, "w", encoding="utf-8") as f:
            json.dump(config, f, indent=2, ensure_ascii=False)
        return True
    except Exception as e:
        print(f"Error guardando broadcast_config.json: {e}")
        return False

def get_webrtc_media_hook_script() -> str:
    """
    Retorna el script JavaScript de inyección temprana para Chromium.
    Hookea navigator.mediaDevices.enumerateDevices y navigator.mediaDevices.getUserMedia
    para garantizar que 'OBS Virtual Camera' y el micrófono 'Logitech' sean priorizados
    y seleccionados como dispositivos predeterminados de la sesión de transmisión.
    """
    return """
    (() => {
        if (!navigator.mediaDevices) return;

        const originalEnumerate = navigator.mediaDevices.enumerateDevices.bind(navigator.mediaDevices);
        const originalGetUserMedia = navigator.mediaDevices.getUserMedia.bind(navigator.mediaDevices);

        // 1. Reordenar dispositivos para que OBS y Logitech aparezcan primeros (índice 0)
        navigator.mediaDevices.enumerateDevices = async function() {
            const devices = await originalEnumerate();
            const obsVideo = [];
            const otherVideo = [];
            const logiAudio = [];
            const otherAudio = [];
            const other = [];

            for (const d of devices) {
                if (d.kind === 'videoinput') {
                    if (d.label && d.label.toLowerCase().includes('obs')) {
                        obsVideo.push(d);
                    } else {
                        otherVideo.push(d);
                    }
                } else if (d.kind === 'audioinput') {
                    if (d.label && d.label.toLowerCase().includes('logitech')) {
                        logiAudio.push(d);
                    } else {
                        otherAudio.push(d);
                    }
                } else {
                    other.push(d);
                }
            }

            // Retornar con prioridad fija: OBS primero en video, Logitech primero en audio
            return [...obsVideo, ...otherVideo, ...logiAudio, ...otherAudio, ...other];
        };

        // 2. Interceptar getUserMedia para forzar deviceId deseado si no está especificado
        navigator.mediaDevices.getUserMedia = async function(constraints) {
            try {
                const devs = await originalEnumerate();
                const obsCam = devs.find(d => d.kind === 'videoinput' && d.label && d.label.toLowerCase().includes('obs'));
                const logiMic = devs.find(d => d.kind === 'audioinput' && d.label && d.label.toLowerCase().includes('logitech'));

                const modified = { ...constraints };

                if (modified.video && obsCam) {
                    if (typeof modified.video === 'boolean') {
                        modified.video = { deviceId: { exact: obsCam.deviceId } };
                    } else if (typeof modified.video === 'object') {
                        // Si no especificó un deviceId exacto distinto, apuntar a OBS
                        if (!modified.video.deviceId || !modified.video.deviceId.exact) {
                            modified.video.deviceId = { ideal: obsCam.deviceId };
                        }
                    }
                }

                if (modified.audio && logiMic) {
                    if (typeof modified.audio === 'boolean') {
                        modified.audio = { deviceId: { exact: logiMic.deviceId } };
                    } else if (typeof modified.audio === 'object') {
                        if (!modified.audio.deviceId || !modified.audio.deviceId.exact) {
                            modified.audio.deviceId = { ideal: logiMic.deviceId };
                        }
                    }
                }

                return await originalGetUserMedia(modified);
            } catch (err) {
                // Fallback directo a getUserMedia estándar si la restricción estricta falla
                return await originalGetUserMedia(constraints);
            }
        };

        console.log('[VELVET AI] Hook WebRTC activo: OBS Virtual Camera y Micrófono Logitech priorizados.');
    })();
    """

async def setup_live_broadcast_room(page, platform_key: str, log_func=None) -> Dict[str, Any]:
    """
    Se ejecuta al entrar en la sala de transmisión en vivo (/broadcast).
    1. Verifica y selecciona en el DOM los dispositivos de cámara (OBS Virtual Camera) y micrófono (Logitech).
    2. Rellena o prepara el tema de la sala asegurando que incluya @SAMBARTONN23.
    3. Notifica la meta del día con sus 3 niveles en consola.
    """
    def log(msg: str):
        if log_func:
            log_func(msg)
        print(f"[LiveBroadcast] {msg}")

    config = load_broadcast_config()
    res = {
        "camera_confirmed": False,
        "camera_name": "No detectada",
        "mic_confirmed": False,
        "mic_name": "No detectado",
        "topic_set": False,
        "topic": config["room_topic"],
        "goals": config["goals"]
    }

    log("\n" + "="*65)
    log("  📹 CONFIGURANDO SALA DE TRANSMISIÓN EN VIVO (LIVE ROOM)")
    log("="*65)

    # 1. Detectar dispositivos en el contexto del navegador
    try:
        devices = await page.evaluate("""
            async () => {
                try {
                    const devs = await navigator.mediaDevices.enumerateDevices();
                    return devs.map(d => ({ kind: d.kind, label: d.label, id: d.deviceId }));
                } catch(e) {
                    return [];
                }
            }
        """)

        video_devs = [d for d in devices if d.get("kind") == "videoinput"]
        audio_devs = [d for d in devices if d.get("kind") == "audioinput"]

        obs_cam = next((d for d in video_devs if "obs" in d.get("label", "").lower()), None)
        logi_mic = next((d for d in audio_devs if "logitech" in d.get("label", "").lower()), None)

        if obs_cam:
            res["camera_confirmed"] = True
            res["camera_name"] = obs_cam.get("label", "OBS Virtual Camera")
            log(f"🎥 Cámara confirmada y asignada: [{res['camera_name']}]")
        else:
            log("⚠️ 'OBS Virtual Camera' no fue detectada directamente en la lista. Si OBS está abierto, inicia 'Iniciar Cámara Virtual'.")

        if logi_mic:
            res["mic_confirmed"] = True
            res["mic_name"] = logi_mic.get("label", "Micrófono Logitech")
            log(f"🎙️ Micrófono verificado: [{res['mic_name']}]")
        else:
            first_mic = audio_devs[0].get("label") if audio_devs else "Predeterminado"
            log(f"ℹ️ Micrófono de entrada activo: [{first_mic}]. Asegura que la cámara Logitech esté conectada.")

    except Exception as e:
        log(f"Nota comprobando dispositivos WebRTC: {e}")

    # 2. Intentar seleccionar en selectores DOM de la plataforma si existen
    try:
        select_script = """
            (() => {
                let camChanged = false;
                let micChanged = false;
                const selects = document.querySelectorAll('select');
                for (const s of selects) {
                    for (const opt of s.options) {
                        const txt = (opt.text || '').toLowerCase();
                        if (!camChanged && (txt.includes('obs virtual') || txt.includes('obs'))) {
                            s.value = opt.value;
                            s.dispatchEvent(new Event('change', { bubbles: true }));
                            camChanged = true;
                        }
                        if (!micChanged && txt.includes('logitech')) {
                            s.value = opt.value;
                            s.dispatchEvent(new Event('change', { bubbles: true }));
                            micChanged = true;
                        }
                    }
                }
                return { camChanged, micChanged };
            })()
        """
        dom_sel = await page.evaluate(select_script)
        if dom_sel.get("camChanged"):
            log("✓ Selector de cámara en la página fijado en OBS Virtual Camera.")
        if dom_sel.get("micChanged"):
            log("✓ Selector de micrófono en la página fijado en Logitech.")
    except Exception:
        pass

    # 3. Aplicar tema de la sala con @SAMBARTONN23
    topic = config["room_topic"]
    if "@SAMBARTONN23" not in topic.upper():
        topic = f"{topic} @SAMBARTONN23".strip()

    try:
        # Intentar rellenar el input de tema / título de la sala en LoyalFans o Stripchat
        topic_selectors = [
            "input[placeholder*='tema']",
            "input[placeholder*='topic']",
            "input[placeholder*='Topic']",
            "input[placeholder*='Title']",
            "input[placeholder*='título']",
            "textarea[placeholder*='tema']",
            "textarea[placeholder*='topic']",
            "input[name='topic']",
            "input[name='title']",
            "input[name='broadcast_topic']"
        ]
        topic_filled = False
        for sel in topic_selectors:
            loc = page.locator(sel).first
            try:
                if await loc.is_visible(timeout=1000):
                    await loc.fill(topic)
                    topic_filled = True
                    log(f"📝 Tema de la sala autocompletado en el formulario: \"{topic}\"")
                    break
            except Exception:
                continue

        if not topic_filled:
            log(f"🏷️ Tema sugerido para tu transmisión (incluye @SAMBARTONN23):")
            log(f"   \"{topic}\"")
            # Copiar al portapapeles de la página para que la modelo pueda pegarlo con Ctrl+V si lo desea
            try:
                await page.evaluate(f"navigator.clipboard.writeText({json.dumps(topic)})")
                log("📋 ¡Tema copiado al portapapeles del navegador para pegar rápidamente con Ctrl+V!")
            except Exception:
                pass
        res["topic_set"] = True

    except Exception as e:
        log(f"Nota en configuración de tema: {e}")

    # 4. Desplegar Objetivo del Día con 3 Niveles
    goals = config["goals"]
    g1 = goals.get("level_1", {})
    g2 = goals.get("level_2", {})
    g3 = goals.get("level_3", {})

    log("─────────────────────────────────────────────────────────────────")
    log("🎯 OBJETIVO DEL DÍA (3 NIVELES ACTIVOS PARA SAM BARTON):")
    log(f"  • {g1.get('name')}: {g1.get('tokens', 250)} TK (${g1.get('usd', 25)} USD) ➔ {g1.get('desc')}")
    log(f"  • {g2.get('name')}: {g2.get('tokens', 750)} TK (${g2.get('usd', 75)} USD) ➔ {g2.get('desc')}")
    log(f"  • {g3.get('name')}: {g3.get('tokens', 1500)} TK (${g3.get('usd', 150)} USD) ➔ {g3.get('desc')}")
    log("─────────────────────────────────────────────────────────────────")
    log("✨ ¡Sala de transmisión lista y configurada con OBS, Logitech y @SAMBARTONN23!")

    return res
