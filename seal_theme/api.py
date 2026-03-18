import frappe
from frappe import _
from frappe.model.meta import get_meta

@frappe.whitelist()
def get_employee_company():
	"""
	Returns the employee's company if ERPNext is installed and the employee record exists otherwise returns 'Organization'.
	"""
	try:
		if "erpnext" not in frappe.get_installed_apps():
			return "Organization"

		company = frappe.defaults.get_user_default("Company")
		
		return company or "Organization"
	except Exception as e:
		frappe.log_error(frappe.get_traceback(), _("Error fetching user company"))
		return "Organization"
