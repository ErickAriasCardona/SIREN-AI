import os
import sys
from pathlib import Path
from playwright.sync_api import sync_playwright

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

html_path = Path(__file__).resolve().parent.parent / "index.html"
file_url = html_path.as_uri()

print(f"Loading {file_url} in Playwright...")

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page(viewport={"width": 1440, "height": 900})

    errors = []
    page.on("pageerror", lambda err: errors.append(f"PageError: {err}"))
    page.on("console", lambda msg: errors.append(f"ConsoleError: {msg.text}") if msg.type == "error" else None)

    page.goto(file_url, wait_until="networkidle")

    # 1. Check title and brand
    title = page.title()
    print("Page Title:", title)
    assert "SIREN AI" in title, f"Title does not contain SIREN AI: {title}"

    brand_title = page.locator(".brand-title").inner_text()
    print("Brand Title:", brand_title)
    assert "SIREN" in brand_title, f"Brand title missing SIREN: {brand_title}"

    # 2. Test main tabs and subtabs
    tabs_to_test = [
        ("tab-perfiles", ["sub-perfil-streamate", "sub-perfil-loyalfans", "sub-perfil-stripchat", "sub-perfil-credenciales-grid"]),
        ("tab-finanzas", ["sub-finanzas-loyalfans", "sub-finanzas-streamate", "sub-finanzas-stripchat", "sub-finanzas-matriz"]),
        ("tab-posicionamiento", ["sub-pos-loyalfans", "sub-pos-streamate", "sub-pos-stripchat"]),
        ("tab-algoritmos", ["sub-algo-comparativa", "sub-algo-streamate", "sub-algo-loyalfans", "sub-algo-stripchat"]),
        ("tab-actualizaciones", ["sub-act-matriz", "sub-act-streamate", "sub-act-loyalfans", "sub-act-stripchat"]),
        ("tab-flujos", ["sub-flujo-hibrido", "sub-flujo-streamate", "sub-flujo-loyalfans", "sub-flujo-stripchat"]),
        ("tab-datascience", []),
        ("tab-roxanne-copilot", [])
    ]

    for tab_id, subtabs in tabs_to_test:
        print(f"\n--- Testing Main Tab: {tab_id} ---")
        page.evaluate(f"switchMainTab('{tab_id}')")
        page.wait_for_timeout(300)
        is_visible = page.is_visible(f"#{tab_id}")
        assert is_visible, f"Tab {tab_id} is not visible!"
        print(f"  ✓ {tab_id} is visible")

        # Test subtabs
        for sub_id in subtabs:
            print(f"  Testing Subtab: {sub_id}")
            # Click the matching button or activate via JS
            sub_selector = f"#{sub_id}"
            assert page.locator(sub_selector).count() > 0, f"Subtab element {sub_id} not found!"
            
            # Find button inside this tab-view that switches to this sub_id
            parts = sub_id.split("-")
            # e.g. sub-algo-streamate -> prefix: sub-algo, platform: streamate
            prefix = "-".join(parts[:-1])
            platform = parts[-1]
            btn_info = page.evaluate(f"""() => {{
                const tab = document.getElementById('{tab_id}');
                const btn = tab.querySelector(".subtab-btn[onclick*='{platform}']");
                const target = document.getElementById('{sub_id}');
                if (btn) btn.click();
                return {{
                    btnFound: !!btn,
                    btnHtml: btn ? btn.outerHTML : null,
                    targetDisplay: target ? target.style.display : null,
                    targetParentDisplay: target && target.parentElement ? target.parentElement.style.display : null,
                    targetParentId: target && target.parentElement ? target.parentElement.id : null
                }};
            }}""")
            page.wait_for_timeout(200)
            print("    Debug:", btn_info)

            # Check that sub_id is visible
            sub_visible = page.is_visible(sub_selector)
            assert sub_visible, f"Subtab {sub_id} did not become visible upon clicking button! Details: {btn_info}"
            print(f"    ✓ {sub_id} became visible")

    # 3. Test Theme Toggle
    print("\n--- Testing Theme Toggle ---")
    page.evaluate("toggleSirenTheme()")
    has_light = page.evaluate("document.body.classList.contains('light-theme')")
    assert has_light, "Light theme class not present after toggleSirenTheme()!"
    print("  ✓ Light theme enabled successfully")

    # Capture light screenshot
    page.screenshot(path="artifacts/siren_ui_light.png")

    page.evaluate("toggleSirenTheme()")
    has_light = page.evaluate("document.body.classList.contains('light-theme')")
    assert not has_light, "Light theme class still present after second toggle!"
    print("  ✓ Dark theme restored successfully")

    # Capture dark screenshot on tab-algoritmos
    page.evaluate("switchMainTab('tab-algoritmos')")
    page.wait_for_timeout(300)
    page.screenshot(path="artifacts/siren_ui_dark_algoritmos.png")

    # Capture dark screenshot on tab-actualizaciones
    page.evaluate("switchMainTab('tab-actualizaciones')")
    page.wait_for_timeout(300)
    page.screenshot(path="artifacts/siren_ui_dark_actualizaciones.png")

    print("\nUI verification complete!")
    if errors:
        print(f"Encountered {len(errors)} non-fatal/console notes:")
        for e in errors[:5]:
            print(" ", e)
    else:
        print("Zero console errors encountered!")

    browser.close()
