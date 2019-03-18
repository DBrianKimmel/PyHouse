"""
@name:      PyHouse/src/Modules/lighting/test/test_lighting_buttons.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2014-2019 by D. Brian Kimmel
@license:   MIT License
@note:      Created on May 22, 2014
@summary:   This module is for testing lighting buttons data.

Passed all 12 tests - DBK - 2019-01-22
"""

__updated__ = '2019-03-18'

# Import system type stuff
import xml.etree.ElementTree as ET
from twisted.trial import unittest

# Import PyMh files and modules.
from test.xml_data import XML_LONG, TESTING_PYHOUSE
from test.testing_mixin import SetupPyHouseObj
from Modules.Core.data_objects import ButtonData
from Modules.Core.Utilities import convert, json_tools
from Modules.Housing.Lighting.lighting_buttons import XML as buttonsXML
from Modules.Housing.Lighting.lighting_xml import LightingXML
from Modules.Housing.test.xml_housing import \
    TESTING_HOUSE_DIVISION
from Modules.Housing.Lighting.test.xml_lighting import \
    TESTING_LIGHTING_SECTION
from Modules.Housing.Lighting.test.xml_buttons import \
    TESTING_LIGHTING_BUTTON_NAME_0, \
    TESTING_LIGHTING_BUTTON_COMMENT_0, \
    TESTING_LIGHTING_BUTTON_FAMILY_0, \
    TESTING_LIGHTING_BUTTON_ACTIVE_0, \
    TESTING_LIGHTING_BUTTON_DEVICE_SUBTYPE_0, \
    TESTING_LIGHTING_BUTTON_DEVICE_TYPE_0, \
    TESTING_LIGHTING_BUTTON_ROOM_NAME_0, \
    TESTING_LIGHTING_BUTTON_KEY_0, \
    TESTING_LIGHTING_BUTTON_UUID_0, \
    TESTING_LIGHTING_BUTTON_ROOM_UUID_0, \
    TESTING_LIGHTING_BUTTON_INSTEON_ADDRESS_0, TESTING_BUTTON_SECTION, TESTING_BUTTON, XML_BUTTON_SECTION
from Modules.Families.family import API as familyAPI
from Modules.Core.Utilities.debug_tools import PrettyFormatAny


class SetupMixin(object):

    def setUp(self, p_root):
        self.m_pyhouse_obj = SetupPyHouseObj().BuildPyHouseObj(p_root)
        self.m_xml = SetupPyHouseObj().BuildXml(p_root)
        self.m_family = familyAPI(self.m_pyhouse_obj).LoadFamilyTesting()
        self.m_pyhouse_obj.FamilyInformation = self.m_family
        # self.m_api = buttonsAPI()
        self.m_button_obj = ButtonData()
        self.m_version = '1.4.0'


class A0(unittest.TestCase):

    def setUp(self):
        pass

    def test_00_Print(self):
        print('Id: test_lighting_buttons')


class A1_Setup(SetupMixin, unittest.TestCase):

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))

    def test_01_PyHouse(self):
        """ Be sure that the XML contains the right stuff.
        """
        self.assertEqual(self.m_pyhouse_obj.House.Irrigation, {})

    def test_02_FindXML(self):
        """ Be sure that the XML contains the right stuff.
        """
        self.assertEqual(self.m_xml.root.tag, TESTING_PYHOUSE)
        self.assertEqual(self.m_xml.house_div.tag, TESTING_HOUSE_DIVISION)
        self.assertEqual(self.m_xml.lighting_sect.tag, TESTING_LIGHTING_SECTION)
        self.assertEqual(self.m_xml.button_sect.tag, TESTING_BUTTON_SECTION)
        self.assertEqual(self.m_xml.button.tag, TESTING_BUTTON)


class A2_Xml(SetupMixin, unittest.TestCase):

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring('<x />'))
        pass

    def test_01_Raw(self):
        l_xml = XML_BUTTON_SECTION
        # print(l_xml)
        self.assertEqual(l_xml[:15], '<ButtonSection>')

    def test_02_Parsed(self):
        l_xml = ET.fromstring(XML_BUTTON_SECTION)
        # print(l_xml)
        self.assertEqual(l_xml.tag, TESTING_BUTTON_SECTION)

    def test_03_Family(self):
        self.assertEqual(self.m_family['Insteon'].Name, 'Insteon')


class B1_Read(SetupMixin, unittest.TestCase):
    """ This section tests the reading and writing of XML used by lighting_controllers.
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))

    def test_01_ReadButtonData(self):
        """ Read in the xml file and fill in the lights
        """
        l_xml = self.m_xml.button_sect[0]
        # print(PrettyFormatAny.form(l_xml, 'B1-01-A - Button'))
        l_button = self.m_button_obj
        l_button = LightingXML()._read_base_device(l_button, l_xml)
        # print(PrettyFormatAny.form(l_button, 'B1-01-B - Button'))
        self.assertEqual(l_button.Name, TESTING_LIGHTING_BUTTON_NAME_0)
        self.assertEqual(str(l_button.Active), TESTING_LIGHTING_BUTTON_ACTIVE_0)
        self.assertEqual(l_button.Comment, TESTING_LIGHTING_BUTTON_COMMENT_0)
        self.assertEqual(l_button.DeviceFamily, TESTING_LIGHTING_BUTTON_FAMILY_0)
        self.assertEqual(str(l_button.DeviceType), TESTING_LIGHTING_BUTTON_DEVICE_TYPE_0)
        self.assertEqual(str(l_button.DeviceSubType), TESTING_LIGHTING_BUTTON_DEVICE_SUBTYPE_0)
        self.assertEqual(l_button.RoomName, TESTING_LIGHTING_BUTTON_ROOM_NAME_0)
        self.assertEqual(l_button.RoomUUID, TESTING_LIGHTING_BUTTON_ROOM_UUID_0)

    def test_02_ReadOneButtonXml(self):
        """ Read in the xml file and fill in the lights
        """
        l_button = buttonsXML()._read_one_button_xml(self.m_pyhouse_obj, self.m_xml.button)
        self.assertEqual(l_button.Name, TESTING_LIGHTING_BUTTON_NAME_0)
        self.assertEqual(l_button.Active, True)
        self.assertEqual(l_button.Key, 0, 'Bad key')
        self.assertEqual(l_button.Name, TESTING_LIGHTING_BUTTON_NAME_0)
        self.assertEqual(l_button.DeviceFamily, TESTING_LIGHTING_BUTTON_FAMILY_0)
        self.assertEqual(l_button.InsteonAddress, convert.dotted_hex2int(TESTING_LIGHTING_BUTTON_INSTEON_ADDRESS_0))

    def test_03_ReadAllButtonsXml(self):
        l_buttons = buttonsXML().read_all_buttons_xml(self.m_pyhouse_obj)
        # print(PrettyFormatAny.form(l_buttons, 'B1-03-B - Button'))
        self.assertEqual(len(l_buttons), 2)


class B2_Write(SetupMixin, unittest.TestCase):
    """ This section tests the reading and writing of XML used by lighting_controllers.
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))

    def test_01_OneButton(self):
        """ Write out the XML file for the button section
        """
        l_button = buttonsXML()._read_one_button_xml(self.m_pyhouse_obj, self.m_xml.button)
        self.m_pyhouse_obj.House.Lighting.Buttons = l_button
        l_xml = buttonsXML()._write_one_button_xml(self.m_pyhouse_obj, l_button)
        # print(PrettyFormatAny.form(l_xml, 'B2-01-A - Button'))
        self.assertEqual(l_xml.attrib['Name'], TESTING_LIGHTING_BUTTON_NAME_0)
        self.assertEqual(l_xml.attrib['Key'], TESTING_LIGHTING_BUTTON_KEY_0)
        self.assertEqual(str(l_xml.attrib['Active']), TESTING_LIGHTING_BUTTON_ACTIVE_0)
        self.assertEqual(l_xml.find('UUID').text, TESTING_LIGHTING_BUTTON_UUID_0)
        self.assertEqual(l_xml.find('Comment').text, TESTING_LIGHTING_BUTTON_COMMENT_0)
        self.assertEqual(l_xml.find('DeviceFamily').text, TESTING_LIGHTING_BUTTON_FAMILY_0)
        self.assertEqual(l_xml.find('DeviceType').text, TESTING_LIGHTING_BUTTON_DEVICE_TYPE_0)
        self.assertEqual(l_xml.find('DeviceSubType').text, TESTING_LIGHTING_BUTTON_DEVICE_SUBTYPE_0)
        self.assertEqual(l_xml.find('RoomName').text, TESTING_LIGHTING_BUTTON_ROOM_NAME_0)
        self.assertEqual(l_xml.find('RoomUUID').text, TESTING_LIGHTING_BUTTON_ROOM_UUID_0)

    def test_02_AllButtons(self):
        """ Write out the XML file for the Buttons section
        """
        l_buttons = buttonsXML().read_all_buttons_xml(self.m_pyhouse_obj)
        self.m_pyhouse_obj.House.Lighting.Buttons = l_buttons
        l_xml = buttonsXML().write_all_buttons_xml(self.m_pyhouse_obj)
        # print(PrettyFormatAny.form(l_xml, 'B2-02-A - Button'))


class J1_Json(SetupMixin, unittest.TestCase):
    """ This section tests the reading and writing of XML used by lighting_controllers.
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))

    def test_06_CreateJson(self):
        """ Create a JSON object for Buttons.
        """
        l_button = buttonsXML().read_all_buttons_xml(self.m_pyhouse_obj)
        self.m_pyhouse_obj.House.Lighting.Buttons = l_button
        # print('Buttons: {}'.format(l_button))
        # print('Button 0: {}'.format(vars(l_button[0])))
        l_json = json_tools.encode_json(l_button)
        # print('JSON: {}'.format(l_json))

# ## END DBK
