import asyncio
import os
import sys
from pathlib import Path

# Configurar stdout a UTF-8 para evitar errores de charmap en Windows
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

# Añadir raíz al sys.path
sys.path.append(str(Path(__file__).resolve().parent.parent.parent))

from google.antigravity import Agent, LocalAgentConfig
from src.tools.loyalfans_intel_tools import (
    ejecutar_scraping_completo_loyalfans,
    consultar_inteligencia_loyalfans,
    recomendar_estrategia_algoritmo,
    generar_plan_tactico_unificado_diana_electra
)
from src.tools.scraper_tools import consultar_ranking_streamate, buscar_posicion_modelo
from src.config import GEMINI_API_KEY

SYSTEM_PROMPT = """Eres ELECTRA, la Especialista en Scraping, Auditoría Técnica y Radar de Algoritmos de VELVET AI.
Tu misión es diseccionar la anatomía de las plataformas para creadoras (LoyalFans, Streamate, Stripchat, Flirt4Free) para que el estudio y las modelos nunca dependan de la suerte, sino de datos exactos.

Tus responsabilidades principales:
1. LOYALFANS FULL INTELLIGENCE:
   - Conocer cada una de las funcionalidades: Tienda de Clips, Tienda de Audios, Go Live, Cam2Cam One-on-One, Mass DMs, Stories y Shoutouts.
   - Conocer al detalle el sistema financiero: 80% modelo / 20% plataforma, mínimo de $50 USD, cortes quincenales, retiros por Paxum, Wire y ACH.
   - Desmantelar el algoritmo de visibilidad interna: optimización de Explore Feed, velocidad de interacción en los primeros 60 minutos, posicionamiento por tags de nicho/fetiche y el empuje masivo que da transmitir en vivo o conectar juguetes Lovense/Kiiroo.
2. Usar tus herramientas:
   - `ejecutar_scraping_completo_loyalfans`: Cuando necesites actualizar o volver a rastrear las guías y centro oficial de LoyalFans.
   - `consultar_inteligencia_loyalfans`: Para extraer respuestas precisas de facturación, herramientas, algoritmo o guías oficiales.
   - `recomendar_estrategia_algoritmo`: Para dar hojas de ruta y planes de acción a la modelo según su perfil.
   - `consultar_ranking_streamate` y `buscar_posicion_modelo`: Para el monitoreo de posiciones en vivo en Streamate.

Tu tono es analítico, implacable, estratégico, claro y enfocado en métricas y dinero. No especulas: operas con base en el scraping y los datos oficiales de la plataforma.
"""

def create_electra_agent(api_key: str = None) -> Agent:
    """Crea e inicializa una instancia del agente ELECTRA."""
    key = api_key or GEMINI_API_KEY or os.getenv("GEMINI_API_KEY", "")
    config = LocalAgentConfig(
        api_key=key if key else None,
        tools=[
            ejecutar_scraping_completo_loyalfans,
            consultar_inteligencia_loyalfans,
            recomendar_estrategia_algoritmo,
            generar_plan_tactico_unificado_diana_electra,
            consultar_ranking_streamate,
            buscar_posicion_modelo
        ],
        system_instructions=SYSTEM_PROMPT
    )
    return Agent(config)

def mostrar_menu():
    print("\n" + "=" * 70)
    print("⚡ ELECTRA — Radar de Algoritmos, Scraping & Platform Intelligence")
    print("=" * 70)
    print("Elige una acción o consulta:")
    print("  [1] 💵 Facturación, Comisiones y Retiros en LoyalFans")
    print("  [2] 🧰 Catálogo Completo de Herramientas y Features de LoyalFans")
    print("  [3] 🧠 Desglose del Algoritmo, Explore Feed y Visibilidad")
    print("  [4] 🔄 Ejecutar Scraping en Vivo a LoyalFans (Actualizar Base)")
    print("  [5] 🎯 Plan Táctico Unificado: Conectar con DIANA (Auditoría) + Algoritmo")
    print("  [6] 📊 Escanear Grilla de Streamate (Playwright Radar Top)")
    print("  [7] 💬 Chat Libre con ELECTRA (Modo Inteligente)")
    print("  [0] 🚪 Salir")
    print("=" * 70)

async def modo_chat_libre():
    key = GEMINI_API_KEY or os.getenv("GEMINI_API_KEY", "")
    if not key:
        print("\n⚠️ AVISO: No se detectó GEMINI_API_KEY en las variables de entorno.")
        print("Para chatear con el LLM en lenguaje natural, configura tu API key en .env.")
        print("Sin embargo, todas las opciones [1] a [6] funcionan al 100% con los datos extraídos.\n")
        return

    print("\n💬 [Modo Chat Libre con ELECTRA activado]. Escribe 'menu' para volver.\n")
    agent_instance = create_electra_agent(key)
    async with agent_instance as agent:
        while True:
            try:
                pregunta = input("Tú > ")
                if pregunta.strip().lower() in ["menu", "volver", "salir", "exit"]:
                    break
                if not pregunta.strip():
                    continue
                print("\nELECTRA > ", end="", flush=True)
                resp = await agent.chat(pregunta)
                async for chunk in resp:
                    print(chunk, end="", flush=True)
                print("\n")
            except (KeyboardInterrupt, EOFError):
                break

async def main():
    while True:
        mostrar_menu()
        try:
            opcion = input("ELECTRA > Elige una opción (0-7): ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\nCerrando sesión de ELECTRA.")
            break

        if opcion == "0":
            print("\nDesconectando radar de ELECTRA. ¡Buenas ganancias!")
            break

        elif opcion == "1":
            print("\n" + consultar_inteligencia_loyalfans("facturacion"))

        elif opcion == "2":
            print("\n" + consultar_inteligencia_loyalfans("herramientas"))

        elif opcion == "3":
            print("\n" + consultar_inteligencia_loyalfans("algoritmo"))

        elif opcion == "4":
            print("\n🔄 Iniciando crawler en vivo de LoyalFans...")
            res = ejecutar_scraping_completo_loyalfans()
            print("\n" + res)

        elif opcion == "5":
            print("\n" + "=" * 70)
            print("🎯 PLAN TÁCTICO UNIFICADO: DIANA (Auditora) x ELECTRA (Radar)")
            print("=" * 70)
            print("¿Cómo deseas generar el plan táctico?")
            print("  [1] 💎 Usar auditoría de DIANA (Sam Barton / @sambarton23 en LoyalFans)")
            print("  [2] ✏️ Personalizar datos (Nicho, fetiche, juguetes y transmisiones)")
            sub = input("Elige (1 o 2) [Enter para opción 1]: ").strip()
            
            if sub == "2":
                nicho = input("Introduce el nicho/estilo (ej: lencería exclusiva, cosplay, dominatriz): ").strip()
                juguete = input("¿Tiene juguete interactivo Lovense? (s/n) [s]: ").strip().lower() != "n"
                en_vivo = input("¿Está dispuesta a hacer transmisiones en vivo? (s/n) [s]: ").strip().lower() != "n"
                print("\n⚙️ Generando plan táctico cruzado con DIANA...")
                res = generar_plan_tactico_unificado_diana_electra(
                    nicho_personalizado=nicho or None,
                    tiene_juguete=juguete,
                    hace_en_vivo=en_vivo
                )
            else:
                print("\n🔬 Conectando con DIANA: extrayendo histórico de @sambarton23...")
                res = generar_plan_tactico_unificado_diana_electra(
                    plataforma="loyalfans",
                    tiene_juguete=True,
                    hace_en_vivo=True
                )
            print("\n" + res)

        elif opcion == "6":
            print("\n🌐 Escaneando primeras 2 páginas de la grilla de Streamate con Playwright...")
            print(consultar_ranking_streamate(paginas=2))

        elif opcion == "7":
            await modo_chat_libre()

        else:
            print("❌ Opción inválida. Por favor ingresa un número del 0 al 7.")

        input("\n[Presiona Enter para continuar...]")

if __name__ == "__main__":
    asyncio.run(main())
