"""
@name: PyHouse/src/Modules/Hvac/test/test_thermostat.py
@author: D. Brian Kimmel
@contact: D.BrianKimmel@gmail.com
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
from Modules.Hvac import thermostats
# from Modules.Housing import house
from Modules.Families import family
from Modules.Web import web_utils
from test.xml_data import XML_LONG
from test.testing_mixin import SetupPyHouseObj
from Modules.Utilities.tools import PrettyPrintAny


class SetupMixin(object):
    """
    """

    def setUp(self, p_root):
        self.m_pyhouse_obj = SetupPyHouseObj().BuildPyHouseObj(p_root)
        self.m_xml = SetupPyHouseObj().BuildXml(p_root)


class C01_XML(SetupMixin, unittest.TestCase):
    """
    This section will verify the XML in the 'Modules.test.xml_data' file is correct and what the node_local module can read/write.
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))
        self.m_pyhouse_obj.House.OBJs.FamilyData = family.API().build_lighting_family_info()
        self.m_api = thermostats.API()
        self.m_thermostat_obj = ThermostatData()


    def test_01_FindXml(self):
        """ Be sure that the XML contains the right stuff.
        """
        self.assertEqual(self.m_xml.root.tag, 'PyHouse', 'Invalid XML - not a PyHouse XML config file')
        self.assertEqual(self.m_xml.house_div.tag, 'HouseDivision', 'XML - No House Division')
        self.assertEqual(self.m_xml.thermostat_sect.tag, 'ThermostatSection', 'XML - No Thermostat section')
        self.assertEqual(self.m_xml.thermostat.tag, 'Thermostat', 'XML - No Thermostat Entry')
        PrettyPrintAny(self.m_pyhouse_obj.House.OBJs, 'PyHouse.House.OBJs', 115)
        PrettyPrintAny(self.m_xml.thermostat, 'ThermostatXML', 120)

    def test_11_ReadThermostatData(self):
        """
        """
        self.m_api._read_thermostat_data(self.m_thermostat_obj, self.m_xml.thermostat)
        PrettyPrintAny(self.m_thermostat_obj, 'ReadControllerData', 100)
        self.assertEqual(self.m_thermostat_obj.ControllerFamily, 'Insteon', 'Bad Controller Family')
        self.assertEqual(self.m_thermostat_obj.CoolSetPoint, 78.0, 'Bad CoolSetPoint')
        self.assertEqual(self.m_thermostat_obj.HeatSetPoint, 71.0, 'Bad HeatSetPoint')
        self.assertEqual(self.m_thermostat_obj.ThermostatMode, 'Cool', 'Bad ThermostatMode')
        self.assertEqual(self.m_thermostat_obj.ThermostatScale, 'F', 'Bad Thermostat Scale')
        self.assertEqual(self.m_thermostat_obj.CurrentTemperature, 76.0, 'Bad CurrentTemperature')

    def test_12_ReadFamilyData(self):
        """
        """
        self.m_thermostat_obj.ControllerFamily = 'Insteon'
        l_family = self.m_api._read_thermostat_data(self.m_thermostat_obj, self.m_xml.thermostat)
        PrettyPrintAny(self.m_thermostat_obj, 'ReadFamilyData', 100)
        PrettyPrintAny(l_family, 'Family', 100)

    def test_13_ReadOneThermostatXml(self):
        """ Read in the xml file and fill in the lights
        """
        PrettyPrintAny(self.m_pyhouse_obj, '0231 PyHouse_obj', 120)
        l_entry = self.m_api.read_one_thermostat_xml(self.m_xml.thermostat, self.m_pyhouse_obj)
        self.assertEqual(l_entry.Active, True, 'Bad Active')
        self.assertEqual(l_entry.Name, 'Test Thermostat One', 'Bad Name')
        self.assertEqual(l_entry.Key, 0, 'Key')
        self.assertEqual(l_entry.HeatSetPoint, 71.0, 'Bad Heat SetPoint')
        self.assertEqual(l_entry.CoolSetPoint, 78.0, 'Bad Cool Se[Point')
        self.assertEqual(l_entry.CurrentTemperature, 76.0, 'Bad Current temperature')
        PrettyPrintAny(l_entry, 'One Thermostat Entry', 100)

    def test_14_ReadAllThermostatsXml(self):
        l_controllers = self.m_api.read_all_thermostats_xml(self.m_pyhouse_obj)
        self.assertEqual(len(l_controllers), 1)
        PrettyPrintAny(l_controllers, 'All Thermostats', 100)

    def test_21_WriteThermostatData(self):
        self.m_api._read_thermostat_data(self.m_thermostat_obj, self.m_xml.thermostat)
        PrettyPrintAny(self.m_thermostat_obj, 'WriteThermostatData', 100)

    def test_22_WriteFamilyData(self):
        self.m_thermostat = self.m_api.read_all_thermostats_xml(self.m_pyhouse_obj)
        PrettyPrintAny(self.m_thermostat_obj, 'WriteFamilyData A', 100)
        PrettyPrintAny(self.m_pyhouse_obj.House.OBJs, 'WriteFamilyData B', 100)

        self.m_api._write_family_data(self.m_thermostat_obj, self.m_xml.thermostat, self.m_pyhouse_obj)
        PrettyPrintAny(self.m_xml.thermostat, 'WriteFamilyData C', 100)

    def test_23_WriteOneThermostatXml(self):
        """ Write out the XML file for the location section
        """
        l_thermostat = self.m_api.read_one_thermostat_xml(self.m_xml.thermostat, self.m_pyhouse_obj)
        l_xml = self.m_api.write_one_thermostat_xml(l_thermostat, self.m_pyhouse_obj)
        PrettyPrintAny(l_xml, 'One thermostat', 100)

    def test_24_WriteAllThermostatsXml(self):
        """ Write out the XML file for the location section
        """
        l_controllers = self.m_api.read_all_thermostats_xml(self.m_pyhouse_obj)
        l_xml = self.m_api.write_all_thermostats_xml(l_controllers, self.m_pyhouse_obj)
        PrettyPrintAny(l_xml, 'AllControllers', 100)

    def test_31_CreateJson(self):
        """ Create a JSON object for Location.
        """
        l_thermostat = self.m_api.read_all_thermostats_xml(self.m_pyhouse_obj)
        l_json = unicode(web_utils.JsonUnicode().encode_json(l_thermostat))
        PrettyPrintAny(l_json, 'JSON', 120)


# class Test_03_Start(testing_mixin.SetupMixin, unittest.TestCase):
    # """
    # This section will verify the XML in the 'Modules.text.xml_data' file is correct and what the node_local module can read/write.
    # """

    # def setUp(self):
    #    self.m_root_xml = ET.fromstring(xml_data.XML_LONG)
    #    # self.m_pyhouse_obj = SetupMixin.setUp(self)
    #    self.m_api = thermostat.API()

    # def test_0301_Xml(self):
    #    """ Be sure that the XML contains the right stuff.
    #    """
    #    PrettyPrintAny(self.m_pyhouse_obj.Xml, 'PyHouse_Obj.Xml', 100)
    #    print('test_0301')
    #    l_xml = self.m_api.setup_xml(self.m_pyhouse_obj)
    #    PrettyPrintAny(l_xml, 'Xml', 100)

# ## END DBK
