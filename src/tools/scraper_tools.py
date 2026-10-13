import asyncio
import json
from datetime import datetime
from typing import Dict, Any, List
from src.scrapers.streamate_scraper import scrape_streamate_grid
from src.config import ARTIFACTS_DIR

def consultar_ranking_streamate(paginas: int = 2) -> str:
    """Escanea las primeras páginas de Streamate y devuelve un resumen del Top y total de modelos activas.

    Args:
        paginas: Número de páginas a escanear (por defecto 2).
    """
    try:
        # Correr la función async dentro de un loop
        results = asyncio.run(scrape_streamate_grid(pages=paginas, headless=True))
        if not results:
            return "No se encontraron modelos en la grilla o el sitio requirió verificación humana."

        # Guardar artefacto en disco
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        artifact_path = ARTIFACTS_DIR / f"ranking_scan_{timestamp}.json"
        with open(artifact_path, "w", encoding="utf-8") as f:
            json.dump(results, f, ensure_ascii=False, indent=2)

        top_5 = "\n".join([f"#{m['rank']} (Pág {m['page']}) -> {m['username']}" for m in results[:5]])
        return (
            f"✅ Escaneo completado con éxito.\n"
            f"- Total modelos detectadas: {len(results)}\n"
            f"- Páginas escaneadas: {paginas}\n"
            f"- Registro guardado en: {artifact_path.name}\n\n"
            f"🏆 Top 5 actual:\n{top_5}"
        )
    except Exception as e:
        return f"Error al consultar el ranking: {str(e)}"

def buscar_posicion_modelo(username: str, paginas_max: int = 5) -> str:
    """Busca la posición y página de una modelo específica en la grilla de Streamate.

    Args:
        username: Nombre de usuario o identificador de la modelo en Streamate.
        paginas_max: Máximo de páginas a recorrer (por defecto 5).
    """
    try:
        results = asyncio.run(scrape_streamate_grid(pages=paginas_max, headless=True))
        username_clean = username.lower().strip()

        for m in results:
            if username_clean in m["username"].lower():
                return (
                    f"🎯 ¡Modelo encontrada!\n"
                    f"- Usuario: {m['username']}\n"
                    f"- Posición general: #{m['rank']}\n"
                    f"- Página: {m['page']}\n"
                    f"- Enlace: {m['href']}"
                )

        return (
            f"❌ La modelo '{username}' no fue encontrada en las primeras {paginas_max} páginas "
            f"({len(results)} modelos analizadas). Puede que esté desconectada o en páginas posteriores."
        )
    except Exception as e:
        return f"Error al buscar la posición de la modelo: {str(e)}"
