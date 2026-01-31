import socket
import threading

class Client:
    PACKET_SIZE = 1024

    def __init__(self):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.server_socket.settimeout(1.0)
        self.stop_event = threading.Event()
        self.listen_thread: threading.Thread = None

    def connect(self, host, port):
        self.server_socket.connect((host, port))
        self.listen_thread = threading.Thread(target=self._listen_to_server, daemon=True)
        self.listen_thread.start()

    def disconnect(self):
        self.stop_event.set()
        self.listen_thread.join()
        self.server_socket.close()

    def _listen_to_server(self):
        while not self.stop_event.is_set():
            try:
                packet = self.server_socket.recv(self.PACKET_SIZE)
                if not packet:
                    continue
                
                print(f"Server: {packet.decode()}")
            except socket.timeout:
                continue
            except OSError:
                break
