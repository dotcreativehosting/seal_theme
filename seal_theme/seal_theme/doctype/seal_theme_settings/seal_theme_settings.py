# Copyright (c) 2025, Stelden EA Ltd and contributors
# For license information, please see license.txt

import os
import frappe
from frappe.model.document import Document
from frappe.modules.utils import get_doctype_module


class SEALThemeSettings(Document):
	def before_save(self):
		self.process_theme_change()

	def process_theme_change(self):
		fields = ['color_scheme', 'apply_to_website']
		settings_changed = False
		changed_fields = []
		
		for field in fields:
			if self.has_value_changed(field):
				settings_changed = True
				changed_fields.append(field)

		if settings_changed:
			if self.apply_to_website:
				self.apply_website_theme()
			else:
				self.reset_website_theme()
			frappe.logger().info(f"App and/or Website theme updated due to changes in: {changed_fields}")

	def apply_website_theme(self):
		try:
			# Validate color scheme exists	
			if not self.color_scheme:
				return

			# Get CSS content
			css_content = self.get_css_content(self.color_scheme.lower())
			
			# Create or update theme
			theme = self.update_website_theme(css_content)
			
			theme.set_as_default()
		except Exception as e:
			frappe.log_error(title=f"Failed to apply website theme", message=str(e))
			frappe.throw(f"Failed to apply website theme: {str(e)}")

	def update_website_theme(self, css_content):
		theme_name = "SEAL Theme"

		try:
			if frappe.db.exists("Website Theme", theme_name):
				theme = frappe.get_doc("Website Theme", theme_name)
				theme.custom_scss = css_content
				theme.save()

				return theme
			else:
				theme = frappe.new_doc("Website Theme")
				theme.theme = theme_name
				theme.module = get_doctype_module(self.doctype)
				theme.custom_scss = css_content
				theme.insert(ignore_permissions=True)

				return theme
		except Exception as e:
			frappe.throw(f"Error updating website theme: {str(e)}")

	def get_css_content(self, color_scheme):
		"""
		Read CSS content from the color scheme file (variables only).

		Note: seal_theme.css (common component styles) is already loaded
		globally via web_include_css in hooks.py, so we only need to load
		the color-specific CSS variables here.
		"""
		app_name = "seal_theme"
		web_themes_dir = os.path.join(
			frappe.get_app_path(app_name),
			"public",
			"css",
			"web_themes"
		)

		color_scheme_path = os.path.join(web_themes_dir, f"{color_scheme}.css")

		# Check if color scheme file exists
		if not os.path.exists(color_scheme_path):
			frappe.throw(f"Color scheme file not found: {color_scheme}.css")

		try:
			# Read color scheme CSS (variables only)
			with open(color_scheme_path, 'r') as file:
				color_css = file.read()

			return color_css
		except Exception as e:
			frappe.throw(f"Error reading color scheme file: {str(e)}")
        
	def reset_website_theme(self):
		try:
			theme_name = "Standard"
			
			if frappe.db.exists("Website Theme", theme_name):
				theme = frappe.get_doc("Website Theme", theme_name)
				
				theme.set_as_default()
		except Exception as e:
			frappe.log_error(title=f"Failed to reset website theme", message=str(e))
			frappe.throw(f"Failed to reset website theme: {str(e)}")

@frappe.whitelist()
def get_theme():
	settings = frappe.get_single("SEAL Theme Settings")
	return settings.color_scheme.lower() if settings and settings.color_scheme else "default"

