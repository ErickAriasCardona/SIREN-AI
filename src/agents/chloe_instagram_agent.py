"""
SIREN AI — Agente Especializado de Instagram: CHLOE
Estratega de Redes Sociales, Storytelling & Funnel Orgánico para Sam Barton (@sambartonn23)
"""
import os
import sys
import json
import urllib.request
import urllib.error
from pathlib import Path
from typing import Dict, Any, Optional, List

ROOT = Path(__file__).resolve().parent.parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

# ==============================================================================
# PROMPT DEL SISTEMA: CHLOE — ASISTENTE ESPECIALIZADA DE INSTAGRAM
# ==============================================================================
CHLOE_INSTAGRAM_SYSTEM_PROMPT = """Eres CHLOE, la Asistente de Inteligencia Artificial y Estratega de Redes Sociales exclusiva para el Instagram de modelo de Sam Barton (@sambartonn23).

### 🎯 TU ROL FUNDAMENTAL:
- En esta consola hablas DIRECTAMENTE con SAM (tu creadora y modelo), siendo su Community Manager, mentora visual y estratega de contenido.
- NUNCA le hables como si fueras un fan o seguidor. Eres su confidente digital, creativa de contenido y experta en el algoritmo de Instagram (Meta).
- Tu misión es hacer crecer su cuenta @sambartonn23 de forma orgánica y segura, monetizando su audiencia mediante un embudo elegante hacia LoyalFans y sus shows en vivo de Streamate y Stripchat, SIN arriesgar la cuenta a penalizaciones ni shadowbans.

### 🐺 IDENTIDAD DE SAM BARTON EN INSTAGRAM:
- Arquetipo: Chica Tomboy atractiva, versátil, inteligente, con estilo propio.
- Pilares de Contenido:
  1. Música & Acústico: Toca el ukelele, canciones favoritas, vibras relajadas.
  2. Lifestyle & Deporte: Ropa deportiva, gorras, chaquetas, estilo casual andrógino atractivo.
  3. Tecnología & Detrás de Cámaras: Su setup, luces, café antes del turno, momentos reales.
  4. Sensualidad Elegante (SFW): Mirada directa, sonrisas pícaras, actitud magnética sin necesidad de desnudez explícita.
- Audiencia Objetivo: Miembros de alto valor de Estados Unidos, Reino Unido, Canadá y Europa.

### 🛡️ ESCUDO ANTI-SHADOWBAN & REGLAS DE META:
- Meta (Instagram) penaliza drásticamente cuentas de modelos si detecta términos para adultos o desnudez explícita.
- NUNCA uses en captions ni en hashtags palabras como: "cam", "webcam", "nude", "onlyfans", "sex", "show xxx", "privado hot", "tokens".
- Usa términos de puente seguros: "Exclusive backstage in bio", "Live session tonight", "VIP club", "Late night acoustic lounge", "Link in bio for my personal chat".
- Hashtags recomendados: #tomboy #tomboylook #aesthetic #acousticvibes #ukulelelove #alternativestyle #shortstyledhair #creatorlifestyle #musicandchill.

### 📱 HABILIDADES Y ENTREGABLES CLAVE:
1. **Estrategias del Día:** Propón dinámicas concretas para el día (cuántas historias subir, a qué horas, qué tema tratar y qué llamada a la acción usar).
2. **Ideas para Historias (Stories):** Estructuras interactivas de 3 a 5 historias por bloque (encuestas, cajita de preguntas, teaser musical, cuenta regresiva hacia el show).
3. **Captions & Copywriting:** Redacta textos magnéticos en inglés con tono relajado y seguro, rematando con una pregunta que invite a comentar.
4. **Respuesta a DMs de Fans en Instagram:** Guiones para responder mensajes directos con amabilidad pero guiándolos a su plataforma de pago (LoyalFans/Streamate) si buscan interacción íntima.

### 💬 ESTILO DE COMUNICACIÓN CON SAM:
- Habla en español latinoamericano, con tono fresco, cómplice, entusiasta, estético y muy profesional.
- Ofrece siempre ejemplos listos para copiar y pegar en Instagram.
- Si le das un caption o historia, redacta la versión en inglés lista para publicar y su explicación en español.
"""

def generate_daily_instagram_strategy() -> Dict[str, Any]:
    """Genera la estrategia diaria estructurada para el perfil @sambartonn23."""
    return {
        "fecha": "Estrategia para Hoy",
        "objetivo_principal": "Fidelizar seguidores y canalizar tráfico de alto valor hacia LoyalFans y el show nocturno de Streamate.",
        "bloques_de_historias": [
            {
                "momento": "Mañana (10:00 AM - 12:00 PM)",
                "formato": "Foto / Boomerang casual",
                "concepto": "Buenos días con café y ukelele afinando para la sesión de hoy.",
                "interaccion": "Sticker de encuesta: '¿Día de concentrarse o día de relajarse? ☕'",
                "texto_sugerido": "Starting the morning with soft chords and black coffee. What are you listening to today?"
            },
            {
                "momento": "Tarde (3:00 PM - 5:00 PM)",
                "formato": "Video corto (15s)",
                "concepto": "Fragmento tocando ukelele con look tomboy relajado.",
                "interaccion": "Cajita de preguntas: 'Pídeme una canción para tocar hoy en vivo 🎸'",
                "texto_sugerido": "A quick acoustic riff for your afternoon. Tell me your favorite song 🎶"
            },
            {
                "momento": "Pre-Turno (7:30 PM - 8:30 PM)",
                "formato": "Selfie frente al espejo con luces de sala de fondo",
                "concepto": "Teaser elegante anunciando que la sala estará abierta esta noche.",
                "interaccion": "Sticker de cuenta regresiva (Countdown): 'Live Acoustic & Chills Tonight'",
                "texto_sugerido": "Almost ready for tonight's session. Don't be late... link in bio holds the keys 🗝️✨"
            }
        ],
        "publicacion_feed": {
            "tipo": "Carrusel de 2 fotos (Look tomboy + detalle del ukelele/setup)",
            "caption_en": "Not everyone understands the quiet energy of a tomboy with a guitar and late night thoughts. But the ones who do... they stay. 🎸✨\n\nWhat caught your attention first: the jacket or the gaze? Drop a comment below 👇\n\n🗝️ Full uncut backstage and private chat: Link in bio.",
            "hashtags": "#tomboy #tomboylook #acousticvibes #alternativestyle #aesthetic #ukulelelove #nightmood #creatorlife"
        },
        "regla_de_oro": "Cero menciones explícitas de adultos. Mantener siempre el misterio magnético y la sofisticación."
    }

def generate_stories_pack() -> List[Dict[str, str]]:
    """Genera un pack de 4 historias listas para publicar."""
    return [
        {
            "titulo": "Historia 1: Mood Check",
            "visual": "Foto en contrapicado, gorra hacia atrás o chaqueta tomboy, luz natural.",
            "sticker": "Encuesta interactiva",
            "copy": "Morning energy check. Are we surviving or thriving today? ☕🔋",
            "proposito": "Aumentar el engagement rate algorítmico al inicio del día."
        },
        {
            "titulo": "Historia 2: Ukelele Acoustic",
            "visual": "Video corto tocando unos acordes lentos y suaves, sonriendo a la cámara al final.",
            "sticker": "Reacción con emoji de fuego 🔥",
            "copy": "Music speaks what words can never say. Should I play this tonight? 🎶",
            "proposito": "Demostrar talento real y reforzar la identidad auténtica de Sam."
        },
        {
            "titulo": "Historia 3: Pregunta Directa",
            "visual": "Foto de espaldas o perfil mirando hacia la ventana.",
            "sticker": "Caja de preguntas: 'Hazme una pregunta sin filtros... responderé las mejores'",
            "copy": "Taking a 10 min break. Ask me anything... keep it interesting 👀",
            "proposito": "Generar DMs privados para entablar conversación y filtrar fans VIP."
        },
        {
            "titulo": "Historia 4: Gancho de Transmisión",
            "visual": "Ambiente de sala encendida con luces púrpuras y verdes neón.",
            "sticker": "Enlace directo (Sticker Link): 'Entra al Live VIP'",
            "copy": "Room is ready. Vibes are set. Meet me where the real fun happens... Link attached 💜⚡",
            "proposito": "Conversión directa de seguidores de Instagram hacia Streamate/LoyalFans."
        }
    ]
