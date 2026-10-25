import re
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

def purify_palette():
    with open('index.html', 'r', encoding='utf-8') as f:
        content = f.read()

    # Exact structured replacements
    replacements = [
        # Root & theme variables
        ('--warning: #fbbf24;', '--warning: #8B53FF;'),
        ("warning: '#FBBF24',", "warning: '#8B53FF',"),
        ("info: '#38BDF8'", "info: '#1AE589'"),
        ("info: '#38BDF8',", "info: '#1AE589',"),

        # Light theme chat
        ('background: #f0f9ff;\n      border-color: #bae6fd;\n      color: #0369a1;', 'background: #f8fafc;\n      border-color: rgba(30, 36, 50, 0.12);\n      color: #1E2432;'),

        # Radial gradients
        ('radial-gradient(circle at 85% 15%, rgba(6, 182, 212, 0.15) 0%,', 'radial-gradient(circle at 85% 15%, rgba(139, 83, 255, 0.15) 0%,'),
        ('radial-gradient(circle at 85% 15%, rgba(6, 182, 212, 0.08) 0%,', 'radial-gradient(circle at 85% 15%, rgba(139, 83, 255, 0.08) 0%,'),
        ('linear-gradient(135deg, #c084fc 0%, #38bdf8 100%)', 'linear-gradient(135deg, #8B53FF 0%, #1AE589 100%)'),
        ('linear-gradient(135deg, #a855f7, #06b6d4)', 'linear-gradient(135deg, #8B53FF, #1AE589)'),
        ('linear-gradient(135deg, #9333ea, #06b6d4)', 'linear-gradient(135deg, #8B53FF, #1AE589)'),
        ('linear-gradient(135deg, #06b6d4, #3b82f6)', 'linear-gradient(135deg, #8B53FF, #1AE589)'),
        ('linear-gradient(135deg, #f59e0b, #06b6d4)', 'linear-gradient(135deg, #8B53FF, #1E2432)'),
        ('linear-gradient(135deg, #f09433, #e6683c, #dc2743, #cc2366, #bc1888)', 'linear-gradient(135deg, #8B53FF, #1AE589)'),
        ('linear-gradient(90deg, #9333ea, #38bdf8)', 'linear-gradient(90deg, #8B53FF, #1AE589)'),

        # Badges and tags
        ('.badge-warning { background: rgba(245, 158, 11, 0.15); color: #fbbf24; border: 1px solid rgba(245, 158, 11, 0.3); }', '.badge-warning { background: rgba(139, 83, 255, 0.15); color: #8B53FF; border: 1px solid rgba(139, 83, 255, 0.3); }'),
        ('.badge-info { background: rgba(6, 182, 212, 0.15); color: #38bdf8; border: 1px solid rgba(6, 182, 212, 0.3); }', '.badge-info { background: rgba(26, 229, 139, 0.15); color: #1AE589; border: 1px solid rgba(26, 229, 139, 0.3); }'),
        ('.tag-streamate { background: rgba(245, 158, 11, 0.2); color: #fbbf24; border: 1px solid rgba(245, 158, 11, 0.4); }', '.tag-streamate { background: rgba(139, 83, 255, 0.15); color: #8B53FF; border: 1px solid rgba(139, 83, 255, 0.35); }'),
        ('.tag-flirt4free { background: rgba(6, 182, 212, 0.2); color: #38bdf8; border: 1px solid rgba(6, 182, 212, 0.4); }', '.tag-flirt4free { background: rgba(26, 229, 139, 0.15); color: #1AE589; border: 1px solid rgba(26, 229, 139, 0.35); }'),

        # Spec dividers
        ('color: #fbbf24;\n      margin: 10px 0 6px 0;', 'color: var(--primary-light);\n      margin: 10px 0 6px 0;'),
        ('color: #b45309;', 'color: var(--primary);'),

        # User chat bubble & Sam avatar
        ('background: rgba(59, 130, 246, 0.15); border: 1px solid rgba(59, 130, 246, 0.3);', 'background: rgba(139, 83, 255, 0.12); border: 1px solid rgba(139, 83, 255, 0.3); color: var(--text-main);'),

        # Sidebar navigation "3 Pendientes" badge
        ('style="background: rgba(245, 158, 11, 0.2); color: #fbbf24;"', 'style="background: rgba(139, 83, 255, 0.18); color: #8B53FF;"'),

        # Streamate badges and borders
        ('background: rgba(245, 158, 11, 0.15); color: #fbbf24; border: 1px solid rgba(245, 158, 11, 0.4);', 'background: rgba(139, 83, 255, 0.15); color: #8B53FF; border: 1px solid rgba(139, 83, 255, 0.35);'),
        ('border-left: 3px solid #fbbf24;', 'border-left: 3px solid #8B53FF;'),
        ('border-left: 3px solid #f59e0b;', 'border-left: 3px solid #8B53FF;'),
        ('border-left: 3px solid #06b6d4;', 'border-left: 3px solid #1AE589;'),
        ('border-left: 3px solid #38bdf8;', 'border-left: 3px solid #1AE589;'),
        ('border-top: 3px solid #f59e0b;', 'border-top: 3px solid #8B53FF;'),
        ('border-top: 3px solid #06b6d4;', 'border-top: 3px solid #1AE589;'),

        # Chloe right panel buttons & colors
        ('border-color: rgba(240, 148, 51, 0.35); background: rgba(240, 148, 51, 0.04);', 'border-color: rgba(139, 83, 255, 0.35); background: rgba(139, 83, 255, 0.04);'),
        ('color: #f97316;', 'color: #8B53FF;'),
        ('background: rgba(240, 148, 51, 0.2); color: #f97316;', 'background: rgba(139, 83, 255, 0.15); color: #8B53FF;'),
        ('border-color: rgba(240, 148, 51, 0.5); color: #fb923c;', 'border-color: rgba(139, 83, 255, 0.4); color: #8B53FF;'),
        ('border-color: rgba(220, 39, 67, 0.5); color: #f43f5e;', 'border-color: rgba(139, 83, 255, 0.4); color: #8B53FF;'),
        ('border-color: rgba(56, 189, 248, 0.5); color: #38bdf8;', 'border-color: rgba(26, 229, 139, 0.4); color: #1AE589;'),

        # Chloe assistant card in deck
        ('background: rgba(240, 148, 51, 0.2); color: #f97316;', 'background: rgba(139, 83, 255, 0.15); color: #8B53FF;'),
        ('background: rgba(220, 39, 67, 0.15); color: #fb7185;', 'background: rgba(139, 83, 255, 0.15); color: #8B53FF;'),
        ('background: rgba(6, 182, 212, 0.15); color: #38bdf8;', 'background: rgba(139, 83, 255, 0.15); color: #8B53FF;'),

        # Streamate warning box
        ('background: rgba(245, 158, 11, 0.08); border: 1px solid rgba(245, 158, 11, 0.3);', 'background: rgba(139, 83, 255, 0.08); border: 1px solid rgba(139, 83, 255, 0.25);'),
        ('background:#fbbf24; box-shadow:0 0 10px #fbbf24;', 'background:#8B53FF; box-shadow:0 0 10px #8B53FF;'),
        ('color:#fbbf24;', 'color:#8B53FF;'),
        ('color: #fbbf24;', 'color: #8B53FF;'),
        ('color:#f59e0b;', 'color:#8B53FF;'),
        ('color: #f59e0b;', 'color: #8B53FF;'),
        ('color:#06b6d4;', 'color:#1AE589;'),
        ('color: #06b6d4;', 'color: #1AE589;'),
        ('color:#38bdf8;', 'color:#1AE589;'),
        ('color: #38bdf8;', 'color: #1AE589;'),
        ('color: #0ea5e9;', 'color: #1AE589;'),
        ('color: #2563eb;', 'color: #8B53FF;'),
        ('color: #3b82f6;', 'color: #8B53FF;'),

        # Progress bars and badges with cyan/blue
        ('background: rgba(56, 189, 248, 0.15); color: #38bdf8;', 'background: rgba(26, 229, 139, 0.15); color: #1AE589;'),
        ('background: rgba(6, 182, 212, 0.2); color: #38bdf8;', 'background: rgba(26, 229, 139, 0.15); color: #1AE589;'),
        ('background: rgba(59, 130, 246, 0.15); color: #3b82f6;', 'background: rgba(139, 83, 255, 0.15); color: #8B53FF;'),
        ('background: rgba(14, 165, 233, 0.15); color: #0ea5e9;', 'background: rgba(26, 229, 139, 0.15); color: #1AE589;'),

        # In-line spans with #38bdf8
        ('style="color:#38bdf8;"', 'style="color:#1AE589;"'),
        ('style="color: #38bdf8;"', 'style="color: #1AE589;"'),
        ('style="color:#fbbf24;"', 'style="color:#8B53FF;"'),
        ('style="color: #fbbf24;"', 'style="color: #8B53FF;"')
    ]

    for old, new in replacements:
        content = content.replace(old, new)

    # General regex pass for any straggler hex codes:
    # 1. Yellows -> #8B53FF or #1AE589
    content = re.sub(r'#fbbf24', '#8B53FF', content, flags=re.IGNORECASE)
    content = re.sub(r'#f59e0b', '#8B53FF', content, flags=re.IGNORECASE)
    content = re.sub(r'#d97706', '#8B53FF', content, flags=re.IGNORECASE)
    content = re.sub(r'#b45309', '#8B53FF', content, flags=re.IGNORECASE)

    # 2. Blues/Cyans -> #1AE589 or #8B53FF
    content = re.sub(r'#38bdf8', '#1AE589', content, flags=re.IGNORECASE)
    content = re.sub(r'#06b6d4', '#1AE589', content, flags=re.IGNORECASE)
    content = re.sub(r'#0ea5e9', '#1AE589', content, flags=re.IGNORECASE)
    content = re.sub(r'#0284c7', '#1AE589', content, flags=re.IGNORECASE)
    content = re.sub(r'#3b82f6', '#8B53FF', content, flags=re.IGNORECASE)
    content = re.sub(r'#2563eb', '#8B53FF', content, flags=re.IGNORECASE)

    # 3. rgba yellow/blues
    content = re.sub(r'rgba\(\s*245,\s*158,\s*11,\s*([0-9.]+)\)', r'rgba(139, 83, 255, \1)', content)
    content = re.sub(r'rgba\(\s*251,\s*191,\s*36,\s*([0-9.]+)\)', r'rgba(139, 83, 255, \1)', content)
    content = re.sub(r'rgba\(\s*6,\s*182,\s*212,\s*([0-9.]+)\)', r'rgba(26, 229, 139, \1)', content)
    content = re.sub(r'rgba\(\s*56,\s*189,\s*248,\s*([0-9.]+)\)', r'rgba(26, 229, 139, \1)', content)
    content = re.sub(r'rgba\(\s*59,\s*130,\s*246,\s*([0-9.]+)\)', r'rgba(139, 83, 255, \1)', content)
    content = re.sub(r'rgba\(\s*14,\s*165,\s*233,\s*([0-9.]+)\)', r'rgba(26, 229, 139, \1)', content)

    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(content)

    print("Purification completed successfully!")

if __name__ == '__main__':
    purify_palette()
