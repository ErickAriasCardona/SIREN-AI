import sys
from pathlib import Path
from typing import Dict, Any, List

sys.path.append(str(Path(__file__).resolve().parent.parent.parent.parent))

class StripchatContentManager:
    """Gestor y preparador de álbumes y clips para Stripchat."""
    
    PLATFORM_NAME = "Stripchat"
    BASE_URL = "https://es.stripchat.com"

    @staticmethod
    def format_album_payload(
        title: str,
        description: str,
        media_paths: List[str],
        price_tokens: int = 0,
        is_fan_club_only: bool = False,
        tags: List[str] = None
    ) -> Dict[str, Any]:
        """Prepara el paquete de contenido para un álbum o video en Stripchat."""
        return {
            "platform": "stripchat",
            "title": title,
            "description": description,
            "media_files": media_paths,
            "price_tokens": price_tokens,
            "fan_club_only": is_fan_club_only,
            "tags": tags or []
        }
