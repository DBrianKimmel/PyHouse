"""
@name:      Modules/Core/core.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2014-2019 by D. Brian Kimmel
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

__updated__ = '2020-01-07'
__version_info__ = (19, 10, 31)
__version__ = '.'.join(map(str, __version_info__))

#  Import system type stuff

#  Import PyMh files and modules.
from Modules.Core import setup_logging  # This must be first as the import causes logging to be initialized
from Modules.Core import setup_pyhouse_obj
from Modules.Core.Config.config_tools import Api as configApi

from Modules.Core.Utilities.debug_tools import PrettyFormatAny

from Modules.Core import logging_pyh as Logger
LOG = Logger.getLogger('PyHouse.Core           ')

MINUTES = 60  # Seconds in a minute
HOURS = 60 * MINUTES
INITIAL_DELAY = 3 * MINUTES
SAVE_DELAY = 3 * HOURS
CONFIG_DIR = '/etc/pyhouse/'
CONFIG_NAME = 'pyhouse'
MIN_CONFIG_VERSION = 2.0

# These components are required!
# We will load them whether they are configured or not.
COMPONENTS = [
    'Computer',
    'House'
    ]

# These modules are required!
# We will load them whether they are configured or not.
MODULES = [
    'Mqtt'
    ]


class CoreApiInformation:
    """
    """

    def __init__(self):
        self.MqttApi = None


class ParameterInformation:
    """
    ==> PyHouse._Parameters.xxx

    These are filled in first and hold things needed for early initialization.
    """

    def __init__(self):
        self.Name = 'Nameless House'
        self.Computer = 'Nameless'
        self.UnitSystem = 'Metric'
        self.ConfigVersion = 2.0


class PyHouseApiInformation:
    """
    ==> PyHouse.xxx

    Most of these have a single entry.
    """

    def __init__(self):
        self.Core = None  # CoreApiInformation()
        self.Computer = None
        self.House = None


class Utility:
    """
    """

    m_config_tools = None
    m_pyhouse_obj = None
    m_components = {}
    m_modules = {}

    def __init__(self, p_pyhouse_obj):
        self.m_pyhouse_obj = p_pyhouse_obj
        self.m_config_tools = configApi(p_pyhouse_obj)

    def _initialize_one_module(self, p_module):
        """
        """
        l_module = p_module.lower()
        l_path = 'Modules.Core.' + p_module
        # LOG.debug('Importing: "{}", "{}"'.format(l_module, l_path))
        l_module = self.m_config_tools.import_module_get_api(l_module, l_path)
        # LOG.debug('done')
        return l_module

    def initialize_core_modules(self, p_modules):
        """ set up all the modules we need
        @param p_modules: is a list of required modules.
        """
        l_modules = {}
        # LOG.debug('Initializing modules {}'.format(p_modules))
        for l_module in p_modules:
            # LOG.debug('Initializing module "{}"'.format(l_module))
            l_api = self._initialize_one_module(l_module)
            l_modules[l_module] = l_api
        LOG.info('Set up modules {}'.format(p_modules))
        self.m_modules = l_module
        return l_modules

    def load_core_modules(self, p_modules):
        """
        @param p_modules: is a dict of modules
        """
        for _l_key, l_module in p_modules.items():
            # LOG.debug('Loading module "{}"'.format(_l_key))
            # LOG.debug(PrettyFormatAny.form(l_module, 'Module'))
            l_module.LoadConfig()
            # LOG.debug('Loaded')

    def start_core_modules(self, p_modules):
        """
        """
        for l_module in p_modules.values():
            # LOG.debug('Starting module "{}"'.format(l_module))
            l_module.Start()

# Components

    def _initialize_one_component(self, p_component):
        l_path = 'Modules.' + p_component
        # LOG.debug('Importing: "{}", "{}"'.format(p_component.lower(), l_path))
        l_component = self.m_config_tools.import_module_get_api(p_component, l_path)
        return l_component

    def initialize_all_components(self, p_components):
        """ Now set up the main components (computer, house)
        """
        l_components = {}
        for l_component in p_components:
            # LOG.debug('Loading component "{}"'.format(l_component))
            l_comp = self._initialize_one_component(l_component)
            l_components[l_component] = l_comp
        # LOG.debug('Set up components {}'.format(l_components))
        self.m_components = l_components
        return l_components

    def _load_one_component(self, p_component):
        """
        """
        p_component.LoadConfig()

    def load_all_components(self):
        """
        """
        # LOG.debug(PrettyFormatAny.form(p_components, 'Components'))
        for l_component in self.m_components.values():
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
        for l_component in self.m_components.values():
            # LOG.debug('Starting component "{}"'.format(l_component))
            _l_comp = self._start_one_component(l_component)

    def save_all_components(self):
        """
        """
        LOG.info('\n======================== Saving Config Files ========================\n')
        for l_key, l_component in self.m_components.items():
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
    m_modules = None  # Modules actually installed
    m_components = None  # Components actually installed
    m_local_config = None
    m_pyhouse_obj = None

    def __init__(self):
        """ **NOR**
        Note that the reactor is *NOT* yet running.
        """
        LOG.info("\n======================== Initializing ======================== Version: {}\n".format(__version__))
        setup_logging.Api()  # Start up logging
        LOG.info('Setting up Main Data areas')
        self.m_pyhouse_obj = setup_pyhouse_obj.setup_pyhouse()
        self._add_storage()
        self.m_utility = Utility(self.m_pyhouse_obj)
        self.m_local_config = LocalConfig(self.m_pyhouse_obj)
        self.m_local_config.load_yaml_config()
        self.m_modules = self.m_utility.initialize_core_modules(MODULES)
        self.m_components = self.m_components = self.m_utility.initialize_all_components(COMPONENTS)
        self.m_pyhouse_obj._Twisted.Reactor.callWhenRunning(self.LoadConfig)
        LOG.info("\n======================== Initialized ======================== Version: {}\n".format(__version__))
        LOG.info('Starting Reactor...')
        self.m_pyhouse_obj._Twisted.Reactor.run()  # reactor never returns so must be last - Event loop will now run
        LOG.info("PyHouse says Bye Now.\n")
        print('PyHouse is exiting.')
        raise SystemExit("PyHouse says Bye Now.")

    def _add_storage(self):
        self.m_pyhouse_obj.Core.MqttApi = None  # Clear before loading

    def LoadConfig(self):
        """ Load in the entire configuration for PyHouse.
        This will fill in pyhouse_obj for all defined features of PyHouse.
        """
        LOG.info("\n======================== Loading Config Files ======================== Version: {}\n".format(__version__))
        #
        self.m_utility.load_core_modules(self.m_modules)
        self.m_utility.start_core_modules(self.m_modules)
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

# ## END DBK
