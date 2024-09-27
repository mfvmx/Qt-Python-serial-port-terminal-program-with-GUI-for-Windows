# messageparser.py
import struct
from variables import *  # Import the global device_status_table variable

pittime = 0x45
devicestatus = 0x46
devicelocation = 0x4A
trackstatus = 0x4C
laptime = 0x50
device_version = 0x56
orgsettings = 0x57
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

class OrgSettings:
    def __init__(self, pVer, orgID, orgV, aYel, TrkMs, PitRate, PitSpd, L35, H35, AccMs, AccSpl, AccMg, VrtSc):
        self.pVer = pVer
        self.orgID = orgID
        self.orgV = orgV
        self.aYel = aYel
        self.TrkMs = TrkMs
        self.PitRate = PitRate
        self.PitSpd = PitSpd
        self.L35 = L35
        self.H35 = H35
        self.AccMs = AccMs
        self.AccSpl = AccSpl
        self.AccMg = AccMg
        self.VrtSc = VrtSc

    def __repr__(self):
        return (f"OrgSettings(pVer={self.pVer}, orgID={self.orgID}, orgV={self.orgV}, "
                f"aYel={self.aYel}, TrkMs={self.TrkMs}, PitRate={self.PitRate}, PitSpd={self.PitSpd}, L35={self.L35}, H35={self.H35}, "
                f"AccMs={self.AccMs}, AccSpl={self.AccSpl}, AccMg={self.AccMg}, VrtSc={self.VrtSc})")

class DeviceDebug:
    def __init__(self, channel=None, did1=None, latitude=None, longitude=None, speed=None, zone=None, rssi=None, unicast=None, lap_entry=None, lap_count=None, last_seen=None):
        self.channel = channel
        self.did1 = did1
        self.latitude = latitude
        self.longitude = longitude
        self.speed = speed
        self.zone = zone
        self.rssi = rssi
        self.unicast = unicast
        self.lap_entry = lap_entry
        self.lap_count = lap_count
        self.last_seen = last_seen

    def __repr__(self):
        return (f"DeviceDebug(channel={self.channel}, did1={self.did1}, latitude={self.latitude}, "
                f"longitude={self.longitude}, speed={self.speed}, zone={self.zone}, "
                f"rssi={self.rssi}, unicast={self.unicast}, lap_entry={self.lap_entry}, lap_count={self.lap_count}, last_seen={self.last_seen})")

def check_for_sequence(self, data):
    command_type = data[2]
    message_length = int.from_bytes(data[3:5], byteorder='little')
    if command_type == devicestatus:
        parse_devicestatus(self, data, 0)
    elif command_type == orgsettings:
        parse_orgsettings(self, data, 0)
    # else:
    #     print(f"Unknown command type: {hex(command_type)}")
    # self.modelDeviceSatus.layoutChanged.emit()
    # self.modelDeviceSatus.dataChanged.emit(self.modelDeviceSatus.index(0, 0), self.modelDeviceSatus.index(0, 1))
    # print(f'Message Type: {hex(command_type)}, Message Length: {message_length}')
    self.statusBar().showMessage(f'Message Type: {hex(command_type)}, Message Length: {message_length}')

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
    # self.statusBar().showMessage(f'Message Type: {hex(devicestatus)}, Message Length: {message_length}, LRC: {hex(lrc)}, End of Message: {hex(endofmessage)}')
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

def parse_orgsettings(self, data, index):
    message_length = int.from_bytes(data[index + 3:index + 5], byteorder='little')
    pVer = data[index + 5]
    orgID = int.from_bytes(data[index + 6:index + 8], byteorder='little')
    orgV = data[index + 8]
    trkID = int.from_bytes(data[index + 9:index + 11], byteorder='little')
    trkV = data[index + 11]
    aYel = data[index + 12]
    Ch1 = data[index + 13]
    Ch2 = data[index + 14]
    Ch3 = data[index + 15]
    Ch4 = data[index + 16]
    w2ch = int.from_bytes(data[index + 17:index + 19], byteorder='little')
    w5ch = int.from_bytes(data[index + 19:index + 21], byteorder='little')
    TrkMs = int.from_bytes(data[index + 21:index + 23], byteorder='little')
    PitRate = data[index + 23]
    PitSpd = data[index + 24]
    L35 = data[index + 25]
    H35 = data[index + 26]
    AccMs = int.from_bytes(data[index + 27:index + 29], byteorder='little')
    AccSpl = int.from_bytes(data[index + 29:index + 31], byteorder='little')
    AccMg = int.from_bytes(data[index + 31:index + 35], byteorder='little')
    VrtSc = data[index + 35]
    TBD = int.from_bytes(data[index + 36:index + 39], byteorder='little')
    org_settings = OrgSettings(pVer, orgID, orgV, aYel, TrkMs, PitRate, PitSpd, L35, H35, AccMs, AccSpl, AccMg, VrtSc)
    # print(org_settings)
    # Update the model or UI as needed
    self.modelOrgSettings._data.append([org_settings.pVer, org_settings.orgID, org_settings.orgV, org_settings.aYel, org_settings.TrkMs, org_settings.PitRate, org_settings.PitSpd, org_settings.L35, org_settings.H35, org_settings.AccMs, org_settings.AccSpl, org_settings.AccMg, org_settings.VrtSc])
    self.modelOrgSettings.layoutChanged.emit()

def parse_debug_data(self, data):
    # Split the data into fields
    fields = data.split(b',')
    print(fields)
    # Create a dictionary to map field names to values
    field_dict = {}
    did1_set = False  # Flag to ensure only the first DID is considered
    for field in fields:
        key_value = field.split(b':')
        if len(key_value) == 2:
            key = key_value[0].strip().decode('utf-8')
            value = key_value[1].strip()
            if key == 'DID' and not did1_set:
                field_dict['DID1'] = value
                did1_set = True
            elif key != 'DID':
                field_dict[key] = value
        elif len(key_value) > 2:  # Handle combined fields like 'sfGPS: Lat: 34.149227'
            key = key_value[0].strip().decode('utf-8')
            sub_key = key_value[1].strip().decode('utf-8')
            value = key_value[2].strip()
            field_dict[sub_key] = value

    # Extract the channel value
    channel_field = next((field for field in fields if field.startswith(b'--------Ch')), None)
    channel = int(channel_field.split(b'Ch')[1]) if channel_field else None

    # Extract the relevant fields from the dictionary
    did1 = int(field_dict.get('DID1', b'0'))
    latitude = float(field_dict.get('Lat', b'0.0'))
    longitude = float(field_dict.get('Lng', b'0.0'))
    speed = int(field_dict.get('MPH', b'0'))
    zone = int(field_dict.get('Zone', b'0'))
    rssi = int(field_dict.get('RSSI', b'0'))
    unicast = int(field_dict.get('Unicast', b'0'))
    lap_entry = field_dict.get('Lap Entry', b'').decode('utf-8')
    lap_count = int(field_dict.get('Lap Count', b'0'))
    # Print extracted values for debugging
    print(f"Channel: {channel}, DID1: {did1}, Latitude: {latitude}, Longitude: {longitude}, Speed: {speed}, Zone: {zone}, RSSI: {rssi}, Unicast: {unicast}, Lap Entry: {lap_entry}, Lap Count: {lap_count}")

    # Create a DeviceDebug object
    device_debug = DeviceDebug(channel, did1, latitude, longitude, speed, zone, rssi, unicast, lap_entry, lap_count)
    print(device_debug)
    # Update the table sorted by the first DID value
    did_exists = False
    for row in self.modelDebug._data:
        if row[1] == device_debug.did1 and row[0] == device_debug.channel:
            row[2] = device_debug.latitude
            row[3] = device_debug.longitude
            row[4] = device_debug.speed
            row[5] = device_debug.zone
            row[6] = device_debug.rssi
            row[7] = device_debug.unicast
            row[8] = device_debug.lap_entry
            row[9] = device_debug.lap_count
            self.add_or_update_marker(device_debug.did1, device_debug.latitude, device_debug.longitude, device_debug.speed, "#ffffff")
            did_exists = True
            break
    if not did_exists:
        self.modelDebug._data.append([device_debug.channel, device_debug.did1, device_debug.latitude, device_debug.longitude, device_debug.speed, device_debug.zone, device_debug.rssi, device_debug.unicast, device_debug.lap_entry, device_debug.lap_count])
    self.modelDebug.layoutChanged.emit()