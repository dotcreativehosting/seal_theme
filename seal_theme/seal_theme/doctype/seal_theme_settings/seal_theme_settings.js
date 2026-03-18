// Copyright (c) 2025, Stelden EA Ltd and contributors
// For license information, please see license.txt

frappe.ui.form.on("SEAL Theme Settings", {
    after_save: function (frm) {
        frappe.call({
            method: "seal_theme.seal_theme.doctype.seal_theme_settings.seal_theme_settings.get_theme",
            callback: function (r) {
                if (r.message && r.message != "") {
                    //only apply theme if it has changed
                    if (r.message != frappe.boot.theme) {
                        frappe.boot.theme = r.message;
                        applyTheme(r.message);
                        frappe.ui.toolbar.clear_cache();
                    }
                }
            }
        });
    }
});