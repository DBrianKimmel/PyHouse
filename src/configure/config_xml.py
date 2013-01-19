#!/usr/bin/env python

"""
Notice that there  is no logging in this module.
The logging file location is read in as a part of the configuration.
All errors are printed out.
"""

# Import system type stuff
import xml.etree.ElementTree as ET

# Import PyMh files
import main.log as Log
import xml_tools
import main.house as House
from lighting import lighting
from schedule import schedule
from web import web_server

# Various data stores.
House_Data = House.House_Data
Log_Data = Log.Log_Data
Web_Data = web_server.Web_Data

# Various data definitions
HouseData = House.HouseData
LocationData = House.LocationData
RoomData = House.RoomData
LightData = lighting.LightData
ButtonData = lighting.ButtonData
ControllerData = lighting.ControllerData
ScheduleData = schedule.ScheduleData

g_debug = 2
g_xmltree = ''
g_logger = None

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

    def get_text(self, p_obj, p_name):
        l_var = p_obj.findtext(p_name)
        try:
            l_var = str(l_var)
        except (ValueError, TypeError):
            l_var = ''
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

    def read_common(self, p_obj, p_entry):
        # print "read_common() ", p_entry
        p_obj.Name = p_entry.get('Name')
        try:
            p_obj.Key = int(p_entry.get('Key'))
        except (AttributeError, TypeError):
            p_obj.Key = 0
        p_obj.Active = self.get_bool(p_entry.get('Active'))
        pass

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

    def read_schedules(self, p_entry, p_name = ''):
        l_count = 0
        l_dict = {}
        try:
            l_sect = p_entry.find('Schedules')
            l_list = l_sect.iterfind('Schedule')
        except AttributeError:
            print "Warning - in read_Schedules - No 'Schedules'"
            l_sect = ET.SubElement(p_entry, 'Schedules')
            l_list = l_sect.iterfind('Schedule')
        for l_entry in l_list:
            l_obj = ScheduleData()
            self.read_common(l_obj, l_entry)
            l_obj.HouseName = l_name = self.get_text(l_entry, 'HouseName')
            l_obj.Key = self.get_int(l_entry, 'Key')
            l_obj.Level = self.get_int(l_entry, 'Level')
            l_obj.LightName = self.get_text(l_entry, 'LightName')
            l_obj.Rate = self.get_int(l_entry, 'Rate')
            l_obj.RoomName = self.get_text(l_entry, 'RoomName')
            l_obj.Time = self.get_text(l_entry, 'Time')
            l_obj.Type = self.get_text(l_entry, 'Type')
            #
            if p_name != '':
                if l_name == p_name:
                    l_dict[l_count] = l_obj
                    l_count += 1
            else:
                l_dict[l_count] = l_obj
                l_count += 1
        if g_debug > 1:
            print "config_xml.read_schedule()  loaded {0:} scheds for {1:}".format(l_count, p_name)
        return l_dict

    def read_location(self, p_entry, p_name = ''):
        if g_debug > 7:
            print "config_xml.read_location()"
        l_dict = {}
        l_count = 0
        l_obj = LocationData()
        if g_debug > 4:
            print "config_xml.read_location() - Active=", l_obj.Active, l_obj.Name
        # Now read the location subsection
        l_entry = p_entry.find('Location')
        l_obj.Street = self.get_text(l_entry, 'Street')
        l_obj.City = self.get_text(l_entry, 'City')
        l_obj.State = self.get_text(l_entry, 'State')
        l_obj.ZipCode = self.get_text(l_entry, 'ZipCode')
        l_obj.Phone = self.get_text(l_entry, 'Phone')
        l_obj.Latitude = self.get_float(l_entry, 'Latitude')
        l_obj.Longitude = self.get_float(l_entry, 'Longitude')
        l_obj.TimeZone = self.get_float(l_entry, 'TimeZone')
        l_obj.SavingTime = self.get_float(l_entry, 'SavingTime')
        l_dict[l_count] = l_obj
        l_count += 1
        if g_debug > 1:
            print "config_xml.read_location()  loaded {0:} locations for {1:}".format(l_count, p_name)
        return l_dict

    def read_rooms(self, p_entry, p_house):
        if g_debug > 7:
            print "config_xml.read_rooms()"
        l_dict = {}
        l_count = 0
        l_rooms = p_entry.find('Rooms')
        l_list = l_rooms.iterfind('Room')
        for l_entry in l_list:
            l_obj = RoomData()
            self.read_common(l_obj, l_entry)
            l_obj.HouseName = p_house
            l_obj.Comment = self.get_text(l_entry, 'Comment')
            l_obj.Corner = l_entry.findtext('Corner')
            l_obj.HouseName = l_entry.findtext('HouseName')
            l_obj.Size = l_entry.findtext('Size')
            l_dict[l_count] = l_obj
            l_count += 1
            if g_debug > 4:
                print "config_xml.read_rooms() - Active=", l_obj.Active, l_obj.Name
        if g_debug > 2:
            print "config_xml.read_rooms()  loaded {0:} rooms".format(l_count)
        return l_dict

    def read_light_common(self, p_entry, p_obj):
        self.read_common(p_obj, p_entry)
        p_obj.Comment = self.get_text(p_entry, 'Comment')
        p_obj.Coords = self.get_text(p_entry, 'Coords')
        p_obj.Dimmable = self.get_bool(p_entry.findtext('Dimmable'))
        p_obj.Family = l_fam = self.get_text(p_entry, 'Family')
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
        if g_debug > 7:
            print "yyy-common ", p_obj
        return p_obj

    def read_buttons(self, p_entry, p_house = ''):
        if g_debug > 7:
            print "config_xml.read_buttons()"
        l_count = 0
        l_dict = {}
        l_sect = p_entry.find('Buttons')
        l_list = l_sect.iterfind('Button')
        for l_entry in l_list:
            l_obj = ButtonData()
            l_obj = self.read_light_common(l_entry, l_obj)
            if p_house != '':
                if l_obj.HouseName == p_house:
                    l_dict[l_count] = l_obj
                    l_count += 1
            else:
                l_dict[l_count] = l_obj
                l_count += 1
        if g_debug > 1:
            print "config_xml.read_buttons()  loaded {0:} buttons for house {1:}".format(l_count, p_house)
        return l_dict

    def read_controllers(self, p_entry, p_house = ''):
        if g_debug > 7:
            print "config_xml.read_controllers()"
        l_count = 0
        l_dict = {}
        l_sect = p_entry.find('Controllers')
        l_list = l_sect.iterfind('Controller')
        for l_entry in l_list:
            l_obj = lighting.ControllerData()
            l_obj = self.read_light_common(l_entry, l_obj)
            l_obj.Interface = l_if = self.get_text(l_entry, 'Interface')
            l_obj.Port = self.get_text(l_entry, 'Port')
            if l_if == 'Serial':
                l_obj.BaudRate = self.get_int(l_entry, 'BaudRate')
                l_obj.ByteSize = self.get_int(l_entry, 'ByteSize')
                l_obj.DtsDtr = self.get_text(l_entry, 'DtsDtr')
                l_obj.InterCharTimeout = self.get_float(l_entry, 'InterCharTimeout')
                l_obj.Parity = self.get_text(l_entry, 'Parity')
                l_obj.RtsCts = self.get_text(l_entry, 'RtsCts')
                l_obj.StopBits = self.get_float(l_entry, 'StopBits')
                l_obj.Timeout = self.get_float(l_entry, 'Timeout')
                l_obj.WriteTimeout = self.get_float(l_entry, 'WriteTimeout')
                l_obj.XonXoff = self.get_text(l_entry, 'XonXoff')
                l_obj.Product = self.get_int(l_entry, 'Product')
                l_obj.Vendor = self.get_int(l_entry, 'Vendor')
            elif l_if == 'USB':
                l_obj.Product = self.get_int(l_entry, 'Product')
                l_obj.Vendor = self.get_int(l_entry, 'Vendor')
            elif l_if == 'Ethernet':
                pass
            if p_house != '':
                if l_obj.HouseName == p_house:
                    l_dict[l_count] = l_obj
                    l_count += 1
            else:
                l_dict[l_count] = l_obj
                l_count += 1
        if g_debug > 1:
            print "config_xml.read_controllers()  loaded {0:} controllers for house {1:}".format(l_count, p_house)
        return l_dict

    def read_lights(self, p_entry, p_house = ''):
        if g_debug > 7:
            print "config_xml.read_lights()"
        l_count = 0
        l_dict = {}
        l_sect = p_entry.find('Lights')
        l_list = l_sect.iterfind('Light')
        for l_entry in l_list:
            l_obj = lighting.LightData()
            l_obj = self.read_light_common(l_entry, l_obj)
            if p_house != '':
                if l_obj.HouseName == p_house:
                    l_dict[l_count] = l_obj
                    l_count += 1
            else:
                l_dict[l_count] = l_obj
                l_count += 1
        if g_debug > 1:
            print "config_xml.read_lights()  loaded {0:} lights for house {1:}".format(l_count, p_house)
        return l_dict

    def read_houses(self):
        """Read house information, location and rooms.

        The main data is House_Data - one dict entry for each house.
        """
        l_count = 0
        try:
            l_sect = self.m_root.find('Houses')
            l_list = l_sect.iterfind('House')  # use l_sect to force error if it is missing
        except AttributeError:
            print "Warning - in read_house - Adding 'Houses' section"
            l_sect = ET.SubElement(self.m_root, 'Houses')
            l_list = l_sect.iterfind('House')
        for l_house in l_list:
            l_obj = HouseData()
            self.read_common(l_obj, l_house)
            l_name = l_obj.Name
            l_obj.Key = l_count
            l_obj.Location = self.read_location(l_house)
            l_obj.Rooms = self.read_rooms(l_house, l_name)
            l_obj.Schedule = self.read_schedules(l_house, l_name)
            l_obj.Buttons = self.read_buttons(l_house, l_name)
            l_obj.Controllers = self.read_controllers(l_house, l_name)
            l_obj.Lights = self.read_lights(l_house, l_name)
            House_Data[l_count] = l_obj
            l_count += 1
        if g_debug > 1:
            print "config_xml.read_houses() loaded {0:} houses.".format(l_count)
        return House_Data

    def read_log_web(self):
        if g_debug > 8:
            print "Debug - reading log_web"
            print xml_tools.prettify(self.m_root)
        try:
            l_sect = self.m_root.find('Logs')
            l_sect.find('Debug')
        except:
            print "Warning - Logs section is missing - Adding empty values now."
            l_sect = ET.SubElement(self.m_root, 'Logs')
            ET.SubElement(l_sect, 'Debug').text = 'None'
            ET.SubElement(l_sect, 'Error').text = 'None'
        l_obj = Log.LogData()
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
        """Create an empty XML section to be filled in.

        @param p_name: is the name of the xml section to be written.
        @return: the e-tree section to be used.
        """
        l_sect = self.m_root.find(p_name)
        try:
            l_sect.clear()
        except AttributeError:
            print "Creating a new sub-element named ", p_name
            l_sect = ET.SubElement(self.m_root, p_name)
        return l_sect

    def write_light_common(self, p_entry, p_obj):
        ET.SubElement(p_entry, 'Comment').text = str(p_obj.Comment)
        ET.SubElement(p_entry, 'Coords').text = str(p_obj.Coords)
        ET.SubElement(p_entry, 'Dimmable').text = self.put_bool(p_obj.Dimmable)
        ET.SubElement(p_entry, 'Family').text = p_obj.Family
        ET.SubElement(p_entry, 'House').text = p_obj.HouseName
        ET.SubElement(p_entry, 'Room').text = p_obj.RoomName
        ET.SubElement(p_entry, 'Type').text = p_obj.Type
        if p_obj.Family == 'Insteon':
            if g_debug > 4:
                print "WriteLightCommon Insteon=", p_obj
            ET.SubElement(p_entry, 'Address').text = p_obj.Address
            ET.SubElement(p_entry, 'Controller').text = self.put_bool(p_obj.Controller)
            ET.SubElement(p_entry, 'DevCat').text = str(p_obj.DevCat)
            ET.SubElement(p_entry, 'GroupList').text = str(p_obj.GroupList)
            ET.SubElement(p_entry, 'GroupNumber').text = str(p_obj.GroupNumber)
            ET.SubElement(p_entry, 'Master').text = str(p_obj.Master)
            ET.SubElement(p_entry, 'ProductKey').text = str(p_obj.ProductKey)
            ET.SubElement(p_entry, 'Responder').text = self.put_bool(p_obj.Responder)
        elif p_obj.Family == 'UPB':
            if g_debug > 4:
                print "WriteLightCommon UPB=", p_obj
            try:
                ET.SubElement(p_entry, 'NetworkID').text = self.put_str(p_obj.NetworkID)
                ET.SubElement(p_entry, 'Password').text = str(p_obj.Password)
                ET.SubElement(p_entry, 'UnitID').text = str(p_obj.UnitID)
            except AttributeError:
                pass

    def write_buttons(self, p_parent, p_dict):
        l_count = 0
        l_sect = ET.SubElement(p_parent, 'Buttons')
        for l_obj in p_dict.itervalues():
            l_entry = self.build_common(l_sect, 'Button', l_obj)
            self.write_light_common(l_entry, l_obj)
            l_count += 1
        if g_debug > 1:
            print "config_xml.write_buttons() - Wrote {0:} buttons".format(l_count)

    def write_controllers(self, p_parent, p_dict):
        l_count = 0
        l_sect = ET.SubElement(p_parent, 'Controllers')
        for l_obj in p_dict.itervalues():
            l_entry = self.build_common(l_sect, 'Controller', l_obj)
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
            l_count += 1
        if g_debug > 1:
            print "config_xml.write_controllers() - Wrote {0:} controllers".format(l_count)

    def write_lights(self, p_parent, p_dict):
        l_count = 0
        l_sect = ET.SubElement(p_parent, 'Lights')
        for l_obj in p_dict.itervalues():
            l_entry = self.build_common(l_sect, 'Light', l_obj)
            self.write_light_common(l_entry, l_obj)
            l_count += 1
        if g_debug > 1:
            print "config_xml.write_lights() - Wrote {0:} lights".format(l_count)

    def write_schedules(self, p_parent, p_dict):
        """Replace all the data in the 'Schedules' section with the current data.
        """
        l_count = 0
        l_sect = ET.SubElement(p_parent, 'Schedules')
        for l_obj in p_dict.itervalues():
            l_entry = ET.SubElement(l_sect, 'Schedule')
            ET.SubElement(l_entry, 'HouseName').text = str(l_obj.HouseName)
            ET.SubElement(l_entry, 'Level').text = str(l_obj.Level)
            ET.SubElement(l_entry, 'LightName').text = l_obj.LightName
            ET.SubElement(l_entry, 'Rate').text = str(l_obj.Rate)
            ET.SubElement(l_entry, 'RoomName').text = str(l_obj.RoomName)
            ET.SubElement(l_entry, 'Time').text = l_obj.Time
            ET.SubElement(l_entry, 'Type').text = l_obj.Type
            l_count += 1
        if g_debug > 1:
            print "config_xml.write_schedules() - Wrote {0:} schedules".format(l_count)

    def write_location(self, p_parent, p_dict):
        """Replace the data in the 'House/Location' section with the current data.
        """
        l_count = 0
        for l_obj in p_dict.itervalues():
            l_entry = ET.SubElement(p_parent, 'Location')
            ET.SubElement(l_entry, 'Street').text = l_obj.Street
            ET.SubElement(l_entry, 'City').text = l_obj.City
            ET.SubElement(l_entry, 'State').text = l_obj.State
            ET.SubElement(l_entry, 'ZipCode').text = l_obj.ZipCode
            ET.SubElement(l_entry, 'Phone').text = l_obj.Phone
            ET.SubElement(l_entry, 'Latitude').text = str(l_obj.Latitude)
            ET.SubElement(l_entry, 'Longitude').text = str(l_obj.Longitude)
            ET.SubElement(l_entry, 'TimeZone').text = str(l_obj.TimeZone)
            ET.SubElement(l_entry, 'SavingTime').text = str(l_obj.SavingTime)
            l_count += 1
        if g_debug > 1:
            print "config_xml.write_location() - Wrote {0:} locations".format(l_count)

    def write_rooms(self, p_parent, p_dict):
        l_count = 0
        l_sect = ET.SubElement(p_parent, 'Rooms')
        for l_obj in p_dict.itervalues():
            l_entry = self.build_common(l_sect, 'Room', l_obj)
            ET.SubElement(l_entry, 'Comment').text = l_obj.Comment
            ET.SubElement(l_entry, 'Corner').text = l_obj.Corner
            ET.SubElement(l_entry, 'HouseName').text = l_obj.HouseName
            ET.SubElement(l_entry, 'Size').text = l_obj.Size
            l_count += 1
        if g_debug > 1:
            print "config_xml.write_rooms() - Wrote {0:} rooms".format(l_count)

    def write_houses(self):
        """Replace the data in the 'Houses' section with the current data.
        """
        l_count = 0
        l_sect = self.write_create_empty('Houses')
        for l_obj in House_Data.itervalues():
            l_house = self.build_common(l_sect, 'House', l_obj)
            self.write_location(l_house, l_obj.Location)
            self.write_rooms(l_house, l_obj.Rooms)
            self.write_buttons(l_house, l_obj.Buttons)
            self.write_controllers(l_house, l_obj.Controllers)
            self.write_lights(l_house, l_obj.Lights)
            self.write_schedules(l_house, l_obj.Schedule)
            if g_debug > 2:
                print "config_xml.write_house() - Name:{0:}, Key:{1:}".format(l_obj.Name, l_obj.Key)
            l_count += 1
        if g_debug > 1:
            print "config_xml.write_house() - Wrote {0:} houses".format(l_count)
        self.write_file()

    def write_log_web(self):
        if g_debug > 1:
            print "Write log_web", Log_Data[0], vars(Log_Data[0])
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
        self.write_file()


class API(ReadConfig, WriteConfig):

    def __init__(self, p_file):
        pass

    def read_config(self):
        if g_debug > 0:
            print "config_xml.read_config()"
        l_rf = ReadConfig()
        l_rf.read_houses()
        l_rf.read_log_web()
        l_rf.read_upnp()
        l_rf.read_scenes()
        l_rf.write_file()

    def write_config(self):
        if g_debug > 0:
            print "config_xml.write_config()"
        l_wf = WriteConfig()
        l_wf.write_houses()
        l_wf.write_log_web()
        l_wf.write_upnp()
        l_wf.write_scenes()
        l_wf.write_file()

# ## END
