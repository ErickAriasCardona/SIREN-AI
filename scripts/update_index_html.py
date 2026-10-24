import sys
import re
from pathlib import Path

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

INDEX_PATH = Path("index.html")
with open(INDEX_PATH, "r", encoding="utf-8") as f:
    content = f.read()

print("Original length:", len(content))

# 1. ADD LIGHT THEME CSS
light_theme_css = """
    /* ========================================== */
    /* ☀️ MODO CLARO (LIGHT THEME) — VELVET AI   */
    /* ========================================== */
    body.light-theme {
      --bg-dark: #f8fafc;
      --bg-surface: #ffffff;
      --bg-card: #ffffff;
      --bg-card-hover: #f1f5f9;
      --border-color: rgba(0, 0, 0, 0.08);
      --border-accent: rgba(147, 51, 234, 0.25);
      --text-main: #0f172a;
      --text-muted: #475569;
      --text-dim: #64748b;
      --shadow-card: 0 4px 20px rgba(0, 0, 0, 0.06);
    }
    body.light-theme #sidebar {
      background: #ffffff;
      border-right: 1px solid #e2e8f0;
      box-shadow: 0 4px 20px rgba(0, 0, 0, 0.04);
    }
    body.light-theme .brand-title {
      color: #0f172a;
    }
    body.light-theme .sidebar-model-pill {
      background: #f8fafc;
      border-color: #e2e8f0;
    }
    body.light-theme .top-bar {
      background: rgba(255, 255, 255, 0.85);
      border-bottom: 1px solid #e2e8f0;
    }
    body.light-theme .top-left h2 {
      color: #0f172a;
    }
    body.light-theme .card,
    body.light-theme .kpi-card,
    body.light-theme .platform-profile-card {
      background: #ffffff;
      border-color: #e2e8f0;
      box-shadow: 0 4px 16px rgba(0, 0, 0, 0.04);
    }
    body.light-theme .kpi-value {
      color: #0f172a;
    }
    body.light-theme .card-title {
      color: #0f172a;
    }
    body.light-theme .bio-preview-box {
      background: #f8fafc;
      color: #1e293b;
      border-color: #cbd5e1;
    }
    body.light-theme .chat-bubble {
      background: #f1f5f9;
      color: #0f172a;
      border-color: #e2e8f0;
    }
    body.light-theme .chat-input-row textarea {
      background: #ffffff;
      color: #0f172a;
      border-color: #cbd5e1;
    }
    body.light-theme .credential-box {
      background: #f8fafc !important;
      border-color: #e2e8f0 !important;
    }
    body.light-theme .custom-table th {
      background: #f8fafc;
      color: #475569;
    }
    body.light-theme .custom-table td {
      border-bottom: 1px solid #f1f5f9;
      color: #1e293b;
    }
    body.light-theme .sidebar-footer {
      background: #f8fafc;
      border-top: 1px solid #e2e8f0;
    }
"""

if "/* ☀️ MODO CLARO (LIGHT THEME)" not in content:
    content = content.replace("    /* Scrollbars */", light_theme_css + "\n    /* Scrollbars */")
    print("Added Light Theme CSS.")

# 2. ADD THEME TOGGLE BUTTON IN TOP BAR
theme_btn_html = """        <button id="theme-toggle-btn" class="action-btn" onclick="toggleVelvetTheme()" title="Alternar Modo Claro / Oscuro" style="display:inline-flex; align-items:center; gap:6px;">
          <i data-lucide="sun" id="theme-icon"></i>
          <span id="theme-label">Modo Claro</span>
        </button>
        <button id="btn-top-refresh" class="action-btn" onclick="refreshAllDataNow()">"""

if 'id="theme-toggle-btn"' not in content:
    content = content.replace("""        <button id="btn-top-refresh" class="action-btn" onclick="refreshAllDataNow()">""", theme_btn_html)
    print("Added Theme Toggle Button to Top Bar.")

with open(INDEX_PATH, "w", encoding="utf-8") as f:
    f.write(content)

print("Step 1 saved!")
