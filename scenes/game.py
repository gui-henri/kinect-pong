from client import Client
from constants import BALL_RADIUS, FIRST_PLAYER_X, PLAYER_HEIGHT, PLAYER_WIDTH, SECOND_PLAYER_X
from entities.ball import Ball
from entities.game import Game
from entities.landmark import Landmarks
from entities.player import Oponent, Player
from entity import Entity
from gesture_recognizer import HandRecognizer
from scene import Scene
from webcam import WebCam

class GameScene(Scene):
    def __init__(self, client: Client, model: HandRecognizer, webcam: WebCam, name: str) -> None:
        super().__init__("game")
        self.client = client
        game = Game(client, name)
        game.scene = self
        player = Player(self.client, PLAYER_WIDTH, PLAYER_HEIGHT, speed=10, name=name)
        enemy = Oponent(self.client, PLAYER_WIDTH, PLAYER_HEIGHT, speed=10)
        ball = Ball(self.client, 200, 200, BALL_RADIUS, [player.rectangle, enemy.rectangle], speed=10)
        landmarks = Landmarks(model, webcam)
        player.reference_update(landmarks.get_hand)
        
        self.entities.append(game)
        self.entities.append(ball)
        self.entities.append(landmarks)
        self.entities.append(player)
        self.entities.append(enemy)

    def get_entities(self) -> list[Entity]:
        return self.entities