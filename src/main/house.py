#!/usr/bin/python

"""Handle the house information.

main/house.py

There is location information for the house.  This is for calculating the
time of sunrise and sunset.  Additional calculations ma be added such as
moonrise, tides, etc.

There is one instance of this for each house configured.

Rooms and lights and HVAC are associated with a particular house.
"""

# Import system type stuff
import logging

# Import PyMh files
from schedule import schedule
from configure import config_xml
from lighting import lighting_tools
import internet
import weather

g_debug = 2
g_logger = None
g_api = None

House_Data = {}
Location_Data = {}
Room_Data = {}

HouseCount = 0
LocationCount = 0
RoomCount = 0


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


class LocationData(lighting_tools.CoreData):

    def __init__(self):
        global LocationCount
        LocationCount += 1
        self.Active = False
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


class RoomData(lighting_tools.CoreData):

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


class HouseAPI(lighting_tools.CoreAPI):
    """
    """

    def load_xml_houses(self):
        """Load all the xml house info.
        """
        global House_Data, Location_Data, Room_Data
        if g_debug > 1:
            print "house.load_xml_houses() 1 ", Location_Data, Room_Data
        House_Data = configure.config_xml.ReadConfig().read_houses()
        if g_debug > 1:
            print "house.load_xml_houses() 2 ", Location_Data, Room_Data

    def save_xml_house(self):
        pass

    def dump_house(self):
        if g_debug > 8:
            print "*** House ****"
            for l_obj in House_Data.itervalues():
                self.dump_device(l_obj, 'House')

    def XXdump_location(self):
        if g_debug > 8:
            print "***** All House Locations ***", Location_Data
            for l_key, l_obj in Location_Data.iteritems():
                self.dump_device(l_obj, 'Location', l_key)
            print

    def XXdump_rooms(self):
        if g_debug > 8:
            print "***** All House Rooms *****", Room_Data
            for l_key, l_obj in Room_Data.iteritems():
                self.dump_device(l_obj, 'Room', l_key)
            print


class API(HouseAPI):
    """
    """

    m_schedules = []
    m_active_houses = 0

    def __init__(self):
        global g_logger
        g_logger = logging.getLogger('PyHouse.House')
        g_logger.info("Initializing all houses.")
        config_xml.read_config()
        if g_debug > 0:
            print "house.__init__() all houses.", House_Data
        #
        for l_obj in House_Data.itervalues():
            if g_debug > 1:
                print "house.__init__() House:{0:}, Active:{1:}".format(l_obj.Name, l_obj.Active)
            if l_obj.Active != True:
                continue
            self.m_schedules.append(schedule.API(l_obj))
            self.m_active_houses += 1
        #
        internet.Init()
        weather.Init()
        g_logger.info("Initialized.")
        if g_debug > 0:
            print "house.__init__() all houses initialized now."

    def Start(self):
        if g_debug > 0:
            print "house.Start()"
        g_logger.info("Starting.")
        self.load_xml_houses()
        self.dump_house()
        #
        for l_ix in self.m_schedules:
            self.m_schedules[l_ix].Start()
        #
        internet.Start()
        weather.Start()
        g_logger.info("Started.")


    def Stop(self):
        if g_debug > 0:
            print "house.Stop()"
        g_logger.info("Stopping.")
        self.save_xml_house()
        #
        self.m_sched.Stop()
        internet.Stop()
        weather.Stop()
        g_logger.info("Stopped.")

# ##  END
