import asyncio
import os
import sys
from pathlib import Path

# Añadir raíz al sys.path
sys.path.append(str(Path(__file__).resolve().parent.parent.parent))

from google.antigravity import Agent, LocalAgentConfig
from src.tools.copilot_tools import sugerir_respuesta_chat, script_negociacion_privado
from src.config import GEMINI_API_KEY

SYSTEM_PROMPT = """Eres ROXANNE, la Voz Seductora y Cerradora de Privados de VELVET AI.
Tu rol es acompañar a la modelo durante sus transmisiones en vivo (en Flirt4Free, Stripchat, etc.) para:
1. Traducir al instante las intenciones de los clientes internacionales (inglés, francés, alemán).
2. Desarmar con elegancia y picardía a los "mirones gratuitos" (freeloaders).
3. Redactar respuestas magnéticas y seductoras que empujen a propinas de menú o cierren shows privados.
4. Usar las herramientas `sugerir_respuesta_chat` y `script_negociacion_privado` cuando corresponda.

Eres rápida, pícara, seductora, astuta y experta en hacer que los hombres quieran gastar más tiempo y dinero contigo.
"""

def create_copilot_agent(api_key: str = None) -> Agent:
    key = api_key or GEMINI_API_KEY or os.getenv("GEMINI_API_KEY", "")
    config = LocalAgentConfig(
        api_key=key if key else None,
        tools=[sugerir_respuesta_chat, script_negociacion_privado],
        system_instructions=SYSTEM_PROMPT
    )
    return Agent(config)

if __name__ == "__main__":
    async def main():
        print("💋 Subagente Copiloto de Chat listo.")
        agent_instance = create_copilot_agent()
        async with agent_instance as agent:
            resp = await agent.chat("Un usuario llamado 'Mark_UK' me acaba de escribir: 'can you stand up and show me your outfit?'. ¿Qué le respondo para que dé propina?")
            async for chunk in resp:
                print(chunk, end="", flush=True)
            print()

    asyncio.run(main())
