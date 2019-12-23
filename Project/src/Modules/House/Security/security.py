"""
@name:      Modules/House/Security/security.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2015-2019 by D. Brian Kimmel
@license:   MIT License
@note:      Created on Jun 29, 2015
@Summary:

"""

__updated__ = '2019-12-23'
__version_info__ = (19, 11, 25)
__version__ = '.'.join(map(str, __version_info__))

# Import system type stuff

# Import PyMh files
from Modules.Core.Config.config_tools import Api as configApi
from Modules.Core.Utilities.extract_tools import get_mqtt_field
from Modules.Core.Utilities.debug_tools import PrettyFormatAny
from Modules.House.Security.__init__ import SecurityInformation, MODULES

from Modules.Core import logging_pyh as Logger
LOG = Logger.getLogger('PyHouse.Security       ')

CONFIG_NAME = 'security'


class MqttActions:
    """
    """

    def __init__(self, p_pyhouse_obj):
        self.m_pyhouse_obj = p_pyhouse_obj

    def decode(self, p_msg):
        """ Decode the Mqtt message
        ==> pyhouse/<house name>/security/<type>/<Name>
        <type> = garage door, motion sensor, camera
        """
        l_topic = p_msg.UnprocessedTopic
        p_msg.UnprocessedTopic = p_msg.UnprocessedTopic[1:]
        p_msg.LogMessage += '\tSecurity:\n'
        if l_topic[0] == 'garage_door':
            p_msg.LogMessage += '\tGarage Door: {}\n'.format(get_mqtt_field(p_msg.Payload, 'Name'))
        elif l_topic[0] == 'motion_detector':
            p_msg.LogMessage += '\tMotion Detector:{}\n\t{}'.format(get_mqtt_field(p_msg.Payload, 'Name'), get_mqtt_field(p_msg.Payload, 'Status'))
        else:
            p_msg.LogMessage += '\tUnknown sub-topic {}'.format(PrettyFormatAny.form(p_msg.Payload, 'Security msg', 160))


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

    m_config_tools = None
    m_local_config = None
    m_pyhouse_obj = None
    m_modules = {}

    def __init__(self, p_pyhouse_obj):
        LOG.info("Initializing - Version:{}".format(__version__))
        self.m_pyhouse_obj = p_pyhouse_obj
        self._add_storage()
        self.m_local_config = LocalConfig(p_pyhouse_obj)
        self.m_config_tools = configApi(p_pyhouse_obj)
        #
        l_path = 'Modules.House.Security'
        l_modules = self.m_config_tools.find_module_list(MODULES)
        self.m_modules = self.m_config_tools.import_module_list(l_modules, l_path)
        #
        # l_needed_list = self.m_utility._find_all_configed_modules(MODULES)
        # self.m_modules = self.m_utility._import_all_found_modules(l_needed_list)
        LOG.info('Initialized')

    def _add_storage(self):
        self.m_pyhouse_obj.House.Security = SecurityInformation()

    def LoadConfig(self):
        """ Load the Security Information
        """
        LOG.info('Loading Config')
        # LOG.debug(PrettyFormatAny.form(self.m_pyhouse_obj.House.Security, 'Security'))
        for l_module in self.m_modules.values():
            # LOG.debug(PrettyFormatAny.form(l_module, 'Module'))
            l_module.LoadConfig()
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
