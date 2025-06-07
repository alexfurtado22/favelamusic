document.addEventListener("alpine:init", () => {
  Alpine.data("artistCreate", () => ({
    name: "",
    instagram: "",
    twitter: "",
    company: "",
  }));

  Alpine.data("producerCreate", () => ({
    name: "",
    company: "",
  }));

  Alpine.data("togglePassword", () => ({
    show: false,
  }));
});
