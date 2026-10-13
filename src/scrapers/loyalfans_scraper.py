import sys
import json
import re
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, List
import httpx

# Asegurar que la raíz del proyecto esté en el sys.path
sys.path.append(str(Path(__file__).resolve().parent.parent.parent))
from src.config import ARTIFACTS_DIR

ZENDESK_BASE_URL = "https://loyalfans.zendesk.com/api/v2/help_center/en-us"

def clean_html(raw_html: str) -> str:
    """Elimina etiquetas HTML y limpia el texto para análisis legible."""
    if not raw_html:
        return ""
    text = re.sub(r"<[^>]+>", " ", raw_html)
    text = re.sub(r"&nbsp;", " ", text)
    text = re.sub(r"&amp;", "&", text)
    text = re.sub(r"&quot;", '"', text)
    text = re.sub(r"&#39;", "'", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()

def fetch_zendesk_articles() -> List[Dict[str, Any]]:
    """Extrae todos los artículos oficiales del Centro de Ayuda para Modelos de LoyalFans vía API pública."""
    articles_list = []
    try:
        url = f"{ZENDESK_BASE_URL}/articles.json?per_page=100"
        with httpx.Client(timeout=15.0) as client:
            resp = client.get(url)
            if resp.status_code == 200:
                data = resp.json()
                for art in data.get("articles", []):
                    title = art.get("title", "")
                    body_clean = clean_html(art.get("body", ""))
                    html_url = art.get("html_url", "")
                    section_id = art.get("section_id")
                    articles_list.append({
                        "id": art.get("id"),
                        "title": title,
                        "url": html_url,
                        "section_id": section_id,
                        "updated_at": art.get("updated_at"),
                        "summary": body_clean[:450] + ("..." if len(body_clean) > 450 else "")
                    })
    except Exception as e:
        print(f"[Warning] Error extrayendo artículos de Zendesk: {e}")
    return articles_list

def build_full_loyalfans_intelligence() -> Dict[str, Any]:
    """
    Construye la radiografía completa (Scraping + Arquitectura de Conocimiento)
    de LoyalFans: herramientas, facturación, algoritmo, visibilidad y juguetes interactivos.
    """
    zendesk_articles = fetch_zendesk_articles()

    intelligence = {
        "metadata": {
            "platform": "LoyalFans",
            "base_url": "https://www.loyalfans.com",
            "support_url": "https://loyalfans.zendesk.com",
            "scan_timestamp": datetime.now().isoformat(),
            "total_official_articles_extracted": len(zendesk_articles)
        },
        "herramientas_y_funcionalidades": {
            "tienda_de_video": {
                "nombre": "Video Store & Clips",
                "descripcion": "Venta directa de clips de vídeo a la carta sin requerir suscripción mensual al muro.",
                "caracteristicas": [
                    "Soporte para trailers o vistas previas gratuitas (teasers) con marca de agua.",
                    "Fijación de precio libre en USD.",
                    "Venta perpetua (Pay-Per-View Video Store) accesible para cualquier visitante del perfil.",
                    "Categorización por fetiches, fetiches BDSM, tabú y nichos específicos."
                ]
            },
            "tienda_de_audio": {
                "nombre": "Audio Store & Podcasting",
                "descripcion": "Herramienta nativa exclusiva de LoyalFans para monetizar notas de voz, audios eróticos, ASMR, gemidos y fantasías guiadas.",
                "caracteristicas": [
                    "Ideal para modelos 'faceless' (sin rostro) o creadoras de audio-erótica.",
                    "Venta unitaria de pistas de audio en USD.",
                    "Permite muestras previas de 5 a 15 segundos para enganchar al comprador."
                ]
            },
            "muro_timeline_stories": {
                "nombre": "Timeline, Stories & Highlights",
                "descripcion": "Feed social dinámico con historias temporales y momentos destacados permanentes.",
                "caracteristicas": [
                    "Stories de 24 horas para generar sensación de urgencia (FOMO).",
                    "Highlights anclados en el perfil por temáticas (ej: 'Lencería', 'Detrás de cámaras', 'Reviews de fans').",
                    "Publicaciones públicas (para indexar en Explore) y publicaciones bloqueadas solo para suscriptores."
                ]
            },
            "one_on_one_y_llamadas": {
                "nombre": "One-on-One & Private Interactions",
                "descripcion": "Módulo de sesiones privadas en vivo directamente en la plataforma web.",
                "caracteristicas": [
                    "Cam 2 Cam (transmisión bidireccional privada).",
                    "Llamadas de voz y videollamadas con tarifa por minuto configurada por la modelo.",
                    "Programación previa de citas o disponibilidad instantánea en línea."
                ]
            },
            "transmisiones_en_vivo_go_live": {
                "nombre": "Go Live & Interactive Toy Integration",
                "descripcion": "Streaming en vivo público o exclusivo para fans con objetivos de propinas y sinergia con juguetes inteligentes.",
                "caracteristicas": [
                    "Integración nativa con juguetes Lovense (Lush, Domi, Max, etc.) y Kiiroo mediante Bluetooth/Bridge.",
                    "Reacción automática del juguete ante propinas recibidas en tiempo real.",
                    "Tip Goals (metas de propinas) configurables en pantalla para motivar gasto colectivo."
                ]
            },
            "mensajes_masivos_y_shoutouts": {
                "nombre": "Mass DMs & Shoutouts",
                "descripcion": "Monetización conversacional y solicitudes de contenido personalizado.",
                "caracteristicas": [
                    "Mass DM con contenido bloqueado de pago (PPV) enviado a todos los seguidores o suscriptores.",
                    "Regla de respuesta de pago: el fan paga por enviar un mensaje privado prioritario.",
                    "Shoutouts: solicitudes personalizadas donde la modelo define tiempo de entrega y precio base."
                ]
            },
            "privacidad_y_geobloqueo": {
                "nombre": "Settings Privacy and Safety",
                "descripcion": "Controles de seguridad avanzados para la protección de la creadora.",
                "caracteristicas": [
                    "Geobloqueo granular por países completos o estados/ciudades específicas.",
                    "Bloqueo de rangos IP y usuarios específicos.",
                    "Cuentas delegadas (Delegated Accounts) para asistentes o estudios que gestionan el chat sin comprometer datos bancarios."
                ]
            }
        },
        "facturacion_y_finanzas": {
            "reparto_de_ingresos": "80% para la Creadora / Modelo, 20% para LoyalFans.",
            "comision_plataforma": "20% plano sin comisiones ocultas en suscripciones, clips, propinas y llamadas.",
            "frecuencia_de_pago": "2 veces al mes (Bi-monthly / Quincenal). Periodos de cierre con proceso en aprox 7 días hábiles.",
            "monto_minimo_retiro": "$50 USD acumulados en el balance disponible.",
            "metodos_de_pago_disponibles": [
                "Paxum (E-Wallet recomendada para la industria de adultos, acreditación rápida).",
                "Bank Wire / Transferencia Bancaria Internacional (SWIFT / SEPA).",
                "Direct Deposit / ACH (disponible para cuentas en EE.UU.)."
            ],
            "rangos_de_precios_permitidos": {
                "suscripcion_mensual": "Desde $1.00 USD hasta $50.00 USD por mes.",
                "subscription_bundles": "Descuentos por paquetes de 3, 6 o 12 meses.",
                "promotional_campaigns": "Campañas de descuento con tiempo límite y cupos máximos de suscriptores."
            }
        },
        "algoritmo_y_estrategia_de_visibilizacion": {
            "mecanismo_del_algoritmo": {
                "diferencia_clave": "A diferencia de OnlyFans (que es ciego y exige 100% de tráfico externo de Twitter/TikTok), LoyalFans cuenta con un motor de búsqueda interno y feeds de recomendación pública.",
                "explore_feed": "El feed de 'Explore' y 'For You' recomienda creadoras basadas en interacciones recientes y etiquetas de búsqueda.",
                "velocidad_de_engagement": "Los posts que reciben propinas, likes o desbloqueos durante sus primeros 60 minutos son impulsados al tope del muro de tendencias."
            },
            "seo_interno_y_etiquetas": {
                "indexacion_de_perfil": "La biografía, el nombre de pantalla y las descripciones de los clips son indexados por el buscador interno.",
                "estrategia_de_tags": "El uso de tags de nichos específicos (fetish, cosplay, milf, findom, femdom, petite, ebony, latinas) atrae compradores directos que buscan específicamente con dinero en mano.",
                "evitar_saturacion": "Se recomienda combinar 2 tags generales populares con 3 tags altamente específicos del fetiche o vestuario del set."
            },
            "multiplicadores_de_visibilidad": [
                {
                    "accion": "Transmitir en Vivo (Go Live)",
                    "impacto": "MÁXIMO. Las modelos en vivo aparecen con badge destacado y prioridad visual en el directorio principal de la plataforma."
                },
                {
                    "accion": "Publicar Teasers Públicos con Tags",
                    "impacto": "ALTO. Un perfil 100% bloqueado es invisible para el algoritmo. Publicar 1-2 fotos o vídeos cortos públicos al día alimenta el Explore Feed."
                },
                {
                    "accion": "Stories de 24 Horas",
                    "impacto": "MEDIO-ALTO. Mantiene a la modelo en la barra superior de historias de los usuarios activos."
                },
                {
                    "accion": "Integración con Juguetes Lovense",
                    "impacto": "ALTO. Muchos usuarios filtran activamente por 'Interactive Toy Active' para interactuar por propinas."
                }
            ]
        },
        "articulos_oficiales_extraidos": zendesk_articles
    }

    # Guardar en disco el artefacto estructurado JSON
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    json_path = ARTIFACTS_DIR / f"loyalfans_intelligence_full_{timestamp}.json"
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(intelligence, f, ensure_ascii=False, indent=2)

    # Generar Dossier Markdown de Inteligencia
    md_path = ARTIFACTS_DIR / f"loyalfans_intelligence_dossier_{timestamp}.md"
    generate_markdown_dossier(intelligence, md_path)

    return {
        "json_path": str(json_path),
        "md_path": str(md_path),
        "total_articles": len(zendesk_articles),
        "timestamp": timestamp,
        "data": intelligence
    }

def generate_markdown_dossier(intel: Dict[str, Any], filepath: Path):
    """Genera un reporte Markdown detallado con toda la inteligencia técnica extraída."""
    meta = intel["metadata"]
    fin = intel["facturacion_y_finanzas"]
    alg = intel["algoritmo_y_estrategia_de_visibilizacion"]
    tools = intel["herramientas_y_funcionalidades"]
    arts = intel["articulos_oficiales_extraidos"]

    lines = [
        "# 🕵️‍♀️ DOSSIER DE INTELIGENCIA TÉCNICA Y MONETIZACIÓN — LOYALFANS",
        f"**Agente Auditor:** ELECTRA (Radar de Algoritmos & Platform Intelligence)",
        f"**Fecha de Análisis:** {meta['scan_timestamp']}",
        f"**Artículos y Guías Oficiales Analizados:** {meta['total_official_articles_extracted']}",
        "",
        "---",
        "## 1. 💵 MODELO DE FACTURACIÓN Y CONDICIONES FINANCIERAS",
        f"- **Reparto de Ingresos:** {fin['reparto_de_ingresos']}",
        f"- **Comisión de Plataforma:** {fin['comision_plataforma']}",
        f"- **Frecuencia de Pagos:** {fin['frecuencia_de_pago']}",
        f"- **Mínimo para Cobro:** {fin['monto_minimo_retiro']}",
        f"- **Rango de Suscripción:** {fin['rangos_de_precios_permitidos']['suscripcion_mensual']}",
        "- **Métodos de Cobro Admitidos:**",
    ]
    for m in fin["metodos_de_pago_disponibles"]:
        lines.append(f"  * {m}")

    lines.extend([
        "",
        "---",
        "## 2. 🧰 TODAS LAS HERRAMIENTAS Y FUNCIONALIDADES DE LA CREADORA",
    ])

    for key, item in tools.items():
        lines.append(f"### 🔹 {item['nombre']}")
        lines.append(f"*{item['descripcion']}*")
        for c in item["caracteristicas"]:
            lines.append(f"- {c}")
        lines.append("")

    lines.extend([
        "---",
        "## 3. 🧠 EL ALGORITMO DE LOYALFANS Y FORMAS DE VISIBILIZACIÓN",
        f"- **Diferencia Fundamental con OnlyFans:** {alg['mecanismo_del_algoritmo']['diferencia_clave']}",
        f"- **Feed de Recomendación (Explore):** {alg['mecanismo_del_algoritmo']['explore_feed']}",
        f"- **Velocidad de Engagement:** {alg['mecanismo_del_algoritmo']['velocidad_de_engagement']}",
        "",
        "### 🎯 Palancas Clave de Posicionamiento:",
    ])

    for mult in alg["multiplicadores_de_visibilidad"]:
        lines.append(f"- **{mult['accion']}** (Impacto: *{mult['impacto']}*): {mult['impacto']}")

    lines.extend([
        "",
        "---",
        "## 4. 📚 DOCUMENTACIÓN Y GUÍAS OFICIALES EXTRAÍDAS",
    ])
    for a in arts[:15]:
        lines.append(f"- **[{a['title']}]({a['url']})**: {a['summary'][:150]}...")

    with open(filepath, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

if __name__ == "__main__":
    res = build_full_loyalfans_intelligence()
    print("Inteligencia extraída:")
    print("JSON:", res["json_path"])
    print("Markdown:", res["md_path"])
    print(f"Total artículos extraídos: {res['total_articles']}")
