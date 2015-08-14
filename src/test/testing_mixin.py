"""
-*- test-case-name: PyHouse.src.test.test_testing_mixin -*-

@name:      PyHouse/src/test/testing_mixin.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2013-2015 by D. Brian Kimmel
@license:   MIT License
@note:      Created on Jun 40, 2013
@summary:   Test handling the information for a house.

"""

# Import system type stuff
import platform
import logging
import sys

# Import PyMh files and modules.
from Modules.Core.data_objects import \
            PyHouseData, PyHouseAPIs, \
            CoreServicesInformation, \
            ComputerInformation, ComputerAPIs, \
            HouseInformation, HouseAPIs, \
            LocationData, \
            TwistedInformation, \
            XmlInformation
from Modules.Utilities.tools import PrettyPrintAny
from Modules.Computer import logging_pyh as Logger
LOG = Logger.getLogger('PyHouse').addHandler(logging.StreamHandler(stream = sys.stderr))


class XmlData(object):
    """
    Testing XML infrastructure
        PyHouse
            Divisions
                Sections
                    Item XML
    """
    def __init__(self):
        self.root = None
        self.house_div = None
        self.button_sect = None
        self.button = None
        self.controller_sect = None
        self.controller = None
        self.light_sect = None
        self.light = None
        self.location_sect = None
        self.room_sect = None
        self.room = None
        self.schedule_sect = None
        self.schedule = None
        self.thermostat_sect = None
        self.thermostat = None
        #
        self.computer_div = None
        self.internet_sect = None
        self.locater_sect = None
        self.mqtt_sect = None
        self.updater_sect = None
        self.log_sect = None
        self.web_sect = None
        #
        self.node_sect = None
        self.node = None
        self.interface_sect = None
        self.interface = None


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
        return l_ret

    def _build_services(self):
        l_ret = CoreServicesInformation()
        return l_ret

    def _build_house(self):
        l_ret = HouseInformation()
        l_ret.Name = 'Test House'
        l_ret.Active = True
        l_ret.Key = 0
        l_ret.Location = LocationData()
        return l_ret

    def _build_computer(self):
        l_ret = ComputerInformation()
        return l_ret

    def _build_apis(self):
        l_apis = PyHouseAPIs()
        l_apis.Computer = ComputerAPIs()
        l_apis.House = HouseAPIs()
        return l_apis

    def BuildPyHouseObj(self, p_root):
        l_pyhouse_obj = PyHouseData()
        l_pyhouse_obj.APIs = self._build_apis()
        l_pyhouse_obj.Computer = self._build_computer()
        l_pyhouse_obj.House = self._build_house()
        l_pyhouse_obj.Services = self._build_services()
        l_pyhouse_obj.Twisted = self._build_twisted()
        l_pyhouse_obj.Xml = self._build_xml(p_root)
        l_pyhouse_obj.Computer.Name = platform.node()
        return l_pyhouse_obj

    def BuildXml(self, p_root_xml):
        l_xml = XmlData()
        l_xml.root = p_root_xml
        try:
            l_xml.house_div = l_xml.root.find('HouseDivision')
            #
            l_xml.irrigation_sect = l_xml.house_div.find('IrrigationSection')
            l_xml.location_sect = l_xml.house_div.find('LocationSection')
            l_xml.room_sect = l_xml.house_div.find('RoomSection')
            l_xml.schedule_sect = l_xml.house_div.find('ScheduleSection')
            l_xml.thermostat_sect = l_xml.house_div.find('ThermostatSection')
            #
            l_xml.lighting_sect = l_xml.house_div.find('LightingSection')
            l_xml.button_sect = l_xml.lighting_sect.find('ButtonSection')
            l_xml.controller_sect = l_xml.lighting_sect.find('ControllerSection')
            l_xml.light_sect = l_xml.lighting_sect.find('LightSection')
            #
            l_xml.button = l_xml.button_sect.find('Button')
            l_xml.controller = l_xml.controller_sect.find('Controller')
            l_xml.irrigation_system = l_xml.irrigation_sect.find('IrrigationSystem')
            l_xml.irrigation_zone = l_xml.irrigation_system.find('Zone')
            l_xml.light = l_xml.light_sect.find('Light')
            l_xml.room = l_xml.room_sect.find('Room')
            l_xml.schedule = l_xml.schedule_sect.find('Schedule')
            l_xml.thermostat = l_xml.thermostat_sect.find('Thermostat')
            #
            #
            #
            l_xml.computer_div = l_xml.root.find('ComputerDivision')
            #
            l_xml.node_sect = l_xml.computer_div.find('NodeSection')
            l_xml.node = l_xml.node_sect.find('Node')
            l_xml.interface_sect = l_xml.node.find('InterfaceSection')
            l_xml.interface = l_xml.interface_sect.find('Interface')
            #
            l_xml.internet_sect = l_xml.computer_div.find('InternetSection')
            l_xml.internet = l_xml.internet_sect.find('Internet')
            l_xml.locater_sect = l_xml.internet_sect.find('LocaterUrlSection')
            l_xml.updater_sect = l_xml.internet_sect.find('UpdaterUrlSection')
            #
            l_xml.mqtt_sect = l_xml.computer_div.find('MqttSection')
            l_xml.broker = l_xml.mqtt_sect.find('Broker')
            #
            l_xml.web_sect = l_xml.computer_div.find('WebSection')

        except AttributeError as e_err:
            print('ERROR {}'.format(e_err))
        return l_xml

    def setUp(self):
        self.BuildPyHouseObj()

# ## END DBK
