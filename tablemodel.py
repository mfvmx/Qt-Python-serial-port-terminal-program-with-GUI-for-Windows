from PySide6.QtCore import Qt, QAbstractTableModel, QModelIndex
from PySide6.QtGui import QColor, QIcon  # Import QIcon from QtGui
from variables import *

DID_col = "      DID      "
DriverID_col = "   DriverID   "
flag_col = "    Flag    "
battery_col = "  Batt  "
ch1_col = "  Ch1  "
ch2_col = "  Ch2  "
ch3_col = "  Ch3  "
ch4_col = "  Ch4  "
com_count = "Command Count"
ext_power_col = "  ExtPwr  "
channel_col = "  Channel  "
did1_col = "      DID1      "
did2_col = "      DID2      "
latitude_col = "  Latitude  "
longitude_col = " Longitude "
speed_col = "   Speed   "
zone_col = "    Zone    "
rssi_col = "RSSI"
temp_col = "Temp"
last_col = "Lastseen"
unicast_col = " Unicast "
lap_entry_col = "   Lap Entry   "
lap_count_col = " Lap Count "
pit_entry_col = "   Pit Entry   "
pit_duration_col = " Pit Duration "

class TableModelTrackStatus(QAbstractTableModel): # Track Status Table Model
    def __init__(self, data):
        QAbstractTableModel.__init__(self)
        # super(CustomTableModel, self).__init__()
        self._data = data
        self._headers = [com_count, flag_col, ch1_col, ch2_col, ch3_col, ch4_col]  # Define the column headers
        self._sort_order = Qt.AscendingOrder

    def data(self, index, role):
        if role == Qt.DisplayRole: # Add this block to display data
            value = self._data[index.row()][index.column()]
            # Default return value
            return value

        if role == Qt.TextAlignmentRole: # Add this block to center the text
            return Qt.AlignVCenter + Qt.AlignHCenter

        if role == Qt.DecorationRole: # Add this block to display icons
            value = self._data[index.row()][index.column()]
            if self._headers[index.column()] == flag_col:
                if value == green_flag:
                    return QIcon(green_flag_icon_path)
                elif value == debris_white_local:
                    return QIcon(debris_white_local_icon_path)
                elif value == double_yellow_full_course_flag:
                    return QColor(Qt.yellow)
                elif value == checkered_flag:
                    return QIcon(checkered_flag_icon_path)
                elif value == black_flag:
                    return QIcon(black_flag_icon_path)
                elif value == blank_flag:
                    return QIcon(blank_flag_icon_path)
                elif value == purple_flag:
                    return QIcon(purple_flag_icon_path)
                elif value == red_flag:
                    return QIcon(red_flag_icon_path)
                elif value == debris_local:
                    return QIcon(debris_local_icon_path)
                elif value == waving_yellow_local:
                    return QIcon(waving_yellow_local_icon_path)
                elif value == white_local:
                    return QIcon(white_local_icon_path)

    def rowCount(self, index=QModelIndex()):
        return len(self._data)

    def columnCount(self, index=QModelIndex()):
        return len(self._headers)

    def headerData(self, section, orientation, role):
        if role != Qt.DisplayRole:
            return None
        if orientation == Qt.Horizontal:
            return self._headers[section]  # Return the appropriate header name
        else:
            return f"{section}"

    def sort(self, column, order):
        self.layoutAboutToBeChanged.emit()
        self._data.sort(key=lambda x: x[column], reverse=(order == Qt.DescendingOrder))
        self.layoutChanged.emit()

class TableModelStatus(QAbstractTableModel): # Device Status Table Model
    def __init__(self, data):
        QAbstractTableModel.__init__(self)
        # super(CustomTableModel, self).__init__()
        self._data = data
        self._headers = [DID_col, flag_col, battery_col, ext_power_col, rssi_col, temp_col, last_col]  # Define the column headers
        self._sort_order = Qt.AscendingOrder

    def data(self, index, role):
        if role == Qt.DisplayRole: # Add this block to display data
            value = self._data[index.row()][index.column()]
            if self._headers[index.column()] == battery_col or self._headers[index.column()] == ext_power_col:
                return f"{value*0.03:.2f}v"
            # Default return value
            return value

        if role == Qt.TextAlignmentRole: # Add this block to center the text
            return Qt.AlignVCenter + Qt.AlignHCenter

        if role == Qt.DecorationRole: # Add this block to display icons
            value = self._data[index.row()][index.column()]
            if self._headers[index.column()] == flag_col:
                if value == green_flag:
                    return QIcon(green_flag_icon_path)
                elif value == debris_white_local:
                    return QIcon(debris_white_local_icon_path)
                elif value == double_yellow_full_course_flag:
                    return QColor(Qt.yellow)
                elif value == checkered_flag:
                    return QIcon(checkered_flag_icon_path)
                elif value == black_flag:
                    return QIcon(black_flag_icon_path)
                elif value == blank_flag:
                    return QIcon(blank_flag_icon_path)
                elif value == purple_flag:
                    return QIcon(purple_flag_icon_path)
                elif value == red_flag:
                    return QIcon(red_flag_icon_path)
                elif value == debris_local:
                    return QIcon(debris_local_icon_path)
                elif value == waving_yellow_local:
                    return QIcon(waving_yellow_local_icon_path)
                elif value == white_local:
                    return QIcon(white_local_icon_path)

    def rowCount(self, index=QModelIndex()):
        return len(self._data)

    def columnCount(self, index=QModelIndex()):
        return len(self._headers)

    def headerData(self, section, orientation, role):
        if role != Qt.DisplayRole:
            return None
        if orientation == Qt.Horizontal:
            return self._headers[section]  # Return the appropriate header name
        else:
            return f"{section}"

    def sort(self, column, order):
        self.layoutAboutToBeChanged.emit()
        self._data.sort(key=lambda x: x[column], reverse=(order == Qt.DescendingOrder))
        self.layoutChanged.emit()

class CustomTableModelDriverID(QAbstractTableModel):
    def __init__(self, data):
        QAbstractTableModel.__init__(self)
        # super(CustomTableModel, self).__init__()
        self._data = data
        self._headers = [DID_col, DriverID_col]  # Define the column headers
        self._sort_order = Qt.AscendingOrder

    def data(self, index, role):
        if role == Qt.DisplayRole: # Add this block to display data
            if index.column() < len(self._data[index.row()]):
                value = self._data[index.row()][index.column()]
            # Default return value
            return value

        if role == Qt.TextAlignmentRole: # Add this block to center the text
            return Qt.AlignVCenter + Qt.AlignHCenter

    def rowCount(self, index):
        return len(self._data)

    def columnCount(self, index):
        return len(self._headers)

    def headerData(self, section, orientation, role):
        if role != Qt.DisplayRole:
            return None
        if orientation == Qt.Horizontal:
            return self._headers[section]  # Return the appropriate header name
        else:
            return f"{section}"
        
class CustomTableModelLapTime(QAbstractTableModel):
    def __init__(self, data):
        super().__init__()
        self._data = data
        self._headers = [DID_col, lap_entry_col, lap_count_col, "Formatted Time", "Time Difference"]  # Add new column header
        self._sort_order = Qt.AscendingOrder

    def data(self, index, role):
        if role == Qt.DisplayRole:  # Display data in cells
            if index.column() < len(self._data[index.row()]):
                value = self._data[index.row()][index.column()]
            
            if self._headers[index.column()] == lap_entry_col:
                return value  # Return raw lap entry value
            
            elif self._headers[index.column()] == "Formatted Time":
                raw_value = self._data[index.row()][self._headers.index(lap_entry_col)]
                hours = raw_value // 3600000
                minutes = (raw_value % 3600000) // 60000
                seconds = (raw_value % 60000) // 1000
                milliseconds = raw_value % 1000
                return f"{hours:02}:{minutes:02}:{seconds:02}.{milliseconds:03}"
            
            elif self._headers[index.column()] == "Time Difference":
                return self.get_time_difference(index.row())  # Compute time difference

            return value  # Default return value for other columns

        if role == Qt.TextAlignmentRole:  # Center text
            return Qt.AlignVCenter + Qt.AlignHCenter

    def get_time_difference(self, current_row):
        """Calculate the time difference between the current and previous lap."""
        current_did = self._data[current_row][self._headers.index(DID_col)]
        current_entry_time = self._data[current_row][self._headers.index(lap_entry_col)]

        # Find the previous lap for the same DID
        previous_entry_time = None
        for row in reversed(self._data[:current_row]):
            if row[self._headers.index(DID_col)] == current_did:
                previous_entry_time = row[self._headers.index(lap_entry_col)]
                break

        if previous_entry_time is None:
            return "N/A"  # No previous lap entry

        time_diff = current_entry_time - previous_entry_time
        minutes = (time_diff // 60000) % 60
        seconds = (time_diff // 1000) % 60
        milliseconds = time_diff % 1000
        return f"{minutes:02}:{seconds:02}.{milliseconds:03}"

    def rowCount(self, index):
        return len(self._data)

    def columnCount(self, index):
        return len(self._headers)

    def headerData(self, section, orientation, role):
        if role != Qt.DisplayRole:
            return None
        if orientation == Qt.Horizontal:
            return self._headers[section]  # Return the appropriate header name
        else:
            return f"{section + 1}"  # Return row numbers starting from 1


class CustomTableModelPitTime(QAbstractTableModel):
    def __init__(self, data):
        QAbstractTableModel.__init__(self)
        # super(CustomTableModel, self).__init__()
        self._data = data
        self._headers = [DID_col, pit_entry_col, pit_duration_col, "Formatted Time"]  # Define the column headers
        self._sort_order = Qt.AscendingOrder

    def data(self, index, role):
        if role == Qt.DisplayRole: # Add this block to display data
            if index.column() < len(self._data[index.row()]):
                value = self._data[index.row()][index.column()]
            if self._headers[index.column()] == pit_entry_col:
                return value  # Return raw value
            elif self._headers[index.column()] == "Formatted Time":
                raw_value = self._data[index.row()][self._headers.index(pit_entry_col)]
                hours = raw_value // 3600
                minutes = (raw_value % 3600) // 60
                seconds = raw_value % 60
                return f"{hours:02}:{minutes:02}:{seconds:02}"
            # Default return value
            return value

        if role == Qt.TextAlignmentRole: # Add this block to center the text
            return Qt.AlignVCenter + Qt.AlignHCenter

    def rowCount(self, index):
        return len(self._data)

    def columnCount(self, index):
        return len(self._headers)

    def headerData(self, section, orientation, role):
        if role != Qt.DisplayRole:
            return None
        if orientation == Qt.Horizontal:
            return self._headers[section]  # Return the appropriate header name
        else:
            return f"{section}"
        
class TableModelLocation(QAbstractTableModel):
    def __init__(self, data):
        QAbstractTableModel.__init__(self)
        # super(CustomTableModel, self).__init__()
        self._data = data
        self._headers = [DID_col, latitude_col, longitude_col, speed_col, zone_col, last_col]  # Define the column headers
        self._sort_order = Qt.AscendingOrder

    def data(self, index, role):
        if role == Qt.DisplayRole: # Add this block to display data
            value = self._data[index.row()][index.column()]
            if self._headers[index.column()] == battery_col or self._headers[index.column()] == ext_power_col:
                return f"{value*0.03:.2f}v"
            # Default return value
            return value

        if role == Qt.TextAlignmentRole: # Add this block to center the text
            return Qt.AlignVCenter + Qt.AlignHCenter

        if role == Qt.DecorationRole: # Add this block to display icons
            value = self._data[index.row()][index.column()]
            if self._headers[index.column()] == flag_col:
                if value == green_flag:
                    return QIcon(green_flag_icon_path)
                    # return QColor(Qt.green)
                elif value == double_yellow_full_course_flag:
                    return QColor(Qt.yellow)

    def rowCount(self, index):
        return len(self._data)

    def columnCount(self, index):
        return len(self._headers)

    def get_location_data(self, did):
        # Assuming self._data is a dictionary or list containing location data
        for row in self._data:
            if row[0] == did:  # DID is the first column
                return row[1], row[2]  # Return latitude and longitude
        return None

    def headerData(self, section, orientation, role):
        if role != Qt.DisplayRole:
            return None
        if orientation == Qt.Horizontal:
            return self._headers[section]  # Return the appropriate header name
        else:
            return f"{section}"

class TableModelOrgSettings(QAbstractTableModel):
    def __init__(self, data):
        QAbstractTableModel.__init__(self)
        self._data = data
        self._headers = [
            "pVer", "orgID", "orgV", "aYel",
            "TrkMs", "PitRate", "PitSpd", "L35", "H35", "AccMs", "AccSpl",
            "AccMg", "VrtSc"
        ]  # Define the column headers
        self._sort_order = Qt.AscendingOrder

    def data(self, index, role):
        if role == Qt.DisplayRole:  # Add this block to display data
            value = self._data[index.row()][index.column()]
            return value

        if role == Qt.TextAlignmentRole:  # Add this block to center the text
            return Qt.AlignVCenter + Qt.AlignHCenter

    def rowCount(self, index=QModelIndex()):
        return len(self._data)

    def columnCount(self, index=QModelIndex()):
        return len(self._headers)

    def headerData(self, section, orientation, role):
        if role != Qt.DisplayRole:
            return None
        if orientation == Qt.Horizontal:
            return self._headers[section]  # Return the appropriate header name
        else:
            return f"{section}"

    def sort(self, column, order):
        self.layoutAboutToBeChanged.emit()
        self._data.sort(key=lambda x: x[column], reverse=(order == Qt.DescendingOrder))
        self.layoutChanged.emit()

class TableModelDebug(QAbstractTableModel):
    def __init__(self, data):
        QAbstractTableModel.__init__(self)
        self._data = data
        self._headers = [channel_col, did1_col, did2_col, latitude_col, longitude_col, speed_col, zone_col, rssi_col, unicast_col, lap_entry_col, lap_count_col]  # Define the column headers
        self._sort_order = Qt.AscendingOrder

    def data(self, index, role):
        if role == Qt.DisplayRole:  # Add this block to display data
            value = self._data[index.row()][index.column()]
            return value

        if role == Qt.TextAlignmentRole:  # Add this block to center the text
            return Qt.AlignVCenter + Qt.AlignHCenter

        if role == Qt.DecorationRole:  # Add this block to display icons if needed
            value = self._data[index.row()][index.column()]
            # Add icon handling logic if needed
            # Example:
            # if self._headers[index.column()] == some_col:
            #     if value == some_value:
            #         return QIcon(some_icon_path)

    def rowCount(self, index=QModelIndex()):
        return len(self._data)

    def columnCount(self, index=QModelIndex()):
        return len(self._headers)

    def headerData(self, section, orientation, role):
        if role != Qt.DisplayRole:
            return None
        if orientation == Qt.Horizontal:
            return self._headers[section]  # Return the appropriate header name
        else:
            return f"{section}"

    def sort(self, column, order):
        self.layoutAboutToBeChanged.emit()
        self._data.sort(key=lambda x: x[column], reverse=(order == Qt.DescendingOrder))
        self.layoutChanged.emit()