# 🌌 VELVET AI — Autonomous Intelligence & Operations Command Center

> **Ecosistema Autónomo de Inteligencia Artificial & Automatización para Creadoras y Estudios Webcam**  
> Potenciado por **Google Antigravity SDK**, **Playwright Stealth**, **Ollama Local (Qwen 2.5)** y **SQLite Analytics**.

---

## 🧭 ¿Qué es VELVET AI?

**VELVET AI** es una plataforma operativa multi-agente diseñada para maximizar el posicionamiento algorítmico, automatizar la interacción y retención de fans mediante copilotos de mensajería (DMs), y gestionar analítica forense 100% real en plataformas como **LoyalFans**, **Streamate**, **Stripchat** y **Flirt4Free**.

### 🌟 Módulos Principales:
1. **VELVET Command Center (`index.html`):** Panel de control interactivo con auditoría financiera en vivo, radar algorítmico de cooldown (bump cada 4h), matriz de pagos y consola de chat en tiempo real.
2. **ROXANNE DM Copilot (Multi-Modelo):** Copiloto de mensajería que opera con **Ollama Local (`qwen2.5:7b-instruct`)** 100% privado y gratuito, o con **Google Gemini Cloud**. Aplica el estricto protocolo de idioma (Inglés por defecto, Español solo si el fan escribe en español).
3. **ELECTRA Radar & Cooldown Monitor:** Auditoría de APIs internas de LoyalFans (`/api/v2/creators`) para detectar ventanas óptimas de actualización y asegurar la posición #1 en el feed.
4. **Data Science & Funnel Engine:** Base de datos relacional SQLite (`velvet_analytics.db`) que modela la tasa de lectura real (18%-25%) y la conversión de compra efectiva (3%-6%).
5. **SCARLETT & DIANA:** Agentes autónomos para despliegue controlado de biografías, menús y respuestas automáticas (7 triggers nativos verificados).
6. **Ingeniería del Algoritmo de LoyalFans:** Explicación técnica y matemática de la ventana móvil de 30 días (*rolling window*), ranking de percentiles (*Top X%*) y factores de posicionamiento. [Ver documentación completa en `docs/ALGORITMO_LOYALFANS_RANKING_PERCENTILES.md`](docs/ALGORITMO_LOYALFANS_RANKING_PERCENTILES.md).

---

## 🗂️ Estructura del Repositorio

```
VELVET-AI/
├── artifacts/              📊 Catálogos de APIs, auditorías de endpoints y reportes forenses
├── brain/                  🧠 Obsidian Vault (Mapas MOC, arquitectura técnica y agentes)
├── data/                   🗃️ Esquemas de analítica y configuraciones seguras
├── docs/                   📚 Documentación técnica e informes de investigación
├── skills/                 ⚡ Skills para Antigravity SDK y automatización con Playwright
├── src/                    💻 Código fuente
│   ├── agents/             🤖 Agentes de IA (ROXANNE Copilot, DIANA, ELECTRA, etc.)
│   ├── analytics/          🔬 Motor de ciencia de datos y pruebas de interfaz
│   ├── automation/         🔐 Autenticación sigilosa y auditoría profunda
│   ├── platforms/          🌐 Conectores por plataforma (LoyalFans, Streamate, Stripchat, Flirt4Free)
│   ├── scrapers/           🕷️ Scrapers Playwright para monitoreo algorítmico
│   ├── server/             🚀 Servidor local FastAPI / HTTP (puerto 8888) con CORS
│   ├── tools/              🛠️ Herramientas operativas
│   └── ui/                 🖥️ Interfaz complementaria
├── index.html              🎛️ VELVET Command & Intelligence Dashboard v2.5
├── iniciar_velvet.bat      ⚡ Script de arranque rápido en Windows
├── requirements.txt        📦 Dependencias de Python
└── .gitignore              🛡️ Reglas estrictas de seguridad y exclusión de secretos
```

---

## 🌿 Convención de Ramas (GitFlow)

Este repositorio sigue la estrategia estandarizada de **GitFlow**:

```
main (Producción estable)
  │
  └── develop (Integración y desarrollo activo)
        │
        ├── feature/funcionalidad  (Nuevas características, ej: feature/roxanne-copilot)
        ├── fix/nombre-del-bug     (Corrección de errores en develop)
        └── hotfix/parche-critico  (Parches de emergencia directos a main)
```

* **`main`**: Rama protegida que contiene las versiones estables y verificadas en producción.
* **`develop`**: Rama base para el desarrollo diario e integración de módulos.
* **`feature/<nombre>`**: Se desprende de `develop` para construir nuevas funcionalidades. Al finalizar, se fusiona de vuelta a `develop`.
* **`fix/<nombre>`**: Corrección de bugs detectados durante pruebas en `develop`.
* **`hotfix/<nombre>`**: Correcciones críticas urgentes que se aplican directamente sobre `main` y luego se propagan a `develop`.

---

## 🚀 Instalación y Puesta en Marcha

### 1. Clonar el repositorio
```bash
git clone https://github.com/ErickAriasCardona/VELVET-AI.git
cd VELVET-AI
```

### 2. Crear entorno virtual e instalar dependencias
```bash
python -m venv venv
# En Windows:
venv\Scripts\activate
# En Linux/macOS:
source venv/bin/activate

pip install -r requirements.txt
playwright install chromium
```

### 3. Configurar variables de entorno
Copia `.env.example` a `.env` y configura tus claves (opcional para modelos en la nube):
```bash
copy .env.example .env
```

### 4. Iniciar VELVET AI Command Center
Para iniciar el servidor local con soporte completo para ROXANNE y el dashboard:
```bash
python src/server/velvet_app_server.py
```
Abre tu navegador en: **`http://localhost:8888`**

> **Nota para inferencia local:** Si utilizas el modelo local Qwen 2.5, asegúrate de tener Ollama corriendo en `http://localhost:11434` con el modelo descargado: `ollama run qwen2.5:7b-instruct`.

---

## 🛡️ Seguridad y Privacidad

* Las credenciales, tokens JWT y perfiles de sesión del navegador (`browser_profiles/`) están estrictamente ignorados por `.gitignore` y **nunca** se suben al repositorio.
* Los datos financieros y de audiencia mostrados se basan 100% en auditorías reales de las plataformas (cero datos simulados o inventados).
