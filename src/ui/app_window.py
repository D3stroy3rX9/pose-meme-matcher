"""
Main application window — pure OpenCV display (no Tkinter).
Left half: webcam feed with pose overlay.
Right half: matched meme.
"""

import cv2
import numpy as np
from PIL import Image
import os


# Display dimensions
CAM_W, CAM_H = 640, 480
MEME_W, MEME_H = 640, 480
WIN_W = CAM_W + MEME_W
WIN_H = max(CAM_H, MEME_H) + 60          # +60 for status bar
WIN_NAME = "Pose Meme Matcher  |  press Q to quit"

# Colours (BGR)
BG       = (30, 30, 30)
TEXT_COL = (0, 255, 0)
HINT_COL = (150, 150, 150)


class AppWindow:
    """OpenCV-based split-screen application window."""

    def __init__(self, pose_detector, gesture_recognizer, meme_manager):
        self.detector   = pose_detector
        self.recognizer = gesture_recognizer
        self.meme_mgr   = meme_manager

        self.current_gesture = "default"
        self._meme_canvas    = self._placeholder_meme()
        self._canvas         = np.full((WIN_H, WIN_W, 3), BG, dtype=np.uint8)

        cv2.namedWindow(WIN_NAME, cv2.WINDOW_NORMAL)
        cv2.resizeWindow(WIN_NAME, WIN_W, WIN_H)

    # ── public API ────────────────────────────────────────────────────────────

    def update_webcam_frame(self, frame):
        """Resize and place the webcam frame on the left half of the canvas."""
        resized = cv2.resize(frame, (CAM_W, CAM_H))
        self._canvas[:CAM_H, :CAM_W] = resized

    def update_meme_display(self, meme_path):
        """Load, resize, and place a meme image on the right half."""
        if meme_path and os.path.exists(meme_path):
            try:
                img = Image.open(meme_path).convert("RGB")
                img.thumbnail((MEME_W, MEME_H), Image.Resampling.LANCZOS)
                arr = np.array(img)
                arr = cv2.cvtColor(arr, cv2.COLOR_RGB2BGR)

                # Centre the meme on a dark tile
                tile = np.full((MEME_H, MEME_W, 3), (20, 20, 20), dtype=np.uint8)
                yoff = (MEME_H - arr.shape[0]) // 2
                xoff = (MEME_W - arr.shape[1]) // 2
                tile[yoff:yoff+arr.shape[0], xoff:xoff+arr.shape[1]] = arr
                self._meme_canvas = tile
                return
            except Exception as e:
                print(f"Error loading meme: {e}")
        self._meme_canvas = self._placeholder_meme()

    def update_status(self, gesture_name, confidence=1.0):
        """Draw the status bar at the bottom of the canvas."""
        bar = np.full((60, WIN_W, 3), (45, 45, 45), dtype=np.uint8)
        label = gesture_name.replace("_", " ").upper() if gesture_name else "NONE"
        cv2.putText(bar, f"Gesture: {label}",
                    (20, 38), cv2.FONT_HERSHEY_SIMPLEX, 0.9, TEXT_COL, 2)
        cv2.putText(bar, "Q = quit   R = reload memes",
                    (WIN_W - 320, 38), cv2.FONT_HERSHEY_SIMPLEX, 0.6, HINT_COL, 1)
        self._canvas[CAM_H:, :] = bar

    # ── main loop ─────────────────────────────────────────────────────────────

    def run(self):
        """Capture → detect → display loop. Blocks until the user presses Q."""
        # Show initial status
        self.update_status(self.current_gesture)

        while True:
            frame, results = self.detector.get_frame_with_pose()
            if frame is not None:
                self.update_webcam_frame(frame)

                gesture, confidence = self.recognizer.recognize_gesture(results)
                if gesture != self.current_gesture:
                    self.current_gesture = gesture
                    meme_path = self.meme_mgr.get_meme_for_gesture(gesture)
                    self.update_meme_display(meme_path)
                    self.update_status(gesture, confidence)

            # Place meme on right half
            self._canvas[:MEME_H, CAM_W:CAM_W+MEME_W] = self._meme_canvas

            cv2.imshow(WIN_NAME, self._canvas)

            key = cv2.waitKey(1) & 0xFF
            if key == ord('q') or key == 27:   # Q or Esc
                break
            elif key == ord('r'):              # R = reload memes
                self.meme_mgr.reload()
                meme_path = self.meme_mgr.get_meme_for_gesture(self.current_gesture)
                self.update_meme_display(meme_path)

        self.quit()

    def quit(self):
        """Release resources."""
        self.detector.release()
        cv2.destroyAllWindows()

    # ── helpers ───────────────────────────────────────────────────────────────

    @staticmethod
    def _placeholder_meme():
        """Dark tile with 'Strike a pose!' text."""
        tile = np.full((MEME_H, MEME_W, 3), (25, 25, 25), dtype=np.uint8)
        cv2.putText(tile, "Strike a pose!",
                    (MEME_W//2 - 160, MEME_H//2),
                    cv2.FONT_HERSHEY_SIMPLEX, 1.2, (80, 80, 80), 2)
        return tile
