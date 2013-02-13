#!/usr/bin/python

"""Handle all the house(s) information.

main/houses.py

This module is a singleton called from PyHouse.
Its main purpose is to initiate the configuration system and then call
the other packages and set up the whole system based on the config read in.


Rooms and lights and HVAC are associated with a particular house.
"""

# Import system type stuff
import logging
import xml.etree.ElementTree as ET

# Import PyMh files
from house import house
from schedule import schedule
from configure import xml_tools
from lighting import lighting_tools
from lighting import lighting
from main import internet
from main import weather
# from configure.config_xml import g_xmltree

g_debug = 0
m_logger = None

Singletons = {}
House_Data = {}
Houses_Data = {}
HouseCount = 0
LocationCount = 0
RoomCount = 0

# object definitions
ButtonData = lighting.ButtonData
LightData = lighting.LightData
ControllerData = lighting.ControllerData


class HousesData(object):
    """This class holds
    """

    def __init__(self):
        self.HouseAPI = None
        self.ScheduleAPI = None
        self.Object = {}


class HouseData(object):

    def __init__(self):
        global HouseCount
        HouseCount += 1
        self.Active = False
        self.Key = 0
        self.Name = None
        self.Buttons = {}
        self.Controllers = {}
        self.Lights = {}
        self.Location = {}
        self.Rooms = {}
        self.Schedule = {}

    def __str__(self):
        l_ret = ' House:: Name :{0:}, Active:{1:}, Key:{2:}'.format(self.Name, self.Active, self.Key)
        return l_ret


class LocationData(lighting_tools.CoreData, HousesData, HouseData):

    def __init__(self):
        global LocationCount
        LocationCount += 1
        self.Active = True
        self.City = None
        self.Key = 0
        self.Latitude = 0.0
        self.Longitude = 0.0
        self.Name = None
        self.Phone = None
        self.SavingTime = 0.0
        self.State = None
        self.Street = None
        self.TimeZone = 0.0
        self.ZipCode = None

    def __str__(self):
        l_ret = ' Location:: Lat:{0:}, Lon:{1:}'.format(self.Latitude, self.Longitude)
        return l_ret

    def get_active(self):
        return self.__Active
    def get_city(self):
        return self.__City
    def get_latitude(self):
        return self.__Latitude
    def get_longitude(self):
        return self.__Longitude
    def get_name(self):
        return self.__Name
    def get_phone(self):
        return self.__Phone
    def get_saving_time(self):
        return self.__SavingTime
    def get_state(self):
        return self.__State
    def get_street(self):
        return self.__Street
    def get_time_zone(self):
        return self.__TimeZone
    def get_zip_code(self):
        return self.__ZipCode

    def set_active(self, value):
        self.__Active = value
    def set_city(self, value):
        self.__City = value
    def set_latitude(self, value):
        self.__Latitude = value
    def set_longitude(self, value):
        self.__Longitude = value
    def set_name(self, value):
        self.__Name = value
    def set_phone(self, value):
        self.__Phone = value
    def set_saving_time(self, value):
        self.__SavingTime = value
    def set_state(self, value):
        self.__State = value
    def set_street(self, value):
        self.__Street = value
    def set_time_zone(self, value):
        self.__TimeZone = value
    def set_zip_code(self, value):
        self.__ZipCode = value

    Active = property(get_active, set_active, None, None)
    City = property(get_city, set_city, None, None)
    Latitude = property(get_latitude, set_latitude, None, None)
    Longitude = property(get_longitude, set_longitude, None, None)
    Name = property(get_name, set_name, None, None)
    Phone = property(get_phone, set_phone, None, None)
    SavingTime = property(get_saving_time, set_saving_time, None, "Minutes offset from standard time Eastern is +60")
    State = property(get_state, set_state, None, None)
    Street = property(get_street, set_street, None, None)
    TimeZone = property(get_time_zone, set_time_zone, None, None)
    ZipCode = property(get_zip_code, set_zip_code, None, None)


class RoomData(LocationData):

    def __init__(self):
        global RoomCount
        RoomCount += 1
        self.Active = False
        self.Comment = None
        self.Corner = None
        self.HouseName = None
        self.Key = 0
        self.Name = None
        self.Size = None

    def __str__(self):
        l_ret = ' Room:: Name:{0:} \t Size:{1:} \t Corner:{2:}\n'.format(self.get_name(), self.get_size(), self.get_corner())
        return l_ret

    def get_active(self):
        return self.__Active
    def get_comment(self):
        return self.__Comment
    def get_corner(self):
        return self.__Corner
    def get_house_name(self):
        return self.__HouseName
    def get_name(self):
        return self.__Name
    def get_size(self):
        return self.__Size
    def set_active(self, value):
        self.__Active = value
    def set_comment(self, value):
        self.__Comment = value
    def set_corner(self, value):
        self.__Corner = value
    def set_house_name(self, value):
        self.__HouseName = value
    def set_name(self, value):
        self.__Name = value
    def set_size(self, value):
        self.__Size = value

    Active = property(get_active, set_active, None, None)
    Comment = property(get_comment, set_comment, None, None)
    Corner = property(get_corner, set_corner, None, None)
    HouseName = property(get_house_name, set_house_name, None, None)
    Name = property(get_name, set_name, None, None)
    Size = property(get_size, set_size, None, None)


class HouseReadConfig(xml_tools.ConfigTools):

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

    def read_location(self, p_entry, p_name = ''):
        if g_debug > 7:
            print "house.read_location()"
        l_dict = {}
        l_count = 0
        l_obj = LocationData()
        if g_debug > 4:
            print "houses.read_location() - Active=", l_obj.Active, l_obj.Name
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
        if g_debug > 4:
            print "houses.read_location()  loaded {0:} locations for {1:}".format(l_count, p_name)
        return l_dict

    def read_rooms(self, p_entry, p_house):
        if g_debug > 7:
            print "houses.read_rooms()"
        l_dict = {}
        l_count = 0
        l_rooms = p_entry.find('Rooms')
        l_list = l_rooms.iterfind('Room')
        for l_entry in l_list:
            l_obj = RoomData()
            self.read_common(l_obj, l_entry)
            l_obj.Key = l_count
            l_obj.HouseName = p_house
            l_obj.Comment = self.get_text(l_entry, 'Comment')
            l_obj.Corner = l_entry.findtext('Corner')
            l_obj.HouseName = l_entry.findtext('HouseName')
            l_obj.Size = l_entry.findtext('Size')
            l_dict[l_count] = l_obj
            l_count += 1
            if g_debug > 4:
                print "houses.read_rooms()   Name:{0:}, Active:{1:}, Key:{2:}".format(l_obj.Name, l_obj.Active, l_obj.Key)
        if g_debug > 4:
            print "houses.read_rooms()  loaded {0:} rooms".format(l_count)
        return l_dict

    def read_light_common(self, p_entry, p_obj):
        """
        @param p_entry: is the e-tree XML house object
        @param p_house: is the text name of the House.
        @return: a dict of the entry to be attached to a house object.
        TODO: move some of lights to lighting or lighting_xxx and family stuff to Device_<family> called from lighting.
        """
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

    def read_buttons(self, p_entry, p_house):
        """
        """
        if g_debug > 7:
            print "houses.read_buttons()"
        l_count = 0
        l_dict = {}
        l_sect = p_entry.find('Buttons')
        l_list = l_sect.iterfind('Button')
        for l_entry in l_list:
            l_obj = ButtonData()
            l_obj = self.read_light_common(l_entry, l_obj)
            # l_obj.Key = l_count
            l_dict[l_count] = l_obj
            l_count += 1
        if g_debug > 4:
            print "houses.read_buttons()  loaded {0:} buttons for house {1:}".format(l_count, p_house)
        return l_dict

    def read_controllers(self, p_entry, p_house = ''):
        if g_debug > 7:
            print "houses.read_controllers()"
        l_count = 0
        l_dict = {}
        l_sect = p_entry.find('Controllers')
        l_list = l_sect.iterfind('Controller')
        for l_entry in l_list:
            l_obj = ControllerData()
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
            # l_obj.Key = l_count
            l_dict[l_count] = l_obj
            l_count += 1
        if g_debug > 4:
            print "houses.read_controllers()  loaded {0:} controllers for house {1:}".format(l_count, p_house)
        return l_dict

    def read_lights(self, p_entry, p_house = ''):
        if g_debug > 7:
            print "houses.read_lights()"
        l_count = 0
        l_dict = {}
        l_sect = p_entry.find('Lights')
        l_list = l_sect.iterfind('Light')
        for l_entry in l_list:
            l_obj = LightData()
            l_obj = self.read_light_common(l_entry, l_obj)
            # l_obj.Key = l_count
            l_dict[l_count] = l_obj
            l_count += 1
        if g_debug > 4:
            print "houses.read_lights()  loaded {0:} lights for house {1:}".format(l_count, p_house)
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
            if g_debug > 1:
                print "houses.read_house() - Loading XML data for House:{0:}".format(l_obj.Name), l_obj
            l_obj.Location = self.read_location(l_house, l_name)
            l_obj.Rooms = self.read_rooms(l_house, l_name)
            l_obj.Buttons = self.read_buttons(l_house, l_name)
            l_obj.Controllers = self.read_controllers(l_house, l_name)
            l_obj.Lights = self.read_lights(l_house, l_name)
            l_obj.Schedule = schedule.API().read_schedules(l_house, l_name)
            House_Data[l_count] = l_obj
            l_count += 1
        if g_debug > 2:
            print "houses.read_houses() loaded {0:} houses.".format(l_count)
        return House_Data


class HouseWriteConfig(xml_tools.ConfigTools):
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
        if g_debug > 4:
            print "houses.write_buttons() - Wrote {0:} buttons".format(l_count)

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
        if g_debug > 4:
            print "houses.write_controllers() - Wrote {0:} controllers".format(l_count)

    def write_lights(self, p_parent, p_dict):
        l_count = 0
        l_sect = ET.SubElement(p_parent, 'Lights')
        for l_obj in p_dict.itervalues():
            l_entry = self.build_common(l_sect, 'Light', l_obj)
            self.write_light_common(l_entry, l_obj)
            l_count += 1
        if g_debug > 4:
            print "houses.write_lights() - Wrote {0:} lights".format(l_count)

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
        if g_debug > 4:
            print "houses.write_location() - Wrote {0:} locations".format(l_count)

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
        if g_debug > 4:
            print "houses.write_rooms() - Wrote {0:} rooms".format(l_count)

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
            schedule.API().write_schedules(l_house, l_obj.Schedule)
            if g_debug > 2:
                print "houses.write_house() - Name:{0:}, Key:{1:}".format(l_obj.Name, l_obj.Key)
            l_count += 1
        if g_debug > 2:
            print "houses.write_house() - Wrote {0:} houses".format(l_count)
        self.write_file(g_xmltree, self.m_filename)


class HouseAPI(lighting_tools.CoreAPI, HouseReadConfig, HouseWriteConfig, RoomData):
    """
    """

    def load_all_houses(self):
        """Load all the house info.
        """
        if g_debug > 1:
            print "houses.load_all_houses()"
        global House_Data
        l_hrc = HouseReadConfig()
        House_Data = l_hrc.read_houses()
        if g_debug > 8:
            print "*** House ****"
            for l_obj in House_Data.itervalues():
                self.dump_device(l_obj, 'House')

    def _save_all_houses(self):
        if g_debug > 1:
            print "houses._save_all_houses()"
        l_hwc = HouseWriteConfig()
        l_hwc.write_houses()


class API(HouseAPI):
    """
    """

    m_schedules = []

    def __new__(cls, *args, **kwargs):
        """This is for all houses.
        Set up the common / global things in this singleton.
        """
        if cls in Singletons:
            return Singletons[cls]
        if g_debug > 0:
            print "houses.__new__()"
        self = object.__new__(cls)
        cls.__init__(self, *args, **kwargs)
        Singletons[cls] = self
        #
        self.m_logger = logging.getLogger('PyHouse.Houses')
        self.m_logger.info("Initializing all houses.")
        internet.Init()
        weather.Init()
        self.m_logger.info("Initialized.")
        if g_debug > 0:
            print "houses.__new__() all houses initialized now."
        #
        return self

    def __init__(self):
        if g_debug > 0:
            print "houses.__init__()", House_Data
            print

    def Start(self):
        """Start processing for all things house.
        May be stopped and then started anew to force reloading info.
        Invoked once no matter how many houses defined.
        """
        if g_debug > 0:
            print "houses.API.Start() Singleton"
        self.m_logger.info("Starting.")
        self.load_all_houses()
        #
        l_count = 0
        for l_house_obj in House_Data.itervalues():
            if g_debug > 1:
                print "houses.API.Start() - begin setting up for House:{0:}, Active:{1:}".format(l_house_obj.Name, l_house_obj.Active)
            l_obj = Houses_Data[l_count] = HousesData()
            l_obj.HouseAPI = house.API()
            l_obj.Object = l_house_obj
            l_obj.ScheduleAPI = schedule.API()
            Houses_Data[l_count] = l_obj
            if l_house_obj.Active:
                l_obj.HouseAPI.Start(l_house_obj)
                # l_obj.ScheduleAPI.Start(l_house_obj)
            l_count += 1
        #
        if g_debug > 0:
            print "houses.API.Start() Houses all started."
        internet.Start()
        weather.Start()
        self.m_logger.info("Started.")


    def Stop(self):
        if g_debug > 0:
            print "houses.API.Stop()"
        self.m_logger.info("Stopping.")
        self.save_all_houses()
        #
        for l_sch in self.m_schedules:
            l_sch.Stop()
        internet.Stop()
        weather.Stop()
        self.m_logger.info("Stopped.")

    def save_all_houses(self):
        """
        """
        if g_debug > 0:
            print "houses.API.save_all_houses()"
        self._save_all_houses()

# ##  END
