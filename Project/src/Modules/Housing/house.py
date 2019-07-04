"""
@name:      PyHouse/Project/src/Modules/Housing/house.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2013-2019 by D. Brian Kimmel
@license:   MIT License
@note:      Created on Apr 10, 2013
@summary:   Handle all of the information for a house.

This is one of two major functions (the other is computer).

House.py knows everything about a single house.

Rooms and lights and HVAC are associated with a particular house.

PyHouse.House.
              FamilyInformation
              Hvac
              Irrigation
              Lighting
              Location
              Pools
              Rooms
              Rules
              Schedules
              ...
"""

__updated__ = '2019-07-02'
__version_info__ = (19, 5, 0)
__version__ = '.'.join(map(str, __version_info__))

#  Import system type stuff
import datetime

#  Import PyMh files
from Modules.Core.data_objects import HouseAPIs, UuidData, BaseUUIDObject
from Modules.Core.Utilities import uuid_tools
from Modules.Core.Utilities.uuid_tools import Uuid
from Modules.Core.Utilities.xml_tools import XmlConfigTools, PutGetXML
from Modules.Families.family import API as familyAPI
from Modules.Housing.Entertainment.entertainment import \
    API as entertainmentAPI, \
    MqttActions as entertainmentMqtt
from Modules.Housing import location, rooms, floors
from Modules.Housing.rooms import Mqtt as roomsMqtt
from Modules.Housing.Hvac.hvac import API as hvacAPI, MqttActions as hvacMqtt
from Modules.Housing.Irrigation.irrigation import API as irrigationAPI, MqttActions as irrigationMqtt
from Modules.Housing.Lighting.lighting import API as lightingAPI, MqttActions as lightingMqtt
from Modules.Housing.Pool.pool import API as poolAPI
from Modules.Housing.Scheduling.schedule import API as scheduleAPI, MqttActions as scheduleMqtt
from Modules.Housing.Security.security import API as securityAPI
from Modules.Housing.Sync.sync import API as syncAPI
# from Modules.Core.Utilities.debug_tools import PrettyFormatAny

from Modules.Computer import logging_pyh as Logger
LOG = Logger.getLogger('PyHouse.House          ')

UUID_FILE_NAME = 'House.uuid'
MODULES = ['Entertainment', 'Hvac', 'Irrigation', 'Lighting', 'Pool', 'Rules', 'Scheduling', 'Security']


class HouseInformation(BaseUUIDObject):
    """ The collection of information about a house.
    Causes JSON errors due to API type data methinks.

    ==> PyHouse.House.xxx as in the def below.
    """

    def __init__(self):
        super(HouseInformation, self).__init__()
        self.HouseMode = 'Home'  # Home, Away, Vacation,
        self.Entertainment = {}  # EntertainmentInformation() in Entertainment/entertainment_data.py
        self.Hvac = {}  # HvacData()
        self.Irrigation = {}  # IrrigationData()
        self.Lighting = {}  # LightingData()
        self.Location = {}  # house.location.LocationInformation() - one location per house.
        self.Pools = {}  # PoolData()
        self.Rooms = {}  # RoomInformation()
        self.Rules = {}  # RulesData()
        self.Schedules = {}  # ScheduleBaseData()
        self.Security = {}  # SecurityData()
        self._Commands = {}  # Module dependent


class MqttActions:
    """
    """

    def __init__(self, p_pyhouse_obj):
        self.m_pyhouse_obj = p_pyhouse_obj

    def decode(self, p_topic, p_message):
        """
        --> pyhouse/<housename>/house/topic03...
        """
        l_logmsg = '\tHouse: {}\n'.format(self.m_pyhouse_obj.House.Name)
        # LOG.debug('MqttHouseDispatch Topic:{}'.format(p_topic))
        if p_topic[0] == 'room':
            l_logmsg += roomsMqtt(self.m_pyhouse_obj)._decode_room(p_topic, p_message, l_logmsg)
        elif p_topic[0] == 'entertainment':
            l_logmsg += entertainmentMqtt(self.m_pyhouse_obj).decode(p_topic[1:], p_message, l_logmsg)
        elif p_topic[0] == 'hvac':
            l_logmsg += hvacMqtt(self.m_pyhouse_obj).decode(p_topic[1:], p_message, l_logmsg)
        elif p_topic[0] == 'irrigation':
            l_logmsg += irrigationMqtt(self.m_pyhouse_obj).decode(p_topic[1:], p_message, l_logmsg)
        elif p_topic[0] == 'lighting':
            l_logmsg += lightingMqtt(self.m_pyhouse_obj).decode(p_topic[1:], p_message, l_logmsg)
        elif p_topic[0] == 'schedule':
            l_logmsg = scheduleMqtt(self.m_pyhouse_obj).decode(p_topic[1:], p_message, l_logmsg)
        else:
            l_logmsg += '\tUnknown sub-topic {}'.format(p_message)
            LOG.warn('Unknown House Topic: {}'.format(p_topic[0]))
        return l_logmsg


class Xml:
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
        l_obj = p_pyhouse_obj.House
        l_xml = XmlConfigTools.find_xml_section(p_pyhouse_obj, 'HouseDivision')
        if l_xml is None:
            l_obj.Name = 'Default Name'
            l_obj.Key = 0
            l_obj.Active = True
            l_obj.Mode = 'Home'
            l_obj.Priority = 0
            return l_obj
        XmlConfigTools.read_base_UUID_object_xml(l_obj, l_xml)
        Xml._add_uuid(p_pyhouse_obj, l_obj)
        l_obj.Mode = PutGetXML.get_text_from_xml(l_xml, 'Mode', 'Home')
        l_obj.Priority = PutGetXML.get_int_from_xml(l_xml, 'Priority', 0)
        return l_obj

    @staticmethod
    def read_house_config(p_pyhouse_obj):
        """Read house information, location and rooms.
        """
        l_obj = Xml._read_house_base(p_pyhouse_obj)
        # l_obj.Location = locationXML.read_location_xml(p_pyhouse_obj)
        # location.Api(p_pyhouse_obj).LoadConfig()
        # l_obj.Rooms = roomsXML().read_rooms_xml(p_pyhouse_obj)
        return l_obj

    def write_house_xml(self, p_pyhouse_obj):
        """Replace the data in the 'Houses' section with the current data.
        """
        l_house_xml = XmlConfigTools.write_base_UUID_object_xml('HouseDivision', p_pyhouse_obj.House)
        # PutGetXML.put_text_element(l_house_xml, 'Mode', p_pyhouse_obj.House.Mode)
        # PutGetXML.put_text_element(l_house_xml, 'Priority', p_pyhouse_obj.House.Priority)
        # l_house_xml.append(locationXML.write_location_xml(p_pyhouse_obj.House.Location))
        # l_house_xml.append(roomsXML().write_rooms_xml(p_pyhouse_obj.House.Rooms))
        return l_house_xml


class Utility:
    """
    """

    m_pyhouse_obj = None

    @staticmethod
    def _init_component_apis(p_pyhouse_obj, p_api):
        """
        Initialize all the house _APIs
        """
        # print(PrettyFormatAny.form(p_pyhouse_obj.House, 'house.API-2', 180))
        p_pyhouse_obj._APIs.House.HouseAPI = p_api
        p_pyhouse_obj._APIs.House.EntertainmentAPI = entertainmentAPI(p_pyhouse_obj)
        p_pyhouse_obj._APIs.House.FamilyAPI = familyAPI(p_pyhouse_obj)
        p_pyhouse_obj._APIs.House.HvacAPI = hvacAPI(p_pyhouse_obj)
        p_pyhouse_obj._APIs.House.IrrigationAPI = irrigationAPI(p_pyhouse_obj)
        p_pyhouse_obj._APIs.House.LightingAPI = lightingAPI(p_pyhouse_obj)
        p_pyhouse_obj._APIs.House.PoolAPI = poolAPI(p_pyhouse_obj)
        p_pyhouse_obj._APIs.House.ScheduleAPI = scheduleAPI(p_pyhouse_obj)
        p_pyhouse_obj._APIs.House.SecurityAPI = securityAPI(p_pyhouse_obj)
        p_pyhouse_obj._APIs.House.SyncAPI = syncAPI(p_pyhouse_obj)

    @staticmethod
    def _load_component_config(p_pyhouse_obj):
        """ Load the XML config file for all the components of the house.
        """
        p_pyhouse_obj._APIs.House.EntertainmentAPI.LoadConfig(p_pyhouse_obj)
        p_pyhouse_obj._APIs.House.FamilyAPI.LoadXml(p_pyhouse_obj)
        p_pyhouse_obj._APIs.House.HvacAPI.LoadXml(p_pyhouse_obj)
        p_pyhouse_obj._APIs.House.IrrigationAPI.LoadXml(p_pyhouse_obj)
        p_pyhouse_obj._APIs.House.LightingAPI.LoadConfig(p_pyhouse_obj)
        p_pyhouse_obj._APIs.House.PoolAPI.LoadXml(p_pyhouse_obj)
        p_pyhouse_obj._APIs.House.ScheduleAPI.LoadXml(p_pyhouse_obj)
        p_pyhouse_obj._APIs.House.SecurityAPI.LoadXml(p_pyhouse_obj)
        p_pyhouse_obj._APIs.House.SyncAPI.LoadXml(p_pyhouse_obj)
        pass

    def start_house_parts(self, p_pyhouse_obj):
        """ Family must start before the other things (that depend on family).
        """
        p_pyhouse_obj._APIs.House.FamilyAPI.Start()
        p_pyhouse_obj._APIs.House.EntertainmentAPI.Start()
        p_pyhouse_obj._APIs.House.HvacAPI.Start()
        p_pyhouse_obj._APIs.House.IrrigationAPI.Start()
        p_pyhouse_obj._APIs.House.LightingAPI.Start()
        p_pyhouse_obj._APIs.House.PoolAPI.Start()
        p_pyhouse_obj._APIs.House.SecurityAPI.Start()
        p_pyhouse_obj._APIs.House.ScheduleAPI.Start()

    @staticmethod
    def XX_save_component_apis(p_pyhouse_obj, p_xml):
        """ These are sub-module parts of the house.
        """
        p_xml.append(p_pyhouse_obj._APIs.House.EntertainmentAPI.SaveXml(p_xml))
        p_xml.append(p_pyhouse_obj._APIs.House.HvacAPI.SaveXml(p_xml))
        p_xml.append(p_pyhouse_obj._APIs.House.IrrigationAPI.SaveXml(p_xml))
        p_xml.append(p_pyhouse_obj._APIs.House.LightingAPI.SaveConfig(p_xml))
        p_xml.append(p_pyhouse_obj._APIs.House.PoolAPI.SaveXml(p_xml))
        p_xml.append(p_pyhouse_obj._APIs.House.ScheduleAPI.SaveXml(p_xml))
        p_xml.append(p_pyhouse_obj._APIs.House.SecurityAPI.SaveXml(p_xml))
        return

    def stop_house_parts(self):
        self.m_pyhouse_obj._APIs.House.EntertainmentAPI.Stop()
        self.m_pyhouse_obj._APIs.House.ScheduleAPI.Stop()


class API(Utility):
    """
    """
    m_location_api = None
    m_rooms_api = None

    def __init__(self, p_pyhouse_obj):
        """ **NoReactor**
        This is part of Core PyHouse - House is the reason we are running!
        Note that the reactor is not yet running.
        """
        LOG.info('Initializing - Version:{}'.format(__version__))
        p_pyhouse_obj.House = HouseInformation()
        self.m_location_api = location.Api(p_pyhouse_obj)
        self.m_floor_api = floors.Api(p_pyhouse_obj)
        self.m_rooms_api = rooms.Api(p_pyhouse_obj)
        p_pyhouse_obj.House.Name = p_pyhouse_obj._Parameters.Name
        p_pyhouse_obj.House.Key = 0
        p_pyhouse_obj.House.Active = True
        p_pyhouse_obj.House.UUID = uuid_tools.get_uuid_file(p_pyhouse_obj, UUID_FILE_NAME)
        p_pyhouse_obj.House.Comment = ''
        p_pyhouse_obj.House.LastUpdate = datetime.datetime.now()
        p_pyhouse_obj._APIs.House = HouseAPIs()
        Utility._init_component_apis(p_pyhouse_obj, self)
        self.m_pyhouse_obj = p_pyhouse_obj
        LOG.info("Initialized - Version:{}".format(__version__))

    def LoadConfig(self, p_pyhouse_obj):
        """ The house is always present but the components of the house are plugins and not always present.
        """
        LOG.info('Loading Config - Version:{}'.format(__version__))
        self.m_location_api.LoadConfig()
        self.m_floor_api.LoadConfig()
        self.m_rooms_api.LoadConfig()
        # l_house = Xml.read_house_config(p_pyhouse_obj)
        # p_pyhouse_obj.House = l_house
        Utility._load_component_config(p_pyhouse_obj)
        LOG.info('Loaded Config - Version:{}'.format(__version__))
        return

    def Start(self):
        """Start processing for all things house.
        May be stopped and then started anew to force reloading info.
        """
        LOG.info("Starting - Version:{}".format(__version__))
        self.start_house_parts(self.m_pyhouse_obj)
        LOG.info("Started House {}".format(self.m_pyhouse_obj.House.Name))

    def SaveConfig(self, p_pyhouse_obj):
        """
        Take a snapshot of the current Configuration/Status and write out the config files.
        """
        LOG.info('Saving Config - Version:{}'.format(__version__))
        self.m_location_api.SaveConfig()
        self.m_floor_api.SaveConfig()
        self.m_rooms_api.SaveConfig()
        l_xml = Xml().write_house_xml(self.m_pyhouse_obj)
        # Utility._save_component_apis(self.m_pyhouse_obj, l_house_xml)  # All the house submodules.
        # p_xml.append(l_house_xml)  # The entire house XML
        p_pyhouse_obj._Config.XmlTree.append(l_xml)
        LOG.info("Saved House XML Config.")
        return

    def Stop(self):
        """ Stop all house stuff.
        """
        LOG.info("Stopping House.")
        self.stop_house_parts()
        LOG.info("Stopped.")

#  ##  END DBK
