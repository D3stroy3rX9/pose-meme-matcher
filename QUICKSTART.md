# ⚡ Quick Start Guide

Get up and running in 5 minutes!

## Step 1: Install Dependencies

```bash
cd pose-meme-matcher
pip install -r requirements.txt
```

This installs:
- `opencv-python` - Webcam access
- `mediapipe` - Pose detection
- `pillow` - Image handling
- `numpy` - Math operations

## Step 2: Generate Placeholder Image

```bash
python create_placeholder.py
```

This creates `assets/placeholder.png` shown when no meme is available.

## Step 3: Add Some Memes

Add at least one meme to get started:

1. Download or find a meme image
2. Save it to the appropriate folder:
   - `memes/thumbs_up/` for thumbs up memes
   - `memes/facepalm/` for facepalm memes
   - `memes/default/` for default/neutral memes
   - etc.

**Tip**: Start with 2-3 memes in `memes/default/` and `memes/thumbs_up/`

## Step 4: Run the App

```bash
python main.py
```

**Current status**: The app skeleton is ready but core functionality needs implementation!

## Next Steps

Since this is still in development, the next phase is to implement:
1. Phase 1: Basic UI with webcam feed
2. Phase 2: Pose detection integration
3. Phase 3: Gesture recognition
4. Phase 4: Meme matching and display

## Testing Individual Components

Once implemented, you can test parts independently:

```bash
# Test meme manager
python -m src.meme.manager

# Test pose detector (needs webcam)
python -m src.pose.detector

# Test UI window
python -m src.ui.app_window
```

## Troubleshooting

### ImportError: No module named 'cv2'
→ Run `pip install -r requirements.txt`

### Webcam not found
→ Make sure no other app is using your webcam
→ Try changing `camera_index` in `config/gestures.json`

### ModuleNotFoundError: No module named 'src'
→ Run from the project root directory: `cd pose-meme-matcher`

---

**Ready to build Phase 1?** Let's implement the foundation! 🚀
