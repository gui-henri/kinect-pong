from entity import Entity

class Scene:
    def __init__(self, name: str) -> None:
        self.entities: list[Entity] = []
        self.name = name
        self.manager: SceneManager | None = None

    def change_scene(self, scene_name: str) -> None:
        self.manager.change_scene(scene_name)

class SceneManager:
    def __init__(self) -> None:
        self.scenes: dict[str, Scene] = {}
        self.current_scene: str | None = None

    def get_current_scene(self) -> Scene:
        return self.scenes[self.current_scene]

    def change_scene(self, scene_name: str) -> None:
        self.current_scene = scene_name
    
    def add_scene(self, scene: Scene) -> None:
        if self.scenes.get(scene.name) is not None:
            return
        scene.manager = self
        if self.current_scene is None:
            self.current_scene = scene.name
        self.scenes[scene.name] = scene
        