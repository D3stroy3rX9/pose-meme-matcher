# 🎨 Adding Memes Guide

This guide shows you how to add, organize, and manage your meme collection.

## Quick Start

**Adding a meme is as simple as:**
1. Find a meme image file (PNG, JPG, JPEG)
2. Drag it into the appropriate gesture folder in `memes/`
3. Done! The app will find it automatically.

## Folder Structure

Your memes live in the `memes/` directory, organized by gesture:

```
memes/
├── arms_crossed/       # Skeptical, defensive memes
├── thumbs_up/          # Approval, positive memes  
├── peace_sign/         # Peace, victory memes
├── thinking/           # Pondering, hmm memes
├── facepalm/          # Disappointment, oh no memes
├── shrug/             # I don't know, whatever memes
└── default/           # Shown when no gesture detected
```

## Supported File Formats

- ✅ PNG (.png)
- ✅ JPEG (.jpg, .jpeg)
- ✅ GIF (.gif) - will show as static image
- ❌ WebP, TIFF, BMP - not currently supported

## File Naming

**You can name files whatever you want!** Examples:
- `epic_facepalm.jpg`
- `surprised_pikachu.png`
- `meme_001.png`
- `2024-12-30-funny.jpg`

The app doesn't care about names, only which folder they're in.

## Image Guidelines

**For best results:**
- **Resolution**: 800x600 or larger looks great
- **Aspect ratio**: Any works, but 4:3 or 16:9 are common
- **File size**: Under 5MB per image (for fast loading)
- **Content**: Make sure the meme is clearly visible

## Adding Your First Memes

### Example: Adding Facepalm Memes

1. **Find or create memes** (search "facepalm meme" online)
2. **Download** them to your computer
3. **Move** them to `memes/facepalm/`
4. **Launch the app** - they'll automatically load!

### How Many Memes Per Gesture?

- **Minimum**: 1 meme per gesture folder
- **Recommended**: 5-10 for variety
- **Maximum**: Unlimited! (but loading might slow down with hundreds)

When you have multiple memes for one gesture, the app randomly picks one each time.

## The Default Folder

The `memes/default/` folder is special:

- Shows when **no gesture** is detected
- Shows during **startup** before detection begins
- Good for "waiting" or "neutral" images

Suggestions for default memes:
- "Waiting patiently" cat
- "Do something" expectant faces
- Neutral expressions
- Your app logo or branding

## Hot-Reloading Memes

Currently, you need to **restart the app** after adding new memes.

> 🔮 **Future feature**: The app will auto-detect new memes without restarting!

## Organizing Tips

### Method 1: Emotion-Based
Match memes to the emotion of the gesture:
- Facepalm → Embarrassment, frustration
- Thumbs up → Approval, agreement
- Thinking → Confusion, pondering

### Method 2: Character-Based
Group by character or franchise:
- `facepalm/picard_facepalm.jpg`
- `facepalm/homer_doh.jpg`
- `thumbs_up/fonzie_ayy.jpg`

### Method 3: Intensity Levels
Use subfolders (future enhancement):
- `facepalm/mild/` - Light disappointment
- `facepalm/extreme/` - Total exasperation

## Troubleshooting

### Meme not showing up?

1. **Check file format** - Is it PNG or JPG?
2. **Check folder** - Is it in the right gesture folder?
3. **Check file permissions** - Can the app read it?
4. **Restart the app** - Did you reload after adding?

### Meme looks blurry or pixelated?

- Use higher resolution source images
- Avoid upscaling small images
- Try different file format (PNG is usually better quality)

### Too many memes loading slowly?

- Reduce total count per folder
- Use smaller file sizes
- Optimize images before adding

## Sample Meme Collections

Need inspiration? Search these terms:
- "Classic memes compilation"
- "[gesture] reaction memes"
- "Relatable memes 2024"
- "Wholesome memes"

Popular meme sources:
- Reddit: r/memes, r/MemeEconomy
- Giphy (download as GIF, will show as static)
- Know Your Meme (image galleries)
- Your own screenshots and creations!

## Creating Custom Memes

Want to make your own?

**Tools:**
- **Free**: GIMP, Paint.NET, Photopea
- **Online**: Imgflip, Kapwing, Canva
- **Mobile**: Meme Generator apps

**Ideas:**
- Inside jokes with friends
- Personal photos with text
- Screenshots from shows/games
- AI-generated art (MidJourney, DALL-E)

## Sharing Your Collection

Want to share your meme pack?

1. Zip up your entire `memes/` folder
2. Share with friends
3. They extract it into their app directory
4. Everyone gets the same memes!

## Advanced: Multiple Meme Sets

Create different meme collections for different moods:

```
memes_wholesome/
memes_dank/
memes_corporate/
```

Swap them by renaming folders (future: built-in switching!)

---

**Happy meme-ing! 🎉**

Got questions? Check the main README or create an issue on GitHub!
