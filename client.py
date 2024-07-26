import socket
import select
import threading
import time

from constants import *

HEADER = 1024
FORMAT = "utf-8"

class Client:
    def __init__(self, addr: str, port: int, name: str) -> None:
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect((addr, port))
        self.send(f"{PLAYER_NAME}:{name}")
        self.messages: list[str] = []
        self.connected = True
        self.rcv = threading.Thread(target=self.handle_recieve)
        self.rcv.start()
    
    def handle_recieve(self):
        while self.connected:
            ready_to_read, _, _ = select.select([self.client], [], [], 0)
            if ready_to_read:
                msg = self.recieve()
                if msg:
                    self.messages.append(msg)
        print("Connection closed")
        self.send(DISCONNECT_MESSAGE)

    def send(self, msg: str):
        message = msg.encode(FORMAT)
        msg_lenght = len(message)
        send_lenght = str(msg_lenght).encode(FORMAT)
        send_lenght += b" " * (HEADER - len(send_lenght))
        try:
            self.client.send(send_lenght)
            self.client.send(message)
        except ConnectionAbortedError:
            self.connected = False
            print("Connection aborted in exceptional way")
        except ConnectionResetError:
            self.connected = False
            print("Connection was forcefully closed by the server or the client")

    def recieve(self):
        try:
            msg_lenght = self.client.recv(HEADER).decode(FORMAT)
            if msg_lenght:
                msg_lenght = int(msg_lenght)
                msg = self.client.recv(msg_lenght).decode(FORMAT)
                return msg
        except ConnectionAbortedError:
            self.connected = False
            print("Connection aborted in exceptional way")
        except ConnectionResetError:
            self.connected = False
            print("Connection was forcefully closed by the server or the client")

    def close(self):
        self.connected = False
        
if __name__ == "__main__":
    c = Client()
    n = input("Name:")
    c.send(f"{PLAYER_NAME}:{n}")
    c.send(f"{READY_MESSAGE}")
    while True:
        time.sleep(10)
        break
    c.send(DISCONNECT_MESSAGE)