"""
Main entry point for the Pose-to-Meme Matcher application.
"""

import sys
import os
import cv2

# Make sure src/ is on the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

from pose.detector import PoseDetector
from pose.gestures import GestureRecognizer
from meme.manager import MemeManager
from ui.app_window import AppWindow


def main():
    print("🎭 Pose-to-Meme Matcher")
    print("=" * 40)

    # Verify webcam before launching UI
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error: Could not open webcam.")
        print("  1. Check webcam is connected.")
        print("  2. Close other apps using the camera.")
        print("  3. Grant camera permissions.")
        return
    cap.release()

    base_dir = os.path.dirname(__file__)
    memes_dir = os.path.join(base_dir, "memes")
    config_path = os.path.join(base_dir, "config", "gestures.json")

    print("Initialising components...")
    detector = PoseDetector(camera_index=0)
    recognizer = GestureRecognizer(detector, config_path=config_path)

    print("Scanning memes...")
    meme_mgr = MemeManager(memes_dir)
    stats = meme_mgr.get_stats()
    print(f"Loaded {stats['total_memes']} meme(s) across {len(stats['gestures'])} gesture(s).")

    print("Launching window — strike a pose!\n")
    app = AppWindow(detector, recognizer, meme_mgr)
    app.run()


if __name__ == "__main__":
    main()
