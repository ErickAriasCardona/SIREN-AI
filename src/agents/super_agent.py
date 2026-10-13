import asyncio
import os
import sys
from pathlib import Path

# Añadir la raíz al path
sys.path.append(str(Path(__file__).resolve().parent.parent.parent))

from google.antigravity import Agent, LocalAgentConfig
from src.tools.scraper_tools import consultar_ranking_streamate, buscar_posicion_modelo
from src.tools.loyalfans_intel_tools import (
    ejecutar_scraping_completo_loyalfans,
    consultar_inteligencia_loyalfans,
    recomendar_estrategia_algoritmo
)
from src.config import GEMINI_API_KEY

SYSTEM_PROMPT = """Eres VELVET, la Super-Agente Orquestadora y Directora General de VELVET AI.
Tu objetivo es dirigir la estrategia de modelos y estudios de webcam para maximizar sus ingresos, cuidar su posicionamiento y coordinar a tus subagentes especialistas:
- ELECTRA: Radar de algoritmos, scraping e inteligencia técnica profunda de plataformas (LoyalFans, Streamate, Stripchat).
- SCARLETT: Carga, marketing y monetización de contenido en LoyalFans, Stripchat y Flirt4Free.
- ROXANNE: Copiloto de chat en vivo y up-selling a privados.
- AURORA: Memoria y fidelización de clientes VIP (Whales).

Mantén una actitud ejecutiva, sofisticada, analítica y protectora. Cada acción debe estar enfocada en ganar más dinero con el menor desgaste para la modelo.
"""

def create_velvet_agent(api_key: str = None) -> Agent:
    """Crea e inicializa una instancia de Velvet Super-Agent."""
    key = api_key or GEMINI_API_KEY or os.getenv("GEMINI_API_KEY", "")
    
    config = LocalAgentConfig(
        api_key=key if key else None,
        tools=[
            consultar_ranking_streamate,
            buscar_posicion_modelo,
            ejecutar_scraping_completo_loyalfans,
            consultar_inteligencia_loyalfans,
            recomendar_estrategia_algoritmo
        ],
        system_instructions=SYSTEM_PROMPT,
    )
    return Agent(config)

async def main():
    print("=" * 60)
    print("🌌 VELVET AI — Webcam Intelligence & Operations Super-Agent")
    print("=" * 60)
    print("Iniciando entorno y cargando herramientas...")

    agent_instance = create_velvet_agent()
    async with agent_instance as agent:
        print("\n[Velvet AI listo]. Escribe 'salir' para terminar.\n")
        while True:
            try:
                user_input = input("Tú > ")
                if user_input.strip().lower() in ["salir", "exit", "quit"]:
                    print("Cerrando sesión de Velvet AI. ¡Buenas ganancias!")
                    break
                if not user_input.strip():
                    continue

                print("\nVelvet AI > ", end="", flush=True)
                response = await agent.chat(user_input)
                async for chunk in response:
                    print(chunk, end="", flush=True)
                print("\n")
            except (KeyboardInterrupt, EOFError):
                break

if __name__ == "__main__":
    asyncio.run(main())
