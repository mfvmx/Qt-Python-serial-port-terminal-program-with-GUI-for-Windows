from PySide6.QtCore import Qt, QAbstractTableModel, QModelIndex
from PySide6.QtGui import QColor, QIcon  # Import QIcon from QtGui
from variables import *

DID_col = "      DID      "
flag_col = "    Flag    "
battery_col = "  Batt  "
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
lap_entry_col = " Lap Entry "
lap_count_col = " Lap Count "

class TableModelStatus(QAbstractTableModel):
    def __init__(self, data):
        QAbstractTableModel.__init__(self)
        # super(CustomTableModel, self).__init__()
        self._data = data
        self._headers = [DID_col, flag_col, battery_col, ext_power_col,rssi_col,temp_col,last_col]  # Define the column headers
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

class CustomTableModelPitTime(QAbstractTableModel):
    def __init__(self, data):
        QAbstractTableModel.__init__(self)
        # super(CustomTableModel, self).__init__()
        self._data = data
        self._headers = [DID_col, "Entry", "Exit"]  # Define the column headers
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
            "pVer", "orgID", "orgV", "trkID", "trkV", "aYel",
            "TrkMs", "PitRate", "PitSpd", "L35", "H35", "AccMs", "AccSpl",
            "AccMg", "VrtSc", "TBD"
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