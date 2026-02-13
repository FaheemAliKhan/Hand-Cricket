import cv2
import mediapipe as mp
import numpy as np

class HandDetector:
    def __init__(self):
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            max_num_hands=1,
            min_detection_confidence=0.7,
            min_tracking_confidence=0.7
        )
        self.drawer = mp.solutions.drawing_utils

    def get_number(self, frame):
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        rgb = np.ascontiguousarray(rgb)

        results = self.hands.process(rgb)

        if not results.multi_hand_landmarks:
            return None

        hand_landmarks = results.multi_hand_landmarks[0]
        handedness = results.multi_handedness[0].classification[0].label

        # Draw landmarks
        self.drawer.draw_landmarks(
            frame,
            hand_landmarks,
            self.mp_hands.HAND_CONNECTIONS
        )

        lm = hand_landmarks.landmark
        fingers = []

        # ---- THUMB (fixed properly) ----
        if handedness == "Right":
            fingers.append(1 if lm[4].x < lm[3].x else 0)
        else:
            fingers.append(1 if lm[4].x > lm[3].x else 0)

        # ---- OTHER FINGERS ----
        tips = [8, 12, 16, 20]
        pips = [6, 10, 14, 18]

        for tip, pip in zip(tips, pips):
            fingers.append(1 if lm[tip].y < lm[pip].y else 0)

        # -----------------------------
        # STRICT NUMBER RULES
        # -----------------------------

        # Custom 6–10 patterns ONLY
        if fingers == [1,0,0,0,0]: return 6
        if fingers == [1,1,0,0,0]: return 7
        if fingers == [1,1,1,0,0]: return 8
        if fingers == [1,1,1,1,0]: return 9
        if fingers == [1,0,0,0,1]: return 10

        # 1–5 normal counting ONLY
        count = sum(fingers)
        if 1 <= count <= 5:
            return count

        return None
