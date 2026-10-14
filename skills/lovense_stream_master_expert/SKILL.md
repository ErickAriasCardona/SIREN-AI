---
name: lovense-stream-master-expert
description: "Guía maestra del ecosistema Lovense (Stream Master, Lovense Connect, Lovense OBS, Cam Extension y API local). Cubre configuración de juguetes, emparejamiento BLE, gestión de propinas interactivas, integración multi-plataforma (Stripchat, LoyalFans) y matriz de respuesta personalizada para Sam Barton."
---

# 💖 Lovense & Stream Master — Manual Maestro de Operación y Automatización

## 1. ¿Qué es Lovense y su Ecosistema?
Lovense es el estándar de la industria cam y creadoras para juguetes interactivos de estimulación sincronizados en vivo con las propinas (tips/tokens) de los usuarios en plataformas como **Stripchat**, **Chaturbate**, **BongaCams**, **Cam4** y plataformas de suscripción como **LoyalFans**.

### Componentes del Ecosistema:
1. **Juguetes (Hardware)**:
   - **Lush (1/2/3)**: Huevo vibrador interno con cola ergonómica (el más popular en shows).
   - **Nora**: Vibrador dual con cabezal rotatorio para punto G y estimulador clitoral.
   - **Domi (1/2)**: Varita mágica (wand) de alta potencia para estimulación externa.
   - **Ferri / Dolce**: Estimuladores de bragas magnéticos y discretos.
   - **Hush (1/2) / Edge (1/2)**: Plugs anales y estimuladores de próstata con vibración profunda.
   - **Max (1/2)**: Masturbador masculino con bomba de aire y contracción interactiva.
   - **Sol / Ridge**: Estimuladores de pezones y corporales.
   - **Máquinas sexuales**: F1, Fortuna y brazos mecánicos sincronizados.

2. **Métodos de Conexión a la PC**:
   - **Lovense USB Bluetooth Dongle (v1 / v2 / v3)**: Conexión BLE directa entre el juguete y la PC (más estable, sin latencia, sin depender del teléfono).
   - **Lovense Connect App**: Aplicación para smartphone (iOS/Android) o Windows que conecta los juguetes por Bluetooth y expone un servidor local en red (puerto `20010` o `30010`) mediante código QR.
   - **Lovense Remote**: App de control a distancia 1 a 1 para videollamadas privadas y sesiones VIP.

3. **Lovense Stream Master**:
   - Suite todo-en-uno desarrollada por Lovense que une:
     - **Lovense Browser** (`chrome.exe` con perfil dedicado): Navegador con la extensión `lovense_cam` preinstalada.
     - **Lovense OBS** (`lvs_obs64.exe`): Fork especializado de OBS Studio con plugins de belleza, multicasting (transmitir a múltiples sitios a la vez) y widgets integrados.
     - **Tip Alert & Rules Engine**: Motor que escucha los tips de los chats y dispara los patrones de vibración correspondientes.
     - **Widgets en Pantalla**: Barra de metas (Tip Goal), juguete virtual animado (Toy Reaction), ruleta de premios (Spin the Wheel) y cartel de mejores propinadores (King of the Room).

---

## 2. Cómo Funciona Lovense Stream Master

### Arquitectura Técnica en Windows:
- **Ruta del Ejecutable**: `C:\Users\MI PC\AppData\Local\Lovense\Stream Master\LovenseBrowser\Browser\chrome.exe`
- **Directorio de Datos del Perfil**: `C:\Users\MI PC\AppData\Local\Lovense\Chromium`
- **Lovense OBS**: `C:\Users\MI PC\AppData\Local\Lovense\Stream Master\LovenseOBS\bin\64bit\lvs_obs64.exe`
- **Extensión Cam**: `C:\Users\MI PC\AppData\Local\Lovense\Stream Master\lovense_cam`

### Flujo de Transmisión Multi-Sitio:
1. **Lanzar Stream Master**: Inicia el navegador y el motor de eventos.
2. **Vincular Juguetes**:
   - Si se usa Dongle USB: El adaptador `Connect/bluetooth-adapter.exe` empareja el juguete automáticamente al encenderlo.
   - Si se usa móvil: Escanear el código QR que muestra Stream Master en pantalla desde la app móvil Lovense Connect.
3. **Iniciar Sesión en Plataformas**:
   - Dentro de Stream Master se abren las pestañas de **Stripchat** y las demás plataformas activas.
   - La extensión `lovense_cam` detecta la sala de Sam Barton y se sincroniza con el websocket del chat.
4. **Respuesta en Tiempo Real**:
   - Cuando un fan envía propinas en tokens, la extensión lee el evento, calcula el rango en la matriz de vibración y activa el juguete instantáneamente.

---

## 3. Matriz Estratégica de Propinas — Sam Barton
*(Alineada al arquetipo: Software/AI Architect, Biker Tomboy, Inteligente, Sensual y Dominante)*

Sam Barton no reacciona como una modelo genérica; sus respuestas tienen carácter, dinamismo y escalada emocional:

| Nivel | Rango de Tokens | Valor Aprox. (USD) | Nivel Juguete | Duración | Reacción de Sam Barton (Personalidad Tomboy) |
|---|---|---|---|---|---|
| **Tier 1** | 1 – 9 tk | $0.05 – $0.45 | Nivel 3 (Leve) | 2 seg | 😏 *"Hey... apenas encendiendo el motor. Se siente sutil pero curioso."* |
| **Tier 2** | 10 – 24 tk | $0.50 – $1.20 | Nivel 7 (Medio) | 4 seg | 🔥 *"Mmm, eso ya tiene mejor cadencia. Me gusta cuando no tienen miedo de subirle."* |
| **Tier 3** | 25 – 49 tk | $1.25 – $2.45 | Nivel 12 (Fuerte) | 6 seg | ⚡ *"Uff... vibración profunda. Código bien compilado, no te detengas."* |
| **Tier 4** | 50 – 99 tk | $2.50 – $4.95 | Nivel 16 (Intenso) | 9 seg | 🏍️ *"¡Santo cielo! Sacude con la fuerza de mi moto en carretera abierta... ¡mírame temblar!"* |
| **Tier 5** | 100 – 249 tk | $5.00 – $12.45 | Nivel 20 (Máximo) | 15 seg | 👑 *"¡AH! Nivel 20 continuo... Me tienes completamente bajo tu control. Bien ganado."* |
| **Tier 6** | 250+ tk | $12.50+ USD | Nivel 20 + Preset Wave | 30 seg | 🚗 *"¡LO LOGRASTE! Cada token va directo a mi carro de diciembre y Cancún. Eres mi consentido oficial."* |

---

## 4. API Local de Lovense para Automatización en VELVET AI

Lovense Connect y Stream Master exponen un servidor HTTP/Socket local en loopback:
- **Host**: `http://127.0.0.1:20010` (o `30010`)
- **HTTPS**: `https://127-0-0-1.lovense.club:30010`

### Endpoints Principales:
1. **Consultar Juguetes Conectados**:
   ```http
   GET http://127.0.0.1:20010/GetToys
   ```
   *Respuesta*:
   ```json
   {
     "code": 200,
     "type": "GetToys",
     "data": {
       "toys": {
         "lush_id": {"name": "lush", "status": 1, "battery": 92}
       }
     }
   }
   ```

2. **Enviar Vibración Manual**:
   ```http
   POST http://127.0.0.1:20010/Vibrate?v=15&t=5&toy=lush_id
   ```
   - `v`: Nivel de intensidad (0 a 20).
   - `t`: Tiempo en segundos.
   - `toy`: ID del juguete (opcional si hay uno solo).

3. **Rotación (Nora)**:
   ```http
   POST http://127.0.0.1:20010/Rotate?v=10&t=4
   ```

4. **Bomba de Aire / Contracción (Max / Edge)**:
   ```http
   POST http://127.0.0.1:20010/Air/Auto?v=2&t=5
   ```

5. **Patrones Especiales (Presets)**:
   ```http
   POST http://127.0.0.1:20010/Preset?name=pulse&t=10
   ```
   - Presets disponibles: `pulse`, `wave`, `fireworks`, `earthquake`.

---

## 5. Control desde VELVET AI

En VELVET AI puedes operar Lovense de tres formas:
1. **Desde la Interfaz Gráfica (`src/ui/app.py`)**:
   - Clic en el botón **`💖 Lovense Master`** en el panel superior. Abre Stream Master en segundo plano de inmediato.
2. **Desde el Módulo Python (`src/integrations/lovense_manager.py`)**:
   - `launch_stream_master()`: Lanza la aplicación.
   - `check_local_lovense_api()`: Diagnostica juguetes y batería.
   - `send_toy_command()`: Dispara estímulos automáticos según metas o eventos.
   - `get_sam_barton_tip_reaction(tokens)`: Devuelve la respuesta ideal para el chat.
3. **Credenciales Seguras**:
   - Almacenadas en `data/credentials.json` bajo la clave `"lovense"` (codificadas y protegidas por `.gitignore`).
