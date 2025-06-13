document.addEventListener("DOMContentLoaded", () => {
  function updateFavicon() {
    const theme = document.documentElement.getAttribute("data-theme");
    const favicon = document.getElementById("favicon");

    const themeFaviconMap = {
      dark: "afroline_orange.svg",
      light: "afroline.svg",
      blue: "afroline_blue.svg",
      dim: "afroline_dim.svg",
      grape: "afroline_grape.svg",
      lime: "afroline_lime.svg",
      choco: "afroline_choco.svg",
    };

    const filename = themeFaviconMap[theme] || "afroline.svg";
    const staticPrefix = document.body?.dataset?.staticPrefix || "/static/";
    const fullPath = staticPrefix + filename;

    console.log("Setting favicon to:", fullPath);

    if (favicon) {
      favicon.href = fullPath;
    }
  }

  updateFavicon();

  const observer = new MutationObserver(updateFavicon);
  observer.observe(document.documentElement, {
    attributes: true,
    attributeFilter: ["data-theme"],
  });
});
