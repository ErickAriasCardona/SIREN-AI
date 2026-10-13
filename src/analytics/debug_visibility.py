import asyncio
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        await page.goto("http://localhost:8888/index.html")
        await page.evaluate("switchMainTab('tab-roxanne-copilot')")
        
        info = await page.evaluate("""() => {
            let el = document.getElementById('copilot-input');
            let path = [];
            while (el) {
                let style = window.getComputedStyle(el);
                path.push({ 
                    tag: el.tagName, 
                    id: el.id, 
                    class: el.className, 
                    display: style.display, 
                    visibility: style.visibility 
                });
                el = el.parentElement;
            }
            return path;
        }""")
        for item in info:
            print(item)
        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())
