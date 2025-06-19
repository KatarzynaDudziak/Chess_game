import socket
import utils


logger = utils.get_logger(__name__)


class ChessClient:
    def __init__(self) -> None:
        self.server_ip = 'localhost'
        self.server_port = 12345
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect(self):
        self.client_socket.connect((self.server_ip, self.server_port))
        logger.info(f"Connected to server at {self.server_ip}:{self.server_port}")

    def send_data(self, move):
        self.client_socket.sendall(move.encode())
        logger.info(f"Sent move: {move}")

    def recv_data(self):
        response = self.client_socket.recv(1024)
        response = response.decode()
        logger.info(f"Received message: {response}")
        return response
        
    def run_client(self):
        self.connect()
        while True:
            response = self.recv_data()
            if not response:
                break
            self.send_data(response)
        self.client_socket.close()


if __name__ == "__main__":
    client = ChessClient()
    try:
        client.run_client()
    except KeyboardInterrupt:
        logger.info("Client stopped.")
    finally:
        client.client_socket.close()
