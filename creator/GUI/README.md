# TikTok Faceless Video Generator GUI

A Python-based graphical user interface for generating TikTok-style faceless videos with audio, images, and captions.

## Features

- 🎵 **Audio Import**: Browse and select audio files (MP3, WAV, M4A, AAC, FLAC)
- 🖼️ **Multiple Image Import**: Select multiple images at once to create dynamic slideshows
- 📝 **Caption Support**: Optional JSON caption files for subtitles
- 🎬 **Easy Rendering**: One-click video generation
- 💾 **Save Anywhere**: Choose where to save your rendered video
- 🧹 **Auto Cleanup**: Automatically cleans up temporary files after rendering

## Requirements

### Python
- Python 3.7 or higher
- tkinter (usually comes with Python)

### Node.js Dependencies
Make sure you have already installed the Node.js dependencies:
```bash
cd creator
npm install
```

## Installation

1. The GUI is already set up in the `GUI` folder
2. No additional Python packages are required (uses only built-in libraries)

## Usage

### Starting the Application

From the `GUI` folder:
```bash
python video_generator_gui.py
```

Or from the `creator` folder:
```bash
python GUI/video_generator_gui.py
```

### Step-by-Step Guide

1. **Select Audio File**
   - Click "Browse Audio" button
   - Select your audio file (MP3, WAV, M4A, AAC, or FLAC)
   - The filename will appear in the audio section

2. **Select Images**
   - Click "Browse Images" button
   - Select multiple images (hold Ctrl/Cmd to select multiple)
   - Supported formats: JPG, JPEG, PNG, WEBP
   - Images will be displayed in the list

3. **Select Caption File (Optional)**
   - Click "Browse Caption" button
   - Select a JSON file containing caption data
   - The caption file should be in the format expected by Remotion captions

4. **Render Video**
   - Click "Render Video" button
   - Wait for the rendering process to complete (this may take several minutes)
   - Monitor progress in the Status Log section

5. **Save Your Video**
   - After rendering completes, a save dialog will appear
   - Choose where to save your video and provide a filename
   - Click Save

6. **Automatic Cleanup**
   - After saving, the application automatically:
     - Clears imported files from assets folders
     - Removes temporary files
     - Resets the UI for the next video
     - Clears all selections

## File Structure

```
creator/
├── GUI/
│   ├── video_generator_gui.py    # Main GUI application
│   └── README.md                  # This file
├── public/
│   └── assets/
│       ├── audio/                 # Audio files are copied here
│       └── images/                # Images are copied here
├── out/
│   └── video.mp4                  # Rendered video (temporary)
└── render.js                      # Node.js render script
```

## How It Works

1. **File Preparation**: Selected files are copied to the `public/assets` folder
   - Audio files go to `assets/audio/`
   - Images are renamed as `image_1.jpg`, `image_2.jpg`, etc. in `assets/images/`
   - Caption files are copied to `assets/audio/`

2. **Rendering**: The GUI runs `npm run render` which:
   - Creates a temporary Remotion composition
   - Bundles the project
   - Renders the video with your assets
   - Outputs to `out/video.mp4`

3. **Saving**: You choose where to save the final video

4. **Cleanup**: All temporary and asset files are removed

## Caption File Format

The caption JSON file should be an array of word objects with timing data. Each object needs:
- `text` - The word or phrase
- `startMs` - Start time in milliseconds
- `endMs` - End time in milliseconds
- `timestampMs` - Timestamp in milliseconds (usually same as startMs)
- `confidence` - Confidence score (0-1, optional)

**Correct format:**
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

**Important Notes:**
- The file must be saved as `Untitled.json` or the GUI will rename it automatically
- Times are in milliseconds (1000ms = 1 second)
- This format is compatible with Remotion's caption system
- You can generate captions using `npm run create-subtitles` (if available)

## Troubleshooting

### "npm not found" error
- Make sure Node.js is installed and npm is in your PATH
- Try restarting your terminal/command prompt

### Render fails
- Check the Status Log for error messages
- Ensure you have all Node.js dependencies installed (`npm install`)
- Verify that your audio and image files are valid

### Video not generating
- Make sure at least one audio file or image is selected
- Check that the assets folders have write permissions
- Review the Status Log for specific error messages

### GUI doesn't start
- Verify Python 3.7+ is installed: `python --version`
- Make sure tkinter is available (it comes with most Python installations)

## Tips

- **Image Order**: Images will be displayed in the order you select them
- **Performance**: Longer audio and more images will take longer to render
- **Quality**: Use high-quality images for best results
- **Captions**: Captions are optional but enhance engagement

## Advanced Usage

### Custom Video Settings

To customize video settings (resolution, FPS, effects), modify the following files:
- `src/Video.jsx` - Main video component with effects
- `render.js` - Rendering configuration
- `src/CaptionDisplay.jsx` - Caption styling

### Running Without GUI

You can still use the original command-line method:
```bash
npm run render
```

Just manually place your files in the assets folders first.

## Support

For issues or questions:
1. Check the Status Log in the GUI for detailed error messages
2. Review the console output if running from terminal
3. Ensure all dependencies are properly installed

## License

This GUI is part of the TikTok Faceless Video Generator project.
