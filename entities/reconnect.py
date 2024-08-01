from pyray import WHITE, draw_text, get_screen_width, is_key_released
from raylib import KEY_SPACE
from client import Client
from entity import Entity
from scene import Scene

class Reconnect(Entity):
    def __init__(self, client: Client, text: str) -> None:
        self.client = client
        self.text = text

    def draw(self) -> None:
        draw_text(self.text, int(get_screen_width() / 2 - len(self.text) * 5), 40, 20, WHITE)