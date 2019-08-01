"""
@name:      PyHouse/Project/src/_test/testing_mixin.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2013-2019 by D. Brian Kimmel
@license:   MIT License
@note:      Created on Jun 4, 2013
@summary:   Test handling the information for a house.

"""

__updated__ = '2019-07-31'

#  Import system type stuff
import os
import platform
import logging
import sys
from twisted.internet import reactor

#  Import PyMh files and modules.
from Modules.Computer.computer import ComputerInformation, ComputerAPIs
from Modules.House.house_data import LocationInformationPrivate
from Modules.House.Entertainment.entertainment import \
    EntertainmentInformation, \
    EntertainmentPluginInformation
from Modules.House.Lighting.lighting import LightingInformation
from Modules.Core.data_objects import \
    PyHouseInformation, \
    PyHouseAPIs, \
    HouseInformation, \
    HouseAPIs, \
    TwistedInformation, \
    SecurityData, \
    UuidInformation, CoreInformation
from Modules.Core.Utilities.config_tools import \
    ConfigInformation
from Modules.House.Family.family import \
    Utility as familyUtil, \
    API as familyAPI
from Modules.House.house import API as housingAPI
from Modules.House.Hvac.hvac_data import HvacData
from Modules.Core import logging_pyh as Logger
from Modules.Core.Mqtt.mqtt_data import MqttInformation
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


class XmlData(object):
    """
    Testing XML infrastructure
    """

    def __init__(self):
        self.root = None
        #
        self.house_div = None
        self.entertainment_sect = None
        self.onkyo_sect = None
        self.panasonic_sect = None
        self.pandora_sect = None
        self.pioneer_sect = None
        self.samsung_sect = None
        self.lighting_sect = None
        self.button_sect = None
        self.button = None
        self.controller_sect = None
        self.controller = None
        self.light_sect = None
        self.light = None
        self.location_sect = None
        self.location = None
        self.irrigation_sect = None
        self.irrigation_system = None
        self.irrigation_zone = None
        self.pool_sect = None
        self.pool = None
        self.room_sect = None
        self.room = None
        self.rules_sect = None
        self.rule = None
        self.schedule_sect = None
        self.schedule = None
        self.security_sect = None
        self.garagedoor_sect = None
        self.garagedoor = None
        # self.motionsensor_sect = None
        # self.motionsensor = None
        self.hvac_sect = None
        self.thermostat_sect = None
        self.thermostat = None
        #
        self.computer_div = None
        self.bridges_sect = None
        self.communication_sect = None
        self.email_sect = None
        self.twitter_sect = None
        self.internet_sect = None
        self.internet = None
        self.internet_locater_sect = None
        self.internet_updater_sect = None
        self.mqtt_sect = None
        self.log_sect = None
        self.web_sect = None
        self.login_sect = None
        self.node_sect = None
        self.node = None
        self.interface_sect = None
        self.interface = None


class YamlData():

    def __init__(self):
        self.root = None


class SetupPyHouseObj():
    """
    """

    def _build_config(self):
        """
        Change the path for finding yaml config files to the PySource src package.
        """
        l_ret = ConfigInformation()
        l_ret.ConfigDir = TEST_PATH
        return l_ret

    def _build_yaml(self, p_root):
        l_ret = YamlData()
        l_ret.YamlRoot = p_root
        l_ret.YamlFileName = '/etc/pyhouse/master.yaml'
        return l_ret

    def _build_twisted(self):
        l_ret = TwistedInformation()
        l_ret.Reactor = reactor
        return l_ret

    @staticmethod
    def _build_entertainment(_p_pyhouse_obj):
        l_ret = EntertainmentInformation()
        l_ret.Plugins = EntertainmentPluginInformation()
        return l_ret

    @staticmethod
    def _build_house_data(p_pyhouse_obj):
        l_ret = HouseInformation()
        l_ret.Location = LocationInformationPrivate()
        l_ret.Entertainment = SetupPyHouseObj._build_entertainment(p_pyhouse_obj)
        l_ret.Lighting = LightingInformation()
        l_ret.Hvac = HvacData()
        l_ret.Security = SecurityData()
        return l_ret

    @staticmethod
    def _build_computer(_p_pyhouse_obj):
        l_ret = ComputerInformation()
        l_ret.Mqtt = MqttInformation()
        return l_ret

    def _build_core(self):
        l_ret = CoreInformation()
        return l_ret

    def _build_apis(self):
        l_apis = PyHouseAPIs()
        l_apis.Computer = ComputerAPIs()
        l_apis.House = HouseAPIs()
        return l_apis

    def _computer_xml(self, p_xml):
        p_xml.computer_div = p_xml.root.find('ComputerDivision')
        if p_xml.computer_div is None:
            return
        #
        p_xml.bridges_sect = p_xml.computer_div.find('BridgesSection')
        if p_xml.bridges_sect is not None:
            p_xml.bridge = p_xml.bridges_sect.find('Bridge')
        p_xml.communication_sect = p_xml.computer_div.find('CommunicationSection')
        if p_xml.communication_sect is not None:
            p_xml.email_sect = p_xml.communication_sect.find('EmailSection')
            p_xml.twitter_sect = p_xml.communication_sect.find('TwitterSection')
        p_xml.node_sect = p_xml.computer_div.find('NodeSection')
        if p_xml.node_sect is not None:
            p_xml.node = p_xml.node_sect.find('Node')
            p_xml.interface_sect = p_xml.node.find('InterfaceSection')
            p_xml.interface = p_xml.interface_sect.find('Interface')
        #
        p_xml.internet_sect = p_xml.computer_div.find('InternetSection')
        if p_xml.internet_sect is not None:
            p_xml.internet = p_xml.internet_sect.find('Internet')
            p_xml.internet_locater_sect = p_xml.internet.find('LocateUrlSection')
            p_xml.internet_updater_sect = p_xml.internet.find('UpdateUrlSection')
        #
        p_xml.mqtt_sect = p_xml.computer_div.find('MqttSection')
        p_xml.broker = p_xml.mqtt_sect.find('Broker')

        p_xml.web_sect = p_xml.computer_div.find('WebSection')
        p_xml.login_sect = p_xml.web_sect.find('LoginSection')

    def _computer_yaml(self, p_yaml):
        pass

    def _house_xml(self, p_xml):
        p_xml.house_div = p_xml.root.find('HouseDivision')
        if p_xml.house_div is None:
            return

        p_xml.entertainment_sect = p_xml.house_div.find('EntertainmentSection')
        if p_xml.entertainment_sect is not None:
            p_xml.panasonic_sect = p_xml.entertainment_sect.find('PanasonicSection')
            p_xml.pandora_sect = p_xml.entertainment_sect.find('PandoraSection')
            p_xml.pioneer_sect = p_xml.entertainment_sect.find('PioneerSection')
            p_xml.samsung_sect = p_xml.entertainment_sect.find('SamsungSection')
            p_xml.onkyo_sect = p_xml.entertainment_sect.find('OnkyoSection')
        #
        p_xml.irrigation_sect = p_xml.house_div.find('IrrigationSection')
        if p_xml.irrigation_sect is not None:
            p_xml.irrigation_system = p_xml.irrigation_sect.find('System')
            if p_xml.irrigation_system is not None:
                p_xml.irrigation_zone = p_xml.irrigation_system.find('Zone')

        p_xml.pool_sect = p_xml.house_div.find('PoolSection')
        if p_xml.pool_sect is not None:
            p_xml.pool = p_xml.pool_sect.find('Pool')

        p_xml.room_sect = p_xml.house_div.find('RoomSection')
        if p_xml.room_sect is not None:
            p_xml.room = p_xml.room_sect.find('Room')

        p_xml.rules_sect = p_xml.house_div.find('RulesSection')
        if p_xml.rules_sect is not None:
            p_xml.rule = p_xml.rules_sect.find('Rule')

        p_xml.schedule_sect = p_xml.house_div.find('ScheduleSection')
        if p_xml.schedule_sect is not None:
            p_xml.schedule = p_xml.schedule_sect.find('Schedule')

        p_xml.security_sect = p_xml.house_div.find('SecuritySection')
        if p_xml.security_sect is not None:
            p_xml.garagedoor_sect = p_xml.security_sect.find('GarageDoorSection')
            p_xml.garagedoor = p_xml.garagedoor_sect.find('GarageDoor')
            p_xml.motiondetector_sect = p_xml.security_sect.find('MotionDetectorSection')
            p_xml.motiondetector = p_xml.motiondetector_sect.find('Motion')

        p_xml.lighting_sect = p_xml.house_div.find('LightingSection')
        if p_xml.lighting_sect is not None:
            p_xml.button_sect = p_xml.lighting_sect.find('ButtonSection')
            p_xml.button = p_xml.button_sect.find('Button')
            p_xml.controller_sect = p_xml.lighting_sect.find('ControllerSection')
            p_xml.controller = p_xml.controller_sect.find('Controller')
            p_xml.light_sect = p_xml.lighting_sect.find('LightSection')
            p_xml.light = p_xml.light_sect.find('Light')

        p_xml.hvac_sect = p_xml.house_div.find('HvacSection')
        if p_xml.hvac_sect is not None:
            p_xml.thermostat_sect = p_xml.hvac_sect.find('ThermostatSection')
            p_xml.thermostat = p_xml.thermostat_sect.find('Thermostat')

        p_xml.location_sect = p_xml.house_div.find('LocationSection')

    def _house_yaml(self, p_yaml):
        pass

    def BuildPyHouseObj(self):
        """ This will create the pyhpuse_obj structure.
        """
        l_pyhouse_obj = PyHouseInformation()
        l_pyhouse_obj.Core = SetupPyHouseObj()._build_core()
        l_pyhouse_obj.Computer = SetupPyHouseObj._build_computer(l_pyhouse_obj)
        l_pyhouse_obj.House = SetupPyHouseObj._build_house_data(l_pyhouse_obj)
        #
        l_pyhouse_obj._APIs = self._build_apis()
        l_pyhouse_obj._Config = self._build_config()
        # l_pyhouse_obj._Families = familyUtil()._init_family_component_apis(l_pyhouse_obj)
        l_pyhouse_obj._Twisted = self._build_twisted()
        l_pyhouse_obj._Uuids = UuidInformation()
        l_pyhouse_obj._Uuids.All = {}
        l_pyhouse_obj.Computer.Name = platform.node()
        return l_pyhouse_obj

    def BuildXml(self, p_root_xml):
        l_xml = XmlData()
        l_xml.root = p_root_xml
        self._computer_xml(l_xml)
        self._house_xml(l_xml)
        return l_xml

    def BuildYaml(self, p_root_yaml):
        l_yaml = YamlData()
        l_yaml.root = p_root_yaml
        self._computer_yaml(l_yaml)
        self._house_yaml(l_yaml)
        return l_yaml

    def LoadComputer(self, p_pyhouse_obj):
        pass

    def LoadHouse(self, p_pyhouse_obj):
        p_pyhouse_obj._Families = familyAPI(p_pyhouse_obj).LoadFamilyTesting()
        housingAPI(p_pyhouse_obj).LoadXml(p_pyhouse_obj)
        return

    def setUp(self):
        self.BuildPyHouseObj()

#  ## END DBK
