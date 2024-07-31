from pyray import init_window, window_should_close, close_window
from pyray import set_target_fps, disable_cursor
from pyray import begin_drawing, clear_background, end_drawing
from pyray import BLACK

from entity import Entity
from scene import SceneManager

class RayLibApp:
    def __init__(self, width: int, height: int, title: str, fps: int, scene_manager: SceneManager) -> None:
        self.width = width
        self.height = height
        self.title = title
        self.fps = fps
        self.scene_manager = scene_manager
        self.background_color = BLACK
        self.entities: list[Entity] = []

        init_window(self.width, self.height, self.title)
        set_target_fps(self.fps)
        disable_cursor()

    def run(self) -> None:
        while not window_should_close():
            self.entities = self.scene_manager.get_current_scene().get_entities()
            self.update()
            self.draw()

    def update(self) -> None:
        for entitiy in self.entities:
            entitiy.update()

    def draw(self) -> None:
        begin_drawing()
        clear_background(self.background_color)
        for entity in self.entities:
            entity.draw()
        end_drawing()

    def end(self) -> None:
        close_window()
