"""
@name: PyHouse/src/Modules/hvac/test/test_thermostat.py
@author: D. Brian Kimmel
@contact: <d.briankimmel@gmail.com
@copyright: 2013-2014 by D. Brian Kimmel
@license: MIT License
@note: Created on Apr 14, 2013
@summary: This module is for testing local node data.

"""

# Import system type stuff
import xml.etree.ElementTree as ET
from twisted.trial import unittest

# Import PyMh files and modules.
from Modules.Core.data_objects import ThermostatData
from Modules.hvac import thermostat
from Modules.housing import house
from Modules.web import web_utils
from Modules.Core import setup
from Modules.utils.tools import PrettyPrintAny
from test import xml_data


class SetupMixin(object):
    """
    """

    def setUp(self):
        self.m_pyhouse_obj = setup.build_pyhouse_obj(self)
        self.m_pyhouse_obj.Xml.XmlRoot = self.m_root_xml
        self.m_thermostat_obj = ThermostatData()
        self.m_api = thermostat.API()
        self.m_pyhouse_obj = house.API().update_pyhouse_obj(self.m_pyhouse_obj)
        return self.m_pyhouse_obj


class Test_02_XML(SetupMixin, unittest.TestCase):
    """
    This section will verify the XML in the 'Modules.test.xml_data' file is correct and what the node_local module can read/write.
    """

    def setUp(self):
        self.m_root_xml = ET.fromstring(xml_data.XML_LONG)
        self.m_pyhouse_obj = SetupMixin.setUp(self)
        house.API().update_pyhouse_obj(self.m_pyhouse_obj)
        self.m_house_div_xml = self.m_root_xml.find('HouseDivision')
        self.m_thermostat_sect_xml = self.m_house_div_xml.find('ThermostatSection')
        self.m_thermostat_xml = self.m_thermostat_sect_xml.find('Thermostat')


    def test_0201_FindXml(self):
        """ Be sure that the XML contains the right stuff.
        """
        self.assertEqual(self.m_root_xml.tag, 'PyHouse', 'Invalid XML - not a PyHouse XML config file')
        self.assertEqual(self.m_house_div_xml.tag, 'HouseDivision', 'XML - No House Division')
        self.assertEqual(self.m_thermostat_sect_xml.tag, 'ThermostatSection', 'XML - No Thermostat section')
        self.assertEqual(self.m_thermostat_xml.tag, 'Thermostat', 'XML - No Thermostat Entry')
        PrettyPrintAny(self.m_pyhouse_obj, 'PyHouse_obj', 120)
        PrettyPrintAny(self.m_thermostat_xml, 'ThermoxtatXML', 120)

    def test_0211_ReadThermostatData(self):
        """
        """
        self.m_api._read_thermostat_data(self.m_thermostat_obj, self.m_thermostat_xml)
        PrettyPrintAny(self.m_thermostat_obj, 'ReadControllerData', 100)
        self.assertEqual(self.m_thermostat_obj.ControllerFamily, 'Insteon', 'Bad Controller Family')

    def test_0212_ReadFamilyData(self):
        """
        """
        self.m_thermostat_obj.ControllerFamily = 'Insteon'
        self.m_api._read_thermostat_data(self.m_thermostat_obj, self.m_thermostat_xml)
        PrettyPrintAny(self.m_thermostat_obj, 'ReadFamilyData', 100)

    def test_0231_ReadOneThermostatXml(self):
        """ Read in the xml file and fill in the lights
        """
        PrettyPrintAny(self.m_pyhouse_obj, '0231 PyHouse_obj', 120)
        l_entry = self.m_api.read_one_thermostat_xml(self.m_thermostat_xml, self.m_pyhouse_obj)
        self.assertEqual(l_entry.Active, True, 'Bad Active')
        self.assertEqual(l_entry.Name, 'Test Thermostat One', 'Bad Name')
        self.assertEqual(l_entry.Key, 0, 'Key')
        self.assertEqual(l_entry.HeatSetPoint, 71.0, 'Bad Heat SetPoint')
        self.assertEqual(l_entry.CoolSetPoint, 78.0, 'Bad Cool Se[Point')
        self.assertEqual(l_entry.CurrentTemperature, 76.0, 'Bad Current temperature')
        PrettyPrintAny(l_entry, 'One Thermostat Entry', 100)

    def test_0232_ReadAllThermostatsXml(self):
        l_controllers = self.m_api.read_all_thermostats_xml(self.m_pyhouse_obj)
        self.assertEqual(len(l_controllers), 1)
        PrettyPrintAny(l_controllers, 'All Thermostats', 100)

    def test_0251_WriteThermostatData(self):
        self.m_api._read_thermostat_data(self.m_thermostat_obj, self.m_thermostat_xml)
        PrettyPrintAny(self.m_thermostat_obj, 'WriteThermostatData', 100)

    def test_0252_WriteFamilyData(self):
        self.m_thermostat = self.m_api.read_all_thermostats_xml(self.m_pyhouse_obj)
        PrettyPrintAny(self.m_thermostat_obj, 'WriteFamilyData A', 100)
        PrettyPrintAny(self.m_pyhouse_obj.House.OBJs, 'WriteFamilyData B', 100)

        self.m_api._write_family_data(self.m_thermostat_obj, self.m_thermostat_xml, self.m_pyhouse_obj)
        PrettyPrintAny(self.m_thermostat_xml, 'WriteFamilyData C', 100)

    def test_0262_WriteOneThermostatXml(self):
        """ Write out the XML file for the location section
        """
        l_thermostat = self.m_api.read_one_thermostat_xml(self.m_thermostat_xml, self.m_pyhouse_obj)
        l_xml = self.m_api.write_one_thermostat_xml(l_thermostat, self.m_pyhouse_obj)
        PrettyPrintAny(l_xml, 'One thermostat', 100)

    def test_0264_WriteAllThermostatsXml(self):
        """ Write out the XML file for the location section
        """
        l_controllers = self.m_api.read_all_thermostats_xml(self.m_pyhouse_obj)
        l_xml = self.m_api.write_all_thermostats_xml(l_controllers, self.m_pyhouse_obj)
        PrettyPrintAny(l_xml, 'AllControllers', 100)

    def test_0281_CreateJson(self):
        """ Create a JSON object for Location.
        """
        l_thermostat = self.m_api.read_all_thermostats_xml(self.m_pyhouse_obj)
        l_json = unicode(web_utils.JsonUnicode().encode_json(l_thermostat))
        PrettyPrintAny(l_json, 'JSON', 120)


class Test_03_Start(SetupMixin, unittest.TestCase):
    """
    This section will verify the XML in the 'Modules.text.xml_data' file is correct and what the node_local module can read/write.
    """

    def setUp(self):
        self.m_root_xml = ET.fromstring(xml_data.XML_LONG)
        self.m_pyhouse_obj = SetupMixin.setUp(self)
        self.m_api = thermostat.API()

    def test_0301_Xml(self):
        """ Be sure that the XML contains the right stuff.
        """
        PrettyPrintAny(self.m_pyhouse_obj.Xml, 'PyHouse_Obj.Xml', 100)
        print('test_0301')
        l_xml = self.m_api.setup_xml(self.m_pyhouse_obj)
        PrettyPrintAny(l_xml, 'Xml', 100)

# ## END DBK
