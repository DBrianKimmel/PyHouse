"""
-*- test-case-name: PyHouse.src.Modules.housing.test.test_house -*-

@name: PyHouse/src/Modules/housing/house.py
@author: D. Brian Kimmel
@contact: <d.briankimmel@gmail.com
@Copyright (c) 2013-2014 by D. Brian Kimmel
@license: MIT License
@note: Created on Apr 10, 2013
@summary: Handle all of the information for a house.

There is one instance of this module for each house being controlled.

House.py knows everything about a single house.

Rooms and lights and HVAC are associated with a particular house.
"""

# Import system type stuff

# Import PyMh files
from Modules.scheduling import schedule
from Modules.computer import internet
from Modules.housing import location
from Modules.housing import rooms
from Modules.utils import pyh_log
from Modules.utils.tools import PrettyPrintAny


g_debug = 1
# 0 = off
# 1 = log extra info
# + = NOT USED HERE
LOG = pyh_log.getLogger('PyHouse.House       ')


class HouseItems(object):
    """
    Process all the house based items:
        Location (1)
        Rooms (0+)
        Schedule (0+)
        Weather (1)

        Communication (0+)
        Entertainment (0+)
        HVAC (0+)
        Irrigation (0+)
        Lighting (0+)
        Pools (0+)
        Security (0+)
    """

    def init_all_components(self):
        # self.m_house_obj.APIs.InternetAPI = internet.API()
        self.m_house_obj.APIs.ScheduleAPI = schedule.API(self.m_house_obj)
        pass


class ReadWriteConfigXml(location.ReadWriteConfigXml, rooms.ReadWriteConfigXml):
    """Use the internal data to read / write an updated config file.

    This is called from the web interface or the GUI when the data has been changed.
    """

    def get_house_xml(self, p_pyhouse_obj):
        l_house_xml = p_pyhouse_obj.Xml.XmlParsed.find('HouseDivision')
        p_pyhouse_obj.Xml.XmlSection = l_house_xml
        return l_house_xml

    def read_house_xml(self, p_pyhouse_obj):
        """Read house information, location and rooms.
        """
        l_xml = p_pyhouse_obj.Xml.XmlSection = p_pyhouse_obj.Xml.XmlParsed.find('HouseDivision')
        self.read_base_object_xml(p_pyhouse_obj.House, l_xml)
        p_pyhouse_obj.House.OBJs.Location = self.read_location_xml(l_xml)
        p_pyhouse_obj.House.OBJs.Rooms = self.read_rooms_xml(l_xml)
        # PrettyPrintAny(p_pyhouse_obj.House, 'House - read_house_xml - PyHouse_obj.House')
        # PrettyPrintAny(p_pyhouse_obj.House.OBJs, 'House - read_house_xml - PyHouse_obj.House.OBJs')
        return p_pyhouse_obj.House.OBJs

    def write_house_xml(self, p_house_obj):
        """Replace the data in the 'Houses' section with the current data.
        """
        # PrettyPrintAny(p_house_obj, 'House obj')
        l_house_xml = self.write_base_object_xml('House', p_house_obj)
        l_house_xml.append(self.write_location_xml(p_house_obj.Location))
        l_house_xml.append(self.write_rooms_xml(p_house_obj.Rooms))
        return l_house_xml


class Utility(ReadWriteConfigXml):
    """
    """

    m_pyhouse_obj = None

    def start_house_parts(self, p_pyhouse_obj):
        # PrettyPrintAny(p_pyhouse_obj, 'House - StartHouseParts - PyHouse')
        # PrettyPrintAny(p_pyhouse_obj.House, 'House - StartHouseParts - PyHouse.House')
        # PrettyPrintAny(p_pyhouse_obj.APIs, 'House - StartHouseParts - PyHouse.House.APIs')
        p_pyhouse_obj.APIs.ScheduleAPI = schedule.API()
        p_pyhouse_obj.APIs.InternetAPI = internet.API()
        p_pyhouse_obj.APIs.ScheduleAPI.Start(self.m_pyhouse_obj)
        p_pyhouse_obj.APIs.InternetAPI.Start(self.m_pyhouse_obj)

    def stop_house_parts(self, p_xml):
        try:
            self.m_pyhouse_obj.APIs.ScheduleAPI.Stop(p_xml)
        except AttributeError:  # New house has  no schedule
            LOG.warning("No schedule XML")
        try:
            self.m_pyhouse_obj.APIs.InternetAPI.Stop(p_xml)
        except AttributeError:  # New house has  no internet
            LOG.warning("No internet XML")


class API(Utility):
    """
    """

    def __init__(self):
        """Create a house object for when we add a new house.
        """

    def Start(self, p_pyhouse_obj):
        """Start processing for all things house.
        Read in the XML file and update the internal data.
        May be stopped and then started anew to force reloading info.
        """
        LOG.info('Starting')
        self.m_pyhouse_obj = p_pyhouse_obj
        p_pyhouse_obj.House.OBJs = self.read_house_xml(p_pyhouse_obj)
        self.start_house_parts(p_pyhouse_obj)
        LOG.info("Started House {0:}, Active:{1:}".format(self.m_pyhouse_obj.House.Name, self.m_pyhouse_obj.House.Active))

    def Stop(self, p_xml):
        """Stop all houses.
        Append the house XML to the passed in xlm tree.
        """
        LOG.info("Stopping House.")
        l_house_xml = self.write_house_xml(self.m_pyhouse_obj.House)
        l_house_xml.append(self.write_location_xml(self.m_pyhouse_obj.House.Location))
        l_house_xml.append(self.write_rooms_xml(self.m_pyhouse_obj.House.Rooms))
        self.stop_house_parts(l_house_xml)
        p_xml.append(l_house_xml)
        LOG.info("Stopped.")

# ##  END DBK
