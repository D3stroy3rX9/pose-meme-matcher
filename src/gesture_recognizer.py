"""
Gesture recognition from pose landmarks.
"""

import time
from gesture_config import GESTURES, GESTURE_CHANGE_COOLDOWN, DEFAULT_GESTURE


class GestureRecognizer:
    def __init__(self, pose_detector):
        self.pose_detector = pose_detector
        self.current_gesture = DEFAULT_GESTURE
        self.last_change_time = 0
        
    def recognize(self, results):
        """
        Recognize gesture from pose landmarks.
        
        Args:
            results: MediaPipe pose results
            
        Returns:
            Detected gesture name (string)
        """
        if not results.pose_landmarks:
            return DEFAULT_GESTURE
        
        # Check cooldown
        current_time = time.time()
        if current_time - self.last_change_time < GESTURE_CHANGE_COOLDOWN:
            return self.current_gesture
        
        # Check each gesture
        for gesture_name, gesture_config in GESTURES.items():
            if self._check_gesture(results, gesture_name, gesture_config):
                if gesture_name != self.current_gesture:
                    self.current_gesture = gesture_name
                    self.last_change_time = current_time
                return gesture_name
        
        # No gesture detected
        if self.current_gesture != DEFAULT_GESTURE:
            self.current_gesture = DEFAULT_GESTURE
            self.last_change_time = current_time
        
        return DEFAULT_GESTURE
    
    def _check_gesture(self, results, gesture_name, gesture_config):
        """
        Check if pose matches a specific gesture.
        
        Args:
            results: MediaPipe pose results
            gesture_name: Name of gesture to check
            gesture_config: Configuration dict for gesture
            
        Returns:
            True if gesture is detected
        """
        conditions = gesture_config["conditions"]
        
        # Check all conditions for this gesture
        if gesture_name == "thumbs_up":
            return self._check_thumbs_up(results)
        elif gesture_name == "peace_sign":
            return self._check_peace_sign(results)
        elif gesture_name == "facepalm":
            return self._check_facepalm(results)
        elif gesture_name == "thinking":
            return self._check_thinking(results)
        elif gesture_name == "arms_crossed":
            return self._check_arms_crossed(results)
        elif gesture_name == "shrug":
            return self._check_shrug(results)
        elif gesture_name == "salute":
            return self._check_salute(results)
        
        return False
    
    def _check_thumbs_up(self, results):
        """Check for thumbs up gesture."""
        # Get landmarks
        left_wrist = self.pose_detector.get_landmark(results, 15)
        right_wrist = self.pose_detector.get_landmark(results, 16)
        left_shoulder = self.pose_detector.get_landmark(results, 11)
        right_shoulder = self.pose_detector.get_landmark(results, 12)
        
        if not all([left_wrist, right_wrist, left_shoulder, right_shoulder]):
            return False
        
        # Check if either wrist is significantly above shoulder
        left_above = left_wrist[1] < left_shoulder[1] - 0.1
        right_above = right_wrist[1] < right_shoulder[1] - 0.1
        
        # Check visibility
        left_visible = left_wrist[3] > 0.5
        right_visible = right_wrist[3] > 0.5
        
        return (left_above and left_visible) or (right_above and right_visible)
    
    def _check_peace_sign(self, results):
        """Check for peace/victory sign."""
        # Get landmarks
        left_wrist = self.pose_detector.get_landmark(results, 15)
        right_wrist = self.pose_detector.get_landmark(results, 16)
        nose = self.pose_detector.get_landmark(results, 0)
        
        if not all([left_wrist, right_wrist, nose]):
            return False
        
        # Check if either hand is near face (shoulder level or above)
        left_dist = self.pose_detector.get_distance(
            (left_wrist[0], left_wrist[1]), 
            (nose[0], nose[1])
        )
        right_dist = self.pose_detector.get_distance(
            (right_wrist[0], right_wrist[1]), 
            (nose[0], nose[1])
        )
        
        # Peace sign typically held near face
        near_face = (left_dist < 0.3 and left_wrist[3] > 0.5) or \
                    (right_dist < 0.3 and right_wrist[3] > 0.5)
        
        # Hand should be at face level or higher
        left_elevated = left_wrist[1] < nose[1] + 0.1
        right_elevated = right_wrist[1] < nose[1] + 0.1
        
        return near_face and (left_elevated or right_elevated)
    
    def _check_facepalm(self, results):
        """Check for facepalm gesture."""
        # Get landmarks
        left_wrist = self.pose_detector.get_landmark(results, 15)
        right_wrist = self.pose_detector.get_landmark(results, 16)
        nose = self.pose_detector.get_landmark(results, 0)
        
        if not all([left_wrist, right_wrist, nose]):
            return False
        
        # Check if hand is very close to face
        left_dist = self.pose_detector.get_distance(
            (left_wrist[0], left_wrist[1]), 
            (nose[0], nose[1])
        )
        right_dist = self.pose_detector.get_distance(
            (right_wrist[0], right_wrist[1]), 
            (nose[0], nose[1])
        )
        
        # Facepalm: hand very close to face
        return (left_dist < 0.15 and left_wrist[3] > 0.5) or \
               (right_dist < 0.15 and right_wrist[3] > 0.5)
    
    def _check_thinking(self, results):
        """Check for thinking pose (hand on chin)."""
        # Get landmarks
        left_wrist = self.pose_detector.get_landmark(results, 15)
        right_wrist = self.pose_detector.get_landmark(results, 16)
        nose = self.pose_detector.get_landmark(results, 0)
        left_shoulder = self.pose_detector.get_landmark(results, 11)
        right_shoulder = self.pose_detector.get_landmark(results, 12)
        
        if not all([left_wrist, right_wrist, nose, left_shoulder, right_shoulder]):
            return False
        
        # Check if hand is near chin/lower face area
        chin_y = nose[1] + 0.08  # Approximate chin position
        
        left_near_chin = abs(left_wrist[1] - chin_y) < 0.1 and \
                         abs(left_wrist[0] - nose[0]) < 0.2 and \
                         left_wrist[3] > 0.5
        
        right_near_chin = abs(right_wrist[1] - chin_y) < 0.1 and \
                          abs(right_wrist[0] - nose[0]) < 0.2 and \
                          right_wrist[3] > 0.5
        
        return left_near_chin or right_near_chin
    
    def _check_arms_crossed(self, results):
        """Check for arms crossed gesture."""
        # Get landmarks
        left_wrist = self.pose_detector.get_landmark(results, 15)
        right_wrist = self.pose_detector.get_landmark(results, 16)
        left_shoulder = self.pose_detector.get_landmark(results, 11)
        right_shoulder = self.pose_detector.get_landmark(results, 12)
        
        if not all([left_wrist, right_wrist, left_shoulder, right_shoulder]):
            return False
        
        # Check if wrists are crossed (left wrist on right side, right wrist on left side)
        left_crossed = left_wrist[0] > nose[0] if 'nose' in locals() else left_wrist[0] > 0.5
        right_crossed = right_wrist[0] < nose[0] if 'nose' in locals() else right_wrist[0] < 0.5
        
        # Alternative: check if hands are near opposite shoulders
        left_to_right_shoulder = self.pose_detector.get_distance(
            (left_wrist[0], left_wrist[1]),
            (right_shoulder[0], right_shoulder[1])
        )
        right_to_left_shoulder = self.pose_detector.get_distance(
            (right_wrist[0], right_wrist[1]),
            (left_shoulder[0], left_shoulder[1])
        )
        
        hands_crossed = (left_to_right_shoulder < 0.2 and right_to_left_shoulder < 0.2) or \
                       (left_wrist[0] > right_wrist[0] + 0.1)
        
        # Both hands should be visible and at chest level
        chest_level = 0.3 < left_wrist[1] < 0.7 and 0.3 < right_wrist[1] < 0.7
        both_visible = left_wrist[3] > 0.5 and right_wrist[3] > 0.5
        
        return hands_crossed and chest_level and both_visible
    
    def _check_shrug(self, results):
        """Check for shrug gesture."""
        # Get landmarks
        left_wrist = self.pose_detector.get_landmark(results, 15)
        right_wrist = self.pose_detector.get_landmark(results, 16)
        left_shoulder = self.pose_detector.get_landmark(results, 11)
        right_shoulder = self.pose_detector.get_landmark(results, 12)
        left_elbow = self.pose_detector.get_landmark(results, 13)
        right_elbow = self.pose_detector.get_landmark(results, 14)
        
        if not all([left_wrist, right_wrist, left_shoulder, right_shoulder, left_elbow, right_elbow]):
            return False
        
        # Hands should be raised, palms up (wrists at or above shoulder level)
        hands_raised = (left_wrist[1] <= left_shoulder[1] + 0.05) and \
                      (right_wrist[1] <= right_shoulder[1] + 0.05)
        
        # Hands should be out to the sides
        hands_wide = abs(left_wrist[0] - right_wrist[0]) > 0.3
        
        # Both hands visible
        both_visible = left_wrist[3] > 0.5 and right_wrist[3] > 0.5
        
        return hands_raised and hands_wide and both_visible
    
    def _check_salute(self, results):
        """Check for salute gesture."""
        # Get landmarks
        left_wrist = self.pose_detector.get_landmark(results, 15)
        right_wrist = self.pose_detector.get_landmark(results, 16)
        nose = self.pose_detector.get_landmark(results, 0)
        
        if not all([left_wrist, right_wrist, nose]):
            return False
        
        # Hand near forehead/temple area
        forehead_y = nose[1] - 0.1  # Above nose
        
        # Check left hand
        left_salute = abs(left_wrist[1] - forehead_y) < 0.08 and \
                     abs(left_wrist[0] - nose[0]) < 0.2 and \
                     left_wrist[3] > 0.5
        
        # Check right hand
        right_salute = abs(right_wrist[1] - forehead_y) < 0.08 and \
                      abs(right_wrist[0] - nose[0]) < 0.2 and \
                      right_wrist[3] > 0.5
        
        return left_salute or right_salute
