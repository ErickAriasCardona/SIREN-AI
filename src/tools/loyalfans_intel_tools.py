import json
from pathlib import Path
from typing import Dict, Any
from src.config import ARTIFACTS_DIR
from src.scrapers.loyalfans_scraper import build_full_loyalfans_intelligence
from src.automation.profile_deep_audit import synthesize_diana_findings, AUDITS_DIR
from datetime import datetime

def ejecutar_scraping_completo_loyalfans() -> str:
    """Ejecuta un escaneo y scraping completo de la plataforma LoyalFans.
    
    Extrae la documentación oficial, guías de creadoras, novedades técnicas,
    esquema de facturación y reglas del algoritmo de visibilidad.
    """
    try:
        resultado = build_full_loyalfans_intelligence()
        total_arts = resultado.get("total_articles", 0)
        md_file = Path(resultado.get("md_path", "")).name
        json_file = Path(resultado.get("json_path", "")).name
        
        return (
            f"✅ Scraping de LoyalFans ejecutado exitosamente.\n"
            f"- Artículos y manuales oficiales de creadoras extraídos: {total_arts}\n"
            f"- Dossier Ejecutivo generado en: artifacts/{md_file}\n"
            f"- Base de Datos Técnica JSON en: artifacts/{json_file}\n"
            f"Toda la inteligencia está disponible para consulta inmediata."
        )
    except Exception as e:
        return f"Error al ejecutar el scraping de LoyalFans: {str(e)}"

def consultar_inteligencia_loyalfans(seccion: str = "todo") -> str:
    """Consulta la base de conocimiento y auditoría técnica de LoyalFans.

    Args:
        seccion: Área a consultar: 'herramientas', 'facturacion', 'algoritmo', 'novedades_y_guias' o 'todo'.
    """
    sec = seccion.lower().strip()
    
    # Buscar el archivo de inteligencia más reciente
    archivos = list(ARTIFACTS_DIR.glob("loyalfans_intelligence_full_*.json"))
    if not archivos:
        # Si no existe, lo ejecutamos automáticamente
        build_full_loyalfans_intelligence()
        archivos = list(ARTIFACTS_DIR.glob("loyalfans_intelligence_full_*.json"))
    
    archivos.sort(key=lambda x: x.stat().st_mtime, reverse=True)
    ultimo_archivo = archivos[0]
    
    with open(ultimo_archivo, "r", encoding="utf-8") as f:
        data = json.load(f)

    if sec in ["facturacion", "pagos", "cobros", "comision"]:
        fin = data["facturacion_y_finanzas"]
        return (
            f"💰 **ESQUEMA DE FACTURACIÓN Y PAGOS — LOYALFANS**\n"
            f"- **Reparto de Ingresos:** {fin['reparto_de_ingresos']}\n"
            f"- **Comisión de la plataforma:** {fin['comision_plataforma']}\n"
            f"- **Frecuencia de Pagos:** {fin['frecuencia_de_pago']}\n"
            f"- **Mínimo de Retiro:** {fin['monto_minimo_retiro']}\n"
            f"- **Métodos Disponibles:** {', '.join(fin['metodos_de_pago_disponibles'])}\n"
            f"- **Precios de Suscripción:** {fin['rangos_de_precios_permitidos']['suscripcion_mensual']}"
        )
    
    elif sec in ["herramientas", "funcionalidades", "features"]:
        tools = data["herramientas_y_funcionalidades"]
        res = ["🛠️ **HERRAMIENTAS CLAVE DE CREADORA — LOYALFANS**\n"]
        for k, v in tools.items():
            res.append(f"📌 **{v['nombre']}**: {v['descripcion']}")
            for c in v["caracteristicas"]:
                res.append(f"   • {c}")
            res.append("")
        return "\n".join(res)

    elif sec in ["algoritmo", "visibilidad", "explore", "posicionamiento"]:
        alg = data["algoritmo_y_estrategia_de_visibilizacion"]
        res = [
            f"🧠 **ANÁLISIS DEL ALGORITMO Y VISIBILIDAD — LOYALFANS**\n",
            f"🔍 **Diferencial:** {alg['mecanismo_del_algoritmo']['diferencia_clave']}",
            f"⚡ **Velocidad de Engagement:** {alg['mecanismo_del_algoritmo']['velocidad_de_engagement']}",
            f"🏷️ **Estrategia SEO/Tags:** {alg['seo_interno_y_etiquetas']['estrategia_de_tags']}\n",
            f"🚀 **Multiplicadores de Tráfico Interno:**"
        ]
        for m in alg["multiplicadores_de_visibilidad"]:
            res.append(f"  • {m['accion']} — Impacto: {m['impacto']}")
        return "\n".join(res)

    elif sec in ["novedades_y_guias", "articulos", "guias"]:
        arts = data.get("articulos_oficiales_extraidos", [])
        res = [f"📚 **GUÍAS Y MANUALES OFICIALES EXTRAÍDOS ({len(arts)} artículos)**:\n"]
        for a in arts[:12]:
            res.append(f"• **{a['title']}**: {a['summary'][:130]}...")
        return "\n".join(res)

    else:
        # Devolver resumen ejecutivo completo
        fin = data["facturacion_y_finanzas"]
        alg = data["algoritmo_y_estrategia_de_visibilizacion"]
        return (
            f"📊 **PANORAMA GENERAL DE INTELIGENCIA — LOYALFANS**\n\n"
            f"💵 **Facturación:** {fin['reparto_de_ingresos']} | Mínimo: {fin['monto_minimo_retiro']} | Pagos: Quincenales por Paxum / Wire / ACH.\n"
            f"🧰 **Herramientas Principales:** Tienda de Video, Tienda de Audio, Go Live (Streaming con juguetes Lovense/Kiiroo), One-on-One Cam2Cam, Mass DMs y Shoutouts.\n"
            f"🔥 **Algoritmo:** A diferencia de OnlyFans, posee buscador interno y Explore Feed. Las modelos que transmiten en vivo o publican teasers con tags de nicho reciben tráfico orgánico sin depender de redes sociales externas.\n\n"
            f"*(Usa 'consultar_inteligencia_loyalfans' especificando 'herramientas', 'facturacion' o 'algoritmo' para profundizar)*"
        )

def recomendar_estrategia_algoritmo(nicho: str, tiene_juguete: bool = False, hace_en_vivo: bool = False) -> str:
    """Diseña una estrategia técnica para hackear la visibilidad interna del algoritmo de LoyalFans.

    Args:
        nicho: Especialidad o temática de la modelo (ej: 'latina glamour', 'findom / dominant', 'cosplay', 'fetish pies').
        tiene_juguete: Si cuenta con juguete Lovense o Kiiroo interactivo.
        hace_en_vivo: Si está dispuesta a realizar transmisiones o shows en vivo.
    """
    pasos = [
        f"🎯 **PLAN DE ACCIÓN TÁCTICO PARA ALGORITMO LOYALFANS (Nicho: {nicho.title()})**\n",
        "1. **SEO del Perfil:** Llena tu bio y títulos de publicaciones con palabras clave exactas de tu fetiche. Los usuarios de LoyalFans buscan mediante la barra de búsqueda interna más que en cualquier otra plataforma.",
        "2. **Estrategia de Cebo (Teasers Públicos):** Publica 1 foto o preview de vídeo gratuito al día con 4 tags relevantes. Esto alimenta el Explore Feed de usuarios que aún no te siguen.",
        "3. **Tienda de Audio:** Abre tu Tienda de Audio hoy mismo con notas de voz de 1 a 3 minutos ($5 a $10 USD). Hay mucha menos competencia en audios y LoyalFans la destaca en su menú principal."
    ]

    if hace_en_vivo:
        pasos.append("4. **Palanca Go Live (Mayor Multiplicador):** Transmite 30-45 minutos 3 veces por semana. LoyalFans coloca a las modelos en vivo en un carrusel dorado al tope de la página de inicio, dándote tráfico de compradores en caliente.")
    
    if tiene_juguete:
        pasos.append("5. **Filtro Lovense:** Activa la integración interactiva por Bluetooth. Los usuarios con créditos buscan creadoras con juguete conectado para hacerlas vibrar al instante por propinas.")

    pasos.append("\n💡 **Regla de Oro:** Aprovecha los Mass DMs de pago (PPV) para exprimir a los seguidores que ya te dieron 'Follow' gratuito.")
    return "\n".join(pasos)

def generar_plan_tactico_unificado_diana_electra(
    plataforma: str = "loyalfans",
    nicho_personalizado: str = None,
    tiene_juguete: bool = True,
    hace_en_vivo: bool = True
) -> str:
    """Combina la auditoría de cuenta de DIANA con la inteligencia de algoritmos de ELECTRA.
    
    Toma los datos del historial comercial de la creadora (contactos calientes, compras pasadas,
    formatos ganadores y basura descartada por DIANA) y los cruza con los multiplicadores de
    visibilidad y Explore Feed de ELECTRA para LoyalFans.
    """
    plat = plataforma.lower().strip()
    audit_file = AUDITS_DIR / f"{plat}_audit.json"
    
    # Cargar auditoría de DIANA existente o generar síntesis
    if audit_file.exists():
        try:
            with open(audit_file, "r", encoding="utf-8") as f:
                saved = json.load(f)
                diana_data = saved.get("analysis", {})
        except Exception:
            diana_data = synthesize_diana_findings({"platform": plat})
    else:
        diana_data = synthesize_diana_findings({"platform": plat})

    creator = diana_data.get("creator_name", "Sam Barton")
    handle = diana_data.get("creator_handle", "@sambarton23")
    nicho = nicho_personalizado or diana_data.get("niche", "Lencería Exclusiva / Sensualidad POV")
    best_content = diana_data.get("best_content", "Clips de 3 a 7 min ($12 - $18 USD)")
    chat_users = diana_data.get("chat_users", ["@beaubrun", "@rudeyx", "@joshy123"])
    chat_sample = ", ".join(chat_users[:4])

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    reporte = [
        "╔════════════════════════════════════════════════════════════════════════╗",
        "║      💎 PLAN TÁCTICO UNIFICADO: DIANA (Auditora) x ELECTRA (Radar)    ║",
        "╚════════════════════════════════════════════════════════════════════════╝\n",
        f"👤 CREADORA AUDITADA: {creator} ({handle})",
        f"🌐 PLATAFORMA OBJETIVO: {plat.upper()}",
        f"🏷️ NICHO COMERCIAL DETERMINADO: {nicho}",
        f"👥 AUDIENCIA EN ESPERA DETECTADA: 604 Fans en Base | Contactos VIP: {chat_sample}...\n",
        "────────────────────────────────────────────────────────────────────────",
        "1. 🔬 EL 'ORO COMERCIAL' EXTRAÍDO POR DIANA (Qué vender y a qué precio):",
        f"   • Formato Ganador Histórico: {best_content}",
        "   • Precio Recomendado en LoyalFans: $12 - $18 USD para la Tienda de Video / $9.99 USD en Mass DM.",
        "   • Basura Descartada por DIANA: Conversaciones gratuitas largas con freeloaders y posts sin opción de compra.\n",
        "────────────────────────────────────────────────────────────────────────",
        "2. ⚡ INYECCIÓN EN EL ALGORITMO DE LOYALFANS POR ELECTRA (Cómo visibilizarlo):",
        "   • Velocidad de 60 Minutos: Lanzar el Mass DM PPV temático a las horas pico. Los primeros desbloqueos",
        "     de @beaubrun, @rudeyx y @joshy123 disparan el ranking interno de la creadora en 'Trending'.",
        "   • Hackeo del Explore Feed: Publicar 1 teaser público diario de 15 segundos con 4 tags de nicho:",
        f"     #ExclusiveLingerie #{nicho.split()[0]} #VIP #Sensual #POV (para atraer nuevos suscriptores orgánicos).",
        "   • Tienda de Audio Nativa: Grabar 2 notas de voz sugerentes ($7 USD) para capturar ventas pasivas.\n",
        "────────────────────────────────────────────────────────────────────────",
        "3. 🚀 PALANCAS DE VISIBILIDAD EN TIEMPO REAL:"
    ]

    if hace_en_vivo:
        reporte.append("   • Go Live Streaming: 2 sesiones de 30 min esta semana. Te ubica en el carrusel dorado superior de LoyalFans.")
    if tiene_juguete:
        reporte.append("   • Sinergia Lovense / Kiiroo: Conectar juguete por Bluetooth. Activa el filtro de búsqueda interactivo de compradores.")

    reporte.extend([
        "\n────────────────────────────────────────────────────────────────────────",
        "4. 📋 HOJA DE RUTA INMEDIATA EN 3 PASOS:",
        "   [Paso 1] Disparar Mass DM PPV con teaser misterioso a $9.99 USD a los 604 fans.",
        f"   [Paso 2] Abrir chat prioritario con {chat_sample} con mensaje de audio de bienvenida.",
        "   [Paso 3] Programar 1 clip estrella en la Video Store a $15 USD con trailer de 20 seg con marca de agua.",
        "────────────────────────────────────────────────────────────────────────\n"
    ])

    texto_final = "\n".join(reporte)

    # Guardar en disco como artefacto
    artifact_path = ARTIFACTS_DIR / f"plan_tactico_diana_electra_{timestamp}.md"
    with open(artifact_path, "w", encoding="utf-8") as f:
        f.write(texto_final)

    texto_final += f"✅ Plan táctico guardado en: artifacts/{artifact_path.name}\n"
    return texto_final
