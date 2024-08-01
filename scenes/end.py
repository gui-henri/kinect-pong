from client import Client
from entities.reconnect import Reconnect
from scene import Scene

class WinScene(Scene):
    def __init__(self, name: str, client: Client) -> None:
        super().__init__("win")
        conn = Reconnect(client, f"Congratulations {name}, YOU WON!!!!!!")
        
        self.entities.append(conn)

class LoseScene(Scene):
    def __init__(self, name: str, client: Client) -> None:
        super().__init__("lose")
        conn = Reconnect(client, f"Sorry {name}, you lose...")
        self.entities.append(conn)