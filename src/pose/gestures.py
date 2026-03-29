"""
Gesture recognition from pose landmarks.
"""

import time
import json
import numpy as np


class GestureRecognizer:
    """Recognizes gestures from MediaPipe pose landmarks."""

    COOLDOWN = 0.8
    DEFAULT = "default"

    def __init__(self, pose_detector, config_path=None):
        self.detector = pose_detector
        self.current_gesture = self.DEFAULT
        self.last_change = 0.0
        self.config = {}
        if config_path:
            self._load_config(config_path)

    def _load_config(self, config_path):
        try:
            with open(config_path) as f:
                self.config = json.load(f)
        except Exception:
            self.config = {}

    def recognize_gesture(self, landmarks):
        """
        Recognize which gesture is being performed.

        Args:
            landmarks: MediaPipe pose results object

        Returns:
            tuple: (gesture_name, confidence)
        """
        if not landmarks or not landmarks.pose_landmarks:
            return self.DEFAULT, 0.0

        now = time.time()
        if now - self.last_change < self.COOLDOWN:
            return self.current_gesture, 1.0

        checks = [
            ("facepalm",     self._detect_facepalm),   # closest to face — check first
            ("salute",       self._detect_salute),      # forehead + lateral — before peace_sign
            ("thinking",     self._detect_thinking),    # chin area
            ("peace_sign",   self._detect_peace_sign),  # hand in front of face
            ("thumbs_up",    self._detect_thumbs_up),
            ("arms_crossed", self._detect_arms_crossed),
            ("shrug",        self._detect_shrug),
        ]

        for name, fn in checks:
            conf = fn(landmarks)
            if conf > 0.0:
                if name != self.current_gesture:
                    self.current_gesture = name
                    self.last_change = now
                return name, conf

        if self.current_gesture != self.DEFAULT:
            self.current_gesture = self.DEFAULT
            self.last_change = now
        return self.DEFAULT, 0.0

    # ── individual detectors ──────────────────────────────────────────────────

    def _detect_thumbs_up(self, results):
        """Thumbs up: one wrist clearly above shoulder AND away from face (not a salute/peace)."""
        lw   = self.detector.get_landmark(results, 15)
        rw   = self.detector.get_landmark(results, 16)
        ls   = self.detector.get_landmark(results, 11)
        rs   = self.detector.get_landmark(results, 12)
        nose = self.detector.get_landmark(results, 0)
        if not all([lw, rw, ls, rs, nose]):
            return 0.0
        for wrist, shoulder in [(lw, ls), (rw, rs)]:
            if wrist[3] < 0.5:
                continue
            above_shoulder = wrist[1] < shoulder[1] - 0.1
            # Must NOT be close to the face (otherwise it's salute/peace)
            dist_to_nose = self.detector.get_distance((wrist[0], wrist[1]), (nose[0], nose[1]))
            away_from_face = dist_to_nose > 0.3
            if above_shoulder and away_from_face:
                return 0.8
        return 0.0

    def _detect_peace_sign(self, results):
        """Peace sign: wrist held in FRONT of face at eye/nose level.
        Distinguished from salute by small lateral offset (hand is centred, not at temple)."""
        lw   = self.detector.get_landmark(results, 15)
        rw   = self.detector.get_landmark(results, 16)
        nose = self.detector.get_landmark(results, 0)
        if not all([lw, rw, nose]):
            return 0.0
        for wrist in [lw, rw]:
            if wrist[3] < 0.5:
                continue
            dist = self.detector.get_distance((wrist[0], wrist[1]), (nose[0], nose[1]))
            # In front of face: moderate distance (not too close = facepalm, not too far)
            dist_ok = 0.12 < dist < 0.35
            # At or near face level (not above forehead like salute)
            level_ok = nose[1] - 0.15 < wrist[1] < nose[1] + 0.1
            # Relatively centred — NOT laterally offset like a salute
            centred  = abs(wrist[0] - nose[0]) < 0.28
            if dist_ok and level_ok and centred:
                return 0.75
        return 0.0

    def _detect_facepalm(self, results):
        lw = self.detector.get_landmark(results, 15)
        rw = self.detector.get_landmark(results, 16)
        nose = self.detector.get_landmark(results, 0)
        if not all([lw, rw, nose]):
            return 0.0
        ld = self.detector.get_distance((lw[0], lw[1]), (nose[0], nose[1]))
        rd = self.detector.get_distance((rw[0], rw[1]), (nose[0], nose[1]))
        if (ld < 0.15 and lw[3] > 0.5) or (rd < 0.15 and rw[3] > 0.5):
            return 0.85
        return 0.0

    def _detect_thinking(self, results):
        """Thinking: one wrist near chin/lower-face area.
        Chin sits ~12-20% of frame below the nose; allow generous x-range for bent arms."""
        lw   = self.detector.get_landmark(results, 15)
        rw   = self.detector.get_landmark(results, 16)
        nose = self.detector.get_landmark(results, 0)
        ls   = self.detector.get_landmark(results, 11)
        rs   = self.detector.get_landmark(results, 12)
        if not all([lw, rw, nose]):
            return 0.0
        chin_y = nose[1] + 0.13          # chin is lower than nose
        for wrist in [lw, rw]:
            if wrist[3] < 0.4:
                continue
            y_ok = abs(wrist[1] - chin_y) < 0.18    # generous vertical band
            x_ok = abs(wrist[0] - nose[0]) < 0.35   # generous lateral range
            # Must be BELOW nose (not a raised-arm gesture)
            below_nose = wrist[1] > nose[1] - 0.05
            if y_ok and x_ok and below_nose:
                return 0.75
        return 0.0

    def _detect_arms_crossed(self, results):
        lw = self.detector.get_landmark(results, 15)
        rw = self.detector.get_landmark(results, 16)
        ls = self.detector.get_landmark(results, 11)
        rs = self.detector.get_landmark(results, 12)
        if not all([lw, rw, ls, rs]):
            return 0.0
        l_to_rs = self.detector.get_distance((lw[0], lw[1]), (rs[0], rs[1]))
        r_to_ls = self.detector.get_distance((rw[0], rw[1]), (ls[0], ls[1]))
        crossed = (l_to_rs < 0.2 and r_to_ls < 0.2) or (lw[0] > rw[0] + 0.1)
        chest = 0.3 < lw[1] < 0.7 and 0.3 < rw[1] < 0.7
        visible = lw[3] > 0.5 and rw[3] > 0.5
        return 0.8 if (crossed and chest and visible) else 0.0

    def _detect_shrug(self, results):
        lw = self.detector.get_landmark(results, 15)
        rw = self.detector.get_landmark(results, 16)
        ls = self.detector.get_landmark(results, 11)
        rs = self.detector.get_landmark(results, 12)
        if not all([lw, rw, ls, rs]):
            return 0.0
        raised = lw[1] <= ls[1] + 0.05 and rw[1] <= rs[1] + 0.05
        wide = abs(lw[0] - rw[0]) > 0.3
        visible = lw[3] > 0.5 and rw[3] > 0.5
        return 0.8 if (raised and wide and visible) else 0.0

    def _detect_salute(self, results):
        """Salute: one wrist at/above forehead level AND laterally offset (at the temple).
        Key distinction from peace_sign: the wrist is to the SIDE of the face, not in front."""
        lw   = self.detector.get_landmark(results, 15)
        rw   = self.detector.get_landmark(results, 16)
        nose = self.detector.get_landmark(results, 0)
        ls   = self.detector.get_landmark(results, 11)
        rs   = self.detector.get_landmark(results, 12)
        if not all([lw, rw, nose, ls, rs]):
            return 0.0
        for wrist, shoulder in [(lw, ls), (rw, rs)]:
            if wrist[3] < 0.5:
                continue
            # Wrist must be above nose level (forehead/temple height)
            if wrist[1] >= nose[1] - 0.02:
                continue
            # Wrist must be raised above the shoulder
            if wrist[1] >= shoulder[1]:
                continue
            # Lateral offset: wrist is at the SIDE of the head (temple), not centered in front
            x_offset = abs(wrist[0] - nose[0])
            if x_offset < 0.06:   # too centered = peace_sign or facepalm
                continue
            return 0.8
        return 0.0

    # ── utilities ─────────────────────────────────────────────────────────────

    @staticmethod
    def _calculate_angle(p1, p2, p3):
        a, b, c = np.array(p1), np.array(p2), np.array(p3)
        ba, bc = a - b, c - b
        cos = np.dot(ba, bc) / (np.linalg.norm(ba) * np.linalg.norm(bc))
        return float(np.degrees(np.arccos(np.clip(cos, -1.0, 1.0))))

    @staticmethod
    def _calculate_distance(p1, p2):
        return float(np.linalg.norm(np.array(p1) - np.array(p2)))


if __name__ == "__main__":
    print("GestureRecognizer ready.")
