"""
Test script to verify GUI setup

This script checks if all required components are in place
and reports any issues.
"""

import os
import sys
from pathlib import Path

def test_gui_setup():
    print("=== Video Generator GUI Setup Test ===\n")
    
    # Get paths
    gui_path = Path(__file__).parent
    creator_path = gui_path.parent
    
    print(f"GUI folder: {gui_path}")
    print(f"Creator folder: {creator_path}\n")
    
    # Check Python version
    print("1. Checking Python version...")
    python_version = sys.version_info
    if python_version >= (3, 7):
        print(f"   ✓ Python {python_version.major}.{python_version.minor}.{python_version.micro} (OK)")
    else:
        print(f"   ✗ Python {python_version.major}.{python_version.minor} (Need 3.7+)")
        return False
    
    # Check tkinter
    print("\n2. Checking tkinter...")
    try:
        import tkinter as tk
        print("   ✓ tkinter is available")
    except ImportError:
        print("   ✗ tkinter is not available")
        print("   Install it with: apt-get install python3-tk (Linux) or reinstall Python (Windows/Mac)")
        return False
    
    # Check required files
    print("\n3. Checking required files...")
    required_files = {
        "video_generator_gui.py": gui_path / "video_generator_gui.py",
        "config.py": gui_path / "config.py",
        "render.js": creator_path / "render.js",
        "package.json": creator_path / "package.json",
    }
    
    all_files_exist = True
    for name, path in required_files.items():
        if path.exists():
            print(f"   ✓ {name}")
        else:
            print(f"   ✗ {name} (missing)")
            all_files_exist = False
    
    # Check required folders
    print("\n4. Checking required folders...")
    required_folders = {
        "public/assets": creator_path / "public" / "assets",
        "public/assets/audio": creator_path / "public" / "assets" / "audio",
        "public/assets/images": creator_path / "public" / "assets" / "images",
        "src": creator_path / "src",
    }
    
    all_folders_exist = True
    for name, path in required_folders.items():
        if path.exists():
            print(f"   ✓ {name}")
        else:
            print(f"   ✗ {name} (missing)")
            all_folders_exist = False
    
    # Check Node.js
    print("\n5. Checking Node.js/npm...")
    try:
        import subprocess
        result = subprocess.run(["npm", "--version"], capture_output=True, text=True, shell=True)
        if result.returncode == 0:
            npm_version = result.stdout.strip()
            print(f"   ✓ npm version {npm_version}")
        else:
            print("   ✗ npm not found")
            print("   Install Node.js from: https://nodejs.org/")
            return False
    except Exception as e:
        print(f"   ✗ Error checking npm: {e}")
        return False
    
    # Check node_modules
    print("\n6. Checking Node.js dependencies...")
    node_modules = creator_path / "node_modules"
    if node_modules.exists():
        print("   ✓ node_modules folder exists")
    else:
        print("   ⚠ node_modules not found")
        print("   Run: npm install (from creator folder)")
    
    # Summary
    print("\n" + "="*40)
    if all_files_exist and all_folders_exist:
        print("✓ All checks passed!")
        print("\nYou can start the GUI with:")
        print("  python video_generator_gui.py")
        print("\nOr double-click:")
        print("  start_gui.bat (Windows)")
        return True
    else:
        print("✗ Some checks failed")
        print("Please fix the issues above")
        return False

if __name__ == "__main__":
    success = test_gui_setup()
    print()
    input("Press Enter to exit...")
    sys.exit(0 if success else 1)
