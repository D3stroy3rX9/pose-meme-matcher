"""
Gesture pattern definitions for pose recognition.

Each gesture is defined by keypoint relationships and angles.
MediaPipe Pose landmarks: https://google.github.io/mediapipe/solutions/pose.html

Key landmarks used:
- 0: nose
- 11, 12: shoulders (left, right)
- 13, 14: elbows (left, right)
- 15, 16: wrists (left, right)
- 19, 20: index fingers (left, right)
- 23, 24: hips (left, right)
"""

GESTURES = {
    "thumbs_up": {
        "description": "One or both thumbs pointing up",
        "conditions": [
            # Wrist above shoulder, thumb extended
            "wrist_above_shoulder",
            "thumb_extended"
        ],
        "min_confidence": 0.7
    },
    
    "peace_sign": {
        "description": "Peace/Victory sign with fingers",
        "conditions": [
            # Hand near face, fingers in V shape
            "hand_near_face",
            "fingers_spread"
        ],
        "min_confidence": 0.7
    },
    
    "facepalm": {
        "description": "Hand covering face",
        "conditions": [
            # Wrist near nose, palm facing face
            "hand_on_face"
        ],
        "min_confidence": 0.75
    },
    
    "thinking": {
        "description": "Hand on chin or near face (thinking pose)",
        "conditions": [
            # Wrist near chin area
            "hand_near_chin"
        ],
        "min_confidence": 0.7
    },
    
    "arms_crossed": {
        "description": "Arms crossed over chest",
        "conditions": [
            # Wrists crossed in front of chest
            "wrists_crossed",
            "hands_near_opposite_shoulders"
        ],
        "min_confidence": 0.75
    },
    
    "shrug": {
        "description": "Shoulder shrug with palms up",
        "conditions": [
            # Shoulders raised, palms facing up
            "shoulders_raised",
            "palms_up"
        ],
        "min_confidence": 0.7
    },
    
    "salute": {
        "description": "Military salute",
        "conditions": [
            # Hand near forehead/temple
            "hand_near_forehead"
        ],
        "min_confidence": 0.75
    }
}

# Confidence threshold for pose detection
POSE_CONFIDENCE_THRESHOLD = 0.5

# Cooldown between gesture changes (seconds)
GESTURE_CHANGE_COOLDOWN = 0.8

# Default gesture when nothing is detected
DEFAULT_GESTURE = "default"
