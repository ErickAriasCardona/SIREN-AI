import sys
import json
import asyncio
from pathlib import Path
from playwright.async_api import async_playwright

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

AUDIT_DIR = Path("artifacts/streamate_audit")
AUDIT_DIR.mkdir(parents=True, exist_ok=True)
JSON_OUTPUT = Path("data/audits/streamate_studio_audit.json")
JSON_OUTPUT.parent.mkdir(parents=True, exist_ok=True)

async def audit_streamate():
    p = await async_playwright().start()
    profile_dir = Path("data/browser_profiles/streamate_profile")
    ctx = await p.chromium.launch_persistent_context(
        user_data_dir=str(profile_dir),
        headless=True,
        args=["--disable-blink-features=AutomationControlled", "--start-maximized"]
    )
    page = ctx.pages[0] if ctx.pages else await ctx.new_page()

    audit_data = {
        "timestamp": "2026-10-24T13:22:00",
        "platform": "Streamate (StreamateModels)",
        "login_email": "efac05@yopmail.com",
        "dashboard_url": "",
        "sections": {},
        "navigation_links": [],
        "screenshots": {}
    }

    print("--- 1. Navigating to Dashboard ---")
    await page.goto("https://streamatemodels.com/dashboard-creator", timeout=35000)
    await page.wait_for_timeout(4000)

    audit_data["dashboard_url"] = page.url
    await page.screenshot(path=str(AUDIT_DIR / "01_dashboard.png"), full_page=True)
    audit_data["screenshots"]["dashboard"] = str(AUDIT_DIR / "01_dashboard.png")

    # Extract all links in the dashboard/menu
    links = await page.evaluate('''() => {
        return Array.from(document.querySelectorAll('a')).map(a => ({
            href: a.href,
            text: (a.innerText || '').trim(),
            title: a.getAttribute('title') || ''
        })).filter(x => x.href && !x.href.startsWith('javascript'));
    }''')
    audit_data["navigation_links"] = links
    print(f"Extracted {len(links)} navigation links.")
    for l in links[:20]:
        if l['text']:
            print(f"  Link: {l['text']} -> {l['href']}")

    # Dashboard body text
    dash_text = await page.evaluate('() => document.body.innerText')
    audit_data["sections"]["dashboard_text"] = dash_text

    # Search for specific profile, settings, rates, studio pages
    targets = [
        ("profile", ["profile", "bio", "about", "model-profile"]),
        ("pricing", ["pricing", "rates", "prices", "shows", "settings/shows"]),
        ("geoblock", ["geoblock", "block", "regions", "security"]),
        ("studio_account", ["studio", "account", "payout", "earnings", "contract"]),
        ("categories", ["category", "categories", "tags", "attributes"])
    ]

    # Let's inspect potential URLs from extracted links or direct patterns
    visited_urls = set()

    for category, keywords in targets:
        matched_link = None
        for l in links:
            h = l['href'].lower()
            t = l['text'].lower()
            if any(k in h or k in t for k in keywords):
                if h not in visited_urls and "logout" not in h:
                    matched_link = l['href']
                    break

        if matched_link:
            visited_urls.add(matched_link)
            print(f"\n--- Auditing {category}: {matched_link} ---")
            try:
                await page.goto(matched_link, timeout=30000)
                await page.wait_for_timeout(3500)
                shot_path = AUDIT_DIR / f"{category}.png"
                await page.screenshot(path=str(shot_path), full_page=True)
                audit_data["screenshots"][category] = str(shot_path)
                
                sec_text = await page.evaluate('() => document.body.innerText')
                audit_data["sections"][category] = {
                    "url": page.url,
                    "title": await page.title(),
                    "text": sec_text
                }
                print(f"  Captured {category} ({len(sec_text)} chars text)")
            except Exception as e:
                print(f"  Error loading {matched_link}: {e}")

    # Save complete JSON
    with open(JSON_OUTPUT, "w", encoding="utf-8") as f:
        json.dump(audit_data, f, indent=2, ensure_ascii=False)
    print(f"\nAudit JSON saved to: {JSON_OUTPUT}")

    await ctx.close()
    await p.stop()

if __name__ == "__main__":
    asyncio.run(audit_streamate())
