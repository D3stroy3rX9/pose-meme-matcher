# 🛠️ Development Guide

This guide is for understanding and extending the codebase.

## Architecture Overview

```
┌─────────────────────────────────────────────────┐
│                   main.py                        │
│         (Entry point & orchestration)            │
└─────────────────────────────────────────────────┘
                      │
        ┌─────────────┼─────────────┐
        │             │             │
        ▼             ▼             ▼
┌─────────────┐ ┌──────────┐ ┌────────────┐
│ AppWindow   │ │  Pose    │ │   Meme     │
│   (UI)      │ │ Detector │ │  Manager   │
└─────────────┘ └──────────┘ └────────────┘
        │             │             │
        │             ▼             │
        │      ┌──────────┐         │
        │      │ Gesture  │         │
        │      │Recognizer│         │
        │      └──────────┘         │
        │             │             │
        └─────────────┴─────────────┘
                      │
                      ▼
              ┌─────────────┐
              │   Display   │
              │   Webcam    │
              │   + Meme    │
              └─────────────┘
```

## Module Responsibilities

### `main.py`
- Application entry point
- Initializes all components
- Manages the main update loop
- Handles shutdown

### `src/ui/app_window.py`
- Creates and manages the GUI window
- Split-screen layout (webcam | meme)
- Updates display elements
- Status bar management

### `src/pose/detector.py`
- Wraps MediaPipe Pose
- Captures webcam frames
- Detects pose landmarks
- Draws skeleton overlay

### `src/pose/gestures.py`
- Analyzes pose landmarks
- Recognizes specific gestures
- Calculates confidence scores
- Uses keypoint geometry (angles, distances)

### `src/meme/manager.py`
- Scans meme directories
- Indexes memes by gesture
- Selects random matching memes
- Provides meme statistics

## Key Data Flow

1. **Webcam Frame Capture**
   ```
   PoseDetector.get_frame_with_pose()
   → Returns (frame, landmarks)
   ```

2. **Gesture Recognition**
   ```
   GestureRecognizer.recognize_gesture(landmarks)
   → Returns (gesture_name, confidence)
   ```

3. **Meme Selection**
   ```
   MemeManager.get_meme_for_gesture(gesture_name)
   → Returns meme_path
   ```

4. **Display Update**
   ```
   AppWindow.update_webcam_frame(frame)
   AppWindow.update_meme_display(meme_path)
   AppWindow.update_status(gesture_name, confidence)
   ```

## MediaPipe Landmarks

MediaPipe Pose provides 33 body landmarks:

```
Key landmarks for gesture detection:
- 0: Nose
- 11, 12: Shoulders
- 13, 14: Elbows
- 15, 16: Wrists
- 17, 18: Pinkies
- 19, 20: Index fingers
- 21, 22: Thumbs
- 23, 24: Hips

Each landmark has:
- x: horizontal position (0-1)
- y: vertical position (0-1)
- z: depth (relative to hips)
- visibility: confidence score
```

## Gesture Detection Techniques

### Angle-based Detection
Calculate angles between joints to detect poses:
```python
def _calculate_angle(p1, p2, p3):
    """
    Calculate angle at p2 formed by p1-p2-p3
    Useful for detecting bent/straight limbs
    """
    # Convert to vectors
    # Calculate angle using dot product
    # Return angle in degrees
```

### Distance-based Detection
Measure distances between landmarks:
```python
def _calculate_distance(p1, p2):
    """
    Euclidean distance between two points
    Useful for detecting proximity (hand near face, etc.)
    """
    # Calculate sqrt((x1-x2)² + (y1-y2)²)
```

### Position-based Detection
Compare relative positions:
```python
# Is left wrist higher than left shoulder?
if landmarks[15].y < landmarks[11].y:
    # Arm is raised
```

## Adding a New Gesture

### Step 1: Create Meme Folder
```bash
mkdir memes/your_gesture_name
```

### Step 2: Add to Config
Edit `config/gestures.json`:
```json
"your_gesture_name": {
  "description": "Your gesture description",
  "enabled": true,
  "confidence_threshold": 0.7,
  "cooldown_ms": 500
}
```

### Step 3: Implement Detection
In `src/pose/gestures.py`:
```python
def _detect_your_gesture(self, landmarks):
    """Detect your custom gesture."""
    # Extract relevant landmarks
    left_wrist = landmarks[15]
    right_wrist = landmarks[16]
    # ... more landmarks
    
    # Apply detection logic
    # Calculate angles, distances, positions
    
    # Return confidence (0.0 - 1.0)
    return confidence_score
```

### Step 4: Add to Recognition Loop
In `recognize_gesture()` method:
```python
gestures_to_check = [
    ('arms_crossed', self._detect_arms_crossed),
    ('thumbs_up', self._detect_thumbs_up),
    # Add your gesture here:
    ('your_gesture_name', self._detect_your_gesture),
]
```

## Configuration System

`config/gestures.json` structure:
```json
{
  "gestures": {
    "gesture_name": {
      "description": "Human-readable description",
      "enabled": true/false,
      "confidence_threshold": 0.0-1.0,
      "cooldown_ms": milliseconds
    }
  },
  "settings": {
    "update_interval_ms": 100,
    "min_detection_confidence": 0.5,
    "min_tracking_confidence": 0.5,
    "camera_index": 0,
    "camera_width": 640,
    "camera_height": 480
  }
}
```

## Performance Optimization Tips

1. **Reduce update frequency** if lagging
   - Increase `update_interval_ms` in config
   
2. **Lower camera resolution**
   - Decrease `camera_width` and `camera_height`
   
3. **Optimize gesture detection**
   - Return early if obvious non-match
   - Cache calculations when possible
   
4. **Efficient meme loading**
   - Preload commonly used memes
   - Resize images once, not every frame

## Testing Components Independently

Each module can be tested separately:

```bash
# Test pose detector
python -m src.pose.detector

# Test gesture recognizer
python -m src.pose.gestures

# Test meme manager
python -m src.meme.manager

# Test UI
python -m src.ui.app_window
```

## Debugging Tips

1. **Print landmarks to console**
   ```python
   for idx, landmark in enumerate(landmarks):
       print(f"{idx}: x={landmark.x:.2f}, y={landmark.y:.2f}")
   ```

2. **Visualize detection zones**
   - Draw circles/rectangles on frame
   - Show angle calculations visually

3. **Log confidence scores**
   - Print all gesture confidences
   - Identify which gestures are competing

4. **Check meme index**
   ```python
   print(meme_manager.get_stats())
   ```

## Future Enhancements

Ideas for expansion:
- [ ] Hot-reload memes without restart
- [ ] Multiple meme sets (themes)
- [ ] Gesture customization UI
- [ ] Recording mode (save gesture videos)
- [ ] Multiplayer mode (side-by-side)
- [ ] Meme history / replay
- [ ] Custom gesture trainer
- [ ] Mobile app version
- [ ] Web version with WebRTC

## Resources

- **MediaPipe Pose**: https://google.github.io/mediapipe/solutions/pose.html
- **Tkinter Docs**: https://docs.python.org/3/library/tkinter.html
- **OpenCV Docs**: https://docs.opencv.org/

---

Happy coding! 🚀
