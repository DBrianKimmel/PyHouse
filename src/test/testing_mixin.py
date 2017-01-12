"""
-*- test-case-name: PyHouse.src.test.test_testing_mixin -*-

@name:      PyHouse/src/test/testing_mixin.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2013-2016 by D. Brian Kimmel
@license:   MIT License
@note:      Created on Jun 40, 2013
@summary:   Test handling the information for a house.

"""

__updated__ = '2017-01-11'

#  Import system type stuff
import platform
import logging
import sys
from twisted.internet import reactor

#  Import PyMh files and modules.
from Modules.Core.data_objects import \
            PyHouseData, \
            PyHouseAPIs, \
            ComputerInformation, \
            ComputerAPIs, \
            HouseInformation, \
            HouseAPIs, \
            LocationData, \
            TwistedInformation, \
            XmlInformation, \
            LightingData, HvacData, SecurityData, AllUuids, UuidData
from Modules.Families.family import Utility as familyUtil, API as familyAPI
from Modules.Housing.house import API as housingAPI
from Modules.Computer import logging_pyh as Logger
from Modules.Core.data_objects import MqttInformation
#
#  Different logging setup to cause testing logs to come out in red on the console.
#
l_format = '\n [%(levelname)s] %(name)s: %(funcName)s %(lineno)s:\n\t%(message)s'
l_formatter = logging.Formatter(fmt=l_format)
l_handler = logging.StreamHandler(stream=sys.stderr)
l_handler.setFormatter(l_formatter)
LOG = Logger.getLogger('PyHouse')
LOG.addHandler(l_handler)


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


class LoadPyHouse(object):
    """
    """

    def __init__(self):
        pass

    def load_computer(self):
        pass

    def load_house(self, p_pyhouse_obj):
        housingAPI.LoadXml(p_pyhouse_obj)
        return


class SetupPyHouseObj(object):
    """
    """

    def _build_xml(self, p_root):
        l_ret = XmlInformation()
        l_ret.XmlRoot = p_root
        l_ret.XmlFileName = '/etc/pyhouse/master.xml'
        return l_ret

    def _build_twisted(self):
        l_ret = TwistedInformation()
        l_ret.Reactor = reactor
        return l_ret

    @staticmethod
    def _build_house(p_pyhouse_obj):
        l_ret = HouseInformation()
        # l_ret.Name = 'Test House'
        l_ret.Location = LocationData()
        l_ret.FamilyData = familyUtil._init_component_apis(p_pyhouse_obj)
        l_ret.Lighting = LightingData()
        l_ret.Hvac = HvacData()
        l_ret.Security = SecurityData()
        return l_ret

    @staticmethod
    def _build_computer(p_pyhouse_obj):
        l_ret = ComputerInformation()
        l_ret.Mqtt = MqttInformation()
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
        p_xml.communication_sect = p_xml.computer_div.find('CommunicationSection')
        p_xml.email_sect = p_xml.communication_sect.find('EmailSection')
        p_xml.twitter_sect = p_xml.communication_sect.find('TwitterSection')
        p_xml.node_sect = p_xml.root.find('ComputerDivision').find('NodeSection')
        p_xml.node = p_xml.node_sect.find('Node')
        p_xml.interface_sect = p_xml.node.find('InterfaceSection')
        p_xml.interface = p_xml.interface_sect.find('Interface')
        #
        p_xml.internet_sect = p_xml.computer_div.find('InternetSection')
        p_xml.internet = p_xml.internet_sect.find('Internet')
        p_xml.internet_locater_sect = p_xml.internet.find('LocateUrlSection')
        p_xml.internet_updater_sect = p_xml.internet.find('UpdateUrlSection')
        #
        p_xml.mqtt_sect = p_xml.computer_div.find('MqttSection')
        p_xml.broker = p_xml.mqtt_sect.find('Broker')
        p_xml.web_sect = p_xml.computer_div.find('WebSection')
        p_xml.login_sect = p_xml.web_sect.find('LoginSection')

    def _house_xml(self, p_xml):
        p_xml.house_div = p_xml.root.find('HouseDivision')
        if p_xml.house_div is None:
            return
        #
        p_xml.entertainment_sect = p_xml.house_div.find('EntertainmentSection')
        p_xml.panasonic_sect = p_xml.entertainment_sect.find('PanasonicSection')
        p_xml.pioneer_sect = p_xml.entertainment_sect.find('PioneerSection')
        p_xml.samsung_sect = p_xml.entertainment_sect.find('SamsungSection')
        #
        p_xml.irrigation_sect = p_xml.house_div.find('IrrigationSection')
        p_xml.location_sect = p_xml.house_div.find('LocationSection')

        p_xml.pool_sect = p_xml.house_div.find('PoolSection')
        p_xml.pool = p_xml.pool_sect.find('Pool')
        p_xml.room_sect = p_xml.house_div.find('RoomSection')
        p_xml.schedule_sect = p_xml.house_div.find('ScheduleSection')
        p_xml.schedule = p_xml.schedule_sect.find('Schedule')

        p_xml.security_sect = p_xml.house_div.find('SecuritySection')
        p_xml.garagedoor_sect = p_xml.security_sect.find('GarageDoorSection')
        p_xml.garagedoor = p_xml.garagedoor_sect.find('GarageDoor')
        p_xml.motiondetector_sect = p_xml.security_sect.find('MotionDetectorSection')
        p_xml.motiondetector = p_xml.motiondetector_sect.find('Motion')
        #
        p_xml.lighting_sect = p_xml.house_div.find('LightingSection')
        p_xml.button_sect = p_xml.lighting_sect.find('ButtonSection')
        p_xml.button = p_xml.button_sect.find('Button')
        p_xml.controller_sect = p_xml.lighting_sect.find('ControllerSection')
        p_xml.controller = p_xml.controller_sect.find('Controller')
        p_xml.light_sect = p_xml.lighting_sect.find('LightSection')
        p_xml.light = p_xml.light_sect.find('Light')
        #
        p_xml.irrigation_system = p_xml.irrigation_sect.find('IrrigationSystem')
        p_xml.irrigation_zone = p_xml.irrigation_system.find('Zone')
        p_xml.room = p_xml.room_sect.find('Room')
        p_xml.hvac_sect = p_xml.house_div.find('HvacSection')
        p_xml.thermostat_sect = p_xml.hvac_sect.find('ThermostatSection')
        p_xml.thermostat = p_xml.thermostat_sect.find('Thermostat')

    def BuildPyHouseObj(self, p_root):
        l_pyhouse_obj = PyHouseData()
        l_pyhouse_obj.APIs = self._build_apis()
        l_pyhouse_obj.Computer = SetupPyHouseObj._build_computer(l_pyhouse_obj)
        l_pyhouse_obj.House = SetupPyHouseObj._build_house(l_pyhouse_obj)
        l_pyhouse_obj.Twisted = self._build_twisted()
        l_pyhouse_obj.Uuids = AllUuids()
        l_pyhouse_obj.Uuids.All = {}
        l_pyhouse_obj.Xml = self._build_xml(p_root)
        l_pyhouse_obj.Computer.Name = platform.node()
        return l_pyhouse_obj

    def BuildXml(self, p_root_xml):
        l_xml = XmlData()
        l_xml.root = p_root_xml
        self._computer_xml(l_xml)
        self._house_xml(l_xml)
        return l_xml

    def LoadComputer(self, p_pyhouse_obj):
        pass

    def LoadHouse(self, p_pyhouse_obj):
        p_pyhouse_obj.House.FamilyData = familyAPI(p_pyhouse_obj).LoadFamilyTesting()
        housingAPI(p_pyhouse_obj).LoadXml(p_pyhouse_obj)
        return

    def setUp(self):
        self.BuildPyHouseObj()

#  ## END DBK
