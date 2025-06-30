import socket
from threading import Thread, Event
import pickle
from enum import Enum
from queue import Queue

from chess_engine import ChessEngine
from pawns import Pawn
import utils

  
logger = utils.get_logger(__name__)


class MessageType(Enum):
    MOVE = "move"
    BOARD = "board"
    MOVE_MADE = "move_made"
    GAME_OVER = "game_over"
    CHECK = "check"
    CHECKMATE = "checkmate"
    INVALID_MOVE = "invalid_move"
    PLAYER_JOINED = "player_joined"
    PLAYER_LEFT = "player_left"


class ChessServer:
    def __init__(self, server_ip, server_port) -> None:
        self.game = ChessEngine()
        self.server_ip = server_ip
        self.server_port = server_port
        self.board_state = self.game.get_board()
        self.queue = Queue()
        self.players = {}

    def start_server(self) -> None:
        try:
            logger.info("Waiting for a connection...")
            self.event_stop = Event()
            self.player_handler = PlayerHandler(self.server_ip, self.server_port, self.event_stop, self.queue, self.players, self.board_state)
            self.player_handler.start()
            logger.info(f"Server started at {self.server_ip}:{self.server_port}")
            while not self.event_stop.is_set():
                self.player_handler.join(timeout=1)
                if not self.queue.empty():
                    message = self.queue.get()
                    if message['type'] == MessageType.MOVE:
                        self.send_data(message['data'][0], pickle.dumps(message))
                    elif message['type'] == MessageType.PLAYER_JOINED:
                        self.handle_player(message['data'])
                    elif message['type'] == MessageType.PLAYER_LEFT:
                        self.remove_player()
        except KeyboardInterrupt as e:
            logger.error(f"{e} - Shutting down server.")
            self.event_stop.set()
            self.player_handler.join()

    def send_data(self, player, data) -> None:
        player.sendall(data)

    def handle_player(self, player) -> None:
        conn, addr = player
        self.players[addr] = conn

    def remove_player(self) -> None:
        pass

    def broadcast(self, message) -> None:
        for player in self.players.values():
            print(f"Broadcasting message to player: {player}")
            try:
                self.send_data(player, pickle.dumps(message))
            except Exception as e:
                logger.error(f"Error sending message to player: {e}")


class PlayerHandler(Thread):
    def __init__(self, ip, port, event_stop, queue, players, board_state) -> None:
        super().__init__()
        self.client_socket = None
        self.ip = ip
        self.port = port
        self.event_stop = event_stop
        self.queue = queue
        self.players = players
        self.board_state = board_state
        self.create_socket()

    def create_socket(self) -> None:
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.bind((self.ip, self.port))
        self.client_socket.settimeout(1)
        logger.info(f"Server listening on {self.ip}:{self.port}")

    def accept_connection(self) -> None:
        try:
            conn, addr = self.client_socket.accept()
            conn.settimeout(1)
            logger.info(f"Connection from {addr} has been established.")
            self.send_board_state(conn)
            message = {'type': MessageType.PLAYER_JOINED, 'data': (conn, addr)}
            self.queue.put(message)
            self.message_handler = MessageHandler(conn, self.queue, self.event_stop)
            self.message_handler.start()
        except socket.timeout:
            pass
    
    def send_board_state(self, conn) -> None:
        board_message = {"type": MessageType.BOARD, "data": self.board_state}
        conn.sendall(pickle.dumps(board_message))
        logger.info("Sent board state to player.")

    def run(self) -> None:
        self.client_socket.listen(1)
        while not self.event_stop.is_set() and len(self.players) < 2:
            self.accept_connection()
        self.message_handler.join()


class MessageHandler(Thread):
    def __init__(self, conn, queue, event) -> None:
        super().__init__()
        self.conn = conn
        self.queue = queue
        self.event = event

    def handle_receive_data(self) -> None:
        try:
            while not self.event.is_set():
                data = self.conn.recv(1024)
                if not data:
                    return None
                message = pickle.loads(data)
                self.queue.put(message)
        except socket.timeout:
            return None
        except Exception as e:
            return None

    def run(self) -> None:
        self.handle_receive_data()
        self.conn.close()


def main():
    server_ip = 'localhost'
    server_port = 12345
    chess_server = ChessServer(server_ip, server_port)
    chess_server.start_server()


if __name__ == "__main__":
    main()
