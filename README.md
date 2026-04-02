# 🚀 SuiteCRM Automation (Excel & Word IA)

> **Compatible con SuiteCRM v7.11.10**

Este proyecto automatiza la carga de registros de tiempos en SuiteCRM mediante dos vías: una tradicional vía Excel y una avanzada usando Inteligencia Artificial para procesar reportes en formato Word.

---

## 📂 Estructura del Proyecto

1.  **`suite_excel/`**: Carga mediante archivo Excel estructurado (`registry.xlsx`).
2.  **`suite_ia/`**: Carga mediante Word (`registry.docx`) procesado por OpenAI.
3.  **`core/automation.py`**: Motor compartido de automatización (Playwright).
4.  **`core/selectors.py`**: Selectores CSS del CRM centralizados (ver sección más abajo).
5.  **`main.py`**: Punto de entrada unificado con CLI.

---

## 📦 Instalación (Paso a Paso)

Este proyecto utiliza **`uv`**, que es el gestor de paquetes más rápido para Python. Sigue las instrucciones según tu sistema operativo:

### 1. Instalar `uv`
*   **Windows (PowerShell):**
    ```powershell
    powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
    ```
*   **macOS / Linux:**
    ```bash
    curl -LsSf https://astral.sh/uv/install.sh | sh
    ```
*   **Manjaro (Pacman):**
    ```bash
    sudo pacman -S uv
    ```

### 2. Preparar el entorno
Clona el repositorio, entra en la carpeta y ejecuta:
```bash
uv sync
```

### 3. Instalar Navegadores (Playwright)
#### 🖥️ En Windows / macOS
Solo ejecuta:
```bash
uv run playwright install
```

#### 🐧 En Manjaro / Arch Linux (Instalación específica)
Debido a las dependencias de sistema de los navegadores en Arch/Manjaro, es necesario instalar las librerías necesarias antes de ejecutar Playwright. Ejecuta este comando (todo en uno):

```bash
sudo pacman -S --needed nss atk at-spi2-core cups libxkbcommon libxcomposite libxdamage libxrandr libxfixes libxext libx11 mesa alsa-lib gtk3 pango cairo gdk-pixbuf2 libxcb libdrm libxshmfence libxrender libxi libxtst libxss dbus expat libffi libevent opus libwebp libjpeg-turbo libpng libtiff icu harfbuzz freetype2 fontconfig flite
```

Y luego:
```bash
uv run playwright install
```

---

## ⚙️ Configuración (.env)

Crea un archivo llamado `.env` en la raíz del proyecto con la siguiente estructura:

```env
CRM_URL=https://crm.metricsalad.com/suitecrm
CRM_USER=tu_usuario
CRM_PASSWORD=tu_password
OPENAI_API_KEY=tu_openai_key_aqui
```

---

## 🚀 Cómo ejecutar la carga

Todo se lanza desde `main.py` usando el flag `--source`:

### Opción A: Carga mediante Excel (Manual)
Ideal para tablas estructuradas.
1. Rellena el archivo `suite_excel/registry.xlsx`.
2. Ejecuta:
   ```bash
   uv run main.py --source excel
   ```

### Opción B: Carga mediante IA (Word)
Ideal para reportes narrativos de trabajo.
1. Escribe tu trabajo libremente en `suite_ia/registry.docx`.
   *   *Ejemplo: "Ayer estuve 3:15 horas en el proyecto BBVA corrigiendo fallos de login."*
2. Ejecuta:
   ```bash
   uv run main.py --source word
   ```
   *El script te mostrará los datos extraídos por la IA y te pedirá confirmación antes de subir.*

---

## 🧪 Flags opcionales

### `--dry-run` — Modo de prueba
Muestra los registros que se subirían **sin lanzar el navegador ni tocar el CRM**. Perfecto para verificar que los datos son correctos antes de ejecutar.
```bash
uv run main.py --source excel --dry-run
uv run main.py --source word --dry-run
```

### `--no-debug` — Carga directa sin pausa
Desactiva la pausa de depuración y sube los registros directamente sin esperar confirmación en el navegador.
```bash
uv run main.py --source excel --no-debug
```

---

## 📋 Historial de subidas (`upload_log.json`)
Cada registro subido con éxito queda registrado automáticamente en `upload_log.json` en la raíz del proyecto.

> ⚠️ **El archivo se crea solo cuando el script guarda automáticamente**, es decir, usando `--no-debug`. En modo debug el usuario guarda manualmente desde el navegador, por lo que el script no puede garantizar que el guardado se completó.

```json
[
  {
    "proyecto": "BBVA",
    "tarea_short": "Fix login bug",
    "fecha": "04/02/2025",
    "horas": 3.5,
    "uploaded_at": "2025-04-02T10:30:00.123456"
  }
]
```

---

## 🎯 Compatibilidad de selectores (`core/selectors.py`)

Todos los selectores CSS que usa Playwright para interactuar con el CRM están centralizados en **`core/selectors.py`**. Están probados y verificados con **SuiteCRM v7.11.10**.

Si actualizas SuiteCRM a una versión más nueva y algo deja de funcionar, **solo tienes que editar ese archivo** — no tocar ningún otro código.

```python
# Ejemplo: si cambia el ID del botón de login en una versión futura
LOGIN_BUTTON = "#bigbutton"  # <- cambiar aquí si falla
```

---

## 🧪 Notas de Depuración
Por defecto la **`pausa_debug`** está activada. El navegador se detendrá antes de guardar para que puedas verificar los datos. Haz clic en el botón "Resume" en el navegador para continuar. Usa `--no-debug` para saltarte esta pausa.

## 📝 Licencia

Este proyecto cuenta con licencia **ISC**.

---
*Desarrollado por [Fernando Garcia](https://github.com/sativonz)*
