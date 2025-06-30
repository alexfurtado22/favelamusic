window.addEventListener("DOMContentLoaded", () => {
  gsap.registerPlugin(SplitText);

  document.fonts.ready.then(() => {
    const split = SplitText.create("#heading", { type: "chars" });

    gsap.set("#heading", { opacity: 1 });

    const mainTimeline = gsap.timeline();

    // 1. Animate heading
    mainTimeline.from(split.chars, {
      y: 20,
      autoAlpha: 0,
      stagger: 0.05,
    });

    // 2. Logo drop-in
    mainTimeline.from(
      "#logo-wrapper svg",
      {
        opacity: 0,
        y: -600,
        scale: 0.8,
        duration: 1.8,
        ease: "power4.out",
      },
      "+=0.3",
    );

    // 3. Logo spin
    mainTimeline.to("#logo-wrapper svg", {
      rotationX: 360,
      duration: 1.5,
      ease: "power2.inOut",
      transformOrigin: "50% 50%",
    });

    // Add label after spin ends
    mainTimeline.add("spinEnd");

    // 4. Dance animation on #logo, starting 0.3s after spin ends
    mainTimeline.to(
      "#logo",
      {
        x: -60,
        rotation: -10,
        scale: 1.4,
        duration: 1.5,
        ease: "sine.inOut",
      },
      "spinEnd+=0.3",
    );

    mainTimeline.to("#logo", {
      x: 0,
      rotation: 0,
      scale: 1,
      duration: 1.5,
      ease: "sine.inOut",
    });
  });
});
