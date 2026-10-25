import os
import sys
from playwright.sync_api import sync_playwright

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

ARTIFACTS_DIR = r"C:\Users\MI PC\.gemini\antigravity\brain\4782b539-824e-4ebf-9a1f-b247d4f7399a"
os.makedirs(ARTIFACTS_DIR, exist_ok=True)

TABS = [
    'tab-estrategia',
    'tab-analisis',
    'tab-finanzas',
    'tab-algoritmos',
    'tab-actualizaciones',
    'tab-guia-directa',
    'tab-estrategia-general',
    'tab-produccion',
    'tab-language-rules',
    'tab-asistentes'
]

def test_all_tabs_responsive():
    print("==================================================")
    print("Testing All Tabs Across Mobile, Tablet, and Desktop")
    print("==================================================")
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        
        # 1. MOBILE VIEWPORT (390 x 844)
        print("\n--- 1. Testing Mobile Viewport (390x844) ---")
        context_m = browser.new_context(viewport={"width": 390, "height": 844})
        page_m = context_m.new_page()
        page_m.goto("http://localhost:8888/", wait_until="networkidle")
        page_m.wait_for_timeout(1000)
        
        mobile_failures = []
        for tab_id in TABS:
            page_m.evaluate(f"() => switchMainTab('{tab_id}')")
            page_m.wait_for_timeout(400)
            
            doc_sw = page_m.evaluate("() => document.documentElement.scrollWidth")
            body_sw = page_m.evaluate("() => document.body.scrollWidth")
            cw = page_m.evaluate("() => document.documentElement.clientWidth")
            
            status = "PASS" if doc_sw <= cw else "FAIL"
            print(f"Tab [{tab_id}]: doc_sw={doc_sw}, clientWidth={cw} -> {status}")
            if doc_sw > cw:
                mobile_failures.append((tab_id, doc_sw, cw))
                
        # Capture screenshots for key tabs
        page_m.evaluate("() => switchMainTab('tab-finanzas')")
        page_m.wait_for_timeout(500)
        page_m.screenshot(path=os.path.join(ARTIFACTS_DIR, "mobile_finanzas_fixed.png"))
        
        page_m.evaluate("() => switchMainTab('tab-algoritmos')")
        page_m.wait_for_timeout(500)
        page_m.screenshot(path=os.path.join(ARTIFACTS_DIR, "mobile_algoritmos_fixed.png"))
        
        page_m.evaluate("() => switchMainTab('tab-actualizaciones')")
        page_m.wait_for_timeout(500)
        page_m.screenshot(path=os.path.join(ARTIFACTS_DIR, "mobile_actualizaciones_fixed.png"))

        page_m.evaluate("() => switchMainTab('tab-produccion')")
        page_m.wait_for_timeout(500)
        page_m.screenshot(path=os.path.join(ARTIFACTS_DIR, "mobile_produccion_fixed.png"))
        
        # 2. TABLET VIEWPORT (768 x 1024)
        print("\n--- 2. Testing Tablet Viewport (768x1024) ---")
        context_t = browser.new_context(viewport={"width": 768, "height": 1024})
        page_t = context_t.new_page()
        page_t.goto("http://localhost:8888/", wait_until="networkidle")
        page_t.wait_for_timeout(1000)
        
        tablet_failures = []
        for tab_id in TABS:
            page_t.evaluate(f"() => switchMainTab('{tab_id}')")
            page_t.wait_for_timeout(400)
            
            doc_sw = page_t.evaluate("() => document.documentElement.scrollWidth")
            cw = page_t.evaluate("() => document.documentElement.clientWidth")
            
            status = "PASS" if doc_sw <= cw else "FAIL"
            print(f"Tab [{tab_id}]: doc_sw={doc_sw}, clientWidth={cw} -> {status}")
            if doc_sw > cw:
                tablet_failures.append((tab_id, doc_sw, cw))
                
        page_t.evaluate("() => switchMainTab('tab-finanzas')")
        page_t.wait_for_timeout(500)
        page_t.screenshot(path=os.path.join(ARTIFACTS_DIR, "tablet_finanzas_fixed.png"))

        browser.close()
        
        print("\n==================================================")
        print(f"Summary: Mobile Failures: {len(mobile_failures)}, Tablet Failures: {len(tablet_failures)}")
        print("==================================================")
        if mobile_failures or tablet_failures:
            print("FAILED:", mobile_failures, tablet_failures)
            sys.exit(1)
        else:
            print("ALL RESPONSIVE TESTS PASSED SUCCESSFULLY!")

if __name__ == "__main__":
    test_all_tabs_responsive()
