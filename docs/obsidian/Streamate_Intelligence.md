---
id: INTEL-STREAMATE
tipo: FICHA_PLATAFORMA
ecosistema: VELVET_AI
plataforma: Streamate
url_oficial: https://www.streamate.com
agente_auditor: ELECTRA
fecha_auditoria: 2026-10-12
tags:
  - plataforma/streamate
  - webcam
  - pvt
  - exclusive
  - scraping
  - ranking
---

# ⚡ Streamate — Auditoría de Algoritmo de Grilla, Monetización y Posicionamiento

> **Dossier de Inteligencia Técnica**  
> *Monitoreado y rastreado por el módulo de radar de grilla de **ELECTRA** (`src/scrapers/streamate_scraper.py`).*

---

## 📌 1. Visión General de Streamate

**Streamate** es una plataforma de webcam premium basada en cobro por minuto (Pay-Per-Minute). A diferencia de los sitios freemium de tokens (donde todo el chat público es explícito), en Streamate el chat gratuito está sujeto a reglas estrictas de censura y la monetización real ocurre al pasar a salas privadas.

> [!IMPORTANT] Dinámica de Salas en Streamate
> 1. **Free Chat:** Sala pública de atracción. No se permite desnudez explícita ni actos sexuales en público. El objetivo es seducir y convertir rápidamente a privado.
> 2. **Private Show (PVT):** El cliente paga por minuto. Otros usuarios pueden entrar a ver pagando también.
> 3. **Exclusive Show:** La sala se cierra únicamente para ese cliente. Es la tarifa más alta por minuto.
> 4. **Cam 2 Cam:** El cliente activa su cámara para interactuar con la modelo (recargo adicional).
> 5. **Gold Shows:** Shows grupales prepagos donde múltiples usuarios compran un ticket en oro (*Gold*) para ver un show explícito conjunto.

---

## 🧠 2. El Algoritmo de la Grilla (Placement Algorithm)

Streamate ordena a las modelos en una **grilla pública dinámica de páginas** (#1 a #50+). Aparecer en la **Página 1 o 2** garantiza un flujo constante de clientes de alto poder adquisitivo (*Whales*).

### Factores Determinantes del Algoritmo:
1. **Dólares por Hora Conectada ($/Hour / EPH):** Es la métrica reina del algoritmo. Si una modelo genera \$100 en 1 hora, el algoritmo la premiará mucho más que a una modelo que genera \$100 en 5 horas de chat libre.
2. **Ratio de Conversión a Privado:** Porcentaje de tiempo que la modelo pasa en estados privados (PVT/Exclusive) vs. tiempo estancada en Free Chat.
3. **Calificación de Clientes y Repetición:** Clientes recurrentes que vuelven a gastar en la misma sala incrementan el *score* de calidad.
4. **Tiempo de Inactividad Penalizado:** Estar conectada en Free Chat sin hablar o sin generar tráfico empuja el perfil hacia las páginas posteriores (#10+).

---

## 💵 3. Esquema Financiero y Facturación

- **Moneda:** Streamate Gold / USD.
- **Modelo de Cobro:** Por minuto en shows privados y propinas en Gold durante Free Chat.
- **Reparto de Ingresos (Split):** Típicamente entre 30% y 35% neto para la modelo si trabaja de forma independiente (la plataforma retiene el resto debido al alto costo de procesamiento de tarjetas y tráfico global). Si trabaja mediante estudio o master-account, los acuerdos de porcentaje varían.
- **Frecuencia de Pagos:** Semanal o quincenal según procesador.
- **Métodos:** Paxum, transferencia bancaria, cheque electrónico.

---

## 🛠️ 4. Herramientas de VELVET AI para Streamate

1. **Radar de Grilla y Posición en Tiempo Real:**  
   - Archivo: [`src/scrapers/streamate_scraper.py`](file:///c:/Users/MI%20PC/Desktop/Sam/VELVET%20AI/src/scrapers/streamate_scraper.py)
   - Funciones en ELECTRA: `consultar_ranking_streamate(paginas)` y `buscar_posicion_modelo(username, paginas_max)`.
   - Permite verificar si la modelo está en Página 1 o si cayó a páginas bajas, alertando para tomar acciones de choque.
2. **ROXANNE (Copiloto de Chat en Vivo):**  
   - Asiste durante la transmisión en Free Chat sugiriendo scripts de respuesta para desarmar "mirones gratuitos" y cerrar el paso a Privado o Exclusivo de inmediato.

---
*Volver al MOC:* [[_MOC_05_VELVET_PLATAFORMAS]] | *Ver Comparativa:* [[Matriz_Comparativa_Plataformas]]
