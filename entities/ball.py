from pyray import draw_circle
from pyray import get_screen_width, get_screen_height
from pyray import Color, Vector2, Rectangle
from pyray import WHITE

from entity import Entity

class Ball(Entity):
    def __init__(self, x: int, y: int, radius: float, collisors: list[Rectangle], color: Color = WHITE, speed: int = 1) -> None:
        self.x = x
        self.y = y
        self.radius = radius
        self.speed = Vector2(speed, speed)
        self.color = color
        self.collisors = collisors
    
    def update(self) -> None:
        self.__keep_inside_screen()
        self.__collide()
        self.x += self.speed.x
        self.y += self.speed.y

    def draw(self) -> None:
        draw_circle(int(self.x), int(self.y), self.radius, self.color)
    
    def __keep_inside_screen(self) -> None:
        if self.x >= get_screen_width() - self.radius or self.x <= self.radius:
            self.x = get_screen_width() / 2
            self.y = get_screen_height() / 2
            self.speed.x *= -1
        if self.y >= get_screen_height() - self.radius or self.y <= self.radius:
            self.speed.y *= -1
    
    def __collide(self) -> None:
        for collisor in self.collisors:
            if self.x >= collisor.x and self.x <= collisor.x + collisor.width:
                if self.y >= collisor.y and self.y <= collisor.y + collisor.height:
                    self.speed.x *= -1
                    break