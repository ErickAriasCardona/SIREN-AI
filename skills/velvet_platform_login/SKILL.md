---
name: velvet-platform-login
description: "Abre de forma automatizada y visual un navegador Chromium con Playwright para iniciar sesión en plataformas de creadoras (Stripchat, LoyalFans, Flirt4Free, Streamate) usando credenciales de usuario y persistiendo la sesión con cookies seguras."
---

# Skill: Automatización de Acceso a Plataformas (Playwright)

## Propósito
Permite al usuario o a los agentes de VELVET AI lanzar instancias de navegador en tiempo real, navegar a las plataformas de transmisión o contenido, autocompletar credenciales (correo y contraseña), interactuar con los botones de acceso y mantener las sesiones abiertas.

## Plataformas Soportadas
1. **Stripchat** (`stripchat`): Portal de inicio de sesión de Stripchat en español/global.
2. **LoyalFans** (`loyalfans`): Portal de creadora de LoyalFans.
3. **Flirt4Free** (`flirt4free`): Formulario de acceso de Flirt4Free.
4. **Streamate** (`streamate`): Portal de login de Streamate.

## Persistencia de Sesión y Superación de Cloudflare Turnstile
1. **Protección Anti-Detección**:
   - `ignore_default_args=["--enable-automation"]`: Elimina la barra y bandera de automatización de Chromium.
   - Script de inicialización stealth: Anula `navigator.webdriver`, simula objetos `window.chrome`, plugins y lenguajes de usuario real.
   - User-Agent alineado a Client Hints (`sec-ch-ua`).
2. **Detección Activa de Retos Cloudflare (`wait_for_cloudflare_resolution`)**:
   - Detecta retos de Cloudflare Turnstile e interstitials ("Just a moment...", "Verificando...", iframes de challenges).
   - Pausa la automatización e instruye al usuario a marcar la casilla ("Human-in-the-Loop") sin recargar bruscamente la página.
3. **Modo Asistido (Manual Booster)**:
   - Permite autenticarse manualmente mediante `python -m src.automation.manual_login_booster --platform stripchat` o el botón `🛡️ MODO ASISTIDO (CLOUDFLARE / 2FA)` en la interfaz gráfica.
   - Las cookies de sesión y tokens de autorización (`cf_clearance`) se guardan de forma permanente en `data/browser_profiles/{plataforma}_profile` y `data/sessions/{plataforma}_storage_state.json`.

