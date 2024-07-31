from typing import Literal
from pyray import WHITE, draw_text, get_screen_width

from client import Client
from constants import MADE_SCORE, WIN, Y_POSITION
from entity import Entity
from scene import Scene

class Game(Entity):
    def __init__(self, client: Client, name: str) -> None:
        self.scene: Scene | None = None
        self.client = client
        self.player_name = name
        self.enemy_name = "loading..."
        self.p1_score = 0
        self.p2_score = 0

    def update(self) -> None:
        self.proccess_messages(self.client.messages)
    
    def proccess_messages(self, messages: list[tuple[Literal['!none'], Literal['']] | tuple[str, Literal['']] | tuple[str, str] | None]):
        msgs = messages.copy()

        for msg in msgs:
            command, value = msg
            if command == Y_POSITION:
                name, _, _ = value.split(',')
                if name != self.player_name:
                    self.enemy_name = name
            elif command == MADE_SCORE:
                my_id = self.client.id
                if my_id == 1:
                    if value == self.player_name:
                        self.p1_score += 1
                    else:
                        self.p2_score += 1
                else:
                    if value == self.player_name:
                        self.p2_score += 1
                    else:
                        self.p1_score += 1

                messages.remove(msg)
            elif command == WIN:
                self.client.close()
                if value == self.player_name:
                    self.scene.manager.change_scene("win")
                else:
                    self.scene.manager.change_scene("lose")
                messages.remove(msg)
    def draw(self) -> None:
        p1_pos = int((get_screen_width() / 4) + len(self.player_name) * 10)
        p2_pos = int((get_screen_width() / 4) * 3 - len(self.enemy_name) * 10)
        if self.client.id == 1:
            draw_text(f"{self.player_name}: {self.p1_score}", p1_pos, 70, 30, WHITE)
            draw_text(f"{self.enemy_name}: {self.p2_score}", p2_pos, 70, 30, WHITE)
        else:
            draw_text(f"{self.enemy_name}: {self.p1_score}", p1_pos, 70, 30, WHITE)
            draw_text(f"{self.player_name}: {self.p2_score}", p2_pos, 70, 30, WHITE)