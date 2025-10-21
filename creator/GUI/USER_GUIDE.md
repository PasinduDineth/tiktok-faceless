# Video Generator GUI - Complete User Guide

## Table of Contents
1. [Introduction](#introduction)
2. [Installation](#installation)
3. [Starting the Application](#starting-the-application)
4. [User Interface Overview](#user-interface-overview)
5. [Creating Your First Video](#creating-your-first-video)
6. [Advanced Features](#advanced-features)
7. [Customization](#customization)
8. [Troubleshooting](#troubleshooting)
9. [FAQ](#faq)

---

## Introduction

The Video Generator GUI is a user-friendly interface for creating TikTok-style faceless videos. It combines audio, images, and optional captions to generate engaging vertical videos perfect for social media.

### What You Can Do
- ✅ Import audio files (MP3, WAV, M4A, AAC, FLAC)
- ✅ Add multiple images with automatic slideshow effects
- ✅ Include synchronized captions (optional)
- ✅ One-click video rendering
- ✅ Save videos anywhere on your computer
- ✅ Automatic cleanup of temporary files

---

## Installation

### Prerequisites

1. **Python 3.7+**
   - Download from: https://www.python.org/downloads/
   - Make sure to check "Add Python to PATH" during installation

2. **Node.js and npm**
   - Download from: https://nodejs.org/
   - Recommended: LTS version

3. **Node.js Dependencies**
   ```bash
   cd creator
   npm install
   ```

### Verify Installation

Run the test script:
```bash
cd GUI
python test_setup.py
```

All checks should pass ✓

---

## Starting the Application

### Method 1: Batch File (Windows)
Double-click `start_gui.bat` in the GUI folder

### Method 2: Command Line
```bash
cd creator
python GUI/video_generator_gui.py
```

### Method 3: Direct Launch
```bash
cd GUI
python video_generator_gui.py
```

---

## User Interface Overview

The GUI is organized into clear sections:

### 1. Audio File Section
- Browse button to select audio
- Clear button to remove selection
- Shows selected filename

### 2. Images Section
- Browse button to select multiple images
- List showing all selected images
- Clear button to remove all images
- Shows count of selected images

### 3. Caption File Section (Optional)
- Browse button to select JSON caption file
- Clear button to remove selection
- Shows selected filename

### 4. Progress Section
- Status label showing current state
- Progress bar during rendering

### 5. Render Button
- Main action button to start video generation

### 6. Status Log
- Detailed log of all operations
- Shows progress, errors, and completion messages

---

## Creating Your First Video

Follow these simple steps:

### Step 1: Prepare Your Assets
- **Audio**: Any MP3, WAV, or supported audio file
- **Images**: 3-10 high-quality images (JPG/PNG recommended)
- **Captions** (optional): JSON file with timing data

### Step 2: Launch the GUI
Double-click `start_gui.bat` or run from command line

### Step 3: Select Audio
1. Click "Browse Audio"
2. Navigate to your audio file
3. Click "Open"
4. Verify the filename appears

### Step 4: Select Images
1. Click "Browse Images"
2. Hold Ctrl (Windows) or Cmd (Mac) to select multiple files
3. Click "Open"
4. Images appear in the list

**Pro Tip**: Select images in the order you want them to appear!

### Step 5: Add Captions (Optional)
1. Click "Browse Caption"
2. Select your JSON caption file
3. Click "Open"

### Step 6: Render Video
1. Click "Render Video"
2. Confirm when prompted
3. Wait for rendering (2-5 minutes typically)
4. Monitor progress in Status Log

### Step 7: Save Your Video
1. Save dialog appears automatically
2. Choose location and filename
3. Click "Save"

### Step 8: Automatic Cleanup
The app automatically:
- Clears assets folders
- Removes temporary files
- Resets UI for next video

---

## Advanced Features

### Image Ordering
Images are processed in the order selected. To reorder:
1. Clear current selection
2. Re-select images in desired order

### Caption Timing
Your JSON file should have this structure (must be an array):
```json
[
  {
    "text": "Hello",
    "startMs": 0,
    "endMs": 500,
    "timestampMs": 0,
    "confidence": 0.95
  },
  {
    "text": "World",
    "startMs": 500,
    "endMs": 1000,
    "timestampMs": 500,
    "confidence": 0.98
  }
]
```

**Important:**
- Times are in **milliseconds** (1000ms = 1 second)
- Must use `startMs` and `endMs` (not `start` and `end`)
- `timestampMs` is usually the same as `startMs`
- `confidence` is optional but recommended (0 to 1 scale)
- The file will be automatically saved as `Untitled.json`

### Multiple Videos
After saving one video:
1. UI automatically clears
2. Select new assets
3. Render again
4. No need to restart application

---

## Customization

### Editing config.py

You can customize the GUI by editing `config.py`:

```python
# Window size
WINDOW_WIDTH = 700
WINDOW_HEIGHT = 600

# Colors
COLOR_READY = "green"
COLOR_PROCESSING = "orange"
COLOR_ERROR = "red"

# Behavior
CONFIRM_BEFORE_RENDER = True
AUTO_CLEANUP_AFTER_SAVE = True
```

Save the file and restart the GUI to see changes.

### Video Effects

To customize video effects, edit these files:
- `src/Video.jsx` - Main video component
- `src/CaptionDisplay.jsx` - Caption styling

Requires knowledge of React and Remotion.

---

## Troubleshooting

### GUI Won't Start

**Symptom**: Double-clicking does nothing or error appears

**Solutions**:
1. Check Python is installed: `python --version`
2. Run test_setup.py to diagnose
3. Try running from command line to see errors

### "npm not found" Error

**Symptom**: Error message about npm during render

**Solutions**:
1. Install Node.js from https://nodejs.org/
2. Restart your computer
3. Verify: `npm --version`

### Rendering Fails

**Symptom**: Render starts but fails with error

**Solutions**:
1. Check Status Log for specific error
2. Verify npm dependencies: `npm install`
3. Check assets are valid files
4. Ensure enough disk space

### No Audio in Video

**Symptom**: Video renders but no sound

**Solutions**:
1. Check audio file plays in media player
2. Verify audio format is supported
3. Check audio file isn't corrupted

### Images Don't Display

**Symptom**: Video is black or images missing

**Solutions**:
1. Use JPG or PNG format
2. Verify images aren't corrupted
3. Check image file sizes (max 10MB recommended)

### Captions Don't Show

**Symptom**: Video renders but no captions appear

**Solutions**:
1. Verify JSON file is valid
2. Check timing values are correct
3. Caption file must be in assets/audio folder

### Slow Rendering

**Symptom**: Rendering takes very long

**Causes**:
- Large image files
- Many images
- Long audio duration
- Older computer

**Solutions**:
1. Reduce image sizes before import
2. Use fewer images
3. Be patient - rendering is CPU-intensive

---

## FAQ

### How long does rendering take?
Typically 2-5 minutes for a 30-60 second video. Depends on:
- Number of images
- Audio length
- Computer speed
- Image sizes

### What video format is created?
MP4 format, H.264 codec, optimized for social media.

### What resolution is the output?
1080x1920 (vertical/portrait), perfect for TikTok, Instagram Reels, YouTube Shorts.

### Can I edit the video after rendering?
Yes! Save the MP4 and edit in any video editor.

### Do I need internet connection?
No, the GUI works completely offline after setup.

### Can I use copyrighted music?
That's your responsibility. This tool doesn't add watermarks or restrictions.

### How many images can I use?
Recommended: 3-10 images. More images = longer render time.

### Can I reuse the same caption file?
Yes, if timing matches the new audio duration.

### What if I close the GUI during rendering?
The process will stop. You'll need to start over.

### Where are temporary files stored?
In `public/assets/` folders. Automatically cleaned after saving.

### Can I run multiple instances?
Not recommended. Assets folders are shared.

### How do I update the GUI?
Replace the files in the GUI folder with new versions.

### Is my data private?
Yes! Everything runs locally on your computer.

### Can I contribute improvements?
Yes! The code is open for modifications.

### What if I want different video dimensions?
Edit `render.js` to change width and height values.

---

## Tips for Best Results

### Audio
- ✅ Use clear, high-quality audio
- ✅ Normalize volume levels
- ✅ Trim silence from start/end
- ✅ Keep under 60 seconds for social media

### Images
- ✅ Use high resolution (1080p+)
- ✅ Portrait orientation works best
- ✅ Ensure good lighting
- ✅ Keep file sizes reasonable (under 5MB each)
- ✅ Use consistent style/theme

### Captions
- ✅ Keep text short and readable
- ✅ Sync timing accurately
- ✅ Use proper punctuation
- ✅ Test on mobile device

### Workflow
- ✅ Organize assets in folders before starting
- ✅ Name files clearly
- ✅ Test with small projects first
- ✅ Keep backup copies of original assets

---

## Getting Help

1. **Check Status Log**: Most issues are logged here
2. **Run test_setup.py**: Diagnoses setup problems
3. **Review this guide**: Most questions answered here
4. **Check console output**: Run from terminal for detailed errors

---

## Summary

The Video Generator GUI simplifies video creation:
1. Select audio, images, and optional captions
2. Click render
3. Wait for completion
4. Save your video
5. Automatic cleanup

That's it! Create unlimited videos with ease.

Happy video creating! 🎬
