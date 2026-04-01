from playwright.sync_api import sync_playwright, expect
import json
import os
from dotenv import load_dotenv

load_dotenv()

CRM_URL = os.getenv("CRM_URL", "https://crm.metricsalad.com/suitecrm")
CRM_USER = os.getenv("CRM_USER")
CRM_PASSWORD = os.getenv("CRM_PASSWORD")

def login(page):
    page.goto(f"{CRM_URL}/index.php?module=Users&action=Login")
    page.fill("#user_name", CRM_USER)
    page.fill("#username_password", CRM_PASSWORD)
    page.click("#bigbutton")
    page.wait_for_load_state("networkidle")
    expect(page).not_to_have_url("**Login**")


def abrir_proyecto(page, nombre_proyecto):
    page.goto(f"{CRM_URL}/index.php?module=Project&action=index")
    page.wait_for_load_state("networkidle")

    page.locator("thead .glyphicon-filter").click()
    expect(page.locator("#searchDialog")).to_be_visible()

    input_search = page.locator("#searchDialog input[name='name_basic']")
    expect(input_search).to_be_visible()
    input_search.fill(nombre_proyecto)

    page.locator("#search_form_submit").click()
    page.wait_for_load_state("networkidle")

    # Hacer clic en el primer resultado que contenga el nombre (no exacto para evitar fallos de mayúsculas/espacios)
    resultado = page.get_by_role("link", name=nombre_proyecto, exact=False).first
    
    if resultado.count() == 0:
        raise RuntimeError(f"No se encontró ningún proyecto que coincida con '{nombre_proyecto}' en los resultados de búsqueda.")
    
    expect(resultado).to_be_visible(timeout=5000)
    resultado.click()

    page.wait_for_url("**DetailView**")
    page.wait_for_load_state("domcontentloaded")
    expect(page.locator("#subpanel_title_sp_timesheet_project")).to_be_visible()


def abrir_quick_create_timesheet(page):
    subpanel = page.locator("#subpanel_title_sp_timesheet_project")

    if subpanel.get_attribute("class") and "collapsed" in subpanel.get_attribute("class"):
        subpanel.click()

    nuevo_btn = page.locator("#sp_timesheet_project_nuevo_button")
    nuevo_btn.wait_for()

    nuevo_btn.scroll_into_view_if_needed()
    nuevo_btn.click(force=True)

    page.wait_for_selector("input#name")
    page.wait_for_selector("textarea#description")
    page.wait_for_selector("input#hours")
    page.wait_for_selector("input#track_date")


def horas_para_crm(horas):
    if isinstance(horas, (int, float)):
        return str(horas).replace(".", ",")
    return str(horas).strip()


def rellenar_formulario_timesheet(page, registro):

    page.fill("input#name", registro["tarea_short"])
    page.fill("textarea#description", registro["tarea_long"])
    
    page.fill("input#hours", horas_para_crm(registro["horas"]))

    fecha_a_usar = registro["fecha"]
    
    fecha_input = page.locator("input#track_date")
    fecha_input.fill("")
    fecha_input.fill(fecha_a_usar)

    valor_fecha = fecha_input.input_value()
    if valor_fecha != fecha_a_usar:
        print(f"ADVERTENCIA: La fecha no coincide perfectamente. Esperado: {fecha_a_usar} / Actual: {valor_fecha}")


def guardar_timesheet(page):
    posibles_botones = [
        "input[title='Guardar']",
        "input[value='Guardar']",
        "#SAVE",
        "input[name='save']",
    ]

    for selector in posibles_botones:
        locator = page.locator(selector)
        if locator.count() > 0 and locator.first.is_visible():
            locator.first.click()
            page.wait_for_load_state("networkidle")
            return

    raise RuntimeError("No se encontró botón de Guardar en el quick create")


def exec_auto_load(registros, headless=False, pausa_debug=False):
    """
    Función unificada para subir una lista de registros al CRM.
    """
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
                    print("PAUSA DEBUG: Revisa los datos en el navegador.")
                    page.pause()
                else:
                    guardar_timesheet(page)
                    print("¡Guardado con éxito!")
            
            except Exception as e:
                print(f"Error cargando registro {i}: {str(e)}")
                if pausa_debug:
                    page.pause()
                continue

        print("\nCarga finalizada.")
        browser.close()
