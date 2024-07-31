from pyray import set_trace_log_level
from client import Client
from gesture_recognizer import HandRecognizer
from raylib_app import RayLibApp
from scene import SceneManager
from scenes.game import GameScene
from webcam import WebCam
from scenes.connect import ReadyScene
import os

def main() -> None:
    os.environ["GLOG_minloglevel"] ="3"
    set_trace_log_level(0)
    webcam = WebCam()
    model = HandRecognizer()

    scene_manager = SceneManager()

    print("[KINECT PONG] Welcome to Kinect Pong!")
    name = input("Enter a nickname: ")

    print("[KINECT PONG] Now, enter the server you want to connect to.")
    addr = input("Server IP addres: ")

    print("[KINECT PONG] Finally, enter the server port.")
    port = int(input("Port: "))
    print("[KINECT PONG] Trying to connect!")
    
    client = Client(addr, port, name)
    print("[KINECT PONG] Connection was successful! Starting game!")

    ready_scene = ReadyScene(name, client, model, webcam)
    game_scene = GameScene(client, model, webcam, name)
    
    scene_manager.add_scene(ready_scene)
    scene_manager.add_scene(game_scene)

    app = RayLibApp(1280, 720, "Kinect Pong", 30, scene_manager)

    app.run()
    app.end()
    webcam.release()
    client.connected = False

if __name__ == "__main__":
    main()