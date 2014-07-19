"""
@name: PyHouse/src/test/test_mixin.py
@author: D. Brian Kimmel
@contact: <d.briankimmel@gmail.com
@Copyright (c) 2013-2014 by D. Brian Kimmel
@license: MIT License
@note: Created on Jun 40, 2013
@summary: Test handling the information for a house.

"""

# Import system type stuff
import xml.etree.ElementTree as ET

# Import PyMh files and modules.
from Modules.Core.data_objects import PyHouseData, PyHouseAPIs, \
            CoreServicesInformation, \
            ComputerInformation, \
            HouseInformation, HouseObjs, \
            TwistedInformation, \
            XmlInformation
# from Modules.utils.tools import PrettyPrintAny
from test import xml_data


class SetupPyHouseObj(object):
    """
    """

    def _BuildHouse(self):
        l_ret = HouseInformation()
        l_ret.Name = 'Test House'
        l_ret.Active = True
        l_ret.Key = 0
        l_ret.OBJs = HouseObjs()
        return l_ret

    def BuildPyHouseObj(self):
        l_ret = PyHouseData()
        l_ret.APIs = PyHouseAPIs
        l_ret.Computer = ComputerInformation()
        l_ret.House = self._BuildHouse()
        l_ret.Services = CoreServicesInformation()
        l_ret.Twisted = TwistedInformation()
        l_ret.Xml = XmlInformation()
        return l_ret

    def BuildXml(self):
        self.m_house_div_xml = self.m_root_xml.find('HouseDivision')
        self.m_button_sect_xml = self.m_house_div_xml.find('ButtonSection')
        self.m_controller_sect_xml = self.m_house_div_xml.find('ControllerSection')
        self.m_family_sect_xml = self.m_house_div_xml.find('FamilySection')
        self.m_light_sect_xml = self.m_house_div_xml.find('LightSection')
        self.m_location_sect_xml = self.m_house_div_xml.find('LocationSection')
        self.m_room_sect_xml = self.m_house_div_xml.find('RoomSection')
        self.m_schedule_sect_xml = self.m_house_div_xml.find('ScheduleSection')
        self.m_thermostat_sect_xml = self.m_controller_sect_xml.find('ThermostatSection')
        self.m_button_xml = self.m_button_sect_xml.find('Button')
        self.m_controller_xml = self.m_house_div_xml.find('Controller')
        self.m_family_xml = self.m_house_div_xml.find('Family')
        self.m_light_xml = self.m_house_div_xml.find('Light')
        self.m_location_xml = self.m_house_div_xml.find('Location')
        self.m_room_xml = self.m_house_div_xml.find('Room')
        self.m_schedule_xml = self.m_house_div_xml.find('Schedule')
        self.m_thermostat_xml = self.m_controller_sect_xml.find('Thermostat')
        #
        self.m_computer_div_xml = self.m_root_xml.find('ComputerDivision')
        self.m_internet_sect_xml = self.m_computer_div_xml.find('InternetSection')
        self.m_log_sect_xml = self.m_computer_div_xml.find('LogSection')
        self.m_node_sect_xml = self.m_computer_div_xml.find('InternetSection')
        self.m_web_sect_xml = self.m_computer_div_xml.find('WebSection')
        self.m_dynamic_dns_sect_xml = self.m_internet_sect_xml.find('DynamicDnsSection')
        # PrettyPrintAny(self, 'TestMixin - Self', 100)

    def setUp(self):
        self.BuildPyHouseObj()


# class SetupMixin(SetupPyHouseObj):
#
#    def __init__(self):
#        self.m_pyhouse_obj = self.BuildPyHouse()
#        try:
#            self.m_root_xml
#        except (NameError, AttributeError):
#            self.m_root_xml = ET.fromstring(xml_data.XML_LONG)
#        self.BuildXml()
#        # PrettyPrintAny(self, 'TestMixin - Setup() -  Self', 100)
#
# ## END DBK
