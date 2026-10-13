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

## Persistencia de Sesión
El sistema almacena el estado de almacenamiento (`storage_state`) en `data/sessions/{plataforma}_session.json`. En ejecuciones posteriores, el navegador recupera las cookies de sesión válidas para saltarse la necesidad de introducir contraseñas o resolver comprobaciones de inicio repetitivas.
