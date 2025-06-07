document.addEventListener("DOMContentLoaded", function () {
  const fileInputs = document.querySelectorAll('input[type="file"]');

  fileInputs.forEach((input) => {
    // Get the field name from the input's id (e.g., 'id_picture' → 'picture')
    const id = input.id || "";
    const fieldName = id.startsWith("id_") ? id.slice(3) : id;
    const filenameDisplay = document.getElementById(`filename-${fieldName}`);

    // If the corresponding display element doesn't exist, skip this input
    if (!filenameDisplay) return;

    // Store the initial text content for reverting if the user cancels file selection
    const initialText = filenameDisplay.textContent;

    input.addEventListener("change", function () {
      if (this.files.length > 0) {
        filenameDisplay.textContent = `New: ${this.files[0].name}`;
      } else {
        // If the user clears the selection or opens/cancels the dialog, revert to initial text
        filenameDisplay.textContent = initialText;
      }
    });

    // Optional: Listen to the "Clear" checkbox if you want to visually update the filename display
    const clearCheckbox = document.getElementById(`${input.id}-clear`);
    if (clearCheckbox) {
      clearCheckbox.addEventListener("change", function () {
        if (this.checked) {
          filenameDisplay.textContent = "Cleared (will remove on save)";
          // Clear the actual file input value to ensure no file is re-uploaded
          input.value = "";
        } else {
          // If unchecked, revert to the initial display (current file or "No file selected")
          filenameDisplay.textContent = initialText;
        }
      });
    }
  });
});
