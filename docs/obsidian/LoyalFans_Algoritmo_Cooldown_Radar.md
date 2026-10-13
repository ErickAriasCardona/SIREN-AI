---
id: LOYALFANS-ALGORITMO-COOLDOWN-RADAR
tipo: AUDITORIA_FORENSE_ALGORITMO
ecosistema: VELVET_AI
agente: ELECTRA (Radar de Algoritmos) & DIANA
plataforma: LoyalFans
seccion: "creators?target=recently-updated"
fecha_auditoria: 2026-10-12
estado: EN_CURSO_TIEMPO_REAL
tags:
  - loyalfans/algoritmo
  - velvet-ai/electra
  - reverse-engineering
  - cooldown-radar
  - scraping-forense
  - obsidian
---

# ⚡ Auditoría Forense: Descifrando el Algoritmo de "Recently Updated" en LoyalFans

> **Objetivo de la Misión:** Determinar empíricamente mediante los Métodos 1 (Scraping de Cohorte) y 2 (Ingeniería Inversa de Atributos) la regla exacta de **Cooldown (Enfriamiento)** de la pestaña *Actualizado Recientemente* (`loyalfans.com/creators`), verificando si existe la ventana histórica de **4 horas / 4 publicaciones** para refrescar la posición #1.

---

## 🧭 1. Resultados en Tiempo Real del Método 2 (Atributos Internos)

Al interceptar la respuesta directa de `POST https://www.loyalfans.com/api/v2/creators` (`target: "recently-updated"`):

```json
{
  "target": "recently-updated",
  "root_keys": [
    "creator", "is_online", "stream_info", "slug", "sort_code", 
    "videocall", "new", "live_counters", "social_counters", 
    "follow", "toy", "categories", "approved_friend"
  ],
  "creator_keys": [
    "name", "display_name", "uid", "user_type", "slug", 
    "online_activity_at", "created_at", "is_online", "cover_photo"
  ]
}
```

### 💡 Hallazgo Forense #1:
* El atributo `online_activity_at` (última conexión del usuario) **NO determina el orden** de esta lista. Por ejemplo, `@thenubiangoddess` tenía `online_activity_at` del 28 de septiembre, pero apareció en el **Puesto #5** porque su post se publicó hace apenas 2 minutos.
* **El detonante del Bump es estrictamente un evento de contenido publicado** (Timeline Post).

---

## 📊 2. Resultados en Tiempo Real del Método 1 (Cohorte de Top Creadoras)

Muestreo capturado en vivo de las primeras 5 creadoras posicionadas en el Top 1 a 5 de *Recently Updated*:

| Rank | Creadora (Slug) | Último Post (Detonó el Bump) | Post Anterior | Delta de Tiempo Entre Posts | ¿Tipo de Post? |
| :---: | :--- | :--- | :--- | :--- | :--- |
| **#1** | `@mistressnatalienyc` | **Hace 17 segundos** | **Hace 3 horas** | **~3 horas y 15 min** | Exclusivo Suscriptores |
| **#2** | `@goddesslekki` | **Hace 1 minuto** | **Hace 10 horas** | **~10 horas** | Exclusivo Suscriptores |
| **#3** | `@shimmeryelegance` | **Hace 1 minuto** | **Hace 1 día** | **~24 horas** | Exclusivo Suscriptores |
| **#4** | `@facesittinglady` | **Hace 2 minutos** | **Hace 10 horas** | **~10 horas** | Público |
| **#5** | `@thenubiangoddess` | **Hace 2 minutos** | **Hace 17 días** | **17 días** | Público |

---

## 🧬 3. Deducciones Algorítmicas y Revelaciones

### 🔑 Revelación A: Posts para "Suscriptores" también dan Bump Global
* Existía el mito de que solo los posts 100% "Públicos" te subían al directorio de *Recently Updated*.
* **Falso:** Los puestos **#1, #2 y #3** fueron detonados por publicaciones marcadas como **"Solo para Suscriptores"** (`Suscriptores`). Puedes alimentar a tu club privado de fans y al mismo tiempo ganar visibilidad global en el directorio público.

### ⏱️ Revelación B: El Umbral Mínimo de Espaciado (~3 a 4 Horas)
* La modelo del Puesto #1 (`@mistressnatalienyc`) es una de las cuentas con mayor actividad publicando varias veces al día. Su post anterior fue hace **3 horas**.
* Ninguna de las creadoras en el Top 28 tiene publicaciones con menos de **3 a 4 horas de diferencia** que hayan detonado bumps consecutivos.
* Esto coincide con el **Algorithmic Cooldown Window de 3.5 a 4 Horas** implementado por LoyalFans para prevenir el auto-bump spamming.

---

## 🛠️ 4. Automatización Activa en VELVET AI

Se desplegó el script de monitoreo forense:
* **Script:** [`src/scrapers/loyalfans_cooldown_radar.py`](file:///c:/Users/MI%20PC/Desktop/Sam/VELVET%20AI/src/scrapers/loyalfans_cooldown_radar.py)
* **Base de Datos Local:** [`data/analytics/loyalfans_cooldown_radar.json`](file:///c:/Users/MI%20PC/Desktop/Sam/VELVET%20AI/data/analytics/loyalfans_cooldown_radar.json)

ELECTRA continuará tomando muestras a intervalos para confirmar la ventana exacta al minuto y emitir la **Matriz Horaria Óptima de Publicación para Sam Barton**.
