"""
Meme collection manager.

This module handles:
- Scanning meme folders
- Indexing memes by gesture type
- Random selection from matching memes
- Hot-reloading (future feature)
"""

import os
import random
from pathlib import Path


class MemeManager:
    """Manages the meme collection."""
    
    def __init__(self, memes_dir="memes"):
        """
        Initialize the meme manager.
        
        Args:
            memes_dir: Path to the memes directory
        """
        self.memes_dir = Path(memes_dir)
        self.meme_index = {}
        self.supported_formats = ['.png', '.jpg', '.jpeg', '.gif']
        
        # TODO: Scan and index all memes
        self._scan_memes()
    
    def _scan_memes(self):
        """Scan the memes directory and build an index."""
        # TODO: Walk through each gesture subfolder
        # TODO: Find all image files
        # TODO: Build index: {gesture_name: [list of image paths]}
        
        print(f"Scanning memes directory: {self.memes_dir}")
        
        if not self.memes_dir.exists():
            print(f"Warning: Memes directory not found: {self.memes_dir}")
            return
        
        # TODO: Implement scanning logic
        pass
    
    def get_meme_for_gesture(self, gesture_name):
        """
        Get a random meme for the specified gesture.
        
        Args:
            gesture_name: Name of the gesture (e.g., 'thumbs_up')
            
        Returns:
            str: Path to a meme image, or None if no memes found for this gesture
        """
        # TODO: Look up gesture in index
        # TODO: Randomly select one meme if multiple available
        # TODO: Return path
        
        # If gesture not found or no memes, try default
        if gesture_name is None or gesture_name not in self.meme_index:
            return self.get_default_meme()
        
        return None
    
    def get_default_meme(self):
        """Get a random meme from the default folder."""
        # TODO: Return random meme from 'default' gesture
        return None
    
    def get_stats(self):
        """
        Get statistics about the meme collection.
        
        Returns:
            dict: Statistics like total memes, memes per gesture, etc.
        """
        # TODO: Calculate and return stats
        stats = {
            'total_memes': 0,
            'gestures': {},
        }
        return stats
    
    def reload(self):
        """Reload the meme index (for hot-reloading feature)."""
        # TODO: Clear current index
        # TODO: Re-scan memes directory
        self._scan_memes()


# For testing the meme manager independently
if __name__ == "__main__":
    print("MemeManager class created (stub)")
    print("This will scan and index your meme collection")
    
    # Test instantiation
    manager = MemeManager()
    print(f"Stats: {manager.get_stats()}")
