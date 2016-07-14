"""
@name:      PyHouse/src/Modules/lighting/test/test_lighting_buttons.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2014-2015 by D. Brian Kimmel
@license:   MIT License
@note:      Created on May 22, 2014
@summary:   This module is for testing lighting buttons data.

Passed all 9 tests - DBK - 2016-07-14
"""

__updated__ = '2016-07-14'

# Import system type stuff
import xml.etree.ElementTree as ET
from twisted.trial import unittest

# Import PyMh files and modules.
from Modules.Core.data_objects import ButtonData
from Modules.Core.test.xml_device import \
        TESTING_DEVICE_COMMENT, \
        TESTING_DEVICE_ROOM_NAME, \
        TESTING_DEVICE_FAMILY_INSTEON
from Modules.Housing.Lighting.lighting_buttons import Utility, API as buttonsAPI
from Modules.Housing.Lighting.test.xml_buttons import \
        TESTING_LIGHTING_BUTTON_NAME_0
from Modules.Families.family import API as familyAPI
from Modules.Core import conversions
from test.xml_data import XML_LONG
from Modules.Families.Insteon.test.xml_insteon import TESTING_INSTEON_ADDRESS_0
from test.testing_mixin import SetupPyHouseObj
from Modules.Utilities import json_tools


class SetupMixin(object):

    def setUp(self, p_root):
        self.m_pyhouse_obj = SetupPyHouseObj().BuildPyHouseObj(p_root)
        self.m_xml = SetupPyHouseObj().BuildXml(p_root)
        self.m_family = familyAPI(self.m_pyhouse_obj).LoadFamilyTesting()
        self.m_pyhouse_obj.House.FamilyData = self.m_family
        self.m_api = buttonsAPI()
        self.m_button_obj = ButtonData()
        self.m_version = '1.4.0'


class A1(SetupMixin, unittest.TestCase):
    """ This section tests the reading and writing of XML used by lighting_controllers.
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))

    def test_01_FindXml(self):
        """ Be sure that the XML contains the right stuff.
        """
        self.assertEqual(self.m_xml.root.tag, 'PyHouse')
        self.assertEqual(self.m_xml.button_sect.tag, 'ButtonSection')
        self.assertEqual(self.m_xml.button.tag, 'Button')

    def test_02_Xml(self):
        pass

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
        l_button = Utility._read_base_device(self.m_pyhouse_obj, self.m_xml.button)
        self.assertEqual(l_button.Name, TESTING_LIGHTING_BUTTON_NAME_0)
        self.assertEqual(l_button.Active, True)
        self.assertEqual(l_button.Comment, TESTING_DEVICE_COMMENT)
        self.assertEqual(l_button.DeviceFamily, TESTING_DEVICE_FAMILY_INSTEON)
        self.assertEqual(l_button.LightingType, 'Button', 'Bad Lighting Type')
        self.assertEqual(l_button.RoomName, TESTING_DEVICE_ROOM_NAME)

    def test_02_ReadOneButtonXml(self):
        """ Read in the xml file and fill in the lights
        """
        l_button = Utility._read_one_button_xml(self.m_pyhouse_obj, self.m_xml.button)
        self.assertEqual(l_button.Name, TESTING_LIGHTING_BUTTON_NAME_0)
        self.assertEqual(l_button.Active, True)
        self.assertEqual(l_button.Key, 0, 'Bad key')
        self.assertEqual(l_button.Name, TESTING_LIGHTING_BUTTON_NAME_0)
        self.assertEqual(l_button.DeviceFamily, 'Insteon', 'Bad Lighting family')
        self.assertEqual(l_button.LightingType, 'Button', 'Bad LightingType')
        self.assertEqual(l_button.InsteonAddress, conversions.dotted_hex2int(TESTING_INSTEON_ADDRESS_0))

    def test_03_ReadAllButtonsXml(self):
        l_buttons = self.m_api.read_all_buttons_xml(self.m_pyhouse_obj, self.m_xml.button_sect)
        self.assertEqual(len(l_buttons), 2)


class B2_Write(SetupMixin, unittest.TestCase):
    """ This section tests the reading and writing of XML used by lighting_controllers.
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))

    def test_01_OneButton(self):
        """ Write out the XML file for the button section
        """
        l_button = Utility._read_one_button_xml(self.m_pyhouse_obj, self.m_xml.button)
        l_xml = Utility._write_one_button_xml(self.m_pyhouse_obj, l_button)

    def test_02_AllButtons(self):
        """ Write out the XML file for the Buttons section
        """
        l_button = self.m_api.read_all_buttons_xml(self.m_pyhouse_obj, self.m_xml.button_sect)
        l_xml = self.m_api.write_buttons_xml(self.m_pyhouse_obj)


class J1_Json(SetupMixin, unittest.TestCase):
    """ This section tests the reading and writing of XML used by lighting_controllers.
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))

    def test_06_CreateJson(self):
        """ Create a JSON object for Buttons.
        """
        l_buttons = self.m_api.read_all_buttons_xml(self.m_pyhouse_obj, self.m_xml.button_sect)
        # print('ButtonsS: {0:}'.format(l_buttons))
        # print('Button 0: {0:}'.format(vars(l_buttons[0])))
        l_json = json_tools.encode_json(l_buttons)
        # print('JSON: {0:}'.format(l_json))

# ## END DBK
