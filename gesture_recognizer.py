import mediapipe as mp
import mediapipe.python.solutions.hands as hands
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
from mediapipe.tasks.python.components.containers import NormalizedLandmark
from cv2.typing import MatLike

class Gesture:
    def __init__(self, top_gesture: str, hand_landmarks: NormalizedLandmark) -> None:
        self.top_gesture = top_gesture
        self.hand_landmarks = hand_landmarks

class Landmarks:
    def __init__(self, landmark) -> None:
        self.landmark = landmark
        if not landmark:
            self.x = 0
            self.y = 0
            self.z = 0
            return
        self.x = landmark.x
        self.y = landmark.y
        self.z = landmark.z

class GestureRecognizer:
    def __init__(self, model_path: str) -> None:
        base_options = python.BaseOptions(model_asset_path=model_path)
        options = vision.GestureRecognizerOptions(base_options=base_options)
        self.recognizer = vision.GestureRecognizer.create_from_options(options)

    def process(self, image: MatLike) -> Gesture:
        img = mp.Image(image_format=mp.ImageFormat.SRGB, data=image)
        res = self.recognizer.recognize(img)
        gesture = res.gestures[0][0] if len(res.gestures) > 0 else ""
        hand_landmarks = res.hand_landmarks if len(res.hand_landmarks) > 0 else []
        return Gesture(gesture, hand_landmarks)

class HandRecognizer(GestureRecognizer):
    def __init__(self) -> None:
        self.recognizer = hands.Hands(max_num_hands=1)
    
    def process(self, image: MatLike) -> Landmarks:
        res = self.recognizer.process(image)
        if not res.multi_hand_landmarks:
            return Gesture("", [])
        hand_landmarks = res.multi_hand_landmarks
        return Gesture("", hand_landmarks)