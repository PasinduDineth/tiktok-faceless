"""
Configuration file for Video Generator GUI

You can customize these settings to change the behavior of the GUI.
"""

# GUI Window Settings
WINDOW_WIDTH = 700
WINDOW_HEIGHT = 600
WINDOW_TITLE = "TikTok Faceless Video Generator"

# File Extensions
AUDIO_EXTENSIONS = [
    ("Audio Files", "*.mp3 *.wav *.m4a *.aac *.flac"),
    ("All Files", "*.*")
]

IMAGE_EXTENSIONS = [
    ("Image Files", "*.jpg *.jpeg *.png *.webp"),
    ("All Files", "*.*")
]

CAPTION_EXTENSIONS = [
    ("JSON Files", "*.json"),
    ("All Files", "*.*")
]

# Default file names
DEFAULT_VIDEO_NAME = "generated_video.mp4"
DEFAULT_CAPTION_NAME = "Untitled.json"

# Logging
ENABLE_DETAILED_LOGGING = True

# Render Settings
CONFIRM_BEFORE_RENDER = True
AUTO_CLEANUP_AFTER_SAVE = True

# UI Colors (optional - tkinter uses system theme by default)
# These are used for status messages
COLOR_READY = "green"
COLOR_PROCESSING = "orange"
COLOR_ERROR = "red"
COLOR_UNSELECTED = "gray"
COLOR_SELECTED = "black"

# Progress Bar Speed (milliseconds between updates)
PROGRESS_BAR_SPEED = 10

# Image Listbox Height (number of visible rows)
IMAGE_LISTBOX_HEIGHT = 6

# Log Text Box Height (number of visible rows)
LOG_TEXT_HEIGHT = 8
