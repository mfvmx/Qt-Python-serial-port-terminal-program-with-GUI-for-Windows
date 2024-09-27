import socket
from PySide6.QtCore import QThread, Signal

class TcpIpHandler(QThread):
    data_received = Signal(bytes)

    def __init__(self, host, port):
        super().__init__()
        self.host = host
        self.port = int(port)
        self.running = True
        self.socket = None  # Initialize socket attribute

    def run(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((self.host, self.port))
        while self.running:
            data = self.socket.recv(1024)
            if data:
                self.data_received.emit(data)

    def stop(self):
        self.running = False
        if self.socket:
            self.socket.close()