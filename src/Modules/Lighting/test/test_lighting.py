"""
@name:      PyHouse/src/Modules/Lighting/test/test_lighting.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2013-2015 by D. Brian Kimmel
@note:      Created on Apr 9, 2013
@license:   MIT License
@summary:   Test the home lighting system automation.

Passed all 0 tests.  DBK 2015-07-21
"""

# Import system type stuff
from twisted.trial import unittest
import xml.etree.ElementTree as ET

# Import PyMh files and modules.
from Modules.Core.data_objects import LightData
from Modules.Families.family import API as familyAPI
from Modules.Lighting.lighting import API as lightingAPI
from test.xml_data import XML_LONG, XML_LONG_1_3
from test.testing_mixin import SetupPyHouseObj
from Modules.Utilities.tools import PrettyPrintAny


class SetupMixin(object):

    def setUp(self, p_root):
        self.m_pyhouse_obj = SetupPyHouseObj().BuildPyHouseObj(p_root)
        self.m_xml = SetupPyHouseObj().BuildXml(p_root)
        self.m_light_obj = LightData()
        self.m_api = lightingAPI(self.m_pyhouse_obj)
        self.m_family = familyAPI(self.m_pyhouse_obj).LoadFamilyTesting()
        self.m_pyhouse_obj.House.RefOBJs.FamilyData = self.m_family


class A1_Setup(SetupMixin, unittest.TestCase):
    """ This section tests the master setup above this.
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG_1_3))

    def test_01_PyHouse(self):
        # PrettyPrintAny(self.m_pyhouse_obj, 'PyHouse')
        pass

    def test_02_XML(self):
        # PrettyPrintAny(self.m_xml, 'm_xml')
        pass

    def test_03_Light(self):
        # PrettyPrintAny(self.m_light_obj, 'm_light_obj')
        pass

    def test_04_Api(self):
        # PrettyPrintAny(self.m_api, 'm_api')
        pass


class A2_XML_1_3(SetupMixin, unittest.TestCase):
    """ This section tests the reading and writing of XML used by node_local.
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG_1_3))

    def test_01_Version(self):
        # PrettyPrintAny(self.m_pyhouse_obj.Xml, 'PyHouse.Xml')
        self.assertEqual(self.m_pyhouse_obj.Xml.XmlVersion, '1.4.0')

    def test_02_XmlTags(self):
        """ Be sure that the XML contains the right stuff.
        """
        # PrettyPrintAny(self.m_xml, 'Tags')
        self.assertEqual(self.m_xml.root.tag, 'PyHouse', 'Invalid XML - not a PyHouse XML config file')
        self.assertEqual(self.m_xml.house_div.tag, 'HouseDivision')
        self.assertEqual(self.m_xml.lighting_sect.tag, 'LightingSection')
        self.assertEqual(self.m_xml.light_sect.tag, 'LightSection', 'XML - No Lights section')
        self.assertEqual(self.m_xml.light.tag, 'Light', 'XML - No Light')


class A3_XML_1_4(SetupMixin, unittest.TestCase):
    """ This section tests the reading and writing of XML used by node_local.
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))

    def test_01_PyHouse(self):
        # PrettyPrintAny(self.m_pyhouse_obj, 'PyHouse')
        # PrettyPrintAny(self.m_pyhouse_obj.Xml, 'PyHouse.Xml')
        pass

    def test_02_XmlTags(self):
        """ Be sure that the XML contains the right stuff.
        """
        # PrettyPrintAny(self.m_xml, 'Tags')
        self.assertEqual(self.m_xml.root.tag, 'PyHouse', 'Invalid XML - not a PyHouse XML config file')
        self.assertEqual(self.m_xml.house_div.tag, 'HouseDivision')
        self.assertEqual(self.m_xml.lighting_sect.tag, 'LightingSection')
        self.assertEqual(self.m_xml.light_sect.tag, 'LightSection', 'XML - No Lights section')
        self.assertEqual(self.m_xml.light.tag, 'Light', 'XML - No Light')


class A4_Utility(SetupMixin, unittest.TestCase):
    """ This section tests the utility class
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))

    def test_01_SetupLighting(self):
        l_xml = self.m_api._setup_lighting(self.m_pyhouse_obj)
        # PrettyPrintAny(l_xml, 'Lighting')
        self.assertTrue(l_xml.find('ButtonSection') is not None)
        self.assertTrue(l_xml.find('ControllerSection') is not None)
        self.assertTrue(l_xml.find('LightSection') is not None)

    def test_02_Controller(self):
        l_xml = self.m_api._setup_lighting(self.m_pyhouse_obj)
        l_version = '1.4.0'
        # PrettyPrintAny(l_xml, 'XML')
        l_ret = self.m_api._read_controllers(self.m_pyhouse_obj, l_xml, l_version)
        # PrettyPrintAny(l_ret, 'Controllers')

    def test_03_ReadLighting(self):
        """Read all the lighting info (Buttons, Controllers, Lights)
        """
        l_obj = self.m_api._read_lighting_xml(self.m_pyhouse_obj)
        # PrettyPrintAny(l_obj, 'ReadObj')
        # PrettyPrintAny(self.m_pyhouse_obj.House.DeviceOBJs, 'Test 02 Read Lighting')
        self.assertEqual(l_obj.Buttons[0].Name, 'Insteon Button')
        self.assertEqual(l_obj.Buttons[1].Name, 'UPB Button')
        self.assertEqual(l_obj.Controllers[0].Name, 'Insteon Serial Controller')
        self.assertEqual(l_obj.Controllers[1].Name, 'UPB USB Controller')
        self.assertEqual(l_obj.Lights[0].Name, 'Insteon Light')
        self.assertEqual(l_obj.Lights[1].Name, 'UPB Light')

    def test_03_Write(self):
        self.m_api._read_lighting_xml(self.m_pyhouse_obj)
        l_obj = self.m_pyhouse_obj.House.DeviceOBJs
        l_xml = ET.Element('HouseDivision')
        # PrettyPrintAny(l_obj, 'Lighting')
        self.m_api._write_lighting_xml(l_obj, l_xml)
        # PrettyPrintAny(l_xml, 'XML')

    def test_04_FamilyData(self):
        # PrettyPrintAny(self.m_pyhouse_obj.House.RefOBJs, 'House')
        # PrettyPrintAny(self.m_pyhouse_obj.House.RefOBJs.FamilyData, 'FamilyData')
        pass

class B1_Utility(SetupMixin, unittest.TestCase):

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))

    def test_01_FindFull(self):
        l_web_obj = LightData()
        l_web_obj.Name = 'dr_chand'
        self.m_api._read_lighting_xml(self.m_pyhouse_obj)
        l_light = self.m_api._find_full_obj(self.m_pyhouse_obj.House.DeviceOBJs.Lights, l_web_obj)
        # PrettyPrintAny(l_light, 'Light')
        self.assertEqual(l_light.Name, 'dr_chand')
        #
        l_web_obj.Name = 'NoSuchLight'
        l_light = self.m_api._find_full_obj(self.m_pyhouse_obj.House.DeviceOBJs.Lights, l_web_obj)
        self.assertEqual(l_light, None)


class C1_Ops(SetupMixin, unittest.TestCase):
    """ This section tests the operations
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))

    def xxtest_01_GetApi(self):
        l_light = self.m_light_obj
        l_light.Name = 'Garage'
        l_light.DeviceFamily = 'Insteon'
        l_api = self.m_api._get_api_for_family(self.m_pyhouse_obj, self.m_light_obj)
        print('Api = {0:}'.format(l_api))

# ## END DBK
