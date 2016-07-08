"""
@name:      PyHouse/src/Modules/Lighting/test/test_lighting.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2013-2016 by D. Brian Kimmel
@note:      Created on Apr 9, 2013
@license:   MIT License
@summary:   Test the home lighting system automation.

Passed all 12 tests.  DBK 2016-06-24

"""

__updated__ = '2016-07-07'


# Import system type stuff
from twisted.trial import unittest
import xml.etree.ElementTree as ET

# Import PyMh files and modules.
from Modules.Core.data_objects import LightData
from Modules.Families.family import API as familyAPI
from Modules.Lighting.lighting import API as lightingAPI
from test.xml_data import XML_LONG
from test.testing_mixin import SetupPyHouseObj
from Modules.Lighting.test.xml_controllers import \
        TESTING_CONTROLLER_NAME_0, \
        TESTING_CONTROLLER_NAME_1
from Modules.Core.test.xml_device import \
        TESTING_DEVICE_FAMILY_INSTEON
from Modules.Utilities.debug_tools import PrettyFormatAny
from Modules.Lighting.test.xml_lights import TESTING_LIGHT_NAME_0, TESTING_LIGHT_NAME_1
from Modules.Lighting.test.xml_buttons import TESTING_LIGHTING_BUTTON_NAME_0, TESTING_LIGHTING_BUTTON_NAME_1


class SetupMixin(object):

    def setUp(self, p_root):
        self.m_pyhouse_obj = SetupPyHouseObj().BuildPyHouseObj(p_root)
        self.m_xml = SetupPyHouseObj().BuildXml(p_root)
        self.m_light_obj = LightData()
        self.m_api = lightingAPI(self.m_pyhouse_obj)
        self.m_family = familyAPI(self.m_pyhouse_obj).LoadFamilyTesting()
        self.m_pyhouse_obj.House.FamilyData = self.m_family
        self.m_version = '1.4.0'


class A1_Setup(SetupMixin, unittest.TestCase):
    """ This section tests the master setup above this.
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))

    def test_1_SetupLighting(self):
        """Verify that we can find items we need in the test XML
        """
        l_xml = self.m_api._setup_lighting(self.m_pyhouse_obj)
        self.assertEqual(l_xml.find('ButtonSection').tag, 'ButtonSection')
        self.assertEqual(l_xml.find('ControllerSection').tag, 'ControllerSection')
        self.assertEqual(l_xml.find('LightSection').tag, 'LightSection')

    def test_2_PyHouse(self):
        self.assertIsNotNone(self.m_pyhouse_obj.Xml)

    def test_3_XML(self):
        self.assertIsNotNone(self.m_xml.house_div)

    def test_4_Light(self):
        self.assertEqual(self.m_light_obj.Name, 'undefined baseobject')

    def test_5_Api(self):
        self.assertIsNotNone(self.m_api)


class A2_XML(SetupMixin, unittest.TestCase):
    """ This section tests the reading and writing of XML used by Lights.
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))

    def test_01_Version(self):
        self.assertGreater(self.m_pyhouse_obj.Xml.XmlVersion, '1.4.0')

    def test_02_XmlTags(self):
        """ Be sure that the XML contains the right stuff.
        """
        self.assertEqual(self.m_xml.root.tag, 'PyHouse')
        self.assertEqual(self.m_xml.house_div.tag, 'HouseDivision')
        self.assertEqual(self.m_xml.lighting_sect.tag, 'LightingSection')
        self.assertEqual(self.m_xml.light_sect.tag, 'LightSection')
        self.assertEqual(self.m_xml.light.tag, 'Light')


class B1_Read(SetupMixin, unittest.TestCase):
    """ This section tests the utility class
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))

    def test_1_Button(self):
        """Utility.
        """
        l_xml = self.m_api._setup_lighting(self.m_pyhouse_obj)
        l_buttons = self.m_api._read_buttons(self.m_pyhouse_obj, l_xml)
        self.assertEqual(len(l_buttons), 2)
        self.assertEqual(l_buttons[0].Name, TESTING_LIGHTING_BUTTON_NAME_0)
        self.assertEqual(l_buttons[0].DeviceFamily, TESTING_DEVICE_FAMILY_INSTEON)
        self.assertEqual(l_buttons[1].Name, TESTING_LIGHTING_BUTTON_NAME_1)

    def test_2_Controller(self):
        """Utility.
        """
        l_xml = self.m_api._setup_lighting(self.m_pyhouse_obj)
        l_dict = self.m_api._read_controllers(self.m_pyhouse_obj, l_xml)
        self.assertEqual(len(l_dict), 2)
        self.assertEqual(l_dict[0].Name, TESTING_CONTROLLER_NAME_0)
        self.assertEqual(l_dict[0].DeviceFamily, TESTING_DEVICE_FAMILY_INSTEON)
        self.assertEqual(l_dict[1].Name, TESTING_CONTROLLER_NAME_1)

    def test_3_Light(self):
        """Utility.
        """
        l_xml = self.m_api._setup_lighting(self.m_pyhouse_obj)
        l_lights = self.m_api._read_lights(self.m_pyhouse_obj, l_xml)
        self.assertEqual(len(l_lights), 2)
        self.assertEqual(l_lights[0].Name, TESTING_LIGHT_NAME_0)
        self.assertEqual(l_lights[0].DeviceFamily, TESTING_DEVICE_FAMILY_INSTEON)
        self.assertEqual(l_lights[1].Name, TESTING_LIGHT_NAME_1)

    def test_4_Lighting(self):
        """Read all the lighting info (Buttons, Controllers, Lights)
        """
        l_obj = self.m_api._read_lighting_xml(self.m_pyhouse_obj)
        self.assertEqual(len(l_obj.Buttons), 2)
        self.assertEqual(len(l_obj.Controllers), 2)
        self.assertEqual(len(l_obj.Lights), 2)
        self.assertEqual(l_obj.Buttons[0].Name, TESTING_LIGHTING_BUTTON_NAME_0)
        self.assertEqual(l_obj.Buttons[1].Name, TESTING_LIGHTING_BUTTON_NAME_1)
        self.assertEqual(l_obj.Controllers[0].Name, TESTING_CONTROLLER_NAME_0)
        self.assertEqual(l_obj.Controllers[1].Name, TESTING_CONTROLLER_NAME_1)
        self.assertEqual(l_obj.Lights[0].Name, TESTING_LIGHT_NAME_0)
        self.assertEqual(l_obj.Lights[1].Name, TESTING_LIGHT_NAME_1)


class B2_Write(SetupMixin, unittest.TestCase):
    """ This section tests the utility class
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))
        self.m_pyhouse_obj.House.Lighting = self.m_api._read_lighting_xml(self.m_pyhouse_obj)

    def test_1_lighting(self):
        """Write out the 'LightingSection' which contains the 'LightSection',
        """
        self.m_api._read_lighting_xml(self.m_pyhouse_obj)
        # print(PrettyFormatAny.form(l_obj, 'House'))
        l_xml = ET.Element('HouseDivision')
        l_xml = self.m_api._write_lighting_xml(self.m_pyhouse_obj, l_xml)
        print(PrettyFormatAny.form(l_xml, 'XML'))
        self.assertEqual(len(l_xml), 3)
        self.assertEqual(len(l_xml[0]), 2)
        self.assertEqual(len(l_xml[1]), 2)
        self.assertEqual(len(l_xml[2]), 2)
        self.assertEqual(l_xml.find('LightSection').tag, 'LightSection')
        self.assertEqual(l_xml.find('ButtonSection').tag, 'ButtonSection')
        self.assertEqual(l_xml.find('ControllerSection').tag, 'ControllerSection')
        self.assertEqual(l_xml.find('ControllerSection/Controller').tag, 'Controller')

# ## END DBK
