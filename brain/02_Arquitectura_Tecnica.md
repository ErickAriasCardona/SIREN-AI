# 🏛️ Arquitectura Técnica de VELVET AI

```
┌────────────────────────────────────────────────────────────────────────┐
│                   VELVET AI — SUPER-AGENT CORE                          │
│               (Orquestación con Google Antigravity SDK)                │
└───────────────────┬────────────────────────────────┬───────────────────┘
                    │                                │
     ┌──────────────┴──────────────┐  ┌──────────────┴──────────────┐
     ▼                             ▼  ▼                             ▼
┌────────────────────────┐ ┌────────────────────────┐ ┌────────────────────────┐
│   SUBAGENTE RADAR      │ │  SUBAGENTE COPILOTO    │ │    SUBAGENTE CRM       │
│  (Ranking & SEO WC)    │ │   (Chat & Persuasión)  │ │   (Memoria de Whales)  │
└───────────┬────────────┘ └───────────┬────────────┘ └───────────┬────────────┘
            │                          │                          │
            ▼                          ▼                          ▼
┌────────────────────────┐ ┌────────────────────────┐ ┌────────────────────────┐
│ Playwright Scraper     │ │ Antigravity Prompts    │ │ SQLite / Persistent    │
│ (Streamate Browser Engine│ LLM Persona Engine     │ Storage Engine           │
└────────────────────────┘ └────────────────────────┘ └────────────────────────┘
```

---

## 🛠️ Stack Tecnológico

1. **Orquestador de Agentes:** `google-antigravity` (SDK en Python).
   * Uso de herramientas personalizadas (`@tool`).
   * Activadores periódicos en segundo plano (`PeriodicTrigger`).
   * Multi-agentes y delegación jerárquica.
2. **Motor de Extracción y Navegación:** `playwright` (Python).
   * Automatización robusta de navegadores Chromium.
   * Auto-waiting y locators precisos para eludir elementos dinámicos complejos.
   * Scroll infinito inteligente y captura de metadatos.
3. **Almacenamiento y Persistencia:**
   * Base de datos local: SQLite / DuckDB para rankings históricos y CRM.
   * Sistema de archivos para artefactos y reportes.
4. **Interfaces de Notificación y Control:**
   * CLI interactiva del Super-Agente.
   * Bot de Telegram / Discord para alertas y control remoto en vivo.

---

## 🔗 Enlaces Relacionados
* [[00_Index_MOC|Volver al Índice]]
* [[Agentes/Velvet_SuperAgent|Super-Agente Velvet]]
* [[Modulos/01_Radar_Posicionamiento|Módulo Radar]]
