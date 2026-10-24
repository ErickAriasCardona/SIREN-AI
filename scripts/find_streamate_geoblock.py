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

async def find_geoblock():
    p = await async_playwright().start()
    profile_dir = Path("data/browser_profiles/streamate_profile")
    ctx = await p.chromium.launch_persistent_context(
        user_data_dir=str(profile_dir),
        headless=True,
        args=["--disable-blink-features=AutomationControlled", "--start-maximized"]
    )
    page = ctx.pages[0] if ctx.pages else await ctx.new_page()

    await page.goto("https://streamatemodels.com/dashboard-creator", timeout=35000)
    await page.wait_for_timeout(3000)

    # Let's inspect all scripts or React routes defined in the window / bundle
    routes = await page.evaluate('''() => {
        const found = [];
        // search all anchor tags or any element with href or onClick
        document.querySelectorAll('*').forEach(el => {
            const h = el.getAttribute('href');
            if (h) found.push(h);
            const to = el.getAttribute('to');
            if (to) found.push(to);
        });
        return Array.from(new Set(found));
    }''')
    print("Found routes/links:", len(routes))
    for r in routes:
        print("  ", r)

    # Let's check common Streamate URLs for geoblocking:
    test_urls = [
        "https://streamatemodels.com/account/block-regions",
        "https://streamatemodels.com/account/geoblock",
        "https://streamatemodels.com/settings/geoblock",
        "https://streamatemodels.com/customer/block-regions",
        "https://streamatemodels.com/security/geoblock",
        "https://streamatemodels.com/compliance/geoblock",
        "https://streamatemodels.com/account/blocked-regions"
    ]
    for u in test_urls:
        try:
            resp = await page.goto(u, timeout=10000)
            await page.wait_for_timeout(2000)
            t = await page.title()
            print(f"URL: {u} -> Status: {resp.status if resp else 'N/A'} | Title: {t} | Final URL: {page.url}")
            if page.url != "https://streamatemodels.com/dashboard-creator" and "404" not in t:
                shot = AUDIT_DIR / f"geoblock_test_{u.split('/')[-1]}.png"
                await page.screenshot(path=str(shot))
                print(f"  FOUND valid page at {u}!")
        except Exception as e:
            pass

    # Let's also check who administers the account (Studio vs Independent)
    # In Streamate, studio models cannot change payment methods directly; payment method is managed by the studio.
    # Let's check earnings / payout page
    try:
        await page.goto("https://streamatemodels.com/reports/earnings", timeout=15000)
        await page.wait_for_timeout(2500)
        await page.screenshot(path=str(AUDIT_DIR / "earnings_main.png"), full_page=True)
    except Exception as e:
        print("Earnings error:", e)

    await ctx.close()
    await p.stop()

if __name__ == "__main__":
    asyncio.run(find_geoblock())
