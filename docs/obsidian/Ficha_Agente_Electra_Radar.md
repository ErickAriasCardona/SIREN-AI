---
id: AGENTE-ELECTRA
tipo: FICHA_AGENTE
ecosistema: VELVET_AI
agente: ELECTRA
rol: Radar de Algoritmos, Scraping & Platform Intelligence
sdk: Google Antigravity SDK
version: 1.0.0
fecha_creacion: 2026-10-12
tags:
  - agente/electra
  - velvet-ai
  - scraping
  - radar
  - antigravity-sdk
---

# ⚡ ELECTRA — Radar de Algoritmos, Scraping & Platform Intelligence

> **Subagente Especialista de VELVET AI**  
> *Diseñada para auditar técnicamente las plataformas de creadoras, extraer datos mediante web scraping y desmantelar el funcionamiento de los algoritmos de recomendación.*

---

## 🎭 1. Identidad y Propósito

* **Nombre Clave:** ELECTRA
* **Título:** Arquitecta de Datos, Scraping y Radar de Algoritmos.
* **Supervisora:** VELVET (Super-Agente Orquestadora).
* **Filosofía:** *"No especulamos con la suerte de una modelo; operamos basados en datos, rankings escaneados y los algoritmos oficiales de cada plataforma."*

---

## 🛠️ 2. Herramientas Integradas en el SDK

ELECTRA está configurada en `src/agents/electra_agent.py` utilizando `google.antigravity.Agent` y `LocalAgentConfig`, con acceso a las siguientes herramientas Python nativas:

| Herramienta | Archivo Fuente | Acción Principal |
| :--- | :--- | :--- |
| `ejecutar_scraping_completo_loyalfans()` | [`src/tools/loyalfans_intel_tools.py`](file:///c:/Users/MI%20PC/Desktop/Sam/VELVET%20AI/src/tools/loyalfans_intel_tools.py) | Extrae en tiempo real la documentación oficial, guías y novedades de LoyalFans. |
| `consultar_inteligencia_loyalfans(seccion)` | [`src/tools/loyalfans_intel_tools.py`](file:///c:/Users/MI%20PC/Desktop/Sam/VELVET%20AI/src/tools/loyalfans_intel_tools.py) | Consulta rápida sobre facturación, herramientas, algoritmo o guías de LoyalFans. |
| `generar_plan_tactico_unificado_diana_electra(...)` | [`src/tools/loyalfans_intel_tools.py`](file:///c:/Users/MI%20PC/Desktop/Sam/VELVET%20AI/src/tools/loyalfans_intel_tools.py) | **Conexión Directa con DIANA**: Une la auditoría de cuenta histórica (Sam Barton / @sambarton23) con el algoritmo de LoyalFans. |
| `recomendar_estrategia_algoritmo(...)` | [`src/tools/loyalfans_intel_tools.py`](file:///c:/Users/MI%20PC/Desktop/Sam/VELVET%20AI/src/tools/loyalfans_intel_tools.py) | Genera un plan táctico de visibilidad y SEO interno para una modelo según su nicho. |
| `consultar_ranking_streamate(paginas)` | [`src/tools/scraper_tools.py`](file:///c:/Users/MI%20PC/Desktop/Sam/VELVET%20AI/src/tools/scraper_tools.py) | Rastrea con Playwright la grilla pública de Streamate e identifica el Top de modelos. |
| `buscar_posicion_modelo(username)` | [`src/tools/scraper_tools.py`](file:///c:/Users/MI%20PC/Desktop/Sam/VELVET%20AI/src/tools/scraper_tools.py) | Localiza en qué página y posición exacta (#) se encuentra una modelo en Streamate. |

---

## 💻 3. Ejecución y Uso

### Ejecución directa desde consola:
```powershell
python src/agents/electra_agent.py
```

### Invocación desde código Python:
```python
import asyncio
from src.agents.electra_agent import create_electra_agent

async def consultar():
    agent = create_electra_agent()
    async with agent as a:
        response = await a.chat("¿Cuál es la estrategia para posicionar a una modelo en el Explore Feed de LoyalFans?")
        async for chunk in response:
            print(chunk, end="")

asyncio.run(consultar())
```

---
*Volver al MOC:* [[_MOC_05_VELVET_PLATAFORMAS]] | *Ver Ficha LoyalFans:* [[LoyalFans_Full_Intelligence]]
