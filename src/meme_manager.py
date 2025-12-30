"""
Meme management - indexing and random selection.
"""

import os
import random
from pathlib import Path


class MemeManager:
    def __init__(self, memes_directory):
        self.memes_dir = Path(memes_directory)
        self.meme_index = {}
        self.supported_formats = {'.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp'}
        self.load_memes()
        
    def load_memes(self):
        """
        Scan memes directory and build index.
        Maps gesture names to list of meme file paths.
        """
        self.meme_index = {}
        
        if not self.memes_dir.exists():
            print(f"Warning: Memes directory not found: {self.memes_dir}")
            return
        
        # Scan each gesture subdirectory
        for gesture_dir in self.memes_dir.iterdir():
            if gesture_dir.is_dir():
                gesture_name = gesture_dir.name
                meme_files = []
                
                # Find all image files in this directory
                for file in gesture_dir.iterdir():
                    if file.suffix.lower() in self.supported_formats:
                        meme_files.append(str(file.absolute()))
                
                if meme_files:
                    self.meme_index[gesture_name] = meme_files
                    print(f"Loaded {len(meme_files)} meme(s) for gesture '{gesture_name}'")
                else:
                    print(f"Warning: No memes found for gesture '{gesture_name}'")
        
        # Create placeholder if default folder is empty
        if "default" not in self.meme_index or not self.meme_index["default"]:
            print("Warning: No default memes found. Using placeholder.")
            self.meme_index["default"] = []
    
    def get_meme(self, gesture_name):
        """
        Get a random meme for the given gesture.
        
        Args:
            gesture_name: Name of detected gesture
            
        Returns:
            Path to meme image file, or None if no meme available
        """
        # Try to get meme for specific gesture
        if gesture_name in self.meme_index and self.meme_index[gesture_name]:
            return random.choice(self.meme_index[gesture_name])
        
        # Fall back to default
        if "default" in self.meme_index and self.meme_index["default"]:
            return random.choice(self.meme_index["default"])
        
        return None
    
    def reload_memes(self):
        """Reload meme index (useful for hot-reloading new memes)."""
        print("Reloading memes...")
        self.load_memes()
    
    def get_gesture_count(self, gesture_name):
        """Get number of memes available for a gesture."""
        if gesture_name in self.meme_index:
            return len(self.meme_index[gesture_name])
        return 0
    
    def get_all_gestures(self):
        """Get list of all gestures with memes."""
        return list(self.meme_index.keys())
    
    def print_stats(self):
        """Print statistics about loaded memes."""
        print("\n=== Meme Statistics ===")
        total = 0
        for gesture, memes in self.meme_index.items():
            count = len(memes)
            total += count
            print(f"  {gesture}: {count} meme(s)")
        print(f"Total: {total} meme(s) loaded")
        print("=" * 25 + "\n")
