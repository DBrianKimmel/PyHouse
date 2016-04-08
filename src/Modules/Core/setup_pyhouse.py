"""
-*- test-case-name: PyHouse.src.Modules.Core.test.test_setup_pyhouse -*-

@name:      PyHouse/src/Modules/Core/setup_pyhouse.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2014-2016 by D. Brian Kimmel
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

#  Import system type stuff

#  Import PyMh files and modules.
from Modules.Computer import logging_pyh as Logger
from Modules.Computer.computer import API as computerAPI
from Modules.Core import setup_logging  #  This must be first as the import causes logging to be initialized
from Modules.Housing.house import API as houseAPI
from Modules.Utilities.config_file import API as configAPI
LOG = Logger.getLogger('PyHouse.CoreSetup      ')

MINUTES = 60  #  Seconds in a minute
HOURS = 60 * MINUTES
INITIAL_DELAY = 3 * MINUTES
XML_SAVE_DELAY = 2 * HOURS  #  2 hours


class PyHouseObj(object):

    m_pyhouse_obj = None

    @classmethod
    def SetObj(cls, p_pyhouse_obj):
        cls.m_pyhouse_obj = p_pyhouse_obj

    @classmethod
    def GetObj(cls):
        return cls.m_pyhouse_obj


class Utility(object):
    """
    """

    def _xml_save_loop(self, p_pyhouse_obj):
        p_pyhouse_obj.Twisted.Reactor.callLater(XML_SAVE_DELAY, self._xml_save_loop, p_pyhouse_obj)
        self.SaveXml()

    @staticmethod
    def _init_components(p_pyhouse_obj):
        pass

    @staticmethod
    def init_uuids(p_pyhouse_obj):
        """be sure that all the uuid files exist in /etc/pyhouse
        Computer.uuid
        House.uuid
        Domain.uuid
        """
        pass

    @staticmethod
    def _sync_startup_logging(p_pyhouse_obj):
        """Start up the logging system.
        This is sync so that logging is up and running before proceeding with the rest of the initialization.
        The logs are at a fixed place and are not configurable.
        """
        l_log = setup_logging.API(p_pyhouse_obj)  #  To eliminate Eclipse warning
        l_log.Start()
        LOG.info("Starting.")


class API(Utility):
    """ Now that any platform dependent initialization has been done, set up the rest of PyHouse
    """

    def __init__(self, p_pyhouse_obj):
        """
        This will initialize much (all?) of the API infrastructure.
        Note that the Configuration file is NOT read until the following Start() method begins.
        Also note that the reactor is *NOT* running.
        """
        self.m_pyhouse_obj = p_pyhouse_obj
        LOG.info('Initializing')
        #  Utility._init_components(p_pyhouse_obj)
        #  Utility.init_uuids(p_pyhouse_obj)
        p_pyhouse_obj.APIs.Computer.ComputerAPI = computerAPI(p_pyhouse_obj)
        p_pyhouse_obj.APIs.House.HouseAPI = houseAPI(p_pyhouse_obj)
        PyHouseObj.SetObj(p_pyhouse_obj)
        Utility._sync_startup_logging(self.m_pyhouse_obj)
        LOG.info('Initialized\n==================================================================\n')

    def LoadXml(self, p_pyhouse_obj):
        LOG.info('Loading XML')
        p_pyhouse_obj = configAPI(p_pyhouse_obj).read_xml_config_file(p_pyhouse_obj)
        p_pyhouse_obj.APIs.Computer.ComputerAPI.LoadXml(p_pyhouse_obj)
        p_pyhouse_obj.APIs.House.HouseAPI.LoadXml(p_pyhouse_obj)
        LOG.info('Loaded XML')

    def Start(self):
        """
        The reactor is now running.

        @param p_pyhouse_obj: is the skeleton Obj filled in some by PyHouse.py.
        """
        #  First we start up the logging system - no need for XML yes as it is at a fixrd location
        #  next Starting the computer and House will load the respective divisions of the config file.
        self.m_pyhouse_obj.APIs.Computer.ComputerAPI.Start()
        self.m_pyhouse_obj.APIs.House.HouseAPI.Start()
        self.m_pyhouse_obj.Twisted.Reactor.callLater(INITIAL_DELAY, self._xml_save_loop, self.m_pyhouse_obj)
        #  LOG.debug(' PyHouseObj: {}'.format(PrettyFormatAny.form(PyHouseObj, 'PyHouseObj')))
        LOG.info("Started.")
        #  print('Everything Started setup_pyhouse-117')

    def SaveXml(self):
        """
        Take a snapshot of the current Configuration/Status and write out an XML file.
        """
        l_xml = configAPI(self.m_pyhouse_obj).create_xml_config_foundation(self.m_pyhouse_obj)
        self.m_pyhouse_obj.APIs.Computer.ComputerAPI.SaveXml(l_xml)
        self.m_pyhouse_obj.APIs.House.HouseAPI.SaveXml(l_xml)
        configAPI(self.m_pyhouse_obj).write_xml_config_file(self.m_pyhouse_obj, l_xml)
        LOG.info("Saved all XML sections to config file.\n")

    def Stop(self):
        self.m_pyhouse_obj.APIs.Computer.MqttAPI.MqttPublish('computer/shutdown', self.m_pyhouse_obj.Computer.Nodes[self.m_pyhouse_obj.Computer.Name])
        self.SaveXml()
        self.m_pyhouse_obj.APIs.Computer.ComputerAPI.Stop()
        self.m_pyhouse_obj.APIs.House.HouseAPI.Stop()
        LOG.info("Stopped.")

#  ## END DBK
