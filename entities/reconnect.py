from pyray import WHITE, draw_text, get_screen_width, is_key_released
from raylib import KEY_SPACE
from client import Client
from entity import Entity
from scene import Scene

class Reconnect(Entity):
    def __init__(self, client: Client, text: str) -> None:
        self.scene: Scene | None = None
        self.client = client
        self.text = text

    def update(self) -> None:
        if is_key_released(KEY_SPACE):
            try:
                self.client.connect()
                self.scene.manager.change_scene('ready')
            except:
                print('[ERROR] Unable to connect to server. Try again.')

    def draw(self) -> None:
        draw_text(self.text, int(get_screen_width() / 2 - len(self.text) * 5), 40, 20, WHITE)