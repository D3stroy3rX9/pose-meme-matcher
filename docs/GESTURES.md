# 🤚 Supported Gestures

This document describes all the gestures the app can detect and how to perform them for best results.

## MVP Gestures

### 1. Arms Crossed 🙅
**How to do it:**
- Cross your arms over your chest
- Keep arms visible to the camera
- Both forearms should be roughly horizontal

**Detection criteria:**
- Wrists are crossed in front of torso
- Elbows are bent at roughly 90 degrees
- Hands are near opposite shoulders

**Good meme matches:**
- "Not impressed" memes
- "Yeah, right" skeptical faces
- Defensive/closed-off reactions

---

### 2. Thumbs Up 👍
**How to do it:**
- Make a fist with thumb pointing up
- Hold it at shoulder height or higher
- Keep thumb clearly visible

**Detection criteria:**
- Thumb is extended upward
- Other fingers are curled
- Hand is raised above waist level

**Good meme matches:**
- Approval memes
- "Nice" reactions
- Positive affirmations

---

### 3. Peace Sign ✌️
**How to do it:**
- Extend index and middle finger in a V shape
- Keep other fingers curled
- Palm can face camera or away

**Detection criteria:**
- Two fingers extended upward
- Fingers separated in V shape
- Hand raised near face or shoulder height

**Good meme matches:**
- Peace/victory memes
- "We good" reactions
- Casual greetings

---

### 4. Thinking 🤔
**How to do it:**
- Rest your chin on your hand
- Elbow can be on table or free
- Fingers can be curled or extended

**Detection criteria:**
- Hand is near chin/face area
- Elbow is bent
- Head may be slightly tilted

**Good meme matches:**
- Pondering memes
- "Hmm..." reactions
- Philosophical thoughts

---

### 5. Facepalm 🤦
**How to do it:**
- Cover your face with your palm
- Can be one or both hands
- Fingers should spread over forehead/eyes

**Detection criteria:**
- Hand is directly in front of face
- Palm covers significant portion of face
- Wrist is near nose/mouth level

**Good meme matches:**
- Disappointment reactions
- "Oh no" moments
- Frustration expressions

---

### 6. Shrug 🤷
**How to do it:**
- Raise both shoulders up
- Extend arms slightly out to sides
- Palms can face up or forward
- Tilt head slightly

**Detection criteria:**
- Shoulders are elevated
- Arms are extended from body
- Hands are roughly waist to shoulder height

**Good meme matches:**
- "I don't know" memes
- Indifferent reactions
- "Whatever" expressions

---

## Tips for Best Detection

1. **Lighting**: Make sure you're well-lit from the front
2. **Distance**: Stand 3-6 feet from camera
3. **Background**: Plain backgrounds work best
4. **Hold steady**: Keep gesture for 1-2 seconds
5. **Full view**: Ensure your upper body is fully visible
6. **Clear gestures**: Make movements deliberate and distinct

---

## Future Gestures (Post-MVP)

Ideas for expansion:
- Salute
- OK sign
- Heart hands
- Rock on / devil horns
- Finger guns
- Jazz hands
- Namaste
- Crossed fingers
- Mind blown (hands on head)

---

## Adding Custom Gestures

Want to add your own gesture? You'll need to:

1. Create a new folder in `memes/your_gesture_name/`
2. Add gesture detection logic in `src/pose/gestures.py`
3. Update `config/gestures.json` with gesture parameters
4. Add memes to your new folder!

See the code comments in `gestures.py` for implementation details.
