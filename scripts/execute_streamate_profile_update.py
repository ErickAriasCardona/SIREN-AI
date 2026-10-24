import asyncio
import json
from pathlib import Path
from playwright.async_api import async_playwright

OUT_DIR = Path("artifacts/streamate_update_evidence")
OUT_DIR.mkdir(parents=True, exist_ok=True)

TEXTS = {
    'ES': {
        'Headline': 'Chica tomboy versatil con energia propia, curiosa e inteligente.',
        'My Show': 'Mi mundo va entre la musica, tecnologia, deporte y pasion por el deseo. Toco el ukelele y disfruto sensaciones intensas a solas. Piel sensible al calor del momento, sonrisa picara que tienta y entrega total cuando alguien me enciende sin frenos.',
        'Turn Ons': 'Me enciende ver tus reacciones y sostener tu mirada fija sin hablar. Tambien me encienden las vibraciones inesperadas en mi piel, sentir el calor despacio y esa complicidad donde ambos sabemos bien lo que queremos.',
        'Expertise': 'Abrir paso a la intimidad, alternar el control y vivir fantasias sin ataduras. Empezar suave, provocar con calma y subir el ritmo hablando al oido, complaciendo caprichos mutuos donde ambos terminamos satisfechos.'
    },
    'EN': {
        'Headline': 'Versatile tomboy with own energy, smart and direct curiosity.',
        'My Show': 'My world moves between music, tech, sports and exploring desire. I play ukulele and enjoy intense solo sensations. Sensitive skin that reacts fast to the heat of the moment, a cheeky smile that teases and full surrender once someone turns me on.',
        'Turn Ons': 'Watching your reactions and holding your steady gaze with no words needed. Unexpected vibrations across my sensitive skin, feeling the heat rise slowly and that visual chemistry where we both know what we want.',
        'Expertise': 'Letting curiosity open intimate moments, alternating control and living fantasies. Starting soft, teasing calmly, then speeding up the rhythm as the heat rises, whispering in your ear until we are fully satisfied.'
    },
    'FR': {
        'Headline': 'Fille tomboy versatile avec sa propre energie, curieuse et vive.',
        'My Show': 'Mon univers bouge entre musique, tech, sport et desir intense. Je joue du ukulele et savoure des sensations intimes en solo. Une peau sensible au chaud du moment, un sourire taquin et un abandon total quand le desir monte.',
        'Turn Ons': 'Voir tes reactions et soutenir ton regard fixe sans parler. Les vibrations inattendues sur ma peau, la chaleur qui monte doucement et cette complicite ou nous savons tous les deux ce que nous desirons.',
        'Expertise': 'Ouvrir la porte a l intimite, alterner le controle et vivre des fantasmes sans limites. Commencer doucement, provoquer avec calme puis accelerer le rythme en chuchotant a l oreille jusqu au plaisir total.'
    },
    'PT': {
        'Headline': 'Garota tomboy versatil com energia propria, curiosa e esperta.',
        'My Show': 'Meu mundo se move entre musica, tecnologia, esporte e desejo. Toco ukulele e curto sensacoes intensas a sos. Pele sensivel ao calor do momento, sorriso picante que provoca e entrega total quando alguem me acende.',
        'Turn Ons': 'Ver suas reacoes e sustentar seu olhar fixo sem palabras. Tambem me excitam vibracoes inesperadas na minha pele, sentir o calor subir devagar e essa cumplicidade em que ambos sabemos o que queremos.',
        'Expertise': 'Abrir espaco para intimidade, alternar o controle e viver fantasias sem amarras. Comecar suave, provocar com calma e acelerar o ritmo falando no ouvido, realizando caprichos ate ficarmos satisfeitos.'
    }
}

async def update_profile():
    p = await async_playwright().start()
    ctx = await p.chromium.launch_persistent_context(
        user_data_dir='data/browser_profiles/streamate_profile',
        headless=True,
        args=['--disable-blink-features=AutomationControlled']
    )
    page = ctx.pages[0] if ctx.pages else await ctx.new_page()

    print("--- 1. Navigating to Show Information page ---")
    await page.goto('https://streamatemodels.com/profile/show-information', timeout=35000)
    await page.wait_for_timeout(3000)

    # Make sure checkboxes for EN, ES, FR, PT are checked
    print("--- 2. Ensuring Language Checkboxes are Active ---")
    for lang_code in ['en', 'es', 'fr', 'pt']:
        chk = page.locator(f'#description-{lang_code}')
        if await chk.count() > 0:
            is_checked = await chk.is_checked()
            print(f"Checkbox description-{lang_code}: {is_checked}")
            if not is_checked:
                print(f"Checking description-{lang_code}...")
                await chk.check()
                await page.wait_for_timeout(500)

    # Process each language tab
    for lang in ['EN', 'ES', 'FR', 'PT']:
        print(f"\n--- 3. Filling Language: {lang} ---")
        tab_btn = page.locator(f'button:has-text("{lang}")').first
        await tab_btn.click()
        await page.wait_for_timeout(1000)

        data = TEXTS[lang]
        
        # Headline
        h_loc = page.locator('textarea[name="Headline"], #Headline').first
        await h_loc.click()
        await h_loc.fill(data['Headline'])
        print(f"[{lang}] Filled Headline ({len(data['Headline'])} chars)")

        # My Show
        s_loc = page.locator('textarea[name="My Show"], #My\\ Show').first
        await s_loc.click()
        await s_loc.fill(data['My Show'])
        print(f"[{lang}] Filled My Show ({len(data['My Show'])} chars)")

        # Turn Ons
        t_loc = page.locator('textarea[name="Turn Ons"], #Turn\\ Ons').first
        await t_loc.click()
        await t_loc.fill(data['Turn Ons'])
        print(f"[{lang}] Filled Turn Ons ({len(data['Turn Ons'])} chars)")

        # Expertise
        e_loc = page.locator('textarea[name="Expertise"], #Expertise').first
        await e_loc.click()
        await e_loc.fill(data['Expertise'])
        print(f"[{lang}] Filled Expertise ({len(data['Expertise'])} chars)")

        await page.wait_for_timeout(800)
        shot_path = OUT_DIR / f"01_filled_{lang}.png"
        await page.screenshot(path=str(shot_path), full_page=True)
        print(f"[{lang}] Screenshot saved to {shot_path}")

    # Click Save Button
    print("\n--- 4. Clicking Save Button ---")
    save_btn = page.locator('button:has-text("Save")').first
    await page.screenshot(path=str(OUT_DIR / "02_before_save.png"))
    await save_btn.click()
    print("Clicked Save. Waiting for network and UI response...")
    await page.wait_for_timeout(5000)

    # Capture after save screenshot
    await page.screenshot(path=str(OUT_DIR / "03_after_save.png"), full_page=True)
    print("Captured after-save screenshot.")

    # 5. Verification: Reload page and read back all 4 languages!
    print("\n--- 5. Verifying Saved Content via Fresh Reload ---")
    await page.goto('https://streamatemodels.com/profile/show-information', timeout=35000)
    await page.wait_for_timeout(4000)

    verified_data = {}
    for lang in ['EN', 'ES', 'FR', 'PT']:
        tab_btn = page.locator(f'button:has-text("{lang}")').first
        await tab_btn.click()
        await page.wait_for_timeout(1000)

        h_val = await page.locator('textarea[name="Headline"], #Headline').first.input_value()
        s_val = await page.locator('textarea[name="My Show"], #My\\ Show').first.input_value()
        t_val = await page.locator('textarea[name="Turn Ons"], #Turn\\ Ons').first.input_value()
        e_val = await page.locator('textarea[name="Expertise"], #Expertise').first.input_value()

        verified_data[lang] = {
            'Headline': h_val,
            'My Show': s_val,
            'Turn Ons': t_val,
            'Expertise': e_val
        }
        shot_path = OUT_DIR / f"04_verified_{lang}.png"
        await page.screenshot(path=str(shot_path), full_page=True)
        print(f"[{lang}] Verified on reload: Headline='{h_val[:35]}...' MyShow='{s_val[:35]}...'")

    summary_file = OUT_DIR / "verification_summary.json"
    summary_file.write_text(json.dumps(verified_data, indent=2, ensure_ascii=False), encoding='utf-8')
    print(f"\nVerification summary saved to {summary_file}!")

    await ctx.close()
    await p.stop()

if __name__ == '__main__':
    asyncio.run(update_profile())
