# 🧜‍♀️ SIREN AI — Live Streaming Intelligence & AI Copilot

> **by ALMA TECH**  
> **Plataforma Operativa Multi-Agente & Automatización Táctica para Transmisiones Webcam**  
> Diseñada para modelos y estudios webcam de alto rendimiento. Optimizada para **Sam Barton** y el ecosistema **Streamate**, **LoyalFans**, **Stripchat** y **Flirt4Free**.

---

## 🧭 ¿Qué es SIREN AI?

**SIREN AI** es la plataforma de copiloto táctico e inteligencia operativa en vivo para Sam Barton. Su objetivo es maximizar la facturación por hora, retener usuarios de alto ticket (VIPs), automatizar la sala de transmisión en menos de 3 segundos con **1-Click Injection** y mantener el ranking #1 en el feed algorítmico sin distracciones en cámara.

### 🌟 Módulos y Capacidades Clave:

1. **Centro de Comando en Vivo (`index.html`):**
   - Interfaz web ultra-fluida con diseño Glassmorphism Esmeralda.
   - Selector de perfil y plataformas (Streamate, LoyalFans, Stripchat, Flirt4Free).
   - Finanzas & Pagos con cálculo de split 100% y conciliación de cortes.
   - Posicionamiento & Radar Algorítmico (detección de cooldown y bump).
   - Consola de ejecución en tiempo real y catálogo de endpoints seguros `/api/v2`.

2. **Inyección Táctica 1-Click (StreamMonitor & SMConnect):**
   - Inyección simultánea en vivo en **Streamate SMConnect**, **LoyalFans Broadcast** y **StreamMonitor Desktop**.
   - **Room Topic dinámico:** Mensaje en inglés calibrado con hashtags de alto impacto (<= 130 caracteres).
   - **Menú Gold (Streamate):** Configuración automática de 6 ítems a 3 Gold validados contra el catálogo oficial de 109 opciones nativas.
   - **Ruleta Íntima (Streamate):** Selección de 10 opciones provocativas a 5 Gold.
   - **Metas de Sala LoyalFans (3 Niveles):**
     - Nivel 1 ($11): Reto o acción teaser inicial.
     - Nivel 2 ($22): Reto o acción intermedia intensa (1 minuto).
     - Nivel 3 ($33): Clímax y meta cumbre del show.
   - **8 Atajos Rápidos (Alt+1 a Alt+8) en StreamMonitor:**
     - `Alt+1` & `Alt+2`: Primera vez en sala (Nuevos).
     - `Alt+3` & `Alt+4`: Ya han entrado antes (Retorno).
     - `Alt+5` & `Alt+6`: Habituales / VIPs (Fidelización).
     - `Alt+7` & `Alt+8`: Llamado a la acción & Clímax a Privado.
   - **3 Disparadores Automáticos:** Saludo de sala (30s), Mensaje de entrada a privado y Agradecimiento coqueto por propinas Gold.
   - **Regla Estricta de Cumplimiento:** Cero emojis manuales en topics, macros ni disparadores.

3. **Ecosistema Multi-Agente de SIREN:**
   - **MAHIA:** Especialista en automatizaciones en vivo y co-piloto táctico de StreamMonitor. Genera y despacha el plan de turno en 1-Click.
   - **ROXANNE:** Copiloto de mensajería privada (DMs) multi-modelo (Ollama Local `qwen2.5:7b-instruct` 100% privado o Gemini Cloud). Protocolo estricto: 100% inglés saliente.
   - **CHLOE:** Diseñadora de contenido y guiones de historias para Instagram sin penalización algorítmica.
   - **DIANA:** Auditora forense de ingresos, historial de cobros y retenciones de tokens.
   - **ELECTRA:** Monitor de ranking algorítmico, visibilidad y ventanas óptimas de transmisión.

4. **Despliegue Satelital USB (`SIREN_USB`):**
   - Paquete plug-and-play para memorias USB (`CONECTAR_ESTUDIO.bat`).
   - Resuelve dinámicamente las rutas de Windows (`%APPDATA%`, `%USERPROFILE%`) en cualquier PC del estudio.
   - Inyecta perfiles y automatiza el cliente de StreamMonitor de forma aislada y segura.

---

## 🗂️ Estructura del Repositorio

```
SIREN-AI/
├── artifacts/              📊 Auditorías forenses, credenciales y reportes de endpoints
├── assets/                 🎨 Recursos visuales, modelos MediaPipe y binarios WASM
├── bin/                    🛠️ Binarios de soporte (Cloudflared, herramientas de red)
├── brain/                  🧠 Bóvedas de memoria contextual de Sam Barton
├── data/                   🗃️ Configuraciones de transmisión y persistencia JSON/SQLite
├── docs/                   📚 Manuales técnicos e ingeniería de algoritmos
├── index.html              🎛️ SIREN Command Dashboard v2.20.0 (by ALMA TECH)
├── iniciar_siren.bat       ⚡ Lanzador principal en Windows
├── iniciar_siren.py        🚀 Entrada Python del servidor local
├── requirements.txt        📦 Dependencias del entorno
├── scripts/                🔧 Scripts auxiliares y orquestadores
├── SIREN_USB/              💾 Automatización satelital para memoria USB
├── src/                    💻 Código fuente modular
│   ├── agents/             🤖 Copilotos IA (Roxanne, Chloe, Diana, Electra, Mahia)
│   ├── analytics/          🔬 Modelos de conversión y embudo
│   ├── automation/         🔐 Autenticación y puente CDP DevTools
│   ├── platforms/          🌐 Conectores (Streamate, LoyalFans, Stripchat, Flirt4Free)
│   └── server/             🚀 Servidor backend local (puerto 8888) con túnel seguro
└── sw.js                   ⚡ Service Worker PWA (alma-tech-v2.20.0)
```

---

## 🌿 Convención de Ramas (GitFlow)

* **`main`**: Rama protegida con la versión estable y auditada.
* **`develop`**: Rama activa de integración de características y ajustes.
* **`gh-pages`**: Rama de distribución para visualización y soporte web.

---

## 🚀 Puesta en Marcha

### 1. Iniciar el Servidor Local
Ejecuta el archivo por lotes en la raíz:
```cmd
iniciar_siren.bat
```
O directamente con Python:
```bash
python src/server/start_tunnel.py
```
El servidor quedará disponible en `http://localhost:8888`.

### 2. Dependencias de Python
```bash
pip install -r requirements.txt
```

---

## 🛡️ Seguridad y Cumplimiento

* **Zero-Touch Video:** SIREN AI no altera drivers de cámara ni decodificadores de video.
* **Protocolo de Privacidad:** Las credenciales y tokens nunca se envían a servidores de terceros no autorizados.
* **ALMA TECH Umbrella:** SIREN AI es una vertical tecnológica especializada desarrollada bajo los estándares de gobernanza y arquitectura de **ALMA TECH**.
