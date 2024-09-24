import socket
from PySide6.QtCore import QThread, Signal

class TcpIpHandler(QThread):
    data_received = Signal(bytes)

    def __init__(self, host, port):
        super().__init__()
        self.host = host
        self.port = port
        self.running = True

    def run(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((self.host, self.port))
            while self.running:
                data = s.recv(1024)
                if data:
                    self.data_received.emit(data)

    def stop(self):
        self.running = False