window.addEventListener("DOMContentLoaded", () => {
  gsap.registerPlugin(SplitText);

  document.fonts.ready.then(() => {
    document.querySelectorAll(".split-heading").forEach((el) => {
      const split = SplitText.create(el, { type: "chars" });

      gsap.set(el, { opacity: 1 });

      gsap.from(split.chars, {
        y: 20,
        autoAlpha: 0,
        stagger: 0.05,
        ease: "power2.out",
      });
    });
  });
});
