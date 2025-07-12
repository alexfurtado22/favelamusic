document.addEventListener("DOMContentLoaded", () => {
  console.log("Page loaded. Script is running.");

  const spinner = document.getElementById("spinner");
  const searchIcon = document.getElementById("searchIcon");
  const searchButton = document.getElementById("searchButton");

  // A common parent element that contains your form.
  // Using document.body is a safe fallback.
  const container = document.body;

  // Listen for the HTMX event that fires BEFORE a request
  container.addEventListener("htmx:beforeRequest", function (evt) {
    console.log("DEBUG: htmx:beforeRequest -> Showing spinner.");

    if (spinner && searchIcon && searchButton) {
      spinner.classList.remove("hidden");
      searchIcon.classList.add("hidden");
      searchButton.disabled = true;
    }
  });

  // Listen for the HTMX event that fires AFTER a request is done
  container.addEventListener("htmx:afterRequest", function (evt) {
    console.log("DEBUG: htmx:afterRequest -> Hiding spinner.");

    if (spinner && searchIcon && searchButton) {
      spinner.classList.add("hidden");
      searchIcon.classList.remove("hidden");
      searchButton.disabled = false;
    }
  });
});
