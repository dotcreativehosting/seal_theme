frappe.after_ajax(() => {
    // Apply theme after page loads
    const selectedTheme = frappe.boot.theme || 'blue'; // Default to blue if no theme set
    applyTheme(selectedTheme);
});

function applyTheme(theme) {
    const theme_name = theme.trim().toLowerCase();
    
    // Remove any existing theme
    let existingThemeLink = document.getElementById("theme-style");
    if (existingThemeLink) {
        existingThemeLink.remove();
    }

    // If no theme specified, don't load any theme CSS
    if (!theme_name || theme_name === 'default') {
        return;
    }

    // Load the selected theme
    const path = `/assets/seal_theme/css/themes/${theme_name}.css`;
    const link = document.createElement('link');
    
    link.id = 'theme-style';
    link.rel = 'stylesheet';
    link.href = path;
    
    document.head.appendChild(link);
    
    console.log(`Applied theme: ${theme_name}`);
}