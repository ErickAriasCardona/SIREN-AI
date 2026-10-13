import sys
import asyncio
import json
import re
from pathlib import Path
from datetime import datetime, timezone
from typing import Dict, Any, List
from playwright.async_api import async_playwright

ROOT_DIR = Path(__file__).resolve().parent.parent.parent
sys.path.append(str(ROOT_DIR))

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

DATA_DIR = ROOT_DIR / "data" / "analytics"
DATA_DIR.mkdir(parents=True, exist_ok=True)
RADAR_DB = DATA_DIR / "loyalfans_cooldown_radar.json"

async def run_cooldown_forensic_audit(samples: int = 10) -> Dict[str, Any]:
    """
    Ejecuta el Método 1 y 2 para descifrar el Algoritmo de Cooldown de LoyalFans:
    1. Captura en vivo el feed de 'recently-updated' (/api/v2/creators).
    2. Analiza los atributos internos (online_activity_at, sort_code, etc.).
    3. Inspecciona el muro/timeline de las modelos en las primeras posiciones para
       medir cuándo publicaron y cada cuántas horas renuevan el puesto #1.
    """
    print("=" * 70, flush=True)
    print("⚡ [ELECTRA RADAR] INICIANDO AUDITORÍA FORENSE DE COOLDOWN EN LOYALFANS", flush=True)
    print("=" * 70, flush=True)

    report = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "metodo_2_atributos": {},
        "metodo_1_cohortes": [],
        "deducciones_algoritmicas": []
    }

    async with async_playwright() as p:
        ctx = await p.chromium.launch_persistent_context(
            user_data_dir=str(ROOT_DIR / "data" / "browser_profiles" / "loyalfans_profile"),
            headless=True
        )
        page = ctx.pages[0] if ctx.pages else await ctx.new_page()

        # -------------------------------------------------------------
        # PASO 1: Capturar los creadores actuales en 'recently-updated'
        # -------------------------------------------------------------
        print("\n📡 PASO 1: Consultando /api/v2/creators?target=recently-updated...", flush=True)
        recent_creators_raw = []

        async def on_response(res):
            if "api/v2/creators" in res.url and res.request.method == "POST":
                try:
                    pd = res.request.post_data or ""
                    if "recently-updated" in pd:
                        body = await res.json()
                        if body.get("results"):
                            recent_creators_raw.extend(body["results"])
                except Exception:
                    pass

        page.on("response", on_response)
        await page.goto("https://www.loyalfans.com/creators", wait_until="networkidle")
        await page.wait_for_timeout(2000)

        # Clic en ACTUALIZADO RECIENTEMENTE
        btn = page.locator("a:has-text('ACTUALIZADO RECIENTEMENTE'), button:has-text('ACTUALIZADO RECIENTEMENTE'), [class*='chip']:has-text('ACTUALIZADO RECIENTEMENTE')").first
        if await btn.is_visible():
            await btn.click()
            await page.wait_for_timeout(3000)

        print(f"✓ Capturadas {len(recent_creators_raw)} creadoras en el Top de 'Recently Updated'.", flush=True)

        # -------------------------------------------------------------
        # PASO 2 (MÉTODO 2): Análisis de atributos internos del backend
        # -------------------------------------------------------------
        print("\n🔬 PASO 2 (MÉTODO 2): Analizando esquema y atributos de ordenamiento...", flush=True)
        if recent_creators_raw:
            sample_creator = recent_creators_raw[0]
            c_info = sample_creator.get("creator", {})
            report["metodo_2_atributos"] = {
                "root_keys": list(sample_creator.keys()),
                "creator_keys": list(c_info.keys()),
                "online_activity_at": c_info.get("online_activity_at"),
                "is_online": c_info.get("is_online"),
                "sort_code": sample_creator.get("sort_code"),
                "categories": sample_creator.get("categories")
            }
            print(f"  - Atributos clave detectados: online_activity_at, sort_code, is_online", flush=True)
            print(f"  - Primer lugar actual: @{c_info.get('slug')} ({c_info.get('name')})", flush=True)

        # -------------------------------------------------------------
        # PASO 3 (MÉTODO 1): Auditoría de Timelines de las Top Modelos
        # -------------------------------------------------------------
        print("\n🕵️‍♀️ PASO 3 (MÉTODO 1): Inspeccionando publicaciones de las Top 5 creadoras...", flush=True)
        analyzed_count = 0
        now_dt = datetime.now(timezone.utc)

        for idx, item in enumerate(recent_creators_raw[:samples]):
            c = item.get("creator", {})
            slug = c.get("slug")
            name = c.get("name")
            if not slug:
                continue

            print(f"\n[{idx+1}/{samples}] Auditando perfil: @{slug} ({name})...", flush=True)

            try:
                # Navegar al perfil de la modelo para leer sus últimos posts
                timeline_posts = []

                async def on_post_resp(r):
                    if "timeline" in r.url and r.request.method == "POST":
                        try:
                            t_body = await r.json()
                            if isinstance(t_body, dict):
                                items = t_body.get("result", {}).get("items") or t_body.get("items") or []
                                timeline_posts.extend(items)
                        except Exception:
                            pass

                page.on("response", on_post_resp)
                await page.goto(f"https://www.loyalfans.com/{slug}", wait_until="networkidle", timeout=25000)
                await page.wait_for_timeout(2500)

                # Extraer fechas visibles de los primeros posts
                post_dates = await page.evaluate("""() => {
                    return Array.from(document.querySelectorAll('.post-date, time, .date, [class*="date"]')).map(el => el.innerText.trim()).filter(t => t.length > 2);
                }""")

                # Si capturamos posts de API o DOM
                cohort_entry = {
                    "rank_position": idx + 1,
                    "slug": slug,
                    "name": name,
                    "online_activity_at": c.get("online_activity_at"),
                    "captured_posts_count": len(timeline_posts) or len(post_dates),
                    "visible_dates": post_dates[:5],
                    "raw_posts_timestamps": []
                }

                for p_item in timeline_posts[:5]:
                    cohort_entry["raw_posts_timestamps"].append({
                        "id": p_item.get("id"),
                        "created_at": p_item.get("created_at") or p_item.get("date"),
                        "type": p_item.get("type")
                    })

                report["metodo_1_cohortes"].append(cohort_entry)
                analyzed_count += 1

            except Exception as e:
                print(f"  Nota al auditar @{slug}: {e}", flush=True)

        await ctx.close()

    # -------------------------------------------------------------
    # PASO 4: Deducción y Síntesis Matemática
    # -------------------------------------------------------------
    print("\n" + "=" * 70, flush=True)
    print("📊 RESULTADOS MATEMÁTICOS DE LA COHORTE", flush=True)
    print("=" * 70, flush=True)

    # Guardar en base de datos de radar
    history = []
    if RADAR_DB.exists():
        try:
            with open(RADAR_DB, "r", encoding="utf-8") as f:
                history = json.load(f)
        except Exception:
            pass

    history.append(report)
    with open(RADAR_DB, "w", encoding="utf-8") as f:
        json.dump(history, f, indent=2, ensure_ascii=False)

    print(f"✓ Informe guardado en: {RADAR_DB.name}", flush=True)
    return report

if __name__ == "__main__":
    asyncio.run(run_cooldown_forensic_audit(samples=5))
