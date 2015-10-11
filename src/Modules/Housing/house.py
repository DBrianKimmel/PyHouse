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
from Modules.Core.data_objects import HouseAPIs, HouseInformation
from Modules.Housing.location import Xml as locationXML
from Modules.Housing.rooms import Xml as roomsXML
from Modules.Entertainment.entertainment import API as entertainmentAPI
from Modules.Families.family import API as familyAPI
from Modules.Hvac.hvac import API as hvacAPI
from Modules.Irrigation.irrigation import API as irrigationAPI
from Modules.Lighting.lighting import API as lightingAPI
from Modules.Pool.pool import API as poolAPI
from Modules.Scheduling.schedule import API as scheduleAPI
from Modules.Scheduling.sunrisesunset import API as sunriseAPI
from Modules.Security.security import API as securityAPI
from Modules.Utilities.xml_tools import XmlConfigTools
from Modules.Computer import logging_pyh as Logger
# from Modules.Utilities.debug_tools import PrettyFormatAny

LOG = Logger.getLogger('PyHouse.House          ')

MODULES = ['Entertainment', 'Hvac', 'Irrigation', 'Lighting', 'Pool', 'Scheduling', 'Security']

class Xml(object):
    """Use the internal data to read / write an updated config file.

    This is called from the web interface or the GUI when the data has been changed.
    """

    @staticmethod
    def _read_base(p_xml):
        l_obj = HouseInformation()
        XmlConfigTools.read_base_object_xml(l_obj, p_xml)
        return l_obj

    @staticmethod
    def read_house_xml(p_pyhouse_obj):
        """Read house information, location and rooms.
        """
        l_xml = p_pyhouse_obj.Xml.XmlRoot.find('HouseDivision')
        p_pyhouse_obj.House = Xml._read_base(l_xml)
        p_pyhouse_obj.House.Location = locationXML.read_location_xml(p_pyhouse_obj)
        p_pyhouse_obj.House.Rooms = roomsXML.read_rooms_xml(l_xml)
        return p_pyhouse_obj.House

    @staticmethod
    def write_house_xml(p_pyhouse_obj):
        """Replace the data in the 'Houses' section with the current data.
        """
        # print(PrettyFormatAny.form(p_pyhouse_obj, 'PyHouse'))
        l_house_obj = p_pyhouse_obj.House
        # print(PrettyFormatAny.form(l_house_obj, 'PyHouse'))
        l_house_xml = XmlConfigTools.write_base_object_xml('HouseDivision', p_pyhouse_obj.House)
        l_house_xml.append(locationXML.write_location_xml(p_pyhouse_obj.House.Location))
        l_house_xml.append(roomsXML.write_rooms_xml(p_pyhouse_obj.House.Rooms))
        return l_house_xml


class Utility(object):
    """
    """

    m_pyhouse_obj = None

    @staticmethod
    def _init_components(p_pyhouse_obj):
        p_pyhouse_obj.House = HouseInformation()
        p_pyhouse_obj.APIs.House = HouseAPIs()

    @staticmethod
    def _init_component_apis(p_pyhouse_obj, p_api):
        """
        Initialize all the house APIs
        """
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

    def start_house_parts(self, p_pyhouse_obj):
        # These two must start before the other things
        p_pyhouse_obj.APIs.House.FamilyAPI.Start()
        #
        p_pyhouse_obj.APIs.House.EntertainmentAPI.Start()
        p_pyhouse_obj.APIs.House.HvacAPI.Start()
        p_pyhouse_obj.APIs.House.IrrigationAPI.Start()
        p_pyhouse_obj.APIs.House.LightingAPI.Start()
        p_pyhouse_obj.APIs.House.PoolAPI.Start()
        p_pyhouse_obj.APIs.House.SecurityAPI.Start()
        #  Last
        p_pyhouse_obj.APIs.House.SunRiseSetAPI.Start()
        p_pyhouse_obj.APIs.House.ScheduleAPI.Start()

    def stop_house_parts(self):
        self.m_pyhouse_obj.APIs.House.ScheduleAPI.Stop()

    @staticmethod
    def _save_component_apis(p_pyhouse_obj, p_xml):
        p_pyhouse_obj.APIs.House.EntertainmentAPI.SaveXml(p_xml)
        p_pyhouse_obj.APIs.House.HvacAPI.SaveXml(p_xml)
        p_pyhouse_obj.APIs.House.IrrigationAPI.SaveXml(p_xml)
        p_pyhouse_obj.APIs.House.LightingAPI.SaveXml(p_xml)
        p_pyhouse_obj.APIs.House.PoolAPI.SaveXml(p_xml)
        p_pyhouse_obj.APIs.House.ScheduleAPI.SaveXml(p_xml)
        p_pyhouse_obj.APIs.House.SecurityAPI.SaveXml(p_xml)
        return p_xml

    def get_sunrise_set(self, p_pyhouse_obj):
        """
        Retrieve datetime.datetime for sunrise and sunset.
        """
        p_pyhouse_obj.APIs.House.SunRiseSetAPI.Start()
        p_pyhouse_obj.House.Location.RiseSet.SunRise = p_pyhouse_obj.APIs.House.SunRiseSetAPI.get_sunrise_datetime()
        p_pyhouse_obj.House.Location.RiseSet.SunSet = p_pyhouse_obj.APIs.House.SunRiseSetAPI.get_sunset_datetime()
        pass


class API(Utility):
    """
    """

    def __init__(self, p_pyhouse_obj):
        """
        """
        self.m_pyhouse_obj = p_pyhouse_obj
        Utility._init_components(p_pyhouse_obj)
        Utility._init_component_apis(p_pyhouse_obj, self)
        LOG.info('Initialized')

    def Start(self):
        """Start processing for all things house.
        Read in the HouseDivision portion XML file and update the internal data.
        May be stopped and then started anew to force reloading info.
        """
        LOG.info("Starting.")
        self.m_pyhouse_obj.House = Xml.read_house_xml(self.m_pyhouse_obj)
        self.get_sunrise_set(self.m_pyhouse_obj)
        self.start_house_parts(self.m_pyhouse_obj)
        LOG.info("Started House {}".format(self.m_pyhouse_obj.House.Name))

    def Stop(self):
        """Stop all houses.
        Append the house XML to the passed in xlm tree.
        """
        LOG.info("Stopping House.")
        self.stop_house_parts()
        LOG.info("Stopped.")

    def LoadXml(self, p_pyhouse_obj):
        l_house = Xml.read_house_xml(p_pyhouse_obj)
        # p_pyhouse_obj.APIs.House.EntertainmentAPI.Start()
        p_pyhouse_obj.APIs.House.HvacAPI.LoadXml(p_pyhouse_obj)
        # p_pyhouse_obj.APIs.House.IrrigationAPI.Start()
        p_pyhouse_obj.APIs.House.LightingAPI.LoadXml(p_pyhouse_obj)
        # p_pyhouse_obj.APIs.House.PoolAPI.Start()
        p_pyhouse_obj.APIs.House.ScheduleAPI.LoadXml(p_pyhouse_obj)
        # p_pyhouse_obj.APIs.House.SecurityAPI.Start()
        return

    def SaveXml(self, p_xml):
        """
        Take a snapshot of the current Configuration/Status and write out an XML file.
        """
        # l_house_xml = ET.Element('HouseDivision')
        l_house_xml = Xml.write_house_xml(self.m_pyhouse_obj)
        Utility._save_component_apis(self.m_pyhouse_obj, l_house_xml)
        p_xml.append(l_house_xml)
        LOG.info("Saved House XML.")
        return p_xml

# ##  END DBK
