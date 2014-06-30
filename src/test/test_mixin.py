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

# Import PyMh files and modules.
from Modules.Core.data_objects import PyHouseData, PyHouseAPIs, \
            CoreServicesInformation, \
            ComputerInformation, \
            HouseInformation, HouseObjs, \
            TwistedInformation, \
            XmlInformation
from Modules.utils.tools import PrettyPrintAny


class SetupPyHouseObj(object):
    """
    """

    def BuildPyHouse(self):
        l_ret = PyHouseData()
        l_ret.APIs = PyHouseAPIs
        l_ret.Computer = ComputerInformation()
        l_ret.House = HouseInformation()
        l_ret.House.OBJs = HouseObjs()
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
        #
        self.m_computer_div_xml = self.m_root_xml.find('ComputerDivision')
        self.m_internet_sect_xml = self.m_computer_div_xml.find('InternetSection')
        self.m_log_sect_xml = self.m_computer_div_xml.find('LogSection')
        self.m_node_sect_xml = self.m_computer_div_xml.find('InternetSection')
        self.m_web_sect_xml = self.m_computer_div_xml.find('WebSection')
        self.m_dynamic_dns_sect_xml = self.m_internet_xml.find('DynamicDnsSection')


class Setup(SetupPyHouseObj):

    def __init__(self):
        self.m_pyhouse_obj = self.BuildPyHouse()
        print('test_mixin.Setup()')
        # PrettyPrintAny(self, 'test_mixin - Setup() - self')
        # PrettyPrintAny(self.m_pyhouse_obj, 'test_mixin - Setup() - pyhouse_obj')

# ## END DBK
