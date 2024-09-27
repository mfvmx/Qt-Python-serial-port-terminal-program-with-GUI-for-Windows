# ComPort class used in Qt terminal programs

from PySide6.QtCore import QIODevice, Qt, Slot
from PySide6.QtSerialPort import QSerialPort, QSerialPortInfo
from PySide6.QtWidgets import QPushButton, QComboBox, QGridLayout, QLineEdit, QLabel, QGroupBox
from tcpiphandler import TcpIpHandler

class ComPort(QGroupBox):  # QWidget
    def __init__(self, name='', baud_rate='115200', main_window=None):
        super().__init__()
        self.setTitle('Serial port ')
        # add layout
        layout = QGridLayout(self)
        ser_info = QSerialPortInfo()
        self.main_window = main_window

        self.b_portlist = [port.portName() for port in ser_info.availablePorts()]  # list of available COM ports
        # baud rates
        self.b_rates = ['9600', '14400', '19200', '28800', '33600', '38400', '57600', '115200', '230400', '460800',
                        '921600']
        self.nmax = 300  # max number of COM port
        self.port_timeout = 0.5  # COM port timeout
        # create buttons, etc
        self.info_label = QLabel('COM closed')
        self.info_label.setStyleSheet('color: red;')
        self.info_label.setMinimumWidth(100)
        self.info_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.info_label, 0, 0)
        #
        self.port_number_label = QLabel('Port number: ')
        self.port_number_label.setStyleSheet('color: #555555;')
        # self.port_number_label.setMinimumWidth(90)
        self.port_number_label.setAlignment(Qt.AlignRight)
        layout.addWidget(self.port_number_label, 0, 1)
        #
        self.port_field = QComboBox()
        self.port_field.addItems(self.b_portlist)
        if self.b_portlist.count(name):
            self.port_field.setCurrentIndex(self.b_portlist.index(name))  # set default item
        layout.addWidget(self.port_field, 0, 2)
        #
        self.open_btn = QPushButton('Open')
        # self.open_btn.setStyleSheet('background-color: #00dd00;')
        layout.addWidget(self.open_btn, 0, 3)
        self.open_btn.clicked.connect(self.open_port)
        #
        self.baud_rate_label = QLabel('Baud rate: ')
        # self.baud_rate_label.setStyleSheet('color: #555555;')
        self.baud_rate_label.setAlignment(Qt.AlignRight)
        layout.addWidget(self.baud_rate_label, 1, 1)
        #
        self.baud_rates = QComboBox()
        self.baud_rates.addItems(self.b_rates)
        if self.b_rates.count(baud_rate):
            self.baud_rates.setCurrentIndex(self.b_rates.index(baud_rate))  # set default item
        layout.addWidget(self.baud_rates, 1, 2)
        #
        self.close_btn = QPushButton('Close')
        # self.close_btn.setStyleSheet('background-color: red;')
        layout.addWidget(self.close_btn, 1, 3)
        self.close_btn.clicked.connect(self.close_port)
        # Create a button to connect to the TCP/IP server
        # Create input fields for IP address and port
        self.ip_address_input = QLineEdit()
        # self.ip_address_input.setPlaceholderText("Enter IP Address")
        self.ip_address_input.setText("10.10.0.254")
        self.port_input = QLineEdit()
        self.port_input.setText("54322")
        self.connect_button = QPushButton("Connect TCP/IP")
        self.disconnect_button = QPushButton("Disconnect TCP/IP")
        layout.addWidget(self.ip_address_input, 2, 0)
        layout.addWidget(self.port_input, 2, 2)
        layout.addWidget(self.connect_button, 2, 3)
        layout.addWidget(self.disconnect_button, 3, 3)
        self.connect_button.clicked.connect(self.connect_to_tcp_ip)
        self.disconnect_button.clicked.connect(self.stop_tcpip_connection)
        # serial port
        self.com_opened = 0
        self.tcpip_opened = 0
        # self.baud_rate = int(baud_rate)
        self.ser = QSerialPort()
        self.ser.errorOccurred.connect(self.ser_error)

    # Define the connect_to_tcp_ip method
    def connect_to_tcp_ip(self):
        if self.tcpip_opened == 0:
            ip_address = self.ip_address_input.text()
            port = self.port_input.text()
            # Add your connection logic here
            self.start_tcpip_connection(ip_address, port)
            self.tcpip_opened = 1
            print(f"Connecting to {ip_address}:{port}")

    def start_tcpip_connection(self, host, port):
        try:
            self.connection_type = 'tcpip'
            self.tcpip_handler = TcpIpHandler(host, port)
            self.tcpip_handler.data_received.connect(self.main_window.on_tcpip_rx)
            self.tcpip_handler.start()
            self.info_label.setText(f'Connected to {host}:{port}')
            self.info_label.setStyleSheet('color: #00dd00;')  # green
        except Exception as e:
            self.info_label.setText(f'Connection failed: {str(e)}')
            self.info_label.setStyleSheet('color: red;')

    def stop_tcpip_connection(self):
        if self.tcpip_opened:
            if self.tcpip_handler:
                self.tcpip_handler.data_received.disconnect(self.main_window.on_tcpip_rx)  # Disconnect the signal
                self.tcpip_opened = 0
                self.tcpip_handler.stop()
                self.tcpip_handler.wait()
                self.tcpip_handler = None
                self.main_window.statusBar().showMessage("TCP/IP connection closed.")

    def open_port(self):
        n = 0
        if self.com_opened == 0:
            com_num = self.port_field.currentText()
            br = self.baud_rates.currentText()
            self.ser.setBaudRate(int(br))
            if com_num:
                self.ser.setPortName(com_num)
                self.ser.open(QIODevice.ReadWrite)
                if self.ser.isOpen():
                    self.info_label.setText(com_num + ' opened')
                    self.info_label.setStyleSheet('color: #00dd00;')  # green
                    self.com_opened = 1
                else:
                    self.info_label.setText('Can not open')
                    self.info_label.setStyleSheet('color: red;')
                    self.com_opened = 0
            else:
                while (n < self.nmax) and (self.com_opened == 0):
                    n = n + 1
                    self.ser.setPortName(str(n))
                    res = self.ser.open(QIODevice.ReadWrite)
                    if res:  # port was successfully opened
                        self.info_label.setText(str(n) + ' opened')
                        self.info_label.setStyleSheet('color: #00dd00;')  # green
                        self.com_opened = 1
                if self.com_opened == 0:
                    self.info_label.setText('Can not open')
                    self.info_label.setStyleSheet('color: red;')

    def close_port(self):
        if self.com_opened:
            self.ser.close()
            self.info_label.setText('COM closed')
            self.info_label.setStyleSheet('color: red;')
            self.com_opened = 0

    @Slot()
    def ser_error(self):
        err = self.ser.error()
        if err == QSerialPort.SerialPortError.NoError:  # if error message is "No error"
            pass
        else:
            self.close_port()  # close port if some error occurred...

    def write(self, data):
        if self.com_opened:
            self.ser.write(data)
        elif self.tcpip_opened:
            self.tcpip_handler.socket.send(data)