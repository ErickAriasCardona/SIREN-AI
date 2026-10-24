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

async def deep_crawl():
    p = await async_playwright().start()
    profile_dir = Path("data/browser_profiles/streamate_profile")
    ctx = await p.chromium.launch_persistent_context(
        user_data_dir=str(profile_dir),
        headless=True,
        args=["--disable-blink-features=AutomationControlled", "--start-maximized"]
    )
    page = ctx.pages[0] if ctx.pages else await ctx.new_page()

    print("--- 1. Navigating to Dashboard ---")
    await page.goto("https://streamatemodels.com/dashboard-creator", timeout=35000)
    await page.wait_for_timeout(3000)

    # Click Hamburger Menu (top-left)
    print("--- 2. Clicking Hamburger Menu ---")
    try:
        # The hamburger menu is typically the first button or an svg with 3 lines
        hamburger = page.locator('header button, [aria-label="menu"], [aria-label="Navigation"], svg path[d*="M3 18h18"]').first
        if await hamburger.count() > 0:
            await hamburger.click()
            await page.wait_for_timeout(1500)
            await page.screenshot(path=str(AUDIT_DIR / "02_hamburger_menu.png"))
            menu_text = await page.evaluate('() => document.querySelector("nav, [role=\'dialog\'], aside, .MuiDrawer-root") ? document.querySelector("nav, [role=\'dialog\'], aside, .MuiDrawer-root").innerText : ""')
            print("Hamburger menu text:\n", menu_text)
    except Exception as e:
        print("Error opening hamburger:", e)

    # Look for User Account Menu (top-right avatar icon)
    print("--- 3. Clicking User Account Menu (Top-Right) ---")
    try:
        # Avatar or account button at top right
        account_btn = page.locator('header button:has([data-testid="AccountCircleIcon"]), header [aria-label*="account"], header button:last-child').first
        await account_btn.click()
        await page.wait_for_timeout(1500)
        await page.screenshot(path=str(AUDIT_DIR / "03_account_menu.png"))
        acc_text = await page.evaluate('() => document.querySelector("[role=\'menu\'], .MuiMenu-paper, [role=\'dialog\']") ? document.querySelector("[role=\'menu\'], .MuiMenu-paper, [role=\'dialog\']").innerText : ""')
        print("Account menu text:\n", acc_text)
    except Exception as e:
        print("Error opening account menu:", e)

    # Direct navigation to known Streamate sub-endpoints
    endpoints = [
        ("my_profile", "https://streamatemodels.com/profile"),
        ("cammodel_profile", "https://streamatemodels.com/cammodel/profile"),
        ("account_settings", "https://streamatemodels.com/account/settings"),
        ("account_details", "https://streamatemodels.com/account"),
        ("pricing_rates", "https://streamatemodels.com/pricing"),
        ("rates_settings", "https://streamatemodels.com/settings/rates"),
        ("geoblock_settings", "https://streamatemodels.com/customer/geoblock"),
        ("geoblock_regions", "https://streamatemodels.com/settings/security"),
        ("payout_settings", "https://streamatemodels.com/reports/payment-options"),
        ("payout_methods", "https://streamatemodels.com/account/payout")
    ]

    results = {}
    for name, url in endpoints:
        print(f"\n--- Testing Endpoint: {name} ({url}) ---")
        try:
            resp = await page.goto(url, timeout=15000)
            await page.wait_for_timeout(2500)
            status = resp.status if resp else "Unknown"
            cur_url = page.url
            title = await page.title()
            print(f"Status: {status} | Current URL: {cur_url} | Title: {title}")
            
            # If not redirected to dashboard or 404
            if cur_url != "https://streamatemodels.com/dashboard-creator" and "404" not in title:
                shot_file = AUDIT_DIR / f"endpoint_{name}.png"
                await page.screenshot(path=str(shot_file), full_page=True)
                body_text = await page.evaluate('() => document.body.innerText')
                results[name] = {
                    "url": cur_url,
                    "title": title,
                    "screenshot": str(shot_file),
                    "text_preview": body_text[:1000]
                }
                print(f"Captured {name}: {len(body_text)} chars")
        except Exception as e:
            print(f"Failed {name}: {e}")

    with open("data/audits/streamate_endpoints_probe.json", "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)

    await ctx.close()
    await p.stop()
    print("\nProbe completed!")

if __name__ == "__main__":
    asyncio.run(deep_crawl())
