# 🚀 Quick Start Guide

Get your Pose Meme Matcher up and running in 5 minutes!

## Prerequisites

- Python 3.9 or higher
- Webcam
- ~500MB free space

## Installation

### Step 1: Clone the Repository
```bash
git clone <your-repo-url>
cd pose-meme-matcher
```

### Step 2: Install Dependencies
```bash
pip install -r requirements.txt
```

This will install:
- OpenCV (for webcam access)
- MediaPipe (for pose detection)
- Pillow (for image handling)
- NumPy (for calculations)

### Step 3: Add Some Memes

Before running, add at least a few memes to get started:

1. Navigate to `memes/default/`
2. Add 2-3 funny images (PNG, JPG, GIF)
3. Optionally add memes to other gesture folders like:
   - `memes/thumbs_up/`
   - `memes/facepalm/`
   - `memes/peace_sign/`

See [MEME_GUIDE.md](MEME_GUIDE.md) for detailed instructions.

### Step 4: Run the App
```bash
python src/main.py
```

That's it! 🎉

## First Run Tips

1. **Grant camera permissions** when prompted
2. **Position yourself** so your upper body is visible in the webcam
3. **Try different gestures**:
   - Thumbs up
   - Peace sign
   - Hand on chin (thinking)
   - Facepalm
   - Arms crossed

4. **Watch the memes change** as you switch poses!

## Troubleshooting

### "Could not open webcam"
- Make sure your webcam is connected
- Close other apps using the camera (Zoom, Teams, etc.)
- Check camera permissions on your system

### "No memes found"
- Add some images to `memes/default/` folder
- Click "Reload Memes" button in the app
- Check file extensions are supported (.png, .jpg, .gif)

### App is laggy
- Close other heavy applications
- Reduce number of memes (stick to 20-40 total)
- Make sure images aren't huge (resize to ~1000px)

### Gestures not detecting
- Make sure you're fully visible in webcam
- Try exaggerating the gesture
- Check lighting (poor lighting affects pose detection)
- See gesture tips in [MEME_GUIDE.md](MEME_GUIDE.md)

## Next Steps

1. **Add more memes** - see MEME_GUIDE.md
2. **Test different gestures** - see what works best for you
3. **Share with friends** - it's more fun with an audience!
4. **Customize** - edit `src/gesture_config.py` to tune detection

## Performance Notes

**Expected Performance:**
- 20-30 FPS webcam feed
- <1 second gesture recognition
- Instant meme switching

**If performance is poor:**
- Update graphics drivers
- Close background apps
- Check CPU isn't thermal throttling

## Need Help?

- Read the [MEME_GUIDE.md](MEME_GUIDE.md) for meme tips
- Check [README.md](README.md) for project overview
- Review gesture patterns in `src/gesture_config.py`

---

Have fun! 🎭🎉
