import sys
import asyncio
from pathlib import Path
from typing import List, Dict, Any, Optional
from playwright.async_api import async_playwright

# Asegurar que la raíz del proyecto esté en el sys.path
sys.path.append(str(Path(__file__).resolve().parent.parent.parent))

from src.config import STREAMATE_BASE_URL

async def auto_scroll(page, max_loops: int = 25, delay_ms: int = 150):
    """Realiza scroll progresivo para cargar elementos dinámicos por lazy-loading."""
    await page.evaluate("""async ([maxLoops, delayMs]) => {
        let lastHeight = 0;
        let loops = 0;
        await new Promise((resolve) => {
            const timer = setInterval(() => {
                window.scrollBy(0, window.innerHeight);
                const newHeight = document.documentElement.scrollHeight;
                loops++;
                if (newHeight === lastHeight || loops >= maxLoops) {
                    clearInterval(timer);
                    resolve();
                }
                lastHeight = newHeight;
            }, delayMs);
        });
    }""", [max_loops, delay_ms])

async def scrape_streamate_grid(
    pages: int = 1, 
    headless: bool = True,
    timeout_ms: int = 30000
) -> List[Dict[str, Any]]:
    """
    Rastrea las páginas principales de Streamate y devuelve la lista ordenada de modelos.
    
    Retorna una lista de diccionarios con:
    - position: posición absoluta (#1, #2, ...)
    - page: número de página
    - href: URL o path del perfil
    - username: nombre de usuario inferido del href
    """
    results: List[Dict[str, Any]] = []
    current_rank = 1

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=headless)
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
            viewport={"width": 1920, "height": 1080}
        )
        page = await context.new_page()

        for page_num in range(1, pages + 1):
            url = f"{STREAMATE_BASE_URL}/page/{page_num}" if page_num > 1 else STREAMATE_BASE_URL
            try:
                await page.goto(url, wait_until="domcontentloaded", timeout=timeout_ms)
                # Esperar brevemente a que el listado inicial renderice
                try:
                    await page.wait_for_selector('[data-ta-locator="PerformerList"]', timeout=8000)
                except Exception:
                    pass

                await auto_scroll(page)

                # Extraer enlaces de cada modelo
                links = await page.locator('[data-ta-locator="PerformerList"] a').evaluate_all(
                    """elements => elements.map(el => {
                        const href = el.getAttribute('href') || '';
                        const text = el.innerText || '';
                        return { href, text };
                    })"""
                )

                seen_hrefs = set()
                for item in links:
                    href = item.get("href", "").strip()
                    if not href or href in seen_hrefs or href.startswith("javascript:") or href == "#":
                        continue
                    
                    seen_hrefs.add(href)
                    # Extraer el username a partir del href si es posible (ej: /cam/username)
                    clean_username = href.strip("/").split("/")[-1]

                    results.append({
                        "rank": current_rank,
                        "page": page_num,
                        "username": clean_username,
                        "href": href if href.startswith("http") else f"{STREAMATE_BASE_URL}{href}",
                    })
                    current_rank += 1

            except Exception as e:
                print(f"[Radar Error] Error al escanear página {page_num}: {e}")
                continue

        await browser.close()

    return results

if __name__ == "__main__":
    # Prueba rápida
    async def test():
        print("Escaneando primeras 2 páginas con Playwright...")
        models = await scrape_streamate_grid(pages=2, headless=True)
        print(f"Total modelos detectadas: {len(models)}")
        for m in models[:5]:
            print(f"#{m['rank']} (Pág {m['page']}) -> {m['username']} [{m['href']}]")

    asyncio.run(test())
