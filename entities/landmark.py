from pyray import draw_circle
import statistics
from pyray import WHITE, GREEN

from entity import Entity
from gesture_recognizer import GestureRecognizer
from webcam import WebCam

class Landmarks(Entity):
    def __init__(self, model: GestureRecognizer, webcam: WebCam) -> None:
        self.model = model
        self.webcam = webcam
        self.hand_x = 0
        self.hand_y = 0
        self.values_x: list[float] = []
        self.values_y: list[float] = []
    
    def update(self) -> None:
        img = self.webcam.read()
        self.hand = self.model.process(img)
        if not len(self.hand.hand_landmarks) > 0:
            return
        
        self.values_x = []
        self.values_y = []
        for landmark in self.hand.hand_landmarks[0].landmark:
            self.values_x.append(landmark.x)
            self.values_y.append(landmark.y)
        self.hand_x = int(statistics.median(self.values_x) * 1280)
        self.hand_y = int(statistics.median(self.values_y) * 1280)

    def get_hand(self) -> tuple[int, int]:
        return (self.hand_x, self.hand_y)

    def draw(self) -> None:
        if not len(self.hand.hand_landmarks) > 0:
            return
        for landmark in self.hand.hand_landmarks[0].landmark:
            draw_circle(int(landmark.x * 1280), int(landmark.y * 1280), 5, WHITE)
        
        draw_circle(self.hand_x, self.hand_y, 5, GREEN)