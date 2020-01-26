"""
@name:      Modules/Computer/computer.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2014-2020 by D. Brian Kimmel
@note:      Created on Jun 24, 2014
@license:   MIT License
@summary:   Handle the computer information.

This handles the Computer part of the node.  (The other part is "House").

"""

__updated__ = '2020-01-25'
__version_info__ = (19, 10, 5)
__version__ = '.'.join(map(str, __version_info__))

#  Import system type stuff
from datetime import datetime
import platform

#  Import PyHouse files
from Modules.Core.Config.config_tools import Api as configApi
from Modules.Core.Utilities import extract_tools, uuid_tools
from Modules.Computer.Nodes.nodes import MqttActions as nodesMqtt
from Modules.Computer.__init__ import MODULES, PARTS

from Modules.Core.Utilities.debug_tools import PrettyFormatAny

from Modules.Core import logging_pyh as Logger
LOG = Logger.getLogger('PyHouse.Computer       ')

CONFIG_NAME = 'computer'


class ComputerInformation:
    """
    ==> PyHouse.Computer.xxx - as in the def below.
    """

    def __init__(self):
        self.Name = None
        self.Comment = None
        self.UUID = None
        self.Primary = False
        self.Priority = 99
        self.Bridges = {}  # BridgeInformation() in Modules.Computer.Bridges.bridges.py
        self.Communication = {}  # CommunicationInformation()
        self.Internet = {}  # InternetInformation()
        self.Nodes = {}  # Node Information()
        self.Weather = {}  # WeatherInformation()
        self.Web = {}  # WebInformation()


class ComputerApis:
    """
    ==> PyHouse.Computer.xxx as in the def below.

    """

    def __init__(self):
        pass


class MqttActions:
    """
    """

    def __init__(self, p_pyhouse_obj):
        self.m_pyhouse_obj = p_pyhouse_obj

    def decode(self, p_msg):
        """ Decode the computer specific portions of the message and append them to the log string.
        @param p_message: is the payload that is JSON
        """
        p_msg.LogMessage += '\tComputer:\n'
        l_topic = p_msg.UnprocessedTopic[0].lower()
        p_msg.UnprocessedTopic = p_msg.UnprocessedTopic[1:]
        if l_topic == 'node':
            nodesMqtt(self.m_pyhouse_obj).decode(p_msg)
        else:
            p_msg.LogMessage += '\tUnknown sub-topic {}'.format(PrettyFormatAny.form(p_msg.Payload, 'Computer msg'))
            LOG.error(p_msg.LogMessage)


class Utility:
    """
    There are currently (2019) 8 components - be sure all are in every method.
    """

    m_pyhouse_obj = None

    def __init__(self, p_pyhouse_obj):
        """
        """
        self.m_pyhouse_obj = p_pyhouse_obj

    def load_module_config(self, p_modules):
        # LOG.debug('Loading Componente')
        for l_module in p_modules.values():
            l_module.LoadConfig()


class LocalConfig:
    """
    """

    m_config_tools = None
    m_pyhouse_obj = None

    def __init__(self, p_pyhouse_obj):
        self.m_pyhouse_obj = p_pyhouse_obj
        self.m_config_tools = configApi(p_pyhouse_obj)
        # LOG.debug('Config - Progress')

    def _extract_computer_info(self, _p_config):
        """ The cpmputer.yamll file only contains module names to force load.

        @param p_pyhouse_obj: is the entire house object
        @param p_config: is the modules to force load.
        """
        l_modules = []
        # for l_ix, l_config in enumerate(p_config):
        #    pass
        return l_modules  # For testing.

    def load_yaml_config(self):
        """ Read the config file.
        """
        LOG.info('Loading Config - Version:{}'.format(__version__))
        # self.m_pyhouse_obj.Computer = None
        l_yaml = self.m_config_tools.read_config_file(CONFIG_NAME)
        if l_yaml == None:
            LOG.error('{}.yaml is missing.'.format(CONFIG_NAME))
            return None
        try:
            l_yaml = l_yaml['Computer']
        except:
            LOG.warning('The config file does not start with "Computer:"')
            return None
        l_computer = self._extract_computer_info(l_yaml)
        # self.m_pyhouse_obj.Computer = l_computer
        # LOG.debug('Computer.Yaml - {}'.format(l_yaml.Yaml))
        return l_computer


class Api:
    """
    """

    m_config_tools = None
    m_local_config = None
    m_found_modules_apis = {}
    m_module_list = None
    m_pyhouse_obj = None

    def __init__(self, p_pyhouse_obj):
        """ Initialize the computer section of PyHouse.
        """
        LOG.info('Initializing')
        self.m_pyhouse_obj = p_pyhouse_obj
        self._add_storage()
        self.m_config_tools = configApi(p_pyhouse_obj)
        self.m_local_config = LocalConfig(p_pyhouse_obj)
        #
        l_path = 'Modules.Computer.'
        l_modules_list = self.m_config_tools.find_module_list(MODULES)
        self.m_found_modules_apis = self.m_config_tools.import_module_list(l_modules_list, l_path)
        #
        LOG.info("Initialized - Version:{}".format(__version__))

    def _add_storage(self):
        """
        """
        self.m_pyhouse_obj.Computer = ComputerInformation()
        self.m_pyhouse_obj.Computer.Name = platform.node()
        self.m_pyhouse_obj.Computer.Key = 0
        self.m_pyhouse_obj.Computer.UUID = uuid_tools.get_uuid_file(self.m_pyhouse_obj, CONFIG_NAME)
        self.m_pyhouse_obj.Computer.Comment = ''
        self.m_pyhouse_obj.Computer.LastUpdate = datetime.now()

    def LoadConfig(self):
        """
        """
        LOG.info('Loading Config - Version:{}'.format(__version__))
        self.m_local_config.load_yaml_config()
        for l_module in self.m_found_modules_apis.values():
            l_module.LoadConfig()
        LOG.info('Loaded all computer Configs.')

    def Start(self):
        """
        Start processing
        """
        for l_module in self.m_found_modules_apis.values():
            l_module.Start()
        LOG.info('Started.')

    def SaveConfig(self):
        """
        Take a snapshot of the current Configuration/Status and write out an XML file.
        """
        for l_module in self.m_found_modules_apis.values():
            l_module.SaveConfig()
        LOG.info("Saved Computer Config.")

    def Stop(self):
        """
        Append the house XML to the passed in xlm tree.
        """
        for l_module in self.m_found_modules_apis.values():
            l_module.Stop()
        LOG.info("Stopped.")

# ## END DBK
