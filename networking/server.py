import socket
import threading
from typing import Dict, Any
from dataclasses import dataclass

class Server:
    @dataclass
    class ClientData:
        ip: str
        port: int
        
    
    HOST = "127.0.0.1"
    PORT = 6969
    PACKET_SIZE = 1024

    def __init__(self):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.server_socket.settimeout(1.0)
        self.stop_event = threading.Event()
        self.listen_thread: threading.Thread = None
        
        self.clients: Dict[Any, Server.ClientData] = {}

    def start(self):
        self.server_socket.bind((self.HOST, self.PORT))
        self.listen_thread = threading.Thread(target=self._listen_to_clients, daemon=True)
        self.listen_thread.start()

    def stop(self):
        self.stop_event.set()
        self.listen_thread.join()
        self.server_socket.close()

    def _listen_to_clients(self):
        while not self.stop_event.is_set():
            try:
                packet, addr = self.server_socket.recvfrom(self.PACKET_SIZE)
                if not packet:
                    continue

                message = packet.decode(errors="replace")
                print(f"Client {addr}: {message}")
            except socket.timeout:
                continue
            except OSError:
                break
            
    def _handle_client_packet(self, packet: bytes, addr):
        pass
