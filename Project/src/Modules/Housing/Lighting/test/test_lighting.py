"""
@name:      PyHouse/src/Modules/Lighting/test/test_lighting.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2013-2019 by D. Brian Kimmel
@note:      Created on Apr 9, 2013
@license:   MIT License
@summary:   Test the home lighting system automation.

Passed all 10 tests.  DBK 2019-01-22

"""

__updated__ = '2019-01-22'

# Import system type stuff
from twisted.trial import unittest
import xml.etree.ElementTree as ET

# Import PyMh files and modules.
from test.xml_data import XML_LONG, TESTING_PYHOUSE
from test.testing_mixin import SetupPyHouseObj
from Modules.Housing.Lighting.lighting_lights import LightData
from Modules.Families.family import API as familyAPI
from Modules.Housing.Lighting.lighting import API as lightingAPI, XML as lightingXML
from Modules.Housing.Lighting.test.xml_lighting import \
    TESTING_LIGHTING_SECTION, \
    XML_LIGHTING
from Modules.Housing.test.xml_housing import \
    TESTING_HOUSE_DIVISION
from Modules.Housing.Lighting.test.xml_controllers import \
    TESTING_CONTROLLER_NAME_0, \
    TESTING_CONTROLLER_NAME_1
from Modules.Core.test.xml_device import \
    TESTING_DEVICE_FAMILY_INSTEON
from Modules.Housing.Lighting.test.xml_lights import \
    TESTING_LIGHT_NAME_0, \
    TESTING_LIGHT_NAME_1, TESTING_LIGHT_SECTION
from Modules.Housing.Lighting.test.xml_buttons import \
    TESTING_LIGHTING_BUTTON_NAME_0, \
    TESTING_LIGHTING_BUTTON_NAME_1
from Modules.Core.Utilities.debug_tools import PrettyFormatAny


class SetupMixin(object):

    def setUp(self, p_root):
        self.m_pyhouse_obj = SetupPyHouseObj().BuildPyHouseObj(p_root)
        self.m_xml = SetupPyHouseObj().BuildXml(p_root)
        self.m_light_obj = LightData()
        self.m_api = lightingAPI(self.m_pyhouse_obj)
        self.m_family = familyAPI(self.m_pyhouse_obj).LoadFamilyTesting()
        self.m_pyhouse_obj.House.FamilyData = self.m_family


class A0(unittest.TestCase):

    def setUp(self):
        pass

    def test_00_Print(self):
        print('Id: test_lighting')


class A1_Setup(SetupMixin, unittest.TestCase):
    """ This section tests the master setup above this.
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))

    def test_01_Version(self):
        self.assertGreater(self.m_pyhouse_obj.Xml.XmlVersion, '1.4.0')

    def test_02_XmlTags(self):
        """ Be sure that the XML contains the right stuff.
        """
        self.assertEqual(self.m_xml.root.tag, TESTING_PYHOUSE)
        self.assertEqual(self.m_xml.house_div.tag, TESTING_HOUSE_DIVISION)
        self.assertEqual(self.m_xml.lighting_sect.tag, TESTING_LIGHTING_SECTION)
        self.assertEqual(self.m_xml.light_sect.tag, 'LightSection')
        self.assertEqual(self.m_xml.button.tag, 'Button')
        self.assertEqual(self.m_xml.controller.tag, 'Controller')
        self.assertEqual(self.m_xml.light.tag, 'Light')


class A2_Xml(SetupMixin, unittest.TestCase):

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring('<x />'))
        pass

    def test_01_Raw(self):
        """ All 3 lighting types
        """
        l_raw = XML_LIGHTING
        # print(l_raw)
        self.assertEqual(l_raw[:17], '<LightingSection>')

    def test_02_Parsed(self):
        """ All 3 lighting types
        """
        l_xml = ET.fromstring(XML_LIGHTING)
        # print(PrettyFormatAny.form(l_xml, 'A2-02-A - Parsed XML'))
        self.assertEqual(l_xml.tag, TESTING_LIGHTING_SECTION)


class B1_Read(SetupMixin, unittest.TestCase):
    """ This section tests the utility class
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))

    def test_1_Button(self):
        """Utility.
        """
        l_xml = lightingXML().read_lighting_xml(self.m_pyhouse_obj)
        self.assertEqual(len(l_xml.Buttons), 2)
        self.assertEqual(l_xml.Buttons[0].Name, TESTING_LIGHTING_BUTTON_NAME_0)
        self.assertEqual(l_xml.Buttons[0].DeviceFamily, TESTING_DEVICE_FAMILY_INSTEON)
        self.assertEqual(l_xml.Buttons[1].Name, TESTING_LIGHTING_BUTTON_NAME_1)

    def test_2_Controller(self):
        """Utility.
        """
        l_xml = lightingXML().read_lighting_xml(self.m_pyhouse_obj)
        self.assertEqual(len(l_xml.Controllers), 2)
        self.assertEqual(l_xml.Controllers[0].Name, TESTING_CONTROLLER_NAME_0)
        self.assertEqual(l_xml.Controllers[0].DeviceFamily, TESTING_DEVICE_FAMILY_INSTEON)
        self.assertEqual(l_xml.Controllers[1].Name, TESTING_CONTROLLER_NAME_1)

    def test_3_Light(self):
        """Utility.
        """
        l_xml = lightingXML().read_lighting_xml(self.m_pyhouse_obj)
        # print(PrettyFormatAny.form(l_xml.Lights, 'B1-3-A - Light'))
        self.assertEqual(len(l_xml.Lights), 3)
        self.assertEqual(l_xml.Lights[0].Name, TESTING_LIGHT_NAME_0)
        self.assertEqual(l_xml.Lights[0].DeviceFamily, TESTING_DEVICE_FAMILY_INSTEON)
        self.assertEqual(l_xml.Lights[1].Name, TESTING_LIGHT_NAME_1)

    def test_4_Lighting(self):
        """Read all the lighting info (Buttons, Controllers, Lights)
        """
        l_obj = lightingXML().read_lighting_xml(self.m_pyhouse_obj)
        # print(PrettyFormatAny.form(l_obj, 'B1-4-A - Lighting'))
        self.assertEqual(len(l_obj.Buttons), 2)
        self.assertEqual(len(l_obj.Controllers), 2)
        self.assertEqual(len(l_obj.Lights), 3)
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
        self.m_pyhouse_obj.House.Lighting = lightingXML().read_lighting_xml(self.m_pyhouse_obj)

    def test_1_lighting(self):
        """Write out the 'LightingSection' which contains the 'LightSection',
        """
        # .read_lighting_xml(self.m_pyhouse_obj)
        # print(PrettyFormatAny.form(l_obj, 'House'))
        l_xml = ET.Element(TESTING_HOUSE_DIVISION)
        l_xml = lightingXML().write_lighting_xml(self.m_pyhouse_obj, l_xml)
        # print(PrettyFormatAny.form(l_xml, 'B2-1-A - XML'))
        self.assertEqual(len(l_xml), 3)
        self.assertEqual(len(l_xml[0]), 2)
        self.assertEqual(len(l_xml[1]), 2)
        self.assertEqual(len(l_xml[2]), 3)
        self.assertEqual(l_xml.find(TESTING_LIGHT_SECTION).tag, TESTING_LIGHT_SECTION)
        self.assertEqual(l_xml.find('ButtonSection').tag, 'ButtonSection')
        self.assertEqual(l_xml.find('ControllerSection').tag, 'ControllerSection')
        self.assertEqual(l_xml.find('ControllerSection/Controller').tag, 'Controller')

# ## END DBK
