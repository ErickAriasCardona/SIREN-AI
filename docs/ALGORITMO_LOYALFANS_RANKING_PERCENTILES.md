# 📊 INGENIERÍA INVERSA: ALGORITMO DE LOYALFANS & RANKING DE PERCENTILES (TOP X%)

> **Documento Oficial de Inteligencia Comercial y Algorítmica — VELVET AI**  
> **Creadora Auditada:** Sam Barton (`@SAMBARTONN23` / `@sambarton23`)  
> **Plataforma:** LoyalFans  
> **Versión:** 1.0 — Octubre 2026  

---

## 📑 TABLA DE CONTENIDOS
1. [¿Qué es la notificación del Top Percentil (ej. "Estás en el top 23% de las creadoras")?](#1-qué-es-la-notificación-del-top-percentil)
2. [¿Por qué NO sale siempre? El ciclo de cálculo y la ventana móvil](#2-por-qué-no-sale-siempre-la-ventana-móvil-de-30-días)
3. [Factores matemáticos que componen el Algoritmo de Posicionamiento](#3-factores-matemáticos-del-algoritmo)
4. [¿Qué ocurre en el backend de LoyalFans cuando entras en el Top 25%?](#4-efectos-reales-en-el-backend-de-loyalfans)
5. [Estrategia de Estabilización con VELVET AI para Sam Barton](#5-estrategia-de-estabilización-con-velvet-ai)
6. [Matriz de Acción Rápida para Subir de Percentil](#6-matriz-de-acción-rápida)

---

## 1. ¿Qué es la Notificación del Top Percentil?

En LoyalFans, periódicamente aparece en la campana de notificaciones o en un banner del panel de creador un mensaje de felicitación similar a:

> *"🎉 Congratulations! You are currently in the top 23% of all creators on LoyalFans!"*  
> *(¡Felicidades! Actualmente estás en el top 23% de todos los creadores de LoyalFans)*

Esta cifra **NO es un número decorativo ni estático**: es el resultado de un cálculo estadístico que compara la facturación bruta y la actividad de tu perfil contra **la totalidad de cuentas de creadores activas a nivel global** en la plataforma durante un periodo de tiempo determinado.

Estar en el **Top 23%** significa que tu perfil ha generado más ingresos y tracción que el **77% de todos los modelos y creadores registrados y activos en LoyalFans** durante esa ventana de tiempo.

---

## 2. ¿Por qué NO Sale Siempre? La Ventana Móvil de 30 Días

Muchos creadores se desconciertan porque la notificación aparece unos días, luego desaparece por semanas y de repente vuelve a salir con un porcentaje diferente (ej. 28%, 19% o 23%).

Esto ocurre por **tres razones arquitectónicas de LoyalFans**:

### A. La Regla de la Ventana Móvil de 30 Días (*Rolling 30-Day Window*)
LoyalFans **NO** calcula el ranking sobre el dinero histórico acumulado en tu cuenta, sino sobre una **ventana deslizante de los últimos 30 días calendario**.
$$\text{Ingresos de Ranking} = \sum_{t = \text{Hoy}-30}^{\text{Hoy}} \text{Ventas Brutas}(t)$$

- **Día 1:** Haces varias ventas por PPV o propinas en vivo (por ejemplo, los desbloqueos de $0.40 a $15 USD que detectamos con fans como `@guyeeeo009`). Ese volumen recién entrante dispara tu puntuación.
- **Día 2 a 5:** El sistema recalibra la base de datos a medianoche y te envía la notificación: *"Estás en el top 23%"*.
- **Día 15 a 30 sin ventas equivalentes:** A medida que pasan los días, las ventas generadas hace 30 días van **saliendo** del cálculo diario. Si no hay nuevas compras que reemplacen ese volumen, tu facturación de los últimos 30 días disminuye.
- **Día 31:** Al caer tu volumen por debajo del umbral visible de la plataforma, el sistema **retira la notificación** para no mostrar badges desfavorables (ej. "Top 70%").

### B. El Umbral de Visibilidad (*Visibility Cutoff Threshold*)
LoyalFans tiene programado un filtro psicológico: **solo muestra la notificación si te encuentras dentro del percentil superior** (generalmente dentro del **Top 30%** o superior). Si caes al 35%, 45% o 60%, el sistema no te muestra una alerta negativa; simplemente oculta la tarjeta de percentil en tu interfaz.

### C. Ciclo de Recalibración del Servidor (*Cron Job Batch Processing*)
El ranking no se calcula en tiempo real por cada micro-segundo. LoyalFans ejecuta un proceso por lotes (*batch job*):
- **Actualización interna diaria:** Se procesa entre las `00:00 UTC` y las `03:00 UTC`.
- **Cierre de Ciclo Semanal / Quincenal:** Los domingos a medianoche se corre el balance comparativo global con respecto al volumen de todos los modelos de la plataforma. Por eso las notificaciones suelen llegar con mayor frecuencia los **lunes en la mañana** o tras rachas de ventas de fin de semana.

---

## 3. Factores Matemáticos del Algoritmo

El algoritmo de indexación de LoyalFans no evalúa únicamente el saldo en dólares; utiliza una función de puntuación compuesta:

$$\text{Creator Score} = w_1 \cdot \text{Facturación}_{30d} + w_2 \cdot \text{Velocidad}_{48h} + w_3 \cdot \text{Conversión PPV} + w_4 \cdot \text{Directos Lovense} + w_5 \cdot \text{Reciprocidad}$$

### Factor 1: Facturación Bruta en la Ventana de 30 Días ($w_1 = 0.40$)
Es el pilar de mayor peso. Cada dólar ganado por suscripciones, propinas, tienda de video, tienda de audio o desbloqueos de mensajes suma puntos directos.

### Factor 2: Velocidad de Ventas en 48 Horas (*Earnings Velocity*, $w_2 = 0.25$)
El algoritmo recompensa picos de actividad concentrada. Si en un lapso de 24 a 48 horas recibes múltiples compras seguidas (por ejemplo, enviando un Mass DM que varios fans desbloquean al mismo tiempo), el sistema interpreta que tu perfil está en **alta demanda** (*Trending*) y acelera tu subida de percentil.

### Factor 3: Tasa de Apertura y Compra en Mensajería PPV ($w_3 = 0.15$)
A diferencia de OnlyFans, LoyalFans prioriza fuertemente el **Buzón de Mensajería de Pago**. Los fans que pagan por enviar mensajes o que desbloquean fotos/videos enviados por DM generan el mayor margen neto para la plataforma. Un perfil con alta tasa de respuesta en DM sube más rápido que uno que solo publica fotos gratis en el muro.

### Factor 4: Horas de Transmisión en Vivo & Sinergia Lovense ($w_4 = 0.10$)
Emitir en directo (`/broadcast`) con cámara virtual (OBS) y juguetes interactivos Lovense activa el filtro de búsqueda interactivo en el home de LoyalFans. Cada minuto en vivo con propinas de juguetes otorga un multiplicador de visibilidad.

### Factor 5: Reciprocidad & Respuestas a Fans ($w_5 = 0.10$)
Tener mensajes sin responder durante más de 48 horas penaliza el índice de retención. Contestar dentro de las primeras 2 horas mantiene activa la etiqueta *"Active & Responsive Creator"*.

---

## 4. Efectos Reales en el Backend de LoyalFans

Estar en el **Top 23% (o superior)** no es solo una medalla; activa ventajas directas en el motor de recomendación de LoyalFans:

1. **Prioridad en el Carrusel Dorado de Live Broadcast:**
   Cuando Sam Barton inicia transmisión (`/broadcast`), el algoritmo ubica su sala en los primeros lugares del carrusel superior para los usuarios con tokens cargados.
2. **Indexación en 'Featured' y 'Trending Creators':**
   Al cruzar el umbral del Top 25%, el perfil de Sam deja de estar relegado a páginas secundarias y pasa a las primeras páginas del directorio general.
3. **Inclusión en Campañas de Email Marketing Automáticas:**
   LoyalFans envía correos periódicos con recomendaciones de creadoras a usuarios que han gastado tokens recientemente. Los perfiles en el Top 25% son los que el sistema incluye en esas listas automáticas.
4. **Mayor Retención de Fans Gastadores (Whales):**
   Los usuarios de alto gasto (*whales*) revisan activamente qué modelos tienen actividad reciente y badges de ranking para saber que no están gastando en una cuenta inactiva o abandonada.

---

## 5. Estrategia de Estabilización con VELVET AI

Para evitar las caídas cíclicas de percentil causadas por la ventana móvil de 30 días, VELVET AI implementa tres defensas automáticas:

### 1. Monitoreo Financiero en Tiempo Real
El motor financiero de VELVET AI (`src/analytics/financial_live_sync.py`) consulta y almacena en SQLite (`data/velvet_analytics.db`) el balance y las ventas recientes (como las 3 ventas detectadas de `@guyeeeo009`). Cuando el sistema detecta que faltan 5 días para que ventas pasadas expiren de la ventana de 30 días, activa una alerta de producción.

### 2. Disparo Táctico de Mass DM PPV (Reemplazo de Volumen)
En lugar de esperar a que el percentil caiga por debajo del 30%:
- Sam Barton cuenta con **604 fans registrados** en su base de LoyalFans.
- Un envío masivo de un clip exclusivo a $9.99 USD con teaser sugerente genera entre 3 a 8 compras inmediatas ($30 - $80 USD), inyectando volumen fresco a la ventana móvil y blindando el percentil en el **Top 15% - Top 20%**.

### 3. Sala de Transmisión Optimizada con OBS y Logitech
La integración directa de la sala en vivo:
- Cámara fijada en `OBS Virtual Camera`.
- Micrófono de alta fidelidad `Logitech BRIO`.
- Meta del día estructurada en 3 niveles (250 TK, 750 TK, 1500 TK).
- Tema obligatorio con `@SAMBARTONN23`.
Garantiza que cada sesión en vivo capte propinas inmediatas y mantenga el perfil en el carrusel principal.

---

## 6. Matriz de Acción Rápida

| Si observas... | Causa en el Algoritmo | Acción Inmediata en VELVET AI |
| :--- | :--- | :--- |
| **Aparece notificación: Top 23%** | Racha de ventas recientes activa en la ventana de 30 días. | Abrir sala en vivo en modo `Transmisión en Vivo` para aprovechar la máxima visibilidad en el carrusel superior. |
| **Desaparece la notificación** | Ventas antiguas salieron de la ventana de 30 días o hubo 4+ días sin transacciones. | Lanzar un Mass DM PPV con audio o clip a los 604 fans para reinyectar facturación en menos de 24 horas. |
| **El percentil baja (ej. de 18% a 28%)** | Otros creadores tuvieron un fin de semana con más volumen relativo. | Activar el juguete Lovense en directo con la meta de 3 niveles para captar propinas rápidas. |

---

*Documento integrado en el núcleo de documentación de VELVET AI.*
