from client import Client
from entities.landmark import Landmarks
from entities.ready import ReadyText
from gesture_recognizer import HandRecognizer
from scene import Scene
from webcam import WebCam

class ReadyScene(Scene):
    def __init__(self, name: str, client: Client, model: HandRecognizer, webcam: WebCam) -> None:
        super().__init__("ready")
        landmarks = Landmarks(model, webcam)
        connect = ReadyText(name, client)
        connect.scene = self
        connect.reference_update(landmarks.get_hand)
        self.entities.append(landmarks)
        self.entities.append(connect)