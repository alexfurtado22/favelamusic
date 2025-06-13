// static/index.js (This script is now specific to home.html, handling the minilogo)

document.addEventListener("DOMContentLoaded", () => {
  function updateMinilogo() {
    const theme = document.documentElement.getAttribute("data-theme");
    const minilogoElement = document.getElementById("minilogo"); // Correctly gets the minilogo element

    // Only run if the minilogo element actually exists on the page
    if (!minilogoElement) {
      // Corrected console.log to reflect the correct ID being checked
      console.log(
        "Minilogo element with ID 'minilogo' not found. Skipping minilogo update.",
      );
      return;
    }

    const themeMinilogoMap = {
      dark: "girl_dark.svg",
      light: "girl_white.svg",
      blue: "girl_blue.svg",
      dim: "girl_dim.svg",
      grape: "girl_grape.svg",
      lime: "girl_lime.svg",
      choco: "girl_choco.svg",
      // Add any other themes and their corresponding 'girl' SVG files here
    };

    const minilogoFilename = themeMinilogoMap[theme] || "girl_white.svg"; // Fallback to girl_white.svg
    const staticPrefix = document.body?.dataset?.staticPrefix || "/static/";

    // Construct the full path to the logo file, ensuring it's in the 'img/' subdirectory
    const fullMinilogoPath = staticPrefix + "img/" + minilogoFilename;

    console.log("Setting minilogo to:", fullMinilogoPath);

    // This is the crucial line: Use minilogoElement here!
    minilogoElement.src = fullMinilogoPath;
  }

  // Initial call for minilogo (only runs if minilogo element is present)
  updateMinilogo();

  // MutationObserver to watch for data-theme changes on the <html> element for minilogo
  const observer = new MutationObserver(() => {
    updateMinilogo();
  });
  observer.observe(document.documentElement, {
    attributes: true,
    attributeFilter: ["data-theme"],
  });
});
