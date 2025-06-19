import socket
import threading

from chessgame import ChessGame
import utils

  
logger = utils.get_logger(__name__)


class ChessServer:
    def __init__(self) -> None:
        self.server_ip = 'localhost'
        self.server_port = 12345
        self.board = None  # Placeholder for the chess board
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.server_ip, self.server_port))
        self.server_socket.settimeout(1)
        self.players = {}
        self.game = ChessGame()

    def player_handler(self) -> None:
        try:
            client_socket, addr = self.server_socket.accept()
            logger.info(f"Connection from {addr} has been established.")
            if "player1" not in self.players:
                self.players["player1"] = client_socket
                logger.info("Player 1 connected.")
                self.send_data(client_socket, "You are Player 1. Waiting for Player 2...")
            elif "player2" not in self.players:
                self.players["player2"] = client_socket
                logger.info("Player 2 connected.")
                self.send_data(client_socket, "You are Player 2. Game starting...")
                self.send_data(self.players["player1"], "Player 2 has joined. Game starting...")
        except Exception as e:
            logger.info(f"An error occurred: {e}")

    def run_server(self) -> None:
        self.stop_event = threading.Event()
        self.server_socket.listen(1)
        logger.info("Waiting for a connection...")
        try:
            while len(self.players) < 2:
                try:
                    self.player_handler()
                except socket.timeout:
                    if self.stop_event.is_set():
                        break

            player1thread = threading.Thread(target=self.handle_move, args=("player1",))
            player2thread = threading.Thread(target=self.handle_move, args=("player2",))
            player1thread.start()
            player2thread.start()
            player1thread.join(timeout=1)
            player2thread.join(timeout=1)
        except KeyboardInterrupt:
            logger.info(f"KeyboardInterrupt: Stopping the server...")
        finally:
            self.stop_event.set()

    def recv_data(self, client_socket) -> str:
        try:
            data = client_socket.recv(1024)
            if not data:
                return None
            data = data.decode()
            logger.info(f"Received move: {data}")
            return data
        except socket.timeout:
            return None
        except Exception as e:
            return None
    
    def send_data(self, client_socket, data: str) -> None:
        client_socket.sendall(data.encode())
        logger.info(f"Sent move: {data}")

    def handle_move(self, player_id: str) -> None:
        client_socket = self.players[player_id]

        while not self.stop_event.is_set():
            try:
                move = self.recv_data(client_socket)
                if move is None:
                    if self.stop_event.is_set():
                        break
                    continue

                logger.info(f"{player_id} made a move: {move}")
            except Exception as e:
                logger.info(f"An error occurred with {player_id}: {e}")
                break

        client_socket.close()
        del self.players[player_id]
        logger.info(f"{player_id} thread terminated.")


if __name__ == "__main__":
    server = ChessServer()
    try:
        server.run_server()
    except KeyboardInterrupt:
        server.stop_event.set()
        server.server_socket.close()
