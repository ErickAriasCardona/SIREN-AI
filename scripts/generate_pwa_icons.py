import os
import sys
from PIL import Image, ImageDraw, ImageFont

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

ICONS_DIR = r"c:\Users\MI PC\Desktop\Sam\VELVET AI\icons"
os.makedirs(ICONS_DIR, exist_ok=True)

def create_siren_icon(size, is_maskable=False):
    # Base canvas
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    bg_color = (30, 36, 50, 255) # #1E2432
    if is_maskable:
        # Full square background for maskable
        draw.rectangle([0, 0, size, size], fill=bg_color)
    else:
        # Rounded squircle for standard icon
        radius = int(size * 0.22)
        draw.rounded_rectangle([0, 0, size, size], radius=radius, fill=bg_color)
    
    # Outer subtle glow/border
    border_color = (139, 83, 255, 180) # #8B53FF
    if not is_maskable:
        draw.rounded_rectangle([2, 2, size - 3, size - 3], radius=int(size * 0.22), outline=border_color, width=max(2, int(size * 0.015)))
    
    # Draw stylized neon 'S' icon inside safe zone
    scale = size / 512.0
    safe_pad = int(size * 0.18) if is_maskable else int(size * 0.12)
    
    # Neon gradient simulation from Purple (#8B53FF) to Neon Green (#1AE589)
    cx, cy = size // 2, size // 2
    
    # Center emblem: Concentric neon curves / cybernetic 'S'
    # Upper loop
    r1 = int(size * 0.22)
    box_upper = [cx - r1, cy - int(r1 * 1.5), cx + r1, cy]
    draw.arc(box_upper, start=180, end=360, fill=(139, 83, 255, 255), width=int(32 * scale))
    
    # Lower loop
    box_lower = [cx - r1, cy, cx + r1, cy + int(r1 * 1.5)]
    draw.arc(box_lower, start=0, end=180, fill=(26, 229, 137, 255), width=int(32 * scale))
    
    # Diagonal connection
    draw.line([cx - int(r1 * 0.7), cy - int(r1 * 0.2), cx + int(r1 * 0.7), cy + int(r1 * 0.2)], fill=(139, 83, 255, 255), width=int(30 * scale))
    
    # Glowing center core
    core_r = int(18 * scale)
    draw.ellipse([cx - core_r, cy - core_r, cx + core_r, cy + core_r], fill=(26, 229, 137, 255))
    
    # Satellite pulse dots
    dot_r = int(10 * scale)
    draw.ellipse([cx + r1 - dot_r, cy - int(r1 * 0.8) - dot_r, cx + r1 + dot_r, cy - int(r1 * 0.8) + dot_r], fill=(26, 229, 137, 255))
    draw.ellipse([cx - r1 - dot_r, cy + int(r1 * 0.8) - dot_r, cx - r1 + dot_r, cy + int(r1 * 0.8) + dot_r], fill=(139, 83, 255, 255))
    
    return img

def create_assistant_avatar_icon(name, initials, color1, color2, size=192):
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # Circular avatar
    draw.ellipse([4, 4, size - 5, size - 5], fill=(30, 36, 50, 255), outline=color1, width=6)
    
    # Inner gradient fill circle
    draw.ellipse([14, 14, size - 15, size - 15], fill=color2)
    
    # Center Initials
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

# Generate PWA standard icons
icon_192 = create_siren_icon(192)
icon_192.save(os.path.join(ICONS_DIR, "icon-192x192.png"))

icon_512 = create_siren_icon(512)
icon_512.save(os.path.join(ICONS_DIR, "icon-512x512.png"))

icon_512_maskable = create_siren_icon(512, is_maskable=True)
icon_512_maskable.save(os.path.join(ICONS_DIR, "icon-512x512-maskable.png"))

badge_72 = create_siren_icon(72)
badge_72.save(os.path.join(ICONS_DIR, "badge-72x72.png"))

# Generate 4 Assistant Icons for Notifications
# 1. Roxanne (Purple)
asst_rox = create_assistant_avatar_icon("Roxanne", "RX", (139, 83, 255, 255), (99, 44, 214, 255))
asst_rox.save(os.path.join(ICONS_DIR, "assistant-roxanne.png"))

# 2. Chloe (Pink/Rose)
asst_chloe = create_assistant_avatar_icon("Chloe", "CH", (244, 63, 94, 255), (190, 24, 93, 255))
asst_chloe.save(os.path.join(ICONS_DIR, "assistant-chloe.png"))

# 3. Diana (Green/Emerald)
asst_diana = create_assistant_avatar_icon("Diana", "DI", (26, 229, 137, 255), (16, 149, 88, 255))
asst_diana.save(os.path.join(ICONS_DIR, "assistant-diana.png"))

# 4. Electra (Cyan/Blue)
asst_electra = create_assistant_avatar_icon("Electra", "EL", (56, 189, 248, 255), (14, 116, 144, 255))
asst_electra.save(os.path.join(ICONS_DIR, "assistant-electra.png"))

print("✓ All PWA and Assistant icons successfully generated in icons/ directory!")
