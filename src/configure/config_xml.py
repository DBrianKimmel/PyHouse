#!/usr/bin/env python

"""
"""

import xml.etree.ElementTree as ET
import log
import xml_tools
import house
from lighting import lighting
from schedule import schedule
import web_server

# Various data stores.
House_Data = house.Location_Data
Location_Data = house.Location_Data
Room_Data = house.Room_Data
#
Light_Data = lighting.Light_Data
Button_Data = lighting.Button_Data
Controller_Data = lighting.Controller_Data
#
Schedule_Data = schedule.Schedule_Data
Log_Data = log.Log_Data
Web_Data = web_server.Web_Data

g_debug = 0
g_xmltree = ''

class ConfigTools(object):

    def get_bool(self, p_arg):
        l_ret = False
        if p_arg == 'True' or p_arg == True:
            l_ret = True
        return l_ret

    def get_float(self, p_obj, p_name):
        l_var = p_obj.findtext(p_name)
        try:
            l_var = float(l_var)
        except (ValueError, TypeError):
            l_var = 0.0
        return l_var

    def get_int(self, p_obj, p_name):
        l_var = p_obj.findtext(p_name)
        try:
            l_var = int(l_var)
        except (ValueError, TypeError):
            l_var = 0
        return l_var

    def put_bool(self, p_arg):
        l_text = 'False'
        if p_arg != False: l_text = 'True'
        return l_text

    def put_str(self, p_obj):
        try:
            l_var = str(p_obj)
        except AttributeError:
            l_var = 'no str value'
        return l_var

    def build_common(self, p_parent, p_title, p_obj):
        """Build a common entry.

        <p_parent>
            <p_title Name=p_obj.Name Key=p_obj.Key Active=o_obj.Active>
            </p_title>
        """
        l_ret = ET.SubElement(p_parent, p_title)
        l_ret.set('Name', p_obj.Name)
        l_ret.set('Key', str(p_obj.Key))
        l_ret.set('Active', self.put_bool(p_obj.Active))
        return l_ret

    def write_file(self):
        g_xmltree.write(self.m_filename, xml_declaration = True)


class ReadConfig(ConfigTools):
    """
    """

    m_filename = None

    def __init__(self):
        """Open the xml config file.

        If the file is missing, an empty minimal skeleton is created.
        """
        global g_xmltree
        self.m_filename = xml_tools.open_config()
        try:
            g_xmltree = ET.parse(self.m_filename)
        except SyntaxError:
            xml_tools.ConfigFile().create_empty_config_file(self.m_filename)
            g_xmltree = ET.parse(self.m_filename)
        self.m_root = g_xmltree.getroot()

    def read_location(self, p_entry):
        l_obj = house.HouseData()
        l_obj.Name = l_name = p_entry.get('Name')
        l_obj.Key = int(p_entry.get('Key'))
        l_obj.Active = self.get_bool(p_entry.get('Active'))
        if g_debug > 5: print "ReadConfig.read_location - Active=", l_obj.Active, l_obj.Name
        # Now read the location subsection
        l_entry = p_entry.find('Location')
        l_obj.Street = l_entry.findtext('Street')
        l_obj.City = l_entry.findtext('City')
        l_obj.State = l_entry.findtext('State')
        l_obj.ZipCode = l_entry.findtext('ZipCode')
        l_obj.Phone = l_entry.findtext('Phone')
        l_obj.Latitude = self.get_float(l_entry, 'Latitude')
        l_obj.Longitude = self.get_float(l_entry, 'Longitude')
        l_obj.TimeZone = self.get_float(l_entry, 'TimeZone')
        l_obj.SavingTime = self.get_float(l_entry, 'SavingTime')
        House_Data[l_obj.Key] = l_obj
        Location_Data[l_obj.Key] = l_obj
        House_Data[l_obj.Key] = l_obj
        self.m_location += 1
        return l_name

    def read_rooms(self, p_entry, p_house):
        l_rooms = p_entry.find('Rooms')
        l_list = l_rooms.iterfind('Room')
        for l_entry in l_list:
            l_obj = house.RoomData()
            l_obj.Name = l_entry.get('Name')
            l_obj.Key = int(l_entry.get('Key'))
            l_obj.HouseName = p_house
            l_obj.Active = self.get_bool(l_entry.get('Active'))
            l_obj.Comment = l_entry.findtext('Comment')
            l_obj.Corner = l_entry.findtext('Corner')
            l_obj.HouseName = l_entry.findtext('HouseName')
            l_obj.Size = l_entry.findtext('Size')
            Room_Data[l_obj.Key] = l_obj
            self.m_rooms += 1

    def read_houses(self):
        """Read house information, location and rooms.
        """
        l_count = 0
        self.m_location = 0
        self.m_rooms = 0
        try:
            l_sect = self.m_root.find('Houses')
            l_list = l_sect.iterfind('House')  # use l_sect to force error if it is missing
        except AttributeError:
            if g_debug > 0: print "Warning - in read_house - Adding 'Houses' section"
            l_sect = ET.SubElement(self.m_root, 'Houses')
            l_list = l_sect.iterfind('House')
        for l_house in l_list:
            l_name = self.read_location(l_house)
            self.read_rooms(l_house, l_name)
            l_count += 1
        return l_count

    def read_light_common(self, p_entry, p_obj):
        p_obj.Key = int(p_entry.get('Key'))
        p_obj.Name = p_entry.get('Name')
        p_obj.Active = self.get_bool(p_entry.get('Active'))
        p_obj.Comment = p_entry.findtext('Comment')
        p_obj.Coords = p_entry.findtext('Coords')
        p_obj.Dimmable = self.get_bool(p_entry.findtext('Dimmable'))
        p_obj.Family = l_fam = p_entry.findtext('Family')
        p_obj.RoomName = p_entry.findtext('Room')
        p_obj.HouseName = p_entry.findtext('House')
        p_obj.Type = p_entry.findtext('Type')
        if l_fam == 'UPB':
            p_obj.NetworkID = l_fam = p_entry.findtext('NetworkID')
            p_obj.Password = p_entry.findtext('Password')
            p_obj.UnitID = p_entry.findtext('UnitID')
        elif l_fam == 'Insteon':
            p_obj.Address = p_entry.findtext('Address')
            p_obj.Controller = p_entry.findtext('Controller')
            p_obj.DevCat = p_entry.findtext('DevCat')
            p_obj.GroupList = p_entry.findtext('GroupList')
            p_obj.GroupNumber = p_entry.findtext('GroupNumber')
            p_obj.Master = p_entry.findtext('Master')
            p_obj.ProductKey = p_entry.findtext('ProductKey')
            p_obj.Responder = p_entry.findtext('Responder')
        return p_obj

    def read_lights(self):
        l_count = 0
        try:
            l_sect = self.m_root.find('Lighting')
            l_list = l_sect.iterfind('Controllers')  # use l_sect to force error if Lighting is missing
        except AttributeError:
            if g_debug > 0: print "Warning - in read_lights - Adding 'Lighting' secyion"
            l_sect = ET.SubElement(self.m_root, 'Lighting')
            ET.SubElement(l_sect, 'Lights')
            ET.SubElement(l_sect, 'Controllers')
            ET.SubElement(l_sect, 'Buttons')
        # read the lights section
        try:
            l_list = l_sect.iterfind('Lights/Light')
        except AttributeError:
            if g_debug > 0: print "Warning - in getting a list of Lights"
            l_list = ET.SubElement(l_sect, 'Lights')
        for l_entry in l_list:
            l_obj = lighting.LightingData()
            self.read_light_common(l_entry, l_obj)
            Light_Data[l_obj.Key] = l_obj
            l_count += 1
        # Read the controllers section
        try:
            l_list = l_sect.iterfind('Controllers/Controller')
        except AttributeError:
            if g_debug > 0: print "-- Error in getting a list of Controllers"
            l_list = ET.SubElement(l_sect, 'Controllers')
        for l_entry in l_list:
            l_obj = lighting.ControllerData()
            self.read_light_common(l_entry, l_obj)
            l_obj.Interface = l_if = l_entry.findtext('Interface')
            l_obj.Port = l_entry.findtext('Port')
            if l_if == 'Serial':
                l_obj.BaudRate = self.get_int(l_entry, 'BaudRate')
                l_obj.ByteSize = self.get_int(l_entry, 'ByteSize')
                l_obj.DtsDtr = l_entry.findtext('DtsDtr')
                l_obj.InterCharTimeout = l_entry.findtext('InterCharTimeout')
                l_obj.Parity = l_entry.findtext('Parity')
                l_obj.RtsCts = l_entry.findtext('RtsCts')
                l_obj.StopBits = self.get_float(l_entry, 'StopBits')
                l_obj.Timeout = self.get_float(l_entry, 'Timeout')
                l_obj.WriteTimeout = self.get_float(l_entry, 'WriteTimeout')
                l_obj.XonXoff = l_entry.findtext('XonXoff')
                try:
                    l_obj.Product = int(l_entry.findtext('Product'), 0)
                    l_obj.Vendor = int(l_entry.findtext('Vendor'), 0)
                except TypeError:
                    l_obj.Product = 0
                    l_obj.Vendor = 0
            elif l_if == 'USB':
                try:
                    l_obj.Product = int(l_entry.findtext('Product'), 0)
                    l_obj.Vendor = int(l_entry.findtext('Vendor'), 0)
                except TypeError:
                    l_obj.Product = 0
                    l_obj.Vendor = 0
            elif l_if == 'Ethernet':
                pass
            Controller_Data[l_obj.Key] = l_obj
            l_count += 1
        # Read the button section
        try:
            l_list = l_sect.iterfind('Buttons/Button')
        except AttributeError:
            if g_debug > 0: print "-- Error in getting a list of Buttons"
            l_list = ET.SubElement(l_sect, 'Buttons')
        for l_entry in l_list:
            l_obj = lighting.ButtonData()
            self.read_light_common(l_entry, l_obj)
            Button_Data[l_obj.Key] = l_obj
            l_count += 1
        return l_count

    def read_schedules(self):
        l_count = 0
        try:
            l_sect = self.m_root.find('Schedules')
            l_list = l_sect.iterfind('Schedule')
        except AttributeError:
            if g_debug > 0: print "Warning - in read_Schedules - Adding 'Schedules'"
            l_sect = ET.SubElement(self.m_root, 'Schedules')
            l_list = l_sect.iterfind('Schedule')
        for l_entry in l_list:
            l_obj = schedule.ScheduleData()
            l_obj.Active = self.get_bool(l_entry.get('Active'))
            l_obj.HouseName = l_entry.findtext('HouseName')
            l_obj.Key = int(l_entry.get('Key'))
            l_obj.Level = int(l_entry.findtext('Level'))
            l_obj.LightName = l_entry.findtext('LightName')
            l_obj.Name = l_entry.get('Name')
            l_obj.Rate = int(l_entry.findtext('Rate'))
            l_obj.RoomName = l_entry.findtext('RoomName')
            l_obj.Time = l_entry.findtext('Time')
            l_obj.Type = l_entry.findtext('Type')
            Schedule_Data[l_obj.Key] = l_obj
            l_count += 1
        return l_count

    def read_log_web(self):
        if g_debug > 8:
            print "Debug - reading log_web"
            print xml_tools.prettify(self.m_root)
        try:
            l_sect = self.m_root.find('Logs')
            l_sect.find('Debug')
        except:
            if g_debug > 0: print "Warning - Logs section is missing - Adding empty values now."
            l_sect = ET.SubElement(self.m_root, 'Logs')
            ET.SubElement(l_sect, 'Debug').text = 'None'
            ET.SubElement(l_sect, 'Error').text = 'None'
        l_obj = log.LogData()
        l_obj.Debug = l_sect.findtext('Debug')
        l_obj.Error = l_sect.findtext('Error')
        Log_Data[0] = l_obj
        try:
            l_sect = self.m_root.find('Web')
            l_sect.find('WebPort')
        except:
            l_sect = ET.SubElement(self.m_root, 'Web')
            ET.SubElement(l_sect, 'WebPort').text = 'None'
        l_obj = web_server.WebData()
        l_obj.WebPort = l_sect.findtext('WebPort')
        Web_Data[0] = l_obj

    def read_upnp(self):
        pass

    def read_scenes(self):
        pass


class WriteConfig(ConfigTools):
    """Use the internal data to write an updated config file.

    This is called from the web interface or the GUI when the data has been changed.
    """

    m_filename = None
    m_root = None

    def __init__(self):
        global g_xmltree
        self.m_filename = xml_tools.open_config()
        try:
            g_xmltree = ET.parse(self.m_filename)
        except SyntaxError:
            xml_tools.ConfigFile().create_empty_config_file(self.m_filename)
            g_xmltree = ET.parse(self.m_filename)
        self.m_root = g_xmltree.getroot()

    def write_create_empty(self, p_name):
        l_sect = self.m_root.find(p_name)
        try:
            l_sect.clear()
        except AttributeError:
            if g_debug > 0: print "Creating a new sub-element named ", p_name
            l_sect = ET.SubElement(self.m_root, p_name)
        return l_sect

    def write_rooms(self, p_parent, p_name):
        for l_obj in Room_Data.itervalues():
            if l_obj.HouseName == p_name:
                l_entry = self.build_common(p_parent, 'Room', l_obj)
                ET.SubElement(l_entry, 'Comment').text = l_obj.Comment
                ET.SubElement(l_entry, 'Corner').text = l_obj.Corner
                ET.SubElement(l_entry, 'HouseName').text = p_name
                ET.SubElement(l_entry, 'Size').text = l_obj.Size
                self.m_room_count += 1

    def write_houses(self):
        """Replace the data in the 'Houses' section with the current data.
        """
        l_sect = self.write_create_empty('Houses')
        self.m_room_count = 0
        for l_obj in House_Data.itervalues():
            l_name = l_obj.Name
            l_house = self.build_common(l_sect, 'House', l_obj)
            l_entry = ET.SubElement(l_house, 'Location')
            ET.SubElement(l_entry, 'Street').text = l_obj.Street
            ET.SubElement(l_entry, 'City').text = l_obj.City
            ET.SubElement(l_entry, 'State').text = l_obj.State
            ET.SubElement(l_entry, 'ZipCode').text = l_obj.ZipCode
            ET.SubElement(l_entry, 'Phone').text = l_obj.Phone
            ET.SubElement(l_entry, 'Latitude').text = str(l_obj.Latitude)
            ET.SubElement(l_entry, 'Longitude').text = str(l_obj.Longitude)
            ET.SubElement(l_entry, 'TimeZone').text = str(l_obj.TimeZone)
            ET.SubElement(l_entry, 'SavingTime').text = str(l_obj.SavingTime)
            l_entry = ET.SubElement(l_house, 'Rooms')
            self.write_rooms(l_entry, l_name)
        self.write_file()

    def write_light_common(self, p_entry, p_obj):
        ET.SubElement(p_entry, 'Comment').text = str(p_obj.Comment)
        ET.SubElement(p_entry, 'Coords').text = str(p_obj.Coords)
        ET.SubElement(p_entry, 'Dimmable').text = self.put_bool(p_obj.Dimmable)
        ET.SubElement(p_entry, 'Family').text = p_obj.Family
        ET.SubElement(p_entry, 'House').text = p_obj.HouseName
        ET.SubElement(p_entry, 'Room').text = p_obj.RoomName
        ET.SubElement(p_entry, 'Type').text = p_obj.Type
        if p_obj.Family == 'Insteon':
            if g_debug > 2: print "WriteLightCommon Insteon=", p_obj
            ET.SubElement(p_entry, 'Address').text = p_obj.Address
            ET.SubElement(p_entry, 'Controller').text = self.put_bool(p_obj.Controller)
            ET.SubElement(p_entry, 'DevCat').text = str(p_obj.DevCat)
            ET.SubElement(p_entry, 'GroupList').text = str(p_obj.GroupList)
            ET.SubElement(p_entry, 'GroupNumber').text = str(p_obj.GroupNumber)
            ET.SubElement(p_entry, 'Master').text = str(p_obj.Master)
            ET.SubElement(p_entry, 'ProductKey').text = str(p_obj.ProductKey)
            ET.SubElement(p_entry, 'Responder').text = self.put_bool(p_obj.Responder)
        elif p_obj.Family == 'UPB':
            if g_debug > 2: print "WriteLightCommon UPB=", p_obj
            try:
                ET.SubElement(p_entry, 'NetworkID').text = self.put_str(p_obj.NetworkID)
                ET.SubElement(p_entry, 'Password').text = str(p_obj.Password)
                ET.SubElement(p_entry, 'UnitID').text = str(p_obj.UnitID)
            except AttributeError:
                pass

    def write_lights(self):
        l_sect = self.write_create_empty('Lighting')
        l_lgts = ET.SubElement(l_sect, 'Lights')
        l_ctls = ET.SubElement(l_sect, 'Controllers')
        l_btns = ET.SubElement(l_sect, 'Buttons')
        for l_obj in Light_Data.itervalues():
            l_entry = self.build_common(l_lgts, 'Light', l_obj)
            self.write_light_common(l_entry, l_obj)
        for l_obj in Button_Data.itervalues():
            l_entry = self.build_common(l_btns, 'Button', l_obj)
            self.write_light_common(l_entry, l_obj)
        for l_obj in Controller_Data.itervalues():
            l_entry = self.build_common(l_ctls, 'Controller', l_obj)
            self.write_light_common(l_entry, l_obj)
            ET.SubElement(l_entry, 'Interface').text = l_obj.Interface
            if l_obj.Interface == 'Serial':
                ET.SubElement(l_entry, 'Port').text = l_obj.Port
                ET.SubElement(l_entry, 'BaudRate').text = str(l_obj.BaudRate)
                ET.SubElement(l_entry, 'Parity').text = str(l_obj.Parity)
                ET.SubElement(l_entry, 'ByteSize').text = str(l_obj.ByteSize)
                ET.SubElement(l_entry, 'StopBits').text = str(l_obj.StopBits)
                ET.SubElement(l_entry, 'Timeout').text = str(l_obj.Timeout)
            elif l_obj.Interface == 'USB':
                ET.SubElement(l_entry, 'Vendor').text = str(l_obj.Vendor)
                ET.SubElement(l_entry, 'Product').text = str(l_obj.Product)
            elif l_obj.Interface == 'Ethernet':
                pass
        self.write_file()

    def write_schedules(self):
        """Replace all the data in the 'Schedules' section with the current data.
        """
        l_sect = self.write_create_empty('Schedules')
        for l_obj in Schedule_Data.itervalues():
            l_entry = self.build_common(l_sect, 'Schedule', l_obj)
            ET.SubElement(l_entry, 'HouseName').text = str(l_obj.HouseName)
            ET.SubElement(l_entry, 'Level').text = str(l_obj.Level)
            ET.SubElement(l_entry, 'LightName').text = l_obj.LightName
            ET.SubElement(l_entry, 'Rate').text = str(l_obj.Rate)
            ET.SubElement(l_entry, 'RoomName').text = str(l_obj.RoomName)
            ET.SubElement(l_entry, 'Time').text = l_obj.Time
            ET.SubElement(l_entry, 'Type').text = l_obj.Type
        self.write_file()
        schedule.Reload()

    def write_log_web(self):
        if g_debug > 2: print "Write log_web", Log_Data[0], vars(Log_Data[0])
        l_sect = self.write_create_empty('Logs')
        l_obj = Log_Data[0]
        # l_entry = self.build_common(l_sect, 'Log', l_obj)
        ET.SubElement(l_sect, 'Debug').text = str(l_obj.Debug)
        ET.SubElement(l_sect, 'Error').text = str(Log_Data[0].Error)
        l_sect = self.write_create_empty('Web')
        l_obj = Web_Data[0]
        ET.SubElement(l_sect, 'WebPort').text = str(Web_Data[0].WebPort)
        self.write_file()

    def write_upnp(self):
        self.write_file()

    def write_scenes(self):
        pass


def read_config():
    if g_debug > 0: print "read_config()"
    l_rf = ReadConfig()
    l_rf.read_houses()
    l_rf.read_lights()
    l_rf.read_schedules()
    l_rf.read_log_web()
    l_rf.read_upnp()
    l_rf.read_scenes()
    l_rf.write_file()

def write_config():
    if g_debug > 0: print "write_config()"
    l_wf = WriteConfig()
    l_wf.write_houses()
    l_wf.write_lights()
    l_wf.write_schedules()
    l_wf.write_log_web()
    l_wf.write_upnp()
    l_wf.write_scenes()

# ## END
