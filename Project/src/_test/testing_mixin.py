"""
@name:      PyHouse/Project/src/_test/testing_mixin.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2013-2020 by D. Brian Kimmel
@license:   MIT License
@note:      Created on Jun 4, 2013
@summary:   Test handling the information for a house.

"""

__updated__ = '2020-01-27'

#  Import system type stuff
import os
import platform
import logging
import sys
from twisted.internet import reactor

#  Import PyMh files and modules.
from Modules.Computer.computer import ComputerInformation
from Modules.House.house_data import LocationInformation
from Modules.House.Hvac.hvac import HvacInformation
from Modules.House.Lighting.lighting import LightingInformation
from Modules.Core.data_objects import PyHouseInformation
from Modules.Core.Config.config_tools import ConfigInformation, AccessInformation
from Modules.House.Family.family import Api as familyApi
from Modules.House.house import HouseInformation
from Modules.Core import logging_pyh as Logger
from Modules.Core.Mqtt.mqtt import MqttInformation
from Modules.Core.setup_pyhouse_obj import CoreInformation, TwistedInformation
#
#  Different logging setup to cause testing logs to come out in red on the console.
#
l_format = '\n [%(levelname)s] %(name)s: %(funcName)s %(lineno)s:\n\t%(message)s'
l_level = 'WARNING'  # 'CRITICAL', 'FATAL', 'ERROR', 'WARNING', 'INFO', 'DEBUG', 'NOTSET'
l_formatter = logging.Formatter(fmt=l_format)
l_handler = logging.StreamHandler(stream=sys.stderr)
l_handler.setFormatter(l_formatter)
LOG = Logger.getLogger('PyHouse')
LOG.addHandler(l_handler)
LOG.setLevel(l_level)

TEST_PATH = os.path.split(os.path.dirname(os.path.realpath(__file__)))[0]


class YamlData:

    def __init__(self):
        self.root = None


class SetupPyHouseObj:
    """
    """

    m_pyhouse_obj = None

    def __init__(self):
        self.m_pyhouse_obj = PyHouseInformation()

    def _build_config(self):
        """
        Change the path for finding yaml config files to the PySource src package.
        """
        l_ret = ConfigInformation()
        l_ret.ConfigDir = TEST_PATH
        return l_ret

    def _build_twisted(self):
        l_ret = TwistedInformation()
        l_ret.Reactor = reactor
        return l_ret

    def _build_house_data(self):
        l_ret = HouseInformation()
        l_ret.Location = LocationInformation()
        l_ret.Family = {}
        l_ret.Entertainment = {}
        l_ret.Lighting = LightingInformation()
        l_ret.Hvac = HvacInformation()
        l_ret.Schedules = {}
        l_ret.Security = AccessInformation()
        return l_ret

    def _build_computer(self):
        l_ret = ComputerInformation()
        return l_ret

    def _build_core(self):
        l_ret = CoreInformation()
        l_ret.Mqtt = MqttInformation()
        return l_ret

    def _computer_yaml(self, p_yaml):
        pass

    def _house_yaml(self, p_yaml):
        pass

    def BuildPyHouseObj(self):
        """ This will create the pyhpuse_obj structure.
        """
        l_pyhouse_obj = PyHouseInformation()
        l_pyhouse_obj.Core = SetupPyHouseObj()._build_core()
        l_pyhouse_obj.Computer = SetupPyHouseObj()._build_computer()
        l_pyhouse_obj.House = SetupPyHouseObj()._build_house_data()
        l_pyhouse_obj._Twisted = self._build_twisted()
        l_pyhouse_obj.Computer.Name = platform.node()
        return l_pyhouse_obj

    def BuildYaml(self, p_root_yaml):
        l_yaml = YamlData()
        l_yaml.root = p_root_yaml
        self._computer_yaml(l_yaml)
        self._house_yaml(l_yaml)
        return l_yaml

    def LoadComputer(self, p_pyhouse_obj):
        pass

    def LoadHouse(self, p_pyhouse_obj):
        p_pyhouse_obj.House.Family = familyApi(p_pyhouse_obj).LoadFamilyTesting()

    def setUp(self):
        self.BuildPyHouseObj()

#  ## END DBK
