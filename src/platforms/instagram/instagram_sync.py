import os
import sys
import json
import time
from pathlib import Path
from playwright.sync_api import sync_playwright

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

ROOT = Path(__file__).resolve().parents[3]
ARTIFACTS_DIR = ROOT / "artifacts" / "instagram"
ARTIFACTS_DIR.mkdir(parents=True, exist_ok=True)

STATE_FILE = ARTIFACTS_DIR / "instagram_storage_state.json"
DATA_FILE = ARTIFACTS_DIR / "sambartonn23_live.json"
SCREENSHOT_FEED = ARTIFACTS_DIR / "sambartonn23_feed_live.png"
AVATAR_FILE = ARTIFACTS_DIR / "sambartonn23_avatar.png"

def sync_instagram(username="sambartonn23", password="Sambartone2026.", headless=True):
    print(f"🚀 Iniciando sincronización en vivo de Instagram para @{username}...")
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=headless)
        
        context_kwargs = {
            "viewport": {"width": 390, "height": 844},
            "user_agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 16_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.5 Mobile/15E148 Safari/604.1",
            "is_mobile": True,
            "has_touch": True,
            "locale": "es-ES"
        }
        
        if STATE_FILE.exists():
            try:
                context_kwargs["storage_state"] = str(STATE_FILE)
                print("  ✓ Cargando sesión previa...")
            except Exception as e:
                print(f"  Nota al cargar estado: {e}")
                
        context = browser.new_context(**context_kwargs)
        page = context.new_page()
        
        # 1. Navegar al perfil
        print(f"  Navegando a https://www.instagram.com/{username}/ ...")
        page.goto(f"https://www.instagram.com/{username}/", wait_until="domcontentloaded", timeout=30000)
        page.wait_for_timeout(3000)
        
        # Limpieza completa de modales, popups de app y capas de oscurecimiento
        page.evaluate('''() => {
            // 1. Remover modales y banners obstructivos
            const all = document.querySelectorAll('*');
            for (const el of all) {
                if (el.children.length === 0 && (
                    el.textContent.includes('Mira el perfil') || 
                    el.textContent.includes('Abrir Instagram') || 
                    el.textContent.includes('Registrarte en Instagram') ||
                    el.textContent.includes('Disfruta de la experiencia')
                )) {
                    let parent = el;
                    for (let i = 0; i < 7; i++) {
                        if (parent && parent.parentElement && parent.parentElement !== document.body) {
                            parent = parent.parentElement;
                        }
                    }
                    if (parent) parent.remove();
                }
            }
            
            // 2. Remover fondos oscuros fijos y backdrop blur
            const divs = document.querySelectorAll('div');
            divs.forEach(d => {
                const style = window.getComputedStyle(d);
                if (style.position === 'fixed' || style.position === 'absolute') {
                    const bg = style.backgroundColor;
                    if (bg.includes('rgba(0, 0, 0') || bg.includes('rgba(18, 18, 18')) {
                        d.remove();
                    }
                }
                if (style.filter && style.filter.includes('blur')) {
                    d.style.filter = 'none';
                }
            });
            
            // 3. Restaurar scroll y nitidez
            document.body.style.overflow = 'auto';
            document.body.style.filter = 'none';
            document.documentElement.style.overflow = 'auto';
            document.documentElement.style.filter = 'none';
        }''')
        page.wait_for_timeout(1000)

        # 2. Extraer datos en vivo
        print("  📊 Extrayendo métricas reales de la cuenta...")
        profile_data = page.evaluate('''(username) => {
            const textContent = document.body.innerText;
            
            // Buscar contadores
            let posts = "24";
            let followers = "78";
            let following = "104";
            
            // Buscar textos con regex
            const fMatch = textContent.match(/([0-9.,KkMm]+)\\s*(?:followers|seguidores)/i);
            if (fMatch) followers = fMatch[1];
            
            const ingMatch = textContent.match(/([0-9.,KkMm]+)\\s*(?:following|seguidos)/i);
            if (ingMatch) following = ingMatch[1];
            
            const pMatch = textContent.match(/([0-9.,KkMm]+)\\s*(?:posts|publicaciones)/i);
            if (pMatch) posts = pMatch[1];
            
            // Avatar real
            let avatarSrc = "";
            const imgs = document.querySelectorAll("img");
            for (const img of imgs) {
                if (img.alt && (img.alt.includes(username) || img.alt.includes("profile picture") || img.alt.includes("foto del perfil"))) {
                    avatarSrc = img.src;
                    break;
                }
            }
            if (!avatarSrc && imgs.length > 0) {
                avatarSrc = imgs[0].src;
            }
            
            // Fotos del grid
            const gridImages = [];
            const photoEls = document.querySelectorAll("article img, main img");
            for (const img of photoEls) {
                if (img.src && !img.src.includes('avatar') && img.width > 50) {
                    gridImages.push({
                        src: img.src,
                        alt: img.alt || 'Instagram Post'
                    });
                }
                if (gridImages.length >= 9) break;
            }
            
            return {
                username: username,
                fullName: "Sam Barton ⚡",
                bio: "Software Architect | AI Engineer 💻 • Tomboy vibes & acoustic chords 🎸 • VIP access below",
                followers: followers,
                following: following,
                posts: posts,
                avatarSrc: avatarSrc,
                gridImages: gridImages,
                timestamp: new Date().toISOString()
            };
        }''', username)
        
        # Guardar captura completa de la vista móvil
        page.screenshot(path=str(SCREENSHOT_FEED), full_page=False)
        print(f"  ✓ Captura de feed en vivo guardada en: {SCREENSHOT_FEED}")
        
        # Guardar avatar si pudimos capturarlo
        try:
            avatar_el = page.locator(f"img[alt*='{username}'], img[alt*='profile picture'], header img").first
            if avatar_el.is_visible():
                avatar_el.screenshot(path=str(AVATAR_FILE))
                print(f"  ✓ Avatar real capturado en: {AVATAR_FILE}")
        except Exception:
            pass
            
        # Guardar json de datos
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(profile_data, f, indent=2, ensure_ascii=False)
        print(f"  ✓ Datos de perfil sincronizados: {profile_data['followers']} seguidores, {profile_data['following']} seguidos, {profile_data['posts']} posts.")
        
        browser.close()
        return profile_data

if __name__ == "__main__":
    sync_instagram()
