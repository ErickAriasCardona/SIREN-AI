import sys
from pathlib import Path
from typing import Dict, Any, List

sys.path.append(str(Path(__file__).resolve().parent.parent.parent.parent))

class LoyalFansContentManager:
    """Gestor y preparador de publicaciones y venta de contenido para LoyalFans."""
    
    PLATFORM_NAME = "LoyalFans"
    BASE_URL = "https://www.loyalfans.com"

    @staticmethod
    def format_post_payload(
        caption: str,
        media_paths: List[str],
        price_usd: float = 0.0,
        is_ppv: bool = False,
        tags: List[str] = None
    ) -> Dict[str, Any]:
        """Prepara el paquete de contenido para ser publicado en LoyalFans."""
        clean_tags = [t if t.startswith("#") else f"#{t}" for t in (tags or [])]
        final_caption = f"{caption}\n\n{' '.join(clean_tags)}".strip()

        return {
            "platform": "loyalfans",
            "type": "ppv_post" if is_ppv else "subscriber_feed",
            "caption": final_caption,
            "media_files": media_paths,
            "price_usd": price_usd,
            "requires_unlock": price_usd > 0 or is_ppv,
            "tags": clean_tags
        }
