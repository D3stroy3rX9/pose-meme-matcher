# 🎭 Pose-Meme Matcher

A real-time desktop app that detects your gestures via webcam and matches them to hilarious memes!

## 🚀 Features

- **Real-time pose detection** using MediaPipe
- **Gesture recognition** for common poses (thumbs up, peace sign, facepalm, etc.)
- **Split-screen UI**: Webcam feed on left, matched meme on right
- **Easy meme management**: Just drop images into folders
- **Fast & responsive**: Sub-second meme matching

## 📋 Requirements

- Python 3.9+
- Webcam

## 🛠️ Installation

```bash
# Clone the repository
git clone <your-repo-url>
cd pose-meme-matcher

# Install dependencies
pip install -r requirements.txt
```

## 🎮 Usage

```bash
python src/main.py
```

## 📁 Adding Memes

1. Navigate to the `memes/` folder
2. Choose the gesture subfolder (e.g., `thumbs_up/`, `facepalm/`)
3. Drop your meme images (PNG, JPG, GIF)
4. The app will automatically detect and use them!

### Supported Gestures

- `arms_crossed` - Arms crossed over chest
- `thumbs_up` - Thumbs up gesture
- `peace_sign` - Peace/victory sign
- `facepalm` - Hand covering face
- `thinking` - Hand on chin
- `shrug` - Shoulder shrug with arms out
- `salute` - Military salute
- `default` - Shown when no gesture detected

## 🏗️ Project Structure

```
pose-meme-matcher/
├── memes/              # Meme image storage
│   ├── arms_crossed/
│   ├── thumbs_up/
│   ├── peace_sign/
│   └── ...
├── src/
│   ├── main.py         # Entry point
│   ├── pose_detector.py    # MediaPipe pose detection
│   ├── gesture_recognizer.py  # Gesture pattern matching
│   ├── meme_manager.py     # Meme indexing & selection
│   └── ui.py           # GUI interface
├── requirements.txt
└── README.md
```

## 🤝 Contributing

This is a hobby project! Feel free to:
- Add new gesture patterns
- Improve detection accuracy
- Submit cool meme collections

## 📝 License

MIT License - Do whatever you want with it!

---

Made with ❤️ and way too much free time
