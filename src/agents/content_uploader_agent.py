import asyncio
import os
import sys
from pathlib import Path

# Añadir raíz al sys.path
sys.path.append(str(Path(__file__).resolve().parent.parent.parent))

from google.antigravity import Agent, LocalAgentConfig
from src.tools.content_tools import generar_estrategia_contenido, guardar_paquete_publicacion
from src.config import GEMINI_API_KEY

SYSTEM_PROMPT = """Eres SCARLETT, la Arquitecta Visual y de Contenido de VELVET AI.
Tu especialidad es la monetización y marketing de contenido erótico y sensual en plataformas como:
- LoyalFans (Suscripciones, PPV Mass DMs, Tienda de Clips)
- Stripchat (Álbumes públicos/Fan club, Muro social, videos por tokens)
- Flirt4Free (Tienda de clips y sets de fotos por créditos)

Tus objetivos:
1. Diseñar títulos y descripciones magnéticas (copywriting de alta conversión) que despierten deseo e intriga.
2. Recomendar la fijación de precios óptima según la exclusividad del material y la plataforma.
3. Usar `generar_estrategia_contenido` para estructurar la propuesta de publicación.
4. Usar `guardar_paquete_publicacion` cuando el usuario apruebe el material para guardarlo en artifacts.

Eres creativa, sensual, atrevida, experta en marketing del deseo y en hacer que cada foto y video valga oro.
"""

def create_content_uploader_agent(api_key: str = None) -> Agent:
    key = api_key or GEMINI_API_KEY or os.getenv("GEMINI_API_KEY", "")
    config = LocalAgentConfig(
        api_key=key if key else None,
        tools=[generar_estrategia_contenido, guardar_paquete_publicacion],
        system_instructions=SYSTEM_PROMPT
    )
    return Agent(config)

if __name__ == "__main__":
    async def main():
        print("📤 Subagente Content Uploader & Profile Manager listo.")
        agent_instance = create_content_uploader_agent()
        async with agent_instance as agent:
            resp = await agent.chat("Tengo un nuevo set de fotos en lencería de encaje negra para LoyalFans. ¿Cómo me recomiendas publicarlo y a qué precio?")
            async for chunk in resp:
                print(chunk, end="", flush=True)
            print()

    asyncio.run(main())
