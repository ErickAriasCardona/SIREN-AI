from playwright.sync_api import sync_playwright

def diagnose():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(viewport={'width': 390, 'height': 844})
        page = context.new_page()
        page.goto('http://localhost:8888/')
        page.wait_for_timeout(1000)
        
        # Test Roxanne
        page.evaluate("switchMainTab('tab-asistentes')")
        page.wait_for_timeout(500)
        page.evaluate("selectAssistant('roxanne')")
        page.wait_for_timeout(500)
        
        # Check Roxanne panel width and elements
        panel_info = page.evaluate("""() => {
            const panel = document.getElementById('panel-tools-roxanne');
            const rightPanel = document.getElementById('roxanne-right-panel');
            const centerChat = document.querySelector('.roxanne-center-chat');
            const container = document.querySelector('.roxanne-layout-container');
            return {
                containerWidth: container ? container.getBoundingClientRect().width : 0,
                centerChatWidth: centerChat ? centerChat.getBoundingClientRect().width : 0,
                rightPanelWidth: rightPanel ? rightPanel.getBoundingClientRect().width : 0,
                panelToolsWidth: panel ? panel.getBoundingClientRect().width : 0,
                panelToolsDisplay: panel ? window.getComputedStyle(panel).display : '',
                panelToolsFlexDirection: panel ? window.getComputedStyle(panel).flexDirection : '',
                childrenWidths: panel ? Array.from(panel.children).map(c => ({
                    tag: c.tagName,
                    className: c.className,
                    width: Math.round(c.getBoundingClientRect().width),
                    scrollWidth: c.scrollWidth
                })) : []
            };
        }""")
        import pprint
        print("Roxanne Panel Metrics:")
        pprint.pprint(panel_info)
        
        overflowing = page.evaluate("""() => {
            const els = document.querySelectorAll('*');
            const res = [];
            for (const el of els) {
                const rect = el.getBoundingClientRect();
                if (rect.right > window.innerWidth + 2) {
                    res.push({
                        tag: el.tagName,
                        id: el.id,
                        className: typeof el.className === 'string' ? el.className : '',
                        right: Math.round(rect.right),
                        width: Math.round(rect.width)
                    });
                }
            }
            return res.slice(0, 20);
        }""")
        print("Overflowing elements in Roxanne view (count:", len(overflowing), "):")
        for item in overflowing:
            print("  ", item)
            
        # Also check all other tabs:
        tabs = ['tab-asistentes', 'tab-live', 'tab-monetizacion', 'tab-finanzas', 'tab-analitica', 'tab-settings']
        for tab in tabs:
            page.evaluate(f"switchMainTab('{tab}')")
            page.wait_for_timeout(300)
            sw = page.evaluate('document.documentElement.scrollWidth')
            bsw = page.evaluate('document.body.scrollWidth')
            csw = page.evaluate('document.querySelector(".content-area") ? document.querySelector(".content-area").scrollWidth : 0')
            print(f"Tab '{tab}': doc.scrollWidth={sw}, body.scrollWidth={bsw}, content-area.scrollWidth={csw}")

        browser.close()

if __name__ == '__main__':
    diagnose()
