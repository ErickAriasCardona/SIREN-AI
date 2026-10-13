import sys
from pathlib import Path
from typing import Dict, Any, List

sys.path.append(str(Path(__file__).resolve().parent.parent.parent.parent))

class Flirt4FreeContentManager:
    """Gestor y preparador de sets de fotos y clips para la tienda de Flirt4Free."""
    
    PLATFORM_NAME = "Flirt4Free"
    BASE_URL = "https://www.flirt4free.com"

    @staticmethod
    def format_media_payload(
        title: str,
        description: str,
        media_paths: List[str],
        price_credits: int = 50,
        category: str = "Solo",
        tags: List[str] = None
    ) -> Dict[str, Any]:
        """Prepara el paquete de contenido para la tienda de Flirt4Free."""
        return {
            "platform": "flirt4free",
            "title": title,
            "description": description,
            "media_files": media_paths,
            "price_credits": price_credits,
            "category": category,
            "tags": tags or []
        }
