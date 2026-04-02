from playwright.sync_api import sync_playwright, expect
from datetime import datetime
import json
import os
from dotenv import load_dotenv
from core.selectors import (
    LOGIN_USER_INPUT, LOGIN_PASSWORD_INPUT, LOGIN_BUTTON, LOGIN_URL_FRAGMENT,
    PROJECT_FILTER_BUTTON, PROJECT_SEARCH_DIALOG, PROJECT_SEARCH_INPUT,
    PROJECT_SEARCH_SUBMIT, PROJECT_DETAIL_URL,
    TIMESHEET_SUBPANEL_TITLE, TIMESHEET_NEW_BUTTON,
    TIMESHEET_NAME_INPUT, TIMESHEET_DESCRIPTION,
    TIMESHEET_HOURS_INPUT, TIMESHEET_DATE_INPUT,
    TIMESHEET_SAVE_SELECTORS,
)

load_dotenv()

# Ruta al log persistente de subidas (raíz del proyecto)
UPLOAD_LOG_PATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "upload_log.json"
)


def save_upload_log(registro):
    """
    Añade una entrada al historial de registros subidos (upload_log.json).
    """
    entry = {
        "proyecto": registro["proyecto"],
        "tarea_short": registro["tarea_short"],
        "fecha": registro["fecha"],
        "horas": registro["horas"],
        "uploaded_at": datetime.now().isoformat()
    }

    logs = []
    if os.path.exists(UPLOAD_LOG_PATH):
        with open(UPLOAD_LOG_PATH, "r", encoding="utf-8") as f:
            try:
                logs = json.load(f)
            except json.JSONDecodeError:
                logs = []

    logs.append(entry)

    with open(UPLOAD_LOG_PATH, "w", encoding="utf-8") as f:
        json.dump(logs, f, indent=2, ensure_ascii=False)

    print(f"   📋 Log guardado en upload_log.json")

CRM_URL = os.getenv("CRM_URL", "https://crm.metricsalad.com/suitecrm")
CRM_USER = os.getenv("CRM_USER")
CRM_PASSWORD = os.getenv("CRM_PASSWORD")


def login(page):
    page.goto(f"{CRM_URL}/index.php?module=Users&action=Login")
    page.fill(LOGIN_USER_INPUT, CRM_USER)
    page.fill(LOGIN_PASSWORD_INPUT, CRM_PASSWORD)
    page.click(LOGIN_BUTTON)
    page.wait_for_load_state("networkidle")
    expect(page).not_to_have_url(LOGIN_URL_FRAGMENT)


def abrir_proyecto(page, nombre_proyecto):
    page.goto(f"{CRM_URL}/index.php?module=Project&action=index")
    page.wait_for_load_state("networkidle")

    page.locator(PROJECT_FILTER_BUTTON).click()
    expect(page.locator(PROJECT_SEARCH_DIALOG)).to_be_visible()

    input_search = page.locator(PROJECT_SEARCH_INPUT)
    expect(input_search).to_be_visible()
    input_search.fill(nombre_proyecto)

    page.locator(PROJECT_SEARCH_SUBMIT).click()
    page.wait_for_load_state("networkidle")

    # Hacer clic en el primer resultado que contenga el nombre (no exacto para evitar fallos de mayúsculas/espacios)
    resultado = page.get_by_role("link", name=nombre_proyecto, exact=False).first
    
    if resultado.count() == 0:
        raise RuntimeError(f"No se encontró ningún proyecto que coincida con '{nombre_proyecto}' en los resultados de búsqueda.")
    
    expect(resultado).to_be_visible(timeout=5000)
    resultado.click()

    page.wait_for_url(PROJECT_DETAIL_URL)
    page.wait_for_load_state("domcontentloaded")
    expect(page.locator(TIMESHEET_SUBPANEL_TITLE)).to_be_visible()


def abrir_quick_create_timesheet(page):
    subpanel = page.locator(TIMESHEET_SUBPANEL_TITLE)

    if subpanel.get_attribute("class") and "collapsed" in subpanel.get_attribute("class"):
        subpanel.click()

    nuevo_btn = page.locator(TIMESHEET_NEW_BUTTON)
    nuevo_btn.wait_for()

    nuevo_btn.scroll_into_view_if_needed()
    nuevo_btn.click(force=True)

    page.wait_for_selector(TIMESHEET_NAME_INPUT)
    page.wait_for_selector(TIMESHEET_DESCRIPTION)
    page.wait_for_selector(TIMESHEET_HOURS_INPUT)
    page.wait_for_selector(TIMESHEET_DATE_INPUT)


def horas_para_crm(horas):
    if isinstance(horas, (int, float)):
        return str(horas).replace(".", ",")
    return str(horas).strip()


def rellenar_formulario_timesheet(page, registro):
    page.fill(TIMESHEET_NAME_INPUT, registro["tarea_short"])
    page.fill(TIMESHEET_DESCRIPTION, registro["tarea_long"])
    page.fill(TIMESHEET_HOURS_INPUT, horas_para_crm(registro["horas"]))

    fecha_a_usar = registro["fecha"]
    fecha_input = page.locator(TIMESHEET_DATE_INPUT)
    fecha_input.fill("")
    fecha_input.fill(fecha_a_usar)

    valor_fecha = fecha_input.input_value()
    if valor_fecha != fecha_a_usar:
        print(f"ADVERTENCIA: La fecha no coincide perfectamente. Esperado: {fecha_a_usar} / Actual: {valor_fecha}")


def guardar_timesheet(page):
    for selector in TIMESHEET_SAVE_SELECTORS:
        locator = page.locator(selector)
        if locator.count() > 0 and locator.first.is_visible():
            locator.first.click()
            page.wait_for_load_state("networkidle")
            return

    raise RuntimeError("No se encontró botón de Guardar en el quick create")


def exec_auto_load(registros, headless=False, pausa_debug=False, dry_run=False):
    """
    Función unificada para subir una lista de registros al CRM.
    Si dry_run=True, solo muestra los registros sin lanzar el navegador.
    """
    if dry_run:
        print("\n🧪 MODO DRY-RUN — registros que se subirían:")
        for i, r in enumerate(registros, start=1):
            print(f"  [{i}] {r['proyecto']} | {r['tarea_short']} | {r['horas']}h | {r['fecha']}")
        return

    if not CRM_USER or not CRM_PASSWORD:
        raise ValueError("Faltan credenciales CRM en el archivo .env")

    if not registros:
        print("No hay registros para cargar.")
        return

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=headless)
        page = browser.new_page()
        page.set_default_timeout(15000)

        print("Iniciando sesión en SuiteCRM...")
        login(page)

        for i, registro in enumerate(registros, start=1):
            print(f"\n[{i}/{len(registros)}] Subiendo: {registro['proyecto']} - {registro['tarea_short']}")
            
            try:
                abrir_proyecto(page, registro["proyecto"])
                abrir_quick_create_timesheet(page)
                rellenar_formulario_timesheet(page, registro)

                if pausa_debug:
                    # El usuario revisa los datos y guarda manualmente en el navegador.
                    # Al hacer 'Resume', el script continúa con el siguiente registro.
                    print("⏸  PAUSA DEBUG: Revisa y guarda manualmente. Luego haz clic en 'Resume'.")
                    page.pause()
                else:
                    guardar_timesheet(page)
                    print("✅ ¡Guardado con éxito!")
                    save_upload_log(registro)
            
            except Exception as e:
                print(f"❌ Error cargando registro {i}: {str(e)}")
                if pausa_debug:
                    page.pause()
                continue

        print("\n✅ Carga finalizada.")
        browser.close()
