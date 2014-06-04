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
from Modules.Core.data_objects import HouseData
from Modules.scheduling import schedule
from Modules.housing import internet
from Modules.housing import location
from Modules.housing import rooms
from Modules.utils import pyh_log
# from src.Modules.utils.tools import PrettyPrintAny

g_debug = 0
# 0 = off
# 1 = log extra info
# + = NOT USED HERE
LOG = pyh_log.getLogger('PyHouse.House       ')


class HouseItems(object):
    """
    Process all the house based items:
        Internet (1)
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
        self.m_house_obj.InternetAPI = internet.API()
        self.m_house_obj.ScheduleAPI = schedule.API(self.m_house_obj)
        pass


class HouseReadWriteXML(location.ReadWriteConfig, rooms.ReadWriteConfig):
    """Use the internal data to read / write an updated config file.

    This is called from the web interface or the GUI when the data has been changed.
    """

    def read_house_xml(self, p_house_xml):
        """Read house information, location and rooms.

        @param p_house_obj: is
        @param p_house_xml: is
        """
        l_house_obj = HouseData()
        self.read_base_object_xml(l_house_obj, p_house_xml)
        l_house_obj.Location = self.read_location_xml(p_house_xml)
        l_house_obj.Rooms = self.read_rooms_xml(p_house_xml)
        return l_house_obj

    def write_house_xml(self, p_house_obj):
        """Replace the data in the 'Houses' section with the current data.
        """
        l_house_xml = self.write_base_object_xml('House', p_house_obj)
        l_house_xml.append(self.write_location_xml(p_house_obj.Location))
        l_house_xml.append(self.write_rooms_xml(p_house_obj.Rooms))
        return l_house_xml


class Utility(HouseReadWriteXML):
    """
    """


class API(Utility):
    """
    """

    def __init__(self):
        """Create a house object for when we add a new house.
        """
        self.m_house_obj = HouseData()

    def Start(self, p_pyhouses_obj):
        """Start processing for all things house.
        Read in the XML file and update the internal data.
        May be stopped and then started anew to force reloading info.
        """
        self.m_pyhouses_obj = p_pyhouses_obj
        # self.m_pyhouses_obj.HouseIndex = self.m_index
        l_house_xml = p_pyhouses_obj.XmlRoot.find('Houses/House')
        self.m_house_obj = self.read_house_xml(l_house_xml)
        LOG.info("Starting House {0:}, Active:{1:}".format(self.m_house_obj.Name, self.m_house_obj.Active))
        self.m_house_obj.ScheduleAPI = schedule.API()
        self.m_house_obj.InternetAPI = internet.API()
        self.m_house_obj.ScheduleAPI.Start(self.m_pyhouses_obj, self.m_house_obj, l_house_xml)

        self.m_house_obj.InternetAPI.Start(p_pyhouses_obj, self.m_house_obj, l_house_xml)

        l_msg = "For house: {0:} ".format(self.m_house_obj.Name)
        l_msg += "- found -  Rooms:{0:}, Schedule:{1:}, Lights:{2:}, Controllers:{3:}".format(
                    len(self.m_house_obj.Rooms), len(self.m_house_obj.Schedules),
                    len(self.m_house_obj.Lights), len(self.m_house_obj.Controllers))
        LOG.info("Started. - {0:}\n".format(l_msg))
        return self.m_house_obj

    def Stop(self, p_xml, p_house_obj):
        """Stop all houses.
        Append the house XML to the passed in xlm tree.
        """
        LOG.info("Stopping House:{0:}.".format(self.m_house_obj.Name))
        l_house_xml = self.write_house_xml(p_house_obj)
        l_house_xml.append(self.write_location_xml(p_house_obj.Location))
        l_house_xml.append(self.write_rooms_xml(p_house_obj.Rooms))
        try:
            self.m_house_obj.ScheduleAPI.Stop(l_house_xml)
        except AttributeError:  # New house has  no schedule
            LOG.warning("No schedule XML")
        try:
            self.m_house_obj.InternetAPI.Stop(l_house_xml)
        except AttributeError:  # New house has  no internet
            LOG.warning("No internet XML")
        p_xml.append(l_house_xml)
        LOG.info("Stopped.")

# ##  END DBK
