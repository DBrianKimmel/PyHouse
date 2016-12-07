"""
-*- test-case-name: PyHouse.src.Modules.Housing.test.test_house -*-

@name:      PyHouse/src/Modules/Housing/house.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2013-2016 by D. Brian Kimmel
@license:   MIT License
@note:      Created on Apr 10, 2013
@summary:   Handle all of the information for a house.

This is one of two major functions (the other is computer).

House.py knows everything about a single house.

Rooms and lights and HVAC are associated with a particular house.

PyHouse.House.
              FamilyData
              Hvac
              Irrigation
              Lighting
              Location
              Pools
              Rooms
              Rules
              Schedules

"""
from Modules.Utilities.debug_tools import PrettyFormatAny

__updated__ = '2016-11-28'

#  Import system type stuff

#  Import PyMh files
from Modules.Core.data_objects import HouseAPIs, HouseInformation, UuidData
from Modules.Housing.Entertainment.entertainment import API as entertainmentAPI
from Modules.Families.family import API as familyAPI
from Modules.Housing.location import Xml as locationXML
from Modules.Housing.rooms import Xml as roomsXML, Mqtt as roomsMqtt
from Modules.Housing.Hvac.hvac import API as hvacAPI
from Modules.Housing.Irrigation.irrigation import API as irrigationAPI
from Modules.Housing.Lighting.lighting import API as lightingAPI
from Modules.Housing.Pool.pool import API as poolAPI
from Modules.Housing.Scheduling.schedule import API as scheduleAPI
from Modules.Housing.Security.security import API as securityAPI
from Modules.Utilities.uuid_tools import Uuid
from Modules.Utilities.xml_tools import XmlConfigTools
from Modules.Computer import logging_pyh as Logger
LOG = Logger.getLogger('PyHouse.House          ')

MODULES = ['Entertainment', 'Hvac', 'Irrigation', 'Lighting', 'Pool', 'Scheduling', 'Security']


class MqttActions(object):
    """
    """

    def __init__(self, p_pyhouse_obj):
        self.m_pyhouse_obj = p_pyhouse_obj

    def decode(self, p_logmsg, p_topic, p_message):
        p_logmsg += '\tHouse: {}\n'.format(self.m_pyhouse_obj.House.Name)
        if p_topic[2] == 'room':
            p_logmsg += roomsMqtt()._decode_room(p_logmsg, p_topic, p_message)
        #  computer/***
        else:
            p_logmsg += '\tUnknown sub-topic {}'.format(PrettyFormatAny.form(p_message, 'House msg', 160))
        return p_logmsg


class Xml(object):
    """Use the internal data to read / write an updated config file.

    This is called from the web interface or the GUI when the data has been changed.
    """

    @staticmethod
    def _add_uuid(p_pyhouse_obj, p_obj):
        l_obj = UuidData()
        l_obj.UUID = p_obj.UUID
        l_obj.UuidType = 'House'
        Uuid.add_uuid(p_pyhouse_obj, l_obj)

    @staticmethod
    def _read_house_base(p_pyhouse_obj):
        l_obj = HouseInformation()
        l_xml = p_pyhouse_obj.Xml.XmlRoot.find('HouseDivision')
        if l_xml is None:
            return l_obj
        XmlConfigTools.read_base_UUID_object_xml(l_obj, l_xml)
        Xml._add_uuid(p_pyhouse_obj, l_obj)
        return l_obj

    @staticmethod
    def read_house_xml(p_pyhouse_obj):
        """Read house information, location and rooms.
        """
        l_obj = Xml._read_house_base(p_pyhouse_obj)
        l_obj.Location = locationXML.read_location_xml(p_pyhouse_obj)
        l_obj.Rooms = roomsXML().read_rooms_xml(p_pyhouse_obj)
        return l_obj

    @staticmethod
    def write_house_xml(p_pyhouse_obj):
        """Replace the data in the 'Houses' section with the current data.
        """
        l_house_xml = XmlConfigTools.write_base_UUID_object_xml('HouseDivision', p_pyhouse_obj.House)
        l_house_xml.append(locationXML.write_location_xml(p_pyhouse_obj.House.Location))
        l_house_xml.append(roomsXML.write_rooms_xml(p_pyhouse_obj.House.Rooms))
        return l_house_xml


class Utility(object):
    """
    """

    m_pyhouse_obj = None

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

    @staticmethod
    def _load_component_xml(p_pyhouse_obj):
        """ Load the XML config file for all the components of the house.
        """
        p_pyhouse_obj.APIs.House.EntertainmentAPI.LoadXml(p_pyhouse_obj)
        p_pyhouse_obj.APIs.House.FamilyAPI.LoadXml(p_pyhouse_obj)
        p_pyhouse_obj.APIs.House.HvacAPI.LoadXml(p_pyhouse_obj)
        p_pyhouse_obj.APIs.House.IrrigationAPI.LoadXml(p_pyhouse_obj)
        p_pyhouse_obj.APIs.House.LightingAPI.LoadXml(p_pyhouse_obj)
        p_pyhouse_obj.APIs.House.PoolAPI.LoadXml(p_pyhouse_obj)
        p_pyhouse_obj.APIs.House.ScheduleAPI.LoadXml(p_pyhouse_obj)
        p_pyhouse_obj.APIs.House.SecurityAPI.LoadXml(p_pyhouse_obj)
        pass

    def start_house_parts(self, p_pyhouse_obj):
        #  Family must start before the other things (that depend on family).
        p_pyhouse_obj.APIs.House.FamilyAPI.Start()
        p_pyhouse_obj.APIs.House.EntertainmentAPI.Start()
        p_pyhouse_obj.APIs.House.HvacAPI.Start()
        p_pyhouse_obj.APIs.House.IrrigationAPI.Start()
        p_pyhouse_obj.APIs.House.LightingAPI.Start()
        p_pyhouse_obj.APIs.House.PoolAPI.Start()
        p_pyhouse_obj.APIs.House.SecurityAPI.Start()
        p_pyhouse_obj.APIs.House.ScheduleAPI.Start()

    @staticmethod
    def _save_component_apis(p_pyhouse_obj, p_xml):
        """ Family does not get saved - it is created dynamically when XML is loaded.
        """
        p_pyhouse_obj.APIs.House.EntertainmentAPI.SaveXml(p_xml)
        p_pyhouse_obj.APIs.House.HvacAPI.SaveXml(p_xml)
        p_pyhouse_obj.APIs.House.IrrigationAPI.SaveXml(p_xml)
        p_pyhouse_obj.APIs.House.LightingAPI.SaveXml(p_xml)
        p_pyhouse_obj.APIs.House.PoolAPI.SaveXml(p_xml)
        p_pyhouse_obj.APIs.House.ScheduleAPI.SaveXml(p_xml)
        p_pyhouse_obj.APIs.House.SecurityAPI.SaveXml(p_xml)
        return p_xml

    def stop_house_parts(self):
        self.m_pyhouse_obj.APIs.House.EntertainmentAPI.Stop()
        self.m_pyhouse_obj.APIs.House.ScheduleAPI.Stop()


class API(Utility):
    """
    """

    def __init__(self, p_pyhouse_obj):
        """
        """
        LOG.info('Initializing')
        p_pyhouse_obj.APIs.House = HouseAPIs()
        Utility._init_component_apis(p_pyhouse_obj, self)
        self.m_pyhouse_obj = p_pyhouse_obj
        LOG.info('Initialized')

    def LoadXml(self, p_pyhouse_obj):
        LOG.info('Loading XML')
        p_pyhouse_obj.House = HouseInformation()  # Clear before loading
        l_house = Xml.read_house_xml(p_pyhouse_obj)
        p_pyhouse_obj.House = l_house
        Utility._load_component_xml(p_pyhouse_obj)
        LOG.info('Loaded XML')
        return l_house

    def Start(self):
        """Start processing for all things house.
        Read in the HouseDivision portion XML file and update the internal data.
        May be stopped and then started anew to force reloading info.
        """
        LOG.info("Starting.")
        self.start_house_parts(self.m_pyhouse_obj)
        LOG.info("Started House {}".format(self.m_pyhouse_obj.House.Name))

    def SaveXml(self, p_xml):
        """
        Take a snapshot of the current Configuration/Status and write out an XML file.
        """
        #  l_house_xml = ET.Element('HouseDivision')
        l_house_xml = Xml.write_house_xml(self.m_pyhouse_obj)
        Utility._save_component_apis(self.m_pyhouse_obj, l_house_xml)
        p_xml.append(l_house_xml)
        LOG.info("Saved House XML.")
        return p_xml

    def Stop(self):
        """Stop all houses.
        Append the house XML to the passed in xlm tree.
        """
        LOG.info("Stopping House.")
        self.stop_house_parts()
        LOG.info("Stopped.")

    def DecodeMqtt(self, p_logmsg, p_topic, p_message):
        MqttActions(self.m_pyhouse_obj).decode(p_logmsg, p_topic, p_message)

#  ##  END DBK
