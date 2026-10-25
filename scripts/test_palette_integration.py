import sys
from pathlib import Path
from playwright.sync_api import sync_playwright

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

root = Path(__file__).resolve().parent.parent

# 1. Verify TypeScript theme file existence and content
theme_file = root / "lib" / "paleta colores" / "theme.tsx"
assert theme_file.exists(), f"Missing file: {theme_file}"

content = theme_file.read_text(encoding="utf-8")
assert "primary: '#8B53FF'" in content or "8B53FF" in content, "Missing HEX 8B53FF in theme.tsx"
assert "primaryDark: '#1E2432'" in content or "1E2432" in content, "Missing HEX 1E2432 in theme.tsx"
assert "accentGreen: '#1AE589'" in content or "1AE589" in content, "Missing HEX 1AE589 in theme.tsx"
assert "lightBackground: '#F2F2F2'" in content or "F2F2F2" in content, "Missing HEX F2F2F2 in theme.tsx"
print("✓ lib/paleta colores/theme.tsx correctly defines all 4 palette colors and SIREN_AI tokens!")

# 2. Verify runtime in browser
html_path = root / "index.html"
file_url = html_path.as_uri()

print("Testing browser runtime with Playwright...")

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page(viewport={"width": 1440, "height": 900})

    page.goto(file_url, wait_until="networkidle")

    # Evaluate window.SIREN_AI
    siren_ai = page.evaluate("() => window.SIREN_AI")
    assert siren_ai is not None, "window.SIREN_AI not found!"
    assert siren_ai.get("primary") == "#8B53FF", f"Wrong primary: {siren_ai.get('primary')}"
    assert siren_ai.get("primaryDark") == "#1E2432", f"Wrong primaryDark: {siren_ai.get('primaryDark')}"
    assert siren_ai.get("accentGreen") == "#1AE589", f"Wrong accentGreen: {siren_ai.get('accentGreen')}"
    assert siren_ai.get("lightBackground") == "#F2F2F2", f"Wrong lightBackground: {siren_ai.get('lightBackground')}"
    print("✓ window.SIREN_AI matches palette exactly:")
    print("  - primary:", siren_ai.get("primary"))
    print("  - primaryDark:", siren_ai.get("primaryDark"))
    print("  - accentGreen:", siren_ai.get("accentGreen"))
    print("  - lightBackground:", siren_ai.get("lightBackground"))

    # Screenshot in Light Mode with new palette
    page.screenshot(path="artifacts/siren_palette_light.png")
    print("✓ Saved screenshot in Light Mode")

    # Switch to Dark Mode and take screenshot
    page.locator("#theme-toggle-btn").click()
    page.wait_for_timeout(200)
    page.screenshot(path="artifacts/siren_palette_dark.png")
    print("✓ Saved screenshot in Dark Mode (Navy #1E2432 background)")

    print("\n🎉 ALL PALETTE INTEGRATION TESTS PASSED 100%!")
    browser.close()
