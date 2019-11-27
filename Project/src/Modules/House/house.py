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

__updated__ = '2019-11-26'
__version_info__ = (19, 10, 1)
__version__ = '.'.join(map(str, __version_info__))

#  Import system type stuff

#  Import PyMh files
from Modules.Core.Config import config_tools, import_tools
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
        self.Name = None
        self.Comment = None
        self.Module = {}  # {modulename: Api}


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
        l_topic = p_topic[0].lower()
        # LOG.debug('MqttHouseDispatch Topic:{}'.format(p_topic))
        if l_topic == 'floor':
            l_logmsg += floorsMqtt(self.m_pyhouse_obj).decode(p_topic, p_message, l_logmsg)

        elif l_topic == 'location':
            l_logmsg += locationMqtt(self.m_pyhouse_obj).decode(p_topic, p_message, l_logmsg)

        elif l_topic == 'room':
            l_logmsg += roomsMqtt(self.m_pyhouse_obj).decode(p_topic, p_message, l_logmsg)

        elif l_topic == 'entertainment':
            l_logmsg += entertainmentMqtt(self.m_pyhouse_obj).decode(p_topic[1:], p_message, l_logmsg)
        elif l_topic == 'hvac':
            l_logmsg += hvacMqtt(self.m_pyhouse_obj).decode(p_topic[1:], p_message, l_logmsg)
        elif l_topic == 'irrigation':
            l_logmsg += irrigationMqtt(self.m_pyhouse_obj).decode(p_topic[1:], p_message, l_logmsg)
        elif l_topic == 'lighting':
            l_logmsg += lightingMqtt(self.m_pyhouse_obj).decode(p_topic[1:], p_message, l_logmsg)
        elif l_topic == 'schedule':
            l_logmsg = scheduleMqtt(self.m_pyhouse_obj).decode(p_topic[1:], p_message, l_logmsg)
        elif l_topic == 'outlet':
            l_logmsg = outletMqtt(self.m_pyhouse_obj).decode(p_topic[1:], p_message, l_logmsg)
        else:
            l_logmsg += '\tUnknown sub-topic {}'.format(p_message)
            LOG.warn('Unknown House Topic: {}\n\tTopic: {}\n\tMessge: {}'.format(p_topic[0], p_topic, p_message))
        return l_logmsg


class Utility:
    """
    """

    m_config_tools = None
    m_import_tools = None
    m_part_needed = []
    m_module_needed = []
    m_pyhouse_obj = None

    def __init__(self, p_pyhouse_obj):
        """
        """
        self.m_pyhouse_obj = p_pyhouse_obj
        self.m_config_tools = config_tools.Yaml(p_pyhouse_obj)
        self.m_import_tools = import_tools.Tools(p_pyhouse_obj)

    def XXXinit_all_house_parts(self, p_parts):
        """
        """
        l_dict = {}
        for l_part in p_parts:
            l_name = l_part.lower()
            # LOG.debug('Working on part {}'.format(l_part))
            l_api = self.m_import_tools.import_module_get_api(l_part, 'Modules.House')
            LOG.info('Inported house part "{}"'.format(l_part))
            l_dict[l_name] = l_api
        LOG.info('Initialized House Parts {}'.format(l_dict))
        return l_dict

    def _find_all_configed_parts(self, p_parts):
        """ Find all house modules that have a "module".yaml config file somewhere in /etc/pyhouse.
        """
        for l_part in p_parts:
            l_path = self.m_config_tools.find_config_file(l_part.lower())
            if l_path != None:
                self.m_part_needed.append(l_part)
                LOG.info(' Found  config file for "{}"'.format(l_part))
            else:
                LOG.info('Missing config file for "{}"'.format(l_part))
        LOG.info('Found config files for: {}'.format(self.m_part_needed))
        return self.m_part_needed  # for debugging

    def _import_all_found_parts(self, p_parts):
        """ Now we know what we need, load and run just those modules.
        """
        l_parts = {}
        l_path = 'Modules.House'
        for l_part in p_parts:
            # LOG.debug('Starting import of Part: "{}"'.format(l_part))
            l_api = self.m_import_tools.import_module_get_api(l_part, l_path)
            l_parts[l_part] = l_api
        LOG.info('Loaded Modules: {}'.format(self.m_module_needed))
        return l_parts

    def load_all_house_parts(self, p_parts):
        """
        """
        LOG.info('Loading parts config files')
        for l_key, l_value in p_parts.items():
            LOG.info('Loading house part "{}"'.format(l_key))
            l_value.LoadConfig()
        LOG.info('Loaded all House Parts {}'.format(p_parts))

    def XXX_start_all_house_parts(self, p_parts):
        """ Family must start before the other things (that depend on family).
        """
        LOG.info('Starting parts config files')
        for l_key, l_value in p_parts.items():
            LOG.info('Starting house part "{}"'.format(l_key))
            l_value.Api.Start()
        LOG.info('Finished loading all house parts config files.')

    def _find_all_configed_modules(self, p_modules):
        """ Find all house modules that have a "module".yaml config file somewhere in /etc/pyhouse.
        @return: a list of required modules per the config files
        """
        for l_module in p_modules:
            l_name = l_module.lower()
            l_path = self.m_config_tools.find_config_file(l_name)
            if l_path != None:
                self.m_module_needed.append(l_module)
                LOG.info(' Found  config file for "{}"'.format(l_module))
            else:
                LOG.info('Missing config file for "{}"'.format(l_module))
        # Add family - It is not configured but is derived from things configured.
        if 'Family' not in self.m_module_needed:
            self.m_module_needed.append('Family')
        LOG.info('Found config files for: {}'.format(self.m_module_needed))
        return self.m_module_needed  # for debugging

    def _import_all_found_modules(self, p_modules):
        """ Now we know what we need, load and run just those modules.
        """
        l_modules = {}
        l_house_path = 'Modules.House.'
        for l_module in p_modules:
            LOG.debug('Starting import of Module: "{}"'.format(l_module))
            l_path = l_house_path + l_module.capitalize()
            l_api = self.m_import_tools.import_module_get_api(l_module, l_path)
            l_modules[l_module] = l_api
        LOG.info('Found Modules: {}'.format(self.m_module_needed))
        self.m_pyhouse_obj.House.Module = l_modules
        return l_modules

    def load_all_modules(self, p_modules):
        """ Load the config file for all the components of the house.
        """
        # LOG.debug(PrettyFormatAny.form(p_modules, 'Modules'))
        for l_module in p_modules.values():
            l_module.LoadConfig()

    def XXX_save_component_apis(self):
        """ These are sub-module parts of the house.
        """
        l_obj = self.m_pyhouse_obj.House
        for l_key in [l_attr for l_attr in dir(l_obj) if not l_attr.startswith('_') and not callable(getattr(l_obj, l_attr))]:
            l_a = getattr(l_obj, l_key)
            if l_key == 'HouseApi':
                continue
            if l_a == None:
                LOG.warn('Skipping "{}"'.format(l_key))
                continue
            l_a.SaveConfig()
        return

    def start_house_modules(self, p_modules):
        """ Family must start before the other things (that depend on family).
        """
        # LOG.debug('Starting configured modules: {}'.format(p_modules))
        for l_module in p_modules.values():
            LOG.debug('Starting configured module: {}'.format(l_module))
            l_module.Start()

    def save_house_modules(self):
        pass

    def stop_house_modules(self):
        l_obj = self.m_pyhouse_obj.House
        for l_key in [l_attr for l_attr in dir(l_obj) if not l_attr.startswith('_') and not callable(getattr(l_obj, l_attr))]:
            l_a = getattr(l_obj, l_key)
            if l_key == 'HouseApi':
                continue
            if l_a == None:
                LOG.warn('Skipping "{}"'.format(l_key))
                continue
            l_a.Stop()
        return
        self.m_pyhouse_obj.House.EntertainmentApi.Stop()
        self.m_pyhouse_obj.House.ScheduleApi.Stop()

    def save_house_parts(self, p_parts_dict):
        LOG.info('Saving parts config files')
        for l_key, l_value in p_parts_dict.items():
            LOG.info('Starting House part "{}"'.format(l_key))
            l_value.Api.SaveConfig()

    def stop_house_parts(self, p_parts_dict):
        LOG.info('Stopping parts config files')
        for l_key, l_value in p_parts_dict.items():
            LOG.info('Stopping house part "{}"'.format(l_key))
            l_value.Api.Stop()


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


class Api:
    """
    """
    m_local_config = None
    m_pyhouse_obj = None
    m_utility = None
    m_parts = {}
    m_modules = {}

    def __init__(self, p_pyhouse_obj):
        """ **NoReactor**
        This is part of Core PyHouse - House is the reason we are running!
        Note that the reactor is not yet running.
        """
        LOG.info('Initializing - Version:{}'.format(__version__))
        self.m_pyhouse_obj = p_pyhouse_obj
        self.m_local_config = LocalConfig(p_pyhouse_obj)
        self.m_utility = Utility(p_pyhouse_obj)
        #
        self._add_storage()
        #
        l_parts = self.m_utility._find_all_configed_parts(PARTS)
        self.m_parts = self.m_utility._import_all_found_parts(l_parts)
        #
        l_modules = self.m_utility._find_all_configed_modules(MODULES)
        self.m_modules = self.m_utility._import_all_found_modules(l_modules)
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
        self.m_utility.load_all_house_parts(self.m_parts)
        self.m_utility.load_all_modules(self.m_modules)
        LOG.info('Loaded Config')
        return

    def Start(self):
        """Start processing for all things house.
        May be stopped and then started anew to force reloading info.
        """
        LOG.info("Starting")
        self.m_utility.start_house_modules(self.m_modules)
        LOG.info('Started House "{}"'.format(self.m_pyhouse_obj.House.Name))

    def SaveConfig(self):
        """
        Take a snapshot of the current Configuration/Status and write out the config files.
        """
        LOG.info('Saving Config - Version:{}'.format(__version__))
        self.m_utility.save_house_parts(self.m_parts)
        self.m_utility.save_house_modules(self.m_modules)
        LOG.info("Saved Config.")
        return

    def Stop(self):
        """ Stop all house stuff.
        """
        LOG.info("Stopping House.")
        self.m_utility.stop_house_parts(self.m_parts)
        self.m_utility.stop_house_modules()
        LOG.info("Stopped.")
        _x = PrettyFormatAny.form(self.m_pyhouse_obj, 'PyHouse_obj')

#  ##  END DBK
