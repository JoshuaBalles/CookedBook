// CookedBook - Theme Switcher with localStorage persistence

(function() {
    'use strict';

    const THEME_KEY = 'cookedbook-theme';
    const DARK_THEME = 'dark';
    const LIGHT_THEME = 'light';

    // Initialize theme on page load
    function initTheme() {
        const savedTheme = localStorage.getItem(THEME_KEY);
        const validThemes = [LIGHT_THEME, DARK_THEME];
        
        if (savedTheme && validThemes.includes(savedTheme)) {
            document.documentElement.setAttribute('data-theme', savedTheme);
        } else {
            // Default to dark mode
            document.documentElement.setAttribute('data-theme', DARK_THEME);
        }
    }

    // Toggle theme between dark and light
    function toggleTheme() {
        const currentTheme = document.documentElement.getAttribute('data-theme');
        const newTheme = currentTheme === LIGHT_THEME ? DARK_THEME : LIGHT_THEME;
        
        if (newTheme === LIGHT_THEME) {
            document.documentElement.setAttribute('data-theme', LIGHT_THEME);
        } else {
            document.documentElement.setAttribute('data-theme', DARK_THEME);
        }
        
        localStorage.setItem(THEME_KEY, newTheme);
    }

    // Expose toggle function globally
    window.toggleTheme = toggleTheme;

    // Initialize on DOM ready
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', initTheme);
    } else {
        initTheme();
    }
})();
