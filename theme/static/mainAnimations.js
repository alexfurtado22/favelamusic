// mainAnimations.js

// Ensure DOM is loaded
window.addEventListener("DOMContentLoaded", () => {
  gsap.registerPlugin(SplitText);

  // Wait for fonts to load before splitting
  document.fonts.ready.then(() => {
    const split = SplitText.create("#heading", { type: "chars" });

    gsap.set("#heading", { opacity: 1 });

    // Create a single timeline to manage all animations
    const mainTimeline = gsap.timeline();

    // 1. Add the heading animation to the timeline
    mainTimeline.from(split.chars, {
      y: 20,
      autoAlpha: 0,
      stagger: 0.05,
    });

    // 2. Add the logo animation, starting 0.3s after the previous one finishes.
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
    ); // 0.3s delay after heading animation

    // 3. Chain the next part of the logo animation
    mainTimeline.to("#logo-wrapper svg", {
      rotationX: 360,
      duration: 1.5,
      ease: "power2.inOut",
      transformOrigin: "50% 50%",
    });
  });
});
