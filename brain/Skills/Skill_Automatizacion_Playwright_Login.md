# ⚡ Skill: Automatización de Login Multi-Plataforma con Playwright

> **Implementación:** `src/automation/platform_auth.py` & `src/ui/app.py`  
> **Skill Spec:** `skills/velvet_platform_login/SKILL.md`

---

## 🎯 ¿Qué hace esta Skill?
Permite el acceso visual asistido a los portales de creadora de las 4 plataformas soportadas (**Stripchat**, **LoyalFans**, **Flirt4Free** y **Streamate**):

1. **Lanzamiento visual (`headless=False`):** El navegador Chromium se abre en la pantalla del usuario.
2. **Navegación inteligente:** Detecta automáticamente las URLs de acceso correctas.
3. **Autocompletado con Playwright:** Localiza los campos de usuario/correo y contraseña usando locators dinámicos por si cambian de nombre.
4. **Envío del formulario:** Realiza clic en el botón de acceso.
5. **Extracción y Dashboard en Vivo (Post-Login):**
   * Extrae nombre de usuario y nickname.
   * Ganancias acumuladas / balance.
   * Cantidad de seguidores / fans.
   * Mensajes sin leer (DMs).
   * Alertas y notificaciones activas.
6. **Persistencia de sesión y credenciales:**
   * Guarda de forma local y cifrada/ofuscada las credenciales en `data/credentials.json`.
   * Al seleccionar cualquier plataforma en el desplegable, los campos de usuario y contraseña se autocompletan instantáneamente.
   * Guarda las cookies de la sesión en `data/browser_profiles/` para evitar re-inicios de sesión innecesarios.

---

## 🖥️ Interfaz de Escritorio
Se provee una app gráfica en **CustomTkinter** ejecutable directamente con:
* `iniciar_velvet.bat` (Doble clic en Windows)
* o `python iniciar_velvet.py`

---

## 🔗 Enlaces Relacionados
* [[00_Index_MOC|Volver al Índice]]
* [[Plataformas/Stripchat|Plataforma Stripchat]]
* [[Plataformas/LoyalFans|Plataforma LoyalFans]]
* [[Plataformas/Flirt4Free|Plataforma Flirt4Free]]
