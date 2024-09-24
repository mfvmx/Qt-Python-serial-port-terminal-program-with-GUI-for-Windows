# variables.py
import os
###############################################################
no_flag_commanded = 0
black_flag_indiv = 1
meatball_indiv = 2
pit_courtesy_indiv = 3
stalled_car_indiv = 4
blank_flag = 66
purple_flag = 67
black_flag = 68
green_flag = 71
checkered_flag = 72
emergency_10_25g = 75
emergency_26_50g = 76
emergency_51_75g = 77
emergency_76_99g = 78
emergency_greater_than_99g = 79
red_flag = 82
safety_car_flag = 83
low_power_mode_0 = 85
low_power_mode_1 = 86
low_power_mode_2 = 87
low_power_mode_3 = 88
low_power_mode_4 = 89
low_power_mode_5 = 90
double_yellow_full_course_flag = 91
ev_white_with_cross_flag = 95
custom_message = 98
clear_local = 100
standing_yellow_local = 101
waving_yellow_local = 102
debris_local = 104
yellow_debris_local = 105
waving_yellow_debris_local = 106
white_local = 108
yellow_white_local = 109
waving_yellow_white_local = 110
debris_white_local = 112
yellow_debris_white_local = 113
waving_debris_white_local = 114
blue_local = 116

script_dir = os.path.dirname(__file__)
# Construct the relative path to the image file
black_flag_icon_path = os.path.join(script_dir, 'Images', 'Flags', 'black_40x40.png')
blank_flag_icon_path = os.path.join(script_dir, 'Images', 'Flags', 'blank_40x40.png')
debris_white_local_icon_path = os.path.join(script_dir, 'Images', 'Flags', 'whitedb_40x40.png')
green_flag_icon_path = os.path.join(script_dir, 'Images', 'Flags', 'green_40x40.png')
checkered_flag_icon_path = os.path.join(script_dir, 'Images', 'Flags', 'checkerd_40x40.png')
debris_local_icon_path = os.path.join(script_dir, 'Images', 'Flags', 'debris_40x40.png')
purple_flag_icon_path = os.path.join(script_dir, 'Images', 'Flags', 'purple_40x40.png')
red_flag_icon_path = os.path.join(script_dir, 'Images', 'Flags', 'red_40x40.png')
waving_yellow_local_icon_path = os.path.join(script_dir, 'Images', 'Flags', 'wavingyel_40x40.png')
white_local_icon_path = os.path.join(script_dir, 'Images', 'Flags', 'white_40x40.png')
   
# Tab button [0,1,2,3]:
# 0 - label of the button
# 1 - command to send
# 2 - foreground color of the button
# 3 - background color of the button

# --------------- TAB1 BUTTONS ---------------
T1_0 = [
    ["Null", b'\x24\x42\x00\xBE\x23', "", "#85c6ff"],
    ["Blank", b'\x24\x42\x42\x7C\x23', "", "#c9c3c9"],
    ["Purple", b'\x24\x42\x43\x7B\x23', "", "#d900ff"],
    ["Black", b'\x24\x42\x44\x7A\x23', "", "#333333"],
]

T1_1 = [
    ["Green", b'\x24\x42\x47\x77\x23', "", "#0fd920"],
    ["Checker", b'\x24\x42\x48\x76\x23', "", "#7c7c7c"],
    ["Red", b'\x24\x42\x52\x6C\x23', "", "#f20505"],
    ["Yellow", b'\x24\x42\x5B\x63\x23', "", "yellow"],
]

T1 = [T1_0, T1_1]

# --------------- TAB2 BUTTONS ---------------
T2_0 = [
    ["Get RSSI", "AT+CSQ", "", ""],
    ["", "", "", ""],
    ["AT+CREG?", "AT+CREG?", "", ""],
    ["AT+CREG=0", "AT+CREG=0", "", ""],
    ["AT+CREG=1", "AT+CREG=1", "", ""],
    ["AT+CREG=2", "AT+CREG=2", "", ""],
    ["", "", "", ""],
]

T2_1 = [
    ["Get APN", "AT+NETAPN?", "", ""],
    ["Set APN", 'AT+NETAPN="IP","",""', "", ""],
    ["", "", "", ""],
    ["Get PDP context", "AT+CGDCONT?", "", "yellow"],
    ["Set PDP context", 'AT+CGDCONT=1,"IP"', "", "yellow"],
]

T2_2 = [
    ["", "", "", ""],
    ["", "", "", ""],
    ["", "", "", ""],
    ["", "", "", ""],
    ["", "", "", ""],
]

T2 = [T2_0, T2_1, T2_2]

# --------------- TAB3 BUTTONS ---------------
T3_0 = [
    ["Get PPP state", "AT+XIIC?", "", ""],
    ["Set PPP link", "AT+XIIC=1", "", "#77dd77"],
    ["Close PPP link", "AT+XIIC=0", "", "pink"],
    ["", "", "", ""],
    ["Set TCP connection", "AT+TCPSETUP=0,google.com,80", "", ""],
    ["Request to send data", "AT+TCPSEND=0,10", "", ""],
    ["Send data", "HEAD  \r\n\r\n", "", ""],
    ["", "", "", ""],
]

T3_1 = [
    ["Get receive mode", "AT+RECVMODE?", "", ""],
    ["Send to UART, ASCII [1,0]", "AT+RECVMODE=1,0", "", ""],
    ["Send to UART, HEX [1,1]", "AT+RECVMODE=1,1", "", ""],
    ["", "", "", ""],
    ["", "", "", ""],
]

T3_2 = [
    ["", "", "", ""],
    ["", "", "", ""],
    ["", "", "", ""],
    ["", "", "", ""],
    ["", "", "", ""],
]

T3 = [T3_0, T3_1, T3_2]

device_status_table = []

device_location_table = []

# Sample data array (id, longitude, latitude)
data_array = [
    {"id": 1, "longitude": -74.006, "latitude": 40.7128},  # New York
    {"id": 2, "longitude": 139.6917, "latitude": 35.6895},  # Tokyo
    {"id": 3, "longitude": 2.3522, "latitude": 48.8566}  # Paris
]