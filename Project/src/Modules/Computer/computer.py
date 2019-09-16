"""
@name:      Modules/Computer/computer.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2014-2019 by D. Brian Kimmel
@note:      Created on Jun 24, 2014
@license:   MIT License
@summary:   Handle the computer information.

This handles the Computer part of the node.  (The other part is "House").

"""

__updated__ = '2019-09-12'
__version_info__ = (19, 5, 1)
__version__ = '.'.join(map(str, __version_info__))

#  Import system type stuff
from datetime import datetime
import platform
import importlib

#  Import PyHouse files
from Modules.Core.Config import config_tools
from Modules.Core.Utilities import extract_tools, uuid_tools
from Modules.Computer.Nodes.nodes import MqttActions as nodesMqtt

from Modules.Core.Utilities.debug_tools import PrettyFormatAny

from Modules.Core import logging_pyh as Logger
LOG = Logger.getLogger('PyHouse.Computer       ')

CONFIG_NAME = 'computer'
MODULES = [  # All modules for the computer must be listed here.  They will be loaded if configured.
    'Bridges',
    'Communication',
    'Internet',
    'Node',
    'Pi',
    # 'Weather',
    'Web'
    ]
PARTS = [
    ]


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
        self.Bridges = {}  # BridgeInformation() in Modules.Computer.Bridges.bridge_data
        self.Communication = {}  # CommunicationInformation()
        self.InternetConnection = {}  # InternetConnectionInformation()
        self.Nodes = {}  # NodeInformation()
        self.Weather = {}  # WeatherInformation()
        self.Web = {}  # WebInformation()


class ComputerAPIs:
    """
    ==> PyHouse._APIs.Computer.xxx as in the def below.

    """

    def __init__(self):
        pass
        # self.BridgesAPI = None
        # self.ComputerAPI = None
        # self.CommAPIs = None  # CommunicationAPIs()
        # self.InternetAPI = None
        # self.NodesAPI = None
        # self.WeatherAPI = None
        # self.WebAPI = None
        # self.WebSocketAPI = None


class MqttActions:
    """
    """

    def __init__(self, p_pyhouse_obj):
        self.m_pyhouse_obj = p_pyhouse_obj

    def decode(self, p_topic, p_message):
        """ Decode the computer specific portions of the message and append them to the log string.
        @param p-logmsg: is the partially decoded Mqtt message json
        @param p_topic: is a list of topic part strings ( pyhouse, housename have been dropped
        @param p_message: is the payload that is JSON
        """
        l_logmsg = '\tComputer:\n'
        if p_topic[0] == 'browser':
            l_logmsg += '\tBrowser: Message {}'.format(PrettyFormatAny.form(p_message, 'Computer msg', 160))
        elif p_topic[0] == 'node' or p_topic[0] == 'nodes':
            l_logmsg += nodesMqtt(self.m_pyhouse_obj).decode(p_topic[1:], p_message, l_logmsg)
        #  computer/ip
        elif p_topic[1] == 'ip':
            l_ip = extract_tools.get_mqtt_field(p_message, 'ExternalIPv4Address')
            l_logmsg += '\tIPv4: {}'.format(l_ip)
        #  computer/startup
        elif p_topic[1] == 'startup':
            self._extract_node(p_message)
            l_logmsg += '\tStartup {}'.format(PrettyFormatAny.form(p_message, 'Computer msg', 160))
            if self.m_myname == self.m_sender:
                l_logmsg += '\tMy own startup of PyHouse\n'
            else:
                l_logmsg += '\tAnother computer started up: {}'.format(self.m_sender)
        #  computer/shutdown
        elif p_topic[1] == 'shutdown':
            del self.m_pyhouse_obj.Computer.Nodes[self.m_name]
            l_logmsg += '\tSelf Shutdown {}'.format(PrettyFormatAny.form(p_message, 'Computer msg', 160))
        #  computer/***
        else:
            l_logmsg += '\tUnknown sub-topic {}'.format(PrettyFormatAny.form(p_message, 'Computer msg', 160))
        return l_logmsg


class Config:
    """
    """

    m_config_tools = None
    m_pyhouse_obj = None

    def __init__(self, p_pyhouse_obj):
        self.m_pyhouse_obj = p_pyhouse_obj
        self.m_config_tools = config_tools.Yaml(p_pyhouse_obj)
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
        LOG.debug('Starting ')
        self.m_config_tools.find_config_file(CONFIG_NAME)

        LOG.debug('New start of config loading...')
        try:
            l_node = config_tools.Yaml(self.m_pyhouse_obj).read_yaml(CONFIG_NAME)
        except:
            return None
        try:
            l_yaml = l_node.Yaml['Computer']
        except:
            LOG.warn('The computer.yaml file does not start with "Computer:"')
            return None
        _l_computer = self._extract_computer_info(l_yaml)
        # self.m_pyhouse_obj.House.Name = l_house.Name
        # l_obj = self.m_pyhouse_obj.Computer
        # LOG.debug('Computer.Yaml - {}'.format(l_yaml.Yaml))
        return l_node  # for testing purposes


class lightingUtility:
    """
    There are currently (2019) 8 components - be sure all are in every method.
    """

    m_config_tools = None
    m_module_needed = ['Nodes']
    m_pyhouse_obj = None

    def __init__(self, p_pyhouse_obj):
        """
        """
        self.m_pyhouse_obj = p_pyhouse_obj
        self.m_config_tools = config_tools.Yaml(p_pyhouse_obj)

    def _find_all_configed_modules(self):
        """ Find all computer modules that have a "module".yaml config file in /etc/pyhouse.
        Build the m_module_needed list.
        """
        # LOG.debug('Progress')
        for l_module in MODULES:
            l_path = self.m_config_tools.find_config_file(l_module.lower())
            if l_path != None:
                self.m_module_needed.append(l_module)
                LOG.debug('Found Computer config file "{}"'.format(l_path))
        LOG.info('Found config files for: {}'.format(self.m_module_needed))
        return self.m_module_needed  # for debugging

    def _import_all_found_modules(self):
        """
        """
        for l_module in self.m_module_needed:
            l_package = 'Modules.Computer.' + l_module.capitalize()  # p_family_obj.PackageName  # contains e.g. 'Modules.Families.Insteon'
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
                LOG.error('ERROR - Module: {}\n\t{}'.format(l_module, e_err))
                LOG.error('Ref: {}'.format(PrettyFormatAny.form(l_ret, 'ModuleRef', 190)))
                l_api = None
            l_api_name = l_module.capitalize() + 'API'
            l_computer = self.m_pyhouse_obj._APIs.Computer
            setattr(l_computer, l_api_name, l_api)
        # LOG.debug(PrettyFormatAny.form(self.m_module_needed, 'Modules', 190))
        LOG.info('Loaded Modules: {}'.format(self.m_module_needed))

    def _init_component_apis(self, p_pyhouse_obj, _p_computer_api):
        """
        Initialize all the computer division APIs
        """
        p_pyhouse_obj._APIs.Computer = ComputerAPIs()

    def _load_component_config(self):
        l_obj = self.m_pyhouse_obj._APIs.Computer
        for l_key in [l_attr for l_attr in dir(l_obj) if not l_attr.startswith('_') and not callable(getattr(l_obj, l_attr))]:
            l_a = getattr(l_obj, l_key)
            if l_key == 'ComputerAPI':
                continue
            l_a.LoadConfig()

    def _start_component_apis(self):
        l_obj = self.m_pyhouse_obj._APIs.Computer
        for l_key in [l_attr for l_attr in dir(l_obj) if not l_attr.startswith('_') and not callable(getattr(l_obj, l_attr))]:
            l_a = getattr(l_obj, l_key)
            if l_key == 'ComputerAPI':
                continue
            l_a.Start()

    def _stop_component_apis(self):
        l_obj = self.m_pyhouse_obj._APIs.Computer
        for l_key in [l_attr for l_attr in dir(l_obj) if not l_attr.startswith('_') and not callable(getattr(l_obj, l_attr))]:
            l_a = getattr(l_obj, l_key)
            if l_key == 'ComputerAPI':
                continue
            l_a.Stop()

    def _save_component_apis(self):
        l_obj = self.m_pyhouse_obj._APIs.Computer
        for l_key in [l_attr for l_attr in dir(l_obj) if not l_attr.startswith('_') and not callable(getattr(l_obj, l_attr))]:
            l_a = getattr(l_obj, l_key)
            if l_key == 'ComputerAPI':
                continue
            l_a.SaveConfig()


class API:
    """
    """

    m_config = None
    m_config_tools = None
    m_pyhouse_obj = None
    m_utility = None

    def __init__(self, p_pyhouse_obj):
        """ Initialize the computer section of PyHouse.
        """
        LOG.info("Initializing - Version:{}".format(__version__))
        self.m_pyhouse_obj = p_pyhouse_obj
        self.m_config = Config(p_pyhouse_obj)
        self.m_config_tools = config_tools.Yaml(p_pyhouse_obj)
        self.m_utility = lightingUtility(p_pyhouse_obj)

        # This overrides any config saved so we can start Logging and MQTT messages early on.
        p_pyhouse_obj.Computer = ComputerInformation()
        p_pyhouse_obj.Computer.Name = platform.node()
        p_pyhouse_obj.Computer.Key = 0
        p_pyhouse_obj.Computer.UUID = uuid_tools.get_uuid_file(p_pyhouse_obj, CONFIG_NAME)
        p_pyhouse_obj.Computer.Comment = ''
        p_pyhouse_obj.Computer.LastUpdate = datetime.now()
        self.m_utility._init_component_apis(p_pyhouse_obj, self)

        self.m_utility._find_all_configed_modules()
        self.m_utility._import_all_found_modules()

        LOG.info("Initialized - Version:{}".format(__version__))

    def LoadConfig(self):
        """
        """
        LOG.info('Loading Config - Version:{}'.format(__version__))
        self.m_config.load_yaml_config()
        self.m_utility._load_component_config()
        LOG.info('Loaded Config.')

    def Start(self):
        """
        Start processing
        """
        LOG.info('Starting')
        self.m_utility._start_component_apis()
        LOG.info('Started.')

    def SaveConfig(self):
        """
        Take a snapshot of the current Configuration/Status and write out an XML file.
        """
        self.m_utility._save_component_apis()
        LOG.info("Saved Computer XML Config.")
        return

    def Stop(self):
        """
        Append the house XML to the passed in xlm tree.
        """
        self.m_utility._stop_component_apis()
        LOG.info("Stopped.")

    def DecodeMqtt(self, p_topic, p_message):
        """ Decode messages sent to the computer module.
        """
        # LOG.debug('\n==Topic: {}\n==Message: {}\n==LogMsg: {}'.format(p_topic, p_message, p_logmsg))
        l_logmsg = MqttActions(self.m_pyhouse_obj).decode(p_topic, p_message)
        return l_logmsg

# ## END DBK
