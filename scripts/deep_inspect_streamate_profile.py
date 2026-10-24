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

async def deep_profile_inspect():
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

    # 1. Click Account Menu (Top Right)
    print("--- 2. Clicking Header Account Button ---")
    try:
        acc_btn = page.locator('#header_account_button').first
        if await acc_btn.count() > 0:
            await acc_btn.click()
            await page.wait_for_timeout(1500)
            await page.screenshot(path=str(AUDIT_DIR / "04_account_menu_open.png"))
            acc_links = await page.evaluate('''() => {
                const menu = document.querySelector('[role="menu"], [role="dialog"], .MuiPopover-root, .MuiMenu-root');
                if (!menu) return { text: "No menu found", links: [] };
                return {
                    text: menu.innerText,
                    links: Array.from(menu.querySelectorAll('a, button')).map(el => ({
                        tag: el.tagName,
                        text: el.innerText.trim(),
                        href: el.getAttribute('href') || ''
                    }))
                };
            }''')
            print("Account Menu Info:", json.dumps(acc_links, indent=2))
            # Close menu by pressing Escape or clicking outside
            await page.keyboard.press("Escape")
            await page.wait_for_timeout(1000)
    except Exception as e:
        print("Error on account menu:", e)

    # 2. Click Hamburger Menu and expand submenus
    print("--- 3. Exploring Hamburger Menu Subsections ---")
    try:
        hamburger = page.locator('header button').first
        await hamburger.click()
        await page.wait_for_timeout(1500)

        # Check all items in drawer
        drawer_items = await page.evaluate('''() => {
            return Array.from(document.querySelectorAll('nav a, nav button, [role="dialog"] button, [role="dialog"] a')).map(el => ({
                text: el.innerText.trim(),
                href: el.getAttribute('href') || '',
                tag: el.tagName
            }));
        }''')
        print("Drawer Items:", json.dumps(drawer_items, indent=2))

        # Click on Customers in drawer if present
        cust_btn = page.locator('nav button:has-text("Customers"), [role="dialog"] button:has-text("Customers")').first
        if await cust_btn.count() > 0:
            await cust_btn.click()
            await page.wait_for_timeout(1000)
            await page.screenshot(path=str(AUDIT_DIR / "05_hamburger_customers_expanded.png"))
            cust_subitems = await page.evaluate('() => document.body.innerText')
            print("Customers subitems text captured.")

        # Close drawer
        close_btn = page.locator('button:has-text("✕"), [aria-label="close"], svg path[d*="M19 6.41"]').first
        if await close_btn.count() > 0:
            await close_btn.click()
            await page.wait_for_timeout(1000)
        else:
            await page.keyboard.press("Escape")
            await page.wait_for_timeout(1000)
    except Exception as e:
        print("Error in drawer exploration:", e)

    # 3. Check Rates & Pricing Modal
    print("--- 4. Exploring Rates & Pricing ---")
    try:
        # Click 3 dots on Rates & Pricing card or Configure Pricing
        rates_dots = page.locator('[aria-label="More"], [data-testid="MoreVertIcon"], button:has-text("Configure Pricing")').first
        if await rates_dots.count() > 0:
            await rates_dots.click()
            await page.wait_for_timeout(1500)
            await page.screenshot(path=str(AUDIT_DIR / "06_rates_options.png"))
            rates_menu = await page.evaluate('() => document.body.innerText')
            print("Rates menu/modal text captured.")
            await page.keyboard.press("Escape")
            await page.wait_for_timeout(1000)
    except Exception as e:
        print("Error on rates dots:", e)

    # 4. Check Public Profile Page on Cammodels / Streamate
    print("--- 5. Checking Public Model Profile (SamBartone) ---")
    try:
        pub_page = await ctx.new_page()
        # Let's check streamate.com/cam/SamBartone or sambartone.cammodels.com
        resp = await pub_page.goto("https://sambartone.cammodels.com", timeout=25000)
        await pub_page.wait_for_timeout(3000)
        await pub_page.screenshot(path=str(AUDIT_DIR / "07_public_profile_cammodels.png"), full_page=True)
        pub_text = await pub_page.evaluate('() => document.body.innerText')
        print(f"Public cammodels profile status: {resp.status if resp else 'N/A'}")
        print("Public profile text preview:\n", pub_text[:1200])

        with open(AUDIT_DIR / "public_profile_text.txt", "w", encoding="utf-8") as f:
            f.write(pub_text)
        await pub_page.close()
    except Exception as e:
        print("Error loading public profile:", e)

    # 5. Let's check streamate.com/cam/SamBartone
    try:
        sm_pub = await ctx.new_page()
        resp2 = await sm_pub.goto("https://streamate.com/cam/SamBartone", timeout=25000)
        await sm_pub.wait_for_timeout(3000)
        await sm_pub.screenshot(path=str(AUDIT_DIR / "08_public_profile_streamate.png"), full_page=True)
        sm_text = await sm_pub.evaluate('() => document.body.innerText')
        print(f"Public Streamate profile status: {resp2.status if resp2 else 'N/A'}")
        print("Streamate profile text preview:\n", sm_text[:1200])
        with open(AUDIT_DIR / "streamate_public_profile_text.txt", "w", encoding="utf-8") as f:
            f.write(sm_text)
        await sm_pub.close()
    except Exception as e:
        print("Error loading streamate public profile:", e)

    await ctx.close()
    await p.stop()
    print("Done deep profile inspect!")

if __name__ == "__main__":
    asyncio.run(deep_profile_inspect())
