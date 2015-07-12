"""
-*- test-case-name: PyHouse.src.Modules.Housing.test.test_house -*-

@name:      PyHouse/src/Modules/Housing/house.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2013-2015 by D. Brian Kimmel
@license:   MIT License
@note:      Created on Apr 10, 2013
@summary:   Handle all of the information for a house.

This is one of two major functions (the other is computer).

House.py knows everything about a single house.

Rooms and lights and HVAC are associated with a particular house.
"""

# Import system type stuff

# Import PyMh files
from Modules.Computer import logging_pyh as Logger
from Modules.Core.data_objects import HouseAPIs, HouseInformation, RefHouseObjs, DeviceHouseObjs
from Modules.Housing import location
from Modules.Housing import rooms
from Modules.Entertainment.entertainment import API as entertainmentAPI
from Modules.Families.family import API as familyAPI
from Modules.Hvac.thermostats import API as hvacAPI
from Modules.Irrigation.irrigation import API as irrigationAPI
from Modules.Lighting.lighting import API as lightingAPI
from Modules.Pool.pool import API as poolAPI
from Modules.Scheduling.schedule import API as scheduleAPI
from Modules.Scheduling.sunrisesunset import API as sunriseAPI
from Modules.Security.security import API as securityAPI
from Modules.Utilities.xml_tools import XmlConfigTools


LOG = Logger.getLogger('PyHouse.House          ')

MODULES = ['Entertainment', 'Hvac', 'Irrigation', 'Lighting', 'Pool', 'Scheduling', 'Security']

class HouseItems(object):
    """
    Process all the house based items:
        Location (1)
        Rooms (0+)
        Schedule (0+)
        Entertainment (0+)
        HVAC (0+)
        Irrigation (0+)
        Lighting (0+)
        Pools (0+)
        Security (0+)
    """

class ReadWriteConfigXml(location.ReadWriteConfigXml, rooms.ReadWriteConfigXml):
    """Use the internal data to read / write an updated config file.

    This is called from the web interface or the GUI when the data has been changed.
    """

    def _get_house_xml(self, p_pyhouse_obj):
        l_xml = p_pyhouse_obj.Xml.XmlRoot.find('HouseDivision')
        return l_xml

    def _read_base(self, p_xml):
        l_xml = HouseInformation()
        l_xml.RefOBJs = RefHouseObjs()
        l_xml.DeviceOBJs = DeviceHouseObjs()
        self.read_base_object_xml(l_xml, p_xml)
        return l_xml

    def _read_location_xml(self, p_xml):
        l_xml = self.read_location_xml(p_xml)
        return l_xml

    def _read_rooms_xml(self, p_xml):
        l_xml = self.read_rooms_xml(p_xml)
        return l_xml

    def read_house_xml(self, p_pyhouse_obj):
        """Read house information, location and rooms.
        """
        l_xml = self._get_house_xml(p_pyhouse_obj)
        l_house = self._read_base(l_xml)
        l_house.RefOBJs.Location = self._read_location_xml(l_xml)
        l_house.RefOBJs.Rooms = self._read_rooms_xml(l_xml)
        return l_house

    def write_house_xml(self, p_house_obj):
        """Replace the data in the 'Houses' section with the current data.
        """
        l_house_xml = XmlConfigTools().write_base_object_xml('HouseDivision', p_house_obj)
        l_house_xml.append(self.write_location_xml(p_house_obj.RefOBJs.Location))
        l_house_xml.append(self.write_rooms_xml(p_house_obj.RefOBJs.Rooms))
        return l_house_xml


class Utility(ReadWriteConfigXml):
    """
    """

    m_pyhouse_obj = None

    @staticmethod
    def _init_component_apis(p_pyhouse_obj, p_api):
        """
        Initialize all the house APIs
        """
        p_pyhouse_obj.APIs.House = HouseAPIs()
        p_pyhouse_obj.APIs.House.HouseAPI = p_api
        p_pyhouse_obj.APIs.House.EntertainmentAPI = entertainmentAPI(p_pyhouse_obj)
        p_pyhouse_obj.APIs.House.FamilyAPI = familyAPI(p_pyhouse_obj)
        p_pyhouse_obj.APIs.House.HvacAPI = hvacAPI(p_pyhouse_obj)
        p_pyhouse_obj.APIs.House.IrrigationAPI = irrigationAPI(p_pyhouse_obj)
        p_pyhouse_obj.APIs.House.LightingAPI = lightingAPI(p_pyhouse_obj)
        p_pyhouse_obj.APIs.House.PoolAPI = poolAPI(p_pyhouse_obj)
        p_pyhouse_obj.APIs.House.ScheduleAPI = scheduleAPI(p_pyhouse_obj)
        p_pyhouse_obj.APIs.House.SecurityAPI = securityAPI(p_pyhouse_obj)
        p_pyhouse_obj.APIs.House.SunRiseSetAPI = sunriseAPI(p_pyhouse_obj)

    @staticmethod
    def _init_pyhouse_data(p_pyhouse_obj):
        p_pyhouse_obj.House = HouseInformation()
        p_pyhouse_obj.House.RefOBJs = RefHouseObjs()
        p_pyhouse_obj.House.DeviceOBJs = DeviceHouseObjs()

    def start_house_parts(self, p_pyhouse_obj):
        # These two must start before the other things
        p_pyhouse_obj.APIs.House.FamilyAPI.Start()
        p_pyhouse_obj.APIs.House.SunRiseSetAPI.Start()
        # self.m_pyhouse_obj.House.RefOBJs.FamilyData = self.m_pyhouse_obj.APIs.House.FamilyAPI.Start()
        p_pyhouse_obj.APIs.House.EntertainmentAPI.Start()
        p_pyhouse_obj.APIs.House.HvacAPI.Start()
        p_pyhouse_obj.APIs.House.IrrigationAPI.Start()
        p_pyhouse_obj.APIs.House.LightingAPI.Start()
        p_pyhouse_obj.APIs.House.PoolAPI.Start()
        p_pyhouse_obj.APIs.House.ScheduleAPI.Start()
        p_pyhouse_obj.APIs.House.SecurityAPI.Start()

    def stop_house_parts(self):
        self.m_pyhouse_obj.APIs.House.ScheduleAPI.Stop()

    def get_sunrise_set(self, p_pyhouse_obj):
        """
        Retrieve datetime.datetime for sunrise and sunset.
        """
        p_pyhouse_obj.APIs.House.SunRiseSetAPI.Start()
        p_pyhouse_obj.House.RefOBJs.Location.RiseSet.SunRise = p_pyhouse_obj.APIs.House.SunRiseSetAPI.get_sunrise_datetime()
        p_pyhouse_obj.House.RefOBJs.Location.RiseSet.SunSet = p_pyhouse_obj.APIs.House.SunRiseSetAPI.get_sunset_datetime()
        pass

    def _store_pyhouse_obj(self, p_pyhouse_obj):
        self.m_pyhouse_obj = p_pyhouse_obj


class API(Utility):
    """
    """

    def __init__(self, p_pyhouse_obj):
        """
        """
        self.m_pyhouse_obj = p_pyhouse_obj
        Utility._init_component_apis(p_pyhouse_obj, self)
        Utility._init_pyhouse_data(p_pyhouse_obj)

    def Start(self):
        """Start processing for all things house.
        Read in the HouseDivision portion XML file and update the internal data.
        May be stopped and then started anew to force reloading info.
        """
        LOG.info("Starting.")
        self.m_pyhouse_obj.House = self.read_house_xml(self.m_pyhouse_obj)
        self.get_sunrise_set(self.m_pyhouse_obj)
        self.start_house_parts(self.m_pyhouse_obj)
        LOG.info("Started House {0:}".format(self.m_pyhouse_obj.House.Name))

    def Stop(self):
        """Stop all houses.
        Append the house XML to the passed in xlm tree.
        """
        LOG.info("Stopping House.")
        self.stop_house_parts()
        LOG.info("Stopped.")

    def SaveXml(self, p_xml):
        """
        Take a snapshot of the current Configuration/Status and write out an XML file.
        """
        # l_house_xml = ET.Element('HouseDivision')
        l_house_xml = XmlConfigTools().write_base_object_xml('HouseDivision', self.m_pyhouse_obj.House)
        l_location_xml = self.write_location_xml(self.m_pyhouse_obj.House.RefOBJs.Location)
        l_house_xml.append(l_location_xml)
        l_rooms_xml = self.write_rooms_xml(self.m_pyhouse_obj.House.RefOBJs.Rooms)
        l_house_xml.append(l_rooms_xml)
        self.m_pyhouse_obj.APIs.House.ScheduleAPI.SaveXml(l_house_xml)
        # l_lighting_xml = ''
        self.m_pyhouse_obj.APIs.House.IrrigationAPI.SaveXml(l_house_xml)
        p_xml.append(l_house_xml)
        LOG.info("Saved XML.")
        return p_xml

# ##  END DBK
