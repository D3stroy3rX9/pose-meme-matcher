"""
Meme collection manager.
"""

import random
from pathlib import Path


class MemeManager:
    """Manages the meme collection — scanning, indexing, and random selection."""

    SUPPORTED = {'.png', '.jpg', '.jpeg', '.gif', '.bmp', '.webp'}

    def __init__(self, memes_dir="memes"):
        self.memes_dir = Path(memes_dir)
        self.meme_index = {}
        self._scan_memes()

    def _scan_memes(self):
        """Scan the memes directory and build a gesture → [paths] index."""
        self.meme_index = {}

        if not self.memes_dir.exists():
            print(f"Warning: memes directory not found: {self.memes_dir}")
            return

        for gesture_dir in self.memes_dir.iterdir():
            if not gesture_dir.is_dir():
                continue
            name = gesture_dir.name
            files = [
                str(f.resolve())
                for f in gesture_dir.iterdir()
                if f.suffix.lower() in self.SUPPORTED
            ]
            self.meme_index[name] = files
            status = f"{len(files)} meme(s)" if files else "empty"
            print(f"  {name}: {status}")

    def get_meme_for_gesture(self, gesture_name):
        """
        Return a random meme path for the given gesture, falling back to default.

        Returns:
            str path or None
        """
        if gesture_name and gesture_name in self.meme_index and self.meme_index[gesture_name]:
            return random.choice(self.meme_index[gesture_name])
        return self.get_default_meme()

    def get_default_meme(self):
        """Return a random meme from the 'default' folder."""
        defaults = self.meme_index.get("default", [])
        return random.choice(defaults) if defaults else None

    def get_stats(self):
        """Return dict with total count and per-gesture breakdown."""
        gestures = {k: len(v) for k, v in self.meme_index.items()}
        return {
            "total_memes": sum(gestures.values()),
            "gestures": gestures,
        }

    def reload(self):
        """Re-scan the meme directory (hot-reload support)."""
        print("Reloading memes...")
        self._scan_memes()
        stats = self.get_stats()
        print(f"Loaded {stats['total_memes']} meme(s) across {len(stats['gestures'])} gesture(s).")


if __name__ == "__main__":
    mgr = MemeManager()
    print(mgr.get_stats())
