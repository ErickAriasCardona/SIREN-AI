import sys
import asyncio
from pathlib import Path
from playwright.async_api import async_playwright

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

VARIATIONS = [
    ("efac05@yopmail.com", "Centenario123@"),
    ("EFAC05@YOPMAIL.COM", "Centenario123@"),
    ("EFAC05", "Centenario123@"),
    ("efac05", "Centenario123@"),
    ("efac05@yopmail.com", "Centenario123"),
    ("efac05@yopmail.com", "centenario123@"),
    ("EFAC05@YOPMAIL.COM", "Centenario123")
]

async def test_variations():
    p = await async_playwright().start()
    profile_dir = Path("data/browser_profiles/streamate_profile")
    profile_dir.mkdir(parents=True, exist_ok=True)

    ctx = await p.chromium.launch_persistent_context(
        user_data_dir=str(profile_dir),
        headless=True,
        args=["--disable-blink-features=AutomationControlled"]
    )
    page = ctx.pages[0] if ctx.pages else await ctx.new_page()

    for user, pwd in VARIATIONS:
        print(f"\n--- Testing User: '{user}' | Pwd: '{pwd}' ---")
        await page.goto("https://streamatemodels.com/login", timeout=30000)
        await page.wait_for_timeout(2000)

        # Clear and fill
        await page.fill("#username", "")
        await page.type("#username", user, delay=20)
        await page.fill("#password", "")
        await page.type("#password", pwd, delay=20)
        await page.click('button[type="submit"]')
        await page.wait_for_timeout(4000)

        url = page.url
        title = await page.title()
        print(f"Result URL: {url} | Title: {title}")

        if "login" not in url.lower() or "dashboard" in url.lower() or "model" in url.lower():
            print(">>> SUCCESS! LOGGED IN! <<<")
            await page.screenshot(path="artifacts/streamate_login_success.png")
            break
        else:
            err = await page.evaluate('''() => {
                const el = document.querySelector('.error, .alert, .alert-danger, [role=alert], .form-error');
                return el ? el.innerText : '';
            }''')
            if not err:
                # check page text for error
                txt = await page.evaluate('() => document.body.innerText')
                for line in txt.split('\n'):
                    if 'incorrect' in line.lower() or 'error' in line.lower() or 'sorry' in line.lower() or 'invalid' in line.lower():
                        err = line.strip()
                        break
            print(f"Error text: {err}")

    await ctx.close()
    await p.stop()

if __name__ == "__main__":
    asyncio.run(test_variations())
