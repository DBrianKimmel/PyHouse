"""
@name:      Modules/Core/core.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2014-2020 by D. Brian Kimmel
@note:      Created on Mar 1, 2014
@license:   MIT License
@summary:   This module sets up the Core part of PyHouse.

In addition to the 'Core' PyHouse system has two parts.
The first part is the 'Computer'.
    It deals with things that pertain to the computer (this one).
    There can be one or more computers running PyHouse.
    Each computer can control two or more control devices.

The second part is the 'House'.
    There is only one house associated with the PyHouse program.
    Every system and sub-system that pertains to the house being automated is here.

This will set up this node and then find all other nodes in the same domain (House).
Then start the House and all the sub systems.
"""

__updated__ = '2020-02-17'
__version_info__ = (20, 2, 17)
__version__ = '.'.join(map(str, __version_info__))

#  Import system type stuff
from twisted.internet import reactor

#  Import PyMh files and modules.
from Modules.Core import setup_logging  # This must be first as the import causes logging to be initialized
from Modules.Core import MODULES, CONFIG_NAME, \
    PyHouseInformation, \
    CoreInformation, \
    CoreComponentInformation, \
    CoreModuleInformation, \
    ParameterInformation, \
    TwistedInformation, PARTS
from Modules.Core.Config.config_tools import Api as configApi

from Modules.Core.Utilities.debug_tools import PrettyFormatAny

from Modules.Core import logging_pyh as Logger
LOG = Logger.getLogger('PyHouse.Core           ')

MINUTES = 60  # Seconds in a minute
HOURS = 60 * MINUTES
INITIAL_DELAY = 3 * MINUTES
SAVE_DELAY = 3 * HOURS
MIN_CONFIG_VERSION = 2.0


class Utility:
    """
    """

    m_config_tools = None
    m_pyhouse_obj = None
    m_component_api = {}
    m_module_api = {}

    def __init__(self, p_pyhouse_obj):
        self.m_pyhouse_obj = p_pyhouse_obj
        self.m_config_tools = configApi(p_pyhouse_obj)

    def _initialize_one_item(self, p_item, p_path):
        """
        """
        # LOG.debug('Importing: "{}", "{}"'.format(p_item, p_path))
        l_path = p_path + p_item
        l_api = self.m_config_tools.import_module_get_api(p_item.lower(), l_path)
        return l_api

    def initialize_core_items(self, p_modules, p_path):
        """ set up all the modules we need
        @param p_modules: is a list of required modules.
        """
        l_apis = {}
        for l_module in p_modules:
            # LOG.debug('Initializing module "{}"'.format(l_module))
            l_apis[l_module.lower()] = self._initialize_one_item(l_module, p_path)
        return l_apis

# Parts

    def _initialize_one_part(self, p_component):
        """ Components (House, Computer)
        """
        l_path = 'Modules.' + p_component
        LOG.debug('Importing: "{}", "{}"'.format(p_component.lower(), l_path))
        l_api = self.m_config_tools.import_module_get_api(p_component, l_path)
        LOG.warning(PrettyFormatAny.form(self.m_module_api, 'Modules'))
        # self.m_module_api['mqtt'].AddDispatchApi(l_api)
        return l_api

    def initialize_all_components(self, p_components):
        """ Now set up the main components (computer, house)
        """
        l_components = {}
        for l_component in p_components:
            # LOG.debug('Loading component "{}"'.format(l_component))
            l_comp = self._initialize_one_component(l_component)
            l_components[l_component] = l_comp
        # LOG.debug('Set up components {}'.format(l_components))
        self.m_component_api = l_components
        return l_components

    def _load_one_component(self, p_component):
        """
        """
        p_component.LoadConfig()

    def load_all_components(self):
        """
        """
        # LOG.debug(PrettyFormatAny.form(p_components, 'Components'))
        for l_component in self.m_component_api.values():
            LOG.info('Loading core component "{}"'.format(l_component))
            self._load_one_component(l_component)

    def _start_one_component(self, p_component):
        """
        """
        p_component.Start()

    def start_all_components(self):
        """
        """
        # LOG.debug(PrettyFormatAny.form(p_components, 'Components'))
        for l_component in self.m_component_api.values():
            # LOG.debug('Starting component "{}"'.format(l_component))
            _l_comp = self._start_one_component(l_component)

    def save_all_components(self):
        """
        """
        LOG.info('\n======================== Saving Config Files ========================\n')
        for l_key, l_component in self.m_component_api.items():
            LOG.info('Saving component "{}"'.format(l_key))
            l_component.SaveConfig()
        LOG.info('\n======================== Saved Config Files ========================\n')

    def _config_save_loop(self, p_pyhouse_obj):
        p_pyhouse_obj._Twisted.Reactor.callLater(SAVE_DELAY, self.save_all_components)
        self.save_all_components()


class LocalConfig:
    """
    """
    m_pyhouse_obj = None
    m_config = None

    def __init__(self, p_pyhouse_obj):
        """
        """
        self.m_pyhouse_obj = p_pyhouse_obj
        self.m_config = configApi(p_pyhouse_obj)

    def _extract_pyhouse_info(self, p_config):
        """
        """
        l_required = ['Name', 'Units', 'Version']
        l_obj = ParameterInformation()
        for l_key, l_value in p_config.items():
            if l_key == 'units':
                l_value = l_value.lower()
            elif l_key == 'version':
                if l_value < MIN_CONFIG_VERSION:
                    LOG.warning('Configuration version is too low.  Some things may have changed.')
            setattr(l_obj, l_key, l_value)
        for l_key in [l_attr for l_attr in dir(l_obj) if not l_attr.startswith('_') and not callable(getattr(l_obj, l_attr))]:
            if getattr(l_obj, l_key) == None and l_key in l_required:
                LOG.warning('pyhouse.yaml is missing an entry for "{}"'.format(l_key))
        return l_obj

    def load_yaml_config(self):
        """ Read the pyhouse.yaml file.
        """
        LOG.info('Loading Config - Version:{}'.format(__version__))
        self.m_pyhouse_obj._Parameters = ParameterInformation()
        l_yaml = self.m_config.read_config_file(CONFIG_NAME)
        if l_yaml == None:
            LOG.error('{}.yaml is missing.'.format(CONFIG_NAME))
            return None
        try:
            l_yaml = l_yaml['PyHouse']
        except:
            LOG.warning('The config file does not start with "PyHouse:"')
            return None
        # LOG.debug('Yaml: {}'.format(l_yaml))
        l_parameter = self._extract_pyhouse_info(l_yaml)
        self.m_pyhouse_obj._Parameters = l_parameter
        # LOG.debug(PrettyFormatAny.form(self.m_pyhouse_obj, 'PyHouse'))
        return l_parameter  # for testing purposes


class Api:
    """
    Called from PyHouse.py
    """
    m_modules_api = None  # Modules actually installed
    m_local_config = None
    m_pyhouse_obj = None
    m_utility = None  # Pointer

    def __init__(self):
        """ **NOR**
        Note that the reactor is *NOT* yet running.
        """
        LOG.info("\n======================== Initializing ======================== Version: {}\n".format(__version__))
        setup_logging.Api()
        LOG.info('Setting up Main Data areas')
        self.m_pyhouse_obj = PyHouseInformation()
        self._add_storage()

    def _init_core(self):
        """ Broken up so we can test parts without the whole of PyHouse being running
        """
        # Initialize classes
        self.m_utility = Utility(self.m_pyhouse_obj)
        self.m_local_config = LocalConfig(self.m_pyhouse_obj)
        self.m_local_config.load_yaml_config()
        # First, start the modules that are used by the major parts (House, Computer)
        self.m_modules_api = self.m_utility.initialize_core_items(MODULES, 'Modules.Core.')
        self.m_modules_api = self.m_utility.initialize_core_items(PARTS, 'Modules.')
        #
        self.m_pyhouse_obj._Twisted.Reactor.callWhenRunning(self.LoadConfig)
        LOG.info("\n======================== Initialized ======================== Version: {}\n".format(__version__))
        LOG.info('Starting Reactor...')
        self.m_pyhouse_obj._Twisted.Reactor.run()  # reactor never returns so must be last - Event loop will now run
        LOG.info("PyHouse says Bye Now.\n")
        print('PyHouse is exiting.')
        raise SystemExit("PyHouse says Bye Now.")

    def _add_storage(self):
        self.m_pyhouse_obj.Core = CoreInformation()
        self.m_pyhouse_obj.Core.Components = CoreComponentInformation()
        self.m_pyhouse_obj.Core.Modules = CoreModuleInformation()
        self.m_pyhouse_obj._Config = {}
        self.m_pyhouse_obj._Parameters = None
        self.m_pyhouse_obj._Twisted = TwistedInformation()
        self.m_pyhouse_obj._Twisted.Reactor = reactor

    def LoadConfig(self):
        """ Load in the entire configuration for PyHouse.
        This will fill in pyhouse_obj for all defined features of PyHouse.
        """
        LOG.info("\n======================== Loading Config Files ======================== Version: {}\n".format(__version__))
        #
        for _l_key, l_module in self.m_modules_api.items():
            l_module.LoadConfig()
        for l_module in self.m_modules_api.values():
            l_module.Start()

        self.m_utility.load_all_components()
        # LOG.debug(PrettyFormatAny.form(self.m_pyhouse_obj.Core.Config, 'Config'))
        # LOG.debug(PrettyFormatAny.form(self.m_pyhouse_obj.Core.Config['schedule']))
        LOG.info("Loaded Config")
        self.m_pyhouse_obj._Twisted.Reactor.callLater(2, self.Start)
        LOG.info("\n======================== Loaded Config Files ======================== Version: {}\n".format(__version__))

    def Start(self):
        """
        The reactor is now running.
        @param p_pyhouse_obj: is the skeleton Obj filled in some by PyHouse.py.
        """
        print('Reactor is now running.')
        LOG.info("\n======================== Starting ======================== Version: {}\n".format(__version__))
        LOG.info('Starting - Reactor is now running.')
        self.m_utility.start_all_components()
        self.m_pyhouse_obj._Twisted.Reactor.callLater(INITIAL_DELAY, self.m_utility._config_save_loop, self.m_pyhouse_obj)
        LOG.info("\n======================== Started ======================== Version: {}\n".format(__version__))
        LOG.info("\n======================== Opperational ========================")

    def SaveConfig(self):
        """
        Take a snapshot of the current Configuration/Status and write out into config files.
        The XML file is a single large file containing everything.
        The Yaml config is broken down into many smaller files and written by each component.
        """
        self.m_utility.save_all_components()

    def Stop(self):
        l_topic = 'computer/shutdown'
        self.m_pyhouse_obj.Core.MqttApi.MqttPublish(l_topic, self.m_pyhouse_obj.Computer.Nodes[self.m_pyhouse_obj.Computer.Name])
        self.SaveConfig()
        LOG.info("Stopped.\n==========\n")
        _x = PrettyFormatAny.form(self.m_pyhouse_obj, 'PyHouse_obj')

    def Publish(self, p_topic, p_body):
        """ Central point to publish a PyHouse message.

        Currently, Mqtt is used as the transport mechanism to carry the message.
        @param p_topic: is the topic of the message (See: Modules/Core/xxx/Design.md for the allowed topics.
        @param p_body: is the body of the message - JSON format
        """
        LOG.debug('"{}" "{}"'.format(p_topic, p_body))
        LOG.debug(PrettyFormatAny.form(self.m_pyhouse_obj.Core.Mqtt, 'Mqtt'))
        LOG.debug(PrettyFormatAny.form(self.m_pyhouse_obj.Core.Mqtt._Api, 'Mqtt._Api'))
        self.m_pyhouse_obj.Core.Mqtt._Api.MqttPublish(p_topic, p_body)
        LOG.debug(PrettyFormatAny.form(self.m_pyhouse_obj.Core.Mqtt, 'Mqtt'))

# ## END DBK
