from pyray import draw_rectangle_rec
from pyray import get_screen_height
from pyray import Color, Rectangle
from pyray import WHITE

from entity import Entity

class Player(Entity):
    def __init__(self, width: int, height: int, color: Color = WHITE, speed: int = 1, name="unknown") -> None:
        self.rectangle = Rectangle(30, 500, width, height)
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

    def draw(self) -> None:
        draw_rectangle_rec(self.rectangle, self.color)
