#!/usr/bin/env python3
"""
Asset Cleanup Script
Deletes files in the following directories (excluding .py and .js files):
- creator/public/assets/audio
- creator/public/assets/images  
- creator/out
- backend/transcribe
"""

import os
import sys
from pathlib import Path
import shutil


def get_project_root():
    """Get the project root directory (parent of backend folder)"""
    current_dir = Path(__file__).parent
    return current_dir.parent


def delete_files_in_directory(directory_path, description):
    """Delete all files in a directory, keeping the directory structure intact"""
    if not directory_path.exists():
        print(f"⚠️  Directory does not exist: {directory_path}")
        return 0
    
    if not directory_path.is_dir():
        print(f"⚠️  Path is not a directory: {directory_path}")
        return 0
    
    # Get all files but exclude .py and .js files
    files = [f for f in directory_path.iterdir() 
             if f.is_file() and f.suffix.lower() not in ['.py', '.js']]
    
    if not files:
        print(f"✅ No files to delete in {description}")
        return 0
    
    print(f"\n📁 {description}:")
    for file in files:
        print(f"   - {file.name}")
    
    deleted_count = 0
    for file in files:
        try:
            file.unlink()
            print(f"🗑️  Deleted: {file.name}")
            deleted_count += 1
        except Exception as e:
            print(f"❌ Failed to delete {file.name}: {e}")
    
    return deleted_count


def main():
    """Main cleanup function"""
    project_root = get_project_root()
    
    # Define directories to clean
    directories_to_clean = [
        {
            "path": project_root / "creator" / "public" / "assets" / "audio",
            "description": "Audio assets"
        },
        {
            "path": project_root / "creator" / "public" / "assets" / "images", 
            "description": "Image assets"
        },
        {
            "path": project_root / "creator" / "out",
            "description": "Output files"
        },
        {
            "path": project_root / "backend" / "transcribe",
            "description": "Transcribe files"
        }
    ]
    
    print("🧹 Asset Cleanup Script")
    print("=" * 50)
    
    # Show what will be deleted
    total_files = 0
    for dir_info in directories_to_clean:
        dir_path = dir_info["path"]
        if dir_path.exists() and dir_path.is_dir():
            files = [f for f in dir_path.iterdir() 
                    if f.is_file() and f.suffix.lower() not in ['.py', '.js']]
            total_files += len(files)
            if files:
                print(f"\n📁 {dir_info['description']} ({dir_path}):")
                for file in files:
                    print(f"   - {file.name}")
    
    if total_files == 0:
        print("\n✅ No files found to delete.")
        return
    
    print(f"\n📊 Total files to delete: {total_files}")
    
    # Confirmation prompt
    response = input("\n❓ Do you want to proceed with deletion? (y/N): ").strip().lower()
    if response not in ['y', 'yes']:
        print("❌ Operation cancelled.")
        return
    
    print("\n🚀 Starting cleanup...")
    
    # Perform cleanup
    total_deleted = 0
    for dir_info in directories_to_clean:
        deleted = delete_files_in_directory(dir_info["path"], dir_info["description"])
        total_deleted += deleted
    
    print(f"\n✅ Cleanup completed! Deleted {total_deleted} files.")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n❌ Operation cancelled by user.")
        sys.exit(1)
    except Exception as e:
        print(f"\n💥 An error occurred: {e}")
        sys.exit(1)