/**
 * This is a minimal config.
 *
 * If you need the full config, get it from here:
 * https://unpkg.com/browse/tailwindcss@latest/stubs/defaultConfig.stub.js
 */

module.exports = {
  darkMode: ["class"],
  content: [
    /**
     * HTML. Paths to Django template files that will contain Tailwind CSS classes.
     */

    /*  Templates within theme app (<tailwind_app_name>/templates), e.g. base.html. */
    "../templates/**/*.html",

    /*
     * Main templates directory of the project (BASE_DIR/templates).
     * Adjust the following line to match your project structure.
     */
    "../../templates/**/*.html",

    /*
     * Templates in other django apps (BASE_DIR/<any_app_name>/templates).
     * Adjust the following line to match your project structure.
     */
    "../../**/templates/**/*.html",

    /**
     * JS: If you use Tailwind CSS in JavaScript, uncomment the following lines and make sure
     * patterns match your project structure.
     */
    /* JS 1: Ignore any JavaScript in node_modules folder. */
    "!../../**/node_modules",
    /* JS 2: Process all JavaScript files in the project. */
    "../../**/*.js",

    /**
     * Python: If you use Tailwind CSS classes in Python, uncomment the following line
     * and make sure the pattern below matches your project structure.
     */
    "../../**/*.py",
  ],
  theme: {
    screens: {
      xxs: "15rem",
      xs: "24rem",
      sm: "32rem",
      md: "42rem",
      lg: "48rem",
      xl: "64rem",
      xxl: "90rem",
      xxxl: "120rem",
    },
    extend: {
      colors: {
        "text-1": "var(--color-text-1)",
        "text-2": "var(--color-text-2)",
        "surface-1": "var(--color-surface-1)",
        "surface-2": "var(--color-surface-2)",
        "surface-3": "var(--color-surface-3)",
        "surface-4": "var(--color-surface-4)",
        "surface-shadow": "var(--color-surface-shadow)",
        brand: "var(--color-brand)",
      },
      boxShadow: {
        soft: "0 2px 4px oklch(var(--color-surface-shadow) / var(--color-shadow-strength))",
      },
      backgroundImage: {
        "light-radial-grid": "radial-gradient(#cecfd3 1px, transparent 1px)",
        "dark-radial-grid": "radial-gradient(#a0a1a4 1px, transparent 1px)",
      },
    },
  },
  plugins: [
    /**
     * '@tailwindcss/forms' is the forms plugin that provides a minimal styling
     * for forms. If you don't like it or have own styling for forms,
     * comment the line below to disable '@tailwindcss/forms'.
     */
    require("@tailwindcss/forms"),
    require("@tailwindcss/typography"),
    require("@tailwindcss/aspect-ratio"),
  ],
};
