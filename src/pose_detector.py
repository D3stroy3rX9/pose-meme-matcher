"""
Pose detection using MediaPipe Pose.
"""

import cv2
import mediapipe as mp
import numpy as np


class PoseDetector:
    def __init__(self):
        self.mp_pose = mp.solutions.pose
        self.pose = self.mp_pose.Pose(
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5,
            model_complexity=1  # 0=lite, 1=full, 2=heavy
        )
        self.mp_drawing = mp.solutions.drawing_utils
        
    def detect(self, frame):
        """
        Detect pose landmarks in frame.
        
        Args:
            frame: BGR image from webcam
            
        Returns:
            results: MediaPipe pose results object
            annotated_frame: Frame with pose landmarks drawn
        """
        # Convert BGR to RGB
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        # Process the frame
        results = self.pose.process(rgb_frame)
        
        # Draw landmarks on frame
        annotated_frame = frame.copy()
        if results.pose_landmarks:
            self.mp_drawing.draw_landmarks(
                annotated_frame,
                results.pose_landmarks,
                self.mp_pose.POSE_CONNECTIONS,
                self.mp_drawing.DrawingSpec(color=(0, 255, 0), thickness=2, circle_radius=2),
                self.mp_drawing.DrawingSpec(color=(0, 0, 255), thickness=2)
            )
        
        return results, annotated_frame
    
    def get_landmark(self, results, landmark_id):
        """
        Get specific landmark coordinates.
        
        Args:
            results: MediaPipe pose results
            landmark_id: Landmark index (e.g., 15 for left wrist)
            
        Returns:
            (x, y, z, visibility) tuple or None if not detected
        """
        if not results.pose_landmarks:
            return None
            
        landmark = results.pose_landmarks.landmark[landmark_id]
        return (landmark.x, landmark.y, landmark.z, landmark.visibility)
    
    def calculate_angle(self, point1, point2, point3):
        """
        Calculate angle between three points.
        
        Args:
            point1, point2, point3: (x, y) tuples
            
        Returns:
            Angle in degrees
        """
        a = np.array(point1)
        b = np.array(point2)
        c = np.array(point3)
        
        ba = a - b
        bc = c - b
        
        cosine_angle = np.dot(ba, bc) / (np.linalg.norm(ba) * np.linalg.norm(bc))
        angle = np.arccos(np.clip(cosine_angle, -1.0, 1.0))
        
        return np.degrees(angle)
    
    def get_distance(self, point1, point2):
        """
        Calculate Euclidean distance between two points.
        
        Args:
            point1, point2: (x, y) tuples
            
        Returns:
            Distance
        """
        return np.linalg.norm(np.array(point1) - np.array(point2))
    
    def close(self):
        """Release resources."""
        self.pose.close()
