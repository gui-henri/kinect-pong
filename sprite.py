from pyray import Vector2, Color
from pyray import load_texture, draw_texture_ex
from pyray import WHITE

class Sprite:
    def __init__(self, position: Vector2, img_path: str, rotation: float = 0, scale: float = 1, color: Color = WHITE):
        self.position = position
        self.rotation = rotation
        self.scale = scale
        self.color = color
        self.image = load_texture(img_path)

    def draw(self) -> None:
        draw_texture_ex(self.image, self.position, self.rotation, self.scale, self.color)