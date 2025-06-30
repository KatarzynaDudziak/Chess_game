import socket
import utils
from threading import Thread
import pickle

from chess_server import MessageType


logger = utils.get_logger(__name__) 


class ChessClient:
    def __init__(self, update_board) -> None:
        self.server_ip = 'localhost'
        self.server_port = 12345
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.update_board = update_board
        self.board = None
        self.active_player = True

    def connect(self):
        self.client_socket.connect((self.server_ip, self.server_port))
        try:
            self.message_handler_thread = Thread(target=self.run_client)
            self.message_handler_thread.daemon = True
            self.message_handler_thread.start()
            logger.info(f"Connected to server at {self.server_ip}:{self.server_port}")
            self.message_handler_thread.join(timeout=1) #check if it is necessary to join the thread here
        except Exception as e:
            logger.error(f"Error connecting to server: {e}")
            self.active_player = False

    def send_data(self, move):
        self.client_socket.sendall(pickle.dumps(move))
        logger.info(f"Sent move: {move}")

    def recv_data(self):
        response = self.client_socket.recv(1024)
        if not response:
            return None
        response = pickle.loads(response)
        logger.info(f"Received message: {response['data']}")
        return response
    
    def get_board(self):
        return self.board

    def run_client(self):
        while self.active_player:
            try:
                response = self.recv_data()
                if response is None:
                    logger.info("No response from server, closing connection.")
                    self.active_player = False
                    break
                if response["type"] == MessageType.BOARD:
                    self.board = response["data"]
                    self.update_board()
                elif response["type"] == MessageType.MOVE:
                    move = response["data"]
                    self.send_data(move)
            except KeyboardInterrupt as e:
                logger.error(f"{e}")
                self.active_player = False
        self.client_socket.close()
        logger.info("Client connection closed.")
