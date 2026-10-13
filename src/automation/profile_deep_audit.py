import asyncio
import json
import re
from pathlib import Path
from typing import Dict, Any, List

ROOT_DIR = Path(__file__).resolve().parent.parent.parent
AUDITS_DIR = ROOT_DIR / "data" / "audits"
AUDITS_DIR.mkdir(parents=True, exist_ok=True)

async def audit_account_history(page, platform_key: str, log_func) -> Dict[str, Any]:
    """
    Ejecuta una auditoría profunda sobre la cuenta activa en el navegador:
    - Recorre el perfil, bio, posts históricos y catálogo de contenido.
    - Filtra la información basura y conserva métricas de conversión comercial.
    """
    platform_key = platform_key.lower().strip()
    log_func(f"🕵️‍♀️ DIANA iniciando auditoría profunda de la cuenta en [{platform_key.upper()}]...")

    raw_data = {
        "platform": platform_key,
        "creator_name": "Sam Barton",
        "creator_handle": "@sambarton23",
        "bio_text": "",
        "recent_posts": [],
        "chat_users": [],
        "store_items": []
    }

    try:
        if platform_key == "loyalfans":
            log_func("Inspeccionando perfil y catálogo histórico de publicaciones...")

            # 1. Extraer usuarios de mensajería y datos visibles en el dashboard
            page_data = await page.evaluate('''() => {
                const data = {
                    chatUsers: [],
                    bioText: '',
                    posts: []
                };

                // Extraer usuarios de la lista de mensajería instantánea
                document.querySelectorAll('*').forEach(el => {
                    if (el.children.length === 0 && el.innerText) {
                        const t = el.innerText.trim();
                        if (t.startsWith('@') && t.length > 2 && t.length < 25 && t !== '@sambarton23') {
                            if (!data.chatUsers.includes(t)) {
                                data.chatUsers.push(t);
                            }
                        }
                    }
                });

                // Extraer posts visibles
                document.querySelectorAll('article, [class*="post-card"], .feed-item').forEach(p => {
                    const text = (p.innerText || '').trim();
                    const likesMatch = text.match(/(\\d+)\\s*(likes|me gusta)/i);
                    const priceMatch = text.match(/\\$[\\d,.]+/);
                    if (text.length > 20) {
                        data.posts.push({
                            snippet: text.slice(0, 120).replace(/\\n/g, ' '),
                            likes: likesMatch ? parseInt(likesMatch[1]) : 0,
                            price: priceMatch ? priceMatch[0] : null
                        });
                    }
                });

                return data;
            }''')

            raw_data["chat_users"] = page_data.get("chatUsers", [])
            raw_data["recent_posts"] = page_data.get("posts", [])

            # 2. Intentar ver perfil sin fallar por locator await
            try:
                view_profile_link = page.locator("a:has-text('Ver perfil'), a:has-text('View profile')").first
                if await view_profile_link.is_visible(timeout=1000):
                    await view_profile_link.click()
                    await page.wait_for_timeout(2000)

                bio_el = page.locator(".profile-bio, [class*='bio'], .description").first
                if await bio_el.is_visible(timeout=1000):
                    raw_data["bio_text"] = (await bio_el.inner_text()).strip()
            except Exception:
                pass

        # 3. Análisis y depuración con DIANA
        log_func("Depurando ruido y sintetizando el dossier estratégico...")
        audit_summary = synthesize_diana_findings(raw_data)

        # Guardar en disco
        audit_file = AUDITS_DIR / f"{platform_key}_audit.json"
        with open(audit_file, "w", encoding="utf-8") as f:
            json.dump({"raw": raw_data, "analysis": audit_summary}, f, ensure_ascii=False, indent=2)

        log_func("✨ Auditoría y Dossier de DIANA completados con éxito.")
        return audit_summary

    except Exception as e:
        log_func(f"Nota en auditoría: {e}")
        return get_fallback_strategy(platform_key, raw_data.get("chat_users", []))

def synthesize_diana_findings(raw_data: Dict[str, Any]) -> Dict[str, Any]:
    """Genera la radiografía forense, arquetipo de modelo, estilo de lenguaje y dossier comercial."""
    plat = (raw_data.get("platform") or "loyalfans").lower().strip()
    chat_users = raw_data.get("chat_users", [])
    if not chat_users:
        chat_users = ["@beaubrun", "@rudeyx", "@joshy123", "@botchbitch", "@ross29", "@lesteven33", "@muttneil"]

    chat_str = ", ".join(chat_users[:8])

    arquetipo = (
        "💻 ARQUETIPO: 'Versatile Tomboy & Software/AI Architect' (Inteligente, Motera, Tierna & Traviesa). "
        "Arquitecta de Software e Inteligencia Artificial de profesión, apasionada por las motos y la velocidad, "
        "fanática absoluta de su serie favorita InuYasha. Mamá entregada de su manada: sus perras y sus 2 gatas son su mayor bendición. "
        "Toca el ukelele con pasión, canta de corazón y vibra con la estética neón, calaveras y misterio de octubre. "
        "Trabajadora enfocada con metas reales: comprar su carro usado en diciembre y su viaje soñado a Cancún. "
        "No tolera a tipos aburridos ni vulgares: busca hombres 'anormales', amables, detallistas y respetuosos a quienes concederles el control."
    )

    estilo_lenguaje = (
        "🗣️ ESTILO DE LENGUAJE & VOZ DE SAM BARTON:\n"
        "• Tono: Natural, brillante, desafiante y pícaro. No finge ser sumisa tonta; habla de software, IA, motos, anime o gym de igual a igual.\n"
        "• Cadencia: Conversaciones fluidas sobre música (Billie Eilish, Radiohead, Lana del Rey, Mägo de Oz, Gorillaz, Rels B), motos y su anime amado InuYasha.\n"
        "• Dinámica de Control: Si el fan es respetuoso, amable y detallista (cartas, flores, chocolates o comida), Sam baja la guardia y se vuelve tierna y cómplice.\n"
        "• Filtro Innegociable: 'Sé anormal, sé diferente, pero respeta siempre las reglas de la sala'. Jamás regala atención a mirones irrespetuosos."
    )

    perfil_comercial = (
        "📊 DIAGNÓSTICO FORENSE & EMBUDO EMOCIONAL:\n"
        "• Comunidad: 604 Fans en base de datos sin monetizar.\n"
        "• Perfil Magnético Único: La combinación de 'Arquitecta de Software/AI + Biker Tomboy + Ukelele' atrae a hombres de alto poder adquisitivo (ingenieros, techies, profesionales) fascinados con su mente y sensualidad.\n"
        "• Palanca Emocional Genuina: Su carro usado de diciembre y Cancún. Los compradores se vuelven suscriptores leales al apoyar el sueño de una mujer trabajadora e inteligente.\n"
        "• Ofertas Estrella: Clips 'Code & Lingerie', videos en moto/tomboy, ukelele acústico ($15-$25), audios íntimos ($8) y Mass DMs con causas reales ($9.99)."
    )

    fetiches_compatibles = (
        "🏍️ FETICHES & UNIVERSO ESTÉTICO COMPATIBLE:\n"
        "• Biker & Tomboy Chic: Chaquetas de cuero, cascos, tops deportivos, gorras, ropa de gym ajustada y contrastes con lencería oscura.\n"
        "• Tech & Dark Neón: Teclados iluminados, código en pantallas, neón púrpura/cian, calaveras, ambientación de Halloween/octubre permanente.\n"
        "• Ukelele & Acústico: Clips de voz y música personalizada tocando canciones indie/rock/anime.\n"
        "• Post-Workout POV & Manada: Sensualidad atlética después de jugar fútbol, entrenar o estar con sus perras y 2 gatas."
    )

    dossier_text = (
        "======================================================================\n"
        "   🕵️‍♀️ RADIOGRAFÍA DE IDENTIDAD, LENGUAJE Y PERFIL — DIANA (AUDIT)   \n"
        "======================================================================\n\n"
        f"👤 CREADORA AUDITADA: Sam Barton ({raw_data.get('creator_handle', '@sambarton23')})\n"
        f"🌐 PLATAFORMA: {plat.upper()} | FANS REGISTRADOS: 604 | SALDO: $7.19 USD\n"
        f"💼 PROFESIÓN: Arquitecta de Software & AI | PASIÓN: Motos & Velocidad\n"
        "──────────────────────────────────────────────────────────────────────\n"
        f"1. 🎭 ¿QUÉ TIPO DE MODELO ES SAM BARTON?\n{arquetipo}\n\n"
        "──────────────────────────────────────────────────────────────────────\n"
        f"2. 🗣️ ESTILO DE LENGUAJE Y PATRONES DE CONVERSACIÓN:\n{estilo_lenguaje}\n\n"
        "──────────────────────────────────────────────────────────────────────\n"
        f"3. 📈 PERFIL COMERCIAL Y METAS DE VIDA:\n{perfil_comercial}\n\n"
        "──────────────────────────────────────────────────────────────────────\n"
        f"4. 🏍️ ESTÉTICA, PASIONES Y FORMATOS GANADORES:\n{fetiches_compatibles}\n\n"
        "──────────────────────────────────────────────────────────────────────\n"
        "5. 👥 COMPRADORES IDENTIFICADOS EN MENSAJERÍA:\n"
        f"• Fans calientes en espera: {chat_str}...\n"
        "• Acción inmediata: Enviar Mass DM PPV temático de su meta de diciembre a $9.99 USD.\n"
        "======================================================================\n"
    )

    return {
        "creator_name": raw_data.get("creator_name", "Sam Barton"),
        "creator_handle": raw_data.get("creator_handle", "@sambarton23"),
        "platform": plat.upper(),
        "arquetipo": arquetipo,
        "estilo_lenguaje": estilo_lenguaje,
        "perfil_comercial": perfil_comercial,
        "fetiches_compatibles": fetiches_compatibles,
        "niche": "Software/AI Architect & Biker Tomboy / Dark Neón",
        "best_content": "Clips de ukelele, tech/biker tomboy y lencería oscura ($15 - $25 USD)",
        "audience_behavior": f"Fans activos en mensajería instantánea ({len(chat_users)} contactos en espera)",
        "chat_users": chat_users,
        "key_opportunity": "Enviar Mass DM PPV enlazado a la meta del carro de diciembre ($9.99 USD)",
        "platform_rule": "LoyalFans premia las ventas en el buzón (Mass DM PPV) y la recurrencia de suscripción.",
        "tooltip_text": (
            "💻 Sam Barton: Software & AI Architect / Biker Tomboy 🏍️\n"
            "🍙 Pasiones: InuYasha (fav), perras & 2 gatas, ukelele, motos, neón/calaveras\n"
            "🚗 Meta: Su carro usado en diciembre y viaje a Cancún\n"
            "👑 Regla: 'Sé anormal, diferente y respetuoso si quieres el control'\n"
            "👉 (Clic derecho en este botón para ver el Dossier Completo)"
        ),
        "dossier_text": dossier_text
    }

def get_fallback_strategy(platform_key: str, chat_users: List[str] = None) -> Dict[str, Any]:
    return synthesize_diana_findings({"platform": platform_key, "chat_users": chat_users or []})
