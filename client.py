import socket
import select
import threading
import time

from constants import *

HEADER = 128
FORMAT = "utf-8"

class Client:
    def __init__(self, addr: str, port: int, name: str) -> None:
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.addr = (addr, port)
        self.name = name
        try:
            self.connect()
        except:
            print("[ERROR] Unable to connect to game server. Please check the address or your internet connection.")
            quit()
    
    def connect(self):
        self.client.connect(self.addr)
        self.send(f"{PLAYER_NAME}:{self.name}")
        command, value = self.recieve()
        if command == ID:
            self.id = int(value)
            print(f"Connected to server with ID {self.id}")
        else:
            raise Exception("Invalid command recieved from server. Expected ID, but got {command}. Try login again.")
        self.messages: list[str] = []
        self.connected = True
        self.rcv = threading.Thread(target=self.handle_recieve)
        self.rcv.start()

    def handle_recieve(self):
        while self.connected:
            ready_to_read, _, _ = select.select([self.client], [], [], 3)
            if ready_to_read:
                for socket in ready_to_read:
                    msg = self.recieve(socket=socket)
                    if msg:
                        self.messages.append(msg)
        print("Connection closed")
        self.send(DISCONNECT_MESSAGE)

    def send(self, msg: str):
        message_bytes = msg.encode(FORMAT)
        padd_bytes = ' '.encode(FORMAT)
        message = message_bytes + padd_bytes * (HEADER - len(message_bytes))
        assert len(message) == 128, "message is not 128 bytes long"
        try:
            self.client.send(message)
        except ConnectionAbortedError:
            self.connected = False
            print("Connection aborted in exceptional way")
        except ConnectionResetError:
            self.connected = False
            print("Connection was forcefully closed by the server or the client")

    def recieve(self, socket=None):
        try:
            if socket != None:
                msg = socket.recv(HEADER).decode(FORMAT).rstrip()
                if not msg:
                    return (NONE_MESSAGE, "")
        
                msg = msg.split(':')
                if len(msg) == 1:
                    return (msg[0], "")
                return (msg[0], msg[1])
            else:
                msg = self.client.recv(HEADER).decode(FORMAT).rstrip()
                if not msg:
                    return (NONE_MESSAGE, "")
        
                msg = msg.split(':')
                if len(msg) == 1:
                    return (msg[0], "")
                return (msg[0], msg[1])
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