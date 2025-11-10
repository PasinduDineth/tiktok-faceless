import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os
import shutil
import subprocess
import json
from pathlib import Path
import threading
import random

# Try to import config, use defaults if not available
try:
    from config import *
except ImportError:
    # Default settings if config.py is not found
    WINDOW_WIDTH = 700
    WINDOW_HEIGHT = 600
    WINDOW_TITLE = "TikTok Faceless Video Generator"
    AUDIO_EXTENSIONS = [("Audio Files", "*.mp3 *.wav *.m4a *.aac *.flac"), ("All Files", "*.*")]
    IMAGE_EXTENSIONS = [("Image Files", "*.jpg *.jpeg *.png *.webp"), ("All Files", "*.*")]
    CAPTION_EXTENSIONS = [("JSON Files", "*.json"), ("All Files", "*.*")]
    DEFAULT_VIDEO_NAME = "generated_video.mp4"
    DEFAULT_CAPTION_NAME = "Untitled.json"
    COLOR_READY = "green"
    COLOR_PROCESSING = "orange"
    COLOR_ERROR = "red"
    COLOR_UNSELECTED = "gray"
    COLOR_SELECTED = "black"
    PROGRESS_BAR_SPEED = 10
    IMAGE_LISTBOX_HEIGHT = 6
    LOG_TEXT_HEIGHT = 8
    CONFIRM_BEFORE_RENDER = True
    AUTO_CLEANUP_AFTER_SAVE = True


class VideoGeneratorGUI:
    def __init__(self, root):
        self.root = root
        self.root.title(WINDOW_TITLE)
        self.root.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
        self.root.resizable(False, False)
        
        # Get the project root directory (parent of GUI folder)
        self.project_root = Path(__file__).parent.parent
        self.assets_path = self.project_root / "public" / "assets"
        self.audio_path = self.assets_path / "audio"
        self.images_path = self.assets_path / "images"
        self.output_path = self.project_root / "out"
        
        # Ensure directories exist
        self.audio_path.mkdir(parents=True, exist_ok=True)
        self.images_path.mkdir(parents=True, exist_ok=True)
        self.output_path.mkdir(parents=True, exist_ok=True)
        
        # Variables to store file paths
        self.audio_file = None
        self.image_files = []
        self.caption_file = None
        self.is_rendering = False
        
        # Path to background music folder
        self.bg_music_path = self.assets_path / "bg"
        
        self.setup_ui()
        
    def setup_ui(self):
        # Main container with padding
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Title
        title_label = ttk.Label(main_frame, text="Video Generator", 
                                font=("Helvetica", 18, "bold"))
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 20))
        
        # Audio File Section
        audio_frame = ttk.LabelFrame(main_frame, text="Audio File", padding="10")
        audio_frame.grid(row=1, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=5)
        
        self.audio_label = ttk.Label(audio_frame, text="No audio file selected", 
                                      foreground=COLOR_UNSELECTED)
        self.audio_label.grid(row=0, column=0, sticky=(tk.W, tk.E), padx=(0, 10))
        
        audio_btn = ttk.Button(audio_frame, text="Browse Audio", 
                               command=self.browse_audio)
        audio_btn.grid(row=0, column=1)
        
        clear_audio_btn = ttk.Button(audio_frame, text="Clear", 
                                     command=self.clear_audio)
        clear_audio_btn.grid(row=0, column=2, padx=(5, 0))
        
        audio_frame.columnconfigure(0, weight=1)
        
        # Images Section
        images_frame = ttk.LabelFrame(main_frame, text="Images", padding="10")
        images_frame.grid(row=3, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=5)
        
        self.images_label = ttk.Label(images_frame, text="No images selected", 
                                       foreground=COLOR_UNSELECTED)
        self.images_label.grid(row=0, column=0, sticky=(tk.W, tk.E), padx=(0, 10))
        
        images_btn = ttk.Button(images_frame, text="Browse Images", 
                                command=self.browse_images)
        images_btn.grid(row=0, column=1)
        
        clear_images_btn = ttk.Button(images_frame, text="Clear", 
                                      command=self.clear_images)
        clear_images_btn.grid(row=0, column=2, padx=(5, 0))
        
        # Images list
        images_list_frame = ttk.Frame(images_frame)
        images_list_frame.grid(row=1, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), 
                               pady=(10, 0))
        
        self.images_listbox = tk.Listbox(images_list_frame, height=IMAGE_LISTBOX_HEIGHT)
        self.images_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        scrollbar = ttk.Scrollbar(images_list_frame, orient=tk.VERTICAL, 
                                 command=self.images_listbox.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.images_listbox.config(yscrollcommand=scrollbar.set)
        
        images_frame.columnconfigure(0, weight=1)
        
        # Caption File Section
        caption_frame = ttk.LabelFrame(main_frame, text="Caption File (Optional)", 
                                       padding="10")
        caption_frame.grid(row=4, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=5)
        
        self.caption_label = ttk.Label(caption_frame, text="No caption file selected", 
                                        foreground=COLOR_UNSELECTED)
        self.caption_label.grid(row=0, column=0, sticky=(tk.W, tk.E), padx=(0, 10))
        
        caption_btn = ttk.Button(caption_frame, text="Browse Caption", 
                                 command=self.browse_caption)
        caption_btn.grid(row=0, column=1)
        
        clear_caption_btn = ttk.Button(caption_frame, text="Clear", 
                                       command=self.clear_caption)
        clear_caption_btn.grid(row=0, column=2, padx=(5, 0))
        
        caption_frame.columnconfigure(0, weight=1)
        
        # Progress Section
        progress_frame = ttk.Frame(main_frame)
        progress_frame.grid(row=5, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=20)
        
        self.progress_label = ttk.Label(progress_frame, text="Ready to render", 
                                        foreground=COLOR_READY)
        self.progress_label.pack()
        
        self.progress_bar = ttk.Progressbar(progress_frame, mode='indeterminate')
        self.progress_bar.pack(fill=tk.X, pady=(10, 0))
        
        # Render Button
        self.render_btn = ttk.Button(main_frame, text="Render Video", 
                                     command=self.render_video, 
                                     style="Accent.TButton")
        self.render_btn.grid(row=6, column=0, columnspan=3, pady=10)
        
        # Status/Log Section
        log_frame = ttk.LabelFrame(main_frame, text="Status Log", padding="10")
        log_frame.grid(row=7, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), 
                       pady=5)
        
        self.log_text = tk.Text(log_frame, height=LOG_TEXT_HEIGHT, wrap=tk.WORD)
        self.log_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        log_scrollbar = ttk.Scrollbar(log_frame, orient=tk.VERTICAL, 
                                     command=self.log_text.yview)
        log_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.log_text.config(yscrollcommand=log_scrollbar.set)
        
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(7, weight=1)
        
        self.log("Application started successfully")
        self.log(f"Project root: {self.project_root}")
    
    def log(self, message):
        """Add a message to the log"""
        self.log_text.insert(tk.END, f"{message}\n")
        self.log_text.see(tk.END)
        self.root.update_idletasks()
    
    def browse_audio(self):
        """Browse for audio file"""
        filename = filedialog.askopenfilename(
            title="Select Audio File",
            filetypes=AUDIO_EXTENSIONS
        )
        if filename:
            self.audio_file = filename
            self.audio_label.config(text=os.path.basename(filename), foreground=COLOR_SELECTED)
            self.log(f"Audio selected: {os.path.basename(filename)}")
    
    def clear_audio(self):
        """Clear selected audio"""
        self.audio_file = None
        self.audio_label.config(text="No audio file selected", foreground=COLOR_UNSELECTED)
        self.log("Audio cleared")
    
    def get_random_bg_music(self):
        """Get a random background music file from the bg folder"""
        try:
            # Get all audio files from bg folder
            audio_extensions = ['.mp3', '.wav', '.m4a', '.aac', '.flac']
            bg_files = [f for f in self.bg_music_path.glob('*') 
                       if f.suffix.lower() in audio_extensions and f.is_file()]
            
            if not bg_files:
                self.log("Warning: No background music files found in assets/bg folder")
                return None
            
            # Select random file
            selected_bg = random.choice(bg_files)
            self.log(f"Randomly selected background music: {selected_bg.name}")
            return selected_bg
        except Exception as e:
            self.log(f"Error selecting random background music: {str(e)}")
            return None
    
    def browse_images(self):
        """Browse for multiple images"""
        filenames = filedialog.askopenfilenames(
            title="Select Images",
            filetypes=IMAGE_EXTENSIONS
        )
        if filenames:
            self.image_files = list(filenames)
            self.images_listbox.delete(0, tk.END)
            for fname in self.image_files:
                self.images_listbox.insert(tk.END, os.path.basename(fname))
            self.images_label.config(text=f"{len(self.image_files)} image(s) selected", 
                                     foreground=COLOR_SELECTED)
            self.log(f"Selected {len(self.image_files)} images")
    
    def clear_images(self):
        """Clear selected images"""
        self.image_files = []
        self.images_listbox.delete(0, tk.END)
        self.images_label.config(text="No images selected", foreground=COLOR_UNSELECTED)
        self.log("Images cleared")
    
    def browse_caption(self):
        """Browse for caption JSON file"""
        filename = filedialog.askopenfilename(
            title="Select Caption File",
            filetypes=CAPTION_EXTENSIONS
        )
        if filename:
            # Validate JSON file
            try:
                with open(filename, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                # Check if it's an array (correct format)
                if not isinstance(data, list):
                    messagebox.showwarning("Format Warning", 
                        "Caption file should be a JSON array, not an object.\n\n"
                        "See CAPTION_TROUBLESHOOTING.md for correct format.")
                    self.log("Warning: Caption file is not an array")
                
                # Check for correct field names
                if data and len(data) > 0:
                    first_item = data[0]
                    if 'start' in first_item or 'end' in first_item:
                        messagebox.showwarning("Format Warning",
                            "Caption file uses 'start'/'end' but should use 'startMs'/'endMs'.\n\n"
                            "See CAPTION_TROUBLESHOOTING.md for correct format.")
                        self.log("Warning: Caption uses 'start'/'end' instead of 'startMs'/'endMs'")
                    elif 'startMs' in first_item and 'endMs' in first_item:
                        self.log(f"Caption format validated: {len(data)} captions found")
                
                self.caption_file = filename
                self.caption_label.config(text=os.path.basename(filename), foreground=COLOR_SELECTED)
                self.log(f"Caption selected: {os.path.basename(filename)}")
            except json.JSONDecodeError as e:
                messagebox.showerror("Invalid File", 
                    f"The selected file is not a valid JSON file.\n\nError: {str(e)}")
                self.log(f"Error: Invalid JSON file - {str(e)}")
    
    def clear_caption(self):
        """Clear selected caption"""
        self.caption_file = None
        self.caption_label.config(text="No caption file selected", foreground=COLOR_UNSELECTED)
        self.log("Caption cleared")
    
    def clear_assets_folders(self):
        """Clear all files in assets/audio and assets/images folders"""
        try:
            # Clear audio folder
            for file in self.audio_path.glob('*'):
                if file.is_file():
                    file.unlink()
            
            # Clear images folder
            for file in self.images_path.glob('*'):
                if file.is_file():
                    file.unlink()
            
            self.log("Cleared assets folders")
        except Exception as e:
            self.log(f"Error clearing assets: {str(e)}")
    
    def copy_files_to_assets(self):
        """Copy selected files to assets folders"""
        try:
            # Copy audio file
            if self.audio_file:
                dest = self.audio_path / os.path.basename(self.audio_file)
                shutil.copy2(self.audio_file, dest)
                self.log(f"Copied audio to: {dest}")
            
            # Copy random background music
            random_bg = self.get_random_bg_music()
            if random_bg:
                dest = self.audio_path / f"bgmusic{random_bg.suffix}"
                shutil.copy2(random_bg, dest)
                self.log(f"Copied background music to: {dest}")
            
            # Process and copy images with FG/BG separation
            if self.image_files:
                self.log(f"Processing {len(self.image_files)} images for FG/BG separation...")
                
                # Import bg_simple processor
                import sys
                gui_dir = Path(__file__).parent
                sys.path.insert(0, str(gui_dir))
                
                try:
                    from bg_simple import process_image
                    
                    for idx, img_file in enumerate(self.image_files, start=1):
                        self.log(f"Processing image {idx}/{len(self.image_files)}: {os.path.basename(img_file)}")
                        
                        # Get file extension
                        ext = os.path.splitext(img_file)[1]
                        base_name = f"image_{idx}"
                        
                        # First copy original to temp location
                        temp_input = self.images_path / f"{base_name}{ext}"
                        shutil.copy2(img_file, temp_input)
                        
                        # Process with bg_simple to generate FG and BG
                        fg_file, bg_file = process_image(
                            str(temp_input), 
                            str(self.images_path),
                            verbose=False
                        )
                        
                        if fg_file and bg_file:
                            self.log(f"  ✓ Generated {os.path.basename(fg_file)} and {os.path.basename(bg_file)}")
                            # Remove the temporary original file
                            temp_input.unlink()
                        else:
                            self.log(f"  ⚠ Failed to process, keeping original")
                    
                    self.log(f"Completed processing {len(self.image_files)} images")
                    
                except ImportError as e:
                    self.log(f"Warning: Could not import bg_simple module: {e}")
                    self.log("Copying images without FG/BG separation...")
                    # Fallback: just copy images normally
                    for idx, img_file in enumerate(self.image_files, start=1):
                        ext = os.path.splitext(img_file)[1]
                        dest = self.images_path / f"image_{idx}{ext}"
                        shutil.copy2(img_file, dest)
                    self.log(f"Copied {len(self.image_files)} images to assets")
            
            # Copy caption file - always use "Untitled.json" to match Video.jsx expectation
            if self.caption_file:
                dest = self.audio_path / "Untitled.json"
                shutil.copy2(self.caption_file, dest)
                self.log(f"Copied caption to: {dest}")
            
            return True
        except Exception as e:
            self.log(f"Error copying files: {str(e)}")
            messagebox.showerror("Error", f"Failed to copy files: {str(e)}")
            return False
    
    def run_render(self):
        """Run the Node.js render process"""
        try:
            self.log("Starting render process...")
            
            # Run npm render command
            result = subprocess.run(
                ["npm", "run", "render"],
                cwd=str(self.project_root),
                capture_output=True,
                text=True,
                shell=True
            )
            
            # Log output
            if result.stdout:
                for line in result.stdout.split('\n'):
                    if line.strip():
                        self.log(line)
            
            if result.stderr:
                for line in result.stderr.split('\n'):
                    if line.strip():
                        self.log(f"Error: {line}")
            
            if result.returncode == 0:
                self.log("Render completed successfully!")
                return True
            else:
                self.log(f"Render failed with code {result.returncode}")
                return False
                
        except Exception as e:
            self.log(f"Error during render: {str(e)}")
            return False
    
    def save_video(self):
        """Allow user to save the rendered video"""
        video_file = self.output_path / "video.mp4"
        
        if not video_file.exists():
            messagebox.showerror("Error", "Rendered video not found!")
            return False
        
        # Ask user where to save
        save_path = filedialog.asksaveasfilename(
            title="Save Video As",
            defaultextension=".mp4",
            filetypes=[("MP4 Files", "*.mp4"), ("All Files", "*.*")],
            initialfile=DEFAULT_VIDEO_NAME
        )
        
        if save_path:
            try:
                shutil.copy2(video_file, save_path)
                self.log(f"Video saved to: {save_path}")
                messagebox.showinfo("Success", f"Video saved successfully!\n{save_path}")
                return True
            except Exception as e:
                self.log(f"Error saving video: {str(e)}")
                messagebox.showerror("Error", f"Failed to save video: {str(e)}")
                return False
        return False
    
    def cleanup_temp_files(self):
        """Clean up temporary files and clear assets"""
        try:
            # Remove temporary remotion entry files
            for file in self.project_root.glob("remotion_entry_*.jsx"):
                try:
                    file.unlink()
                    self.log(f"Removed temp file: {file.name}")
                except Exception:
                    pass
            
            # Clear assets folders
            self.clear_assets_folders()
            
            # Clear the out folder
            video_file = self.output_path / "video.mp4"
            if video_file.exists():
                try:
                    video_file.unlink()
                    self.log("Removed rendered video from out folder")
                except Exception:
                    pass
            
            self.log("Cleanup completed")
        except Exception as e:
            self.log(f"Error during cleanup: {str(e)}")
    
    def render_video(self):
        """Main render function"""
        if self.is_rendering:
            messagebox.showwarning("Busy", "A render is already in progress!")
            return
        
        # Validate inputs
        if not self.audio_file and not self.image_files:
            messagebox.showwarning("Missing Files", 
                                  "Please select at least an audio file or images!")
            return
        
        # Confirm render
        if CONFIRM_BEFORE_RENDER:
            confirm = messagebox.askyesno("Confirm Render", 
                                         "Start rendering video?\n\nThis may take several minutes.")
            if not confirm:
                return
        
        # Disable render button
        self.is_rendering = True
        self.render_btn.config(state=tk.DISABLED)
        self.progress_label.config(text="Rendering in progress...", foreground=COLOR_PROCESSING)
        self.progress_bar.start(PROGRESS_BAR_SPEED)
        
        # Run rendering in separate thread
        thread = threading.Thread(target=self.render_thread)
        thread.start()
    
    def render_thread(self):
        """Thread function for rendering"""
        try:
            # Step 1: Clear old assets
            self.log("Step 1: Clearing old assets...")
            self.clear_assets_folders()
            
            # Step 2: Copy new files to assets
            self.log("Step 2: Copying files to assets...")
            if not self.copy_files_to_assets():
                self.finish_render(False)
                return
            
            # Step 3: Run render
            self.log("Step 3: Running render...")
            success = self.run_render()
            
            if not success:
                self.finish_render(False)
                return
            
            # Step 4: Save video
            self.log("Step 4: Waiting for user to save video...")
            self.root.after(0, self.handle_save_video)
            
        except Exception as e:
            self.log(f"Unexpected error: {str(e)}")
            self.finish_render(False)
    
    def handle_save_video(self):
        """Handle video saving in main thread"""
        saved = self.save_video()
        
        if saved:
            # Step 5: Cleanup
            self.log("Step 5: Cleaning up...")
            self.cleanup_temp_files()
            
            # Clear UI selections
            self.clear_audio()
            self.clear_images()
            self.clear_caption()
            
            self.log("All done! Ready for next video.")
            self.finish_render(True)
        else:
            self.log("Video not saved. Keeping files for review.")
            self.finish_render(False)
    
    def finish_render(self, success):
        """Finish rendering and update UI"""
        self.is_rendering = False
        self.progress_bar.stop()
        
        if success:
            self.progress_label.config(text="Render completed successfully!", 
                                      foreground=COLOR_READY)
        else:
            self.progress_label.config(text="Render failed or cancelled", 
                                      foreground=COLOR_ERROR)
        
        self.render_btn.config(state=tk.NORMAL)


def main():
    root = tk.Tk()
    app = VideoGeneratorGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
