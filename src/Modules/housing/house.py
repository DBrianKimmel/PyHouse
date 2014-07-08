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
from Modules.Core.data_objects import HouseInformation, HouseObjs
from Modules.scheduling import schedule
from Modules.housing import location
from Modules.housing import rooms
from Modules.utils import pyh_log
# from Modules.utils.tools import PrettyPrintAny

g_debug = 1
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
        self.m_house_obj.APIs.ScheduleAPI = schedule.API(self.m_house_obj)
        pass


class ReadWriteConfigXml(location.ReadWriteConfigXml, rooms.ReadWriteConfigXml):
    """Use the internal data to read / write an updated config file.

    This is called from the web interface or the GUI when the data has been changed.
    """

    def get_house_xml(self, p_pyhouse_obj):
        l_xml = p_pyhouse_obj.Xml.XmlRoot.find('HouseDivision')
        return l_xml

    def read_house_xml(self, p_pyhouse_obj):
        """Read house information, location and rooms.
        """
        l_xml = self.get_house_xml(p_pyhouse_obj)
        self.read_base_object_xml(p_pyhouse_obj.House, l_xml)
        p_pyhouse_obj.House.OBJs.Location = self.read_location_xml(l_xml)
        p_pyhouse_obj.House.OBJs.Rooms = self.read_rooms_xml(l_xml)
        return p_pyhouse_obj.House.OBJs

    def write_house_xml(self, p_house_obj):
        """Replace the data in the 'Houses' section with the current data.
        """
        l_house_xml = self.write_base_object_xml('HouseDivision', p_house_obj)
        l_house_xml.append(self.write_location_xml(p_house_obj.OBJs.Location))
        l_house_xml.append(self.write_rooms_xml(p_house_obj.OBJs.Rooms))
        return l_house_xml


class Utility(ReadWriteConfigXml):
    """
    """

    m_pyhouse_obj = None

    def update_pyhouse_obj(self, p_pyhouse_obj):
        p_pyhouse_obj.House = HouseInformation()
        p_pyhouse_obj.House.OBJs = HouseObjs()
        return p_pyhouse_obj

    def add_api_references(self, p_pyhouse_obj):
        p_pyhouse_obj.APIs.HouseAPI = self
        p_pyhouse_obj.APIs.ScheduleAPI = schedule.API()

    def start_house_parts(self, p_pyhouse_obj):
        p_pyhouse_obj.APIs.ScheduleAPI.Start(self.m_pyhouse_obj)

    def stop_house_parts(self, p_xml):
        try:
            self.m_pyhouse_obj.APIs.ScheduleAPI.Stop(p_xml)
        except AttributeError as e_error:  # New house has  no schedule
            LOG.warning("No schedule XML - {0:}".format(e_error))


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
        LOG.info("Starting.")
        self.update_pyhouse_obj(p_pyhouse_obj)
        self.add_api_references(p_pyhouse_obj)
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
        self.stop_house_parts(l_house_xml)
        p_xml.append(l_house_xml)
        LOG.info("Stopped.")

    def Reload(self, p_xml):
        """
        Take a snapshot of the current Configuration/Status and write out an XML file.
        """
        LOG.info("Reloading.")
        l_xml = self.write_house_xml(self.m_pyhouse_obj.House)
        self.stop_house_parts(l_xml)
        p_xml.append(l_xml)
        LOG.info("Reloaded.")

# ##  END DBK
