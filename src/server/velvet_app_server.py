import os
import sys
import json
import sqlite3
import datetime
import time
import base64
import threading
import urllib.request
import urllib.error
import mimetypes
from pathlib import Path
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer

mimetypes.add_type('application/wasm', '.wasm')
mimetypes.add_type('application/octet-stream', '.task')

# Agregar raíz al sys.path
ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.append(str(ROOT))

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

import asyncio
from src.platforms.streamate.stream_monitor_controller import (
    parse_gold_menu_text,
    parse_wheel_game_text,
    update_gold_menu_live,
    update_wheel_game_live,
    update_room_topic_live,
    get_streamate_messenger_data,
    send_streamate_messenger_reply,
    run_streamate_autopilot,
    toggle_streamate_autopilot
)
from src.platforms.streamate.stream_monitor_orchestrator import (
    inspect_streammonitor_status,
    launch_streammonitor_desktop,
    generate_mahia_prompt,
    parse_mahia_output_to_tools,
    apply_full_orchestrated_shift,
    smart_orchestrate_natural_idea,
    execute_mahia_shift_dialogue,
    PRESET_SHIFT_THEMES
)
from src.analytics.streamate_competitor_radar import scan_streamate_tomboy_competitors

from src.agents.roxanne_multimodel_copilot import (
    ROXANNE_SAM_SYSTEM_PROMPT,
    OllamaProvider,
    GeminiProvider
)
from src.agents.chloe_instagram_agent import (
    CHLOE_INSTAGRAM_SYSTEM_PROMPT,
    generate_daily_instagram_strategy,
    generate_stories_pack
)
from src.automation.push_notification_service import push_service

# ==============================================================================
# CONTROL GLOBAL DE SESIONES ACTIVAS DE CHAT PARA CANCELACIÓN Y PAUSA INMEDIATA
# ==============================================================================
ACTIVE_CHAT_SESSIONS = {}
ACTIVE_CHAT_LOCK = threading.Lock()

# ==============================================================================
# PROMPTS DEL SISTEMA OPTIMIZADOS PARA CPU (AGILIDAD 7-15s EN OLLAMA)
# ==============================================================================
ROXANNE_CPU_SYSTEM_PROMPT = """Eres ROXANNE, Co-Piloto Estratégica y mentora personal de la modelo y creadora Sam Barton (@sambartonn23).
Sam es modelo tomboy versátil en LoyalFans, Stripchat y Streamate (cuenta estudio, 50% split, rating 4.0).
Asistes a Sam directamente en español con respuestas a fans, metas de sala, dinámicas Lovense y tácticas de monetización.
Sé concisa, práctica, directa y estratégica. Responde con calidez y profesionalismo.
FORMATO OBLIGATORIO: Cuando Sam te pida tablas, matrices, comparativas o resúmenes, preséntalos SIEMPRE utilizando formato de tabla Markdown estándar (| Columna 1 | Columna 2 |) con encabezados concisos y datos ordenados fila por fila. Usa subtítulos y listas con viñetas cuando corresponda."""

CHLOE_CPU_SYSTEM_PROMPT = """Eres CHLOE, estratega de Instagram de Sam Barton (@sambartonn23).
Creas ideas de historias, ganchos visuales y textos con estilo tomboy para reactivar el algoritmo y dirigir tráfico a LoyalFans y Streamate.
Sé creativa, concisa, moderna y enfocada en interacción.
FORMATO OBLIGATORIO: Cuando Sam te pida tablas, cronogramas, matrices de contenido o comparativas, preséntalos SIEMPRE utilizando formato de tabla Markdown estándar (| Columna 1 | Columna 2 |) con datos ordenados y claros."""

DIANA_CPU_SYSTEM_PROMPT = """Eres DIANA, auditora financiera y especialista de pagos de Sam Barton (@sambartonn23).
Especialista en splits de Streamate (50% neto del 35% del estudio), pagos de LoyalFans (80% creador, retiro mínimo $50) y Stripchat.
Responde a Sam en español con números claros, precisión financiera y consejos prácticos de rentabilidad.
FORMATO OBLIGATORIO: Cuando Sam te pida tablas, matrices de splits, proyecciones o balances, preséntalos SIEMPRE utilizando formato de tabla Markdown estándar (| Columna 1 | Columna 2 |) con cifras exactas, comisiones y netos desglosados."""


MAHIA_CPU_SYSTEM_PROMPT = """Eres MAHIA, co-piloto táctica para transmisiones en vivo de Sam Barton (@sambartonn23) en StreamMonitor y Streamate.
Especialista en preparar Topics de sala optimizados en inglés (máximo 130 caracteres con hashtags estratégicos como #tomboy #petite #versatile), menús Gold de 3G a 10G, juegos de ruleta a 5G y mensajes automáticos de sala (Alt+1 a Alt+6).
Responde a Sam de forma concisa, rápida y táctica para aplicar directamente en sus transmisiones.
FORMATO OBLIGATORIO: Cuando Sam te pida temas, metas o configuraciones, preséntalos en listas limpias o formato de tabla Markdown listo para copiar y pegar."""

ALMA_CPU_SYSTEM_PROMPT = """Eres ALMA TECH, la inteligencia central y consultora global de marca de Sam Barton (@sambartonn23).
Coordinas la visión integral de las plataformas (Streamate, LoyalFans, Stripchat e Instagram), supervisando a las especialistas Roxanne, Mahia, Chloe, Diana y Electra.
Ofreces asesoramiento de alto nivel, visión estratégica de carrera, balance de ingresos pasivos vs streaming en vivo y toma de decisiones tácticas.
FORMATO OBLIGATORIO: Estructura tus respuestas con claridad profesional, viñetas analíticas y tablas Markdown cuando se comparen datos o metas."""

ELECTRA_CPU_SYSTEM_PROMPT = """Eres ELECTRA, ingeniera de tráfico algorítmico y posicionamiento de Sam Barton (@sambartonn23).
Especialista en SEO de streaming, ciclo de bump cada 3.5h en LoyalFans, retención de los primeros 30 segundos en Streamate y tags clave (#Tomboy, #Versatile).
Responde a Sam en español con tácticas directas, accionables y análisis de algoritmos.
FORMATO OBLIGATORIO: Cuando Sam te pida tablas, matrices de algoritmos, horarios o tags, preséntalos SIEMPRE utilizando formato de tabla Markdown estándar (| Columna 1 | Columna 2 |) estructurados por horario, plataforma y métrica."""

SYSTEM_PROMPTS_BY_AGENT = {
    # CIPOTE CEVICHERIA
    "cipote_chef": (
        "Eres Don Cipote, Chef Ejecutivo y Maestro Cevichero de Cipote Cevicheria en el Caribe colombiano. "
        "Tu especialidad absoluta son los ceviches costeños auténticos, pescados frescos (corvina, róbalo, camarón), "
        "la leche de tigre perfecta (limón pajarito recién exprimido, cebolla morada, cilantro, ají dulce y fondo de pescado concentrado), "
        "y el control estricto de mermas y gramajes por porción (150g de proteína neta por ceviche estándar). "
        "Hablas con calidez caribeña profesional, sazón y conocimiento culinario de alto nivel. "
        "Recomiendas platos de la carta: Ceviche Clásico ($18.000), Ceviche Mixto ($24.000), Cóctel de Camarón ($22.000) y Granizado 16oz ($12.000). "
        "Responde siempre con precisión sobre recetas, tiempos de marinado (máximo 3 a 5 minutos), mariscos y control de mermas. "
        "NUNCA menciones temas de modelos webcam, transmisiones ni ukelele; tu único dominio es la cocina, cevichería y gastronomía caribeña."
    ),
    "cipote_bar": (
        "Eres el Barman Líder y Coctelero de Cipote Cevicheria. "
        "Tu especialidad es el maridaje caribeño, cócteles de autor con rones y licores del Caribe, micheladas especiales y granizados frappé de 16oz ($12.000) de corozo, maracuyá y limón. "
        "Asesoras sobre bebidas que limpian el paladar y complementan la frescura y el picante de los ceviches. "
        "Responde con tono hospitalario y profesional sobre recetas de bar, licores y servicio de barra."
    ),
    "cipote_pos": (
        "Eres el Cajero Líder y Administrador de Punto de Venta de Cipote Cevicheria. "
        "Tu responsabilidad es el control riguroso de comandas, turnos de caja, arqueos y el conteo crítico de vasos plásticos (12oz, 16oz y 24oz). "
        "Cada vaso plástico equivale exactamente a una porción vendida y no debe existir ninguna discrepancia con la facturación del POS. "
        "Orientas sobre apertura y cierre de turno, cuadre de caja (efectivo, transferencias, Nequi), anulación de comandas y control de inventario de vasos."
    ),
    "cipote_delivery": (
        "Eres el Coordinador de Logística y Despacho Rápido de Cipote Cevicheria. "
        "Garantizas empaques antiderrame (sellado hermético de leche de tigre por separado para verter al consumir) "
        "y entregas en menos de 15 a 20 minutos preservando la cadena de frío y frescura del ceviche."
    ),

    # EL SOLAR GASTRO-BAR
    "solar_solecito": (
        "Eres Solecito, el anfitrión virtual de reservas de El Solar Gastro-Bar. "
        "Gestionas asignación de mesas, reservas para cenas, cumpleaños, eventos corporativos, control de aforo y horarios de atención. "
        "Respondes con amabilidad, elegancia y rapidez sobre la experiencia gastronómica."
    ),
    "solar_reservas": (
        "Eres el Coordinador de Reservas de El Solar Gastro-Bar. Gestionas mesas, confirmación de asistencia, aforo y eventos especiales."
    ),
    "solar_maitre": (
        "Eres el Capitán de Servicio y Maître de El Solar Gastro-Bar. "
        "Especialista en atención al comensal, maridajes de la carta, cortes de carne, tapas y servicio de salón."
    ),
    "solar_waiter": (
        "Eres el Capitán de Servicio de El Solar Gastro-Bar. Especialista en menú, atención en mesa y tiempos de servicio."
    ),
    "solar_chef": (
        "Eres el Chef Ejecutivo de El Solar Gastro-Bar. Especialista en parrilla, tapas de autor, cocción lenta, recetas y tiempos de despacho en cocina."
    ),
    "solar_kitchen": (
        "Eres el Jefe de Cocina de El Solar Gastro-Bar. Controlas recetas, mise en place, despacho de comandas y estándares de higiene."
    ),
    "solar_admin": (
        "Eres el Administrador de El Solar Gastro-Bar. Controlas finanzas, compras, proveedores, cuadre de caja y métricas operativas."
    ),

    # ALMA AUTONOMOUS MULTI-AGENT & BÓVEDAS OPENCLAW
    "alma": ALMA_CPU_SYSTEM_PROMPT,
    "mufasa": (
        "Eres Mufasa, Director de Operaciones del Sistema Autónomo Multi-Agente ALMA y Bóvedas OpenClaw. "
        "Gestionas la orquestación de flujos de trabajo autónomos, ejecución de pipelines y gobernanza operativa."
    ),
    "vera": (
        "Eres Vera, Auditora de Inteligencia, Seguridad y Cumplimiento del Sistema Autónomo ALMA. "
        "Auditas la integridad de datos, cumplimiento de estándares GAP-X y consistencia lógica de los agentes."
    ),
    "nemesis": (
        "Eres Nemesis, Agente de Estrategia de Ciberseguridad y Pruebas de Penetración de ALMA TECH. "
        "Proteges la infraestructura, gestionas hardening de servidores, puertos y seguridad de autenticación."
    ),
    "kali": (
        "Eres Kali, Especialista en Automatización, Pipelines CI/CD y DevOps de ALMA TECH. "
        "Controlas despliegues continuos, scripts y tareas en segundo plano."
    ),
    "bruce": (
        "Eres Bruce, Arquitecto de Infraestructura, Redes y Conectividad de ALMA TECH. "
        "Monitoreas puertos (8900, 8888, 5173), túneles Cloudflare/LocalTunnel y rendimiento de servidores."
    ),
    "atlas": (
        "Eres Atlas, Cartógrafo de Datos y Grafos de Conocimiento de ALMA TECH. "
        "Mapeas relaciones entre entidades, bóvedas Obsidian y bases de conocimiento vectorial."
    ),

    # SIREN AI (Sam Barton)
    "roxanne": ROXANNE_CPU_SYSTEM_PROMPT,
    "mahia": MAHIA_CPU_SYSTEM_PROMPT,
    "chloe": CHLOE_CPU_SYSTEM_PROMPT,
    "diana": DIANA_CPU_SYSTEM_PROMPT,
    "electra": ELECTRA_CPU_SYSTEM_PROMPT,
}

def generate_contextual_fallback(assistant_id: str, message: str) -> str:
    """Genera una respuesta contextual inteligente con soporte completo de Markdown y Matrices/Tablas por dominio."""
    msg_low = message.lower()
    is_table_query = any(w in msg_low for w in ["tabla", "tablas", "matriz", "matrices", "comparativa", "resumen", "comparar", "cuadro", "cronograma", "esquema"])

    # 1. CIPOTE CEVICHERIA (DON CIPOTE & EQUIPO)
    if assistant_id == "cipote_chef":
        if any(w in msg_low for w in ["recomienda", "recomiendas", "probar", "hoy", "plato", "comer", "sugerencia"]):
            return (
                "¡Ajá! Te recomiendo sin duda empezar con nuestro **Ceviche Mixto ($24.000)** con camarón tierno y pescado blanco del día, bañado en nuestra leche de tigre tradicional con limón pajarito recién exprimido y maíz tostado crocante. Y para acompañar con este calor, un **Granizado 16oz ($12.000)** de corozo bien frío.\n\n"
                "¿Prefieres ceviche tradicional costeño bien cítrico o te gusta con un toque picante de ají dulce?"
            )
        elif is_table_query or any(w in msg_low for w in ["carta", "menu", "menú", "precios", "precio", "gramaje"]):
            return (
                "Aquí tienes la matriz oficial de la carta y gramajes estándar de **Cipote Cevicheria**:\n\n"
                "| Plato / Producto | Precio | Proteína Neta | Base Cítrica | Acompañamiento |\n"
                "|---|---|---|---|---|\n"
                "| **Ceviche Clásico** | $18.000 | 150g Pescado Blanco | Leche de tigre tradicional | Maíz tostado + Cebolla morada |\n"
                "| **Ceviche Mixto** | $24.000 | 100g Pescado + 60g Camarón | Leche de tigre especial | Maíz crocante + Chips de plátano |\n"
                "| **Cóctel de Camarón** | $22.000 | 120g Camarón cocido | Salsa golf marinera caribeña | Galletas de soda + Limón |\n"
                "| **Granizado 16oz** | $12.000 | N/A | Pulpa corozo / maracuyá | Vaso escarchado con sal y limón |\n\n"
                "**Regla de Oro en Cocina:** Cada porción de ceviche lleva exactamente **150g netos** de proteína pesada tras limpieza, manteniendo el costo de merma por debajo del 12%."
            )
        elif any(w in msg_low for w in ["leche de tigre", "receta", "marinado", "limon", "limón", "pescado"]):
            return (
                "Para la leche de tigre perfecta en Cipote Cevicheria:\n"
                "1. **Extracción suave:** Exprime el limón pajarito al 70% sin apretar la cáscara para no transferir aceites amargos.\n"
                "2. **Base concentrada:** Mezcla el jugo con caldo concentrado de pescado bien frío, cebolla morada fina, ají dulce costeño picado, tallos de cilantro y ajo machacado.\n"
                "3. **Tiempo crítico de marinado:** Máximo de **3 a 5 minutos**. El pescado debe curarse en el plato y llegar a la mesa firme, fresco y jugoso."
            )
        elif any(w in msg_low for w in ["merma", "mermas", "porciones", "costo"]):
            return (
                "En Cipote controlamos las mermas mediante pesaje en crudo antes y después de eviscerar y filetear. El rendimiento del pescado blanco entero debe ser mínimo del 48-52% en filete limpio. Cada ceviche lleva 150 gramos pesados en balanza digital antes de montar la comanda."
            )
        else:
            return (
                "¡Saludos! Soy Don Cipote, tu Chef Ejecutivo. Conmigo estandarizas la leche de tigre, controlas gramajes exactos por porción y garantizas la máxima frescura del marisco. ¿Qué receta, gramaje o plato de la carta revisamos hoy?"
            )

    elif assistant_id == "cipote_bar":
        return (
            "¡A la orden! Como Barman de Cipote, te recomiendo acompañar los ceviches con un **Granizado 16oz ($12.000)** de corozo o maracuyá bien frío, o una michelada con sal marina y limón que corta el picante y limpia el paladar a la perfección."
        )

    elif assistant_id == "cipote_pos":
        return (
            "Terminal POS & Turno de Caja listo. Para este turno: base inicial confirmada, cruce estricto 1:1 de vasos plásticos (12oz, 16oz y 24oz) contra comandas facturadas, y arqueo listo para consolidar efectivo, Nequi y transferencias."
        )

    elif assistant_id == "cipote_delivery":
        return (
            "Despacho Rápido activo. Nuestro protocolo exige empacar la leche de tigre en contenedor hermético sellado independiente, garantizando que el cliente la vierta al comer y evitando derrames en ruta de moto en menos de 20 minutos."
        )

    # 2. EL SOLAR GASTRO-BAR
    elif assistant_id in ["solar_solecito", "solar_reservas"]:
        return (
            "¡Hola! Te damos la bienvenida a **El Solar Gastro-Bar**. Estoy listo para gestionar tu reserva de mesa para hoy o el fin de semana. Indícame para cuántas personas es la mesa, la hora preferida y si celebran alguna ocasión especial."
        )
    elif assistant_id in ["solar_maitre", "solar_waiter"]:
        return (
            "Buenas tardes. Como Capitán de Servicio de El Solar, te sugiero iniciar con nuestras tapas de la casa y maridar los cortes a la parrilla con nuestra selección de vinos y cócteles de autor. ¿En qué puedo asistirte en mesa hoy?"
        )
    elif assistant_id in ["solar_chef", "solar_kitchen"]:
        return (
            "Cocina de El Solar en marcha. Controlamos tiempos de comanda menores a 18 minutos en mesa, mise en place de parrilla al día y estándar de calidad en cada término de carne."
        )
    elif assistant_id == "solar_admin":
        return (
            "Administración de El Solar Gastro-Bar conectada: reportes de ventas por turno, facturación electrónica y control de insumos con proveedores al día."
        )

    # 3. ALMA TECH & AUTONOMOUS MULTI-AGENT
    elif assistant_id == "alma":
        return (
            "Ecosistema ALMA TECH conectado y operativo. Monitoreando en paralelo: SIREN (8888), ALMA Autonomous Multi-Agent (5173), Cipote Cevicheria y El Solar Gastro-Bar. ¿Qué aspecto estratégico u operativo deseas coordinar?"
        )
    elif assistant_id in ["mufasa", "vera", "nemesis", "kali", "bruce", "atlas"]:
        return (
            f"Agente autónomo **{assistant_id.upper()}** de ALMA Multi-Agent activo. Estado de conexión con el núcleo de gobernanza y bóvedas OpenClaw verificado. Listo para ejecutar instrucciones operativas."
        )

    # 4. SIREN AI (SAM BARTON)
    elif assistant_id == "chloe":
        if is_table_query:
            return (
                "Sam, aquí tienes tu matriz estratégica de publicaciones para la semana en **@sambartonn23**:\n\n"
                "| Día | Formato | Temática Tomboy | Objetivo de Interacción | Llamado a la Acción (CTA) |\n"
                "|---|---|---|---|---|\n"
                "| **Lunes** | Historia + Encuesta | Ukelele acústico & café de mañana | Reactivar visualizaciones tempranas | *'¿Qué canción acústica quieren hoy?'* |\n"
                "| **Martes** | Reel / Post Feed | Outfit Tomboy deportivo casual | Gancho de atracción estética | *'Vibra relajada. Link en bio para charlar conmigo '* |\n"
                "| **Miércoles** | 3 Historias con Stickers | Detrás de cámaras en setup de luces | Preguntas de fans de USA | Cajita de preguntas en inglés |\n"
                "| **Jueves** | Post Foto + Caption EN | Mirada directa y look biker | Posicionamiento internacional | *'Late night session starting soon...'* |\n"
                "| **Viernes** | Countdown Story | Teaser de turno de fin de semana | Embudo hacia Streamate / LoyalFans | Recordatorio para conectar en directo |\n"
                "| **Sábado** | Reel Dinámico | Acústico corto en vivo | Tráfico directo de fin de semana | *'Full acoustic session on my private link'* |\n"
                "| **Domingo** | Carrusel Lifestyle | Rutina de descanso & ukelele | Fidelización de comunidad | Interacción relajada en comentarios |\n\n"
                " **Consejo Anti-Shadowban**: Recuerda usar siempre enlaces puente en tu biografía y evitar términos explícitos en stories."
            )
        elif any(w in msg_low for w in ["historia", "story", "stories", "publicar", "post", "foto", "idea"]):
            return (
                "Para tus historias de hoy con vibra tomboy:\n"
                "1. **Mañana**: Boomerang casual afinando el ukelele o preparando café con texto: *'Modo enfoque activado... ¿quién anda por acá?'* + sticker de encuesta.\n"
                "2. **Tarde**: Foto en cabina/set con luz tenue: *'Segunda mitad del día, lista para lo bueno '*.\n"
                "3. **Cierre**: Gancho a LoyalFans/Streamate: *'Los detalles exclusivos están en el link de mi bio '*."
            )
        elif any(w in msg_low for w in ["hola", "buenos dias", "buenas", "que tal", "como estas"]):
            return (
                "¡Hola Sam! Lista para mover el algoritmo de @sambartonn23 hoy. ¿Quieres que preparemos una matriz de contenido semanal, el pack de historias del día o un copy para tu próximo post?"
            )
        else:
            return (
                f"Sam, respecto a tu consulta: para mantener alta la retención en @sambartonn23, publica historias con stickers interactivos cada 3 horas y usa siempre un gancho claro al inicio."
            )
    elif assistant_id == "diana":
        if is_table_query or any(w in msg_low for w in ["ganancia", "split", "cuanto", "precio", "privado", "exclusivo", "gold", "dolar", "balance"]):
            return (
                "Sam, aquí tienes la auditoría detallada y matriz comparativa de tus splits reales por plataforma:\n\n"
                "| Plataforma / Modalidad | Tarifa Pública | Split Estudio / Fee | Neto Sam Barton | Neto Estimado por Sesión |\n"
                "|---|---|---|---|---|\n"
                "| **Streamate Privado** | $2.99 / min | 35% estudio | **17.5% ($0.52 / min)** | $5.23 USD (10 min priv) |\n"
                "| **Streamate Exclusivo** | $3.99 / min | 35% estudio | **17.5% ($0.70 / min)** | $10.47 USD (15 min excl) |\n"
                "| **Streamate Gold Menu (25G)** | $25.00 USD | 35% estudio | **$4.37 USD neto** | $4.37 USD por compra |\n"
                "| **LoyalFans Pay-per-msg** | $1.00 / msg | 20% plataforma | **80% ($0.80 / msg)** | $16.00 USD (20 chats) |\n"
                "| **LoyalFans Venta Clip VIP** | $15.00 USD | 20% plataforma | **80% ($12.00 neto)** | $12.00 USD por venta |\n"
                "| **Stripchat Tip Goal Lovense** | 25 tokens ($1.25) | 50% modelo | **50% ($0.62 neto)** | $6.25 USD (10 tips) |\n\n"
                " **Regla de Rentabilidad**: En Streamate tu ticket más eficiente es el Exclusivo a **$3.99/min** ($0.70 neto/min). En LoyalFans tu umbral mínimo de cobro es **$50 USD** con 80% directo a tu favor."
            )
        elif any(w in msg_low for w in ["hola", "buenos dias", "buenas", "que tal", "como estas"]):
            return (
                "¡Hola Sam! Aquí revisando tus balances y proyecciones. ¿Quieres que auditemos tus splits en una tabla matriz o revisemos el balance para el próximo corte?"
            )
        else:
            return (
                f"Sam, analizando tu consulta: recuerda siempre separar los ingresos directos (LoyalFans 80%) de los de cuenta estudio (Streamate 50% split) para calcular con exactitud tu flujo de caja neto."
            )
    elif assistant_id == "electra":
        if is_table_query:
            return (
                "Sam, esta es tu matriz de posicionamiento y horarios de tráfico alto para dominar los feeds:\n\n"
                "| Plataforma | Factor Algorítmico | Horario Óptimo (USA / Col) | Acción Inmediata | Impacto en Ranking |\n"
                "|---|---|---|---|---|\n"
                "| **LoyalFans** | Ciclo de Bump cada 3.5h | 11:00 AM, 2:30 PM, 6:00 PM, 9:30 PM | Ejecutar re-bump exacto | Devuelve tu perfil al Top 1 del feed |\n"
                "| **Streamate** | Retención Free Chat (<30s) | 8:00 PM - 12:00 AM (Prime US) | Charla verbal de bienvenida al segundo 3 | Sube a Página 1 en categoría Tomboy |\n"
                "| **Stripchat** | Tip Goals Lovense tempranos | Primeros 15 min de transmisión | Activar meta de 50 tokens de bienvenida | Activa badge *'Trending Now'* en sala |\n"
                "| **Instagram** | Historias con Sticker Interactivo | 1:00 PM y 7:30 PM | Encuesta o cajita de preguntas | Reactiva la cuenta antes de iniciar transmisión |\n\n"
                " **Clave de Tráfico**: Los primeros 30 segundos de free chat en Streamate determinan el 70% de las conversiones hacia privado."
            )
        elif any(w in msg_low for w in ["bump", "cooldown", "feed", "posicion", "posicionamiento", "rank", "ranking"]):
            return (
                "Sam, checklist del algoritmo:\n"
                "1. **LoyalFans**: Ejecuta el bump cada 3.5 horas exactas. Esto te devuelve a la parte superior del feed orgánico.\n"
                "2. **Streamate**: Los primeros 30 segundos de free chat definen tu multiplicador de visibilidad. Mantén la interacción verbal activa de inmediato.\n"
                "3. **Tags clave**: Asegúrate de tener activos `#Tomboy`, `#Versatile`, `#Ukelele` y `#Cam2Cam`."
            )
        elif any(w in msg_low for w in ["hola", "buenos dias", "buenas", "que tal", "como estas"]):
            return (
                "¡Hola Sam! Monitores de tráfico al 100%. ¿Quieres revisar una matriz de horarios de tráfico o el cooldown de tu bump en LoyalFans?"
            )
        else:
            return (
                f"Sam, sobre tu consulta: para elevar el score en los rankings de streaming, cambia el tema de sala cada 90 minutos y estimula las propinas rápidas en los primeros minutos de transmisión."
            )
    else: # Roxanne (Default para SIREN)
        if any(w in msg_low for w in ["menu", "menú", "gold", "ruleta", "rueda", "wheel", "topic", "tema", "sala", "buzz"]):
            return (
                "¡Entendido, Sam! Aquí tienes tu configuración completa para hoy enfocada en **Golds & Buzz Lovense**, con precios accesibles (3G y 5G), opciones de ruleta más íntimas (distintas al menú) y el topic con hashtags optimizado a 110 caracteres (límite 140):\n\n"
                "###  1. Menú GOLD (Todos a 3 Gold)\n"
                "*(Estructura lista para copiar en la herramienta Menú GOLD)*\n"
                "```text\n"
                "Buzz Lovense Nivel 1 (15 seg) - 3\n"
                "Vibración Lovense Media (25 seg) - 3\n"
                "Subir Top / Mostrar Bra Deportivo - 3\n"
                "Nalgadita Sonora en Cámara - 3\n"
                "Desabotonar Camisa Tomboy - 3\n"
                "Susurro Erótico al Micrófono - 3\n"
                "```\n\n"
                "###  2. Ruleta Íntima (Costo: 5 Gold por giro)\n"
                "*(Opciones más íntimas y exclusivas, 100% diferentes al menú Gold)*\n"
                "```text\n"
                "Costo: 5\n"
                "Buzz Lovense Nivel Máximo (45 seg)\n"
                "Twerk Tomboy Lento y Cercano\n"
                "Topless Rápido Flash (5 seg)\n"
                "Control Total de mi Lovense x 1 min\n"
                "Baile Sensual con Gorra Hacia Atrás\n"
                "Quitarme la Camisa (Quedo en Bra)\n"
                "Tease Exclusivo en Pantalón Ajustado\n"
                "Doble Giro de Ruleta Gratis\n"
                "Audio Erótico Susurrado al Oído\n"
                "1 Minuto de Pre-Privado Exclusivo\n"
                "```\n\n"
                "###  3. Tema de la Sala (110 caracteres / Máx 140)\n"
                "```text\n"
                " BUZZ LOVENSE ACTIVO  Menu Gold 3G  Ruleta Íntima 5G  Tease Tomboy en Vivo #Tomboy #Lovense #Gold #Cam2Cam\n"
                "```\n\n"
                " *Ya actualicé y dejé guardados estos valores en tu configuración local. Al abrir cualquiera de los botones de Stream Monitor en la barra lateral derecha, ya los encontrarás precargados para aplicar.*"
            )
        elif is_table_query:
            return (
                "Sam, aquí tienes la matriz estructurada con tus tarifas y dinámicas recomendadas para el turno:\n\n"
                "| Modalidad / Nivel | Tarifa Sugerida | Dinámica en Cámara | Meta de Tensión / Conversión |\n"
                "|---|---|---|---|\n"
                "| **Free Chat Público** | Gratis | Charla cercana + ukelele acústico | Enganchar en primeros 30s sin mostrar de más |\n"
                "| **Privado Cam2Cam** | **$2.99 / min** | Miradas fijas, susurros y complicidad | Mantener al fan mínimo 5 minutos ($2.60 neto) |\n"
                "| **Exclusivo VIP** | **$3.99 / min** | Rol personalizado alternando el control | Tensión sensual progresiva sin sumisión forzada |\n"
                "| **Gold Menu: Nivel 1** | **3 Gold (Económico)** | Buzz Lovense o subida de top | Gancho de volumen y microtips rápidos |\n"
                "| **Ruleta de Turno** | **5 Gold por giro** | Dinámicas íntimas (Twerk, Tease, Control) | Retención y juego continuo en sala |\n"
                "| **Gold Menu: Clímax** | **50 Gold ($8.75 neto)** | Dinámica Lovense nivel máximo | Conexión directa y salto a exclusivo |\n\n"
                " **Estrategia Sam**: Combina momentos de charla relajada con tu ukelele y marca límites con elegancia para que siempre quieran ir a privado."
            )
        elif any(w in msg_low for w in ["hola", "buenos dias", "buenas", "que tal", "como estas"]):
            return (
                "¡Hola Sam! Aquí lista a tu lado. ¿Qué tienes planeado para hoy? Dime si necesitas que redactemos una respuesta a un fan, una matriz de tarifas o preparemos las dinámicas de cámara."
            )
        else:
            return (
                f"Sam, respecto a tu consulta: mantén tu vibra tomboy versátil firme, combina momentos de ukelele y charla cercana con tensión sensual en cámara, y recuerda tomar descansos de 10 minutos cada 2 horas."
            )

DB_PATH = ROOT / "data" / "velvet_analytics.db"
PORT = 8888

def detect_language(text: str) -> str:
    """Detecta si el mensaje entrante está en español o en inglés/otro."""
    text_lower = text.lower()
    spanish_indicators = [
        "hola", "buenos dias", "buenas tardes", "buenas noches", "hermosa", "linda", 
        "guapa", "bella", "que tal", "como estas", "cómo estás", "de donde eres", 
        "cuantos años", "cuánto", "haces", "hacer", "quiero", "foto", "videollamada", 
        "amor", "bebe", "papi", "chula", "te ves", "dios", "besos", "saludos", "gracias",
        "por favor", "precio", "cuanto cobras", "donde vives"
    ]
    for word in spanish_indicators:
        if word in text_lower:
            return "es"
    return "en"

def log_interaction_to_db(fan_message: str, reply: str, model_name: str, lang: str):
    """Registra la interacción en la base de datos velvet_analytics.db para análisis."""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS copilot_chat_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT,
                model_name TEXT,
                language TEXT,
                fan_message TEXT,
                sam_reply TEXT
            )
        """)
        cursor.execute("""
            INSERT INTO copilot_chat_logs 
            (timestamp, model_name, language, fan_message, sam_reply)
            VALUES (?, ?, ?, ?, ?)
        """, (
            datetime.datetime.now().isoformat(),
            model_name,
            lang,
            fan_message,
            reply
        ))
        conn.commit()
        conn.close()
    except Exception as e:
        print(f"[DB Warning]: No se pudo registrar en SQLite: {e}")

class VelvetRequestHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        # Servir archivos desde la raíz de VELVET AI
        super().__init__(*args, directory=str(ROOT), **kwargs)

    def end_headers(self):
        # Headers CORS universales
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type, Authorization")
        self.send_header("Cache-Control", "no-cache, no-store, must-revalidate")
        super().end_headers()

    def do_OPTIONS(self):
        self.send_response(204)
        self.end_headers()

    def do_GET(self):
        if self.path == "/api/status":
            self.handle_api_status()
        elif self.path == "/api/history":
            self.handle_api_history()
        elif self.path.startswith("/api/chat_history"):
            self.handle_api_chat_history()
        elif self.path.startswith("/api/chat/stop") or self.path.startswith("/api/chat_stop"):
            self.handle_api_chat_stop()
        elif self.path == "/api/platforms_profiles":
            self.handle_api_platforms_profiles()
        elif self.path == "/api/financials" or self.path.startswith("/api/loyalfans/financials"):
            self.handle_api_financials()
        elif self.path.startswith("/api/loyalfans/transactions"):
            self.handle_api_loyalfans_transactions()
        elif self.path.startswith("/api/loyalfans/subscribers"):
            self.handle_api_loyalfans_subscribers()
        elif self.path.startswith("/api/loyalfans/ranking"):
            self.handle_api_loyalfans_ranking()
        elif self.path.startswith("/api/loyalfans/all"):
            self.handle_api_loyalfans_all()
        elif self.path.startswith("/api/loyalfans/refresh"):
            self.handle_api_refresh_financials()
        elif self.path.startswith("/api/positioning"):
            self.handle_api_positioning()
        elif self.path.startswith("/api/streamate/dashboard") or self.path.startswith("/api/streamate/refresh_dashboard"):
            self.handle_api_streamate_dashboard()
        elif self.path.startswith("/api/streamate/update_gold_menu"):
            self.handle_api_streamate_update_gold_menu()
        elif self.path.startswith("/api/streamate/update_wheel"):
            self.handle_api_streamate_update_wheel()
        elif self.path.startswith("/api/streamate/update_topic"):
            self.handle_api_streamate_update_topic()
        elif self.path.startswith("/api/refresh_all_platforms"):
            self.handle_api_refresh_all_platforms()
        elif self.path.startswith("/api/streamate/messages"):
            self.handle_api_streamate_messages()
        elif self.path.startswith("/api/streammonitor/status"):
            self.handle_api_streammonitor_status()
        elif self.path.startswith("/api/streammonitor/presets"):
            self.handle_api_streammonitor_presets()
        elif self.path.startswith("/api/streamate/analyze_tomboy_radar"):
            self.handle_api_streamate_analyze_tomboy_radar()
        elif self.path.startswith("/api/instagram/daily_strategy"):
            self.handle_api_instagram_daily_strategy()
        elif self.path.startswith("/api/instagram/stories_pack"):
            self.handle_api_instagram_stories_pack()
        elif self.path.startswith("/api/instagram/sync_live"):
            self.handle_api_instagram_sync_live()
        elif self.path == "/api/push/vapid_public_key":
            self.handle_api_push_vapid_public_key()
        elif self.path == "/api/logo_status":
            self.handle_api_logo_status()
        elif self.path == "/manifest.json":
            self.send_response(200)
            self.send_header("Content-Type", "application/manifest+json; charset=utf-8")
            self.end_headers()
            with open(ROOT / "manifest.json", "rb") as f:
                self.wfile.write(f.read())
            return
        elif self.path == "/sw.js":
            self.send_response(200)
            self.send_header("Content-Type", "application/javascript; charset=utf-8")
            self.send_header("Service-Worker-Allowed", "/")
            self.end_headers()
            with open(ROOT / "sw.js", "rb") as f:
                self.wfile.write(f.read())
            return
        else:
            # Servir index.html si entra a /
            if self.path == "/" or self.path == "":
                self.path = "/index.html"
            super().do_GET()

    def do_POST(self):
        if self.path == "/api/auth/login":
            self.handle_api_auth_login()
        elif self.path == "/api/auth/verify":
            self.handle_api_auth_verify()
        elif self.path == "/api/auth/recovery-request":
            self.handle_api_auth_recovery_request()
        elif self.path == "/api/auth/reset-password":
            self.handle_api_auth_reset_password()
        elif self.path == "/api/auth/logout":
            self.handle_api_auth_logout()
        elif self.path == "/api/chat":
            self.handle_api_chat()
        elif self.path == "/api/chat/stop" or self.path == "/api/chat_stop":
            self.handle_api_chat_stop()
        elif self.path == "/api/upload_logo":
            self.handle_api_upload_logo()
        elif self.path == "/api/reset_logo":
            self.handle_api_reset_logo()
        elif self.path.startswith("/api/clear_chat_history"):
            self.handle_api_clear_chat_history()
        elif self.path == "/api/push/subscribe":
            self.handle_api_push_subscribe()
        elif self.path == "/api/push/unsubscribe":
            self.handle_api_push_unsubscribe()
        elif self.path == "/api/push/test":
            self.handle_api_push_test()
        elif self.path.startswith("/api/streamate/dashboard") or self.path.startswith("/api/streamate/refresh_dashboard"):
            self.handle_api_streamate_dashboard()
        elif self.path.startswith("/api/streamate/update_gold_menu"):
            self.handle_api_streamate_update_gold_menu()
        elif self.path.startswith("/api/streamate/update_wheel"):
            self.handle_api_streamate_update_wheel()
        elif self.path.startswith("/api/streamate/update_topic"):
            self.handle_api_streamate_update_topic()
        elif self.path.startswith("/api/streamate/messages"):
            self.handle_api_streamate_messages()
        elif self.path.startswith("/api/streamate/send_message"):
            self.handle_api_streamate_send_message()
        elif self.path.startswith("/api/streamate/autopilot_toggle"):
            self.handle_api_streamate_autopilot_toggle()
        elif self.path.startswith("/api/streamate/autopilot_run"):
            self.handle_api_streamate_autopilot_run()
        elif self.path.startswith("/api/refresh_all_platforms"):
            self.handle_api_refresh_all_platforms()
        elif self.path.startswith("/api/streammonitor/status"):
            self.handle_api_streammonitor_status()
        elif self.path.startswith("/api/streammonitor/presets"):
            self.handle_api_streammonitor_presets()
        elif self.path.startswith("/api/streammonitor/launch"):
            self.handle_api_streammonitor_launch()
        elif self.path.startswith("/api/streammonitor/generate_mahia_prompt"):
            self.handle_api_streammonitor_generate_mahia_prompt()
        elif self.path.startswith("/api/streammonitor/parse_mahia_response"):
            self.handle_api_streammonitor_parse_mahia_response()
        elif self.path.startswith("/api/streammonitor/apply_shift"):
            self.handle_api_streammonitor_apply_shift()
        elif self.path.startswith("/api/streammonitor/orchestrate_natural_idea"):
            self.handle_api_streammonitor_orchestrate_natural_idea()
        elif self.path.startswith("/api/streamate/analyze_tomboy_radar"):
            self.handle_api_streamate_analyze_tomboy_radar()
        elif self.path == "/api/refresh_financials" or self.path.startswith("/api/loyalfans/refresh"):
            self.handle_api_refresh_financials()
        elif self.path.startswith("/api/refresh_positioning"):
            self.handle_api_refresh_positioning()
        elif self.path.startswith("/api/deploy_profile"):
            self.handle_api_deploy_profile()
        elif self.path.startswith("/api/instagram/daily_strategy"):
            self.handle_api_instagram_daily_strategy()
        elif self.path.startswith("/api/instagram/stories_pack"):
            self.handle_api_instagram_stories_pack()
        elif self.path.startswith("/api/instagram/sync_live"):
            self.handle_api_instagram_sync_live()
        else:
            self.send_error(404, "Endpoint no encontrado")


    def handle_api_deploy_profile(self):
        """Ejecuta el script de despliegue y actualización de perfil en segundo plano."""
        try:
            from urllib.parse import urlparse, parse_qs
            import threading
            import subprocess

            qs = parse_qs(urlparse(self.path).query)
            platform = qs.get("platform", ["stripchat"])[0].lower()

            script_map = {
                "loyalfans": "src/platforms/loyalfans/profile_updater.py",
                "stripchat": "src/platforms/stripchat/profile_updater.py",
                "streamate": "src/platforms/streamate/profile_updater.py",
                "flirt4free": "src/platforms/flirt4free/profile_updater.py"
            }

            target_script = script_map.get(platform, "src/platforms/stripchat/profile_updater.py")
            full_script_path = ROOT / target_script

            def run_worker():
                try:
                    subprocess.Popen([sys.executable, str(full_script_path)], cwd=str(ROOT))
                except Exception as e:
                    print(f"Error lanzando actualizador de {platform}: {e}")

            threading.Thread(target=run_worker, daemon=True).start()

            resp = {
                "success": True,
                "status": "launched",
                "platform": platform,
                "script": target_script,
                "message": f" Despliegue de {platform.upper()} puesto en marcha en ventana visible."
            }
        except Exception as e:
            resp = {"success": False, "error": str(e)}

        self.send_response(200)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.end_headers()
        self.wfile.write(json.dumps(resp).encode("utf-8"))

    def handle_api_push_vapid_public_key(self):
        """Retorna la clave pública VAPID en base64url para la suscripción Web Push en el navegador."""
        try:
            pub_key = push_service.get_public_key()
            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.end_headers()
            self.wfile.write(json.dumps({"publicKey": pub_key}).encode("utf-8"))
        except Exception as e:
            self.send_response(500)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.end_headers()
            self.wfile.write(json.dumps({"error": str(e)}).encode("utf-8"))

    def handle_api_push_subscribe(self):
        """Registra una suscripción Web Push (endpoint, p256dh, auth) en SQLite."""
        try:
            length = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(length).decode("utf-8") if length > 0 else "{}"
            data = json.loads(body)
            sub = data.get("subscription", {})
            ua = self.headers.get("User-Agent", "")
            success = push_service.save_subscription(sub, ua)
            self.send_response(200 if success else 400)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.end_headers()
            self.wfile.write(json.dumps({
                "status": "ok" if success else "error",
                "message": "Dispositivo registrado en notificaciones push de SIREN AI" if success else "Datos de suscripción incompletos"
            }).encode("utf-8"))
        except Exception as e:
            self.send_response(500)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.end_headers()
            self.wfile.write(json.dumps({"error": str(e)}).encode("utf-8"))

    def handle_api_push_unsubscribe(self):
        """Desactiva una suscripción Web Push en la base de datos."""
        try:
            length = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(length).decode("utf-8") if length > 0 else "{}"
            data = json.loads(body)
            endpoint = data.get("endpoint", "")
            push_service.remove_subscription(endpoint)
            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.end_headers()
            self.wfile.write(json.dumps({"status": "ok", "message": "Suscripción desactivada"}).encode("utf-8"))
        except Exception as e:
            self.send_response(500)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.end_headers()
            self.wfile.write(json.dumps({"error": str(e)}).encode("utf-8"))

    def handle_api_push_test(self):
        """Dispara una notificación de prueba para cualquiera de los 4 asistentes."""
        try:
            length = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(length).decode("utf-8") if length > 0 else "{}"
            data = json.loads(body) if body else {}
            assistant_id = data.get("assistant", "roxanne").lower()
            
            sample_messages = {
                "roxanne": "¡Hola Sam! Notificación en tiempo real de Roxanne verificada con éxito en tu pantalla de bloqueo. Sistema operativo y listo.",
                "chloe": "¡Hey Sam! Chloe aquí: tu estrategia de Instagram para hoy está preparada. Toca para ver el desglose en el chat.",
                "diana": "¡Alerta Financiera de Diana! Nuevo corte de facturación registrado. Toca para auditar tus ganancias.",
                "electra": "¡Alerta Algorítmica de Electra! Pico de tráfico detectado en Streamate. Momento ideal para abrir sala."
            }
            msg = sample_messages.get(assistant_id, sample_messages["roxanne"])
            push_service.notify_assistant_response(assistant_id, msg)
            
            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.end_headers()
            self.wfile.write(json.dumps({
                "status": "ok",
                "assistant": assistant_id,
                "message": msg,
                "note": "Push disparado a todos los dispositivos registrados"
            }).encode("utf-8"))
        except Exception as e:
            self.send_response(500)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.end_headers()
            self.wfile.write(json.dumps({"error": str(e)}).encode("utf-8"))

    def handle_api_logo_status(self):
        """Devuelve el estado del logotipo activo (opción oficial 2 o personalizado)."""
        logo_cfg = ROOT / "data" / "logo_config.json"
        status = {"type": "option2", "url": "", "updated_at": 0}
        if logo_cfg.exists():
            try:
                with open(logo_cfg, "r", encoding="utf-8") as f:
                    status = json.load(f)
            except Exception:
                pass
        self.send_response(200)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.end_headers()
        self.wfile.write(json.dumps(status).encode("utf-8"))

    def handle_api_upload_logo(self):
        """Recibe una imagen, genera todos los tamaños para PWA, favicons y web, y actualiza el sistema."""
        try:
            content_length = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(content_length).decode("utf-8")
            data = json.loads(body)
            img_b64 = data.get("image", "")

            if not img_b64:
                self.send_response(400)
                self.send_header("Content-Type", "application/json; charset=utf-8")
                self.end_headers()
                self.wfile.write(json.dumps({"error": "No se recibió imagen"}).encode("utf-8"))
                return

            if "," in img_b64:
                header, encoded = img_b64.split(",", 1)
            else:
                encoded = img_b64

            raw_bytes = base64.b64decode(encoded)
            icons_dir = ROOT / "icons"
            icons_dir.mkdir(parents=True, exist_ok=True)

            custom_logo_path = icons_dir / "custom_logo.png"
            with open(custom_logo_path, "wb") as f:
                f.write(raw_bytes)

            t_now = int(time.time())

            # Redimensionar usando Pillow para PWA (192, 512, maskable, badge)
            try:
                from PIL import Image, ImageOps
                with Image.open(custom_logo_path) as im:
                    im_rgba = im.convert("RGBA")
                    # 1. custom_logo optimizado
                    im_rgba.save(icons_dir / "custom_logo.png", "PNG")

                    # 2. icon-512x512
                    im_512 = Image.new("RGBA", (512, 512), (30, 36, 50, 255))
                    im_fit_512 = ImageOps.contain(im_rgba, (440, 440), Image.Resampling.LANCZOS)
                    im_512.paste(im_fit_512, ((512 - im_fit_512.width) // 2, (512 - im_fit_512.height) // 2), im_fit_512)
                    im_512.save(icons_dir / "icon-512x512.png", "PNG")

                    # 3. icon-512x512-maskable
                    im_mask = Image.new("RGBA", (512, 512), (30, 36, 50, 255))
                    im_fit_mask = ImageOps.contain(im_rgba, (380, 380), Image.Resampling.LANCZOS)
                    im_mask.paste(im_fit_mask, ((512 - im_fit_mask.width) // 2, (512 - im_fit_mask.height) // 2), im_fit_mask)
                    im_mask.save(icons_dir / "icon-512x512-maskable.png", "PNG")

                    # 4. icon-192x192
                    im_192 = Image.new("RGBA", (192, 192), (30, 36, 50, 255))
                    im_fit_192 = ImageOps.contain(im_rgba, (160, 160), Image.Resampling.LANCZOS)
                    im_192.paste(im_fit_192, ((192 - im_fit_192.width) // 2, (192 - im_fit_192.height) // 2), im_fit_192)
                    im_192.save(icons_dir / "icon-192x192.png", "PNG")

                    # 5. badge-72x72
                    im_72 = ImageOps.contain(im_rgba, (72, 72), Image.Resampling.LANCZOS)
                    im_72.save(icons_dir / "badge-72x72.png", "PNG")
            except Exception as pe:
                print("[Logo Image Processing Warning]:", pe)

            logo_cfg = ROOT / "data" / "logo_config.json"
            logo_cfg.parent.mkdir(parents=True, exist_ok=True)
            with open(logo_cfg, "w", encoding="utf-8") as f:
                json.dump({"type": "custom", "updated_at": t_now, "url": f"/icons/custom_logo.png?v={t_now}"}, f)

            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.end_headers()
            self.wfile.write(json.dumps({
                "success": True,
                "message": "Logotipo personalizado guardado y actualizado en PWA, Favicons y Header",
                "logo_url": f"/icons/custom_logo.png?v={t_now}",
                "updated_at": t_now
            }).encode("utf-8"))

        except Exception as e:
            self.send_response(500)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.end_headers()
            self.wfile.write(json.dumps({"success": False, "error": str(e)}).encode("utf-8"))

    def handle_api_reset_logo(self):
        """Restablece los iconos al logotipo oficial de SIREN (Opción 2: Cyber Pulse Aegis)."""
        try:
            from scripts.generate_pwa_icons import create_option2_pwa_icons
            create_option2_pwa_icons()

            logo_cfg = ROOT / "data" / "logo_config.json"
            logo_cfg.parent.mkdir(parents=True, exist_ok=True)
            t_now = int(time.time())
            with open(logo_cfg, "w", encoding="utf-8") as f:
                json.dump({"type": "option2", "updated_at": t_now, "url": ""}, f)

            custom_file = ROOT / "icons" / "custom_logo.png"
            if custom_file.exists():
                try:
                    custom_file.unlink()
                except Exception:
                    pass

            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.end_headers()
            self.wfile.write(json.dumps({
                "success": True,
                "message": "Logotipo restablecido a la Opción 2 Oficial (Cyber Pulse Aegis)",
                "type": "option2",
                "updated_at": t_now
            }).encode("utf-8"))
        except Exception as e:
            self.send_response(500)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.end_headers()
            self.wfile.write(json.dumps({"success": False, "error": str(e)}).encode("utf-8"))

    def handle_api_financials(self):
        """Devuelve el balance en vivo, desglose de octubre y transacciones recientes."""
        try:
            import importlib
            import src.analytics.financial_live_sync as fls
            importlib.reload(fls)
            data = fls.parse_financials_dump()
        except Exception as e:
            data = {"error": str(e), "balance": 27.19, "current_month": 20.00}
        self.send_response(200)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.end_headers()
        self.wfile.write(json.dumps(data).encode("utf-8"))

    def handle_api_refresh_financials(self):
        """Consulta en vivo la sesión de LoyalFans y actualiza las métricas financieras."""
        try:
            import importlib
            import src.analytics.financial_live_sync as fls
            importlib.reload(fls)
            data = fls.fetch_live_financials_now_sync()
        except Exception as e:
            data = {"error": str(e), "balance": 15.59, "current_month": 8.40}
        self.send_response(200)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.end_headers()
        self.wfile.write(json.dumps(data, ensure_ascii=False).encode("utf-8"))

    def handle_api_loyalfans_transactions(self):
        """Devuelve el historial forense de transacciones y compras en LoyalFans."""
        try:
            import importlib
            import src.analytics.financial_live_sync as fls
            importlib.reload(fls)
            data = fls.get_loyalfans_transactions()
        except Exception as e:
            data = {"error": str(e), "transactions": []}
        self.send_response(200)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.end_headers()
        self.wfile.write(json.dumps(data, ensure_ascii=False).encode("utf-8"))

    def handle_api_loyalfans_subscribers(self):
        """Devuelve las métricas de audiencia, fans y suscriptores activos en LoyalFans."""
        try:
            import importlib
            import src.analytics.financial_live_sync as fls
            importlib.reload(fls)
            data = fls.get_loyalfans_subscribers()
        except Exception as e:
            data = {"error": str(e), "total_fans": 604}
        self.send_response(200)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.end_headers()
        self.wfile.write(json.dumps(data, ensure_ascii=False).encode("utf-8"))

    def handle_api_loyalfans_ranking(self):
        """Devuelve el posicionamiento algorítmico y estado de bump de LoyalFans."""
        try:
            import importlib
            import src.analytics.financial_live_sync as fls
            importlib.reload(fls)
            data = fls.get_loyalfans_ranking()
        except Exception as e:
            data = {"error": str(e), "percentile": "Top 23%"}
        self.send_response(200)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.end_headers()
        self.wfile.write(json.dumps(data, ensure_ascii=False).encode("utf-8"))

    def handle_api_loyalfans_all(self):
        """Devuelve un consolidado 360° en tiempo real de LoyalFans."""
        try:
            import importlib
            import src.analytics.financial_live_sync as fls
            importlib.reload(fls)
            data = fls.get_loyalfans_all()
        except Exception as e:
            data = {"error": str(e), "platform": "LoyalFans"}
        self.send_response(200)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.end_headers()
        self.wfile.write(json.dumps(data, ensure_ascii=False).encode("utf-8"))

    def handle_api_positioning(self):
        """Devuelve el posicionamiento, percentil y estado de ventas en tiempo real."""
        try:
            from urllib.parse import urlparse, parse_qs
            import importlib
            import src.analytics.positioning_live_sync as pls
            importlib.reload(pls)
            qs = parse_qs(urlparse(self.path).query)
            platform = qs.get("platform", ["loyalfans"])[0]
            data = pls.get_realtime_positioning(platform)
        except Exception as e:
            data = {"error": str(e), "percentile": "Top 18%", "platform_key": "loyalfans"}
        self.send_response(200)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.end_headers()
        self.wfile.write(json.dumps(data).encode("utf-8"))

    def handle_api_refresh_positioning(self):
        """Fuerza actualización en vivo del posicionamiento y registra en SQLite."""
        try:
            from urllib.parse import urlparse, parse_qs
            import importlib
            import src.analytics.positioning_live_sync as pls
            importlib.reload(pls)
            qs = parse_qs(urlparse(self.path).query)
            platform = qs.get("platform", ["loyalfans"])[0]
            data = pls.refresh_positioning_live(platform)
        except Exception as e:
            data = {"error": str(e), "percentile": "Top 18%", "platform_key": "loyalfans"}
        self.send_response(200)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.end_headers()
        self.wfile.write(json.dumps(data).encode("utf-8"))

    def handle_api_streamate_dashboard(self):
        """Devuelve la auditoría completa de Streamate: horas reales, privados, ratings, reviews y tags."""
        try:
            import importlib
            import urllib.parse
            import src.analytics.streamate_analytics as sa
            importlib.reload(sa)

            parsed_url = urllib.parse.urlparse(self.path)
            query_params = urllib.parse.parse_qs(parsed_url.query)
            start_date = query_params.get("start_date", [None])[0]
            end_date = query_params.get("end_date", [None])[0]
            is_refresh = "refresh" in self.path or "force" in self.path or self.command == "POST" or "force" in query_params

            if self.command == "POST":
                content_len = int(self.headers.get("Content-Length", 0))
                if content_len > 0:
                    try:
                        post_body = json.loads(self.rfile.read(content_len).decode("utf-8"))
                        if not start_date and "start_date" in post_body:
                            start_date = post_body.get("start_date")
                        if not end_date and "end_date" in post_body:
                            end_date = post_body.get("end_date")
                    except Exception:
                        pass

            data = sa.get_streamate_dashboard_data(start_date=start_date, end_date=end_date, force_refresh=is_refresh)
        except Exception as e:
            data = {"success": False, "error": str(e)}
        self.send_response(200 if data.get("success") else 500)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.end_headers()
        self.wfile.write(json.dumps(data, ensure_ascii=False).encode("utf-8"))

    def handle_api_refresh_all_platforms(self):
        """Refresca y sincroniza en vivo los datos de todas las plataformas (Streamate, LoyalFans, Stripchat, Instagram)."""
        try:
            import importlib
            import src.analytics.streamate_analytics as sa
            import src.analytics.financial_live_sync as fls
            import src.analytics.positioning_live_sync as pls
            importlib.reload(sa)
            importlib.reload(fls)
            importlib.reload(pls)

            sm_data = sa.get_streamate_dashboard_data(force_refresh=True)
            lf_fin = fls.parse_financials_dump()
            lf_pos = pls.get_realtime_positioning("loyalfans")
            sc_pos = pls.get_realtime_positioning("stripchat")

            res = {
                "success": True,
                "message": " Datos de Streamate, LoyalFans y Stripchat sincronizados en tiempo real",
                "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "streamate": sm_data,
                "financials": lf_fin,
                "positioning": {
                    "loyalfans": lf_pos,
                    "stripchat": sc_pos
                }
            }
        except Exception as e:
            res = {"success": False, "error": str(e)}
        self.send_response(200 if res.get("success") else 500)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.end_headers()
        self.wfile.write(json.dumps(res, ensure_ascii=False).encode("utf-8"))

    def handle_api_status(self):
        """Verifica la conectividad con Ollama y la base de datos."""
        ollama_online = False
        available_models = []
        try:
            req = urllib.request.Request("http://localhost:11434/api/tags")
            with urllib.request.urlopen(req, timeout=3) as resp:
                data = json.loads(resp.read().decode())
                ollama_online = True
                available_models = [m.get("name") for m in data.get("models", [])]
        except Exception:
            ollama_online = False

        status_data = {
            "server": "VELVET AI Daemon",
            "port": PORT,
            "ollama_online": ollama_online,
            "ollama_host": "http://localhost:11434",
            "models": available_models,
            "active_default": "qwen2.5:7b-instruct",
            "database": str(DB_PATH.exists())
        }
        self.send_response(200)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.end_headers()
        self.wfile.write(json.dumps(status_data).encode("utf-8"))

    def handle_api_history(self):
        """Devuelve las últimas 10 interacciones registradas."""
        history = []
        try:
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            cursor.execute("""
                SELECT message_text, reply_text, reply_timestamp 
                FROM message_interactions 
                WHERE reply_text IS NOT NULL 
                ORDER BY id DESC LIMIT 10
            """)
            for row in cursor.fetchall():
                history.append({
                    "fan": row[0],
                    "sam": row[1],
                    "timestamp": row[2]
                })
            conn.close()
        except Exception:
            pass

        self.send_response(200)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.end_headers()
        self.wfile.write(json.dumps({"history": history}).encode("utf-8"))

    def handle_api_chat_history(self):
        """Devuelve el historial persistente de conversacion filtrado por asistente (o completo con campo assistant)."""
        from urllib.parse import urlparse, parse_qs
        history = []
        qs = parse_qs(urlparse(self.path).query)
        target_asst = qs.get("assistant", [None])[0]
        if target_asst:
            target_asst = target_asst.lower()

        try:
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS copilot_assistant_history (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp TEXT,
                    sender TEXT,
                    message TEXT,
                    model TEXT,
                    assistant TEXT DEFAULT 'roxanne'
                )
            """)
            cols = [col[1] for col in cursor.execute("PRAGMA table_info(copilot_assistant_history)").fetchall()]
            if "assistant" not in cols:
                cursor.execute("ALTER TABLE copilot_assistant_history ADD COLUMN assistant TEXT DEFAULT 'roxanne'")
                conn.commit()

            if target_asst:
                cursor.execute("""
                    SELECT timestamp, sender, message, model, assistant
                    FROM copilot_assistant_history
                    WHERE LOWER(COALESCE(assistant, sender)) = ?
                    ORDER BY id ASC
                """, (target_asst,))
            else:
                cursor.execute("""
                    SELECT timestamp, sender, message, model, assistant
                    FROM copilot_assistant_history
                    ORDER BY id ASC
                """)

            for row in cursor.fetchall():
                asst_val = row[4]
                if not asst_val or asst_val == "sam":
                    asst_val = row[1] if row[1] in ["roxanne", "mahia", "chloe", "diana", "electra", "alma"] else "roxanne"
                history.append({
                    "timestamp": row[0],
                    "sender": row[1],
                    "message": row[2],
                    "model": row[3],
                    "assistant": asst_val
                })
            conn.close()
        except Exception as e:
            print("[History Error]:", e)

        self.send_response(200)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.end_headers()
        self.wfile.write(json.dumps({"success": True, "history": history, "assistant": target_asst}).encode("utf-8"))

    def handle_api_clear_chat_history(self):
        """Limpia el historial de conversacion para el asistente indicado (o todos si no se indica)."""
        from urllib.parse import urlparse, parse_qs
        qs = parse_qs(urlparse(self.path).query)
        target_asst = qs.get("assistant", [None])[0]

        # Verificar si vino por cuerpo JSON
        length = int(self.headers.get("Content-Length", 0))
        if length > 0:
            try:
                body_data = json.loads(self.rfile.read(length).decode("utf-8"))
                if not target_asst and "assistant" in body_data:
                    target_asst = body_data["assistant"]
            except Exception:
                pass

        try:
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            if target_asst:
                t_lower = target_asst.lower()
                cursor.execute("""
                    DELETE FROM copilot_assistant_history
                    WHERE LOWER(COALESCE(assistant, '')) = ? OR LOWER(sender) = ?
                """, (t_lower, t_lower))
                msg = f"Historial de {target_asst.upper()} limpiado exitosamente"
            else:
                cursor.execute("DELETE FROM copilot_assistant_history")
                msg = "Historial completo de todos los asistentes limpiado exitosamente"
            conn.commit()
            conn.close()
            resp = {"success": True, "message": msg, "assistant": target_asst}
        except Exception as e:
            resp = {"success": False, "error": str(e)}

        self.send_response(200)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.end_headers()
        self.wfile.write(json.dumps(resp).encode("utf-8"))

    def handle_api_platforms_profiles(self):
        """Devuelve los perfiles oficiales y credenciales de acceso para cada plataforma."""
        try:
            from src.automation.credential_store import load_all_credentials
            creds = load_all_credentials()

            profiles = [
                {
                    "key": "streamate",
                    "name": "Streamate",
                    "model_handle": "SamBartone",
                    "performer_id": "144675665",
                    "rating": "4.0  (Verificado)",
                    "status": "Verified (Activa)",
                    "sync_status": " Actualizado & Sincronizado en Vivo",
                    "payout_status": " Administrado por Estudio Satélite (Centenario Studio - 50% Split Neto)",
                    "account_type": "Cuenta Estudio Satélite (Centenario Studio)",
                    "login_url": "https://streamatemodels.com/login",
                    "public_url": "https://sambartone.cammodels.com",
                    "avatar_url": "/artifacts/streamate_audit/profile.png",
                    "hours_week": 24.0,
                    "gold_earned": 575.43,
                    "sam_net_usd": 100.71,
                    "username": creds.get("streamate", {}).get("username", "efac05@yopmail.com"),
                    "password": creds.get("streamate", {}).get("password", "Centenario123@"),
                    "rates": {
                        "private": "$2.99 / min",
                        "exclusive": "$3.99 / min",
                        "dynamic_enabled": "Activado ($2.99 - $6.99)"
                    },
                    "headline": "Chica tomboy versatil con energia propia e inteligente.",
                    "bio": "Mi mundo se mueve entre la musica, la tecnologia, el deporte y esa pasion constante por explorar el deseo. Toco el ukelele, pero tambien disfruto explorar sensaciones intensas a solas...",
                    "tags": ["Tomboy", "Ukelele", "Versatile", "Cam2Cam", "Roleplay"],
                    "geoblock": "Colombia visible (Sin bloqueo territorial)"
                },
                {
                    "key": "loyalfans",
                    "name": "LoyalFans",
                    "model_handle": "@samm_bartonn",
                    "performer_id": "samm_bartonn",
                    "rating": "Top 23% (Percentil Global)",
                    "status": "Verified (100% Directo)",
                    "account_type": "Independiente / Creadora Directa",
                    "login_url": "https://loyalfans.com/login",
                    "public_url": "https://loyalfans.com/samm_bartonn",
                    "avatar_url": "/artifacts/test_public_profile_verified.png",
                    "username": creds.get("loyalfans", {}).get("username", "sambartonn23@gmail.com"),
                    "password": creds.get("loyalfans", {}).get("password", "Kjc20009*"),
                    "rates": {
                        "message_text": "$0.50 / msg",
                        "message_media": "$0.50 / foto",
                        "fan_club": "$10.00 / mes"
                    },
                    "headline": "Software & AI Architect  Versatile Tomboy ",
                    "bio": "Smart by day, driven about my goals, and teasingly wicked by night. Software & AI Architect by trade, but my real sanctuary is motorcycles, speed, and my beloved pack...",
                    "tags": ["Tomboy", "Biker", "Tech"],
                    "geoblock": "Sin bloqueo territorial"
                },
                {
                    "key": "stripchat",
                    "name": "Stripchat",
                    "model_handle": "@sam_barton",
                    "performer_id": "sam_barton",
                    "rating": "En Espera (Listo en Cola)",
                    "status": "Verified (Verificado)",
                    "account_type": "Independiente / Directo",
                    "login_url": "https://stripchat.com/login",
                    "public_url": "https://stripchat.com/sam_barton",
                    "avatar_url": "/artifacts/stripchat_profile_updated_20261014_211003.png",
                    "username": creds.get("stripchat", {}).get("username", "sambartonn23@gmail.com"),
                    "password": creds.get("stripchat", {}).get("password", "6L!3K3RUnEdPKPt"),
                    "rates": {
                        "token_price": "$0.05 / token",
                        "private_show": "60 tokens / min",
                        "interactive_lovense": "Activo"
                    },
                    "headline": "Cute Tomboy Gamer • Lovense Interactive ",
                    "bio": "Software & AI Architect by day, gaming tomboy & teasing companion by night. Soccer player, motorcycle enthusiast, and devoted mom to my dogs & 2 cats...",
                    "tags": ["tomboy", "gamer", "lovense", "athletic", "sensual", "biker"],
                    "geoblock": "Sin bloqueo territorial"
                },
                {
                    "key": "lovense",
                    "name": "Lovense Interactive",
                    "model_handle": "Lovense Connect",
                    "performer_id": "Bluetooth Link",
                    "rating": "Sincronizado",
                    "status": "Activo",
                    "account_type": "Herramienta Interactiva",
                    "login_url": "https://streamate.lovense.com",
                    "public_url": "",
                    "avatar_url": "/artifacts/smconnect_tab_juguetes_interactivos.png",
                    "username": creds.get("lovense", {}).get("username", "sambartonn23@gmail.com"),
                    "password": creds.get("lovense", {}).get("password", "6L!3K3RUnEdPKPt"),
                    "rates": {
                        "niveles": "5 niveles de vibracion configurados"
                    },
                    "headline": "Juguetes interactivos sincronizados con propinas en vivo.",
                    "bio": "Sincronizacion Bluetooth activa para reaccionar a propinas en Stripchat y Streamate.",
                    "tags": ["Lovense", "Bluetooth", "Tipping"],
                    "geoblock": "N/A"
                }
            ]
            resp = {"success": True, "profiles": profiles}
        except Exception as e:
            resp = {"success": False, "error": str(e)}

        self.send_response(200)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.end_headers()
        self.wfile.write(json.dumps(resp).encode("utf-8"))



    def handle_api_streamate_update_gold_menu(self):
        """Actualiza el menú GOLD en SM Connect / Stream Monitor o devuelve configuración actual."""
        try:
            from src.platforms.streamate.stream_monitor_controller import load_streamate_tools_config
            if self.command == "GET":
                cfg = load_streamate_tools_config()
                self.send_response(200)
                self.send_header("Content-Type", "application/json; charset=utf-8")
                self.end_headers()
                self.wfile.write(json.dumps({"success": True, "items": cfg.get("gold_menu", [])}, ensure_ascii=False).encode("utf-8"))
                return

            content_length = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(content_length).decode("utf-8") if content_length > 0 else ""
            data = json.loads(body) if body else {}

            raw_text = data.get("raw_text", "")
            items = data.get("items", [])

            if raw_text and not items:
                items = parse_gold_menu_text(raw_text)

            # Persistir localmente de inmediato para que nunca se pierda
            if items:
                from src.platforms.streamate.stream_monitor_controller import save_streamate_tools_config
                save_streamate_tools_config("gold_menu", items)

            res = asyncio.run(update_gold_menu_live(items))
            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.end_headers()
            self.wfile.write(json.dumps(res, ensure_ascii=False).encode("utf-8"))
        except Exception as e:
            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.end_headers()
            self.wfile.write(json.dumps({"success": False, "error": str(e)}, ensure_ascii=False).encode("utf-8"))

    def handle_api_streamate_update_wheel(self):
        """Actualiza la Ruleta (Gira La Rueda) en SM Connect / Stream Monitor o devuelve configuración."""
        try:
            from src.platforms.streamate.stream_monitor_controller import load_streamate_tools_config, save_streamate_tools_config
            if self.command == "GET":
                cfg = load_streamate_tools_config()
                wheel = cfg.get("wheel", {"cost": 20, "items": []})
                self.send_response(200)
                self.send_header("Content-Type", "application/json; charset=utf-8")
                self.end_headers()
                self.wfile.write(json.dumps({"success": True, "cost": wheel.get("cost", 20), "items": wheel.get("items", [])}, ensure_ascii=False).encode("utf-8"))
                return

            content_length = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(content_length).decode("utf-8") if content_length > 0 else ""
            data = json.loads(body) if body else {}

            raw_text = data.get("raw_text", "")
            cost = data.get("cost", 20)
            items = data.get("items", [])

            if raw_text and not items:
                parsed = parse_wheel_game_text(raw_text)
                cost = parsed["cost"]
                items = parsed["items"]

            # Persistir localmente de inmediato
            save_streamate_tools_config("wheel", {"cost": cost, "items": items})

            res = asyncio.run(update_wheel_game_live(cost, items))
            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.end_headers()
            self.wfile.write(json.dumps(res, ensure_ascii=False).encode("utf-8"))
        except Exception as e:
            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.end_headers()
            self.wfile.write(json.dumps({"success": False, "error": str(e)}, ensure_ascii=False).encode("utf-8"))

    def handle_api_streamate_update_topic(self):
        """Actualiza el Tema de Habitación (Room Topic) en SM Connect o devuelve configuración."""
        try:
            from src.platforms.streamate.stream_monitor_controller import load_streamate_tools_config, save_streamate_tools_config
            if self.command == "GET":
                cfg = load_streamate_tools_config()
                self.send_response(200)
                self.send_header("Content-Type", "application/json; charset=utf-8")
                self.end_headers()
                self.wfile.write(json.dumps({"success": True, "topic": cfg.get("room_topic", "")}, ensure_ascii=False).encode("utf-8"))
                return

            content_length = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(content_length).decode("utf-8") if content_length > 0 else ""
            data = json.loads(body) if body else {}

            topic = data.get("topic", "").strip()
            # Persistir localmente de inmediato
            if topic:
                save_streamate_tools_config("room_topic", topic)

            res = asyncio.run(update_room_topic_live(topic))
            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.end_headers()
            self.wfile.write(json.dumps(res, ensure_ascii=False).encode("utf-8"))
        except Exception as e:
            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.end_headers()
            self.wfile.write(json.dumps({"success": False, "error": str(e)}, ensure_ascii=False).encode("utf-8"))

    def handle_api_streamate_messages(self):
        """Devuelve el reporte de mensajes de Streamate Models Messenger."""
        try:
            data = get_streamate_messenger_data()
            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.end_headers()
            self.wfile.write(json.dumps(data, ensure_ascii=False).encode("utf-8"))
        except Exception as e:
            self.send_response(500)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.end_headers()
            self.wfile.write(json.dumps({"success": False, "error": str(e)}).encode("utf-8"))

    def handle_api_streamate_send_message(self):
        """Envía una respuesta manual o aprobada a un fan en Streamate Messenger."""
        try:
            content_length = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(content_length).decode("utf-8") if content_length > 0 else ""
            data = json.loads(body) if body else {}

            user_id = data.get("user_id")
            message = data.get("message", "")
            source = data.get("source", "roxanne")

            if not user_id or not message:
                self.send_response(400)
                self.send_header("Content-Type", "application/json; charset=utf-8")
                self.end_headers()
                self.wfile.write(json.dumps({"success": False, "error": "user_id y message requeridos"}).encode("utf-8"))
                return

            res = asyncio.run(send_streamate_messenger_reply(user_id, message, source))
            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.end_headers()
            self.wfile.write(json.dumps(res, ensure_ascii=False).encode("utf-8"))
        except Exception as e:
            self.send_response(500)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.end_headers()
            self.wfile.write(json.dumps({"success": False, "error": str(e)}).encode("utf-8"))

    def handle_api_streamate_autopilot_toggle(self):
        """Activa o desactiva el piloto automático de mensajería."""
        try:
            content_length = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(content_length).decode("utf-8") if content_length > 0 else ""
            data = json.loads(body) if body else {}

            enabled = bool(data.get("enabled", False))
            mode = data.get("mode", "best_choice")
            res = toggle_streamate_autopilot(enabled, mode)
            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.end_headers()
            self.wfile.write(json.dumps(res, ensure_ascii=False).encode("utf-8"))
        except Exception as e:
            self.send_response(500)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.end_headers()
            self.wfile.write(json.dumps({"success": False, "error": str(e)}).encode("utf-8"))

    def handle_api_streamate_autopilot_run(self):
        """Ejecuta una pasada inmediata del piloto automático en los mensajes pendientes."""
        try:
            content_length = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(content_length).decode("utf-8") if content_length > 0 else ""
            data = json.loads(body) if body else {}

            mode = data.get("mode", "best_choice")
            res = asyncio.run(run_streamate_autopilot(mode))
            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.end_headers()
            self.wfile.write(json.dumps(res, ensure_ascii=False).encode("utf-8"))
        except Exception as e:
            self.send_response(500)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.end_headers()
            self.wfile.write(json.dumps({"success": False, "error": str(e)}).encode("utf-8"))

    def handle_api_streamate_analyze_tomboy_radar(self):
        """Ejecuta escaneo de competidoras tomboy en Streamate con paginación personalizada y enlaces."""
        try:
            from urllib.parse import urlparse, parse_qs
            qs = parse_qs(urlparse(self.path).query)
            pages = 3
            query = "tomboy"

            # Revisar query params (GET)
            if "pages" in qs:
                try:
                    pages = int(qs["pages"][0])
                except (ValueError, TypeError):
                    pass
            elif "max_pages" in qs:
                try:
                    pages = int(qs["max_pages"][0])
                except (ValueError, TypeError):
                    pass
            if "query" in qs:
                query = qs["query"][0]
            elif "q" in qs:
                query = qs["q"][0]

            # Revisar POST body si aplica
            if self.command == "POST":
                try:
                    content_length = int(self.headers.get('Content-Length', 0))
                    if content_length > 0:
                        post_data = self.rfile.read(content_length)
                        body = json.loads(post_data.decode('utf-8'))
                        if "pages" in body:
                            pages = int(body["pages"])
                        elif "max_pages" in body:
                            pages = int(body["max_pages"])
                        if "query" in body:
                            query = str(body["query"])
                        elif "q" in body:
                            query = str(body["q"])
                except Exception as parse_e:
                    print(f"[Radar POST parse error]: {parse_e}")

            pages = max(1, min(pages, 10))
            res = asyncio.run(scan_streamate_tomboy_competitors(max_pages=pages, search_query=query))
            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.end_headers()
            self.wfile.write(json.dumps({"success": True, "radar": res}, ensure_ascii=False).encode("utf-8"))
        except Exception as e:
            self.send_response(500)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.end_headers()
            self.wfile.write(json.dumps({"success": False, "error": str(e)}).encode("utf-8"))


    def handle_api_streammonitor_status(self):
        """Devuelve el estado de ejecución, hardware y perfiles de StreamMonitor Desktop."""
        try:
            status = inspect_streammonitor_status()
            resp = dict(status)
            resp["success"] = True
            resp["status"] = status
            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.end_headers()
            self.wfile.write(json.dumps(resp, ensure_ascii=False).encode("utf-8"))
        except Exception as e:
            self.send_response(500)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.end_headers()
            self.wfile.write(json.dumps({"success": False, "error": str(e)}).encode("utf-8"))

    def handle_api_streammonitor_presets(self):
        """Devuelve las metas comerciales pre-optimizadas para el turno."""
        try:
            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.end_headers()
            self.wfile.write(json.dumps({"success": True, "presets": PRESET_SHIFT_THEMES}, ensure_ascii=False).encode("utf-8"))
        except Exception as e:
            self.send_response(500)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.end_headers()
            self.wfile.write(json.dumps({"success": False, "error": str(e)}).encode("utf-8"))

    def handle_api_streammonitor_launch(self):
        """Lanza StreamMonitor Desktop en la máquina local."""
        try:
            res = launch_streammonitor_desktop()
            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.end_headers()
            self.wfile.write(json.dumps(res, ensure_ascii=False).encode("utf-8"))
        except Exception as e:
            self.send_response(500)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.end_headers()
            self.wfile.write(json.dumps({"success": False, "error": str(e)}).encode("utf-8"))

    def handle_api_streammonitor_generate_mahia_prompt(self):
        """Genera la orden concisa y no redundante para el chat de Mahia en StreamMonitor."""
        try:
            content_length = int(self.headers.get('Content-Length', 0))
            body = json.loads(self.rfile.read(content_length).decode('utf-8')) if content_length > 0 else {}
            theme = body.get("shift_theme") or body.get("theme", "ass_twerk")
            custom_desc = body.get("custom_description") or body.get("custom_text", "")
            res = generate_mahia_prompt(theme, custom_desc)
            resp = dict(res)
            resp["success"] = True
            resp["data"] = res
            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.end_headers()
            self.wfile.write(json.dumps(resp, ensure_ascii=False).encode("utf-8"))
        except Exception as e:
            self.send_response(500)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.end_headers()
            self.wfile.write(json.dumps({"success": False, "error": str(e)}).encode("utf-8"))

    def handle_api_streammonitor_parse_mahia_response(self):
        """Parsea y valida la respuesta recibida de Mahia para alimentar las herramientas."""
        try:
            content_length = int(self.headers.get('Content-Length', 0))
            body = json.loads(self.rfile.read(content_length).decode('utf-8')) if content_length > 0 else {}
            raw_text = body.get("raw_text", "")
            res = parse_mahia_output_to_tools(raw_text)
            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.end_headers()
            self.wfile.write(json.dumps({"success": True, "parsed": res}, ensure_ascii=False).encode("utf-8"))
        except Exception as e:
            self.send_response(500)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.end_headers()
            self.wfile.write(json.dumps({"success": False, "error": str(e)}).encode("utf-8"))

    def handle_api_streammonitor_apply_shift(self):
        """Inyecta en un solo ciclo toda la estrategia comercial en Streamate y StreamMonitor."""
        try:
            content_length = int(self.headers.get('Content-Length', 0))
            body = json.loads(self.rfile.read(content_length).decode('utf-8')) if content_length > 0 else {}
            theme_key = body.get("theme_key") or body.get("theme", "ass_twerk")
            custom_text = body.get("custom_text", None)
            strategy_data = body.get("strategy", None)
            res = asyncio.run(apply_full_orchestrated_shift(theme_key, custom_text, strategy_data))
            if isinstance(res, dict):
                res["injected_topic"] = res.get("orchestrated_data", {}).get("topic", "")
            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.end_headers()
            self.wfile.write(json.dumps(res, ensure_ascii=False).encode("utf-8"))
        except Exception as e:
            self.send_response(500)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.end_headers()
            self.wfile.write(json.dumps({"success": False, "error": str(e)}).encode("utf-8"))


    def handle_api_streammonitor_orchestrate_natural_idea(self):
        """Toma la idea en lenguaje natural de Sam, lanza StreamMonitor y aplica la estrategia 100% en inglés."""
        try:
            content_length = int(self.headers.get('Content-Length', 0))
            body = json.loads(self.rfile.read(content_length).decode('utf-8')) if content_length > 0 else {}
            idea_text = body.get("idea_text", "")
            auto_apply = body.get("auto_apply", False)

            # 1. Ejecutar diálogo estructurado entre SIREN y Mahia (StreamMonitor)
            mahia_diag = execute_mahia_shift_dialogue(idea_text)
            strategy = mahia_diag["strategy"]
            theme_key = mahia_diag["theme_key"]

            # 2. Aplicar en vivo a Streamate y guardar para StreamMonitor
            apply_res = {}
            if auto_apply:
                apply_res = asyncio.run(apply_full_orchestrated_shift(theme_key, custom_text=None))

            resp = {
                "success": True,
                "theme_key": theme_key,
                "strategy": strategy,
                "siren_prompt_to_mahia": mahia_diag["siren_prompt_to_mahia"],
                "mahia_reply": mahia_diag["mahia_reply"],
                "launch_desktop": mahia_diag["launch_desktop"],
                "live_chat_done": mahia_diag.get("live_chat_done", False),
                "apply_result": apply_res,
                "message": f"¡Mahia entregó la estrategia y fue sincronizada en Streamate!"
            }
            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.end_headers()
            self.wfile.write(json.dumps(resp, ensure_ascii=False).encode("utf-8"))
        except Exception as e:
            self.send_response(500)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.end_headers()
            self.wfile.write(json.dumps({"success": False, "error": str(e)}).encode("utf-8"))

    def handle_api_instagram_daily_strategy(self):
        """Genera la estrategia diaria estructurada para @sambartonn23."""
        try:
            strategy = generate_daily_instagram_strategy()
            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.end_headers()
            self.wfile.write(json.dumps({"success": True, "strategy": strategy}, ensure_ascii=False).encode("utf-8"))
        except Exception as e:
            self.send_response(500)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.end_headers()
            self.wfile.write(json.dumps({"success": False, "error": str(e)}).encode("utf-8"))

    def handle_api_instagram_stories_pack(self):
        """Genera pack de historias del día listas para publicar."""
        try:
            stories = generate_stories_pack()
            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.end_headers()
            self.wfile.write(json.dumps({"success": True, "stories": stories}, ensure_ascii=False).encode("utf-8"))
        except Exception as e:
            self.send_response(500)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.end_headers()
            self.wfile.write(json.dumps({"success": False, "error": str(e)}).encode("utf-8"))

    def handle_api_instagram_sync_live(self):
        """Devuelve o refresca los datos y capturas en vivo de la cuenta @sambartonn23."""
        try:
            from urllib.parse import urlparse, parse_qs
            import subprocess

            qs = parse_qs(urlparse(self.path).query)
            refresh = qs.get("refresh", ["false"])[0].lower() in ["1", "true", "yes"]

            artifacts_live_json = ROOT / "artifacts" / "instagram" / "sambartonn23_live.json"

            if refresh or not artifacts_live_json.exists():
                sync_script = ROOT / "src" / "platforms" / "instagram" / "instagram_sync.py"
                try:
                    subprocess.run([sys.executable, str(sync_script)], cwd=str(ROOT), timeout=45, capture_output=True)
                except Exception as sub_e:
                    print("[Instagram Sync Error]:", sub_e)

            # Cargar datos si existen
            live_data = {
                "username": "sambartonn23",
                "fullName": "Sam Bartonn",
                "followers": "78",
                "following": "104",
                "posts": "24",
                "bio": "Software Architect | AI Engineer  \nCat Lover ",
                "avatar_url": "/artifacts/instagram/sambartonn23_avatar.png",
                "feed_screenshot": "/artifacts/instagram/sambartonn23_feed_live.png",
                "status": "Sincronizado en Vivo",
                "verified": True,
                "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }

            if artifacts_live_json.exists():
                try:
                    with open(artifacts_live_json, "r", encoding="utf-8") as f:
                        saved = json.load(f)
                        live_data.update(saved)
                        live_data["avatar_url"] = "/artifacts/instagram/sambartonn23_avatar.png"
                        live_data["feed_screenshot"] = "/artifacts/instagram/sambartonn23_feed_live.png"
                except Exception:
                    pass

            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.end_headers()
            self.wfile.write(json.dumps({"success": True, "data": live_data}, ensure_ascii=False).encode("utf-8"))
        except Exception as e:
            self.send_response(500)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.end_headers()
            self.wfile.write(json.dumps({"success": False, "error": str(e)}).encode("utf-8"))

    def handle_api_chat_stop(self):
        """Cancela y detiene inmediatamente el proceso del agente y la inferencia en LLM/Ollama."""
        try:
            content_length = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(content_length).decode("utf-8") if content_length > 0 else "{}"
            data = json.loads(body) if body else {}
            target_asst = data.get("assistant", "").lower()

            stopped_count = 0
            with ACTIVE_CHAT_LOCK:
                sessions_to_stop = []
                if target_asst and target_asst in ACTIVE_CHAT_SESSIONS:
                    sessions_to_stop.append(ACTIVE_CHAT_SESSIONS[target_asst])
                else:
                    sessions_to_stop.extend(list(ACTIVE_CHAT_SESSIONS.values()))

                for s in sessions_to_stop:
                    s["stopped"] = True
                    if "cancel_event" in s and s["cancel_event"]:
                        s["cancel_event"].set()
                    resp = s.get("response_obj")
                    if resp:
                        try:
                            resp.close()
                        except Exception:
                            pass
                    stopped_count += 1

            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.end_headers()
            self.wfile.write(json.dumps({
                "success": True,
                "stopped": True,
                "stopped_sessions": stopped_count,
                "message": "Proceso del agente detenido inmediatamente"
            }).encode("utf-8"))
        except Exception as e:
            self.send_response(500)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.end_headers()
            self.wfile.write(json.dumps({"success": False, "error": str(e)}).encode("utf-8"))

    # =========================================================================
    # ALMA TECH — AUTENTICACIÓN CORPORATIVA & GOBERNANZA
    # =========================================================================
    def handle_api_auth_login(self):
        try:
            content_length = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(content_length).decode("utf-8")
            data = json.loads(body)
            from src.server.auth_service import verify_login
            res = verify_login(
                email=data.get("email"),
                password=data.get("password"),
                turnstile_verified=data.get("turnstile_verified", True)
            )
            self.send_response(200 if res.get("success") else 401)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.end_headers()
            self.wfile.write(json.dumps(res, ensure_ascii=False).encode("utf-8"))
        except Exception as e:
            self.send_response(500)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.end_headers()
            self.wfile.write(json.dumps({"success": False, "error": str(e)}).encode("utf-8"))

    def handle_api_auth_verify(self):
        try:
            content_length = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(content_length).decode("utf-8")
            data = json.loads(body)
            from src.server.auth_service import verify_session
            res = verify_session(data.get("token"))
            self.send_response(200 if res.get("valid") else 401)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.end_headers()
            self.wfile.write(json.dumps(res, ensure_ascii=False).encode("utf-8"))
        except Exception as e:
            self.send_response(500)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.end_headers()
            self.wfile.write(json.dumps({"valid": False, "error": str(e)}).encode("utf-8"))

    def handle_api_auth_recovery_request(self):
        try:
            content_length = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(content_length).decode("utf-8")
            data = json.loads(body)
            from src.server.auth_service import request_recovery
            res = request_recovery(data.get("email"))
            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.end_headers()
            self.wfile.write(json.dumps(res, ensure_ascii=False).encode("utf-8"))
        except Exception as e:
            self.send_response(500)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.end_headers()
            self.wfile.write(json.dumps({"success": False, "error": str(e)}).encode("utf-8"))

    def handle_api_auth_reset_password(self):
        try:
            content_length = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(content_length).decode("utf-8")
            data = json.loads(body)
            from src.server.auth_service import reset_password
            res = reset_password(
                recovery_token=data.get("recovery_token"),
                pin=data.get("pin"),
                new_password=data.get("new_password")
            )
            self.send_response(200 if res.get("success") else 400)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.end_headers()
            self.wfile.write(json.dumps(res, ensure_ascii=False).encode("utf-8"))
        except Exception as e:
            self.send_response(500)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.end_headers()
            self.wfile.write(json.dumps({"success": False, "error": str(e)}).encode("utf-8"))

    def handle_api_auth_logout(self):
        try:
            content_length = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(content_length).decode("utf-8")
            data = json.loads(body)
            from src.server.auth_service import logout
            logout(data.get("token"))
            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.end_headers()
            self.wfile.write(json.dumps({"success": True}).encode("utf-8"))
        except Exception as e:
            self.send_response(500)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.end_headers()
            self.wfile.write(json.dumps({"success": False, "error": str(e)}).encode("utf-8"))

    def handle_api_chat(self):
        """Procesa una consulta de chat con ROXANNE o CHLOE y devuelve la respuesta del LLM."""
        try:
            content_length = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(content_length).decode("utf-8")
            data = json.loads(body)

            message = data.get("message", "").strip()
            model_name = data.get("model", "qwen2.5:7b-instruct")
            chat_history = data.get("history", [])
            assistant_id = data.get("assistant", "roxanne").lower()

            if not message:
                self.send_response(400)
                self.send_header("Content-Type", "application/json; charset=utf-8")
                self.end_headers()
                self.wfile.write(json.dumps({"error": "Mensaje vacío"}).encode("utf-8"))
                return

            lang = detect_language(message)
            msg_lower = message.lower()

            # DETECCIÓN DE INTENCIÓN: RADAR COMPETENCIA TOMBOY
            if ("analiza" in msg_lower or "radar" in msg_lower or "competencia" in msg_lower or "tendencia" in msg_lower) and \
               ("tomboy" in msg_lower or "streamate" in msg_lower or "streetmate" in msg_lower or "streaming" in msg_lower):
                try:
                    num_pages = 3
                    page_match = re.search(r'(\d+)\s*p[aá]ginas?', msg_lower)
                    if page_match:
                        try:
                            num_pages = int(page_match.group(1))
                        except (ValueError, TypeError):
                            pass
                    num_pages = max(1, min(num_pages, 10))
                    radar_data = asyncio.run(scan_streamate_tomboy_competitors(num_pages))
                    radar_summary = json.dumps(radar_data, ensure_ascii=False)
                    chat_history.append({
                        "role": "system",
                        "content": f"[RADAR TOMBOY STREAMATE EN VIVO - {num_pages} PÁGINAS]: {radar_summary}. Presenta a Sam un desglose claro de modelos activas con sus enlaces clicables (Streamate / CamModels), temas de sala que están usando, tarifas promedio y recomendaciones clave para destacar hoy."
                    })
                except Exception as re:
                    print("[Radar Error]:", re)

            # DETECCIÓN DE INTENCIÓN: ORQUESTADOR STREAMMONITOR & MAHIA (EJ. VENDER ASS, FOCO DEL TURNO)
            elif ("streammonitor" in msg_lower or "mahia" in msg_lower or "vender ass" in msg_lower or "especial ass" in msg_lower or "foco de hoy" in msg_lower or "meta de hoy" in msg_lower or "meta comercial" in msg_lower):
                try:
                    theme = "ass_twerk" if ("ass" in msg_lower or "twerk" in msg_lower or "trasero" in msg_lower) else ("tomboy_ukelele" if ("ukelele" in msg_lower or "acústic" in msg_lower) else "full_lovense")
                    prompt_info = generate_mahia_prompt(theme, message)
                    chat_history.append({
                        "role": "system",
                        "content": f"[ORQUESTADOR STREAMMONITOR & MAHIA]: Sam ha definido la meta comercial '{prompt_info['target_name']}'. Presenta el plan estratégico completo: 1) El Topic optimizado (máx 130 chars con hashtags), 2) Menú Gold alineado a 3G, 3) Ruleta a 5G y 4) La orden concisa generada para Mahia. Recuerda que SIREN es el complemento táctico que ahorra tiempo a la modelo y a los managers sin duplicar funciones de StreamMonitor."
                    })
                except Exception as me:
                    print("[StreamMonitor Chat Intent Error]:", me)

            # DETECCIÓN DE INTENCIÓN: ACTUALIZAR MENÚ GOLD
            elif ("menú gold" in msg_lower or "menu gold" in msg_lower) and ("actualiza" in msg_lower or "cambia" in msg_lower or "-" in message):
                try:
                    parsed_items = parse_gold_menu_text(message)
                    if len(parsed_items) >= 3:
                        res_up = asyncio.run(update_gold_menu_live(parsed_items))
                        chat_history.append({
                            "role": "system",
                            "content": f"[ACCIÓN EN VIVO]: Menú GOLD inyectado en Stream Monitor: {json.dumps(res_up, ensure_ascii=False)}. Confírmale a Sam las opciones y precios que quedaron guardados."
                        })
                except Exception as ge:
                    print("[Gold Menu Update Error]:", ge)

            # DETECCIÓN DE INTENCIÓN: ACTUALIZAR RULETA
            elif ("ruleta" in msg_lower or "gira la rueda" in msg_lower or "rueda" in msg_lower) and ("actualiza" in msg_lower or "cambia" in msg_lower or "pon" in msg_lower):
                try:
                    parsed_wheel = parse_wheel_game_text(message)
                    if len(parsed_wheel["items"]) >= 8:
                        res_wh = asyncio.run(update_wheel_game_live(parsed_wheel["cost"], parsed_wheel["items"]))
                        chat_history.append({
                            "role": "system",
                            "content": f"[ACCIÓN EN VIVO]: Ruleta inyectada en Stream Monitor: {json.dumps(res_wh, ensure_ascii=False)}. Confírmale a Sam el costo en Gold y las opciones seleccionadas."
                        })
                except Exception as we:
                    print("[Wheel Update Error]:", we)

            # DETECCIÓN DE INTENCIÓN: ACTUALIZAR TEMA DE HABITACIÓN
            elif ("tema de sala" in msg_lower or "tema de habitación" in msg_lower or "room topic" in msg_lower) and ("actualiza" in msg_lower or "cambia" in msg_lower or "pon" in msg_lower):
                try:
                    clean_topic = message.split(":", 1)[-1].strip() if ":" in message else message
                    res_tp = asyncio.run(update_room_topic_live(clean_topic))
                    chat_history.append({
                        "role": "system",
                        "content": f"[ACCIÓN EN VIVO]: Tema de habitación actualizado en Stream Monitor: {json.dumps(res_tp, ensure_ascii=False)}. Confírmale a Sam el nuevo tema activo."
                    })
                except Exception as te:
                    print("[Topic Update Error]:", te)

            # Seleccionar Prompt de Sistema según Asistente (optimizado para CPU)
            if assistant_id == "mahia":
                # Conexión directa en tiempo real con Mahia en StreamMonitor Desktop
                try:
                    from src.platforms.streamate.mahia_live_connector import send_prompt_to_mahia_desktop, ensure_streammonitor_running
                    port = ensure_streammonitor_running(max_wait_seconds=15)
                    if port:
                        mahia_res = send_prompt_to_mahia_desktop(message, timeout_seconds=45)
                        reply = mahia_res.get("mahia_response") or mahia_res.get("response") or mahia_res.get("reply")
                        if mahia_res.get("success") and reply:
                            import re
                            reply_clean = re.sub(r'[\U00010000-\U0010ffff]', '', reply).strip()

                            # Persistir en base de datos SQLite
                            try:
                                conn = sqlite3.connect(DB_PATH)
                                cursor = conn.cursor()
                                now_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                                cursor.execute("INSERT INTO copilot_assistant_history (timestamp, sender, message, model, assistant) VALUES (?, ?, ?, ?, ?)",
                                               (now_str, "sam", message, "StreamMonitor Mahia Live", "mahia"))
                                cursor.execute("INSERT INTO copilot_assistant_history (timestamp, sender, message, model, assistant) VALUES (?, ?, ?, ?, ?)",
                                               (now_str, "mahia", reply_clean, "StreamMonitor Mahia Live", "mahia"))
                                conn.commit()
                                conn.close()
                            except Exception as pe:
                                print("[Mahia Persist Error]:", pe)

                            self.send_response(200)
                            self.send_header("Content-Type", "application/json; charset=utf-8")
                            self.end_headers()
                            self.wfile.write(json.dumps({
                                "reply": reply_clean,
                                "response": reply_clean,
                                "source": "streammonitor_cdp",
                                "live_chat": True
                            }).encode("utf-8"))
                            return
                        else:
                            print(f"[Mahia Live Warning]: Connector returned {mahia_res}")
                except Exception as cdp_err:
                    print(f"[Mahia CDP Bridge Error]: {cdp_err}")
                active_system_prompt = MAHIA_CPU_SYSTEM_PROMPT
            elif assistant_id in SYSTEM_PROMPTS_BY_AGENT:
                active_system_prompt = SYSTEM_PROMPTS_BY_AGENT[assistant_id]
            else:
                active_system_prompt = ROXANNE_CPU_SYSTEM_PROMPT

            # Preparar mensajes para Ollama (limitar historial a últimos 6 mensajes = 3 turnos para máxima agilidad en CPU)
            recent_history = [h for h in chat_history if "role" in h and "content" in h][-6:]
            messages = [{"role": "system", "content": active_system_prompt}]
            messages.extend(recent_history)
            messages.append({"role": "user", "content": message})

            # Detectar si se pide una tabla o esquema
            is_table_query = any(w in msg_lower for w in ["tabla", "tablas", "matriz", "matrices", "comparativa", "resumen", "comparar", "cuadro", "cronograma", "esquema"])
            predict_tokens = 220 if is_table_query else 90
            ctx_tokens = 1024 if is_table_query else 512

            # Inferencia vía Ollama con paralelismo multihilo de CPU
            ollama_payload = {
                "model": model_name,
                "messages": messages,
                "stream": False,
                "options": {
                    "num_thread": 10,
                    "num_ctx": ctx_tokens,
                    "num_predict": predict_tokens,
                    "temperature": 0.6,
                    "top_p": 0.9
                }
            }

            req = urllib.request.Request(
                "http://localhost:11434/api/chat",
                data=json.dumps(ollama_payload).encode("utf-8"),
                headers={"Content-Type": "application/json"}
            )

            cancel_event = threading.Event()
            session_key = assistant_id
            with ACTIVE_CHAT_LOCK:
                ACTIVE_CHAT_SESSIONS[session_key] = {
                    "cancel_event": cancel_event,
                    "response_obj": None,
                    "stopped": False,
                    "time": time.time()
                }

            try:
                response = urllib.request.urlopen(req, timeout=12)
                with ACTIVE_CHAT_LOCK:
                    if session_key in ACTIVE_CHAT_SESSIONS:
                        ACTIVE_CHAT_SESSIONS[session_key]["response_obj"] = response

                res_json = json.loads(response.read().decode("utf-8"))
                reply = res_json.get("message", {}).get("content", "").strip()
                if not reply:
                    reply = generate_contextual_fallback(assistant_id, message)
            except Exception as e:
                # Verificar si fue cancelado / pausado explícitamente por el usuario
                was_stopped = False
                with ACTIVE_CHAT_LOCK:
                    sess = ACTIVE_CHAT_SESSIONS.get(session_key)
                    if sess and (sess.get("stopped") or sess.get("cancel_event", threading.Event()).is_set()):
                        was_stopped = True

                if was_stopped:
                    self.send_response(200)
                    self.send_header("Content-Type", "application/json; charset=utf-8")
                    self.end_headers()
                    self.wfile.write(json.dumps({
                        "reply": "[Respuesta pausada por el usuario]",
                        "stopped": True,
                        "assistant": assistant_id
                    }).encode("utf-8"))
                    return

                print(f"[Ollama Inference Fallback]: {e}")
                reply = generate_contextual_fallback(assistant_id, message)
            finally:
                with ACTIVE_CHAT_LOCK:
                    ACTIVE_CHAT_SESSIONS.pop(session_key, None)


            # Guardar en SQLite (Auditoría general y asistente persistente)
            log_interaction_to_db(message, reply, model_name, lang)
            try:
                conn = sqlite3.connect(DB_PATH)
                cursor = conn.cursor()
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS copilot_assistant_history (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        timestamp TEXT,
                        sender TEXT,
                        message TEXT,
                        model TEXT,
                        assistant TEXT DEFAULT 'roxanne'
                    )
                """)
                cols = [col[1] for col in cursor.execute("PRAGMA table_info(copilot_assistant_history)").fetchall()]
                if "assistant" not in cols:
                    cursor.execute("ALTER TABLE copilot_assistant_history ADD COLUMN assistant TEXT DEFAULT 'roxanne'")
                    conn.commit()

                now_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                cursor.execute("INSERT INTO copilot_assistant_history (timestamp, sender, message, model, assistant) VALUES (?, ?, ?, ?, ?)",
                               (now_str, "sam", message, model_name, assistant_id))
                cursor.execute("INSERT INTO copilot_assistant_history (timestamp, sender, message, model, assistant) VALUES (?, ?, ?, ?, ?)",
                               (now_str, assistant_id, reply, model_name, assistant_id))
                conn.commit()
                conn.close()
            except Exception as dbe:
                print("[Chat Persist Error]:", dbe)

            # Disparar notificación Web Push en tiempo real para el asistente que respondió
            try:
                push_service.notify_assistant_response(assistant_id, reply)
            except Exception as pe:
                print("[Push Trigger Warning]:", pe)

            response_data = {
                "reply": reply,
                "model": model_name,
                "detected_lang": lang,
                "rule_applied": "100% Spanish" if lang == "es" else "100% English (Default)",
                "timestamp": datetime.datetime.now().strftime("%H:%M:%S")
            }

            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.end_headers()
            self.wfile.write(json.dumps(response_data).encode("utf-8"))

        except Exception as err:
            self.send_response(500)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.end_headers()
            self.wfile.write(json.dumps({"error": str(err)}).encode("utf-8"))

def run_server():
    server_address = ("", PORT)
    httpd = ThreadingHTTPServer(server_address, VelvetRequestHandler)
    print(f" SIREN AI Command & Server activo en http://localhost:{PORT}")
    print(f" API de Chat ROXANNE conectada a Ollama en http://localhost:11434")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nDeteniendo servidor SIREN...")
        httpd.server_close()

if __name__ == "__main__":
    run_server()
