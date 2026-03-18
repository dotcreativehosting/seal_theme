import frappe

BI_THEME = "theme"
BI_COMPANY = "company"

def boot_session(bootinfo):
    init_session(bootinfo)

def init_session(bootinfo):
    try:
        settings = frappe.get_single("SEAL Theme Settings")
        theme = settings.color_scheme.lower() if settings and settings.color_scheme else "blue"
    except Exception:
        # If settings don't exist or there's an error, default to blue
        theme = "blue"
    
    bootinfo[BI_THEME] = theme

    # Inject company name
    try:
        default_company = frappe.defaults.get_defaults().get("company")
        if default_company:
            bootinfo[BI_COMPANY] = default_company
    except Exception:
        pass