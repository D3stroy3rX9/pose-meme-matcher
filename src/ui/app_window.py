"""
Application window and GUI layout.

This module creates the main window with:
- Left side: Webcam feed with pose overlay
- Right side: Matched meme display
- Status bar with current gesture info
"""

import tkinter as tk
from tkinter import ttk


class AppWindow:
    """Main application window."""
    
    def __init__(self):
        """Initialize the application window."""
        # TODO: Create main window
        # TODO: Set up left panel (webcam)
        # TODO: Set up right panel (meme display)
        # TODO: Add status bar
        # TODO: Configure layout and styling
        pass
    
    def update_webcam_frame(self, frame):
        """Update the webcam display with a new frame."""
        # TODO: Convert OpenCV frame to Tkinter format
        # TODO: Update webcam canvas
        pass
    
    def update_meme_display(self, meme_path):
        """Update the meme display with a new image."""
        # TODO: Load image from path
        # TODO: Resize to fit panel
        # TODO: Update meme canvas
        pass
    
    def update_status(self, gesture_name, confidence):
        """Update status bar with current gesture info."""
        # TODO: Update status label
        pass
    
    def run(self):
        """Start the GUI event loop."""
        # TODO: Start Tkinter mainloop
        pass


# For testing the UI independently
if __name__ == "__main__":
    app = AppWindow()
    print("AppWindow class created (stub)")
