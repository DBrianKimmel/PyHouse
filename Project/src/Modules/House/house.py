"""
@name:      Modules/House/house.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2013-2019 by D. Brian Kimmel
@license:   MIT License
@note:      Created on Apr 10, 2013
@summary:   Handle all of the information for a house.

This is one of two major functions (the other is computer).

"""

__updated__ = '2019-08-17'
__version_info__ = (19, 5, 0)
__version__ = '.'.join(map(str, __version_info__))

#  Import system type stuff
import datetime
import importlib

#  Import PyMh files
from Modules.Core.data_objects import HouseAPIs, BaseUUIDObject
from Modules.Core.Utilities import uuid_tools, config_tools
from Modules.House import location, rooms, floors
from Modules.House.rooms import Mqtt as roomsMqtt

from Modules.House.Entertainment.entertainment import MqttActions as entertainmentMqtt
from Modules.House.Hvac.hvac import MqttActions as hvacMqtt
from Modules.House.Irrigation.irrigation import MqttActions as irrigationMqtt
from Modules.House.Lighting.lighting import MqttActions as lightingMqtt
from Modules.House.Schedule.schedule import MqttActions as scheduleMqtt
from Modules.House.Lighting.outlets import MqttActions as outletMqtt

from Modules.Core.Utilities.debug_tools import PrettyFormatAny

from Modules.Core import logging_pyh as Logger
LOG = Logger.getLogger('PyHouse.House          ')

CONFIG_FILE_NAME = 'house.yaml'
UUID_FILE_NAME = 'House.uuid'

# Note that the following are in the order needed to sequence the startup
MODULES = [
        'Lighting',
        'Hvac',
        'Security',
        'Irrigation',
        'Pool',
        'Rules',
        'Schedule',
        'Sync',
        'Entertainment',
        'Family'
        ]


class HouseInformation(BaseUUIDObject):
    """ The collection of information about a house.
    Causes JSON errors due to API type data methinks.

    ==> PyHouse.House.xxx as in the def below.
    """

    def __init__(self):
        super(HouseInformation, self).__init__()
        # self.HouseMode = 'Home'  # Home, Away, Vacation,
        #
        self.Entertainment = {}  # EntertainmentInformation() in Entertainment/entertainment_data.py
        self.Family = {}
        self.Hvac = {}  # HvacData()
        self.Irrigation = {}  # IrrigationData()
        self.Lighting = {}  # LightingInformation()
        self.Location = {}  # house.location.LocationInformation() - one location per house.
        self.Pools = {}  # PoolData()
        self.Rooms = {}  # RoomInformation()
        self.Rules = {}  # RulesData()
        self.Schedules = {}  # ScheduleInformation()
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
        elif p_topic[0] == 'outlet':
            l_logmsg = outletMqtt(self.m_pyhouse_obj).decode(p_topic[1:], p_message, l_logmsg)
        else:
            l_logmsg += '\tUnknown sub-topic {}'.format(p_message)
            LOG.warn('Unknown House Topic: {}\n\tTopic: {}\n\tMessge: {}'.format(p_topic[0], p_topic, p_message))
        return l_logmsg


class Config:
    """
    """

    def __init__(self, p_pyhouse_obj):
        self.m_pyhouse_obj = p_pyhouse_obj

    def _extract_modules_info(self, p_yaml):
        """
        """
        l_required = ['Name']
        l_obj = HouseInformation()
        try:
            l_modules = p_yaml['Modules']
        except:
            LOG.warn('No "Modules" list in "house.yaml"')
            return
        for l_module in l_modules:
            LOG.debug('found Module "{}" in house config file.'.format(l_module))
        return l_obj

    def _extract_house_info(self, p_config):
        """
        """
        l_required = ['Name']
        l_obj = HouseInformation()
        for l_key, l_value in p_config.items():
            if l_key == 'Modules':
                pass
            setattr(l_obj, l_key, l_value)
        for l_key in [l_attr for l_attr in dir(l_obj) if not l_attr.startswith('_') and not callable(getattr(l_obj, l_attr))]:
            if getattr(l_obj, l_key) == None and l_key in l_required:
                LOG.warn('house.yaml is missing an entry for "{}"'.format(l_key))
        return l_obj

    def LoadYamlConfig(self):
        """ Read the Rooms.Yaml file.
        It contains Rooms data for all rooms in the house.
        """
        # LOG.deb('Loading Config - Version:{}'.format(__version__))
        try:
            l_node = config_tools.Yaml(self.m_pyhouse_obj).read_yaml(CONFIG_FILE_NAME)
        except:
            return None
        try:
            l_yaml = l_node.Yaml['House']
        except:
            LOG.warn('The house.yaml file does not start with "House:"')
            return None
        l_house = self._extract_house_info(l_yaml)
        self.m_pyhouse_obj.House.Name = l_house.Name
        return l_node  # for testing purposes

# ----------

    def _copy_to_yaml(self):
        """
        """
        l_node = self.m_pyhouse_obj._Config.YamlTree[CONFIG_FILE_NAME]
        l_config = l_node.Yaml['House']
        self.m_pyhouse_obj._Config.YamlTree[CONFIG_FILE_NAME].Yaml['House'] = l_config
        l_ret = {'House': l_config}
        return l_ret

    def SaveYamlConfig(self):
        """
        """
        LOG.info('Saving Config - Version:{}'.format(__version__))
        l_config = self._copy_to_yaml()
        config_tools.Yaml(self.m_pyhouse_obj).write_yaml(l_config, CONFIG_FILE_NAME, addnew=True)
        return l_config


class Utility:
    """
    """

    m_module_needed = []
    m_pyhouse_obj = None
    m_debugging_skip = []

    def __init__(self, p_pyhouse_obj):
        """
        """
        self.m_pyhouse_obj = p_pyhouse_obj

    def find_all_configed_modules(self):
        """ Find all house modules that have a "module".yaml config file somewhere in /etc/pyhouse.
        """
        for l_module in MODULES:
            l_filename = l_module.lower() + '.yaml'
            l_node = config_tools.Yaml.find_config_node(self, l_filename)
            if l_node != None:
                self.m_module_needed.append(l_module)
        # Add family - It is not configured but is derived from things configured.
        if 'Family' not in self.m_module_needed:
            self.m_module_needed.append('Family')
        LOG.info('Found config files for: {}'.format(self.m_module_needed))
        return self.m_module_needed  # for debugging

    def _import_all_found_modules(self):
        """ Now we know what we need, load and run just those modules.
        """
        for l_module in self.m_module_needed:
            if l_module in self.m_debugging_skip:
                LOG.warn('Skip import (for debugging) of module "{}"'.format(l_module))
                continue
            # LOG.debug('Starting import of Module: "{}"'.format(l_module))
            l_package = 'Modules.House.' + l_module.capitalize()  # p_family_obj.PackageName  # contains e.g. 'Modules.Families.Insteon'
            l_name = l_package + '.' + l_module.lower()
            try:
                l_ret = importlib.import_module(l_name, package=l_package)
            except ImportError as e_err:
                l_msg = 'ERROR importing module: {}\n\tErr:{}.'.format(l_module, e_err)
                LOG.error(l_msg)
                l_ret = None
            try:
                l_api = l_ret.API(self.m_pyhouse_obj)
            except Exception as e_err:
                LOG.error('ERROR - Initializing Module: "{}"\n\tError: {}'.format(l_module, e_err))
                LOG.error('Ref: {}'.format(PrettyFormatAny.form(l_ret, 'ModuleRef', 190)))
                l_api = None
            # LOG.debug('Imported: {}'.format(l_ret))
            l_api_name = l_module.capitalize() + 'API'
            l_house = self.m_pyhouse_obj._APIs.House
            setattr(l_house, l_api_name, l_api)
            # LOG.debug(PrettyFormatAny.form(l_house, 'House'))
        # LOG.debug(PrettyFormatAny.form(self.m_module_needed, 'Modules', 190))
        LOG.info('Loaded Modules: {}'.format(self.m_module_needed))

    def _load_component_config(self):
        """ Load the config file for all the components of the house.
        """
        LOG.debug('Loading configured modules: {}'.format(self.m_module_needed))
        l_obj = self.m_pyhouse_obj._APIs.House
        for l_key in [l_attr for l_attr in dir(l_obj) if not l_attr.startswith('_') and not callable(getattr(l_obj, l_attr))]:
            l_a = getattr(l_obj, l_key)
            if l_key == 'HouseAPI':
                continue
            if l_a == None:
                LOG.warn('Skipping "{}"'.format(l_key))
                continue
            LOG.debug('Loading House Module "{}"'.format(l_key))
            l_a.LoadConfig()
        return

    def _start_house_parts(self):
        """ Family must start before the other things (that depend on family).
        """
        LOG.debug('Starting configured modules: {}'.format(self.m_module_needed))
        l_obj = self.m_pyhouse_obj._APIs.House
        for l_key in [l_attr for l_attr in dir(l_obj) if not l_attr.startswith('_') and not callable(getattr(l_obj, l_attr))]:
            l_a = getattr(l_obj, l_key)
            if l_key == 'HouseAPI':
                continue
            if l_a == None:
                LOG.warn('Skipping "{}"'.format(l_key))
                continue
            l_a.Start()
        return

    def _save_component_apis(self):
        """ These are sub-module parts of the house.
        """
        l_obj = self.m_pyhouse_obj._APIs.House
        for l_key in [l_attr for l_attr in dir(l_obj) if not l_attr.startswith('_') and not callable(getattr(l_obj, l_attr))]:
            l_a = getattr(l_obj, l_key)
            if l_key == 'HouseAPI':
                continue
            if l_a == None:
                LOG.warn('Skipping "{}"'.format(l_key))
                continue
            l_a.SaveConfig()
        return

    def stop_house_parts(self):
        l_obj = self.m_pyhouse_obj._APIs.House
        for l_key in [l_attr for l_attr in dir(l_obj) if not l_attr.startswith('_') and not callable(getattr(l_obj, l_attr))]:
            l_a = getattr(l_obj, l_key)
            if l_key == 'HouseAPI':
                continue
            if l_a == None:
                LOG.warn('Skipping "{}"'.format(l_key))
                continue
            l_a.Stop()
        return
        self.m_pyhouse_obj._APIs.House.EntertainmentAPI.Stop()
        self.m_pyhouse_obj._APIs.House.ScheduleAPI.Stop()


class API:
    """
    """
    m_config = None
    m_location_api = None
    m_rooms_api = None
    m_utility = None

    def __init__(self, p_pyhouse_obj):
        """ **NoReactor**
        This is part of Core PyHouse - House is the reason we are running!
        Note that the reactor is not yet running.
        """
        LOG.info('Initializing - Version:{}'.format(__version__))
        self.m_pyhouse_obj = p_pyhouse_obj
        self.m_config = Config(p_pyhouse_obj)
        self.m_utility = Utility(p_pyhouse_obj)
        #
        p_pyhouse_obj.House = HouseInformation()
        self.m_location_api = location.Api(p_pyhouse_obj)
        self.m_floor_api = floors.Api(p_pyhouse_obj)
        self.m_rooms_api = rooms.Api(p_pyhouse_obj)
        #
        p_pyhouse_obj.House.Name = p_pyhouse_obj._Parameters.Name
        p_pyhouse_obj.House.Key = 0
        # p_pyhouse_obj.House.Active = True
        p_pyhouse_obj.House.UUID = uuid_tools.get_uuid_file(p_pyhouse_obj, UUID_FILE_NAME)
        p_pyhouse_obj.House.Comment = ''
        p_pyhouse_obj.House.LastUpdate = datetime.datetime.now()
        p_pyhouse_obj._APIs.House = HouseAPIs()
        p_pyhouse_obj._APIs.House.HouseAPI = self
        # LOG.debug(PrettyFormatAny.form(self.m_pyhouse_obj.House, 'House', 190))
        #
        self.m_utility.find_all_configed_modules()
        self.m_utility._import_all_found_modules()

        LOG.info("Initialized - Version:{}".format(__version__))

    def LoadConfig(self):
        """ The house is always present but the components of the house are plugins and not always present.
        """
        LOG.info('Loading Config - Version:{}'.format(__version__))
        self.m_config.LoadYamlConfig()
        self.m_location_api.LoadConfig()
        self.m_floor_api.LoadConfig()
        self.m_rooms_api.LoadConfig()
        self.m_utility._load_component_config()
        LOG.info('Loaded Config - Version:{}'.format(__version__))
        return

    def Start(self):
        """Start processing for all things house.
        May be stopped and then started anew to force reloading info.
        """
        LOG.info("Starting - Version:{}".format(__version__))
        self.m_utility._start_house_parts()
        LOG.info("Started House {}".format(self.m_pyhouse_obj.House.Name))

    def SaveConfig(self):
        """
        Take a snapshot of the current Configuration/Status and write out the config files.
        """
        LOG.info('Saving Config - Version:{}'.format(__version__))
        # self.m_config.SaveYamlConfig()
        # self.m_location_api.SaveConfig()
        # self.m_floor_api.SaveConfig()
        self.m_rooms_api.SaveConfig()
        self.m_utility._save_component_apis()  # All the house submodules.
        LOG.info("Saved House Config.")
        return

    def Stop(self):
        """ Stop all house stuff.
        """
        LOG.info("Stopping House.")
        self.m_utility.stop_house_parts()
        LOG.info("Stopped.")

#  ##  END DBK