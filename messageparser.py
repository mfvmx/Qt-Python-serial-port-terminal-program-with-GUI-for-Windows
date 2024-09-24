# messageparser.py
import struct
from variables import *  # Import the global device_status_table variable

pittime = 0x45
devicestatus = 0x46
devicelocation = 0x4A
trackstatus = 0x4C
laptime = 0x50
device_version = 0x56
driver_id = 0x5C

# devicestatuslist
class DeviceStatusList:
    def __init__(self, did, flag, batv, extv, rssi, temp, lasttime):
        self.did = did
        self.flag = flag
        self.batv = batv
        self.extv = extv
        self.rssi = rssi
        self.temp = temp
        self.lasttime = lasttime

    def __repr__(self):
        return f"DeviceStatusList(did={self.did}, flag={self.flag}, batv={self.batv}, extv={self.extv}, rssi={self.rssi}, temp={self.temp}, lasttime={self.lasttime})"

class DevicePitTime:
    def __init__(self, did, entrytime, exittime):
        self.did = did
        self.entrytime = entrytime
        self.exittime = exittime

    def __repr__(self):
        return f"DevicePitTime(did={self.did}, entrytime={self.entrytime}, exittime={self.exittime})"

class DeviceLocation:
    def __init__(self, did, latitude, longitude, speed, zone, last_seen):
        self.did = did
        self.latitude = latitude
        self.longitude = longitude
        self.speed = speed
        self.zone = zone
        self.last_seen = last_seen

    def __repr__(self):
        return f"DeviceLocation(did={self.did}, latitude={self.latitude}, longitude={self.longitude}, speed={self.speed}, zone={self.zone}, last_seen={self.last_seen})"

def check_for_sequence(self, data):
    # global device_status_table # Use the global device_status_table variable
    # sequence = b"\x24\x5F"
    # if sequence in data:
        # index = data.find(sequence)
        # print(f"Sequence {sequence} detected at position {index}!")

        # if index + 3 < len(data):
    command_type = data[2]
    message_length = int.from_bytes(data[3:5], byteorder='little')
    # device_status_table[0][0] = command_type
    # device_status_table[0][1] = message_length
    if command_type == pittime:
        parse_pittime(self, data, 0)
    elif command_type == devicelocation:
        parse_devicelocation(self, data, 0)
    elif command_type == devicestatus:
        parse_devicestatus(self, data, 0)
    # else:
        # print(f"Unknown message type: {hex(command_type)}")
    # self.modelDeviceSatus.layoutChanged.emit()
    # self.modelDeviceSatus.dataChanged.emit(self.modelDeviceSatus.index(0, 0), self.modelDeviceSatus.index(0, 1))
    # print(f'Message Type: {hex(command_type)}, Message Length: {message_length}')
    self.statusBar().showMessage(f'Message Type: {hex(command_type)}, Message Length: {message_length}')

def parse_pittime(self, data, index):
    message_length = int.from_bytes(data[index + 3:index + 5], byteorder='little')
    devicepittimelists = []
    for i in range(message_length // 12):
        start = index + 5 + i * 12
        did = int.from_bytes(data[start:start + 4], byteorder='little')
        entrytime = int.from_bytes(data[start + 4:start + 8], byteorder='little')
        exittime = int.from_bytes(data[start + 8:start + 12], byteorder='little')
        devicepittimelists.append(DevicePitTime(did, entrytime, exittime))
    for devicepittime in devicepittimelists:
        did_exists = False
        for row in self.modelPitTimes._data:
            if row[0] == devicepittime.did:
                row[1] = devicepittime.entrytime
                row[2] = devicepittime.exittime
                did_exists = True
                break
        if not did_exists:
            self.modelPitTimes._data.append([devicepittime.did, devicepittime.entrytime, devicepittime.exittime])
        self.modelPitTimes.layoutChanged.emit()
        # print(self.modelPitTimes._data)

def parse_devicestatus(self, data, index):
    message_length = int.from_bytes(data[index + 3:index + 5], byteorder='little')
    # print(f'parse_devicestatus: {" ".join(f"{byte:02X}" for byte in data)}')
    # print(f'Message Type: {hex(command_type)}, Message Length: {message_length}')
    devicestatuslists = []
    for i in range(message_length // 13):
        start = index + 5 + i * 13
        # print(f'Start: {start}, values: {hex(data[start])}')
        did = int.from_bytes(data[start:start + 4], byteorder='little')
        # print(' '.join(f'{byte:02X}' for byte in data[start:start + 4]))
        flag = data[start + 4]
        batv = data[start + 5]
        extv = data[start + 6]
        rssi = data[start + 7]
        temp = data[start + 8]
        lasttime = int.from_bytes(data[start + 9:start + 13], byteorder='little')
        devicestatuslists.append(DeviceStatusList(did, flag, batv, extv, rssi, temp, lasttime))
    # lrc = data[index + message_length - 1]
    # endofmessage = data[index + message_length]
    # print(f'Message Type: {hex(command_type)}, Message Length: {message_length}, Size: {message_length}, LRC: {hex(lrc)}, End of Message: {hex(endofmessage)}')
    # self.statusBar().showMessage(f'Message Type: {hex(command_type)}, Message Length: {message_length}, LRC: {hex(lrc)}, End of Message: {hex(endofmessage)}')
    # Print the parsed device status lists
    for devicestatus in devicestatuslists:
        # print(devicestatus)
        # Check if DID already exists in device_status_table
        did_exists = False
        for row in self.modelDeviceSatus._data:
            if row[0] == devicestatus.did:
                # Overwrite the existing row
                row[1] = devicestatus.flag
                if devicestatus.batv != 0:
                    row[2] = devicestatus.batv
                if devicestatus.extv != 0:
                    row[3] = devicestatus.extv
                row[4] = devicestatus.rssi
                if devicestatus.temp != 0:
                    row[5] = devicestatus.temp
                row[6] = devicestatus.lasttime
                did_exists = True
                break
        if not did_exists:
            # Append a new row if DID does not exist
            self.modelDeviceSatus._data.append([devicestatus.did, devicestatus.flag, devicestatus.batv, devicestatus.extv, devicestatus.rssi, devicestatus.temp, devicestatus.lasttime])
        # Emit dataChanged signal for the entire table
        self.modelDeviceSatus.layoutChanged.emit()
        # self.modelDeviceSatus.dataChanged.emit(self.modelDeviceSatus.index(0, 0), self.modelDeviceSatus.index(0, 1))
        # print(self.modelDeviceSatus._data)

def parse_devicelocation(self, data, index):
    message_length = int.from_bytes(data[index + 3:index + 5], byteorder='little')
    devicelocationlists = []
    # print(f'parse_devicelocation: {" ".join(f"{byte:02X}" for byte in data)}')
    for i in range((message_length - 14) // 16):
        start = index + 13 + i * 16
        did = int.from_bytes(data[start:start + 4], byteorder='little')
        # print(' '.join(f'{byte:02X}' for byte in data[start:start + 4]))
        latitude = struct.unpack('<f', data[start + 4:start + 8])[0]
        # print(' '.join(f'{byte:02X}' for byte in data[start + 4:start + 8]))
        longitude = struct.unpack('<f', data[start + 8:start + 12])[0]
        speed = data[start + 12]
        zone = data[start + 13]
        last_seen = int.from_bytes(data[start + 14:start + 16], byteorder='little')
        devicelocationlists.append(DeviceLocation(did, latitude, longitude, speed, zone, last_seen))
    for devicelocation in devicelocationlists:
        did_exists = False
        for row in self.modelDeviceLocation._data:
            if row[0] == devicelocation.did:
                row[1] = devicelocation.latitude
                row[2] = devicelocation.longitude
                row[3] = devicelocation.speed
                row[4] = devicelocation.zone
                row[5] = devicelocation.last_seen
                self.add_or_update_marker(devicelocation.did, devicelocation.latitude, devicelocation.longitude, devicelocation.did, "#ffffff")
                did_exists = True
                break
        if not did_exists:
            self.modelDeviceLocation._data.append([devicelocation.did, devicelocation.latitude, devicelocation.longitude, devicelocation.speed, devicelocation.zone, devicelocation.last_seen])
        self.modelDeviceLocation.layoutChanged.emit()
        # print(self.modelDeviceLocation._data)