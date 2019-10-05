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

__updated__ = '2019-10-05'
__version_info__ = (19, 10, 1)
__version__ = '.'.join(map(str, __version_info__))

#  Import system type stuff
import datetime
import importlib

#  Import PyMh files
from Modules.Core.data_objects import HouseAPIs
from Modules.Core.Config import config_tools
from Modules.Core.Config.config_tools import Api as configApi
from Modules.Core.Utilities import uuid_tools
# Parts
from Modules.House.floors import Mqtt as floorsMqtt
from Modules.House.location import Mqtt as locationMqtt
from Modules.House.rooms import Mqtt as roomsMqtt
# Modules
from Modules.House.Entertainment.entertainment import MqttActions as entertainmentMqtt
from Modules.House.Hvac.hvac import MqttActions as hvacMqtt
from Modules.House.Irrigation.irrigation import MqttActions as irrigationMqtt
from Modules.House.Lighting.lighting import MqttActions as lightingMqtt
from Modules.House.Schedule.schedule import MqttActions as scheduleMqtt
from Modules.House.Lighting.outlets import MqttActions as outletMqtt

from Modules.Core.Utilities.debug_tools import PrettyFormatAny

from Modules.Core import logging_pyh as Logger
LOG = Logger.getLogger('PyHouse.House          ')

CONFIG_NAME = 'house'
# Note that the following are in the order needed to sequence the startup
MODULES = [  # All modules for the House must be listed here.  They will be loaded if configured.
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
PARTS = [
    'Location',
    'Floors',
    'Rooms'
    ]


class HouseInformation:

    def __init__(self):
        self.Name = None


class HousePartInformation:
    """
    """

    def __init__(self):
        self.Name = None
        self.Package = None
        self.Api = None


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
        if p_topic[0] == 'floor':
            l_logmsg += floorsMqtt(self.m_pyhouse_obj).decode(p_topic, p_message, l_logmsg)

        elif p_topic[0] == 'location':
            l_logmsg += locationMqtt(self.m_pyhouse_obj).decode(p_topic, p_message, l_logmsg)

        elif p_topic[0] == 'room':
            l_logmsg += roomsMqtt(self.m_pyhouse_obj).decode(p_topic, p_message, l_logmsg)

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


class LocalConfig:
    """
    """
    m_config = None
    m_pyhouse_obj = None

    def __init__(self, p_pyhouse_obj):
        self.m_pyhouse_obj = p_pyhouse_obj
        self.m_config = configApi(p_pyhouse_obj)

    def _extract_modules_info(self, p_yaml):
        """
        """
        _l_required = ['Name']
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

    def load_yaml_config(self):
        """ Read the house.yaml file.
         """
        LOG.info('Loading Config - Version:{}'.format(__version__))
        self.m_pyhouse_obj.House.Name = 'Unknown House Name'
        l_yaml = self.m_config.read_config(CONFIG_NAME)
        if l_yaml == None:
            LOG.error('{}.yaml is missing.'.format(CONFIG_NAME))
            return None
        try:
            l_yaml = l_yaml['House']
        except:
            LOG.warn('The config file does not start with "House:"')
            return None
        l_house = self._extract_house_info(l_yaml)
        self.m_pyhouse_obj.House.Name = l_house.Name
        return l_house  # for testing purposes


class houseUtility:
    """
    """

    m_config_tools = None
    m_module_needed = []
    m_parts_needed = []
    m_pyhouse_obj = None
    m_debugging_skip = []

    def __init__(self, p_pyhouse_obj):
        """
        """
        self.m_pyhouse_obj = p_pyhouse_obj
        self.m_config_tools = config_tools.Yaml(p_pyhouse_obj)

    def _do_import(self, p_name, submodule=''):
        """

        """
        l_package = 'Modules.House' + submodule
        l_name = l_package + '.' + p_name.lower()
        try:
            l_ret = importlib.import_module(l_name, package=l_package)
        except ImportError as e_err:
            l_msg = 'ERROR importing module: "{}"\n\tErr:{}.'.format(p_name, e_err)
            LOG.error(l_msg)
            l_ret = None
        return l_ret

    def _find_all_configed_modules(self):
        """ Find all house modules that have a "module".yaml config file somewhere in /etc/pyhouse.
        """
        for l_module in MODULES:
            l_path = self.m_config_tools.find_config_file(l_module.lower())
            if l_path != None:
                self.m_module_needed.append(l_module)
                LOG.info('Found config file for "{}"'.format(l_module))
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
            l_ret = self._do_import(l_module, submodule='.' + l_module)
            try:
                l_api = l_ret.Api(self.m_pyhouse_obj)
            except Exception as e_err:
                LOG.error('ERROR - Initializing Module: "{}"\n\tError: {}'.format(l_module, e_err))
                LOG.error('Ref: {}'.format(PrettyFormatAny.form(l_ret, 'ModuleRef', 190)))
                l_api = None
            # LOG.debug('Imported: {}'.format(l_ret))
            l_api_name = l_module.capitalize() + 'Api'
            l_house = self.m_pyhouse_obj._APIs.House
            setattr(l_house, l_api_name, l_api)
            # LOG.debug(PrettyFormatAny.form(l_house, 'House'))
            # LOG.debug(PrettyFormatAny.form(self.m_module_needed, 'Modules', 190))
        LOG.info('Loaded Modules: {}'.format(self.m_module_needed))

    def _load_modules_config(self):
        """ Load the config file for all the components of the house.
        """
        LOG.info('Loading configured modules: {}'.format(self.m_module_needed))
        l_obj = self.m_pyhouse_obj._APIs.House
        for l_key in [l_attr for l_attr in dir(l_obj) if not l_attr.startswith('_') and not callable(getattr(l_obj, l_attr))]:
            l_a = getattr(l_obj, l_key)
            if l_key == 'HouseAPI':
                continue
            if l_a == None:
                LOG.warn('Skipping "{}"'.format(l_key))
                continue
            LOG.info('Loading House Module "{}"'.format(l_key))
            l_a.LoadConfig()
        LOG.info('Finished loading all configured modules: {}'.format(self.m_module_needed))
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

    def _init_house_modules(self):
        self.m_modules = self._find_all_configed_modules()
        self._import_all_found_modules()
        return self.m_modules

    def _load_house_modules(self):
        pass

    def _start_house_modules(self):
        """ Family must start before the other things (that depend on family).
        """
        LOG.debug('Starting configured modules: {}'.format(self.m_module_needed))
        l_obj = self.m_pyhouse_obj._APIs.House
        for l_key in [l_attr for l_attr in dir(l_obj) if not l_attr.startswith('_') and not callable(getattr(l_obj, l_attr))]:
            LOG.debug('Start module "{}"'.format(l_key))
            l_a = getattr(l_obj, l_key)
            if l_key == 'HouseAPI':
                continue
            if l_a == None:
                LOG.warn('Skipping module "{}"'.format(l_key))
                continue
            l_a.Start()
        return

    def _save_house_modules(self):
        pass

    def _stop_house_modules(self):
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

    def _init_house_parts(self):
        """
        """
        l_dict = {}
        for l_part in PARTS:
            LOG.debug('Working on part {}'.format(l_part))
            self.m_parts_needed.append(l_part)
            l_obj = HousePartInformation()
            l_ret = self._do_import(l_part)
            l_obj.Name = l_part.lower()
            l_obj.Api = l_ret.Api(self.m_pyhouse_obj)
            LOG.info('Initializing house part "{}"'.format(l_obj.Name))
            l_dict[l_part] = l_obj
        return l_dict

    def _load_house_parts(self, p_parts_dict):
        """
        """
        LOG.info('Loading parts config files')
        for l_key, l_value in p_parts_dict.items():
            LOG.info('Loading house part "{}"'.format(l_key))
            l_value.Api.LoadConfig()

    def _start_house_parts(self, p_parts_dict):
        """ Family must start before the other things (that depend on family).
        """
        LOG.info('Starting parts config files')
        for l_key, l_value in p_parts_dict.items():
            LOG.info('Starting house part "{}"'.format(l_key))
            l_value.Api.Start()
        LOG.info('Finished loading all house parts config files.')

    def _save_house_parts(self, p_parts_dict):
        LOG.info('Saving parts config files')
        for l_key, l_value in p_parts_dict.items():
            LOG.info('Starting House part "{}"'.format(l_key))
            l_value.Api.SaveConfig()

    def _stop_house_parts(self, p_parts_dict):
        LOG.info('Stopping parts config files')
        for l_key, l_value in p_parts_dict.items():
            LOG.info('Stopping house part "{}"'.format(l_key))
            l_value.Api.Stop()


class Api:
    """
    """
    m_local_config = None
    m_parts = {}
    m_modules = {}
    m_utility = None

    def __init__(self, p_pyhouse_obj):
        """ **NoReactor**
        This is part of Core PyHouse - House is the reason we are running!
        Note that the reactor is not yet running.
        """
        LOG.info('Initializing - Version:{}'.format(__version__))
        self.m_pyhouse_obj = p_pyhouse_obj
        self.m_local_config = LocalConfig(p_pyhouse_obj)
        self.m_utility = houseUtility(p_pyhouse_obj)
        #
        p_pyhouse_obj.House = HouseInformation()
        p_pyhouse_obj.House.Name = p_pyhouse_obj._Parameters.Name
        p_pyhouse_obj.House.Comment = ''
        p_pyhouse_obj.House.UUID = uuid_tools.get_uuid_file(p_pyhouse_obj, CONFIG_NAME)
        p_pyhouse_obj.House.LastUpdate = datetime.datetime.now()
        p_pyhouse_obj._APIs.House = HouseAPIs()
        p_pyhouse_obj._APIs.House.HouseAPI = self
        self.m_parts = self.m_utility._init_house_parts()
        self.m_modules = self.m_utility._init_house_modules()
        LOG.info("Initialized ")

    def LoadConfig(self):
        """ The house is always present but the components of the house are plugins and not always present.
        """
        LOG.info('Loading Config - Version:{}'.format(__version__))
        self.m_local_config.load_yaml_config()
        self.m_utility._load_house_parts(self.m_parts)
        self.m_utility._load_modules_config()
        LOG.info('Loaded Config')
        return

    def Start(self):
        """Start processing for all things house.
        May be stopped and then started anew to force reloading info.
        """
        LOG.info("Starting")
        self.m_utility._start_house_parts(self.m_parts)
        self.m_utility._start_house_modules()
        LOG.info('Started House "{}"'.format(self.m_pyhouse_obj.House.Name))

    def SaveConfig(self):
        """
        Take a snapshot of the current Configuration/Status and write out the config files.
        """
        LOG.info('Saving Config - Version:{}'.format(__version__))
        # self.m_config.save_yaml_config()
        self.m_utility._save_house_parts(self.m_parts)
        self.m_utility._save_house_modules()
        # self.m_utility._save_component_apis()  # All the house submodules.
        LOG.info("Saved Config.")
        return

    def Stop(self):
        """ Stop all house stuff.
        """
        LOG.info("Stopping House.")
        self.m_utility._stop_house_parts(self.m_parts)
        self.m_utility._stop_house_modules()
        LOG.info("Stopped.")
        _x = PrettyFormatAny.form(self.m_pyhouse_obj, 'PyHouse_obj')

#  ##  END DBK
