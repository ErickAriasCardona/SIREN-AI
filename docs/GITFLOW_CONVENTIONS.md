# 🌿 Estrategia de Ramas GitFlow — VELVET AI

Esta guía documenta la convención oficial de ramas del repositorio **VELVET AI**:

---

## 1. Ramas Principales (Standing Branches)

### `main` (Producción Estable)
* **Propósito:** Contiene exclusivamente el código listo para producción, probado y verificado.
* **Protección:** No se realizan commits directos. Solo recibe fusiones (*merges*) validadas desde `develop` (para releases) o desde `hotfix/*` (para emergencias).
* **Tags:** Cada versión mayor o menor lleva su tag (ej: `v2.5.0`).

### `develop` (Desarrollo Continuo)
* **Propósito:** Es la rama central de integración. Todos los nuevos desarrollos convergen aquí antes de salir a producción.
* **Base para features:** Cualquier nueva característica se desprende a partir de `develop`.

---

## 2. Ramas de Trabajo (Supporting Branches)

### `feature/<nombre-funcionalidad>`
* **Propósito:** Desarrollo de nuevas capacidades, módulos o conectores de plataformas.
* **Origen:** Se crea a partir de `develop`.
* **Destino:** Se fusiona de vuelta a `develop` mediante Pull Request (PR) o merge.
* **Ejemplos:**
  * `feature/roxanne-copilot-multimodel`
  * `feature/streamate-private-cam-scraper`
  * `feature/flirt4free-vip-connector`

### `fix/<nombre-del-bug>` (o `bugfix/<nombre>`)
* **Propósito:** Corrección de defectos encontrados durante pruebas en `develop` antes de liberar una versión.
* **Origen:** Se crea a partir de `develop`.
* **Destino:** Se fusiona a `develop`.
* **Ejemplo:**
  * `fix/copilot-textarea-visibility`
  * `fix/api-catalog-unclosed-section`

### `hotfix/<nombre-del-parche>`
* **Propósito:** Solución inmediata para incidentes críticos detectados en producción (`main`).
* **Origen:** Se crea a partir de `main`.
* **Destino:** Se fusiona simultáneamente a **`main`** (generando un patch tag) y a **`develop`** (para no perder el arreglo).
* **Ejemplo:**
  * `hotfix/security-token-leak-prevention`
  * `hotfix/loyalfans-api-header-bypass`

---

## 3. Flujo Operativo Rápido (Cheat Sheet)

```bash
# Iniciar una nueva funcionalidad
git checkout develop
git pull origin develop
git checkout -b feature/nueva-funcionalidad

# Trabajar y hacer commits
git add .
git commit -m "feat: implementar nueva funcionalidad"

# Subir la rama al repositorio remoto
git push -u origin feature/nueva-funcionalidad

# Una vez probada, integrar a develop
git checkout develop
git pull origin develop
git merge feature/nueva-funcionalidad
git push origin develop
```
