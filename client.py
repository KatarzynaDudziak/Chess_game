import socket


class ChessClient:
    def __init__(self) -> None:
        self.server_ip = 'localhost'
        self.server_port = 12345
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect(self):
        self.client_socket.connect((self.server_ip, self.server_port))
        print(f"Connected to server at {self.server_ip}:{self.server_port}")

    def send_move(self, move):
        self.client_socket.sendall(move.encode())
        print(f"Sent move: {move}")

    def receive_message(self):
        response = self.client_socket.recv(1024)
        response = response.decode()
        print(f"Received message: {response}")
        return response
        
    def run_client(self):
        self.connect()
        while True:
            response = self.receive_message()
            if not response:
                break
            self.send_move(response)
        self.client_socket.close()


if __name__ == "__main__":
    client = ChessClient()
    try:
        client.run_client()
    except KeyboardInterrupt:
        print("Client stopped.")
    finally:
        client.client_socket.close()
