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

async def inspect_more():
    p = await async_playwright().start()
    profile_dir = Path("data/browser_profiles/streamate_profile")
    ctx = await p.chromium.launch_persistent_context(
        user_data_dir=str(profile_dir),
        headless=True,
        args=["--disable-blink-features=AutomationControlled", "--start-maximized"]
    )
    page = ctx.pages[0] if ctx.pages else await ctx.new_page()

    # 1. Check performer client
    print("--- 1. Navigating to Performer Client ---")
    try:
        await page.goto("https://performerclient.streamatemodels.com/client", timeout=30000)
        await page.wait_for_timeout(4000)
        shot = AUDIT_DIR / "09_performer_client.png"
        await page.screenshot(path=str(shot), full_page=True)
        text = await page.evaluate('() => document.body.innerText')
        print(f"Performer Client URL: {page.url} | chars: {len(text)}")
        print("Performer Client preview:\n", text[:800])
    except Exception as e:
        print("Performer client error:", e)

    # 2. Check message pricing
    print("--- 2. Navigating to Message Pricing ---")
    try:
        await page.goto("https://streamatemodels.com/engagement/message-pricing", timeout=20000)
        await page.wait_for_timeout(3000)
        shot = AUDIT_DIR / "10_message_pricing.png"
        await page.screenshot(path=str(shot), full_page=True)
        text2 = await page.evaluate('() => document.body.innerText')
        print(f"Message Pricing chars: {len(text2)}")
        print("Message pricing preview:\n", text2[:800])
    except Exception as e:
        print("Message pricing error:", e)

    # 3. Check Peer Link
    print("--- 3. Navigating to Peer Link ---")
    try:
        await page.goto("https://www.streamatemodels.com/account/peer-link", timeout=20000)
        await page.wait_for_timeout(3000)
        shot = AUDIT_DIR / "11_peer_link.png"
        await page.screenshot(path=str(shot), full_page=True)
        text3 = await page.evaluate('() => document.body.innerText')
        print("Peer link preview:\n", text3[:800])
    except Exception as e:
        print("Peer link error:", e)

    await ctx.close()
    await p.stop()

if __name__ == "__main__":
    asyncio.run(inspect_more())
