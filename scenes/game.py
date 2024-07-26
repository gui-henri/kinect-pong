from entities.ball import Ball
from entities.landmark import Landmarks
from entities.player import Player
from gesture_recognizer import HandRecognizer
from scene import Scene
from webcam import WebCam

class GameScene(Scene):
    def __init__(self, model: HandRecognizer, webcam: WebCam, name: str) -> None:
        super().__init__("game")
        player = Player(35, 200, speed=10, name=name)
        ball = Ball(200, 200, 20, [player.rectangle], speed=10)
        landmarks = Landmarks(model, webcam)
        player.reference_update(landmarks.get_hand)
        
        self.entities.append(ball)
        self.entities.append(landmarks)
        self.entities.append(player)