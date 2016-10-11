"""
@name:      PyHouse/src/Modules/lights/test/test_lighting_lights.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2014-2016 by D. Brian Kimmel
@note:      Created on May 23, 2014
@license:   MIT License
@summary:   This module is for testing lighting data.

Passed all 15 tests - DBK - 2016-07-17

"""

__updated__ = '2016-10-10'

#  Import system type stuff
import xml.etree.ElementTree as ET
from twisted.trial import unittest

#  Import PyMh files and modules.
from Modules.Core.data_objects import LightingData
from Modules.Housing.Lighting.lighting_lights import Utility, API as lightsAPI
from Modules.Core import conversions
from Modules.Families.family import API as familyAPI
from Modules.Families.Insteon.test.xml_insteon import \
        TESTING_INSTEON_ADDRESS_0, \
        TESTING_INSTEON_DEVCAT_0, \
        TESTING_INSTEON_GROUP_LIST_0, \
        TESTING_INSTEON_GROUP_NUM_0, \
        TESTING_INSTEON_PRODUCT_KEY_0
from Modules.Core.test.xml_device import \
        TESTING_DEVICE_FAMILY_INSTEON
from Modules.Housing.Lighting.test.xml_lights import \
        TESTING_LIGHT_NAME_0, \
        TESTING_LIGHT_CUR_LEVEL_0, \
        TESTING_LIGHT_IS_DIMMABLE_0, \
        TESTING_LIGHT_DIMMABLE_1, \
        TESTING_LIGHT_KEY_0, \
        TESTING_LIGHT_ACTIVE_0, \
        TESTING_LIGHT_COMMENT_0, \
        TESTING_LIGHT_ROOM_NAME_0, \
        TESTING_LIGHT_UUID_0, \
        TESTING_LIGHT_ROOM_X, \
        TESTING_LIGHT_ROOM_Y, \
        TESTING_LIGHT_ROOM_Z, \
        TESTING_LIGHT_DEVICE_TYPE_0, \
        TESTING_LIGHT_DEVICE_SUBTYPE_0, \
        TESTING_LIGHT_DEVICE_FAMILY_0, \
        TESTING_LIGHT_ROOM_UUID_0
from test.xml_data import XML_LONG
from test.testing_mixin import SetupPyHouseObj
from Modules.Utilities import json_tools
from Modules.Utilities.debug_tools import PrettyFormatAny


class SetupMixin(object):
    """
    """

    def setUp(self, p_root):
        self.m_pyhouse_obj = SetupPyHouseObj().BuildPyHouseObj(p_root)
        self.m_xml = SetupPyHouseObj().BuildXml(p_root)
        self.m_family = familyAPI(self.m_pyhouse_obj).LoadFamilyTesting()
        self.m_pyhouse_obj.House.FamilyData = self.m_family


class A1_Setup(SetupMixin, unittest.TestCase):
    """
    This section tests the above setup for things we will need further down in the tests.
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))

    def test_1_Objects(self):
        """ Be sure that the XML contains the right stuff.
        """
        # print(PrettyFormatAny.form(self.m_xml, 'A1-1-A - Tags'))
        self.assertEqual(self.m_xml.root.tag, 'PyHouse')
        self.assertEqual(self.m_xml.house_div.tag, 'HouseDivision')
        self.assertEqual(self.m_xml.light_sect.tag, 'LightSection')
        self.assertEqual(self.m_xml.light.tag, 'Light')
        self.assertEqual(self.m_xml.controller_sect.tag, 'ControllerSection')
        self.assertEqual(self.m_xml.controller.tag, 'Controller')
        self.assertEqual(self.m_xml.button_sect.tag, 'ButtonSection')
        self.assertEqual(self.m_xml.button.tag, 'Button')

    def test_2_Family(self):
        """ Be sure that the XML contains the right stuff.
        """
        # print(PrettyFormatAny.form(self.m_pyhouse_obj, 'A1-2-A -PyHouse'))
        # # print(PrettyFormatAny.form(self.m_pyhouse_obj.House, 'PyHouse House'))
        self.assertNotEqual(self.m_pyhouse_obj, None)
        # self.assertEqual(self.m_pyhouse_obj.House.Name, TESTING_HOUSE_NAME)


class A2_XML(SetupMixin, unittest.TestCase):
    """
    This section tests the reading and writing of XML used by lighting_lights.
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))

    def test_1_lights(self):
        """ Be sure that the XML contains the right stuff.
        """
        l_xml = self.m_xml.light_sect
        # print(PrettyFormatAny.form(l_xml, 'A2-1-A - XML'))
        self.assertEqual(l_xml[0].attrib['Name'], TESTING_LIGHT_NAME_0)

    def test_2_light(self):
        """Ensure that the lighting objects are correct in the XML
        """
        l_xml = self.m_xml.light
        # print(PrettyFormatAny.form(l_xml, 'A2-2-A - PyHouse'))
        self.assertEqual(l_xml.attrib['Name'], TESTING_LIGHT_NAME_0)


class B1_Read(SetupMixin, unittest.TestCase):
    """
    This section tests the reading and writing of XML used by lighting_lights.
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))

    def test_1_Base(self):
        """Test the Base read - the device information
        """
        l_xml = self.m_xml.light
        # print(PrettyFormatAny.form(l_xml, 'B1-1-A  Base'))
        l_obj = Utility._read_base_device(self.m_pyhouse_obj, l_xml)
        # print(PrettyFormatAny.form(l_obj, 'R1-1-B - Base'))
        self.assertEqual(l_obj.Name, TESTING_LIGHT_NAME_0)
        self.assertEqual(str(l_obj.Key), TESTING_LIGHT_KEY_0)
        self.assertEqual(str(l_obj.Active), TESTING_LIGHT_ACTIVE_0)
        self.assertEqual(l_obj.UUID, TESTING_LIGHT_UUID_0)
        self.assertEqual(l_obj.Comment, TESTING_LIGHT_COMMENT_0)
        self.assertEqual(l_obj.DeviceFamily, TESTING_LIGHT_DEVICE_FAMILY_0)
        self.assertEqual(str(l_obj.DeviceType), TESTING_LIGHT_DEVICE_TYPE_0)
        self.assertEqual(str(l_obj.DeviceSubType), TESTING_LIGHT_DEVICE_SUBTYPE_0)
        self.assertEqual(l_obj.RoomName, TESTING_LIGHT_ROOM_NAME_0)
        self.assertEqual(str(l_obj.RoomCoords.X_Easting), TESTING_LIGHT_ROOM_X)
        self.assertEqual(str(l_obj.RoomCoords.Y_Northing), TESTING_LIGHT_ROOM_Y)
        self.assertEqual(str(l_obj.RoomCoords.Z_Height), TESTING_LIGHT_ROOM_Z)

    def test_2_LightData(self):
        """Test the light information is read properly
        """
        l_obj = Utility._read_base_device(self.m_pyhouse_obj, self.m_xml.light)
        Utility._read_light_data(self.m_pyhouse_obj, l_obj, self.m_xml.light)
        # print(PrettyFormatAny.form(l_obj, 'B1-2-A - Base'))
        self.assertEqual(str(l_obj.CurLevel), TESTING_LIGHT_CUR_LEVEL_0)
        self.assertEqual(str(l_obj.IsDimmable), TESTING_LIGHT_IS_DIMMABLE_0)

    def test_3_FamilyData(self):
        """Test the family data read.
        """
        l_obj = Utility._read_base_device(self.m_pyhouse_obj, self.m_xml.light)
        Utility._read_family_data(self.m_pyhouse_obj, l_obj, self.m_xml.light)
        # print(PrettyFormatAny.form(l_obj, 'B1-3-A - Base'))
        self.assertEqual(l_obj.InsteonAddress, conversions.dotted_hex2int(TESTING_INSTEON_ADDRESS_0))

    def test_4_OneLight(self):
        """ Read everything about one light.
        """
        l_obj = Utility._read_one_light_xml(self.m_pyhouse_obj, self.m_xml.light)
        # print(PrettyFormatAny.form(l_obj, 'B1-4-A - One Light'))
        # print(PrettyFormatAny.form(l_obj.RoomCoords, 'B1-4-B - One Light'))
        self.assertEqual(l_obj.Name, TESTING_LIGHT_NAME_0)
        self.assertEqual(str(l_obj.Key), TESTING_LIGHT_KEY_0)
        self.assertEqual(str(l_obj.Active), TESTING_LIGHT_ACTIVE_0)
        self.assertEqual(l_obj.UUID, TESTING_LIGHT_UUID_0)
        self.assertEqual(l_obj.Comment, TESTING_LIGHT_COMMENT_0)
        self.assertEqual(l_obj.DeviceFamily, TESTING_DEVICE_FAMILY_INSTEON)
        self.assertEqual(l_obj.RoomName, TESTING_LIGHT_ROOM_NAME_0)
        self.assertEqual(l_obj.InsteonAddress, conversions.dotted_hex2int(TESTING_INSTEON_ADDRESS_0))

    def test_5_AllLights(self):
        """Read everything for all lights.
        """
        l_objs = lightsAPI.read_all_lights_xml(self.m_pyhouse_obj, self.m_xml.light_sect)
        # print(PrettyFormatAny.form(l_objs, 'B1-5-A - All Lights'))
        # print(PrettyFormatAny.form(l_objs[0], 'B1-5-B - All Lights'))
        # print(PrettyFormatAny.form(l_objs[0].RoomCoords, 'B1-5-c - All Lights'))
        self.assertEqual(len(l_objs), 2)


class B2_Write(SetupMixin, unittest.TestCase):
    """
    This section tests the reading and writing of XML used by lighting_lights.
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))
        self.m_obj = Utility._read_one_light_xml(self.m_pyhouse_obj, self.m_xml.light)

    def test_01_Base(self):
        """Test the write for proper XML elements
        """
        l_xml = Utility._write_base_device('Light', self.m_obj)
        # print(PrettyFormatAny.form(l_xml, 'B2-01-A - ML'))
        self.assertEqual(l_xml.attrib['Name'], TESTING_LIGHT_NAME_0)
        self.assertEqual(l_xml.attrib['Key'], '0')
        self.assertEqual(l_xml.attrib['Active'], 'True')
        self.assertEqual(l_xml.find('UUID').text, TESTING_LIGHT_UUID_0)
        self.assertEqual(l_xml.find('Comment').text, TESTING_LIGHT_COMMENT_0)
        self.assertEqual(l_xml.find('DeviceFamily').text, TESTING_DEVICE_FAMILY_INSTEON)
        self.assertEqual(l_xml.find('RoomName').text, TESTING_LIGHT_ROOM_NAME_0)
        self.assertEqual(l_xml.find('RoomUUID').text, TESTING_LIGHT_ROOM_UUID_0)

    def test_02_LightData(self):
        l_xml = Utility._write_base_device('Light', self.m_obj)
        Utility._write_light_data(self.m_obj, l_xml)
        # print(PrettyFormatAny.form(l_xml, 'W1-02-A - XML'))
        self.assertEqual(l_xml.find('CurLevel').text, TESTING_LIGHT_CUR_LEVEL_0)
        self.assertEqual(l_xml.find('IsDimmable').text, TESTING_LIGHT_DIMMABLE_1)

    def test_03_LightFamily(self):
        l_xml = Utility._write_base_device('Light', self.m_obj)
        Utility._write_light_data(self.m_obj, l_xml)
        Utility._write_family_data(self.m_pyhouse_obj, self.m_obj, l_xml)
        # print(PrettyFormatAny.form(l_xml, 'W1-03-A - W1-04-A - XML'))
        self.assertEqual(l_xml.find('InsteonAddress').text, TESTING_INSTEON_ADDRESS_0)
        self.assertEqual(l_xml.find('DevCat').text, TESTING_INSTEON_DEVCAT_0)
        self.assertEqual(l_xml.find('GroupList').text, TESTING_INSTEON_GROUP_LIST_0)
        self.assertEqual(l_xml.find('GroupNumber').text, TESTING_INSTEON_GROUP_NUM_0)
        self.assertEqual(l_xml.find('ProductKey').text, TESTING_INSTEON_PRODUCT_KEY_0)

    def test_04_OneLight(self):
        """ Write out the XML file for the location section
        """
        l_xml = Utility._write_one_light_xml(self.m_pyhouse_obj, self.m_obj)
        # print(PrettyFormatAny.form(l_xml, 'XML'))
        self.assertEqual(l_xml.attrib['Name'], TESTING_LIGHT_NAME_0)
        self.assertEqual(l_xml.attrib['Key'], TESTING_LIGHT_KEY_0)
        self.assertEqual(l_xml.attrib['Active'], TESTING_LIGHT_ACTIVE_0)
        self.assertEqual(l_xml.find('UUID').text, TESTING_LIGHT_UUID_0)
        self.assertEqual(l_xml.find('Comment').text, TESTING_LIGHT_COMMENT_0)
        self.assertEqual(l_xml.find('DeviceFamily').text, TESTING_DEVICE_FAMILY_INSTEON)
        self.assertEqual(l_xml.find('RoomName').text, TESTING_LIGHT_ROOM_NAME_0)
        self.assertEqual(l_xml.find('RoomUUID').text, TESTING_LIGHT_ROOM_UUID_0)
        self.assertEqual(l_xml.find('CurLevel').text, TESTING_LIGHT_CUR_LEVEL_0)
        self.assertEqual(l_xml.find('IsDimmable').text, TESTING_LIGHT_IS_DIMMABLE_0)
        self.assertEqual(l_xml.find('InsteonAddress').text, TESTING_INSTEON_ADDRESS_0)
        self.assertEqual(l_xml.find('DevCat').text, TESTING_INSTEON_DEVCAT_0)
        self.assertEqual(l_xml.find('GroupList').text, TESTING_INSTEON_GROUP_LIST_0)
        self.assertEqual(l_xml.find('GroupNumber').text, TESTING_INSTEON_GROUP_NUM_0)
        self.assertEqual(l_xml.find('ProductKey').text, TESTING_INSTEON_PRODUCT_KEY_0)

    def test_05_AllLights(self):
        l_objs = lightsAPI.read_all_lights_xml(self.m_pyhouse_obj, self.m_xml.light_sect)
        self.m_pyhouse_obj.House.Lighting = LightingData()
        self.m_pyhouse_obj.House.Lighting.Lights = l_objs
        l_xml = lightsAPI.write_all_lights_xml(self.m_pyhouse_obj)
        print(PrettyFormatAny.form(l_xml, 'W1-05-A - Lights XML'))
        l_xml0 = l_xml.find('Light')
        self.assertEqual(l_xml0.find('UUID').text, TESTING_LIGHT_UUID_0)
        self.assertEqual(l_xml0.find('Comment').text, TESTING_LIGHT_COMMENT_0)


class Z1_JSON(SetupMixin, unittest.TestCase):
    """
    This section tests the reading and writing of XML used by lighting_lights.
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))

    def test_01_CreateJson(self):
        """ Create a JSON object for Location.
        """
        l_obj = lightsAPI.read_all_lights_xml(self.m_pyhouse_obj, self.m_xml.light_sect)
        # print(PrettyFormatAny.form(l_obj, 'Z1-01-A - Lights'))
        l_json = json_tools.encode_json(l_obj)
        # print(PrettyFormatAny.form(l_json, 'Z1-01-B - JSON'))
        self.assertEqual(l_json[0], '{')

#  ## END DBK
