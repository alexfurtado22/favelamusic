document.addEventListener("alpine:init", () => {
  Alpine.directive("flash", (el, { expression }, { evaluate }) => {
    // Fade + slide in when shown
    gsap.fromTo(
      el,
      { opacity: 0, y: -10 },
      { opacity: 1, y: 0, duration: 0.4, ease: "power2.out" },
    );

    // Watch Alpine `show` state to trigger exit
    let observer = new MutationObserver(() => {
      if (!el._x_dataStack?.[0]?.show) {
        gsap.to(el, {
          opacity: 0,
          y: -10,
          duration: 0.7,
          ease: "power2.in",
          onComplete: () => el.remove(),
        });
        observer.disconnect();
      }
    });

    observer.observe(el, { attributes: true, attributeFilter: ["x-show"] });
  });
});
