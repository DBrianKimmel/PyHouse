"""
@name:      Modules/House/house.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2013-2020 by D. Brian Kimmel
@license:   MIT License
@note:      Created on Apr 10, 2013
@summary:   Handle all of the information for a house.

This is one of two major functions (the other is computer).

"""

__updated__ = '2020-01-25'
__version_info__ = (20, 1, 25)
__version__ = '.'.join(map(str, __version_info__))

#  Import system type stuff
# from typing import Union

#  Import PyMh files
from Modules.Core.Config import config_tools
from Modules.Core.Config.config_tools import Api as configApi
# Parts
from Modules.House.floors import MqttActions as floorsMqtt
from Modules.House.location import MqttActions as locationMqtt
from Modules.House.rooms import MqttActions as roomsMqtt
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
    """
    ==> PyHouse_obj.House.xxx
    """

    def __init__(self):
        self.Name: Union[str, None] = None
        self.Comment: str = ''
        self.Module = {}  # {modulename: Api}


class MqttActions:
    """
    """

    def __init__(self, p_pyhouse_obj):
        self.m_pyhouse_obj = p_pyhouse_obj

    def decode(self, p_msg):
        """
        ==> pyhouse/<housename>/house/topic03...
        ==> pyhouse/<housename>/topic
        """
        p_msg.LogMessage += '\tHouse: {}\n'.format(self.m_pyhouse_obj.House.Name)
        l_topic = p_msg.UnprocessedTopic[0].lower()
        p_msg.UnprocessedTopic = p_msg.UnprocessedTopic[1:]
        if l_topic == 'floor':
            floorsMqtt(self.m_pyhouse_obj).decode(p_msg)
        elif l_topic == 'location':
            locationMqtt(self.m_pyhouse_obj).decode(p_msg)
        elif l_topic == 'room':
            roomsMqtt(self.m_pyhouse_obj).decode(p_msg)

        elif l_topic == 'entertainment':
            entertainmentMqtt(self.m_pyhouse_obj).decode(p_msg)
        elif l_topic == 'hvac':
            hvacMqtt(self.m_pyhouse_obj).decode(p_msg)
        elif l_topic == 'irrigation':
            irrigationMqtt(self.m_pyhouse_obj).decode(p_msg)
        elif l_topic in ['lighting']:
            lightingMqtt(self.m_pyhouse_obj).decode(p_msg)
        elif l_topic == 'schedule':
            scheduleMqtt(self.m_pyhouse_obj).decode(p_msg)
        elif l_topic == 'outlet':
            outletMqtt(self.m_pyhouse_obj).decode(p_msg)
        else:
            p_msg.LogMessage += '\tUnknown sub-topic: "{}"'.format(l_topic)
            LOG.warning('Unknown House Topic: {}\n\tTopic: {}\n\tMessge: {}'.format(l_topic, p_msg.Topic, p_msg.Payload))


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
            LOG.warning('No "Modules" list in "house.yaml"')
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
                LOG.warning('house.yaml is missing an entry for "{}"'.format(l_key))
        return l_obj

    def load_yaml_config(self):
        """ Read the house.yaml file.
         """
        LOG.info('Loading Config - Version:{}'.format(__version__))
        self.m_pyhouse_obj.House.Name = 'Unknown House Name'
        l_yaml = self.m_config.read_config_file(CONFIG_NAME)
        if l_yaml == None:
            LOG.error('{}.yaml is missing.'.format(CONFIG_NAME))
            return None
        try:
            l_yaml = l_yaml['House']
        except:
            LOG.warning('The config file does not start with "House:"')
            return None
        l_house = self._extract_house_info(l_yaml)
        self.m_pyhouse_obj.House.Name = l_house.Name
        return l_house  # for testing purposes


class Api:
    """
    """

    m_config_tools = None
    m_local_config = None
    m_pyhouse_obj = None
    m_parts = {}
    m_modules_apis: dict = {}

    def __init__(self, p_pyhouse_obj):
        """ **NoReactor**
        This is part of Core PyHouse - House is the reason we are running!
        Note that the reactor is not yet running.
        """
        LOG.info('Initializing')
        self.m_pyhouse_obj = p_pyhouse_obj
        self._add_storage()
        self.m_config_tools = config_tools.Yaml(p_pyhouse_obj)
        self.m_local_config = LocalConfig(p_pyhouse_obj)
        #
        LOG.info('Initializing Parts')
        l_path = 'Modules.House'
        l_parts = self.m_config_tools.find_module_list(PARTS)
        self.m_parts = self.m_config_tools.import_module_list(l_parts, l_path)
        #
        LOG.info('Initializing Modules')
        l_path = 'Modules.House.'
        l_modules = self.m_config_tools.find_module_list(MODULES)
        l_modules.append('Family')
        self.m_modules_apis = self.m_config_tools.import_module_list(l_modules, l_path)
        #
        LOG.info("Initialized ")

    def _add_storage(self):
        """
        """
        self.m_pyhouse_obj.House = HouseInformation()
        self.m_pyhouse_obj.House.Comment = ''

    def LoadConfig(self):
        """ The house is always present but the components of the house are plugins and not always present.
        """
        LOG.info('Loading Config - Version:{}'.format(__version__))
        self.m_local_config.load_yaml_config()
        LOG.info('Loading parts config files')
        for l_key, l_value in self.m_parts.items():
            LOG.info('Loading house part "{}"'.format(l_key))
            l_value.LoadConfig()
        for l_module in self.m_modules_apis.values():
            l_module.LoadConfig()
        LOG.info('Loaded Config')

    def Start(self):
        """Start processing for all things house.
        May be stopped and then started anew to force reloading info.
        """
        LOG.info("Starting")
        for l_module in self.m_modules_apis.values():
            l_module.Start()
        LOG.info('Started House "{}"'.format(self.m_pyhouse_obj.House.Name))

    def SaveConfig(self):
        """
        Take a snapshot of the current Configuration/Status and write out the config files.
        """
        LOG.info('Saving Config - Version:{}'.format(__version__))
        for l_module in self.m_parts.values():
            l_module.SaveConfig()
        for l_module in self.m_modules_apis.values():
            l_module.SaveConfig()
        LOG.info("Saved Config.")

    def Stop(self):
        """ Stop all house stuff.
        """
        LOG.info("Stopping House.")
        for l_module in self.m_modules_apis.values():
            l_module.Stop()
        LOG.info("Stopped.")
        _x = PrettyFormatAny.form(self.m_pyhouse_obj, 'PyHouse_obj')

#  ##  END DBK
