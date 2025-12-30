"""
Main application - Pose Meme Matcher
"""

import cv2
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import os
import sys

# Add src directory to path
sys.path.insert(0, os.path.dirname(__file__))

from pose_detector import PoseDetector
from gesture_recognizer import GestureRecognizer
from meme_manager import MemeManager


class PoseMemeMatcherApp:
    def __init__(self, root):
        self.root = root
        self.root.title("🎭 Pose Meme Matcher")
        self.root.geometry("1400x700")
        self.root.configure(bg='#1e1e1e')
        
        # Initialize components
        self.pose_detector = PoseDetector()
        self.gesture_recognizer = GestureRecognizer(self.pose_detector)
        
        # Get memes directory (parent of src/)
        base_dir = os.path.dirname(os.path.dirname(__file__))
        memes_dir = os.path.join(base_dir, "memes")
        self.meme_manager = MemeManager(memes_dir)
        self.meme_manager.print_stats()
        
        # Webcam
        self.cap = cv2.VideoCapture(0)
        self.current_gesture = "default"
        self.current_meme_path = None
        
        # Create UI
        self.create_ui()
        
        # Start video loop
        self.update_frame()
        
    def create_ui(self):
        """Create the split-screen UI."""
        # Main container
        main_frame = tk.Frame(self.root, bg='#1e1e1e')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Left panel - Webcam feed
        left_panel = tk.Frame(main_frame, bg='#2d2d2d', relief=tk.RAISED, borderwidth=2)
        left_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5))
        
        left_label = tk.Label(left_panel, text="📹 Webcam Feed", 
                             bg='#2d2d2d', fg='#ffffff', 
                             font=('Arial', 14, 'bold'))
        left_label.pack(pady=10)
        
        self.webcam_label = tk.Label(left_panel, bg='#000000')
        self.webcam_label.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Right panel - Meme display
        right_panel = tk.Frame(main_frame, bg='#2d2d2d', relief=tk.RAISED, borderwidth=2)
        right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(5, 0))
        
        right_label = tk.Label(right_panel, text="🎭 Matched Meme", 
                              bg='#2d2d2d', fg='#ffffff', 
                              font=('Arial', 14, 'bold'))
        right_label.pack(pady=10)
        
        self.meme_label = tk.Label(right_panel, bg='#1a1a1a', 
                                   text="Strike a pose!", 
                                   fg='#888888',
                                   font=('Arial', 24))
        self.meme_label.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Gesture indicator
        self.gesture_indicator = tk.Label(right_panel, 
                                         text="Gesture: None detected",
                                         bg='#2d2d2d', fg='#00ff00',
                                         font=('Arial', 12, 'bold'))
        self.gesture_indicator.pack(pady=10)
        
        # Bottom controls
        control_frame = tk.Frame(self.root, bg='#1e1e1e')
        control_frame.pack(fill=tk.X, padx=10, pady=(0, 10))
        
        reload_btn = tk.Button(control_frame, text="🔄 Reload Memes", 
                              command=self.reload_memes,
                              bg='#4a4a4a', fg='#ffffff',
                              font=('Arial', 10, 'bold'),
                              relief=tk.RAISED, borderwidth=2,
                              padx=15, pady=8)
        reload_btn.pack(side=tk.LEFT, padx=5)
        
        quit_btn = tk.Button(control_frame, text="❌ Quit", 
                           command=self.quit_app,
                           bg='#ff4444', fg='#ffffff',
                           font=('Arial', 10, 'bold'),
                           relief=tk.RAISED, borderwidth=2,
                           padx=15, pady=8)
        quit_btn.pack(side=tk.RIGHT, padx=5)
        
        self.fps_label = tk.Label(control_frame, text="FPS: --",
                                 bg='#1e1e1e', fg='#888888',
                                 font=('Arial', 9))
        self.fps_label.pack(side=tk.RIGHT, padx=10)
    
    def update_frame(self):
        """Main update loop - capture frame, detect pose, match meme."""
        ret, frame = self.cap.read()
        
        if ret:
            # Flip frame horizontally for mirror effect
            frame = cv2.flip(frame, 1)
            
            # Detect pose
            results, annotated_frame = self.pose_detector.detect(frame)
            
            # Recognize gesture
            gesture = self.gesture_recognizer.recognize(results)
            
            # Update meme if gesture changed
            if gesture != self.current_gesture:
                self.current_gesture = gesture
                self.update_meme(gesture)
            
            # Display webcam feed
            self.display_webcam(annotated_frame)
            
        # Schedule next update (30 FPS)
        self.root.after(33, self.update_frame)
    
    def display_webcam(self, frame):
        """Display webcam frame in left panel."""
        # Resize frame to fit panel
        display_frame = cv2.resize(frame, (640, 480))
        
        # Convert BGR to RGB
        rgb_frame = cv2.cvtColor(display_frame, cv2.COLOR_BGR2RGB)
        
        # Convert to PIL Image
        pil_image = Image.fromarray(rgb_frame)
        
        # Convert to PhotoImage
        photo = ImageTk.PhotoImage(image=pil_image)
        
        # Update label
        self.webcam_label.configure(image=photo)
        self.webcam_label.image = photo  # Keep reference
    
    def update_meme(self, gesture):
        """Update displayed meme based on detected gesture."""
        meme_path = self.meme_manager.get_meme(gesture)
        
        # Update gesture indicator
        gesture_display = gesture.replace('_', ' ').title()
        self.gesture_indicator.configure(text=f"Gesture: {gesture_display}")
        
        if meme_path and os.path.exists(meme_path):
            try:
                # Load and display meme
                meme_image = Image.open(meme_path)
                
                # Resize to fit panel while maintaining aspect ratio
                max_size = (600, 500)
                meme_image.thumbnail(max_size, Image.Resampling.LANCZOS)
                
                photo = ImageTk.PhotoImage(meme_image)
                
                self.meme_label.configure(image=photo, text="")
                self.meme_label.image = photo  # Keep reference
                
                self.current_meme_path = meme_path
            except Exception as e:
                print(f"Error loading meme: {e}")
                self.show_placeholder(f"Error loading meme\n{gesture_display}")
        else:
            # Show placeholder
            self.show_placeholder(f"No meme found for:\n{gesture_display}")
    
    def show_placeholder(self, text):
        """Show placeholder text when no meme is available."""
        self.meme_label.configure(image='', text=text, 
                                 fg='#888888', font=('Arial', 18))
        self.meme_label.image = None
    
    def reload_memes(self):
        """Reload meme index."""
        self.meme_manager.reload_memes()
        self.meme_manager.print_stats()
        
        # Refresh current meme
        self.update_meme(self.current_gesture)
    
    def quit_app(self):
        """Clean up and quit."""
        self.cap.release()
        self.pose_detector.close()
        self.root.destroy()


def main():
    """Entry point."""
    # Check if webcam is available
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error: Could not open webcam!")
        print("Please check if:")
        print("  1. Webcam is connected")
        print("  2. Another application is using the webcam")
        print("  3. You have camera permissions enabled")
        return
    cap.release()
    
    # Create and run app
    root = tk.Tk()
    app = PoseMemeMatcherApp(root)
    
    # Handle window close
    root.protocol("WM_DELETE_WINDOW", app.quit_app)
    
    root.mainloop()


if __name__ == "__main__":
    main()
