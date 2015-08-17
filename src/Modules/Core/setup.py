"""
-*- test-case-name: PyHouse.src.Modules.Core.test.test_setup -*-

@name:      PyHouse/src/Modules/Core/setup.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2014-2015 by D. Brian Kimmel
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

# Import system type stuff

# Import PyMh files and modules.
from Modules.Core import setup_logging  # This must be first as the import causes logging to be initialized
from Modules.Computer import logging_pyh as Logger
from Modules.Computer.computer import API as computerAPI
from Modules.Housing.house import API as houseAPI
from Modules.Utilities.config_file import API as configAPI
from Modules.Communication.ir_control import g_pyhouse_obj
from Modules.Utilities.debug_tools import PrettyFormatAny

LOG = Logger.getLogger('PyHouse.CoreSetup      ')

INTER_NODE = 'tcp:port=8581'
INTRA_NODE = 'unix:path=/var/run/pyhouse/node:lockfile=1'
INITIAL_DELAY = 3 * 60
REPEAT_DELAY = 2 * 60 * 60  # 2 hours


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

    def log_start(self):
        LOG.info("""\n------------------------------------------------------------------

        """)

    def _xml_save_loop(self, p_pyhouse_obj):
        p_pyhouse_obj.Twisted.Reactor.callLater(REPEAT_DELAY, self._xml_save_loop, p_pyhouse_obj)
        self.SaveXml()



class API(Utility):

    def __init__(self, p_pyhouse_obj):
        """
        This will initialize much (all?) of the API infrastructure.
        Note that the Configuration file is read as part of the following Start() method.
        Also note that the reactor is *NOT* running.
        """
        self.m_pyhouse_obj = p_pyhouse_obj
        p_pyhouse_obj.APIs.Computer.ComputerAPI = computerAPI(p_pyhouse_obj)
        p_pyhouse_obj.APIs.House.HouseAPI = houseAPI(p_pyhouse_obj)
        PyHouseObj.SetObj(p_pyhouse_obj)

    def Start(self):
        """
        The reactor is now running.

        This controls the order that Configuration things are read-in and initialized.

        @param p_pyhouse_obj: is the skeleton Obj filled in some by PyHouse.py.
        """
        l_log = setup_logging.API(self.m_pyhouse_obj)  # To eliminate Eclipse warning
        l_log.Start()

        # Next is the XML file do things can be read in and customized
        self.m_pyhouse_obj = configAPI(self.m_pyhouse_obj).read_xml_config_file(self.m_pyhouse_obj)
        # print("XML loaded")

        # Next is the logging system
        self.log_start()
        LOG.info("Starting.")
        # print("Log Started")

        # Logging system is now enabled
        # Starting the computer and House will load the respective divisions of the config file.
        self.m_pyhouse_obj.APIs.Computer.ComputerAPI.Start()
        self.m_pyhouse_obj.APIs.House.HouseAPI.Start()
        self.m_pyhouse_obj.Twisted.Reactor.callLater(INITIAL_DELAY, self._xml_save_loop, self.m_pyhouse_obj)
        LOG.debug(' PyHouseObj: {}'.format(PrettyFormatAny.form(PyHouseObj, 'PyHouseObj')))
        LOG.info("Everything has been started.\n")

    def Stop(self):
        self.SaveXml()
        self.m_pyhouse_obj.APIs.Computer.ComputerAPI.Stop()
        self.m_pyhouse_obj.APIs.House.HouseAPI.Stop()
        LOG.info("Stopped.")

    def SaveXml(self):
        """
        Take a snapshot of the current Configuration/Status and write out an XML file.
        """
        l_xml = configAPI(self.m_pyhouse_obj).create_xml_config_foundation(self.m_pyhouse_obj)
        self.m_pyhouse_obj.APIs.Computer.ComputerAPI.SaveXml(l_xml)
        self.m_pyhouse_obj.APIs.House.HouseAPI.SaveXml(l_xml)
        configAPI(self.m_pyhouse_obj).write_xml_config_file(self.m_pyhouse_obj, l_xml)
        LOG.info("Saved all XML sections to config file.\n")

# ## END DBK
