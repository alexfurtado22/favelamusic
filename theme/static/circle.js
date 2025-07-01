document.addEventListener("DOMContentLoaded", () => {
  setTimeout(() => {
    const loader = document.querySelector(".loader.rainbow");
    const totalCircles = 100;

    for (let i = 1; i <= totalCircles; i++) {
      const circle = document.createElement("div");
      circle.className = "circle";
      circle.style.setProperty("--i", i);
      loader.appendChild(circle);
    }
  }, 5000); // 5000 ms = 5 seconds delay
});
