# Example Configuration Variations

## Example 1: Minimal GUI (Small Window)

```python
# Compact version for smaller screens
WINDOW_WIDTH = 600
WINDOW_HEIGHT = 500
IMAGE_LISTBOX_HEIGHT = 4
LOG_TEXT_HEIGHT = 6
```

## Example 2: Large GUI (Big Screen)

```python
# Expanded version for large monitors
WINDOW_WIDTH = 900
WINDOW_HEIGHT = 800
IMAGE_LISTBOX_HEIGHT = 10
LOG_TEXT_HEIGHT = 12
```

## Example 3: Auto-Mode (No Confirmations)

```python
# Skip confirmation dialogs for faster workflow
CONFIRM_BEFORE_RENDER = False
AUTO_CLEANUP_AFTER_SAVE = True
ENABLE_DETAILED_LOGGING = False
```

## Example 4: Debug Mode (Verbose)

```python
# Keep all files and show detailed logs
CONFIRM_BEFORE_RENDER = True
AUTO_CLEANUP_AFTER_SAVE = False  # Don't auto-clean
ENABLE_DETAILED_LOGGING = True
```

## Example 5: Custom Branding

```python
# Customize for your brand
WINDOW_TITLE = "MyBrand Video Creator Pro"
DEFAULT_VIDEO_NAME = "mybrand_video.mp4"

# Custom colors
COLOR_READY = "#00ff00"
COLOR_PROCESSING = "#ffa500"
COLOR_ERROR = "#ff0000"
```

## Example 6: Additional File Types

```python
# Support more formats
AUDIO_EXTENSIONS = [
    ("Audio Files", "*.mp3 *.wav *.m4a *.aac *.flac *.ogg *.wma"),
    ("MP3 Files", "*.mp3"),
    ("All Files", "*.*")
]

IMAGE_EXTENSIONS = [
    ("Image Files", "*.jpg *.jpeg *.png *.webp *.bmp *.gif *.tiff"),
    ("JPEG Files", "*.jpg *.jpeg"),
    ("PNG Files", "*.png"),
    ("All Files", "*.*")
]
```

## How to Use

1. Copy the examples you want to `config.py`
2. Modify values as needed
3. Save and restart the GUI
4. Changes take effect immediately

## Tips

- **Start small**: Change one setting at a time
- **Test**: Try each change to see the effect
- **Backup**: Keep a copy of the original config
- **Reset**: Delete config.py to use defaults

## Advanced: Dynamic Configuration

For advanced users, you can modify the GUI code to load different configs based on environment variables or command-line arguments.

Example:
```python
import os

# Load config based on environment
if os.getenv("GUI_MODE") == "compact":
    WINDOW_WIDTH = 600
    WINDOW_HEIGHT = 500
elif os.getenv("GUI_MODE") == "large":
    WINDOW_WIDTH = 900
    WINDOW_HEIGHT = 800
else:
    # Default
    WINDOW_WIDTH = 700
    WINDOW_HEIGHT = 600
```

Then run:
```bash
# Windows
set GUI_MODE=compact
python video_generator_gui.py

# Linux/Mac
export GUI_MODE=compact
python video_generator_gui.py
```
