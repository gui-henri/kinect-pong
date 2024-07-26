import random

from pyray import draw_text, draw_circle
from pyray import get_screen_width
from pyray import Vector2
from pyray import WHITE

from constants import *
from client import Client
from entity import Entity
from scene import Scene

class ReadyText(Entity):
    def __init__(self, name: str, client: Client) -> None:
        self.scene: Scene | None = None    
        self.name = name
        self.ready = False
        self.text = "Put your hand focus inside the red sphere to be ready..."
        self.client = client
        self.reference = (0, 0)
        self.reference_update_callback: callable = None

        self.sphere = Vector2(random.randint(100, 1180), random.randint(200, 600))
        self.radius = 50

    def reference_update(self, callback: callable) -> None:
        if self.reference_update_callback is None:
            self.reference_update_callback = callback
        self.reference: tuple[int, int] = callback()

    def update(self) -> None:
        if self.reference_update_callback is not None:
            self.reference = self.reference_update_callback()
        dist_x = abs(self.reference[0] - self.sphere.x)
        dist_y = abs(self.reference[1] - self.sphere.y)
        
        if not self.ready and dist_x < self.radius and dist_y < self.radius:
            self.ready = True
            self.text = "You are ready! Waiting for other player..."
            self.client.send(f"{READY_MESSAGE}")
    
        msgs = self.client.messages
        print('Before start message processing: ', msgs)
        l = len(msgs)
        for i, msg in enumerate(msgs):
            if msg[0] == START_MESSAGE:
                self.text = "Both players are ready! Starting game..."
                self.scene.manager.change_scene("game")
                l = i + 1
        self.client.messages = msgs[l:]
        print("after start message processing: ", self.client.messages)

    def draw(self) -> None:
        draw_text(self.text, int(get_screen_width() / 2), 40, 20, WHITE)
        if not self.ready:
            draw_circle(int(self.sphere.x), int(self.sphere.y), self.radius, WHITE)