"""
@name: PyHouse/src/Modules/families/UPB/test/test_Device_UPB.py
@author: D. Brian Kimmel
@contact: D.BrianKimmel@gmail.com
@Copyright (c) 2013-2014 by D. Brian Kimmel
@license: MIT License
@note: Created on Apr 8, 2013
@summary: This module is for testing UPB devices.

"""

# Import system type stuff
import xml.etree.ElementTree as ET
from twisted.trial import unittest

# Import PyMh files and modules.
from Modules.Core.data_objects import UPBData
from Modules.families.UPB import Device_UPB
from Modules.lights import lighting_lights
from Modules.hvac import thermostat
from Modules.housing import house
from Modules.Core import setup
from test import xml_data
from Modules.utils.tools import PrettyPrintAny


class SetupMixin(object):
    """
    """

    def setUp(self):
        self.m_pyhouse_obj.Xml.XmlRoot = self.m_root_xml
        self.m_thermostat_obj = UPBData()
        self.m_pyhouse_obj = house.API().update_pyhouse_obj(self.m_pyhouse_obj)
        # PrettyPrintAny(self.m_pyhouse_obj, 'SetupMixin.Setup - PyHouse_obj', 100)
        self.m_api = Device_UPB.API()
        self.m_thermostat_api = thermostat.API()
        self.m_light_api = lighting_lights.LightingLightsAPI(self.m_pyhouse_obj)
        return self.m_pyhouse_obj


class Test_02_ReadXML(SetupMixin, unittest.TestCase):
    """ This section tests the reading and writing of XML used by node_local.
    """

    def setUp(self):
        self.m_root_xml = ET.fromstring(xml_data.XML_LONG)
        self.m_pyhouse_obj = SetupMixin.setUp(self)
        house.API().update_pyhouse_obj(self.m_pyhouse_obj)
        self.m_house_div_xml = self.m_root_xml.find('HouseDivision')
        self.m_thermostat_sect_xml = self.m_house_div_xml.find('ThermostatSection')
        self.m_thermostat_xml = self.m_thermostat_sect_xml.find('Thermostat')
        self.m_light_sect_xml = self.m_house_div_xml.find('LightSection')
        self.m_light_xml = self.m_light_sect_xml.find('Light')


    def test_0202_FindXml(self):
        """ Be sure that the XML contains the right stuff.
        """
        self.assertEqual(self.m_root_xml.tag, 'PyHouse', 'Invalid XML - not a PyHouse XML config file')
        self.assertEqual(self.m_thermostat_sect_xml.tag, 'ThermostatSection', 'XML - No Thermostat section')
        self.assertEqual(self.m_thermostat_xml.tag, 'Thermostat', 'XML - No Thermostat Entry')
        self.assertEqual(self.m_light_sect_xml.tag, 'LightSection', 'XML - No Light section')
        self.assertEqual(self.m_light_xml.tag, 'Light', 'XML - No Light Entry')

    def test_0203_ReadOneLightXml(self):
        """ Read in the xml file and fill in the lights
        """
        l_entry = self.m_thermostat_api.read_one_thermostat_xml(self.m_thermostat_xml, self.m_pyhouse_obj)
        self.assertEqual(l_entry.Active, True, 'Bad Active')
        self.assertEqual(l_entry.Name, 'Test Thermostat One', 'Bad Name')

        l_light = self.m_light_api.read_one_light_xml(self.m_light_xml)
        l_insteon_obj = self.m_api.extract_device_xml(l_light, self.m_light_xml)
        PrettyPrintAny(l_insteon_obj)
        self.assertEqual(l_light.Name, 'Test LR Overhead', 'Bad Name')
        self.assertEqual(l_light.Key, 0, 'Bad Key')
        self.assertEqual(l_light.Active, True, 'Bad Active')
        self.assertEqual(l_light.UUID, 'ec9d9930-89c9-11e3-a1ab-082e5f8cdfd2', 'Bad UUID')
        self.assertEqual(l_light.InsteonAddress, 1122867, 'Bad Address')

# ## END DBK
