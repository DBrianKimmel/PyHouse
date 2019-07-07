"""
@name:      PyHouse/Project/src/Modules/Core/setup_pyhouse.py
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
from Modules.Core.Utilities.debug_tools import PrettyFormatAny

__updated__ = '2019-07-07'
__version_info__ = (19, 6, 1)
__version__ = '.'.join(map(str, __version_info__))

#  Import system type stuff
import os
from xml.etree import ElementTree as ET

#  Import PyMh files and modules.
# These 3 must be the first so logging is running as the rest of PyHouse starts up.
from Modules.Core import setup_logging  # This must be first as the import causes logging to be initialized
from Modules.Core.Utilities import config_tools
from Modules.Core.data_objects import ParameterInformation, CoreInformation
#
from Modules.Core.Mqtt.mqtt_data import MqttInformation
from Modules.Core.Mqtt.mqtt import API as mqttAPI
from Modules.Computer import logging_pyh as Logger
LOG = Logger.getLogger('PyHouse.CoreSetupPyHous')
# #
from Modules.Core.Utilities.config_tools import API as configAPI, ConfigInformation
from Modules.Core.Utilities.uuid_tools import Uuid as toolUuid

from Modules.Computer.computer import API as computerAPI
from Modules.Housing.house import API as houseAPI
# from Modules.Core.Utilities.xml_tools import PutGetXML

# from Modules.Core.Utilities.debug_tools import PrettyFormatAny

MINUTES = 60  # Seconds in a minute
HOURS = 60 * MINUTES
INITIAL_DELAY = 1 * MINUTES
XML_SAVE_DELAY = 3 * HOURS  # 2 hours
CONFIG_DIR = '/etc/pyhouse/'
XML_FILE_NAME = 'master.xml'
CONFIG_FILE_NAME = 'pyhouse.yaml'


class Utility(object):
    """
    """

    def _xml_save_loop(self, p_pyhouse_obj):
        p_pyhouse_obj._Twisted.Reactor.callLater(XML_SAVE_DELAY, self._xml_save_loop, p_pyhouse_obj)
        self.SaveConfig(p_pyhouse_obj)

    @staticmethod
    def init_uuids(p_pyhouse_obj):
        """be sure that all the uuid files exist in /etc/pyhouse
        Computer.uuid
        House.uuid
        Domain.uuid
        """
        # LOG.debug(PrettyFormatAny.form(p_pyhouse_obj, 'PyHouse', 190))
        p_pyhouse_obj._Uuids.All = {}
        l_path = os.path.join(CONFIG_DIR, 'Computer.uuid')
        try:
            l_file = open(l_path, mode='r')
            _l_uuid = l_file.read()
        except IOError:
            _l_uuid = toolUuid.create_uuid()

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
        l_log = setup_logging.API(p_pyhouse_obj)  # To eliminate Eclipse warning
        l_log.Start()
        LOG.info("Starting.")

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

    def _setup_config(self, p_pyhouse_obj):
        """
        """
        if p_pyhouse_obj._Config.ConfigDir is None:
            p_pyhouse_obj._Config.ConfigDir = CONFIG_DIR
        try:
            l_xmltree = ET.parse(p_pyhouse_obj._Config.ConfigDir + XML_FILE_NAME)
        except (SyntaxError, IOError):
            l_xml = ET.Element("PyHouse")
            l_xmltree = ET.ElementTree(element=l_xml)
        p_pyhouse_obj._Config.XmlRoot = l_xmltree.getroot()

    def initialize_pyhouse_obj(self, p_pyhouse_obj):
        """
        """
        p_pyhouse_obj.Core = CoreInformation()
        # p_pyhouse_obj.Core.Mqtt = MqttInformation()
        p_pyhouse_obj._Config = ConfigInformation()
        p_pyhouse_obj._Parameters = ParameterInformation()
        self._setup_config(p_pyhouse_obj)
        self._load_pyhouse_yaml_file(p_pyhouse_obj)


class API(Utility):
    """ Now that any platform dependent initialization has been done, set up the rest of PyHouse.
    Called from PyHouse.py
    """

    def __init__(self, p_pyhouse_obj):
        """ **NOR**
        This will initialize much (all?) of the API infrastructure.
        Note that the Configuration file is NOT read until the following Start() method begins.
        Also note that the reactor is *NOT* yet running.
        """
        LOG.info('Initializing - Version:{} - {}'.format(__version__, p_pyhouse_obj))
        self.initialize_pyhouse_obj(p_pyhouse_obj)
        Utility.init_uuids(p_pyhouse_obj)
        Utility._sync_startup_logging(p_pyhouse_obj)

        # print(PrettyFormatAny.form(p_pyhouse_obj._APIs, 'Debug', 190))

        p_pyhouse_obj._APIs.Core.MqttAPI = mqttAPI(p_pyhouse_obj, self)
        p_pyhouse_obj._APIs.Computer.ComputerAPI = computerAPI(p_pyhouse_obj)
        p_pyhouse_obj._APIs.House.HouseAPI = houseAPI(p_pyhouse_obj)
        # Utility._sync_startup_logging(p_pyhouse_obj)
        self.m_pyhouse_obj = p_pyhouse_obj
        LOG.info('Initialized.')

    def LoadConfig(self, p_pyhouse_obj):
        """ Load in the entire configuration for PyHouse.
        This will fill in pyhouse_obj for all defined features of PyHouse.
        """
        LOG.info("Loading Config - Version:{}\n======================== Loading Config Files ========================\n".format(__version__))
        # p_pyhouse_obj = configAPI(p_pyhouse_obj).LoadConfig(p_pyhouse_obj)
        p_pyhouse_obj._APIs.Computer.ComputerAPI.LoadConfig(p_pyhouse_obj)
        p_pyhouse_obj._APIs.House.HouseAPI.LoadConfig(p_pyhouse_obj)
        LOG.info("Loaded Config - Version:{}".format(__version__))

    def Start(self):
        """
        The reactor is now running.

        @param p_pyhouse_obj: is the skeleton Obj filled in some by PyHouse.py.
        """
        #  First we start up the logging system - no need for Config yet as it is at a fixed location
        #  next Starting the computer and House will load the respective divisions of the config files.
        self.m_pyhouse_obj._APIs.Computer.ComputerAPI.Start()
        self.m_pyhouse_obj._APIs.House.HouseAPI.Start()
        self.m_pyhouse_obj._Twisted.Reactor.callLater(INITIAL_DELAY, self._xml_save_loop, self.m_pyhouse_obj)
        LOG.info("Started.\n==========\n")

    def SaveConfig(self, p_pyhouse_obj):
        """
        Take a snapshot of the current Configuration/Status and write out into config files.
        The XML file is a single large file containing everything.
        The Yaml config is broken down into many smaller files and written by each component.
        """
        LOG.info('\n======================== Saving Config Files ========================\n')
        configAPI(p_pyhouse_obj).create_xml_config_foundation(p_pyhouse_obj)
        p_pyhouse_obj._APIs.Computer.ComputerAPI.SaveConfig(p_pyhouse_obj)
        p_pyhouse_obj._APIs.House.HouseAPI.SaveConfig(p_pyhouse_obj)
        configAPI(p_pyhouse_obj).write_xml_config_file(p_pyhouse_obj)
        LOG.info("Saved all Config sections.\n======================== Saved Config Files ========================\n")

    def Stop(self):
        l_topic = 'computer/shutdown'
        self.m_pyhouse_obj._APIs.Core.MqttAPI.MqttPublish(l_topic, self.m_pyhouse_obj.Computer.Nodes[self.m_pyhouse_obj.Computer.Name])
        self.SaveConfig()
        self.m_pyhouse_obj._APIs.Computer.ComputerAPI.Stop()
        self.m_pyhouse_obj._APIs.House.HouseAPI.Stop()
        LOG.info("Stopped.\n==========\n")

# ## END DBK
