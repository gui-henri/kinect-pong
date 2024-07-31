from typing import Literal
from pyray import draw_rectangle_rec
from pyray import get_screen_height
from pyray import Color, Rectangle
from pyray import WHITE, RED

from client import Client
from constants import *
from entity import Entity

class Player(Entity):
    def __init__(self, client: Client, width: int, height: int, color: Color = WHITE, speed: int = 1, name="unknown") -> None:
        self.client = client
        pos = FIRST_PLAYER_X
        if self.client.id == 2:
            pos = SECOND_PLAYER_X
        self.rectangle = Rectangle(pos, 500, width, height)
        self.speed = speed
        self.color = color
        self.last_y = 0
        self.direction = 1
        self.reference = (0, 0)
        self.reference_update_callback: callable = None
        self.name = name
    
    def reference_update(self, callback: callable) -> None:
        if self.reference_update_callback is None:
            self.reference_update_callback = callback
        self.reference: tuple[int, int] = callback()

    def update(self) -> None:
        msgs = self.client.messages
        self.process_messages(msgs)

        if self.reference_update_callback is not None:
            self.reference = self.reference_update_callback()

        distance = self.reference[1] - self.rectangle.y - self.rectangle.height / 2
        if distance < 0:
            self.direction = -1
        elif distance > 0:
            self.direction = 1
        movement = min(abs(distance) / 3, self.speed)
        self.rectangle.y += movement * self.direction

        if self.rectangle.y >= get_screen_height() - self.rectangle.height:
            self.rectangle.y = get_screen_height() - self.rectangle.height
        if self.rectangle.y <= 0:
            self.rectangle.y = 0
        
        self.client.send(f"{Y_POSITION}:{self.rectangle.y}")

    def draw(self) -> None:
        draw_rectangle_rec(self.rectangle, self.color)

    def process_messages(self, messages: list[tuple[Literal['!none'], Literal['']] | tuple[str, Literal['']] | tuple[str, str] | None]) -> None:
        msgs = messages.copy()
        
        for msg in msgs:
            if msg[0] == NONE_MESSAGE:
                messages.remove(msg)
            else:
                continue 

class Oponent(Player):
    def __init__(self, client: Client, width: int, height: int, color: Color = RED, speed: int = 1, name="unknown") -> None:
        super().__init__(client, width, height, color, speed, name)
        pos = SECOND_PLAYER_X
        if self.client.id == 2:
            pos = FIRST_PLAYER_X
        self.rectangle = Rectangle(pos, 500, width, height)

    def update(self) -> None:
        self.process_messages(self.client.messages)

    def process_messages(self, messages: list[tuple[Literal['!none'], Literal['']] | tuple[str, Literal['']] | tuple[str, str] | None]) -> None:
        msgs = messages.copy()

        for msg in msgs:
            command, value = msg
            if command == Y_POSITION:
                name, id, y = value.split(',')
                if int(id) != self.client.id:
                    self.name = name
                    self.rectangle.y = int(y)
                messages.remove(msg)
            else:
                continue