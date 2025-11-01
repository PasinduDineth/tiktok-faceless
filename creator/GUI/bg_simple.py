"""
Simple Color-Based Background Separation for Comics
Works by detecting and removing the background color
Can be used as a module or standalone script
"""

import cv2
import numpy as np
from PIL import Image 
import sys
import os

# ============================================
# QUICK SETTINGS - ADJUST THESE
# ============================================

# Background color detection
# True = auto-detect (recommended), False = use manual color below
AUTO_DETECT = True
MANUAL_BG_COLOR = [255, 255, 255]  # White background [R, G, B]

# How much color variation to treat as background (10-80)
# Lower = stricter (only exact color), Higher = more flexible
COLOR_TOLERANCE = 12  # Lower value = MORE foreground (background must be closer to exact color)

# Advanced options
SMOOTH_EDGES = True
BLUR_AMOUNT = 3        # Edge smoothing (1-7)
REMOVE_NOISE = True
MIN_SIZE = 200         # Remove regions smaller than this

# ============================================
# PROCESSING FUNCTION
# ============================================

def process_image(input_path, output_dir=None, verbose=True):
    """
    Process an image to separate foreground and background
    
    Args:
        input_path: Path to input image
        output_dir: Directory to save outputs (default: same as input)
        verbose: Print progress messages
    
    Returns:
        tuple: (fg_filename, bg_filename) paths to generated files
    """
    if verbose:
        print("="*60)
        print("🎨 Simple Background Removal for Comics")
        print("="*60)
    
    # Load image
    if verbose:
        print(f"\n📥 Loading: {os.path.basename(input_path)}")
    
    img = cv2.imread(input_path)
    if img is None:
        if verbose:
            print(f"❌ Error: Could not load image: {input_path}")
        return None, None
    
    h, w = img.shape[:2]
    if verbose:
        print(f"   ✓ Size: {w}x{h} pixels")
    
    # Convert to RGB for PIL
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    
    # Detect background color
    if AUTO_DETECT:
        # Sample corners - background is usually at edges
        margin = min(h, w) // 10
        corners = [
            img_rgb[0:margin, 0:margin],
            img_rgb[0:margin, w-margin:w],
            img_rgb[h-margin:h, 0:margin],
            img_rgb[h-margin:h, w-margin:w]
        ]
        bg_color = np.mean([np.mean(c, axis=(0,1)) for c in corners], axis=0).astype(int)
        if verbose:
            print(f"\n🎨 Auto-detected background: RGB({bg_color[0]}, {bg_color[1]}, {bg_color[2]})")
    else:
        bg_color = np.array(MANUAL_BG_COLOR)
        if verbose:
            print(f"\n🎨 Using manual background: RGB({bg_color[0]}, {bg_color[1]}, {bg_color[2]})")
    
    # Calculate color difference from background
    if verbose:
        print(f"\n🔍 Separating foreground (tolerance: {COLOR_TOLERANCE})...")
    
    diff = np.sqrt(np.sum((img_rgb.astype(float) - bg_color)**2, axis=2))
    
    # Normalize to 0-100 range
    max_diff = np.sqrt(3 * 255**2)
    diff_percent = (diff / max_diff) * 100
    
    # Create mask: pixels different from background = foreground
    foreground_mask = (diff_percent > COLOR_TOLERANCE).astype(np.uint8) * 255
    
    if verbose:
        initial_fg = (np.sum(foreground_mask > 0) / (h*w)) * 100
        print(f"   Initial: {initial_fg:.1f}% foreground")
    
    # Remove noise
    if REMOVE_NOISE:
        num_labels, labels, stats, _ = cv2.connectedComponentsWithStats(foreground_mask, connectivity=8)
        cleaned = np.zeros_like(foreground_mask)
        removed_count = 0
        for i in range(1, num_labels):
            if stats[i, cv2.CC_STAT_AREA] >= MIN_SIZE:
                cleaned[labels == i] = 255
            else:
                removed_count += 1
        foreground_mask = cleaned
        if verbose and removed_count > 0:
            print(f"   Removed {removed_count} noise regions")
    
    # Smooth edges
    if SMOOTH_EDGES:
        # Slight morphological closing to fill gaps
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
        foreground_mask = cv2.morphologyEx(foreground_mask, cv2.MORPH_CLOSE, kernel)
    # Smooth edges
    if SMOOTH_EDGES:
        # Slight morphological closing to fill gaps
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
        foreground_mask = cv2.morphologyEx(foreground_mask, cv2.MORPH_CLOSE, kernel)
        
        # Gaussian blur for smooth edges
        foreground_mask = cv2.GaussianBlur(foreground_mask, (BLUR_AMOUNT, BLUR_AMOUNT), 0)
        if verbose:
            print(f"   Applied edge smoothing")
    
    if verbose:
        final_fg = (np.sum(foreground_mask > 127) / (h*w)) * 100
        print(f"   Final: {final_fg:.1f}% foreground / {100-final_fg:.1f}% background")
    
    # Get base filename and output directory
    base_name = os.path.splitext(os.path.basename(input_path))[0]
    if output_dir is None:
        output_dir = os.path.dirname(input_path)
    
    # Create outputs
    if verbose:
        print(f"\n💾 Saving outputs...")
    
    # Foreground with transparency
    fg_rgba = np.dstack((img_rgb, foreground_mask))
    fg_filename = os.path.join(output_dir, f"{base_name}_FG.png")
    Image.fromarray(fg_rgba).save(fg_filename)
    if verbose:
        print(f"   ✓ {os.path.basename(fg_filename)}")
    
    # Keep original image as background (no alpha channel modification)
    bg_filename = os.path.join(output_dir, f"{base_name}_BG.png")
    Image.fromarray(img_rgb).save(bg_filename)
    if verbose:
        print(f"   ✓ {os.path.basename(bg_filename)} (original)")
    
    if verbose:
        print("\n" + "="*60)
        print("✅ DONE!")
        print("="*60)
        final_fg = (np.sum(foreground_mask > 127) / (h*w)) * 100
        print(f"\n📊 Result: {final_fg:.1f}% foreground extracted")
        print(f"Background: Original image preserved")
        
        if final_fg < 20:
            print(f"\n⚠️  LOW FOREGROUND ({final_fg:.1f}%) - Try:")
            print(f"   • Decrease COLOR_TOLERANCE to {COLOR_TOLERANCE - 5}")
        elif final_fg > 80:
            print(f"\n⚠️  HIGH FOREGROUND ({final_fg:.1f}%) - Try:")
            print(f"   • Increase COLOR_TOLERANCE to {COLOR_TOLERANCE + 5}")
        else:
            print(f"\n✅ Good balance!")
        
        print(f"\n💡 To adjust split: Edit COLOR_TOLERANCE (current: {COLOR_TOLERANCE})")
        print(f"   Lower = more foreground | Higher = less foreground")
        print("="*60)
    
    return fg_filename, bg_filename


# ============================================
# COMMAND LINE USAGE
# ============================================

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python bg_simple.py <input_image> [output_directory]")
        print("Example: python bg_simple.py image.jpg")
        print("Example: python bg_simple.py image.jpg C:/output/")
        sys.exit(1)
    
    input_image = sys.argv[1]
    output_dir = sys.argv[2] if len(sys.argv) > 2 else None
    
    if not os.path.exists(input_image):
        print(f"❌ Error: File not found: {input_image}")
        sys.exit(1)
    
    fg_file, bg_file = process_image(input_image, output_dir, verbose=True)
    
    if fg_file and bg_file:
        sys.exit(0)
    else:
        sys.exit(1)
