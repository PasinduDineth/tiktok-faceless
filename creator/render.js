import path from "path";
import fs from "fs";
import { bundle } from "@remotion/bundler";
import { renderMedia, getCompositions } from "@remotion/renderer";

const imagesDir = path.join(process.cwd(), "public/assets/images");
const audioDir = path.join(process.cwd(), "public/assets/audio");
const placeholderImage = path.join(process.cwd(), "public/assets/placeholder.png");
const outPath = path.join(process.cwd(), "out/video.mp4");
const fps = 30;

// Collect images and sort by numeric suffix (image_1.jpg, image_2.jpg...)
let images = [];
if (fs.existsSync(imagesDir)) {
  images = fs.readdirSync(imagesDir)
    .filter((f) => /\.(jpg|jpeg|png|webp)$/i.test(f) && f !== "placeholder.png")
    .sort((a, b) => {
      const na = parseInt((a.match(/_(\d+)\./) || [])[1] || "0", 10);
      const nb = parseInt((b.match(/_(\d+)\./) || [])[1] || "0", 10);
      return na - nb;
    })
    // Use relative paths from public folder for staticFile()
    .map((f) => `assets/images/${f}`);
}

// Use placeholder if no images
if (images.length === 0) {
  console.warn("⚠️ No images found. Using placeholder.");
  if (fs.existsSync(placeholderImage)) {
    images.push(placeholderImage);
  } else {
    console.warn("⚠️ No placeholder found. Video will render black screen.");
  }
}

// Pick first audio and read duration (exclude bgmusic files)
let audio = ""; // absolute path to pass into Remotion
let audioAbsolute = ""; // absolute path used for metadata reading
let audioDurationSeconds = 0;
if (fs.existsSync(audioDir)) {
  const auds = fs.readdirSync(audioDir)
    .filter((f) => /\.(mp3|wav|m4a|aac|flac)$/i.test(f))
    .filter((f) => !f.startsWith('bgmusic')); // Exclude background music files
  if (auds.length > 0) {
    audioAbsolute = path.join(audioDir, auds[0]);
  }
}
if (!audioAbsolute) {
  console.warn("⚠️ No audio found. Video will be silent and default to 10s.");
  audioDurationSeconds = 10;
  audio = ""; // Keep empty for no audio
} else {
  try {
    const mm = await import("music-metadata");
    const meta = await mm.parseFile(audioAbsolute);
    audioDurationSeconds = meta.format.duration || 0;
    if (!audioDurationSeconds || Number.isNaN(audioDurationSeconds)) {
      console.warn("⚠️ Couldn't read audio duration, defaulting to 10s");
      audioDurationSeconds = 10;
    }
    // Use relative path from public folder for staticFile()
    const audioFileName = path.basename(audioAbsolute);
    audio = `assets/audio/${audioFileName}`;
  } catch (err) {
    console.warn("⚠️ Error reading audio metadata:", err.message);
    audioDurationSeconds = 10;
    const audioFileName = path.basename(audioAbsolute);
    audio = `assets/audio/${audioFileName}`;
  }
}

// Validate duration and compute frames
if (!Number.isFinite(audioDurationSeconds) || audioDurationSeconds <= 0) {
  console.warn("⚠️ Invalid audio duration detected, defaulting to 10s");
  audioDurationSeconds = 10;
}

const totalFrames = Math.max(1, Math.ceil(audioDurationSeconds * fps));

// Create a temporary entry file that sets the composition durationInFrames to totalFrames
// We need to pass the actual images and audio data into the composition
const entryTemplate = `import { registerRoot, Composition } from "remotion";
import { Video } from "./src/Video";

const fps = ${fps};
const width = 1080;
const height = 1920;

// The actual props will be passed via inputProps in renderMedia
export const RemotionRoot = () => {
  return (
    <Composition
      id="Video"
      component={Video}
      fps={fps}
      width={width}
      height={height}
      durationInFrames={${totalFrames}}
      defaultProps={{
        images: ${JSON.stringify(images)},
        audio: ${JSON.stringify(audio)},
        durationSeconds: ${audioDurationSeconds.toFixed(3)},
      }}
    />
  );
};

registerRoot(RemotionRoot);
`;

const tempEntry = path.join(process.cwd(), `remotion_entry_${Date.now()}.jsx`);
fs.writeFileSync(tempEntry, entryTemplate, "utf8");

(async () => {
  try {
    console.log("📦 Bundling project with computed duration...");
    const bundleLocation = await bundle({ entryPoint: tempEntry });
    console.log("✅ Bundle ready:", bundleLocation);

    // List compositions in the bundle to verify values
    let comps = [];
    try {
      comps = await getCompositions(bundleLocation);
      console.log("📋 Compositions found:", comps.map((c) => ({ id: c.id, durationInFrames: c.durationInFrames, fps: c.fps, width: c.width, height: c.height })) );
      console.log("📦 Full composition object:", comps[0]);
    } catch (err) {
      console.warn("⚠️ Could not list compositions:", err.message);
    }

    // Prepare input props
    const inputProps = {
      images,
      audio,
      durationSeconds: audioDurationSeconds,
    };

    console.log("🎬 Rendering video...");
    console.log("🔎 Diagnostics:", {
      imagesCount: images.length,
      audio,
      audioDurationSeconds,
      totalFrames,
      fps,
    });
    // Ensure out directory exists
    const outDir = path.dirname(outPath);
    if (!fs.existsSync(outDir)) fs.mkdirSync(outDir, { recursive: true });

    if (comps.length === 0) {
      throw new Error('No compositions found in bundle');
    }

    // Validate composition fps
    if (!Number.isFinite(comps[0].fps)) {
      throw new Error(`Composition fps is invalid: ${comps[0].fps}`);
    }

    console.log("🔧 Composition fps type:", typeof comps[0].fps, comps[0].fps);

    const compDuration = comps[0].durationInFrames;
    const renderOptions = {
      serveUrl: bundleLocation,
      composition: comps[0],
      codec: "h264",
      outputLocation: outPath,
      inputProps,
      frameRange: [0, Math.max(0, compDuration - 1)],
      everyNthFrame: 1,
    };

    console.log("🔧 renderMedia options:", renderOptions);

    await renderMedia(renderOptions);

    console.log("✅ Render done! File saved at:", outPath);
  } catch (err) {
    console.error("❌ Render failed:", err);
    process.exit(1);
  } finally {
    try {
      fs.unlinkSync(tempEntry);
    } catch (err) {
      // ignore
    }
  }
})();
