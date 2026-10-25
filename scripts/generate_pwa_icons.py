import os
import sys
import math
from PIL import Image, ImageDraw, ImageFont

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

ICONS_DIR = r"c:\Users\MI PC\Desktop\Sam\VELVET AI\icons"
os.makedirs(ICONS_DIR, exist_ok=True)

def create_option2_icon(size, is_maskable=False):
    """Genera el icono oficial Opción 2: Cyber Pulse Aegis (Hexagonal Prism)."""
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    bg_color = (30, 36, 50, 255) # #1E2432

    if is_maskable:
        draw.rectangle([0, 0, size, size], fill=bg_color)
    else:
        radius = int(size * 0.22)
        draw.rounded_rectangle([0, 0, size, size], radius=radius, fill=bg_color)
        draw.rounded_rectangle([2, 2, size - 3, size - 3], radius=radius, outline=(139, 83, 255, 180), width=max(2, int(size * 0.015)))

    # Blasón hexagonal biselado
    cx, cy = size // 2, size // 2
    r = size * (0.34 if is_maskable else 0.38)
    
    points = []
    for i in range(6):
        angle = math.radians(60 * i - 30)
        px = cx + r * math.cos(angle)
        py = cy + r * math.sin(angle)
        points.append((px, py))
    
    draw.polygon(points, fill=(139, 83, 255, 30), outline=(139, 83, 255, 255), width=max(3, int(size * 0.02)))
    
    # Borde interno sutil
    r_in = r * 0.88
    points_in = []
    for i in range(6):
        angle = math.radians(60 * i - 30)
        px = cx + r_in * math.cos(angle)
        py = cy + r_in * math.sin(angle)
        points_in.append((px, py))
    draw.polygon(points_in, outline=(26, 229, 137, 100), width=max(1, int(size * 0.008)))
    
    # 3 barras de ecualizador vertical
    w = max(4, int(size * 0.04))
    h_center = r * 0.95
    h_side = r * 0.6
    spacing = r * 0.38
    
    # Barra central verde neón (#1AE589)
    draw.rounded_rectangle([cx - w//2, cy - h_center//2, cx + w//2, cy + h_center//2], radius=w//2, fill=(26, 229, 137, 255))
    # Barras laterales púrpura (#8B53FF)
    draw.rounded_rectangle([cx - spacing - w//2, cy - h_side//2, cx - spacing + w//2, cy + h_side//2], radius=w//2, fill=(139, 83, 255, 255))
    draw.rounded_rectangle([cx + spacing - w//2, cy - h_side//2, cx + spacing + w//2, cy + h_side//2], radius=w//2, fill=(139, 83, 255, 255))

    return img

def create_assistant_avatar_icon(name, initials, color1, color2, size=192):
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    draw.ellipse([4, 4, size - 5, size - 5], fill=(30, 36, 50, 255), outline=color1, width=6)
    draw.ellipse([14, 14, size - 15, size - 15], fill=color2)
    try:
        font = ImageFont.truetype("arial.ttf", int(size * 0.38))
    except Exception:
        font = ImageFont.load_default()
        
    bbox = draw.textbbox((0, 0), initials, font=font)
    tw = bbox[2] - bbox[0]
    th = bbox[3] - bbox[1]
    tx = (size - tw) // 2
    ty = (size - th) // 2 - int(size * 0.05)
    draw.text((tx, ty), initials, fill=(255, 255, 255, 255), font=font)
    return img

def create_option2_pwa_icons():
    """Genera todos los iconos PWA oficiales basados en Opción 2."""
    create_option2_icon(192, False).save(os.path.join(ICONS_DIR, "icon-192x192.png"))
    create_option2_icon(512, False).save(os.path.join(ICONS_DIR, "icon-512x512.png"))
    create_option2_icon(512, True).save(os.path.join(ICONS_DIR, "icon-512x512-maskable.png"))
    create_option2_icon(72, False).save(os.path.join(ICONS_DIR, "badge-72x72.png"))

if __name__ == "__main__":
    create_option2_pwa_icons()
    create_assistant_avatar_icon("Roxanne", "RX", (139, 83, 255, 255), (99, 44, 214, 255)).save(os.path.join(ICONS_DIR, "assistant-roxanne.png"))
    create_assistant_avatar_icon("Chloe", "CH", (244, 63, 94, 255), (190, 24, 93, 255)).save(os.path.join(ICONS_DIR, "assistant-chloe.png"))
    create_assistant_avatar_icon("Diana", "DI", (26, 229, 137, 255), (16, 149, 88, 255)).save(os.path.join(ICONS_DIR, "assistant-diana.png"))
    create_assistant_avatar_icon("Electra", "EL", (56, 189, 248, 255), (14, 116, 144, 255)).save(os.path.join(ICONS_DIR, "assistant-electra.png"))
    print("✓ All Option 2 PWA and Assistant icons successfully generated in icons/ directory!")
