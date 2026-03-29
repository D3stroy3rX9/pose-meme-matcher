# 🎭 Pose-to-Meme Matcher

A real-time desktop application that detects your gestures via webcam and displays matching memes!

## 🚀 Features

- Real-time pose detection using MediaPipe
- Gesture-based meme matching
- Easy meme management (just drag & drop!)
- Smooth, responsive UI
- 100% free and open-source

## 📋 Requirements

- Python 3.9 or higher
- Webcam
- Windows/Mac/Linux

## 🛠️ Installation

1. **Clone or download this project**

2. **Install dependencies:**
```bash
pip install -r requirements.txt
```

3. **Run the app:**
```bash
python main.py
```

## 📁 Project Structure

```
pose-meme-matcher/
├── main.py                 # Main application entry point
├── src/
│   ├── ui/
│   │   └── app_window.py   # GUI window and layout
│   ├── pose/
│   │   ├── detector.py     # MediaPipe pose detection
│   │   └── gestures.py     # Gesture pattern recognition
│   └── meme/
│       └── manager.py      # Meme indexing and selection
├── memes/                  # Your meme collection
│   ├── arms_crossed/
│   ├── thumbs_up/
│   ├── peace_sign/
│   ├── thinking/
│   ├── facepalm/
│   ├── shrug/
│   └── default/            # Shown when no gesture detected
├── config/
│   └── gestures.json       # Gesture detection patterns
├── assets/
│   └── placeholder.png     # Default image
└── docs/
    ├── GESTURES.md         # List of supported gestures
    └── ADDING_MEMES.md     # How to add new memes
```

## 🎨 Adding Memes

**Super simple!**

1. Find or create a meme image (PNG, JPG, GIF)
2. Drop it into the appropriate folder in `memes/`
   - Example: Put a facepalm meme in `memes/facepalm/`
3. The app will automatically detect it on next run!

**File naming**: Doesn't matter! Name it whatever you want.

See [ADDING_MEMES.md](docs/ADDING_MEMES.md) for more details.

## 🤚 Supported Gestures (MVP)

- **Arms Crossed**: Cross your arms over your chest
- **Thumbs Up**: Classic thumbs up gesture
- **Peace Sign**: Two fingers up (V sign)
- **Thinking**: Hand on chin
- **Facepalm**: Hand covering face
- **Shrug**: Shoulders up, hands out

See [GESTURES.md](docs/GESTURES.md) for detailed pose descriptions.

## ⚙️ Configuration

Edit `config/gestures.json` to:
- Adjust gesture detection sensitivity
- Add new gesture patterns
- Modify cooldown timers

## 🐛 Troubleshooting

**Webcam not detected?**
- Check if another app is using the webcam
- Try changing the camera index in settings

**Gestures not detecting?**
- Ensure good lighting
- Stand 3-6 feet from camera
- Make gestures clear and deliberate

**Memes not showing?**
- Check file format (PNG, JPG, JPEG supported)
- Ensure images are in correct gesture folder

## 📝 License

MIT License - Free to use, modify, and share!

## 🙏 Credits

- **MediaPipe** by Google - Pose detection
- **You!** - For the memes and vibes

---

**Have fun! 🎉**
