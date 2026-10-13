import os
import json
from datetime import datetime
from typing import Dict, Any, List
from src.config import ARTIFACTS_DIR
from src.platforms.loyalfans.content_uploader import LoyalFansContentManager
from src.platforms.stripchat.content_uploader import StripchatContentManager
from src.platforms.flirt4free.content_uploader import Flirt4FreeContentManager

def generar_estrategia_contenido(
    plataforma: str,
    tipo_contenido: str,
    concepto_o_fetiche: str,
    tono_modelo: str = "seductora y dominante"
) -> str:
    """Genera títulos atractivos, descripciones persuasivas (captions), tags recomendados y precios sugeridos.

    Args:
        plataforma: 'loyalfans', 'stripchat' o 'flirt4free'.
        tipo_contenido: 'video_clip', 'set_fotos', 'teaser' o 'mass_dm'.
        concepto_o_fetiche: Tema del contenido (ej. 'lenceria roja', 'pies y medias', 'aceite', 'casual traviesa').
        tono_modelo: Personalidad de la modelo (ej. 'dulce y timida', 'dominante y picante', 'morbosa').
    """
    plat = plataforma.lower().strip()
    
    # Precios y formatos sugeridos según plataforma
    if plat == "loyalfans":
        precio_sug = "$15 - $25 USD (si es PPV o Clip)" if tipo_contenido != "set_fotos" else "$8 - $12 USD"
        formato = "Feed de suscriptores o Mass DM de pago"
        tags_populares = ["#LoyalFans", "#exclusive", "#fetish", "#vip", "#sneakpeek"]
    elif plat == "stripchat":
        precio_sug = "150 - 300 Tokens" if tipo_contenido != "teaser" else "Gratis (público para atraer)"
        formato = "Álbum comprable con tokens o exclusivo para Fan Club"
        tags_populares = ["#stripchat", "#fanclub", "#hottie", "#camgirl", "#private"]
    elif plat == "flirt4free":
        precio_sug = "50 - 120 Créditos"
        formato = "Tienda de videos y sets de fotos"
        tags_populares = ["#flirt4free", "#fetishclip", "#glamour", "#exclusive"]
    else:
        return f"Plataforma '{plataforma}' no soportada actualmente. Opciones: loyalfans, stripchat, flirt4free."

    propuestas_titulos = [
        f"Algo secreto que solo tú mereces ver... ({concepto_o_fetiche})",
        f"¿Puedes soportar verme así de cerca? 💋",
        f"Tu fantasía favorita hecha realidad hoy 🖤"
    ]

    captions = (
        f"🔥 **Estrategia de Publicación para {plat.upper()}**\n\n"
        f"📌 **Formato:** {formato}\n"
        f"💰 **Precio Sugerido:** {precio_sug}\n"
        f"🏷️ **Tags recomendados:** {' '.join(tags_populares)}\n\n"
        f"✨ **Títulos sugeridos:**\n"
        + "\n".join([f"- {t}" for t in propuestas_titulos]) + "\n\n"
        f"📝 **Caption persuasivo (Tono: {tono_modelo}):**\n"
        f"\"Sé lo mucho que has estado pensando en mí hoy... No aguanté las ganas y grabé esto para ti. "
        f"Desbloquéalo y cuéntame en un mensaje al oído qué parte te gustó más... Te estoy esperando 😈\"\n"
    )

    return captions

def guardar_paquete_publicacion(
    plataforma: str,
    titulo: str,
    caption: str,
    precio: float,
    media_paths: str = ""
) -> str:
    """Registra y guarda el paquete de publicación listo para ser cargado en la plataforma.

    Args:
        plataforma: 'loyalfans', 'stripchat' o 'flirt4free'.
        titulo: Título del set, álbum o post.
        caption: Texto descriptivo de la publicación.
        precio: Precio en la moneda de la plataforma (USD para LoyalFans, Tokens para Stripchat, Créditos para Flirt4Free).
        media_paths: Rutas separadas por comas a los archivos multimedia (fotos/videos).
    """
    plat = plataforma.lower().strip()
    paths = [p.strip() for p in media_paths.split(",") if p.strip()]

    if plat == "loyalfans":
        payload = LoyalFansContentManager.format_post_payload(caption=caption, media_paths=paths, price_usd=precio)
    elif plat == "stripchat":
        payload = StripchatContentManager.format_album_payload(title=titulo, description=caption, media_paths=paths, price_tokens=int(precio))
    elif plat == "flirt4free":
        payload = Flirt4FreeContentManager.format_media_payload(title=titulo, description=caption, media_paths=paths, price_credits=int(precio))
    else:
        return f"Plataforma '{plataforma}' no soportada."

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    file_path = ARTIFACTS_DIR / f"upload_package_{plat}_{timestamp}.json"
    
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)

    return f"✅ Paquete de publicación para {plat.upper()} guardado con éxito en: artifacts/{file_path.name}"
