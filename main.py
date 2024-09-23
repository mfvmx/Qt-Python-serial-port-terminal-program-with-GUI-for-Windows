# This is a Qt (PySide) terminal program


from PySide6.QtCore import QIODevice
from PySide6.QtSerialPort import QSerialPort, QSerialPortInfo
from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import QApplication, QMainWindow, QTableView, QWidget, QVBoxLayout, QHBoxLayout, QTextEdit
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtWebEngineCore import QWebEngineSettings
from PySide6.QtCore import QFile, QIODevice
from PySide6.QtGui import QKeySequence, QShortcut
import sys
import folium
from folium import JsCode
from folium.plugins import Realtime
import datetime
from comport import ComPort
from controls import *
from messageparser import *
from tablemodel import *
from variables import *

###############################################################

term_title = "QtTerminal"

nmax = 300  # max number of COM port, used in get_free_ports()

com_port_name = "COM19"
default_baud_rate = "115200"

window_min_height = 900
window_min_width = 1200

term_min_width = 400

sms = "SMS test"

cmd_end = b"\r"
sms_end = b"\x1A"

time_stamp = 1  # to add time stamp (1) or not (0)
echo = 0  # show echo (1) or not (0)
new_line = 1  # set add_time = 1 after receiving '\r' or '\n'

# Names of notebook's tables
tab1Name = "Flag Commands"
tab2Name = "Net"
tab3Name = "TCP/IP"

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        # Initialize a buffer to store incoming data
        self.rx_buffer = bytearray()
        # Add an instance variable to store the Developer Tools window
        self.dev_tools = None

        self.setWindowTitle(term_title)
        self.statusBar().showMessage("Welcome!")
        # central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        # create vertical layout
        infovbox = QVBoxLayout(central_widget)
        self.modelPitTimes = CustomTableModelPitTime(device_status_table)
        self.modelDeviceSatus = TableModelStatus(device_status_table)
        self.modelDeviceLocation = TableModelLocation(device_location_table)
        # self.tableboxStatus = QTableView()
        # self.tableboxStatus.setModel(self.modelDeviceSatus)
        # self.tableboxStatus.setSortingEnabled(True)
        # self.tableboxStatus.resizeColumnsToContents()
        # Manually set the row height
        # row_height = 10  # Set your desired row height here
        # for row in range(self.tableboxStatus.model().rowCount()):
        #     self.tableboxStatus.setRowHeight(row, row_height)
        # self.tableboxStatusPitTimes = QTableView()
        # self.tableboxStatusPitTimes.setModel(self.modelPitTimes)
        # self.tableboxStatusPitTimes.setSortingEnabled(True)
        # self.tableboxStatusPitTimes.resizeColumnsToContents()
        # self.tableboxStatusLocation = QTableView()
        # self.tableboxStatusLocation.setModel(self.modelDeviceLocation)
        # self.tableboxStatusLocation.setSortingEnabled(True)
        # self.tableboxStatusLocation.resizeColumnsToContents()

        # create hbox (horizontal layout)
        hbox = QHBoxLayout()
        # verticalTableLayout = infovbox()
        infovbox.addLayout(hbox)
        # create term
        self.term = QTextEdit()
        self.term.setReadOnly(True)
        self.term.setMinimumWidth(term_min_width)
        self.term.setStyleSheet(
            """
                background-color: #000000;
                color: #FFFFFF;
                font-family: Titillium;
                font-size: 12px;
                """
        )
        # hbox.addWidget(self.term)
        # infovbox.addWidget(self.term) # Bottom of the window
        self.map = folium.Map(location=[34.138595, -83.818801], zoom_start=13)
        # Initialize the data array
        self.data_array = [
            {"id": 1, "longitude": -83.818801, "latitude": 34.138595}  # Initial marker data
        ]
        self.mapweb_view = QWebEngineView()
        self.enable_developer_tools()

        # Binding Developer Tools to a keypress, for example, F12
        self.shortcut = QShortcut(QKeySequence("F12"), self)
        self.shortcut.activated.connect(self.open_developer_tools)
        self.testshortcut = QShortcut(QKeySequence("F11"), self)
        self.testshortcut.activated.connect(self.test_js_execution)
        self.testshortcut1 = QShortcut(QKeySequence("F10"), self)
        self.testshortcut1.activated.connect(self.test_js_execution2)

        self.update_map()
        self.expose_map_js()
        # self.test_js_execution()
        # w.setHtml(m.get_root().render())
        infovbox.addWidget(self.mapweb_view)

        self.table_notebook = Notebook()
        # add tables to the notebook
        self.table_notebook.add_tab_tableview("Status", self.modelDeviceSatus, self.send)
        self.table_notebook.add_tab_tableview("Pit Times", self.modelPitTimes, self.send)
        self.table_notebook.add_tab_tableview("Location", self.modelDeviceLocation, self.send)
        hbox.addWidget(self.table_notebook)

        # verticalTableLayout.addWidget(self.tableboxStatus)
        # verticalTableLayout.addWidget(self.tableboxStatusPitTimes)
        # verticalTableLayout.addWidget(self.tableboxStatusLocation)
        # hbox.addLayout(verticalTableLayout)
        hbox.addWidget(self.table_notebook)
        # create vbox (vertical layout)
        vbox = QVBoxLayout()
        # add vbox to main window
        hbox.addLayout(vbox)
        # create Controls and bind handlers
        self.controls = Controls()
        self.controls.clear_btn.clicked.connect(self.clear_term)
        self.controls.copy_btn.clicked.connect(self.copy)
        self.controls.cut_btn.clicked.connect(self.cut)
        self.controls.info_btn.clicked.connect(self.ports_info)
        self.controls.free_btn.clicked.connect(self.get_free_ports)
        self.controls.time_box.toggled.connect(self.time_box_toggled)
        self.controls.time_box.setChecked(True)
        self.controls.echo_box.toggled.connect(self.echo_box_toggled)
        # create Com port
        self.port = ComPort(com_port_name, default_baud_rate)
        self.port.ser.readyRead.connect(self.on_port_rx)
        self.port.ser.errorOccurred.connect(self.port_error)
        # create any_panels and bind handlers
        self.any_panel_1 = SendAny()
        self.any_panel_2 = SendAny()
        self.any_panel_1.any_btn.clicked.connect(self.send_any)
        self.any_panel_2.any_btn.clicked.connect(self.send_any)
        # create notebook
        self.notebook = Notebook()
        # add tables to the notebook
        self.notebook.add_tab_btn(tab1Name, T1, self.send)
        self.notebook.add_tab_btn(tab2Name, T2, self.send)
        self.notebook.add_tab_btn(tab3Name, T3, self.send)
        # add controls to side panel
        vbox.addWidget(self.port)
        vbox.addWidget(self.controls)
        vbox.addWidget(self.any_panel_1)
        vbox.addWidget(self.any_panel_2)
        vbox.addWidget(self.notebook)

    def add_marker_to_map(self, lat, lon, popup_text): # Add a marker to the map
        """Dynamically add a marker without zooming or panning the map."""
        js_code = f"""
            if (typeof window.map !== 'undefined') {{
                var marker = L.marker([{lat}, {lon}]).addTo(window.map);
                marker.bindPopup('{popup_text}');
                console.log('Marker added at: {lat}, {lon}');
            }} else {{
                console.error('window.map is not available.');
            }}
        """
        self.mapweb_view.page().runJavaScript(js_code)

    def add_or_update_marker(self, marker_id, lat, lon, popup_text, color):
        """Dynamically add or update a marker with a custom color."""
        js_code = f"""
            // Initialize the markers object if it doesn't exist
            if (typeof window.markers === 'undefined') {{
                window.markers = {{}};
            }}

            // Extract the last 4 characters of the marker_id
            var short_id = '{marker_id}'.slice(-4);

            // Create a custom divIcon with a dynamic background color
            var customIcon = L.divIcon({{
                html: '<div style="background-color:{color};padding:2px;border-radius:5px;border:2px solid black;">' + short_id + '</div>',
                className: 'custom-marker',  // Optional class for more styling
                iconSize: [30, 20],          // Adjust the size of the marker
                iconAnchor: [15, 10]         // Center the marker on the coordinates
            }});

            // Check if a marker with this ID already exists
            if (window.markers['{marker_id}']) {{
                // Update the existing marker's position and popup
                window.markers['{marker_id}'].setLatLng([{lat}, {lon}]).bindPopup('{popup_text}');
                window.markers['{marker_id}'].setIcon(customIcon);  // Update the icon
                console.log('Updated marker {marker_id} to new position: {lat}, {lon}');
            }} else {{
                // Add a new marker with the custom colored icon
                var marker = L.marker([{lat}, {lon}], {{ icon: customIcon }}).addTo(window.map).bindPopup('{popup_text}');
                window.markers['{marker_id}'] = marker;  // Store the marker by ID
                console.log('Added new marker {marker_id} at: {lat}, {lon}');
            }}
        """
        # Execute the JavaScript to dynamically add or update the marker
        self.mapweb_view.page().runJavaScript(js_code)

    def remove_marker(self, marker_id): # Remove a marker by ID
        js_code = f"""
            if (window.markers && window.markers['{marker_id}']) {{
                window.map.removeLayer(window.markers['{marker_id}']);
                delete window.markers['{marker_id}'];
                console.log('Removed marker {marker_id}');
            }} else {{
                console.log('No marker found with ID {marker_id}');
            }}
        """
        self.mapweb_view.page().runJavaScript(js_code)

    def test_js_execution2(self):
        self.add_marker_to_map(34.1355, -83.8188, "New Dynamic Marker10")
        print("Marker added at:")
    def test_js_execution(self):
        self.add_marker_to_map(34.136, -83.819, "New Dynamic Marker")
        print("Marker added at:")
        # """Test if JavaScript execution works from Python."""
        # js_code = """
        #     console.log('Python-triggered JavaScript is running.');
        # """
        # # Execute the JavaScript
        # self.mapweb_view.page().runJavaScript(js_code)
        
    def enable_developer_tools(self):
        """Enable Developer Tools in QWebEngineView."""
        # These settings can remain if you want to enable other attributes like JavaScript
        self.mapweb_view.settings().setAttribute(QWebEngineSettings.LocalStorageEnabled, True)
        self.mapweb_view.settings().setAttribute(QWebEngineSettings.JavascriptEnabled, True)

        pass


    def open_developer_tools(self):
        """Open Developer Tools in QWebEngineView and keep it open."""
        if self.dev_tools is None:
            self.dev_tools = QWebEngineView()  # Create a new QWebEngineView for the DevTools
            self.mapweb_view.page().setDevToolsPage(self.dev_tools.page())  # Set the dev tools page
        self.dev_tools.show()  # Show the dev tools window

    def send(self, btn):
        # global cmd_end
        global sms_end
        cmd_to_send = btn.get_cmd()
        if cmd_to_send:
            if cmd_to_send == sms:  # if need to send SMS
                self.write(cmd_to_send.encode("ascii") + sms_end)
            else:
                if isinstance(cmd_to_send, bytes):  # if type of cmd_to_send is bytes
                    # self.write(cmd_to_send.encode("ascii") + cmd_end)
                    self.write(cmd_to_send)
                else:
                    print(
                        "send(): something went wrong sending to UART (ASCII encoding failed)!"
                    )

    def send_any(self):
        global cmd_end
        if self.port.com_opened:
            ref = self.sender()  # get object created received signal
            cmd_to_send = (
                ref.parent().any_field.text()
            )  # get text from any_field using parent
            if cmd_to_send:
                self.write(cmd_to_send.encode("ascii") + cmd_end)

    def ports_info(self):
        ser_info = QSerialPortInfo()
        ports = ser_info.availablePorts()
        self.term.insertPlainText("\r" + "-" * 18 + " Ports info " + "-" * 18 + "\r")
        for ser in ports:
            self.term.insertPlainText(ser.portName() + "\r")
            self.term.insertPlainText(ser.description() + "\r")
            if ser.hasVendorIdentifier():
                self.term.insertPlainText("VID: " + hex(ser.vendorIdentifier()) + "\r")
            if ser.hasProductIdentifier():
                self.term.insertPlainText("PID: " + hex(ser.productIdentifier()) + "\r")
            self.term.insertPlainText("Manufacturer: " + ser.manufacturer() + "\r")
            self.term.insertPlainText("-" * 50 + "\r")
        self.term.ensureCursorVisible()

    def get_free_ports(self):
        n = 0
        self.term.insertPlainText("\r" + "-" * 17 + " Free ports " + "-" * 17 + "\r")
        temp_port = QSerialPort()
        while n < nmax:
            n = n + 1
            temp_port.setPortName("COM" + str(n))
            res = temp_port.open(QIODevice.ReadWrite)
            if res:  # port was successfully opened
                self.term.insertPlainText("COM" + str(n) + "\r")
                temp_port.close()
        self.term.insertPlainText("-" * 50 + "\r")
        self.term.ensureCursorVisible()

    def write(self, data):
        global echo
        if echo:
            str_data = self.decode_and_prepare(b"    <<<    " + data)
            self.term.insertPlainText(str_data)
            self.term.ensureCursorVisible()
        self.port.write(data)

    def clear_term(self):
        try:
            self.term.clear()  # clear terminal
            self.statusBar().showMessage("Terminal cleared")
        except Exception:
            self.statusBar().showMessage("Failed to clear terminal!")

    def copy(self):
        try:
            curs = self.term.textCursor()  # cursor, used when unselecting all
            self.term.selectAll()  # select all
            self.term.copy()  # copy to the clipboard
            self.term.setTextCursor(curs)  # unselect all
            self.statusBar().showMessage("Successfully copied from terminal")
        except Exception:
            self.statusBar().showMessage("Failed to copy from terminal!")

    def cut(self):
        try:
            self.term.selectAll()  # select all
            self.term.copy()  # copy to the clipboard
            self.term.clear()  # clear terminal
            self.statusBar().showMessage("Successfully cut from terminal")
        except Exception:
            self.statusBar().showMessage("Failed to cut from terminal!")
        
    def expose_map_js(self):
        """Add a script to expose the map object globally."""
        expose_script = """
            document.addEventListener("DOMContentLoaded", function() {
                window.map = map;
                console.log('Map object has been exposed to window.map.');
            });
        """
        # Inject this script into the QWebEngineView
        self.mapweb_view.page().runJavaScript(expose_script)

    def update_map(self):
        """Render the Folium map and dynamically detect the map object."""
        # Render the folium map as usual
        data = self.map.get_root().render()

        # Inject JavaScript to dynamically detect and expose the map object
        data = data.replace(
            "<script>",
            """<script>
            function waitForMap() {
                // Search for the dynamically generated map object (window.map_*)
                for (var key in window) {
                    if (window.hasOwnProperty(key) && key.startsWith('map_')) {
                        window.map = window[key];  // Assign the dynamically generated map to window.map
                        console.log('Map object has been exposed to window.map:', key);
                        return;
                    }
                }

                // Retry if the map is not yet initialized
                console.log('Waiting for the map to initialize...');
                setTimeout(waitForMap, 100);  // Retry every 100ms
            }

            document.addEventListener("DOMContentLoaded", function() {
                waitForMap();  // Start waiting for map initialization
            });
            """
        )

        # Load the map into QWebEngineView
        self.mapweb_view.setHtml(data)

    def closeEvent(self, event):
        self.port.close_port()
        event.accept()

    @staticmethod
    def nice_hex(
        binstr,
    ):  # convert binary string to readable HEX-like string: F1 34 0A 5D 00 7A...
        nicestr = ""
        for x in binstr:
            nicestr = nicestr + bytes([x]).hex().upper() + " "
        return nicestr[:-1]

    @staticmethod
    def show_hex(ch):  # convert byte to readable HEX-like symbol like: <0x1A>
        return "<0x" + ch.hex().upper() + ">"

    def decode_and_format(
        self, binstr
    ):  # types of binstr: <class 'PySide6.QtCore.QByteArray'>, <class 'bytes'>
        global time_stamp
        global new_line
        ascii_str = ""
        # for i in range(0, binstr.size()):
        for i in binstr:
            if isinstance(
                i, int
            ):  # if type of binstr is <bytes> then type of i will be <int>!
                i = bytes([i])  # convert <int> to <bytes>
            if (
                i == b"\x00"
            ):  # when self.term.insertPlainText('\x00') we get Exception: ValueError: embedded null character
                ascii_symbol = "<0x00>"  # replace byte 0x00 with string '<0x00>'
            else:
                ascii_symbol = self.show_hex(i)
                # try:
                #     ascii_symbol = i.decode("ascii")
                # except Exception:
                #     ascii_symbol = self.show_hex(i)
            if ascii_symbol == "\r" or ascii_symbol == "\n":
                new_line = 1
                ascii_symbol = ""  # remove '\r' and '\n' to not to print empty lines
            else:
                if new_line:
                    ascii_str = ascii_str + "\r"
                    new_line = 0
                    if time_stamp:
                        curr_time = datetime.datetime.now()
                        ascii_str = (
                            ascii_str + curr_time.strftime("%H:%M:%S:%f")[:12] + "    "
                        )
            ascii_str = ascii_str + ascii_symbol
        return ascii_str

    def on_port_rx(self):
        num_rx_bytes = self.port.ser.bytesAvailable()
        rx_bytes = self.port.ser.read(num_rx_bytes)
        rx_bytes = bytes(rx_bytes)
        # Append the received bytes to the buffer
        self.rx_buffer.extend(rx_bytes)
        # Check for the specific binary sequence
        # print(f"Received bytes: {[hex(b) for b in rx_bytes]}")
        # check_for_sequence(self, rx_bytes)
        # Check for complete messages in the buffer
        while self.has_complete_message():
            # print("Complete message found")
            # Extract the complete message from the buffer
            complete_message = self.extract_complete_message()
            # print(f"Complete message: {[hex(b) for b in complete_message]}")
            # Process the complete message
            check_for_sequence(self, complete_message)

    def has_complete_message(self):
        """
        Check if the buffer contains a complete message.
        """
        # print(f"Buffer: {[hex(b) for b in self.rx_buffer]}")
        if len(self.rx_buffer) < 4:
            # print("Not enough data to extract message type and length")
            return False  # Minimum length for a message is 4 bytes

        if self.rx_buffer[0] != 0x24:
            print("No start byte found")
            # Remove bytes until we find the start byte 0x24
            while self.rx_buffer and self.rx_buffer[0] != 0x24:
                # print("Removing byte:", hex(self.rx_buffer[0]))
                self.rx_buffer.pop(0)
            return False

        message_type = self.rx_buffer[1]
        if message_type in range(0x42, 0x49) or message_type in range(0x52, 0x59):
            message_length = 2 + (message_type & 0x0F)  # Fixed length messages
        elif message_type in [0x4F, 0x5F]:
            if len(self.rx_buffer) < 6:
                return False  # Minimum length for variable length message is 6 bytes
            message_length = int.from_bytes(self.rx_buffer[3:5], byteorder='little')  # Variable length messages
            # message_length = 6 + (self.rx_buffer[2] << 8 | self.rx_buffer[3])  # Variable length messages
        else:
            print("Unknown message type")
            return False  # Unknown message type
        # if len(self.rx_buffer) < message_length:
        #     print("Not enough data to extract complete message")
        # else:
        #     print(f"Message type: {hex(message_type)}, Message length: {message_length}")
        # print(f"Message type: {hex(message_type)}, Message length: {message_length}")
        # print(f"Buffer: {[hex(b) for b in self.rx_buffer]}")
        # Ensure the buffer has enough data to check the end byte
        if len(self.rx_buffer) <= message_length:
            return False
        # print(f"buff len: {len(self.rx_buffer)}, Message length: {message_length}")
        return self.rx_buffer[message_length] == 0x23

    def extract_complete_message(self):
        """
        Extract a complete message from the buffer.
        """
        message_type = self.rx_buffer[1]
        if message_type in range(0x42, 0x49) or message_type in range(0x52, 0x59):
            message_length = 2 + (message_type & 0x0F)  # Fixed length messages
        elif message_type in [0x4F, 0x5F]:
            length = (self.rx_buffer[2] << 8) | self.rx_buffer[3]
            message_length = length  # Variable length messages

        complete_message = self.rx_buffer[:message_length]
        self.rx_buffer = self.rx_buffer[message_length:]
        return complete_message

    def echo_box_toggled(self, checked):
        global echo
        if checked:
            echo = 1
        else:
            echo = 0

    def time_box_toggled(self, checked):
        global time_stamp
        if checked:
            time_stamp = 1
        else:
            time_stamp = 0

    def indicate_port_error(
        self, err
    ):  # separated function for indication is a good idea if we have more than one serial port
        if err == QSerialPort.SerialPortError.NoError:
            err_msg = "OK"
        elif err == QSerialPort.SerialPortError.DeviceNotFoundError:
            err_msg = "device not found"
        elif err == QSerialPort.SerialPortError.PermissionError:
            err_msg = "permission error"
        elif err == QSerialPort.SerialPortError.OpenError:
            err_msg = "open error"
        elif err == QSerialPort.SerialPortError.NotOpenError:
            err_msg = "not open error"
        elif err == QSerialPort.SerialPortError.WriteError:
            err_msg = "write error"
        elif err == QSerialPort.SerialPortError.ReadError:
            err_msg = "read error"
        elif err == QSerialPort.SerialPortError.ResourceError:
            err_msg = "resource error"
        elif err == QSerialPort.SerialPortError.UnsupportedOperationError:
            err_msg = "unsupported operation"
        elif err == QSerialPort.SerialPortError.TimeoutError:
            err_msg = "timeout error"
        elif err == QSerialPort.SerialPortError.UnknownError:
            err_msg = "unknown error"
        else:
            err_msg = "undefined error"
        self.statusBar().showMessage("Serial port: " + err_msg)

    def port_error(self):
        self.indicate_port_error(self.port.ser.error())


def main():
    app = QApplication([])
    main_win = MainWindow()
    main_win.resize(window_min_width, window_min_height)
    main_win.show()
    sys.exit(app.exec())  # PySide6
    # sys.exit(app.exec_())        # PySide2


if __name__ == "__main__":
    main()
