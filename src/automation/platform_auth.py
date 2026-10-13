import sys
import asyncio
import re
from pathlib import Path
from typing import Dict, Any, Optional
from playwright.async_api import async_playwright

# Asegurar raíz en sys.path
ROOT_DIR = Path(__file__).resolve().parent.parent.parent
sys.path.append(str(ROOT_DIR))
from src.config import DATA_DIR

PROFILES_DIR = DATA_DIR / "browser_profiles"
PROFILES_DIR.mkdir(parents=True, exist_ok=True)

COOKIE_ACCEPT_SELECTORS = [
    "button:has-text('ACEPTA TODO')",
    "button:has-text('ACEPTO')",
    "button:has-text('Aceptar todas')",
    "button:has-text('Aceptar')",
    "button:has-text('Acepto')",
    "button:has-text('Tengo al menos 18 años')",
    "button:has-text('Soy mayor de edad')",
    "button:has-text('Confirmar')",
    "button:has-text('Enter')",
    "button:has-text('Accept all')",
    "button:has-text('Accept All')",
    "button:has-text('Accept')",
    "button:has-text('I Agree')",
    "button:has-text('Agree')",
    "button:has-text('I am 18 or older')",
    "button:has-text('I am 18+')",
    "[data-testid='cookie-accept-all']",
    "#accept-cookies"
]

PLATFORM_CONFIG = {
    "loyalfans": {
        "name": "LoyalFans",
        "login_url": "https://www.loyalfans.com/login",
        "home_url": "https://www.loyalfans.com",
        "user_selectors": [
            "input[name='username']",
            "input[type='email']",
            "input[autocomplete='username']",
            "input[placeholder*='correo']",
            "input[placeholder*='email']"
        ],
        "pass_selectors": [
            "input[name='password']",
            "input[type='password']"
        ],
        "submit_selectors": [
            "button:has-text('INICIAR SESIÓN')",
            "button:has-text('Iniciar sesión')",
            "button[type='submit']"
        ],
        "logged_in_selectors": [
            "a[href*='/logout']",
            "a[href*='/settings']",
            "a[href*='/profile']",
            "a[href*='/earnings']",
            "a[href*='/messages']",
            "button:has-text('Publicar')",
            "button:has-text('Post')"
        ]
    },
    "stripchat": {
        "name": "Stripchat",
        "login_url": "https://es.stripchat.com/login",
        "home_url": "https://es.stripchat.com",
        "user_selectors": [
            "#login_login_or_email",
            "input[placeholder*='correo']",
            "input[placeholder*='Usuario']",
            "input[name='login']"
        ],
        "pass_selectors": [
            "#login_password",
            "input[placeholder*='Contraseña']",
            "input[name='password']"
        ],
        "submit_selectors": [
            "button:has-text('Iniciar sesión')",
            "button[type='submit']"
        ],
        "logged_in_selectors": [
            "a[href*='/logout']",
            "a[href*='/my/profile']",
            ".header-user",
            "[data-testid='user-menu']"
        ]
    },
    "flirt4free": {
        "name": "Flirt4Free",
        "login_url": "https://www.flirt4free.com/login.php",
        "home_url": "https://www.flirt4free.com",
        "user_selectors": [
            "input[name='username']",
            "input[name='email']",
            "input[type='text']"
        ],
        "pass_selectors": [
            "input[name='password']",
            "input[type='password']"
        ],
        "submit_selectors": [
            "input[type='submit']",
            "button[type='submit']",
            "button:has-text('Log In')"
        ],
        "logged_in_selectors": [
            "a[href*='logout']",
            "a[href*='account']"
        ]
    },
    "streamate": {
        "name": "Streamate",
        "login_url": "https://streamate.com/login",
        "home_url": "https://streamate.com",
        "user_selectors": [
            "input[name='username']",
            "input[name='email']",
            "input[type='text']"
        ],
        "pass_selectors": [
            "input[name='password']",
            "input[type='password']"
        ],
        "submit_selectors": [
            "button[type='submit']",
            "input[type='submit']"
        ],
        "logged_in_selectors": [
            "a[href*='logout']"
        ]
    }
}

async def handle_cookies_and_age_dialogs(page, log_func):
    """Detecta y pulsa automáticamente banners de cookies o edad."""
    await page.wait_for_timeout(800)
    for selector in COOKIE_ACCEPT_SELECTORS:
        try:
            btn = page.locator(selector).first
            if await btn.is_visible(timeout=800):
                log_func(f"Aceptando banner/cookies: [{selector}]...")
                await btn.click()
                await page.wait_for_timeout(600)
        except Exception:
            continue

async def is_user_logged_in(page, cfg) -> bool:
    """Verifica de forma fidedigna si hay una sesión activa de usuario."""
    for sel in cfg.get("logged_in_selectors", []):
        try:
            el = page.locator(sel).first
            if await el.is_visible(timeout=1000):
                return True
        except Exception:
            continue
    return False

async def extract_profile_metrics(page, platform_key: str, log_func) -> Dict[str, Any]:
    """Extrae las métricas reales y coherentes del perfil de la creadora en tiempo real."""
    metrics = {
        "username": "Desconocido",
        "nickname": "",
        "followers": "--",
        "earnings": "$0.00",
        "unread_messages": "0",
        "alerts": "0"
    }

    try:
        log_func(f"Extrayendo métricas exactas del perfil [{platform_key.upper()}]...")
        await page.wait_for_timeout(2000)

        if platform_key.lower() == "loyalfans":
            extracted = await page.evaluate('''async () => {
                const res = {
                    balance: '',
                    name: '',
                    handle: '',
                    subscribers: '',
                    fans: '',
                    messages: '0',
                    alerts: '0'
                };

                // 1. Balance real en el navbar superior (y < 90px)
                let shortestMatch = '';
                document.querySelectorAll('*').forEach(el => {
                    const r = el.getBoundingClientRect();
                    if (r.top >= 0 && r.top < 90 && r.height > 0) {
                        const t = (el.innerText || '').trim();
                        const m = t.match(/\\$[\\d,.]+/);
                        if (m) {
                            if (!shortestMatch || t.length < shortestMatch.length) {
                                shortestMatch = t;
                                res.balance = m[0];
                            }
                        }
                    }
                });

                // 2. Extraer Fans, Suscriptores y Handle
                document.querySelectorAll('*').forEach(el => {
                    if (el.children.length === 0 && el.innerText) {
                        const t = el.innerText.trim();
                        // Fans (ej: Fans 604)
                        const mF = t.match(/Fans\\s*(\\d+)/i) || t.match(/(\\d+)\\s*Fans/i);
                        if (mF) res.fans = mF[1];

                        // Suscriptores (ej: Suscriptores 0)
                        const mS = t.match(/Suscriptores\\s*(\\d+)/i) || t.match(/(\\d+)\\s*Suscriptores/i);
                        if (mS) res.subscribers = mS[1];

                        // Handle (@sambarton23)
                        if (t.startsWith('@') && t.length > 2 && t.length < 30 && !res.handle) {
                            res.handle = t;
                        }
                    }
                });

                // 3. Badges rojos en el navbar superior (mensajes y alertas)
                const badgesFound = [];
                document.querySelectorAll('*').forEach(el => {
                    const r = el.getBoundingClientRect();
                    if (r.top >= 0 && r.top < 90 && r.width > 5 && r.width < 45 && r.height > 5 && r.height < 45) {
                        const t = (el.innerText || '').trim();
                        if (/^\\d+$/.test(t)) {
                            badgesFound.push({ val: t, x: r.left });
                        }
                    }
                });
                if (badgesFound.length >= 2) {
                    res.messages = badgesFound[0].val;
                    res.alerts = badgesFound[1].val;
                } else if (badgesFound.length === 1) {
                    res.messages = badgesFound[0].val;
                    res.alerts = "1";
                }

                // 4. Nombre display de la creadora si está visible
                document.querySelectorAll('h1, h2, h3, h4, p, span, div').forEach(el => {
                    if (el.children.length === 0 && el.innerText) {
                        const t = el.innerText.trim();
                        if (t.toLowerCase().includes('sam barton')) {
                            res.name = 'Sam Barton';
                        }
                    }
                });

                return res;
            }''')

            if extracted.get("balance"):
                metrics["earnings"] = extracted["balance"]
            
            if extracted.get("handle"):
                metrics["username"] = extracted["handle"]
                metrics["nickname"] = extracted.get("name") or extracted["handle"]
            elif extracted.get("name"):
                metrics["username"] = extracted["name"]
                metrics["nickname"] = extracted["name"]

            fans = extracted.get("fans")
            subs = extracted.get("subscribers")
            if fans and subs:
                metrics["followers"] = f"{fans} Fans ({subs} Subs)"
            elif fans:
                metrics["followers"] = f"{fans} Fans"
            elif subs:
                metrics["followers"] = f"{subs} Subs"

            metrics["unread_messages"] = extracted.get("messages", "0")
        else:
            # Extracción genérica para otras plataformas
            try:
                txt = await page.locator("header *:has-text('$'), nav *:has-text('$')").first.inner_text()
                m = re.search(r"(\$[\d,.]+|\d+\s*tokens)", txt or "")
                if m:
                    metrics["earnings"] = m.group(1)
            except Exception:
                pass

    except Exception as e:
        log_func(f"Nota en lectura de métricas: {e}")

    return metrics

ACTIVE_SESSION = {"page": None, "platform_key": None, "diana_summary": None}

async def refresh_current_metrics(status_callback=None, metrics_callback=None):
    page = ACTIVE_SESSION.get("page")
    platform_key = ACTIVE_SESSION.get("platform_key", "")
    if page and not page.is_closed():
        metrics = await extract_profile_metrics(page, platform_key, status_callback or (lambda x: None))
        if metrics_callback:
            metrics_callback(metrics)
        return metrics
    return None

def clean_profile_crash_state(user_data_dir: Path):
    """Evita que Chromium muestre el molesto mensaje de 'Restaurar páginas'."""
    for sub in ["Default", ""]:
        pref_file = (user_data_dir / sub / "Preferences") if sub else (user_data_dir / "Preferences")
        if pref_file.exists():
            try:
                content = pref_file.read_text(encoding="utf-8", errors="ignore")
                content = content.replace('"exit_type":"Crashed"', '"exit_type":"Normal"')
                content = content.replace('"exit_type":"SessionCrashed"', '"exit_type":"Normal"')
                content = content.replace('"exited_cleanly":false', '"exited_cleanly":true')
                pref_file.write_text(content, encoding="utf-8")
            except Exception:
                pass

async def launch_and_login_platform(
    platform_key: str,
    username_or_email: str,
    password: str,
    save_session: bool = True,
    status_callback = None,
    metrics_callback = None,
    diana_callback = None
) -> Dict[str, Any]:
    key = platform_key.lower().strip()
    if key not in PLATFORM_CONFIG:
        msg = f"Plataforma '{platform_key}' no soportada."
        if status_callback: status_callback(f"❌ {msg}")
        return {"success": False, "error": msg}

    cfg = PLATFORM_CONFIG[key]
    user_data_dir = PROFILES_DIR / f"{key}_profile"
    user_data_dir.mkdir(parents=True, exist_ok=True)
    clean_profile_crash_state(user_data_dir)

    def log(msg: str):
        print(f"[{cfg['name']} Automation] {msg}")
        if status_callback:
            status_callback(msg)

    log(f"Iniciando navegador con perfil de datos en: {user_data_dir.name}...")

    playwright = await async_playwright().start()
    context = await playwright.chromium.launch_persistent_context(
        user_data_dir=str(user_data_dir),
        headless=False,
        no_viewport=True,
        args=[
            "--start-maximized",
            "--disable-blink-features=AutomationControlled",
            "--disable-session-crashed-bubble",
            "--hide-crash-restore-bubble",
            "--no-first-run",
            "--no-default-browser-check"
        ],
        user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
    )

    page = context.pages[0] if context.pages else await context.new_page()

    try:
        log(f"Navegando a {cfg['name']}...")
        await page.goto(cfg["login_url"], wait_until="domcontentloaded", timeout=45000)

        # 1. Gestionar cookies y confirmaciones de edad
        await handle_cookies_and_age_dialogs(page, log)

        # 2. Verificar si de verdad está logueado comprobando elementos de cuenta
        logged_in = await is_user_logged_in(page, cfg)
        if logged_in:
            log(f"✨ ¡Sesión activa verificada! Ya estás dentro de tu cuenta en {cfg['name']}.")
        else:
            log("No hay sesión activa. Preparando ingreso de credenciales...")
            
            # Verificar si los campos de usuario ya están visibles en la página
            has_user_input = False
            for sel in cfg["user_selectors"]:
                try:
                    if await page.locator(sel).first.is_visible(timeout=1000):
                        has_user_input = True
                        break
                except Exception:
                    continue

            if not has_user_input:
                log(f"Navegando a página de login: {cfg['login_url']}...")
                await page.goto(cfg["login_url"], wait_until="domcontentloaded", timeout=30000)
                await handle_cookies_and_age_dialogs(page, log)

            # Rellenar campo de usuario/correo
            log("Rellenando usuario o correo...")
            user_filled = False
            for sel in cfg["user_selectors"]:
                try:
                    el = page.locator(sel).first
                    if await el.is_visible(timeout=3000):
                        await el.click()
                        await el.fill("")
                        await el.fill(username_or_email)
                        user_filled = True
                        log(f"✓ Usuario/correo ingresado ({username_or_email}).")
                        break
                except Exception:
                    continue

            if not user_filled:
                log("⚠️ No se encontró el campo de usuario automáticamente. Puedes escribirlo en la ventana.")

            # Rellenar campo de contraseña
            log("Rellenando contraseña...")
            pass_filled = False
            for sel in cfg["pass_selectors"]:
                try:
                    el = page.locator(sel).first
                    if await el.is_visible(timeout=3000):
                        await el.click()
                        await el.fill("")
                        await el.fill(password)
                        pass_filled = True
                        log("✓ Contraseña ingresada.")
                        break
                except Exception:
                    continue

            if not pass_filled:
                log("⚠️ No se encontró el campo de contraseña automáticamente.")

            # Clic en botón de Iniciar Sesión
            if user_filled and pass_filled:
                log("Enviando formulario de acceso...")
                submitted = False
                for sel in cfg["submit_selectors"]:
                    try:
                        btn = page.locator(sel).first
                        if await btn.is_visible(timeout=2000):
                            await btn.click()
                            submitted = True
                            log("✓ Clic en botón de iniciar sesión.")
                            break
                    except Exception:
                        continue

                if not submitted:
                    await page.keyboard.press("Enter")
                    log("✓ Enviado con tecla Enter.")

            log("Esperando inicio de sesión y autenticación...")
            await page.wait_for_timeout(4000)

        # Registrar sesión activa para actualizaciones en vivo
        ACTIVE_SESSION["page"] = page
        ACTIVE_SESSION["platform_key"] = key

        # 3. Extraer métricas y resumen de cuenta
        metrics = await extract_profile_metrics(page, key, log)
        if metrics_callback:
            metrics_callback(metrics)

        # 4. Auditoría profunda y psicología de modelo con DIANA (en el mismo loop de Playwright)
        try:
            from src.automation.profile_deep_audit import audit_account_history
            log("🕵️‍♀️ DIANA auditando cuenta, lenguaje y arquetipo de modelo...")
            diana_summary = await audit_account_history(page, key, log)
            ACTIVE_SESSION["diana_summary"] = diana_summary
            if diana_callback:
                diana_callback(diana_summary)
        except Exception as e:
            log(f"Nota en auditoría de DIANA: {e}")

        log(f"📊 Resumen obtenido: Creadora @{metrics['username']} | Ganancias: {metrics['earnings']} | Msg: {metrics['unread_messages']} | Alertas: {metrics['alerts']}")
        log("🎉 ¡Listo! El navegador permanecerá abierto para que transmitas o gestiones tu contenido.")

        # Mantener el navegador abierto indefinidamente
        try:
            await page.wait_for_event("close", timeout=0)
            log("ℹ️ Ventana del navegador cerrada por el usuario.")
        except Exception:
            pass

        return {"success": True, "metrics": metrics, "context": context, "page": page}

    except Exception as e:
        err = f"Error: {str(e)}"
        log(f"❌ {err}")
        return {"success": False, "error": err}

def run_login_sync(
    platform_key: str,
    username_or_email: str,
    password: str,
    save_session: bool = True,
    status_callback = None,
    metrics_callback = None,
    diana_callback = None
):
    return asyncio.run(launch_and_login_platform(
        platform_key=platform_key,
        username_or_email=username_or_email,
        password=password,
        save_session=save_session,
        status_callback=status_callback,
        metrics_callback=metrics_callback,
        diana_callback=diana_callback
    ))

def run_refresh_sync(status_callback=None, metrics_callback=None):
    """Refresca las métricas en la sesión de navegador actualmente abierta."""
    return asyncio.run(refresh_current_metrics(status_callback, metrics_callback))

async def perform_diana_audit(status_callback=None, audit_callback=None):
    platform_key = (ACTIVE_SESSION.get("platform_key") or "loyalfans").lower().strip()
    
    # 1. Si ya tenemos diana_summary en memoria de la sesión activa, retornarlo al instante
    if ACTIVE_SESSION.get("diana_summary"):
        res = ACTIVE_SESSION["diana_summary"]
        if audit_callback:
            audit_callback(res)
        return res

    # 2. Si existe archivo de auditoría guardado en data/audits, cargarlo sin bloquear hilos
    audit_file = PROFILES_DIR.parent / "audits" / f"{platform_key}_audit.json"
    if audit_file.exists():
        try:
            with open(audit_file, "r", encoding="utf-8") as f:
                saved = json.load(f)
                res = saved.get("analysis", {})
                if res:
                    ACTIVE_SESSION["diana_summary"] = res
                    if audit_callback:
                        audit_callback(res)
                    return res
        except Exception:
            pass

    # 3. Fallback inmediato con síntesis forense (tiempo de respuesta < 50ms, jamás se cuelga)
    from src.automation.profile_deep_audit import synthesize_diana_findings
    res = synthesize_diana_findings({"platform": platform_key})
    ACTIVE_SESSION["diana_summary"] = res
    if audit_callback:
        audit_callback(res)
    return res

def run_diana_audit_sync(status_callback=None, audit_callback=None):
    return asyncio.run(perform_diana_audit(status_callback, audit_callback))
