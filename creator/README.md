# TikTok/Reels Video Generator

A Remotion-based video generator that creates 9:16 aspect ratio videos from sequential images and audio.

## 🎨 NEW: Python GUI Available!

**Easy-to-use graphical interface for video generation!**

- 📁 Browse and select audio files
- 🖼️ Import multiple images at once
- 📝 Add caption files (optional)
- 🎬 One-click rendering
- 💾 Save videos anywhere
- 🧹 Automatic cleanup

**Get Started:** See the [GUI folder](./GUI/) or run:
```bash
python GUI/video_generator_gui.py
```

📖 **Full Documentation:** [GUI/README.md](./GUI/README.md)

---

## Features

- **Sequential Image Display**: Images named `image_1.jpg`, `image_2.jpg`, etc. are displayed in numerical order
- **Audio Sync**: Video duration automatically matches the audio file length
- **9:16 Aspect Ratio**: Perfect for TikTok, Instagram Reels, and YouTube Shorts
- **Auto-scaling**: Images are scaled/cropped to cover the full frame without black bars
- **Equal Duration**: Each image gets equal screen time (total audio duration ÷ number of images)
- **Dynamic Transitions**: Each image features subtle panning animations from different directions (top, bottom, left, right, diagonals) with slight zoom effects for more engaging visuals

## Setup

1. Install dependencies:
```bash
npm install
```

2. Prepare your assets:
   - Place images in `public/assets/images/` named sequentially: `image_1.png`, `image_2.png`, etc.
   - Place your audio file in `public/assets/audio/` (supports .mp3, .wav, .m4a, .aac, .flac)

## Usage

### Option 1: GUI (Recommended for Beginners)

Launch the graphical interface:
```bash
# Windows
python GUI/video_generator_gui.py
# Or double-click GUI/start_gui.bat

# Mac/Linux
python3 GUI/video_generator_gui.py
```

Then:
1. Browse and select your audio file
2. Browse and select multiple images
3. Optionally add a caption JSON file
4. Click "Render Video"
5. Save your video when prompted

See [GUI/QUICKSTART.md](./GUI/QUICKSTART.md) for detailed instructions.

### Option 2: Command Line (Original Method)

Manually place files in assets folders, then generate your video:
```bash
npm run render
```

The output video will be saved to `out/video.mp4`.

## Asset Requirements

### Images
- **Location**: `public/assets/images/`
- **Naming**: `image_1.ext`, `image_2.ext`, `image_3.ext`, etc.
- **Formats**: `.jpg`, `.jpeg`, `.png`, `.webp`
- **Order**: Images are sorted numerically by the number in the filename

### Audio
- **Location**: `public/assets/audio/`
- **Formats**: `.mp3`, `.wav`, `.m4a`, `.aac`, `.flac`
- **Note**: The first audio file found will be used

## Output Specifications

- **Resolution**: 1080×1920 (9:16 aspect ratio)
- **Frame Rate**: 30 FPS
- **Codec**: H.264
- **Duration**: Matches audio file duration exactly
- **Image Timing**: Each image displays for `(audio duration) ÷ (number of images)` seconds

## Example Structure

```
creator/
├── public/
│   └── assets/
│       ├── images/
│       │   ├── image_1.png
│       │   ├── image_2.png
│       │   ├── image_3.png
│       │   └── ...
│       └── audio/
│           └── audio.mp3
├── out/
│   └── video.mp4 (generated)
└── ...
```

## Notes

- If no images are found, a placeholder will be used
- If no audio is found, the video will be silent with a default 10-second duration
- Images are centered and scaled to cover the entire 9:16 frame
- No image repeats - each image appears exactly once in sequence



# Steps
- Add images and audio to public folder.
- run npm run create-subtitles "public/assets/audio/Untitled.wav" to generate the caption file
- run npm run render to generate the video


# script to download from whisk

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
