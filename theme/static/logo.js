document.addEventListener("DOMContentLoaded", () => {
  function updateLogo() {
    const theme = document.documentElement.getAttribute("data-theme");
    const logoElement = document.getElementById("logo"); // Get your logo element by its ID (it's 'logo' in home.html)

    // Only run if the logo element actually exists on the page
    if (!logoElement) {
      console.log(
        "Logo element with ID 'logo' not found. Skipping logo update.",
      );
      return;
    }

    const themeLogoMap = {
      dark: "girl_dark.svg",
      light: "girl_white.svg",
      blue: "girl_blue.svg",
      dim: "girl_dim.svg",
      grape: "girl_grape.svg",
      lime: "girl_lime.svg",
      choco: "girl_choco.svg",
      // Add any other themes and their corresponding 'girl' SVG files here
    };

    const logoFilename = themeLogoMap[theme] || "girl_white.svg"; // Fallback to girl_white.svg
    const staticPrefix = document.body?.dataset?.staticPrefix || "/static/";

    // Construct the full path to the logo file, ensuring it's in the 'img/' subdirectory
    const fullLogoPath = staticPrefix + "img/" + logoFilename;

    console.log("Setting logo to:", fullLogoPath);

    logoElement.src = fullLogoPath;
  }

  // Initial call for logo (only runs if logo element is present)
  updateLogo();

  // MutationObserver to watch for data-theme changes on the <html> element for logo
  const observer = new MutationObserver(() => {
    updateLogo();
  });
  observer.observe(document.documentElement, {
    attributes: true,
    attributeFilter: ["data-theme"],
  });
});
