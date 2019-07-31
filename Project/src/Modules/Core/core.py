"""
@name:      Modules/Core/core.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2014-2019 by D. Brian Kimmel
@note:      Created on Mar 1, 2014
@license:   MIT License
@summary:   This module sets up the Core part of PyHouse.

The PyHouse system has two parts.
The first part is the computer.
    It deals with things that pertain to the computer (this one).
    There can be one or more computers running PyHouse.
    Each computer can control two or more control devices.

The second part is the house.
    There is only one house associated with the PyHouse program.
    Every system and sub-system that pertains to the house being automated is here.

This will set up this node and then find all other nodes in the same domain (House).
Then start the House and all the sub systems.
"""

__updated__ = '2019-07-31'
__version_info__ = (19, 8, 1)
__version__ = '.'.join(map(str, __version_info__))

#  Import system type stuff
import os
from twisted.internet import reactor

#  Import PyMh files and modules.
# These 3 must be the first so logging is running as the rest of PyHouse starts up.
from Modules.Core import setup_logging  # This must be first as the import causes logging to be initialized
from Modules.Core.Utilities import config_tools
from Modules.Core.data_objects import \
    PyHouseInformation, \
    PyHouseAPIs, \
    CoreAPIs, \
    CoreInformation, \
    ParameterInformation, \
    UuidInformation, \
    TwistedInformation, \
    UuidData
from Modules.Core.Mqtt.mqtt import API as mqttAPI, MqttInformation
from Modules.Core.Utilities.config_tools import \
    API as configAPI, \
    ConfigInformation
from Modules.Core.Utilities.uuid_tools import Uuid as toolUuid
from Modules.Computer.computer import API as computerAPI, ComputerInformation
from Modules.House.house import API as houseAPI, HouseInformation

from Modules.Core.Utilities.debug_tools import PrettyFormatAny

from Modules.Core import logging_pyh as Logger
LOG = Logger.getLogger('PyHouse.Core           ')

MINUTES = 60  # Seconds in a minute
HOURS = 60 * MINUTES
INITIAL_DELAY = 1 * MINUTES
XML_SAVE_DELAY = 3 * HOURS  # 2 hours
CONFIG_DIR = '/etc/pyhouse/'
XML_FILE_NAME = 'master.xml'
CONFIG_FILE_NAME = 'pyhouse.yaml'


class Config:
    """
    """
    m_pyhouse_obj = None

    def __init__(self, p_pyhouse_obj):
        """
        """
        self.m_pyhouse_obj = p_pyhouse_obj


class Utility:
    """
    """

    def _config_save_loop(self, p_pyhouse_obj):
        p_pyhouse_obj._Twisted.Reactor.callLater(XML_SAVE_DELAY, self._config_save_loop, p_pyhouse_obj)
        self.SaveConfig()

    @staticmethod
    def save_uuids(p_pyhouse_obj):
        """be sure to save all the uuid files in /etc/pyhouse
        Computer.uuid
        House.uuid
        Domain.uuid
        """
        _l_uuids = p_pyhouse_obj._Uuids.All

    @staticmethod
    def _sync_startup_logging(p_pyhouse_obj):
        """Start up the logging system.
        This is sync so that logging is up and running before proceeding with the rest of the initialization.
        The logs are at a fixed place and are not configurable.
        """
        # l_log = setup_logging.API(p_pyhouse_obj)  # To eliminate Eclipse warning
        # l_log.Start()
        # LOG.info("Starting.")

    def _load_pyhouse_yaml_file(self, p_pyhouse_obj):
        """
        """
        l_yaml = config_tools.Yaml(p_pyhouse_obj).read_yaml(CONFIG_FILE_NAME)
        try:
            l_dict = l_yaml.Yaml['PyHouse']
            p_pyhouse_obj._Parameters.UnitSystem = l_dict['UnitSystem']
            p_pyhouse_obj._Parameters.Name = l_dict['Name']
            p_pyhouse_obj._Parameters.ConfigVersion = l_dict['ConfigVersion']
        except:
            LOG.error('Invalid "pyhouse.yaml" file!')
            p_pyhouse_obj._Parameters.UnitSystem = 'Metric'
            p_pyhouse_obj._Parameters.Name = 'nameless wonder'
            p_pyhouse_obj._Parameters.ConfigVersion = 1.0

    def _setup_Core(self):
        """
        """
        LOG.info('Setting up Core modules.')
        l_obj = CoreInformation()
        l_obj.Mqtt = MqttInformation()
        return l_obj

    def _setup_Computer(self):
        """
        """
        l_obj = ComputerInformation()
        return l_obj

    def _setup_House(self):
        """
        """
        l_obj = HouseInformation()
        return l_obj

    def _setup_APIs(self):
        """
        """
        l_obj = PyHouseAPIs()
        l_obj.Core = CoreAPIs()
        l_obj.Core.PyHouseMainAPI = self
        return l_obj

    def _setup_Config(self):
        """
        """
        l_obj = ConfigInformation()
        if l_obj.ConfigDir is None:
            l_obj.ConfigDir = CONFIG_DIR
        return l_obj

    def _setup_Families(self):
        """
        """
        l_obj = {}
        return l_obj

    def _setup_Parameters(self):
        """
        """
        l_obj = ParameterInformation()
        return l_obj

    def _setup_Twisted(self):
        """
        """
        l_obj = TwistedInformation()
        l_obj.Reactor = reactor
        return l_obj

    def _setup_Uuids(self):
        """
        """
        l_obj = UuidInformation()
        l_obj.All = UuidData()
        l_obj.All = {}
        l_path = os.path.join(CONFIG_DIR, 'Computer.uuid')
        try:
            l_file = open(l_path, mode='r')
            _l_uuid = l_file.read()
        except IOError:
            _l_uuid = toolUuid.create_uuid()
        # LOG.debug(PrettyFormatAny.form(self.m_pyhouse_obj, 'SetupUuids-PyHouse', 190))
        return l_obj


class API(Utility):
    """
    Called from PyHouse.py
    """

    m_pyhouse_obj = None

    def __init__(self):
        """ **NOR**
        This will initialize much (all?) of the API infrastructure.
        Note that the Configuration file is NOT read until the following Start() method begins.
        Also note that the reactor is *NOT* yet running.
        """
        LOG.info('Initializing - Version:{}'.format(__version__))
        setup_logging.API()  # Start up logging
        LOG.info('Setting up Main Data areas')
        self.m_pyhouse_obj = PyHouseInformation()
        self.m_pyhouse_obj.Core = self._setup_Core()  # First
        self.m_pyhouse_obj._APIs = self._setup_APIs()
        self.m_pyhouse_obj._Config = self._setup_Config()
        self.m_pyhouse_obj._Families = self._setup_Families()
        self.m_pyhouse_obj._Parameters = self._setup_Parameters()
        self.m_pyhouse_obj._Twisted = self._setup_Twisted()
        self.m_pyhouse_obj._Uuids = self._setup_Uuids()
        self.m_pyhouse_obj.Computer = self._setup_Computer()
        self.m_pyhouse_obj.House = self._setup_House()
        #
        self._load_pyhouse_yaml_file(self.m_pyhouse_obj)
        self._sync_startup_logging(self.m_pyhouse_obj)
        self.m_pyhouse_obj._APIs.Core.MqttAPI = mqttAPI(self.m_pyhouse_obj, self)
        self.m_pyhouse_obj._APIs.Core.MqttAPI.LoadConfig()
        self.m_pyhouse_obj._APIs.Core.MqttAPI.Start()
        self.m_pyhouse_obj._APIs.Computer.ComputerAPI = computerAPI(self.m_pyhouse_obj)
        self.m_pyhouse_obj._APIs.House.HouseAPI = houseAPI(self.m_pyhouse_obj)
        LOG.info('All data has been set up.')
        #
        self.m_pyhouse_obj._Twisted.Reactor.callWhenRunning(self.LoadConfig)
        LOG.info("Initialized - Version:{}\n======================== Initialized ========================\n".format(__version__))
        LOG.info('Starting Reactor...')
        self.m_pyhouse_obj._Twisted.Reactor.run()  # reactor never returns so must be last - Event loop will now run
        #
        LOG.info("PyHouse says Bye Now.\n")
        print('PyHouse is exiting.')
        raise SystemExit("PyHouse says Bye Now.")

    def LoadConfig(self):
        """ Load in the entire configuration for PyHouse.
        This will fill in pyhouse_obj for all defined features of PyHouse.
        """
        LOG.info("Loading Config - Version:{}\n======================== Loading Config Files ========================\n".format(__version__))
        self.m_pyhouse_obj._APIs.Computer.ComputerAPI.LoadConfig()
        self.m_pyhouse_obj._APIs.House.HouseAPI.LoadConfig()
        LOG.info("Loaded Config - Version:{}".format(__version__))
        self.m_pyhouse_obj._Twisted.Reactor.callLater(3, self.Start)
        LOG.info("Loaded Config - Version:{}\n======================== Loaded Config Files ========================\n".format(__version__))
        # self.Start()

    def Start(self):
        """
        The reactor is now running.

        @param p_pyhouse_obj: is the skeleton Obj filled in some by PyHouse.py.
        """
        print('Reactor is now running.')
        LOG.info('Starting - Reactor is now running.')
        self.m_pyhouse_obj._APIs.Computer.ComputerAPI.Start()
        self.m_pyhouse_obj._APIs.House.HouseAPI.Start()
        self.m_pyhouse_obj._Twisted.Reactor.callLater(INITIAL_DELAY, self._config_save_loop, self.m_pyhouse_obj)
        LOG.info("Started.\n==========\n")

    def SaveConfig(self):
        """
        Take a snapshot of the current Configuration/Status and write out into config files.
        The XML file is a single large file containing everything.
        The Yaml config is broken down into many smaller files and written by each component.
        """
        LOG.info('\n======================== Saving Config Files ========================\n')
        configAPI(self.m_pyhouse_obj).create_xml_config_foundation(self.m_pyhouse_obj)
        self.m_pyhouse_obj._APIs.Computer.ComputerAPI.SaveConfig()
        self.m_pyhouse_obj._APIs.House.HouseAPI.SaveConfig()
        LOG.info("Saved all Config sections.\n======================== Saved Config Files ========================\n")

    def Stop(self):
        l_topic = 'computer/shutdown'
        self.m_pyhouse_obj._APIs.Core.MqttAPI.MqttPublish(l_topic, self.m_pyhouse_obj.Computer.Nodes[self.m_pyhouse_obj.Computer.Name])
        self.SaveConfig()
        self.m_pyhouse_obj._APIs.Computer.ComputerAPI.Stop()
        self.m_pyhouse_obj._APIs.House.HouseAPI.Stop()
        LOG.info("Stopped.\n==========\n")

# ## END DBK
