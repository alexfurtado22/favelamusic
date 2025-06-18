// static/index.js (This script is now specific to home.html, handling the minilogo)

document.addEventListener("DOMContentLoaded", () => {
  function updateMinilogo() {
    const theme = document.documentElement.getAttribute("data-theme");

    // Get references to BOTH desktop and mobile logo elements using their unique IDs
    const desktopMinilogoElement = document.getElementById("desktop-minilogo");
    const mobileMinilogoElement = document.getElementById("mobile-minilogo");

    // Define the mapping of themes to logo filenames
    const themeMinilogoMap = {
      dark: "girl_dark.svg",
      light: "girl_white.svg", // Ensure this exists and is your default
      blue: "girl_blue.svg",
      dim: "girl_dim.svg",
      grape: "girl_grape.svg",
      lime: "girl_lime.svg",
      choco: "girl_choco.svg",
      // Add any other themes and their corresponding 'girl' SVG files here
    };

    // Determine the correct logo filename based on the current theme
    const minilogoFilename = themeMinilogoMap[theme] || "girl_white.svg"; // Fallback to girl_white.svg
    const staticPrefix = document.body?.dataset?.staticPrefix || "/static/";

    // Construct the full path to the logo file, ensuring it's in the 'img/' subdirectory
    const fullMinilogoPath = staticPrefix + "img/" + minilogoFilename;

    console.log("Current Theme:", theme);
    console.log("Setting minilogo to:", fullMinilogoPath);

    // Update the src for the desktop logo if it exists
    if (desktopMinilogoElement) {
      desktopMinilogoElement.src = fullMinilogoPath;
      console.log("Desktop minilogo updated.");
    } else {
      console.log(
        "Desktop minilogo element with ID 'desktop-minilogo' not found.",
      );
    }

    // Update the src for the mobile logo if it exists
    if (mobileMinilogoElement) {
      mobileMinilogoElement.src = fullMinilogoPath;
      console.log("Mobile minilogo updated.");
    } else {
      console.log(
        "Mobile minilogo element with ID 'mobile-minilogo' not found.",
      );
    }
  }

  // Initial call to update the logos (will now attempt to update both)
  updateMinilogo();

  // MutationObserver to watch for data-theme changes on the <html> element
  const observer = new MutationObserver(() => {
    updateMinilogo(); // Re-run the update when the theme changes
  });
  observer.observe(document.documentElement, {
    attributes: true,
    attributeFilter: ["data-theme"],
  });
});
