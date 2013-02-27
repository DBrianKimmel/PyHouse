#!/usr/bin/python

"""Handle all the house(s) information.

main/house.py

There is one instance of this module for each house being controlled.



There is location information for the house.  This is for calculating the
time of sunrise and sunset.  Additional calculations may be added such as
moonrise, tides, etc.

There is one instance of this (Singleton).

Rooms and lights and HVAC are associated with a particular house.
"""

# Import system type stuff
import logging
import xml.etree.ElementTree as ET

# Import PyMh files
from schedule import schedule
from lighting import lighting
from configure import xml_tools

g_debug = 3
m_logger = None

Singletons = {}
House_Data = {}
HouseCount = 0
LocationCount = 0
RoomCount = 0

# object definitions
ButtonData = lighting.ButtonData
LightData = lighting.LightData
ControllerData = lighting.ControllerData
ScheduleData = schedule.ScheduleData


class HouseData(object):

    def __init__(self):
        global HouseCount
        HouseCount += 1
        self.Active = False
        self.Key = 0
        self.Name = None
        self.Buttons = {}
        self.Controllers = {}
        self.LightingAPI = None
        self.Lights = {}
        self.Location = {}
        self.Rooms = {}
        self.Schedule = {}
        self.ScheduleAPI = None

    def __str__(self):
        l_ret = ' House:: Name :{0:}, Active:{1:}, Key:{2:}, LightingAPI:{3:}'.format(self.Name, self.Active, self.Key, self.LightingAPI)
        return l_ret


class LocationData(HouseData):

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


class HouseReadWriteConfig(xml_tools.ConfigTools):
    """Use the internal data to read / write an updated config file.

    This is called from the web interface or the GUI when the data has been changed.
    """

    def read_location(self, p_entry, p_name = ''):
        if g_debug > 7:
            print "house.read_location()"
        l_dict = {}
        l_count = 0
        l_location_obj = LocationData()
        if g_debug > 4:
            print "house.read_location() - Active=", l_location_obj.Active, l_location_obj.Name
        # Now read the location subsection
        l_entry = p_entry.find('Location')
        l_location_obj.Street = self.get_text(l_entry, 'Street')
        l_location_obj.City = self.get_text(l_entry, 'City')
        l_location_obj.State = self.get_text(l_entry, 'State')
        l_location_obj.ZipCode = self.get_text(l_entry, 'ZipCode')
        l_location_obj.Phone = self.get_text(l_entry, 'Phone')
        l_location_obj.Latitude = self.get_float(l_entry, 'Latitude')
        l_location_obj.Longitude = self.get_float(l_entry, 'Longitude')
        l_location_obj.TimeZone = self.get_float(l_entry, 'TimeZone')
        l_location_obj.SavingTime = self.get_float(l_entry, 'SavingTime')
        l_dict[l_count] = l_location_obj
        l_count += 1
        if g_debug > 4:
            print "house.read_location()  loaded {0:} locations for {1:}".format(l_count, p_name)
        return l_dict

    def read_rooms(self, p_entry, p_house):
        if g_debug > 7:
            print "house.read_rooms()"
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
                print "house.read_rooms()   Name:{0:}, Active:{1:}, Key:{2:}".format(l_obj.Name, l_obj.Active, l_obj.Key)
        if g_debug > 4:
            print "house.read_rooms()  loaded {0:} rooms".format(l_count)
        return l_dict

    def read_house(self, p_house_obj, p_house_xml):
        """Read house information, location and rooms.

        The main data is House_Data.
        """
        l_count = 0
        l_obj = p_house_obj
        self.read_common(l_obj, p_house_xml)
        l_name = l_obj.Name
        # l_obj.Key = l_count
        if g_debug > 1:
            print "house.read_house() - Loading XML data for House:{0:}".format(l_obj.Name), l_obj
        l_obj.Location = self.read_location(p_house_xml, l_name)
        l_obj.Rooms = self.read_rooms(p_house_xml, l_name)
        House_Data[l_count] = l_obj
        l_count += 1
        if g_debug > 2:
            print "house.read_house() loaded {0:} houses.".format(l_count), l_obj
        return House_Data

    def write_location(self, p_parent_xml, p_dict):
        """Replace the data in the 'House/Location' section with the current data.
        """
        l_count = 0
        for l_location_obj in p_dict.itervalues():
            l_entry = ET.SubElement(p_parent_xml, 'Location')
            ET.SubElement(l_entry, 'Street').text = l_location_obj.Street
            ET.SubElement(l_entry, 'City').text = l_location_obj.City
            ET.SubElement(l_entry, 'State').text = l_location_obj.State
            ET.SubElement(l_entry, 'ZipCode').text = l_location_obj.ZipCode
            ET.SubElement(l_entry, 'Phone').text = l_location_obj.Phone
            ET.SubElement(l_entry, 'Latitude').text = str(l_location_obj.Latitude)
            ET.SubElement(l_entry, 'Longitude').text = str(l_location_obj.Longitude)
            ET.SubElement(l_entry, 'TimeZone').text = str(l_location_obj.TimeZone)
            ET.SubElement(l_entry, 'SavingTime').text = str(l_location_obj.SavingTime)
            l_count += 1
        if g_debug > 2:
            print "house.write_location() - Wrote {0:} locations".format(l_count)

    def write_rooms(self, p_parent_xml, p_dict):
        l_count = 0
        l_sect = ET.SubElement(p_parent_xml, 'Rooms')
        for l_room_obj in p_dict.itervalues():
            l_entry = self.build_common(l_sect, 'Room', l_room_obj)
            ET.SubElement(l_entry, 'Comment').text = l_room_obj.Comment
            ET.SubElement(l_entry, 'Corner').text = l_room_obj.Corner
            ET.SubElement(l_entry, 'HouseName').text = l_room_obj.HouseName
            ET.SubElement(l_entry, 'Size').text = l_room_obj.Size
            l_count += 1
        if g_debug > 2:
            print "house.write_rooms() - Wrote {0:} rooms".format(l_count)

    def write_house(self, p_parent_xml, p_house_obj):
        """Replace the data in the 'Houses' section with the current data.
        """
        p_parent_xml.set('Name', p_house_obj.Name)
        p_parent_xml.set('Key', str(p_house_obj.Key))
        p_parent_xml.set('Active', self.put_bool(p_house_obj.Active))
        self.write_location(p_parent_xml, p_house_obj.Location)
        self.write_rooms(p_parent_xml, p_house_obj.Rooms)
        if g_debug > 2:
            print "house.write_house() - Name:{0:}, Key:{1:}".format(p_house_obj.Name, p_house_obj.Key)
        return p_parent_xml


class LoadSaveAPI(RoomData, HouseReadWriteConfig):
    """
    """


class API(LoadSaveAPI):
    """
    """

    m_schedule = None
    m_house_obj = None

    def __init__(self):
        if g_debug > 0:
            print "house.__init__()"
        self.m_logger = logging.getLogger('PyHouse.House')

    def Start(self, p_houses_obj, p_house_xml):
        """Start processing for all things house.
        May be stopped and then started anew to force reloading info.
        """
        if g_debug > 0:
            print "house.API.Start() 1"
        self.m_house_obj = HouseData()
        self.m_house_obj.ScheduleAPI = schedule.API()
        self.read_house(self.m_house_obj, p_house_xml)
        if g_debug > 0:
            print "house.API.Start() - House:{0:}, Active:{1:}".format(self.m_house_obj.Name, self.m_house_obj.Active)
        self.m_logger.info("Starting House {0:}.".format(self.m_house_obj.Name))
        self.m_house_obj.ScheduleAPI.Start(self.m_house_obj, p_house_xml)
        if g_debug > 0:
            print "house.API.Start() - Rooms:{0:}, Schedule:{1:}, Lights:{2:}, Controllers:{3:}".format(
                    len(self.m_house_obj.Rooms), len(self.m_house_obj.Schedule), len(self.m_house_obj.Lights), len(self.m_house_obj.Controllers))
        self.m_logger.info("Started.")
        return self.m_house_obj


    def Stop(self, p_xml):
        """Stop active houses - not active have never been started.
        Return a filled in XML for the house.
        """
        if g_debug > 0:
            print "\nhouse.Stop() - House:{0:}".format(self.m_house_obj.Name)
        l_house_xml = ET.Element('House')
        self.write_house(l_house_xml, self.m_house_obj)
        self.m_logger.info("Stopping house {0:}.".format(self.m_house_obj.Name))
        l_xml = self.m_house_obj.ScheduleAPI.Stop(l_house_xml)
        p_xml.append(l_house_xml)
        self.m_logger.info("Stopped.")
        if g_debug > 0:
            print "house.Stop() - appended schedulwe _ sub-modules"
        return p_xml

# ##  END
