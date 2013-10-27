#!/usr/bin/python

"""Handle all the house(s) information.

main/house.py

There is one instance of this module for each house being controlled.

House.py knows everything about a single house.

There is location information for the house.  This is for calculating the
time of sunrise and sunset.  Additional calculations may be added such as
moonrise, tides, etc.

"""

# Import system type stuff
import logging
import uuid

# Import PyMh files
from src.scheduling import schedule
from src.housing import internet
from src.housing import location
from src.housing import rooms
#from src.families import family


g_debug = 0
# 0 = off
# 1 = log extra info
# 2 = major routine entry
# 3 = get/put xml config info
# + = NOT USED HERE
g_logger = logging.getLogger('PyHouse.House       ')


class HouseData(object):

    def __init__(self):
        self.Name = ''
        self.Key = 0
        self.Active = False
        self.UUID = None
        self.InternetAPI = None
        self.LightingAPI = None
        self.ScheduleAPI = None
        self.Location = location.LocationData()  # one location per house.
        # a dict of zero or more of the following.
        self.Buttons = {}
        self.Controllers = {}
        self.FamilyData = {}
        self.Internet = {}
        self.Lights = {}
        self.Rooms = {}
        self.Schedules = {}

    def __str__(self):
        l_ret = ' House:: '
        l_ret += 'Name:{0:}, '.format(self.Name)
        l_ret += "Active:{0:}, ".format(self.Active)
        l_ret += "Key:{0:}, ".format(self.Key)
        l_ret += "Lights:{0:}, ".format(len(self.Lights))
        l_ret += "Controllers:{0:}, ".format(len(self.Controllers))
        l_ret += "Buttons:{0:}, ".format(len(self.Buttons))
        l_ret += "Rooms:{0:}, ".format(len(self.Rooms))
        l_ret += "Schedules:{0:}, ".format(len(self.Schedules))
        l_ret += 'UUID:{0:};'.format(self.UUID)
        return l_ret

    def reprJSON(self):
        l_ret = dict(Name = self.Name, Key = self.Key, Active = self.Active,
                    Buttons = self.Buttons, Controllers = self.Controllers, Lights = self.Lights,
                    Location = self.Location,
                    Internet = self.Internet,
                    Family = self.FamilyData,
                    Rooms = self.Rooms,
                    Schedules = self.Schedules,
                    UUID = self.UUID)
        return l_ret


class HouseReadWriteConfig(location.ReadWriteConfig, rooms.ReadWriteConfig):
    """Use the internal data to read / write an updated config file.

    This is called from the web interface or the GUI when the data has been changed.
    """

    def read_house_xml(self, p_house_obj, p_house_xml):
        """Read house information, location and rooms.
        """
        self.xml_read_common_info(p_house_obj, p_house_xml)
        p_house_obj.UUID = self.get_uuid_from_xml(p_house_xml, 'UUID')
        p_house_obj.Location = self.read_location_xml(p_house_obj, p_house_xml)
        p_house_obj.Rooms = self.read_rooms_xml(p_house_obj, p_house_xml)
        if g_debug >= 3:
            print "house.read_house_xml() - Loading XML data for House:{0:}".format(p_house_obj.Name)
        return p_house_obj

    def write_house_xml(self, p_house_obj):
        """Replace the data in the 'Houses' section with the current data.
        """
        l_house_xml = self.xml_create_common_element('House', p_house_obj)
        self.put_text_element(l_house_xml, 'UUID', p_house_obj.UUID)
        return l_house_xml


class API(HouseReadWriteConfig):
    """
    """

    def __init__(self):
        """Create a house object for when we add a new house.
        """
        self.m_house_obj = HouseData()

    def Start(self, p_house_xml):
        """Start processing for all things house.
        Read in the XML file and update the internal data.
        May be stopped and then started anew to force reloading info.
        """
        self.read_house_xml(self.m_house_obj, p_house_xml)
        g_logger.info("Starting House {0:}, Active:{1:}".format(self.m_house_obj.Name, self.m_house_obj.Active))
        self.m_house_obj.ScheduleAPI = schedule.API(self.m_house_obj)
        self.m_house_obj.InternetAPI = internet.API()
        self.m_house_obj.ScheduleAPI.Start(self.m_house_obj, p_house_xml)
        self.m_house_obj.InternetAPI.Start(self.m_house_obj, p_house_xml)
        l_msg = "For house: {0:} ".format(self.m_house_obj.Name)
        l_msg += "- found -  Rooms:{0:}, Schedule:{1:}, Lights:{2:}, Controllers:{3:}".format(
                    len(self.m_house_obj.Rooms), len(self.m_house_obj.Schedules),
                    len(self.m_house_obj.Lights), len(self.m_house_obj.Controllers))
        if g_debug >= 2:
            print "house.API.Start() ", l_msg
        g_logger.info("Started. - {0:}\n".format(l_msg))
        return self.m_house_obj


    def Stop(self, p_xml, p_house_obj):
        """Stop all houses.
        Return a filled in XML for the house.
        """
        if g_debug >= 2:
            print "\nhouse.API.Stop() - House:{0:}".format(self.m_house_obj.Name)
        g_logger.info("Stopping House:{0:}.".format(self.m_house_obj.Name))
        l_house_xml = self.write_house_xml(p_house_obj)
        l_house_xml.append(self.write_location_xml(p_house_obj.Location))
        l_house_xml.append(self.write_rooms_xml(p_house_obj))
        try:
            l_house_xml.extend(self.m_house_obj.ScheduleAPI.Stop(l_house_xml, p_house_obj))
            l_house_xml.append(self.m_house_obj.InternetAPI.Stop())
        except AttributeError:  # New house has  no schedule or internet
            pass
        if g_debug >= 2:
            print "house.API.Stop() - Name:{0:}, Count:{1:}".format(self.m_house_obj.Name, len(l_house_xml))
        g_logger.info("Stopped.")
        return l_house_xml

    def UpdateXml(self, p_xml):
        l_xml = self.write_house_xml(self.m_house_obj)
        l_xml.append(self.write_location_xml(self.m_house_obj.Location))
        l_xml.append(self.write_rooms_xml(self.m_house_obj))
        ###l_xml.extend(self.m_house_obj.ScheduleAPI.UpdateXml(l_xml))
        self.m_house_obj.ScheduleAPI.UpdateXml(l_xml)
        self.m_house_obj.InternetAPI.UpdateXml(l_xml)
        p_xml.append(l_xml)

    def Update(self, p_entry):
        """
        """
        if g_debug >= 0:
            print "house.API.Update() - House:{0:}".format(self.m_house_obj.Name)
            print '    ', p_entry
        l_type = p_entry.Type

# ##  END DBK
