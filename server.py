import socket
import threading

from constants import *

class ServerState():
    WAITING_PLAYERS = 0
    WAITING_READY = 1
    GAME_RUNNING = 2
    GAME_END = 3

class Player():
    def __init__(self, name: str, conn: socket, addr, id: int, is_connected=True):
        self.name = name
        self.conn = conn
        self.addr = addr
        self.score = 0
        self.y = 0
        self.id = id
        self.ready = False
        self.width = PLAYER_WIDTH
        self.height = PLAYER_HEIGHT
        self.is_connected = is_connected

class Ball():
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y
        self.dx = 1
        self.dy = 1
        self.players: list[Player] = []
        self.last_collision: Player | None = None
        self.last_score: Player | None = None

    def update(self):
        change_x = False
        for player in self.players:
            player_start_y = player.y
            player_end_y = player.y + PLAYER_HEIGHT
            player_x = FIRST_PLAYER_X + player.width if player.id == 1 else SECOND_PLAYER_X
            ball_x = self.x - BALL_RADIUS if player.id == 1 else self.x + BALL_RADIUS

            if ball_x <= player_x and self.y >= player_start_y and self.y <= player_end_y:
                print(f"[DEBUG] Collision with {player.name}")
                change_x = True
                self.last_collision = player

        if self.x >= 1280 - BALL_RADIUS:
            self.reset_position()
            change_x = True
            p = self.player_by_id(1)
            self.last_score = p
        elif self.x <= BALL_RADIUS:
            self.reset_position()
            change_x = True
            p = self.player_by_id(2)
            self.last_score = p

        if change_x:
            self.dx *= -1
        if self.y >= 720 - BALL_RADIUS or self.y <= BALL_RADIUS:
            self.dy *= -1
        self.x += self.dx * BALL_SPEED
        self.y += self.dy * BALL_SPEED

    def reset_position(self):
        self.x = SCREEN_WIDTH / 2
        self.y = SCREEN_HEIGHT / 2
    
    def last_scoring_player(self) -> Player:
        last_score: Player = self.last_score
        self.last_score = None
        return last_score
    
    def last_colliding_player(self) -> Player:
        last_collision: Player = self.last_collision
        self.last_collision = None
        return last_collision

    def player_by_id(self, id: int) -> Player:
        for player in self.players:
            if player.id == id:
                return player

class Server():
    def __init__(self):
        self.HEADER = 1024
        self.PORT = 4321
        self.HOST = socket.gethostbyname(socket.gethostname())
        self.ADDR = (self.HOST, self.PORT)
        self.FORMAT = "utf-8"

        self.state = ServerState.WAITING_PLAYERS
        self.players: list[Player] = []
        self.ball = Ball(640, 480)

        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind(self.ADDR)
    
    def run(self):
        self.server.listen()
        print(f"[LISTENING] Server is listening on {self.HOST}")
        while True:
            if self.state == ServerState.WAITING_PLAYERS:
                if all([not p.is_connected for p in self.players]):
                    self.players = []
                    print("[DEBUG] Game has no players currently.")
                if len(self.players) == 1:
                    self.players[0].id = 1
                conn, addr = self.server.accept()
                command, value = self.recieve_message(conn)

                if command == PLAYER_NAME and value != "":
                    assert len(self.players) < 2, "Max players reached."
                    player = Player(value, conn, addr, id=len(self.players) + 1)
                    self.add_player(player)

                    print(f"[NEW PLAYER] {player.name} connected.")
                    thread = threading.Thread(target=self.handle_client, args=(player,))
                    thread.start()
                    if threading.active_count() - 1 == 2:
                        self.state = ServerState.WAITING_READY
                        print("[DEBUG] Game is waiting players to be ready.")
                    print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}")

                elif command == DISCONNECT_MESSAGE:
                    conn.close()
                    print(f"[DISCONNECT] {addr} disconnected.")
                    continue
                else:
                    continue
                
            elif self.state == ServerState.WAITING_READY:
                if len(self.players) < 2:
                    self.state = ServerState.WAITING_PLAYERS
                    print("[DEBUG] Game is waiting for more players.")
                    continue
                if all([p.ready for p in self.players]):
                    self.state = ServerState.GAME_RUNNING
                    self.broadcast(f"{START_MESSAGE}")
                    print("[DEBUG] Game is running.")

            elif self.state == ServerState.GAME_RUNNING:
                if len(self.players) < 2:
                    for player in self.players:
                        self.send_message(f"{WIN}:{player.name}", player)
                    self.state = ServerState.GAME_END
                    print("[DEBUG] Game ended by withdrawal.")
                    continue
                self.ball.update()
                last_score = self.ball.last_scoring_player()
                if last_score:
                    last_score.score += 1
                    if last_score.score == MAX_SCORE:
                        self.broadcast(f"{WIN}:{last_score.name}")
                        self.state = ServerState.GAME_END
                        print("[DEBUG] Game ended by score. Winner: ", last_score.name)
                        continue
                    self.broadcast(f"{MADE_SCORE}:{last_score.name}")
                self.broadcast(f"{BALL}:{self.ball.x},{self.ball.y},{self.ball.dx},{self.ball.dy}")
                for player in self.players:
                    self.broadcast(f"{player.name}:{player.y}")

            elif self.state == ServerState.GAME_END:
                print("[DEBUG] Game ended. Disconnecting players and starting over.")
                for player in self.players:
                    player.is_connected = False
                self.state = ServerState.WAITING_PLAYERS

    def add_player(self, player: Player):
        self.players.append(player)
        self.ball.players.append(player)
    
    def remove_player(self, player: Player):
        try:
            self.players.remove(player)
            self.ball.players.remove(player)
        except ValueError:
            print(f"[ERROR] {player.name} is not in the game. Check for errors when removing players from player list.")

    def handle_client(self, player: Player):
        while player.is_connected:
            command, value = self.recieve_message(player.conn)
            if command == DISCONNECT_MESSAGE or command == FORCE_CLOSED:
                self.remove_player(player)
                print(f"[DISCONNECT] {player.addr} disconnected.")
                break
            elif command == READY_MESSAGE:
                player.ready = True
                print(f"[READY] {player.name} is ready.")
            elif command == Y_POSITION:
                player.y = int(value)
            elif command == NONE_MESSAGE:    
                continue
            else:
                print(f"[ERROR] Unknown command: {command}")
        try:
            player.conn.close()
        except ConnectionAbortedError:
            print(f"[ERROR] error closing connection with {player.name}. It may have disconnected.")

    def recieve_message(self, conn: socket) -> tuple[str, str]:
        try:
            msg = conn.recv(self.HEADER).decode(self.FORMAT)
            msg = msg.split(':')
            if len(msg) == 1:
                return (msg[0], "")
            return (msg[0], msg[1])
        except ConnectionAbortedError:
            print(f"[ERROR] error receiving data from {conn}. It may have disconnected.")
            return (NONE_MESSAGE, "")
        except ConnectionResetError:
            print(f"[ERROR] connection {conn} was forcefully closed by the client.")
            return (FORCE_CLOSED, "")

    def send_message(self, msg: str, player: Player):
        message = msg.encode(self.FORMAT)
        try:
            player.conn.send(message)
        except ConnectionAbortedError:
            print(f"[ERROR] error sending data to {player.name}. It may have disconnected.")
        except ConnectionResetError:
            print(f"[ERROR] connection was forcefully closed by the client.")
    
    def broadcast(self, msg: str):
        for player in self.players:
            self.send_message(msg, player)

if __name__ == "__main__":
    print("[DEBUG] Server is starting...")
    server = Server()
    server.run()