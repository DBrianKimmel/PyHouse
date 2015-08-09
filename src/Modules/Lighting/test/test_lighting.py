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
from test.xml_data import XML_LONG
from test.testing_mixin import SetupPyHouseObj
from Modules.Utilities.tools import PrettyPrintAny
from Modules.Lighting.test.xml_controllers import \
        TESTING_CONTROLLER_NAME_1, \
        TESTING_CONTROLLER_NAME_2
from Modules.Core.test.xml_device import \
        TESTING_DEVICE_FAMILY
from Modules.Lighting.test.xml_lights import \
        TESTING_LIGHTING_LIGHTS_NAME_1, \
        TESTING_LIGHTING_LIGHTS_NAME_2


class SetupMixin(object):

    def setUp(self, p_root):
        self.m_pyhouse_obj = SetupPyHouseObj().BuildPyHouseObj(p_root)
        self.m_xml = SetupPyHouseObj().BuildXml(p_root)
        self.m_light_obj = LightData()
        self.m_api = lightingAPI(self.m_pyhouse_obj)
        self.m_family = familyAPI(self.m_pyhouse_obj).LoadFamilyTesting()
        self.m_pyhouse_obj.House.FamilyData = self.m_family


class A1_Setup(SetupMixin, unittest.TestCase):
    """ This section tests the master setup above this.
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))

    def test_01_PyHouse(self):
        self.assertIsNotNone(self.m_pyhouse_obj.Xml)

    def test_02_XML(self):
        self.assertIsNotNone(self.m_xml.house_div)

    def test_03_Light(self):
        self.assertEqual(self.m_light_obj.Name, 'Undefined BaseObject')

    def test_04_Api(self):
        self.assertIsNotNone(self.m_api)


class A2_XML(SetupMixin, unittest.TestCase):
    """ This section tests the reading and writing of XML used by Lights.
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))

    def test_01_Version(self):
        self.assertEqual(self.m_pyhouse_obj.Xml.XmlVersion, '1.4.0')

    def test_02_XmlTags(self):
        """ Be sure that the XML contains the right stuff.
        """
        self.assertEqual(self.m_xml.root.tag, 'PyHouse')
        self.assertEqual(self.m_xml.house_div.tag, 'HouseDivision')
        self.assertEqual(self.m_xml.lighting_sect.tag, 'LightingSection')
        self.assertEqual(self.m_xml.light_sect.tag, 'LightSection')
        self.assertEqual(self.m_xml.light.tag, 'Light')


class A3_Utility(SetupMixin, unittest.TestCase):
    """ This section tests the utility class
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))

    def test_01_SetupLighting(self):
        l_xml = self.m_api._setup_lighting(self.m_pyhouse_obj)
        self.assertTrue(l_xml.find('ButtonSection') is not None)
        self.assertTrue(l_xml.find('ControllerSection') is not None)
        self.assertTrue(l_xml.find('LightSection') is not None)

    def test_02_Controller(self):
        l_xml = self.m_api._setup_lighting(self.m_pyhouse_obj)
        l_version = '1.4.0'
        l_dict = self.m_api._read_controllers(self.m_pyhouse_obj, l_xml, l_version)
        self.assertEqual(len(l_dict), 2)
        # PrettyPrintAny(l_dict[0], 'Controllers')
        self.assertEqual(l_dict[0].Name, TESTING_CONTROLLER_NAME_1)
        self.assertEqual(l_dict[0].DeviceFamily, TESTING_DEVICE_FAMILY)
        self.assertEqual(l_dict[1].Name, TESTING_CONTROLLER_NAME_2)

    def test_03_ReadLighting(self):
        """Read all the lighting info (Buttons, Controllers, Lights)
        """
        l_obj = self.m_api._read_lighting_xml(self.m_pyhouse_obj)
        self.assertEqual(len(l_obj.Buttons), 2)
        self.assertEqual(len(l_obj.Controllers), 2)
        self.assertEqual(len(l_obj.Lights), 2)
        self.assertEqual(l_obj.Buttons[0].Name, 'Insteon Button')
        self.assertEqual(l_obj.Buttons[1].Name, 'UPB Button')
        self.assertEqual(l_obj.Controllers[0].Name, TESTING_CONTROLLER_NAME_1)
        self.assertEqual(l_obj.Controllers[1].Name, TESTING_CONTROLLER_NAME_2)
        self.assertEqual(l_obj.Lights[0].Name, TESTING_LIGHTING_LIGHTS_NAME_1)
        self.assertEqual(l_obj.Lights[1].Name, TESTING_LIGHTING_LIGHTS_NAME_2)

    def test_03_Write(self):
        self.m_api._read_lighting_xml(self.m_pyhouse_obj)
        l_obj = self.m_pyhouse_obj.House
        l_xml = ET.Element('HouseDivision')
        self.m_api._write_lighting_xml(l_obj, l_xml)
        # PrettyPrintAny(l_xml, 'XML')
        self.assertEqual(l_xml.find('HouseDivision').text, 1)

    def test_04_FamilyData(self):
        # PrettyPrintAny(self.m_pyhouse_obj.House.FamilyData, 'FamilyData')
        pass

class B1_Utility(SetupMixin, unittest.TestCase):

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))

    def test_01_FindFull(self):
        l_web_obj = LightData()
        l_web_obj.Name = 'dr_chand'
        self.m_api._read_lighting_xml(self.m_pyhouse_obj)
        l_light = self.m_api._find_full_obj(self.m_pyhouse_obj.House.Lights, l_web_obj)
        # PrettyPrintAny(l_light, 'Light')
        self.assertEqual(l_light.Name, 'dr_chand')
        #
        l_web_obj.Name = 'NoSuchLight'
        l_light = self.m_api._find_full_obj(self.m_pyhouse_obj.House.Lights, l_web_obj)
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
