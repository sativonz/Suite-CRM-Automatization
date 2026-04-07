# =============================================================================
# core/selectors.py
# Selectores CSS de SuiteCRM — versión compatible: 7.11.10
#
# Si actualizas SuiteCRM y algún selector deja de funcionar,
# este es el único archivo que debes editar.
# =============================================================================


# ── Login ─────────────────────────────────────────────────────────────────────
LOGIN_USER_INPUT     = "#user_name"
LOGIN_PASSWORD_INPUT = "#username_password"
LOGIN_BUTTON         = "#bigbutton"
LOGIN_URL_FRAGMENT   = "**Login**" 


# ── Lista de proyectos ────────────────────────────────────────────────────────
PROJECT_FILTER_BUTTON  = "thead .glyphicon-filter"
PROJECT_SEARCH_DIALOG  = "#searchDialog"
PROJECT_SEARCH_INPUT   = "#searchDialog input[name='name_basic']"
PROJECT_SEARCH_SUBMIT  = "#search_form_submit"
PROJECT_DETAIL_URL     = "**DetailView**"


# ── Subpanel Timesheet ────────────────────────────────────────────────────────
TIMESHEET_SUBPANEL_TITLE  = "#subpanel_title_sp_timesheet_project"
TIMESHEET_NEW_BUTTON      = "#sp_timesheet_project_nuevo_button"


# ── Formulario Quick Create Timesheet ─────────────────────────────────────────
TIMESHEET_NAME_INPUT  = "input#name"
TIMESHEET_DESCRIPTION = "textarea#description"
TIMESHEET_HOURS_INPUT = "input#hours"
TIMESHEET_DATE_INPUT  = "input#track_date"


# ── Botón Guardar (se prueba en orden hasta encontrar uno visible) ─────────────
TIMESHEET_SAVE_SELECTORS = [
    "input[title='Guardar']",
    "input[value='Guardar']",
    "#SAVE",
    "input[name='save']",
]
