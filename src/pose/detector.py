"""
MediaPipe pose detection wrapper (Tasks API — mediapipe 0.10+).
"""

import os
import cv2
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
import numpy as np

# MediaPipe pose landmark connections (same indices as the old solutions API)
POSE_CONNECTIONS = [
    (0,1),(1,2),(2,3),(3,7),(0,4),(4,5),(5,6),(6,8),  # face
    (9,10),                                             # mouth
    (11,12),                                            # shoulders
    (11,13),(13,15),(15,17),(15,19),(15,21),            # left arm
    (12,14),(14,16),(16,18),(16,20),(16,22),            # right arm
    (11,23),(12,24),(23,24),                            # torso
    (23,25),(25,27),(27,29),(29,31),(27,31),            # left leg
    (24,26),(26,28),(28,30),(30,32),(28,32),            # right leg
]

# Default model path — relative to this file's package root
_DEFAULT_MODEL = os.path.join(
    os.path.dirname(__file__), "..", "..", "models", "pose_landmarker.task"
)


class PoseDetector:
    """Webcam capture + MediaPipe Pose Landmarker (Tasks API)."""

    def __init__(self, camera_index=0, model_path=None,
                 min_detection_confidence=0.5, min_tracking_confidence=0.5):
        model_path = os.path.abspath(model_path or _DEFAULT_MODEL)

        options = vision.PoseLandmarkerOptions(
            base_options=python.BaseOptions(model_asset_path=model_path),
            running_mode=vision.RunningMode.IMAGE,
            min_pose_detection_confidence=min_detection_confidence,
            min_pose_presence_confidence=min_detection_confidence,
            min_tracking_confidence=min_tracking_confidence,
        )
        self.landmarker = vision.PoseLandmarker.create_from_options(options)
        self.cap = cv2.VideoCapture(camera_index)

    def get_frame_with_pose(self):
        """
        Capture a webcam frame, run pose detection, draw landmarks.

        Returns:
            (annotated_frame, result) — frame is BGR, result is PoseLandmarkerResult.
            Returns (None, None) on failure.
        """
        ret, frame = self.cap.read()
        if not ret:
            return None, None

        frame = cv2.flip(frame, 1)
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb)
        result = self.landmarker.detect(mp_image)

        annotated = frame.copy()
        if result.pose_landmarks:
            landmarks = result.pose_landmarks[0]
            h, w = frame.shape[:2]
            # Draw connections
            for a, b in POSE_CONNECTIONS:
                if a < len(landmarks) and b < len(landmarks):
                    lm_a, lm_b = landmarks[a], landmarks[b]
                    if lm_a.visibility > 0.5 and lm_b.visibility > 0.5:
                        cv2.line(annotated,
                                 (int(lm_a.x * w), int(lm_a.y * h)),
                                 (int(lm_b.x * w), int(lm_b.y * h)),
                                 (0, 0, 255), 2)
            # Draw landmark dots
            for lm in landmarks:
                if lm.visibility > 0.5:
                    cv2.circle(annotated,
                               (int(lm.x * w), int(lm.y * h)),
                               4, (0, 255, 0), -1)

        return annotated, result

    def get_landmark(self, results, landmark_id):
        """Return (x, y, z, visibility) for a specific landmark, or None."""
        if not results or not results.pose_landmarks:
            return None
        landmarks = results.pose_landmarks[0]
        if landmark_id >= len(landmarks):
            return None
        lm = landmarks[landmark_id]
        return (lm.x, lm.y, lm.z, lm.visibility)

    def calculate_angle(self, point1, point2, point3):
        """Angle in degrees at point2 formed by point1–point2–point3."""
        a, b, c = np.array(point1), np.array(point2), np.array(point3)
        ba, bc = a - b, c - b
        cosine = np.dot(ba, bc) / (np.linalg.norm(ba) * np.linalg.norm(bc))
        return float(np.degrees(np.arccos(np.clip(cosine, -1.0, 1.0))))

    def get_distance(self, point1, point2):
        """Euclidean distance between two (x, y) points."""
        return float(np.linalg.norm(np.array(point1) - np.array(point2)))

    def is_open(self):
        return self.cap.isOpened()

    def release(self):
        if self.cap.isOpened():
            self.cap.release()
        self.landmarker.close()
