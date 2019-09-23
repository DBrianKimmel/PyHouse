"""
@name:      PyHouse/Project/src/_test/testing_mixin.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2013-2019 by D. Brian Kimmel
@license:   MIT License
@note:      Created on Jun 4, 2013
@summary:   Test handling the information for a house.

"""
from Modules.Core.core import ParameterInformation

__updated__ = '2019-09-19'

#  Import system type stuff
import os
import platform
import logging
import sys
from twisted.internet import reactor

#  Import PyMh files and modules.
from Modules.Computer.computer import ComputerInformation, ComputerAPIs
from Modules.House.house_data import LocationInformation
from Modules.House.Hvac.hvac import HvacInformation
from Modules.House.Entertainment.entertainment import \
    EntertainmentInformation, \
    EntertainmentPluginInformation
from Modules.House.Lighting.lighting import LightingInformation
from Modules.Core.data_objects import \
    PyHouseInformation, \
    PyHouseAPIs, \
    HouseAPIs, \
    TwistedInformation, \
    UuidInformation, CoreInformation
from Modules.Core.Config.config_tools import \
    ConfigInformation, SecurityInformation
from Modules.House.Family.family import API as familyAPI
from Modules.House.house import HouseInformation
from Modules.Core import logging_pyh as Logger
from Modules.Core.Mqtt.mqtt import MqttInformation
#
#  Different logging setup to cause testing logs to come out in red on the console.
#
l_format = '\n [%(levelname)s] %(name)s: %(funcName)s %(lineno)s:\n\t%(message)s'
l_formatter = logging.Formatter(fmt=l_format)
l_handler = logging.StreamHandler(stream=sys.stderr)
l_handler.setFormatter(l_formatter)
LOG = Logger.getLogger('PyHouse')
LOG.addHandler(l_handler)

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

    def build_params(self):
        l_ret = ParameterInformation()
        l_ret.Name = 'Test'
        return l_ret

    def _build_yaml(self, p_root):
        l_ret = YamlData()
        l_ret.YamlRoot = p_root
        l_ret.YamlFileName = 'pyhouse.yaml'
        return l_ret

    def _build_twisted(self):
        l_ret = TwistedInformation()
        l_ret.Reactor = reactor
        return l_ret

    def _build_entertainment(self):
        l_ret = EntertainmentInformation()
        l_ret.Plugins['test'] = EntertainmentPluginInformation()
        return l_ret

    def _build_house_data(self):
        l_ret = HouseInformation()
        l_ret.Location = LocationInformation()
        l_ret.Entertainment = self._build_entertainment()
        l_ret.Lighting = LightingInformation()
        l_ret.Hvac = HvacInformation()
        l_ret.Security = SecurityInformation()
        return l_ret

    def _build_computer(self):
        l_ret = ComputerInformation()
        return l_ret

    def _build_core(self):
        l_ret = CoreInformation()
        l_ret.Mqtt = MqttInformation()
        return l_ret

    def _build_apis(self):
        l_apis = PyHouseAPIs()
        l_apis.Computer = ComputerAPIs()
        l_apis.House = HouseAPIs()
        return l_apis

    def _computer_yaml(self, p_yaml):
        pass

    def _house_yaml(self, p_yaml):
        pass

    def BuildPyHouseObj(self):
        """ This will create the pyhpuse_obj structure.
        """
        l_pyhouse_obj = PyHouseInformation()
        l_pyhouse_obj.Computer = SetupPyHouseObj()._build_computer()
        l_pyhouse_obj.House = SetupPyHouseObj()._build_house_data()
        #

        l_pyhouse_obj._APIs = self._build_apis()
        l_pyhouse_obj._Config = self._build_config()
        l_pyhouse_obj._Parameters = self.build_params()
        l_pyhouse_obj._Twisted = self._build_twisted()
        l_pyhouse_obj._Uuids = UuidInformation()
        l_pyhouse_obj._Uuids.All = {}
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
        p_pyhouse_obj.House.Family = familyAPI(p_pyhouse_obj).LoadFamilyTesting()

    def setUp(self):
        self.BuildPyHouseObj()

#  ## END DBK
