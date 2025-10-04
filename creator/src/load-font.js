import { continueRender, delayRender } from "remotion";

let loadPromise = null;

export const loadFont = () => {
  if (loadPromise) {
    return loadPromise;
  }

  const handle = delayRender();

  // Load Bangers font from Google Fonts
  loadPromise = Promise.all([
    // Load the font CSS
    new Promise((resolve, reject) => {
      const link = document.createElement('link');
      link.href = 'https://fonts.googleapis.com/css2?family=Bangers&display=swap';
      link.rel = 'stylesheet';
      link.onload = resolve;
      link.onerror = reject;
      document.head.appendChild(link);
    }),
    // Wait a bit for the font to be available
    new Promise(resolve => setTimeout(resolve, 500))
  ])
    .then(() => {
      continueRender(handle);
    })
    .catch((err) => {
      console.error("Failed to load Bangers font", err);
      continueRender(handle);
    });

  return loadPromise;
};

export const BoldFont = "Bangers, cursive";