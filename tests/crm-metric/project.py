from playwright.sync_api import sync_playwright, expect

def test_suitecrm():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        # 1. Ir a login
        page.goto("https://crm.metricsalad.com/suitecrm/index.php?module=Users&action=Login")

        # 2. Usuario
        page.fill("#user_name", "fernando.garcia")

        # 3. Password
        page.fill("#username_password", "password")

        # 4. Submit
        page.click("#bigbutton")

        # 5. Esperar redirección
        page.wait_for_load_state("networkidle")

        # 6. Validar login
        expect(page).not_to_have_url("Login")
        expect(page.locator("body")).to_contain_text("Inicio")

        # Ir a proyectos
        page.goto("https://crm.metricsalad.com/suitecrm/index.php?module=Project&action=index")

        # Abrir filtro
        page.locator("thead .glyphicon-filter").click()

        # Esperar modal
        expect(page.locator("#searchDialog")).to_be_visible()

        # Buscar proyecto
        nombre_proyecto = "SUB_ME_23_08_V01_EOI_Digital_Skills_2023_CValencia"

        input_search = page.locator("#searchDialog input[name='name_basic']")
        expect(input_search).to_be_visible()
        input_search.fill(nombre_proyecto)

        page.locator("#search_form_submit").click()

        page.wait_for_load_state("networkidle")

        # Click en resultado
        page.get_by_role("link", name=nombre_proyecto).click()

        # Esperar detalle
        page.wait_for_url("**DetailView**")
        page.wait_for_load_state("domcontentloaded")
        expect(page.locator("#subpanel_title_sp_timesheet_project")).to_be_visible()

        # Subpanel
        page.locator("#subpanel_title_sp_timesheet_project").click()
        page.locator("#sp_timesheet_project_nuevo_button").click()

        page.wait_for_selector("input#name")
        page.fill("input#name", "Proyecto automático Playwright")

        # Pausa debug (equivalente a page.pause())
        page.pause()

        browser.close()


test_suitecrm()