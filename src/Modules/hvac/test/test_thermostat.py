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
from Modules.families import family
from Modules.web import web_utils
from Modules.utils.tools import PrettyPrintAny
from src.test import xml_data, test_mixin


class SetupMixin(object):
    """
    """

    def setUp(self):
        test_mixin.Setup()
        test_mixin.Setup().BuildPyHouse()
        self.m_pyhouse_obj = test_mixin.SetupPyHouseObj().BuildPyHouse()
        self.m_pyhouse_obj.House.OBJs.FamilyData = family.API().build_lighting_family_info()


class Test_02_XML(SetupMixin, unittest.TestCase):
    """
    This section will verify the XML in the 'Modules.text.xml_data' file is correct and what the node_local module can read/write.
    """

    def setUp(self):
        self.m_root_xml = ET.fromstring(xml_data.XML_LONG)
        SetupMixin.setUp(self)

        self.m_house_div_xml = self.m_root_xml.find('HouseDivision')
        self.m_thermostat_sect_xml = self.m_house_div_xml.find('ThermostatSection')
        self.m_thermostat_xml = self.m_thermostat_sect_xml.find('Thermostat')
        self.m_thermostat_obj = ThermostatData()

        self.m_api = thermostat.API()
        PrettyPrintAny(self.m_pyhouse_obj, 'PyHouse_obj', 120)

    def test_0202_FindXml(self):
        """ Be sure that the XML contains the right stuff.
        """
        self.assertEqual(self.m_root_xml.tag, 'PyHouse', 'Invalid XML - not a PyHouse XML config file')
        self.assertEqual(self.m_house_div_xml.tag, 'HouseDivision', 'XML - No House Division')
        self.assertEqual(self.m_thermostat_sect_xml.tag, 'ThermostatSection', 'XML - No Thermostat section')
        self.assertEqual(self.m_thermostat_xml.tag, 'Thermostat', 'XML - No Thermostat Entry')
        PrettyPrintAny(self.m_pyhouse_obj, 'PyHouse_obj', 120)
        PrettyPrintAny(self.m_pyhouse_obj.Xml, 'PyHouse_obj.Xml', 120)

    def test_0242_ReadOneThermostatXml(self):
        """ Read in the xml file and fill in the lights
        """
        l_entry = self.m_api.read_one_thermostat_xml(self.m_thermostat_xml)
        self.assertEqual(l_entry.Active, True, 'Bad Active')
        self.assertEqual(l_entry.Name, 'Test Thermostat One', 'Bad Name')
        self.assertEqual(l_entry.Key, 0, 'Key')
        self.assertEqual(l_entry.SetTemperature, 76.0, 'Bad Set Temperature')
        self.assertEqual(l_entry.CurrentTemperature, 76.0, 'Bad Current temperature')
        PrettyPrintAny(l_entry, 'One Thermostat Entry', 100)

    def test_0244_ReadAllThermostatsXml(self):
        l_controllers = self.m_api.read_all_thermostats_xml(self.m_thermostat_sect_xml)
        self.assertEqual(len(l_controllers), 1)
        PrettyPrintAny(l_controllers, 'All Thermostats', 100)

    def test_0262_WriteOneThermostatXml(self):
        """ Write out the XML file for the location section
        """
        l_thermostat = self.m_api.read_one_thermostat_xml(self.m_thermostat_xml)
        l_xml = self.m_api.write_one_thermostat_xml(l_thermostat)
        PrettyPrintAny(l_xml, 'One thermostat', 100)

    def test_0264_WriteAllThermostatsXml(self):
        """ Write out the XML file for the location section
        """
        l_controllers = self.m_api.read_all_thermostats_xml(self.m_thermostat_sect_xml)
        l_xml = self.m_api.write_all_thermostats_xml(l_controllers)
        PrettyPrintAny(l_xml, 'AllControllers', 100)

    def test_0281_CreateJson(self):
        """ Create a JSON object for Location.
        """
        l_thermostat = self.m_api.read_all_thermostats_xml(self.m_thermostat_sect_xml)
        l_json = unicode(web_utils.JsonUnicode().encode_json(l_thermostat))
        PrettyPrintAny(l_json, 'JSON', 120)


# ## END DBK
