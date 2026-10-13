import asyncio
import json
import sys
from pathlib import Path
from playwright.async_api import async_playwright

ROOT = Path(__file__).resolve().parent.parent.parent.parent
PROFILE_DIR = ROOT / "data" / "browser_profiles" / "loyalfans_profile"
JWT_PATH = ROOT / "artifacts" / "current_jwt.txt"

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

AUTOMATION_RULES = [
    {
        "name": "1. Non Follower Starts Following (Nuevo Seguidor)",
        "rule": "FAN",
        "action": "FOLLOWS",
        "delay": 15,
        "message": (
            "Hey there! Welcome to my dark neon corner 💀✨.\n\n"
            "Software architect by day, biker & ukulele lover by night. "
            "Glad you made it here.\n\n"
            "Check out my exclusive clips in my store or unlock my timeline to see what I'm working on. "
            "Tell me, what caught your eye first? 🖤"
        )
    },
    {
        "name": "2. Non Follower Subscribes (Nuevo Suscriptor Directo)",
        "rule": "FAN",
        "action": "SUBSCRIBES",
        "delay": 15,
        "message": (
            "You just joined the inner circle... I like that a lot 🐾.\n\n"
            "You now have full VIP access to my daily timeline, discounted DMs, and all my private updates. "
            "Get comfortable. What made you finally take the leap? The tech brain or the biker attitude? 😈"
        )
    },
    {
        "name": "3. Non Follower Buys Video (Compra Video en Tienda)",
        "rule": "FAN",
        "action": "VIDEO_STORE_PURCHASE",
        "delay": 15,
        "message": (
            "Couldn't resist unlocking that clip, huh? I don't blame you... that one is a personal favorite 🖤.\n\n"
            "Hope you enjoyed every second. Did you know you get heavy discounts on all my future videos "
            "by subscribing to my club? Slide into my DMs if you want something custom 🚗💨"
        )
    },
    {
        "name": "4. Non Follower Buys Audio (Compra Audio en Tienda)",
        "rule": "FAN",
        "action": "AUDIO_STORE_PURCHASE",
        "delay": 15,
        "message": (
            "Loved having my voice whispering right in your ear? 🎧\n\n"
            "Close your eyes and let my words take you wherever you want to be. "
            "I post new voice notes and songs regularly. Tell me what fantasy you want next... 😉"
        )
    },
    {
        "name": "5. Follower Subscribes (Seguidor se Convierte en Suscriptor)",
        "rule": "FOLLOWER",
        "action": "SUBSCRIBES",
        "delay": 15,
        "message": (
            "Look at you stepping up from just watching to being part of my crew! 🏍️⚡\n\n"
            "Welcome to the VIP club. Every subscription gets me closer to my December car goal 🚗. "
            "Send me a message whenever you're ready to chat—I always prioritize my subscribers."
        )
    },
    {
        "name": "6. Follower Buys Video (Seguidor Compra Video)",
        "rule": "FOLLOWER",
        "action": "VIDEO_STORE_PURCHASE",
        "delay": 15,
        "message": (
            "Thank you for supporting my work and unlocking that video! 🖤\n\n"
            "Did it leave you craving more? If you subscribe, you unlock my full video vault at a discount. "
            "Tell me your favorite moment from that clip 😏"
        )
    },
    {
        "name": "7. Follower Buys Audio (Seguidor Compra Audio)",
        "rule": "FOLLOWER",
        "action": "AUDIO_STORE_PURCHASE",
        "delay": 15,
        "message": (
            "My voice in your headphones, my words in your head... 😈\n\n"
            "Hope it hit all the right spots. What kind of audio do you want me to record next? "
            "I'm listening..."
        )
    }
]

async def update_all():
    token = JWT_PATH.read_text().strip()
    print(f"Token leído desde {JWT_PATH} ({token[:30]}...)")
    
    async with async_playwright() as p:
        ctx = await p.chromium.launch_persistent_context(
            user_data_dir=str(PROFILE_DIR),
            headless=True
        )
        page = await ctx.new_page()
        await page.goto("https://www.loyalfans.com/settings/profile", wait_until="networkidle")
        await page.wait_for_timeout(1000)

        results = []
        for idx, item in enumerate(AUTOMATION_RULES, 1):
            print(f"[{idx}/7] Desplegando: {item['name']}...")
            res = await page.evaluate("""async ({ token, rule, action, message, delay }) => {
                try {
                    const r = await fetch('/api/v2/messages/automations/create-bundle?ngsw-bypass=true', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                            'Authorization': token
                        },
                        body: JSON.stringify({
                            rule: rule,
                            action: action,
                            message: {
                                lcm: false,
                                message: message,
                                media: []
                            },
                            delay: delay,
                            active: 1
                        })
                    });
                    const data = await r.json();
                    return { status: r.status, success: data.success, httpCode: data.httpCode };
                } catch(e) {
                    return { error: e.toString() };
                }
            }""", {
                "token": token,
                "rule": item["rule"],
                "action": item["action"],
                "message": item["message"],
                "delay": item["delay"]
            })
            print(f"     Resultado: HTTP {res.get('status')} - Success: {res.get('success')}")
            results.append({"name": item["name"], "res": res})
            await asyncio.sleep(0.8)

        # Capturar pantalla final
        await page.goto("https://www.loyalfans.com/settings/messages/messages-automation", wait_until="networkidle")
        await page.wait_for_timeout(2000)
        await page.screenshot(path=str(ROOT / "artifacts" / "all_automations_updated_verified.png"))
        print("Captura guardada en artifacts/all_automations_updated_verified.png")

        with open(ROOT / "artifacts" / "automations_update_result.json", "w", encoding="utf-8") as f:
            json.dump(results, f, indent=2, ensure_ascii=False)

        await ctx.close()

if __name__ == "__main__":
    asyncio.run(update_all())
