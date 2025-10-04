# TikTok/Reels Video Generator

A Remotion-based video generator that creates 9:16 aspect ratio videos from sequential images and audio.

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

Generate your video:
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