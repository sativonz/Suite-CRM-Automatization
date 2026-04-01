from dotenv import load_dotenv
import os
import json
import sys
from openai import OpenAI
from docx import Document

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.automation import exec_auto_load

load_dotenv()

client = OpenAI()

def limpiar_json(content):
    content = content.strip()
    if content.startswith("```"):
        content = content.replace("```json", "")
        content = content.replace("```", "")
    return content.strip()


def extraer_datos_multiples(texto):
    """
    Usa OpenAI para extraer una lista de registros a partir de un texto libre.
    """
    prompt = f"""
Extrae los datos del siguiente texto y devuélvelos como una LISTA de objetos JSON.

REGLAS DE PROCESAMIENTO:
1. **HORAS**: Convierte siempre a formato decimal (ej: 2:30 -> 2.5).
2. **FECHA**: Devuelve siempre en formato DD/MM/YYYY.
3. **TAREA_SHORT**: Crea un título técnico muy breve (ej: "Integración API", "Maquetación Home").
4. **TAREA_LONG**: Redacta una descripción PROFESIONAL y TÉCNICA. 
   - Elimina muletillas ("Menudo jaleo", "Hice esto...").
   - Elimina referencias a tiempos o fechas ("Ayer", "Estuve 3 horas...").
   - Usa un tono impersonal (ej: "Implementación de...", "Corrección de errores...").
   - Que sea concisa pero técnica.
5. **PROYECTO**: Nombre del proyecto.

Cada objeto debe tener este formato EXACTO:
{{
  "proyecto": "string",
  "tarea_short": "string",
  "tarea_long": "string",
  "horas": number,
  "fecha": "DD/MM/YYYY"
}}

Devuelve SOLO un array JSON válido.

Texto a procesar:
\"\"\"{texto}\"\"\"
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "Eres un asistente experto en extraer datos estructurados de reportes de trabajo."},
            {"role": "user", "content": prompt}
        ],
        temperature=0
    )

    content = response.choices[0].message.content
    print("RAW GPT RESPONSE:", content)

    content = limpiar_json(content)
    
    try:
        return json.loads(content)
    except json.JSONDecodeError:
        print("ERROR: No se pudo decodificar el JSON de la respuesta.")
        return []


def leer_word(ruta):
    """
    Lee todos los párrafos de un archivo .docx y los une en un solo texto.
    """
    if not os.path.exists(ruta):
        raise FileNotFoundError(f"No se encontró el archivo: {ruta}")
    
    doc = Document(ruta)
    texto = "\n".join([p.text for p in doc.paragraphs if p.text.strip()])
    return texto


def main():
    ruta_word = "suite_ia/registry.docx"
    
    print(f"--- Leyendo archivo Word: {ruta_word} ---")
    texto_completo = leer_word(ruta_word)
    
    print("\n--- Procesando con IA ---")
    registros = extraer_datos_multiples(texto_completo)
    
    print("\n--- REGISTROS EXTRAÍDOS ---")
    print(json.dumps(registros, indent=2, ensure_ascii=False))

    if not registros:
        print("No se extrajeron registros. Abortando.")
        return

    print("\n¿Deseas subir estos datos a SuiteCRM? (s/n)")
    respuesta = input().lower()
    
    if respuesta == 's':
        exec_auto_load(
            registros=registros,
            headless=False,
            pausa_debug=True,  
        )
    else:
        print("Carga cancelada.")


if __name__ == "__main__":
    main()