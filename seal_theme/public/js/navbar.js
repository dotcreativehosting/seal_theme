frappe.after_ajax(() => {
    let checkNavbar = setInterval(() => {
        let navbar = document.querySelector(".navbar-brand.navbar-home");

        if (navbar) {
            clearInterval(checkNavbar);

            const companyElement = "custom-navbar-company";
            if (!document.querySelector("." + companyElement)) {
                let element = document.createElement("span");
                element.className = companyElement;

                frappe.call({
                    method: "seal_theme.api.get_employee_company",
                    callback: function (r) {
                        element.innerHTML = r.message || "Organization";
                        navbar.appendChild(element);
                    }
                });
            }
        }
    }, 200);
});