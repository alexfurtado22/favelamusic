document.addEventListener("DOMContentLoaded", () => {
  console.log("✅ color_schemes.js loaded");

  const switcher = document.querySelector("#theme-switcher");
  const doc = document.documentElement;

  function setTheme(theme) {
    if (theme === "auto") {
      doc.removeAttribute("data-theme");
    } else {
      doc.setAttribute("data-theme", theme);
    }
    localStorage.setItem("theme", theme);
  }

  if (!switcher) {
    console.error("❌ #theme-switcher element not found");
    return;
  }

  switcher.addEventListener("change", (e) => setTheme(e.target.value));

  // Load saved theme or default to auto
  const savedTheme = localStorage.getItem("theme") || "auto";
  setTheme(savedTheme);

  // Set select to saved value
  const selectedOption = switcher.querySelector(
    `option[value="${savedTheme}"]`,
  );
  if (selectedOption) selectedOption.selected = true;

  // Optional: React to OS theme changes when on 'auto'
  const mediaQuery = window.matchMedia("(prefers-color-scheme: dark)");
  mediaQuery.addEventListener("change", () => {
    if (
      !localStorage.getItem("theme") ||
      localStorage.getItem("theme") === "auto"
    ) {
      setTheme("auto");
    }
  });
});
