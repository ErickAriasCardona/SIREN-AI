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
from src.automation.profile_deep_audit import synthesize_diana_findings
from src.config import GEMINI_API_KEY

def analizar_identidad_y_lenguaje_creadora(creator_handle: str = "@sambarton23") -> str:
    """Extrae el arquetipo de modelo, tono de voz, estilo de lenguaje y perfil comercial de la creadora."""
    data = synthesize_diana_findings({"creator_handle": creator_handle})
    return data.get("dossier_text", "")

SYSTEM_PROMPT = """Eres DIANA, la Subagente Auditora de Cuenta, Minería de Inteligencia y Psicología Comercial de VELVET AI.
Tu especialidad es entender en profundidad a la creadora (su estilo de lenguaje, qué tipo de modelo es, su arquetipo de seducción y su perfil comercial) y analizar historiales completos de cuentas en plataformas +18 (LoyalFans, Stripchat, Flirt4Free, Streamate).

Tus capacidades nucleares:
1. ARQUETIPO Y ESTILO DE MODELO:
   - Identificar con precisión quirúrgica el tipo de modelo (ej. 'Confident Sensual GFE', 'Glamour Intimate POV', 'Dominatriz', 'Cosplay Niche').
   - Describir su tono de voz, cadencia de habla, léxico persuasivo y fórmulas de conversación para enganchar a los clientes.
2. MINERÍA FORENSE DE CUENTA:
   - Depurar implacablemente la información basura (mirones sin dinero, spam, métricas de vanidad).
   - Extraer el 'oro comercial': fetiches más comprados, formatos ganadores (clips 3-7 min, audios íntimos) y precios óptimos.
3. ADAPTACIÓN A PLATAFORMAS:
   - Conectar el estilo natural de la modelo con las mecánicas de monetización de LoyalFans (Mass DM PPV, suscripciones y Tienda de Audios).

Sé perspicaz, analítica, directa, sofisticada y orientada a monetizar la esencia única de la modelo.
"""

def create_diana_agent(api_key: str = None) -> Agent:
    """Crea e inicializa una instancia del agente DIANA."""
    key = api_key or GEMINI_API_KEY or os.getenv("GEMINI_API_KEY", "")
    config = LocalAgentConfig(
        api_key=key if key else None,
        tools=[analizar_identidad_y_lenguaje_creadora],
        system_instructions=SYSTEM_PROMPT
    )
    return Agent(config)

def mostrar_menu_diana():
    print("\n" + "=" * 70)
    print("🔬 DIANA — Auditora de Identidad, Perfil y Minería de Cuentas")
    print("=" * 70)
    print("Acciones disponibles:")
    print("  [1] 🎭 Radiografía Completa de SAM BARTON (Arquetipo, Lenguaje y Perfil)")
    print("  [2] 🗣️ Análisis de Tono de Voz y Fórmulas de Conversación")
    print("  [3] 👠 Fetiches Compatibles y Formatos Ganadores")
    print("  [4] 👥 Contactos VIP y Audiencia en Espera en LoyalFans")
    print("  [5] 💬 Chat Libre con DIANA (Modo Inteligente)")
    print("  [0] 🚪 Salir")
    print("=" * 70)

async def modo_chat_libre_diana():
    key = GEMINI_API_KEY or os.getenv("GEMINI_API_KEY", "")
    if not key:
        print("\n⚠️ AVISO: No se detectó GEMINI_API_KEY en variables de entorno.")
        print("Para conversar con el LLM en lenguaje natural, configura tu API key en .env.")
        print("Las opciones [1] a [4] funcionan de inmediato con la auditoría forense local.\n")
        return

    print("\n💬 [Modo Chat con DIANA activado]. Escribe 'menu' para volver.\n")
    agent_instance = create_diana_agent(key)
    async with agent_instance as agent:
        while True:
            try:
                pregunta = input("Tú > ")
                if pregunta.strip().lower() in ["menu", "volver", "salir", "exit"]:
                    break
                if not pregunta.strip():
                    continue
                print("\nDIANA > ", end="", flush=True)
                resp = await agent.chat(pregunta)
                async for chunk in resp:
                    print(chunk, end="", flush=True)
                print("\n")
            except (KeyboardInterrupt, EOFError):
                break

async def main():
    while True:
        mostrar_menu_diana()
        try:
            opcion = input("DIANA > Elige una opción (0-5): ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\nCerrando sesión de DIANA.")
            break

        if opcion == "0":
            print("\nCerrando terminal de DIANA. ¡Oro comercial asegurado!")
            break

        elif opcion == "1":
            print("\n" + analizar_identidad_y_lenguaje_creadora("@sambarton23"))

        elif opcion == "2":
            data = synthesize_diana_findings({"creator_handle": "@sambarton23"})
            print("\n" + data.get("estilo_lenguaje", ""))

        elif opcion == "3":
            data = synthesize_diana_findings({"creator_handle": "@sambarton23"})
            print("\n" + data.get("fetiches_compatibles", ""))
            print(f"💰 Formato Óptimo: {data.get('best_content', '')}")

        elif opcion == "4":
            data = synthesize_diana_findings({"creator_handle": "@sambarton23"})
            users = ", ".join(data.get("chat_users", []))
            print(f"\n👥 Fans detectados en base: 604 seguidores.")
            print(f"📩 Contactos activos en mensajería: {users}")
            print(f"🎯 Oportunidad Clave: {data.get('key_opportunity', '')}")

        elif opcion == "5":
            await modo_chat_libre_diana()

        else:
            print("❌ Opción inválida. Elige un número del 0 al 5.")

        input("\n[Presiona Enter para continuar...]")

if __name__ == "__main__":
    asyncio.run(main())
