#!/usr/bin/python

"""Handle the house information.
"""

# Import system type stuff
import logging

# Import PyMh files
import configure_mh
import config_xml
import internet
import lighting_tools


Configure_Data = configure_mh.Configure_Data
House_Data = {}
Location_Data = {}
Room_Data = {}


LocationCount = 0
RoomCount = 0
g_logger = None


class HouseData(object):

    def __init__(self):
        self.Active = False
        self.Name = None

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
        l_ret = ' House:{0:}, Active:{1:}, Lat:{2:}, Lon:{3:}'.format(
            self.get_name(), self.get_active(), self.get_latitude(),
            self.get_longitude())
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
        l_ret = '** Room:{0:} \t Size:{1:} \t Corner:{2:}\n'.format(self.get_name(), self.get_size(), self.get_corner())
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

    def get_LocationCount(self):
        return LocationCount

    def get_RoomCount(self):
        return RoomCount

    def load_all_locations(self, p_dict):
        """Get the data from the config file.
        """
        for l_dict in p_dict.itervalues():
            self.load_location(l_dict)

    def load_location(self, p_dict):
        l_house = HouseData()
        l_entry = LocationData()
        l_entry.Active = self.getBool(p_dict, 'Active')
        l_house.Active = l_entry.Active
        l_entry.City = self.getText(p_dict, 'City')
        l_entry.Latitude = self.getFloat(p_dict, 'Latitude')
        l_entry.Longitude = self.getFloat(p_dict, 'Longitude')
        l_entry.Key = self.get_LocationCount()
        l_entry.Name = self.getText(p_dict, 'Name')
        l_house.Name = l_entry.Name
        l_entry.Phone = self.getText(p_dict, 'Phone')
        l_entry.SavingTime = self.getFloat(p_dict, 'SavingTime')
        l_entry.State = self.getText(p_dict, 'State')
        l_entry.Street = self.getText(p_dict, 'Street')
        l_entry.TimeZone = self.getFloat(p_dict, 'TimeZone')
        l_entry.ZipCode = self.getText(p_dict, 'ZipCode')
        Location_Data[l_entry.Key] = l_entry
        House_Data[l_entry.Key] = l_house

    def load_xml_house(self):
        """Load all the xml house info.
        If there is none, fall back to using the old config files.
        This fallback is temporary until the xml and gui is fully functional.
        """
        l_ct = config_xml.ReadConfig().read_houses()
        if l_ct == 0:
            self.load_all_locations(Configure_Data['HouseLocation'])

    def dump_location(self):
        print "***** All House Locations *****"
        for l_key, l_obj in Location_Data.iteritems():
            self.dump_device(l_obj, 'Location', l_key)
        print

    def load_all_rooms(self, p_dict):
        for l_dict in p_dict.itervalues():
            self.load_room(l_dict)

    def load_room(self, p_dict):
        l_entry = RoomData()
        l_entry.Active = self.getBool(p_dict, 'Active')
        l_entry.Comment = self.getText(p_dict, 'Comment')
        l_entry.Corner = self.getText(p_dict, 'Corner')
        l_entry.HouseName = self.getText(p_dict, 'HouseName')
        l_entry.Key = self.get_RoomCount()
        l_entry.Name = self.getText(p_dict, 'Name')
        l_entry.Size = self.getText(p_dict, 'Size')
        Room_Data[l_entry.Key] = l_entry

    def dump_rooms(self):
        print "***** All House Rooms *****"
        for l_key, l_obj in Room_Data.iteritems():
            self.dump_device(l_obj, 'Room', l_key)
        print


def Init():
    global g_logger
    g_logger = logging.getLogger('PyHouse.House')
    g_logger.info("Initializing.")
    #HouseAPI().load_all_locations(Configure_Data['HouseLocation'])
    HouseAPI().load_xml_house()
    #HouseAPI().load_all_rooms(Configure_Data['Rooms'])
    #HouseAPI().dump_location()
    #HouseAPI().dump_rooms()
    internet.Init()

def Start(p_reactor):
    pass

###  END
