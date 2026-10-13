from typing import Dict, Any

def sugerir_respuesta_chat(
    mensaje_usuario: str,
    idioma_usuario: str = "ingles",
    tipo_usuario: str = "curioso",
    objetivo: str = "llevar_a_privado"
) -> str:
    """Genera respuestas sugeridas para el chat en vivo en el idioma del cliente y su traducción al español.

    Args:
        mensaje_usuario: Lo que el cliente escribió en el chat.
        idioma_usuario: Idioma del cliente ('ingles', 'frances', 'aleman', 'italiano').
        tipo_usuario: 'curioso' (freeloader), 'comprador' (interesado en show) o 'whale' (cliente VIP).
        objetivo: 'llevar_a_privado', 'pedir_propina' o 'coquetear_sin_mostrar'.
    """
    msg_lower = mensaje_usuario.lower()
    
    # Lógica de sugerencias basada en objetivos
    if objetivo == "llevar_a_privado":
        sug_en = "I'm feeling so naughty right now... take me to private where no one else can see us and let's play ❤️"
        sug_es = "Me siento tan traviesa ahora mismo... llévame a privado donde nadie más nos vea y juguemos ❤️"
    elif objetivo == "pedir_propina":
        sug_en = "You know what makes me smile really big? Tips on my menu, baby... show me some love ✨"
        sug_es = "¿Sabes qué me hace sonreír mucho? Propinas de mi menú, amor... demuéstrame algo de cariño ✨"
    else:
        sug_en = "You're so charming today... what kind of trouble do you have in mind for us? 😈"
        sug_es = "Estás muy encantador hoy... ¿qué tipo de travesura tienes en mente para nosotros? 😈"

    return (
        f"💬 **Respuesta Sugerida para el Chat en Vivo:**\n\n"
        f"🇺🇸 **Para enviar al cliente ({idioma_usuario.capitalize()}):**\n"
        f"\"{sug_en}\"\n\n"
        f"🇪🇸 **Significado en español:**\n"
        f"\"{sug_es}\"\n\n"
        f"💡 **Táctica psicológica:** No regales detalles explícitos en público. Vende la fantasía de intimidad y exclusividad."
    )

def script_negociacion_privado(precio_minuto: float = 4.99, tiempo_minimo: int = 5) -> str:
    """Genera un guión para cerrar rápidamente la entrada a un show privado con condiciones claras.

    Args:
        precio_minuto: Precio por minuto en dólares o tokens equivalentes.
        tiempo_minimo: Tiempo mínimo sugerido para el show.
    """
    return (
        f"🔒 **Guión de Cierre para Privado:**\n\n"
        f"• Frase de gancho: \"My private room is open just for you... let's have our own secret moment.\"\n"
        f"• Condición dulce: \"Stay with me at least {tiempo_minimo} minutes so I can give you the full experience you deserve 💋\"\n"
        f"• Valor configurado: ${precio_minuto}/minuto."
    )
