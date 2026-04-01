# 🚀 Automatización de carga de SuiteCRM

Este proyecto ofrece dos formas de automatizar la carga de registros de tiempos en SuiteCRM.

## 📂 Estructura del Proyecto

1.  **`suite_excel/`**: Carga tradicional mediante archivo Excel estructurado.
2.  **`suite_ia/`**: Carga avanzada mediante Word (IA).
3.  **`core/`**: Motor compartido de automatización con Playwright.

---

## 📊 1. Carga mediante Excel (Manual)

Ideal cuando ya tienes tus horas registradas en una tabla.

### 📁 Archivo
`suite_excel/registry.xlsx`

### 📋 Formato
| NOMBRE DEL PROYECTO | TAREA SHORT | TAREA LONG | HORAS | FECHA |
|-------------------|-------------|------------|-------|-------|
| CRM Gregal        | Bugfix      | Fix en login| 2     | 12/3/2026 |

### ▶️ Ejecución
```bash
uv run suite_excel/loader.py
```

---

## 🤖 2. Carga mediante IA (Word)

Ideal para escribir tu trabajo del día de forma libre y que la IA extraiga los datos automáticamente.

### 📁 Archivo
`suite_ia/registry.docx` (Puedes escribir párrafos libres allí).

### 🧪 Ejemplo de contenido del Word:
> "Hoy 12 de marzo estuve 3 horas en el proyecto BBVASPARK maquetando la home."

### ▶️ Ejecución
```bash
uv run suite_ia/processor.py
```

---

## ⚙️ Configuración (.env)

Asegúrate de tener tus credenciales en el archivo `.env`:

```env
CRM_URL=https://crm.metricsalad.com/suitecrm
CRM_USER=tu_usuario
CRM_PASSWORD=tu_password
OPENAI_API_KEY=tu_key_aqui
```

## 📦 Instalación

```bash
uv sync
uv run playwright install
```

## 🧪 Notas de Debug
Ambos scripts tienen activada la `pausa_debug = True` por defecto para que puedas verificar los datos en el navegador antes de que el script haga clic en "Guardar".
