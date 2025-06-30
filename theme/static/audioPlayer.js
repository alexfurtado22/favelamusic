document.querySelectorAll(".audio-player").forEach((player) => {
  const audio = player.querySelector(".player-audio");
  const playBtn = player.querySelector(".play-pause-btn");
  const playIcon = player.querySelector(".play-icon");
  const pauseIcon = player.querySelector(".pause-icon");
  const progress = player.querySelector(".progress");
  const progressBar = player.querySelector(".progress-bar-container");
  const currentTime = player.querySelector(".current-time");
  const totalDuration = player.querySelector(".total-duration");
  const volumeSlider = player.querySelector(".volume-slider");
  const muteBtn = player.querySelector(".mute-btn");
  const volumeOnIcon = player.querySelector(".volume-on-icon");
  const volumeOffIcon = player.querySelector(".volume-off-icon");

  // Format time
  const formatTime = (seconds) => {
    const min = Math.floor(seconds / 60);
    const sec = Math.floor(seconds % 60);
    return `${min}:${sec.toString().padStart(2, "0")}`;
  };

  // Toggle play
  playBtn.addEventListener("click", () => {
    const isPlaying = !audio.paused;
    document.querySelectorAll(".player-audio").forEach((a) => {
      if (a !== audio) {
        a.pause();
        a.closest(".audio-player")
          .querySelector(".play-icon")
          .classList.remove("hidden");
        a.closest(".audio-player")
          .querySelector(".pause-icon")
          .classList.add("hidden");
      }
    });

    if (isPlaying) {
      audio.pause();
      playIcon.classList.remove("hidden");
      pauseIcon.classList.add("hidden");
    } else {
      audio.play();
      playIcon.classList.add("hidden");
      pauseIcon.classList.remove("hidden");
    }
  });

  // Time updates
  audio.addEventListener("loadedmetadata", () => {
    totalDuration.textContent = formatTime(audio.duration);
  });

  audio.addEventListener("timeupdate", () => {
    const percent = (audio.currentTime / audio.duration) * 100;
    progress.style.width = `${percent}%`;
    currentTime.textContent = formatTime(audio.currentTime);
  });

  // Seek
  progressBar.addEventListener("click", (e) => {
    const rect = progressBar.getBoundingClientRect();
    const x = e.clientX - rect.left;
    const ratio = x / progressBar.clientWidth;
    audio.currentTime = ratio * audio.duration;
  });

  // Volume slider
  volumeSlider.addEventListener("input", () => {
    audio.volume = volumeSlider.value;
  });

  // Mute toggle
  muteBtn.addEventListener("click", () => {
    audio.muted = !audio.muted;
    volumeOnIcon.classList.toggle("hidden", audio.muted);
    volumeOffIcon.classList.toggle("hidden", !audio.muted);
  });
});
