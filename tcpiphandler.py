import socket
import time
from PySide6.QtCore import QThread, Signal

class TcpIpHandler(QThread):
    data_received = Signal(bytes)
    error_occurred = Signal(str)
    
    def __init__(self, host, port, keep_alive_interval=30, dummy_message=b'ping'):
        super().__init__()
        self.host = host
        self.port = int(port)
        self.running = False
        self.socket = None
        self.keep_alive_interval = keep_alive_interval  # Interval between keep-alive messages
        self.dummy_message = dummy_message  # Dummy message to send as keep-alive

    def run(self):
        try:
            print(f"Trying to connect to {self.host}:{self.port}")
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.settimeout(5.0)
            self.socket.connect((self.host, self.port))
            print("Connection established")
            self.running = True

            last_keep_alive = time.time()  # Track the last time we sent a dummy message

            while self.running:
                try:
                    # Check if it's time to send the keep-alive message
                    if time.time() - last_keep_alive >= self.keep_alive_interval:
                        self.send_keep_alive()
                        last_keep_alive = time.time()

                    # Try receiving data from the server
                    data = self.socket.recv(1024)
                    if data:
                        self.data_received.emit(data)

                except socket.timeout:
                    continue  # Timeout occurred, continue waiting for data
                except socket.error as e:
                    self.error_occurred.emit(f"Socket error: {e}")
                    break  # Exit the loop on other socket errors

        except (socket.error, ValueError) as e:
            self.error_occurred.emit(f"Connection failed: {e}")
        finally:
            if self.socket:
                self.socket.close()

    def send_keep_alive(self):
        """Send a dummy message to keep the connection alive."""
        if self.socket and self.running:
            try:
                print("Sending keep-alive message")
                self.socket.send(self.dummy_message)
            except socket.error as e:
                self.error_occurred.emit(f"Error sending keep-alive: {e}")
                self.running = False  # Stop the connection if the keep-alive fails

    def stop(self):
        self.running = False
        if self.socket:
            try:
                self.socket.shutdown(socket.SHUT_RDWR)
                self.socket.close()
            except socket.error as e:
                self.error_occurred.emit(f"Error while closing socket: {e}")
