# 🚀 SuiteCRM Automation (Excel & Word IA)

Este proyecto automatiza la carga de registros de tiempos en SuiteCRM mediante dos vías: una tradicional vía Excel y una avanzada usando Inteligencia Artificial para procesar reportes en formato Word.

---

## 📂 Estructura del Proyecto

1.  **`suite_excel/`**: Carga mediante archivo Excel estructurado (`registry.xlsx`).
2.  **`suite_ia/`**: Carga mediante Word (`registry.docx`) procesado por OpenAI.
3.  **`core/`**: Motor compartido de automatización (Playwright).

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

### Opción A: Carga mediante Excel (Manual)
Ideal para tablas estructuradas.
1. Rellena el archivo `suite_excel/registry.xlsx`.
2. Ejecuta:
   ```bash
   uv run suite_excel/loader.py
   ```

### Opción B: Carga mediante IA (Word)
Ideal para reportes narrativos de trabajo.
1. Escribe tu trabajo libremente en `suite_ia/registry.docx`.
   *   *Ejemplo: "Ayer estuve 3:15 horas en el proyecto BBVA corrigiendo fallos de login."*
2. Ejecuta:
   ```bash
   uv run suite_ia/processor.py
   ```
   *El script te mostrará los datos extraídos por la IA y te pedirá confirmación antes de subir.*

---

## 🧪 Notas de Depuración
Por defecto, ambos scripts tienen activada la **`pausa_debug = True`**. El navegador se detendrá antes de guardar para que puedas verificar los datos. Haz clic en el botón "Resume" en el navegador para continuar.
