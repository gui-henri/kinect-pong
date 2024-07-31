from typing import Literal
from pyray import draw_circle
from pyray import get_screen_width, get_screen_height
from pyray import Color, Vector2, Rectangle
from pyray import WHITE

from client import Client
from constants import BALL
from entity import Entity

class Ball(Entity):
    def __init__(self, client: Client, x: int, y: int, radius: float, collisors: list[Rectangle], color: Color = WHITE, speed: int = 1) -> None:
        self.client = client
        self.x = x
        self.y = y
        self.radius = radius
        self.speed = Vector2(speed, speed)
        self.color = color
        self.collisors = collisors
    
    def update(self) -> None:
        self.proccess_messages(self.client.messages)

    def draw(self) -> None:
        draw_circle(int(float(self.x)), int(float(self.y)), self.radius, self.color)
    
    def proccess_messages(self, messages: list[tuple[Literal['!none'], Literal['']] | tuple[str, Literal['']] | tuple[str, str] | None]):
        msgs = messages.copy()

        for msg in msgs:
            command, value = msg
            if command == BALL:
                x, y, _, _ = value.split(',')
                self.x = x
                self.y = y
                messages.remove(msg)