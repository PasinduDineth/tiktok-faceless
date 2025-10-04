(async () => {
  const delay = ms => new Promise(r => setTimeout(r, ms));
  const images = []; // Store objects: { src, position }
  const SCROLL_STEP = 200;
  const MAX_SCROLL = 4000;

  // 1️⃣ Scroll in chunks and collect images
  for (let scrolled = 0; scrolled <= MAX_SCROLL; scrolled += SCROLL_STEP) {
    // Scroll the window
    window.scrollBy({ top: SCROLL_STEP, behavior: 'smooth' });

    // Scroll all scrollable divs
    const scrollableDivs = Array.from(document.querySelectorAll('div'))
      .filter(div => div.scrollHeight > div.clientHeight);
    scrollableDivs.forEach(div => div.scrollTop += SCROLL_STEP);

    await delay(800); // Wait for images to load

    const container = document.querySelector('.PTre');
    if (!container) continue;

    const imgs = container.querySelectorAll('img');
    imgs.forEach((img, idx) => {
      const src = img.src;
      if (src) {
        images.push({ src, position: scrolled + idx });
      }
    });

    console.log(`📌 Scrolled to ${scrolled}px, collected ${imgs.length} images so far`);
  }

  // 2️⃣ Remove duplicates and sort by position
  const uniqueImagesMap = new Map();
  images.forEach(img => {
    if (!uniqueImagesMap.has(img.src)) {
      uniqueImagesMap.set(img.src, img.position);
    }
  });

  const uniqueImages = Array.from(uniqueImagesMap.entries())
    .map(([src, position]) => ({ src, position }))
    .sort((a, b) => a.position - b.position);

  console.log(`🗂 Total unique images: ${uniqueImages.length}`);

  // 3️⃣ Print unique image links in order
  uniqueImages.forEach((img, i) => {
    console.log(`${i + 1}: ${img.src}`);
  });

  // ✅ Downloading part commented out
  for (let i = 0; i < uniqueImages.length; i++) {
    const { src } = uniqueImages[i];
    try {
      const res = await fetch(src);
      const blob = await res.blob();
      const url = URL.createObjectURL(blob);

      const a = document.createElement("a");
      a.href = url;
      a.download = `image_${i + 1}.png`;
      document.body.appendChild(a);
      a.click();
      document.body.removeChild(a);

      URL.revokeObjectURL(url);
      console.log(`💾 Downloaded image_${i + 1}.png`);
      await delay(300);
    } catch (e) {
      console.warn(`⚠️ Failed to download ${src}`, e);
    }
  }

})();


// "C:\Program Files\Google\Chrome\Application\chrome.exe" --remote-debugging-port=9222 --user-data-dir="C:\ChromeDebug"
