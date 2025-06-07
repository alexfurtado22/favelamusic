document.addEventListener("DOMContentLoaded", () => {
  const fields = [
    { id: "id_picture", label: "filename-picture" },
    { id: "id_track", label: "filename-track" },
    { id: "id_video", label: "filename-video" },
  ];

  fields.forEach(({ id, label }) => {
    const input = document.getElementById(id);
    const output = document.getElementById(label);

    if (input && output) {
      input.addEventListener("change", () => {
        const fileName = input.files[0]?.name || "No file selected";
        output.textContent = fileName;
      });
    }
  });
});
