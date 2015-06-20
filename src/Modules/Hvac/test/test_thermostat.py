"""
@name:      PyHouse/src/Modules/Hvac/test/test_thermostat.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2013-2015 by D. Brian Kimmel
@license:   MIT License
@note:      Created on Apr 14, 2013
@summary:   This module is for testing local node data.

"""

# Import system type stuff
import xml.etree.ElementTree as ET
from twisted.trial import unittest

# Import PyMh files and modules.
from Modules.Core.data_objects import ThermostatData
from Modules.Core import conversions
from Modules.Hvac import thermostats
# from Modules.Housing import house
from Modules.Families import family
from Modules.Web import web_utils
from test.xml_data import XML_LONG, XML_EMPTY
from test.testing_mixin import SetupPyHouseObj
from Modules.Utilities.tools import PrettyPrintAny



class SetupMixin(object):
    """
    """

    def setUp(self, p_root):
        self.m_pyhouse_obj = SetupPyHouseObj().BuildPyHouseObj(p_root)
        self.m_pyhouse_obj.House.RefOBJs.FamilyData = family.API().build_lighting_family_info()
        self.m_xml = SetupPyHouseObj().BuildXml(p_root)
        self.m_api = thermostats.API()
        self.m_thermostat_obj = ThermostatData()



class C01_XML(SetupMixin, unittest.TestCase):
    """
    This section will verify the XML in the 'Modules.test.xml_data' file is correct and what the node_local module can read/write.
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))
        self.m_pyhouse_obj.House.RefOBJs.FamilyData = family.API().build_lighting_family_info()


    def test_01_FindXml(self):
        """ Be sure that the XML contains the right stuff.
        """
        self.assertEqual(self.m_xml.root.tag, 'PyHouse', 'Invalid XML - not a PyHouse XML config file')
        self.assertEqual(self.m_xml.house_div.tag, 'HouseDivision', 'XML - No House Division')
        self.assertEqual(self.m_xml.thermostat_sect.tag, 'ThermostatSection', 'XML - No Thermostat section')
        self.assertEqual(self.m_xml.thermostat.tag, 'Thermostat', 'XML - No Thermostat Entry')
        PrettyPrintAny(self.m_pyhouse_obj.House.DeviceOBJs, 'PyHouse.House.DeviceOBJs', 115)
        PrettyPrintAny(self.m_xml.thermostat_sect, 'Thermostat Sect', 120)
        PrettyPrintAny(self.m_xml.thermostat, 'ThermostatXML', 120)



class C02_Read(SetupMixin, unittest.TestCase):
    """
    This section will verify the XML in the 'Modules.test.xml_data' file is correct and what the node_local module can read/write.
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))
        self.m_pyhouse_obj.House.RefOBJs.FamilyData = family.API().build_lighting_family_info()

    def test_01_xml(self):
        PrettyPrintAny(self.m_xml.thermostat, 'Base', 100)
        PrettyPrintAny(self.m_pyhouse_obj.House.RefOBJs, 'House RefOBJs')
        PrettyPrintAny(self.m_pyhouse_obj.House.RefOBJs.FamilyData, 'Family')

    def test_02_Base(self):
        l_thermostat = self.m_api._read_thermostat_base(self.m_xml.thermostat)
        PrettyPrintAny(l_thermostat, 'Base', 100)
        self.assertEqual(l_thermostat.Name, 'Test Thermostat One')
        self.assertEqual(l_thermostat.Key, 0)
        self.assertEqual(l_thermostat.Active, True,)
        self.assertEqual(l_thermostat.UUID, None)

    def test_03_ThermostatData(self):
        """
        """
        l_thermostat = self.m_api._read_thermostat_base(self.m_xml.thermostat)
        self.m_api._read_thermostat_data(l_thermostat, self.m_xml.thermostat)
        PrettyPrintAny(l_thermostat, 'ReadControllerData', 100)
        self.assertEqual(l_thermostat.ControllerFamily, 'Insteon', 'Bad Controller Family')
        self.assertEqual(l_thermostat.CoolSetPoint, 78.0, 'Bad CoolSetPoint')
        self.assertEqual(l_thermostat.HeatSetPoint, 71.0, 'Bad HeatSetPoint')
        self.assertEqual(l_thermostat.ThermostatMode, 'Cool', 'Bad ThermostatMode')
        self.assertEqual(l_thermostat.ThermostatScale, 'F', 'Bad Thermostat Scale')
        self.assertEqual(l_thermostat.CurrentTemperature, 76.0, 'Bad CurrentTemperature')

    def test_04_FamilyData(self):
        """
        """
        l_thermostat = self.m_api._read_thermostat_base(self.m_xml.thermostat)
        self.m_api._read_thermostat_data(l_thermostat, self.m_xml.thermostat)
        PrettyPrintAny(l_thermostat, 'Thermostat 1', 100)
        self.m_api._read_family_data(self.m_pyhouse_obj, l_thermostat, self.m_xml.thermostat)
        PrettyPrintAny(l_thermostat, 'Thermostat 2', 100)
        self.assertEqual(l_thermostat.ControllerFamily, 'Insteon')
        self.assertEqual(l_thermostat.InsteonAddress, conversions.dotted_hex2int('18.C9.4A'))

    def test_05_OneThermostat(self):
        """ Read in the xml file and fill in the lights
        """
        PrettyPrintAny(self.m_pyhouse_obj, '0231 PyHouse_obj', 120)
        l_thermostat = self.m_api._read_one_thermostat_xml(self.m_pyhouse_obj, self.m_xml.thermostat)
        PrettyPrintAny(l_thermostat, 'Thermostat 1', 100)
        self.assertEqual(l_thermostat.Active, True, 'Bad Active')
        self.assertEqual(l_thermostat.Name, 'Test Thermostat One', 'Bad Name')
        self.assertEqual(l_thermostat.Key, 0, 'Key')
        self.assertEqual(l_thermostat.HeatSetPoint, 71.0, 'Bad Heat SetPoint')
        self.assertEqual(l_thermostat.CoolSetPoint, 78.0, 'Bad Cool SetPoint')
        self.assertEqual(l_thermostat.CurrentTemperature, 76.0, 'Bad Current temperature')
        PrettyPrintAny(l_thermostat, 'One Thermostat Entry', 100)

    def test_06_AllThermostats(self):
        l_thermostats = self.m_api.read_all_thermostats_xml(self.m_pyhouse_obj)
        PrettyPrintAny(l_thermostats, 'Thermostats')
        self.assertEqual(len(l_thermostats), 1)
        PrettyPrintAny(l_thermostats, 'All Thermostats', 100)



class C03_Write(SetupMixin, unittest.TestCase):
    """
    This section will verify the XML in the 'Modules.test.xml_data' file is correct and what the node_local module can read/write.
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))
        self.m_pyhouse_obj.House.RefOBJs.FamilyData = family.API().build_lighting_family_info()

    def test_01_Base(self):
        l_thermostat = self.m_api._read_one_thermostat_xml(self.m_pyhouse_obj, self.m_xml.thermostat)
        l_xml = self.m_api._write_thermostat_base(l_thermostat)
        PrettyPrintAny(l_xml, 'XML')

    def test_02_ThermostatData(self):
        l_thermostat = self.m_api._read_thermostat_data(self.m_thermostat_obj, self.m_xml.thermostat)
        l_xml = self.m_api._write_thermostat_base(l_thermostat)
        l_xml = self.m_api._write_thermostat_data(l_xml, l_thermostat)
        PrettyPrintAny(l_xml, 'WriteThermostatData', 100)

    def test_03_FamilyData(self):
        l_thermostat = self.m_api._read_one_thermostat_xml(self.m_pyhouse_obj, self.m_xml.thermostat)
        PrettyPrintAny(l_thermostat, 'Thermostat')
        l_out_xml = self.m_api._write_thermostat_base(l_thermostat)
        self.m_api._write_thermostat_data(l_out_xml, l_thermostat)
        self.m_api._write_thermostat_family(self.m_pyhouse_obj, l_out_xml, l_thermostat)
        PrettyPrintAny(l_out_xml, 'xml')

    def test_04_One(self):
        """ Write out the XML file for the location section
        """
        l_thermostat = self.m_api._read_one_thermostat_xml(self.m_pyhouse_obj, self.m_xml.thermostat)
        l_out_xml = self.m_api._write_one_thermostat_xml(self.m_pyhouse_obj, l_thermostat)
        PrettyPrintAny(l_out_xml, 'One thermostat', 100)

    def test_05_All(self):
        """ Write out the XML file for the location section
        """
        l_thermostats = self.m_api.read_all_thermostats_xml(self.m_pyhouse_obj)
        self.m_pyhouse_obj.House.DeviceOBJs.Thermostats = l_thermostats
        PrettyPrintAny(self.m_pyhouse_obj.House.DeviceOBJs.Thermostats, 'PyHouse')
        PrettyPrintAny(l_thermostats, 'Thermostats')
        l_out_xml = self.m_api.write_all_thermostats_xml(self.m_pyhouse_obj)
        PrettyPrintAny(l_out_xml, 'AllControllers')



class C04_JSON(SetupMixin, unittest.TestCase):
    """
    This section will verify the XML in the 'Modules.test.xml_data' file is correct and what the node_local module can read/write.
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))
        self.m_pyhouse_obj.House.RefOBJs.FamilyData = family.API().build_lighting_family_info()

    def test_01_Create(self):
        """ Create a JSON object for Location.
        """
        l_thermostat = self.m_api.read_all_thermostats_xml(self.m_pyhouse_obj)
        l_json = unicode(web_utils.JsonUnicode().encode_json(l_thermostat))
        PrettyPrintAny(l_json, 'JSON', 120)


class C05_Empty(SetupMixin, unittest.TestCase):
    """
    This section will verify the XML in the 'Modules.test.xml_data' file is correct and what the node_local module can read/write.
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_EMPTY))
        self.m_pyhouse_obj.House.RefOBJs.FamilyData = family.API().build_lighting_family_info()

    def test_01_ReadAll(self):
        l_thermostats = self.m_api.read_all_thermostats_xml(self.m_pyhouse_obj)
        PrettyPrintAny(l_thermostats, 'Thermostats')
        self.assertEqual(len(l_thermostats), 0)
        PrettyPrintAny(l_thermostats, 'All Thermostats', 100)

    def test_02_WriteAll(self):
        """ Write out the XML file for the location section
        """
        l_thermostats = self.m_api.read_all_thermostats_xml(self.m_pyhouse_obj)
        self.m_pyhouse_obj.House.DeviceOBJs.Thermostats = l_thermostats
        PrettyPrintAny(self.m_pyhouse_obj.House.DeviceOBJs.Thermostats, 'PyHouse')
        PrettyPrintAny(l_thermostats, 'Thermostats')
        l_out_xml = self.m_api.write_all_thermostats_xml(self.m_pyhouse_obj)
        PrettyPrintAny(l_out_xml, 'AllControllers')

    def test_03_Json(self):
        """ Create a JSON object for Location.
        """
        l_thermostat = self.m_api.read_all_thermostats_xml(self.m_pyhouse_obj)
        l_json = unicode(web_utils.JsonUnicode().encode_json(l_thermostat))
        PrettyPrintAny(l_json, 'JSON', 120)


class C06_Util(SetupMixin, unittest.TestCase):
    """
    Test the Utilities.
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))
        self.m_pyhouse_obj.House.RefOBJs.FamilyData = family.API().build_lighting_family_info()

    def test_01_Xml(self):
        l_xml = self.m_api.setup_xml(self.m_pyhouse_obj)
        PrettyPrintAny(l_xml, 'XML')
        print(l_xml.tag)
        self.assertEqual(l_xml.tag, 'ThermostatSection')

# ## END DBK
