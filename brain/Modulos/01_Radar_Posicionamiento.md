# 📡 Módulo 1: Radar de Posicionamiento y Ranking

## 🎯 Objetivo
Monitorear de forma autónoma la posición de cualquier modelo en las listas públicas y categorías de **Streamate**, registrando variaciones en su ranking y notificando cambios críticos.

---

## 🔍 Datos que captura el Radar

Para cada modelo detectada en la grilla:
1. **Posición Global:** Número de página (1, 2, 3...) y posición absoluta (#1 a #N).
2. **Username / URL:** Enlace directo a la sala y nombre de usuario.
3. **Estado de Transmisión:**
   * En público (Free Chat).
   * En privado (Exclusive / Private).
   * En Gold Show / C2C.
4. **Metadatos Comerciales:**
   * Precio por minuto configurado.
   * Tags activos (ej. `#blonde`, `#latina`, `#fetish`, etc.).
   * Estado de la cámara (HD, audio, etc.).

---

## ⚡ Lógica de Detección

```
Playwright Navega -> Recorre páginas -> Auto-Scroll -> Extrae Cards de Streamers
                                                              │
                                                              ▼
Alertas (Telegram) <--- Compara con estado anterior <--- Guarda en BD SQLite
```

---

## 🔗 Enlaces Relacionados
* [[00_Index_MOC|Volver al Índice]]
* [[Agentes/Subagente_Radar|Subagente Radar]]
* [[Conocimiento_Industria/Algoritmo_Streamate_Ranking|Algoritmo de Streamate]]
