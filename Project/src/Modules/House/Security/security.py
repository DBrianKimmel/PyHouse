"""
@name:      Modules/House/Security/security.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2015-2019 by D. Brian Kimmel
@license:   MIT License
@note:      Created on Jun 29, 2015
@Summary:

"""
from Modules.Core.Config import config_tools, import_tools

__updated__ = '2019-11-28'
__version_info__ = (19, 11, 25)
__version__ = '.'.join(map(str, __version_info__))

# Import system type stuff

# Import PyMh files
from Modules.Core.Config.config_tools import Api as configApi
from Modules.Core.Utilities.extract_tools import get_mqtt_field
from Modules.Core.Utilities.debug_tools import PrettyFormatAny

from Modules.Core import logging_pyh as Logger
LOG = Logger.getLogger('PyHouse.Security       ')

CONFIG_NAME = 'security'
# LOCATION = House.Security

MODULES = [  # All modules for the House must be listed here.  They will be loaded if configured.
    'Cameras',
    'Door_Bells',
    'Garage_Doors',
    'Motion_Detectors'
    ]


class SecurityData:
    """
    DeviceType = 3
    ==> PyHouse.House.Security.xxx as in the def below
    """

    def __init__(self):
        self.Cameras = {}
        self.Door_Bells = {}
        self.Garage_Doors = {}
        self.Motion_Detectors = {}


class MqttActions:
    """
    """

    def __init__(self, p_pyhouse_obj):
        self.m_pyhouse_obj = p_pyhouse_obj

    def decode(self, p_topic, p_message):
        """ Decode the Mqtt message
        ==> pyhouse/<house name>/security/<type>/<Name>
        <type> = garage door, motion sensor, camera
        """
        l_logmsg = '\tSecurity:\n'
        if p_topic[0] == 'garage_door':
            l_logmsg += '\tGarage Door: {}\n'.format(get_mqtt_field(p_message, 'Name'))
        elif p_topic[0] == 'motion_detector':
            l_logmsg += '\tMotion Detector:{}\n\t{}'.format(get_mqtt_field(p_message, 'Name'), get_mqtt_field(p_message, 'Status'))
        else:
            l_logmsg += '\tUnknown sub-topic {}'.format(PrettyFormatAny.form(p_message, 'Security msg', 160))
        return l_logmsg


class Utility:
    """
    There are currently (2019) 8 components - be sure all are in every method.
    """

    m_config_tools = None
    m_import_tools = None
    m_modules_needed = []
    m_pyhouse_obj = None

    def __init__(self, p_pyhouse_obj):
        """
        """
        self.m_pyhouse_obj = p_pyhouse_obj
        self.m_config_tools = config_tools.Yaml(p_pyhouse_obj)
        self.m_import_tools = import_tools.Tools(p_pyhouse_obj)

    def _find_all_configed_modules(self, p_module_list):
        """ we don't want to import all modules, just the ones we have config files for.
        @param p_modules: is a list of possible modules.
        @return: A list of possible modules that has a config file
        """
        for l_module in p_module_list:
            # LOG.debug('Finding config for module "{}"'.format(l_module))
            l_path = self.m_config_tools.find_config_file(l_module.lower())
            if l_path != None:
                self.m_modules_needed.append(l_module)
                LOG.info('Found config file for "{}"'.format(l_module))
        LOG.info('Set up modules {}'.format(p_module_list))
        return self.m_modules_needed

    def _import_all_found_modules(self, p_modules):
        """
        @param p_modules: is a list of all needed modules
        """
        l_modules = {}
        l_path = 'Modules.House.Security'
        # LOG.debug('Needed Modules {}'.format(p_modules))
        for l_module in p_modules:
            l_api = self.m_import_tools.import_module_get_api(l_module, l_path)
            l_modules[l_module] = l_api
        LOG.info('Loaded Modules: {}'.format(self.m_modules_needed))
        return l_modules


class LocalConfig:
    """
    """

    m_config = None
    m_pyhouse_obj = None

    def __init__(self, p_pyhouse_obj):
        self.m_pyhouse_obj = p_pyhouse_obj
        self.m_config = configApi(p_pyhouse_obj)

    def import_all_modules(self, p_modules):
        """
        """
        for l_module in p_modules.values():
            l_module.LoadConfig()


class Api:
    """ Called from house.
    """

    m_local_config = None
    m_pyhouse_obj = None
    m_utility = None
    m_modules = {}

    def __init__(self, p_pyhouse_obj):
        LOG.info("Initializing - Version:{}".format(__version__))
        self.m_pyhouse_obj = p_pyhouse_obj
        self._add_storage()
        self.m_utility = Utility(p_pyhouse_obj)
        self.m_local_config = LocalConfig(p_pyhouse_obj)
        #
        l_needed_list = self.m_utility._find_all_configed_modules(MODULES)
        self.m_modules = self.m_utility._import_all_found_modules(l_needed_list)
        LOG.info('Initialized')

    def _add_storage(self):
        self.m_pyhouse_obj.House.Security = SecurityData()  # Clear before loading

    def LoadConfig(self):
        """ Load the Security Information
        """
        LOG.info('Loading Config')
        # self.m_local_config.import_all_modules(self.m_modules)
        LOG.info('Loaded Config')
        return self.m_pyhouse_obj.House.Security

    def Start(self):
        # self.m_api.Start()
        LOG.info("Started.")

    def SaveConfig(self):
        LOG.info("Saved Config.")

    def Stop(self):
        LOG.info("Stopped.")

# ## END DBK
