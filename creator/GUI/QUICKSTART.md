# Quick Start Guide - Video Generator GUI

## 🚀 Launch the GUI

### Option 1: Double-click (Windows)
Double-click `start_gui.bat` in the GUI folder

### Option 2: Command Line
```bash
cd creator
python GUI/video_generator_gui.py
```

## 📋 Steps to Create a Video

1. **Click "Browse Audio"** → Select your audio file (MP3, WAV, etc.)

2. **Click "Browse Images"** → Select multiple images (hold Ctrl to select multiple)

3. **Click "Browse Caption"** (Optional) → Select your caption JSON file

4. **Click "Render Video"** → Wait for rendering to complete

5. **Save your video** → Choose location and filename when prompted

6. **Done!** → Files are automatically cleaned up and GUI is ready for next video

## ⚙️ First Time Setup

Before using the GUI, make sure you have:

1. **Python 3.7+** installed
   ```bash
   python --version
   ```

2. **Node.js dependencies** installed
   ```bash
   cd creator
   npm install
   ```

## 💡 Tips

- **Image order matters**: Select images in the order you want them to appear
- **Check the log**: The Status Log shows real-time progress
- **Be patient**: Rendering can take 2-5 minutes depending on video length
- **High quality**: Use good quality images for best results

## ⚠️ Common Issues

**Problem**: "npm is not recognized"
- **Solution**: Install Node.js from https://nodejs.org/

**Problem**: GUI doesn't start
- **Solution**: Check Python is installed and in PATH

**Problem**: Rendering fails
- **Solution**: Check Status Log for errors, ensure npm dependencies are installed

## 📁 What Gets Cleaned Up?

After you save your video, the app automatically removes:
- ✅ Files from `assets/audio/` folder
- ✅ Files from `assets/images/` folder  
- ✅ Temporary `remotion_entry_*.jsx` files
- ✅ The temporary video in `out/video.mp4`

Your saved video is safe! Only the working files are removed.

## 🎬 Your First Video

Try it with these test files:
1. Any MP3 audio file (music, narration, etc.)
2. 3-5 images (JPG or PNG)
3. No caption file needed to start

Click Render and see the magic happen!

---

**Need more help?** Check the full README.md in the GUI folder.
