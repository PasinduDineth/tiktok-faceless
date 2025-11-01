import React, { useCallback, useEffect, useMemo, useState } from "react";
import { AbsoluteFill, Sequence, Audio, useVideoConfig, staticFile, interpolate, useCurrentFrame, Img, delayRender, continueRender, cancelRender } from "remotion";
import { createTikTokStyleCaptions } from "@remotion/captions";
import CaptionDisplay from "./CaptionDisplay.jsx";
import { loadFont } from "./load-font.js";

// Continuous image display that shows the correct image at each frame
const ContinuousImageDisplay = ({ images, frameDurations, durationInFrames, fps }) => {
  const frame = useCurrentFrame();
  
  // *** CONFIGURABLE SHAKE SETTINGS ***
  // SHAKE_SPEED OPTIONS:
  // 0.1 = ultra slow, 0.5 = slow, 1 = normal, 2 = fast, 
  // 4 = very fast, 6 = super fast, 8 = extreme, 10 = insane, 15+ = crazy fast
  const SHAKE_SPEED = 6; // Change this value for different speeds
  const SHAKE_INTENSITY = 1; // Shake distance in pixels: 0.5=very subtle, 1=subtle, 2=moderate, 3=noticeable, 5=intense
  
  // *** KEN BURNS EFFECT SETTINGS ***
  const ENABLE_KEN_BURNS = true; // Enable/disable Ken Burns effect
  const KEN_BURNS_SCALE_MIN = 1.0; // Minimum scale (1.0 = normal size)
  const KEN_BURNS_SCALE_MAX = 1.2; // Maximum scale (1.2 = 20% zoom)
  const KEN_BURNS_PAN_DISTANCE = 40; // Maximum pan distance in pixels
  
  // Find which image should be displayed at current frame
  let cumulative = 0;
  let currentImageIndex = 0;
  let imageStartFrame = 0;
  
  for (let i = 0; i < images.length; i++) {
    if (frame >= cumulative && frame < cumulative + frameDurations[i]) {
      currentImageIndex = i;
      imageStartFrame = cumulative;
      break;
    }
    cumulative += frameDurations[i];
  }
  
  const currentImage = images[currentImageIndex];
  const currentDuration = frameDurations[currentImageIndex];
  const localFrame = frame - imageStartFrame; // Frame within this image's duration
  
  // Determine BG and FG image paths
  // Remove _FG or _BG from the filename to get base name
  let baseName = currentImage.replace(/_FG(\.[^.]+)$/, '$1').replace(/_BG(\.[^.]+)$/, '$1');
  
  // Get file extension
  const extension = currentImage.match(/\.[^.]+$/)?.[0] || '.png';
  
  // Remove extension from base name if it was added
  baseName = baseName.replace(extension, '');
  
  // Construct both image paths
  const bgImage = `${baseName}_BG${extension}`;
  const fgImage = `${baseName}_FG${extension}`;
  
  // *** KEN BURNS EFFECT CALCULATION ***
  let kenBurnsPanX = 0;
  let kenBurnsPanY = 0;
  let kenBurnsScale = 1;
  
  if (ENABLE_KEN_BURNS) {
    // Create deterministic but varied random values for each image
    const seed = currentImageIndex * 12345;
    const random1 = (Math.sin(seed * 0.1) + 1) / 2;
    const random2 = (Math.sin(seed * 0.2) + 1) / 2;
    const random3 = (Math.sin(seed * 0.3) + 1) / 2;
    const random4 = (Math.sin(seed * 0.4) + 1) / 2;
    const random5 = (Math.sin(seed * 0.5) + 1) / 2;
    const random6 = (Math.sin(seed * 0.6) + 1) / 2;
    
    // Determine random start and end scales
    const startScale = KEN_BURNS_SCALE_MIN + (random1 * (KEN_BURNS_SCALE_MAX - KEN_BURNS_SCALE_MIN));
    const endScale = KEN_BURNS_SCALE_MIN + (random2 * (KEN_BURNS_SCALE_MAX - KEN_BURNS_SCALE_MIN));
    
    // Random pan direction and distance
    const startX = (random3 - 0.5) * 2 * KEN_BURNS_PAN_DISTANCE;
    const startY = (random4 - 0.5) * 2 * KEN_BURNS_PAN_DISTANCE;
    const endX = (random5 - 0.5) * 2 * KEN_BURNS_PAN_DISTANCE;
    const endY = (random6 - 0.5) * 2 * KEN_BURNS_PAN_DISTANCE;
    
    // Interpolate over the entire image duration
    kenBurnsScale = interpolate(
      localFrame,
      [0, currentDuration - 1],
      [startScale, endScale],
      { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' }
    );
    
    kenBurnsPanX = interpolate(
      localFrame,
      [0, currentDuration - 1],
      [startX, endX],
      { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' }
    );
    
    kenBurnsPanY = interpolate(
      localFrame,
      [0, currentDuration - 1],
      [startY, endY],
      { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' }
    );
  }
  
  // Calculate shake effect for foreground layer
  // Create pseudo-random but deterministic shake based on frame and image index
  const shakeSeedX = (frame + currentImageIndex * 1000) * SHAKE_SPEED;
  const shakeSeedY = (frame + currentImageIndex * 1500 + 500) * SHAKE_SPEED;
  
  // Generate smooth shake movement using sine waves with different frequencies
  const shakeX = 
    Math.sin(shakeSeedX * 0.3) * SHAKE_INTENSITY * 0.7 +
    Math.sin(shakeSeedX * 0.7) * SHAKE_INTENSITY * 0.2 +
    Math.sin(shakeSeedX * 1.3) * SHAKE_INTENSITY * 0.1;
    
  const shakeY = 
    Math.sin(shakeSeedY * 0.35) * SHAKE_INTENSITY * 0.7 +
    Math.sin(shakeSeedY * 0.8) * SHAKE_INTENSITY * 0.2 +
    Math.sin(shakeSeedY * 1.1) * SHAKE_INTENSITY * 0.1;
  
  return (
    <AbsoluteFill style={{ backgroundColor: "black" }}>
      {/* Background Layer - With Ken Burns Effect */}
      <Img
        src={staticFile(bgImage)}
        style={{
          width: "100%",
          height: "100%",
          objectFit: "cover",
          position: "absolute",
          top: 0,
          left: 0,
          transform: `translate(${kenBurnsPanX}px, ${kenBurnsPanY}px) scale(${kenBurnsScale})`,
        }}
      />
      {/* Foreground Layer - With Ken Burns + Shake Effect */}
      <Img
        src={staticFile(fgImage)}
        style={{
          width: "100%",
          height: "100%",
          objectFit: "cover",
          position: "absolute",
          top: 0,
          left: 0,
          transform: `translate(${kenBurnsPanX + shakeX}px, ${kenBurnsPanY + shakeY}px) scale(${kenBurnsScale})`,
        }}
      />
    </AbsoluteFill>
  );
};

// Simple component with no crossfade - just perfect timing
const SimplePanningImage = ({ src, duration, imageIndex }) => {
  const frame = useCurrentFrame();
  
  // More varied pan directions including diagonals
  const panTypes = [
    { name: 'bottom', startX: 0, startY: 45, endX: 0, endY: 0 },
    { name: 'top', startX: 0, startY: -45, endX: 0, endY: 0 },
    { name: 'left', startX: -50, startY: 0, endX: 0, endY: 0 },
    { name: 'right', startX: 50, startY: 0, endX: 0, endY: 0 },
    { name: 'bottom-left', startX: -40, startY: 40, endX: 0, endY: 0 },
    { name: 'bottom-right', startX: 40, startY: 40, endX: 0, endY: 0 },
    { name: 'top-left', startX: -40, startY: -40, endX: 0, endY: 0 },
    { name: 'top-right', startX: 40, startY: -40, endX: 0, endY: 0 },
  ];
  
  // Use image index to create deterministic but varied randomness
  const panType = panTypes[imageIndex % panTypes.length];
  
  // Add some scale animation for more dynamic effect
  const startScale = 1.05; // Start slightly zoomed in
  const endScale = 1.0;    // End at normal scale
  
  // Speed up the panning - complete the animation in the first 60% of the image duration
  const panDuration = Math.floor(duration * 0.6); // Pan completes in first 60% of image time
  
  // Interpolate position over the shorter pan duration for faster movement
  const translateX = interpolate(
    frame,
    [0, panDuration],
    [panType.startX, panType.endX],
    { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' }
  );
  
  const translateY = interpolate(
    frame,
    [0, panDuration],
    [panType.startY, panType.endY],
    { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' }
  );
  
  const scale = interpolate(
    frame,
    [0, panDuration],
    [startScale, endScale],
    { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' }
  );
  
  return (
    <AbsoluteFill
      style={{
        backgroundColor: "black", // Solid black background
        width: "100%",
        height: "100%",
      }}
    >
      <Img
        src={staticFile(src)}
        style={{
          width: "100%",
          height: "100%",
          objectFit: "cover",
          transform: `translate(${translateX}px, ${translateY}px) scale(${scale})`,
          position: "absolute",
          top: 0,
          left: 0,
        }}
      />
    </AbsoluteFill>
  );
};

// Component for individual image with crossfade and panning animation
const CrossfadePanningImage = ({ src, duration, imageIndex, crossfadeDuration, isLast }) => {
  const frame = useCurrentFrame();
  
  // Calculate opacity for crossfade
  let opacity = 1;
  if (!isLast && frame > duration - crossfadeDuration) {
    // Fade out in the last crossfadeDuration frames
    opacity = interpolate(
      frame,
      [duration - crossfadeDuration, duration],
      [1, 0],
      { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' }
    );
  }
  
  // More varied pan directions including diagonals
  const panTypes = [
    { name: 'bottom', startX: 0, startY: 45, endX: 0, endY: 0 },
    { name: 'top', startX: 0, startY: -45, endX: 0, endY: 0 },
    { name: 'left', startX: -50, startY: 0, endX: 0, endY: 0 },
    { name: 'right', startX: 50, startY: 0, endX: 0, endY: 0 },
    { name: 'bottom-left', startX: -40, startY: 40, endX: 0, endY: 0 },
    { name: 'bottom-right', startX: 40, startY: 40, endX: 0, endY: 0 },
    { name: 'top-left', startX: -40, startY: -40, endX: 0, endY: 0 },
    { name: 'top-right', startX: 40, startY: -40, endX: 0, endY: 0 },
  ];
  
  // Use image index to create deterministic but varied randomness
  const panType = panTypes[imageIndex % panTypes.length];
  
  // Add some scale animation for more dynamic effect
  const startScale = 1.05; // Start slightly zoomed in
  const endScale = 1.0;    // End at normal scale
  
  // Speed up the panning - complete the animation in the first 60% of the image duration
  const panDuration = Math.floor(duration * 0.6); // Pan completes in first 60% of image time
  
  // Interpolate position over the shorter pan duration for faster movement
  const translateX = interpolate(
    frame,
    [0, panDuration],
    [panType.startX, panType.endX],
    { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' }
  );
  
  const translateY = interpolate(
    frame,
    [0, panDuration],
    [panType.startY, panType.endY],
    { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' }
  );
  
  const scale = interpolate(
    frame,
    [0, panDuration],
    [startScale, endScale],
    { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' }
  );
  
  return (
    <AbsoluteFill
      style={{
        display: "flex",
        justifyContent: "center",
        alignItems: "center",
        overflow: "hidden",
        backgroundColor: "black",
        opacity: opacity, // Apply crossfade opacity
      }}
    >
      <img
        src={staticFile(src)}
        style={{
          width: "100%",
          height: "100%",
          objectFit: "cover",
          transform: `translate(${translateX}px, ${translateY}px) scale(${scale})`,
          backgroundColor: "black", // Prevent flash of white
          display: "block", // Ensure proper rendering
        }}
        // Force the image to always display, no loading states
        loading="eager"
        decoding="sync"
      />
    </AbsoluteFill>
  );
};

// Legacy component kept for compatibility
const PanningImage = ({ src, duration, imageIndex }) => {
  const frame = useCurrentFrame();
  
  // More varied pan directions including diagonals
  const panTypes = [
    { name: 'bottom', startX: 0, startY: 45, endX: 0, endY: 0 },
    { name: 'top', startX: 0, startY: -45, endX: 0, endY: 0 },
    { name: 'left', startX: -50, startY: 0, endX: 0, endY: 0 },
    { name: 'right', startX: 50, startY: 0, endX: 0, endY: 0 },
    { name: 'bottom-left', startX: -40, startY: 40, endX: 0, endY: 0 },
    { name: 'bottom-right', startX: 40, startY: 40, endX: 0, endY: 0 },
    { name: 'top-left', startX: -40, startY: -40, endX: 0, endY: 0 },
    { name: 'top-right', startX: 40, startY: -40, endX: 0, endY: 0 },
  ];
  
  // Use image index to create deterministic but varied randomness
  const panType = panTypes[imageIndex % panTypes.length];
  
  // Add some scale animation for more dynamic effect
  const startScale = 1.05; // Start slightly zoomed in
  const endScale = 1.0;    // End at normal scale
  
  // Speed up the panning - complete the animation in the first 60% of the image duration
  const panDuration = Math.floor(duration * 0.6); // Pan completes in first 60% of image time
  
  // Interpolate position over the shorter pan duration for faster movement
  const translateX = interpolate(
    frame,
    [0, panDuration],
    [panType.startX, panType.endX],
    { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' }
  );
  
  const translateY = interpolate(
    frame,
    [0, panDuration],
    [panType.startY, panType.endY],
    { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' }
  );
  
  const scale = interpolate(
    frame,
    [0, panDuration],
    [startScale, endScale],
    { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' }
  );
  
  return (
    <AbsoluteFill
      style={{
        display: "flex",
        justifyContent: "center",
        alignItems: "center",
        overflow: "hidden",
        backgroundColor: "black",
      }}
    >
      <img
        src={staticFile(src)}
        style={{
          width: "100%",
          height: "100%", 
          objectFit: "cover",
          transform: `translate(${translateX}px, ${translateY}px) scale(${scale})`,
          backgroundColor: "black", // Prevent flash of white
          display: "block", // Ensure proper rendering
        }}
        // Force the image to always display, no loading states
        loading="eager"
        decoding="sync"
      />
    </AbsoluteFill>
  );
};

export const Video = ({ images = [], audio = "", durationSeconds = 10 }) => {
  const { fps, durationInFrames } = useVideoConfig();
  const [subtitles, setSubtitles] = useState([]);
  const [handle] = useState(() => delayRender());

  // How many captions should be displayed at a time?
  // Set to 200ms to display one word at a time
  const SWITCH_CAPTIONS_EVERY_MS = 200;

  // Load captions from video.json
  const fetchSubtitles = useCallback(async () => {
    try {
      await loadFont();
      const res = await fetch(staticFile("assets/audio/Untitled.json"));
      const data = await res.json();
      
      // Convert your format to Remotion's expected format
      const convertedData = data.map(item => ({
        text: item.text,
        startMs: item.startMs,
        endMs: item.endMs,
        timestampMs: item.timestampMs,
        confidence: item.confidence
      }));
      
      setSubtitles(convertedData);
      continueRender(handle);
    } catch (e) {
      console.log("No captions file found or error loading captions:", e);
      continueRender(handle);
    }
  }, [handle]);

  useEffect(() => {
    fetchSubtitles();
  }, [fetchSubtitles]);

  // Create TikTok-style caption pages
  const { pages } = useMemo(() => {
    if (!subtitles || subtitles.length === 0) {
      return { pages: [] };
    }
    return createTikTokStyleCaptions({
      combineTokensWithinMilliseconds: SWITCH_CAPTIONS_EVERY_MS,
      captions: subtitles,
    });
  }, [subtitles, SWITCH_CAPTIONS_EVERY_MS]);

  if (!images || images.length === 0) {
    return (
      <AbsoluteFill
        style={{
          backgroundColor: "black",
          color: "white",
          fontSize: 50,
          display: "flex",
          justifyContent: "center",
          alignItems: "center",
        }}
      >
        No images provided
      </AbsoluteFill>
    );
  }

  // Aggressive preloading to prevent flickering
  React.useEffect(() => {
    const preloadPromises = images.map((src) => {
      return new Promise((resolve, reject) => {
        const img = new Image();
        img.onload = resolve;
        img.onerror = reject;
        img.src = staticFile(src);
        // Force immediate decode
        if (img.decode) {
          img.decode().then(resolve).catch(reject);
        }
      });
    });
    
    // Wait for all images to be ready
    Promise.allSettled(preloadPromises);
  }, [images]);

  // Calculate exact frames per image so that sum equals durationInFrames
  const base = Math.floor(durationInFrames / images.length);
  const remainder = durationInFrames - base * images.length;

  let cumulative = 0;
  
  // Pre-calculate all frame durations to ensure they sum to exactly durationInFrames
  const frameDurations = images.map((_, i) => {
    const extra = i < remainder ? 1 : 0;
    return base + extra;
  });
  
  // Verify the sum is correct (for debugging)
  const totalCalculated = frameDurations.reduce((sum, frames) => sum + frames, 0);
  console.log(`Frame calculation: ${totalCalculated} = ${durationInFrames} (should match)`);

  return (
    <AbsoluteFill style={{ backgroundColor: "black" }}>
      <ContinuousImageDisplay 
        images={images} 
        frameDurations={frameDurations}
        durationInFrames={durationInFrames}
        fps={fps}
      />
      {audio ? <Audio src={staticFile(audio)} /> : null}
      
      {/* Render captions on top of the video */}
      {pages.map((page, index) => {
        const nextPage = pages[index + 1] ?? null;
        const subtitleStartFrame = (page.startMs / 1000) * fps;
        
        // Use the next word's start time as the end time for this word
        // This makes each word stay until the very moment the next word appears
        const subtitleEndFrame = nextPage 
          ? (nextPage.startMs / 1000) * fps 
          : durationInFrames; // Last word stays until video ends
          
        const captionDurationInFrames = subtitleEndFrame - subtitleStartFrame;
        
        if (captionDurationInFrames <= 0) {
          return null;
        }

        return (
          <Sequence
            key={index}
            from={subtitleStartFrame}
            durationInFrames={captionDurationInFrames}
          >
            <CaptionDisplay page={page} />
          </Sequence>
        );
      })}
    </AbsoluteFill>
  );
};
