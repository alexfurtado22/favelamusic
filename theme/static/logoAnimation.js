window.addEventListener("DOMContentLoaded", () => {
  gsap
    .timeline()
    .from("#logo-wrapper svg", {
      opacity: 0,
      y: -600,
      scale: 0.8,
      duration: 1.8,
      ease: "power4.out",
    })
    .to("#logo-wrapper svg", {
      rotationX: 360,
      duration: 1.5,
      ease: "power2.inOut",
      transformOrigin: "50% 50%",
    });
});
