import sys
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
from playwright.sync_api import sync_playwright

def scan_all_views():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(viewport={'width': 390, 'height': 844})
        page.goto('http://localhost:8888/')
        page.wait_for_timeout(1000)

        tabs = page.evaluate("""() => {
            return Array.from(document.querySelectorAll('.tab-view')).map(t => t.id);
        }""")
        print("Discovered tabs:", tabs)

        for tab_id in tabs:
            page.evaluate(f"switchMainTab('{tab_id}')")
            page.wait_for_timeout(300)

            # Check all subtabs if any
            subtabs = page.evaluate(f"""() => {{
                const tab = document.getElementById('{tab_id}');
                const btns = tab.querySelectorAll('.subtab-btn');
                return Array.from(btns).map((b, i) => ({{ text: b.textContent.trim(), idx: i }}));
            }}""")

            if not subtabs:
                subtabs = [{'text': 'default', 'idx': -1}]

            for st in subtabs:
                if st['idx'] >= 0:
                    page.evaluate(f"""() => {{
                        const tab = document.getElementById('{tab_id}');
                        const btns = tab.querySelectorAll('.subtab-btn');
                        if (btns[{st['idx']}]) btns[{st['idx']}].click();
                    }}""")
                    page.wait_for_timeout(200)

                # If this is tab-asistentes, check each assistant
                if tab_id == 'tab-asistentes':
                    for asst in ['roxanne', 'chloe', 'diana', 'electra']:
                        page.evaluate(f"selectAssistant('{asst}')")
                        page.wait_for_timeout(200)
                        ca_sw = page.evaluate('document.querySelector(".content-area").scrollWidth')
                        doc_sw = page.evaluate('document.documentElement.scrollWidth')
                        if ca_sw > 390 or doc_sw > 390:
                            print(f"❌ OVERFLOW in {tab_id} (assistant: {asst}): ca.scrollWidth={ca_sw}, doc.scrollWidth={doc_sw}")
                        else:
                            print(f"✓ OK in {tab_id} (assistant: {asst}): ca={ca_sw}, doc={doc_sw}")
                else:
                    ca_sw = page.evaluate('document.querySelector(".content-area").scrollWidth')
                    doc_sw = page.evaluate('document.documentElement.scrollWidth')
                    st_name = st['text'][:25]
                    if ca_sw > 390 or doc_sw > 390:
                        print(f"❌ OVERFLOW in {tab_id} [{st_name}]: ca.scrollWidth={ca_sw}, doc.scrollWidth={doc_sw}")
                    else:
                        print(f"✓ OK in {tab_id} [{st_name}]: ca={ca_sw}, doc={doc_sw}")

        browser.close()

if __name__ == '__main__':
    scan_all_views()
