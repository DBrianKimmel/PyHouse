"""
@name:      PyHouse/src/Modules/Housing/Lighting/test/test_lighting_lights.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2014-2019 by D. Brian Kimmel
@note:      Created on May 23, 2014
@license:   MIT License
@summary:   This module is for testing lighting data.

Passed all 26 tests - DBK - 2018-12-21

"""

__updated__ = '2019-06-24'

#  Import system type stuff
import xml.etree.ElementTree as ET
from twisted.trial import unittest

#  Import PyMh files and modules.
from test.xml_data import XML_LONG, TESTING_PYHOUSE
from test.testing_mixin import SetupPyHouseObj
from Modules.Core.data_objects import LightingData
from Modules.Core.Utilities import convert
from Modules.Housing.Lighting.lighting_lights import XML as lightsXML
from Modules.Housing.Lighting.lighting_xml import LightingXML
from Modules.Families.family import API as familyAPI
from Modules.Families.Insteon.test.xml_insteon import \
    TESTING_INSTEON_ADDRESS_0, \
    TESTING_INSTEON_DEVCAT_0, \
    TESTING_INSTEON_GROUP_LIST_0, \
    TESTING_INSTEON_GROUP_NUM_0, \
    TESTING_INSTEON_PRODUCT_KEY_0
from Modules.Core.test.xml_device import \
    TESTING_DEVICE_FAMILY_INSTEON, \
    TESTING_DEVICE_FAMILY_UPB
from Modules.Housing.test.xml_housing import \
    TESTING_HOUSE_DIVISION
from Modules.Housing.Lighting.test.xml_lighting import \
    TESTING_LIGHTING_SECTION
from Modules.Housing.Lighting.test.xml_lights import \
    TESTING_LIGHT_NAME_0, \
    TESTING_LIGHT_CUR_LEVEL_0, \
    TESTING_LIGHT_IS_DIMMABLE_0, \
    TESTING_LIGHT_KEY_0, \
    TESTING_LIGHT_ACTIVE_0, \
    TESTING_LIGHT_COMMENT_0, \
    TESTING_LIGHT_ROOM_NAME_0, \
    TESTING_LIGHT_UUID_0, \
    TESTING_LIGHT_ROOM_X0, \
    TESTING_LIGHT_ROOM_Y0, \
    TESTING_LIGHT_ROOM_Z0, \
    TESTING_LIGHT_DEVICE_TYPE_0, \
    TESTING_LIGHT_DEVICE_SUBTYPE_0, \
    TESTING_LIGHT_DEVICE_FAMILY_0, \
    TESTING_LIGHT_ROOM_UUID_0, \
    TESTING_LIGHT_NAME_1, \
    TESTING_LIGHT_KEY_1, \
    TESTING_LIGHT_ACTIVE_1, \
    TESTING_LIGHT_UUID_1, \
    TESTING_LIGHT_COMMENT_1, \
    TESTING_LIGHT_DEVICE_FAMILY_1, \
    TESTING_LIGHT_DEVICE_TYPE_1, \
    TESTING_LIGHT_DEVICE_SUBTYPE_1, \
    TESTING_LIGHT_ROOM_NAME_1, \
    TESTING_LIGHT_ROOM_UUID_1, \
    TESTING_LIGHT_CUR_LEVEL_1, \
    TESTING_LIGHT_IS_DIMMABLE_1, \
    TESTING_LIGHT, \
    L_LIGHT_SECTION_START, \
    TESTING_LIGHT_SECTION, \
    XML_LIGHT_SECTION
from Modules.Families.UPB.test.xml_upb import \
    TESTING_UPB_ADDRESS, \
    TESTING_UPB_NETWORK, \
    TESTING_UPB_PASSWORD
from Modules.Core.Utilities import json_tools
from Modules.Core.Utilities.debug_tools import PrettyFormatAny


class SetupMixin(object):
    """
    """

    def setUp(self, p_root):
        self.m_pyhouse_obj = SetupPyHouseObj().BuildPyHouseObj(p_root)
        self.m_xml = SetupPyHouseObj().BuildXml(p_root)
        self.m_family = familyAPI(self.m_pyhouse_obj).LoadFamilyTesting()
        self.m_pyhouse_obj._Families = self.m_family


class A0(unittest.TestCase):

    def test_00_Print(self):
        print('Id: test_lighting_lights')


class A1_Setup(SetupMixin, unittest.TestCase):
    """
    This section tests the above setup for things we will need further down in the tests.
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))

    def test_01_Tags(self):
        """ Be sure that the XML contains the right stuff.
        """
        # print(PrettyFormatAny.form(self.m_xml, 'A1-01-A - Tags'))
        self.assertEqual(self.m_xml.root.tag, TESTING_PYHOUSE)
        self.assertEqual(self.m_xml.house_div.tag, TESTING_HOUSE_DIVISION)
        self.assertEqual(self.m_xml.lighting_sect.tag, TESTING_LIGHTING_SECTION)
        self.assertEqual(self.m_xml.light.tag, TESTING_LIGHT)
        self.assertEqual(self.m_xml.controller_sect.tag, 'ControllerSection')
        self.assertEqual(self.m_xml.controller.tag, 'Controller')
        self.assertEqual(self.m_xml.button_sect.tag, 'ButtonSection')
        self.assertEqual(self.m_xml.button.tag, 'Button')

    def test_02_Family(self):
        """ Be sure that the XML contains the right stuff.
        """
        # print(PrettyFormatAny.form(self.m_pyhouse_obj, 'A1-02-A -PyHouse'))
        # # print(PrettyFormatAny.form(self.m_pyhouse_obj.House, 'PyHouse House'))
        self.assertNotEqual(self.m_pyhouse_obj, None)
        # self.assertEqual(self.m_pyhouse_obj.House.Name, TESTING_HOUSE_NAME)


class A2_SetupXml(SetupMixin, unittest.TestCase):
    """ Test that the XML contains no syntax errors.
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring('<x />'))
        pass

    def test_01_Raw(self):
        l_raw = XML_LIGHT_SECTION
        # print('A2-01-A - Raw\n{}'.format(l_raw))
        self.assertEqual(l_raw[:14], L_LIGHT_SECTION_START)

    def test_02_Parsed(self):
        l_xml = ET.fromstring(XML_LIGHT_SECTION)
        # print('A2-02-A - Parsed\n{}'.format(PrettyFormatAny.form(l_xml, 'A2-02-A - Parsed')))
        self.assertEqual(l_xml.tag, TESTING_LIGHT_SECTION)


class A3_XML(SetupMixin, unittest.TestCase):
    """
    This section tests the reading and writing of XML used by lighting_lights.
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))

    def test_01_lights(self):
        """ Be sure that the XML contains the right stuff.
        """
        l_xml = self.m_xml.light_sect
        # print(PrettyFormatAny.form(l_xml, 'A2-01-A - XML'))
        self.assertEqual(l_xml[0].attrib['Name'], TESTING_LIGHT_NAME_0)

    def test_02_light(self):
        """Ensure that the lighting objects are correct in the XML
        """
        l_xml = self.m_xml.light
        # print(PrettyFormatAny.form(l_xml, 'A2-02-A - PyHouse'))
        self.assertEqual(l_xml.attrib['Name'], TESTING_LIGHT_NAME_0)


class B1_XmlRead(SetupMixin, unittest.TestCase):
    """
    This section tests the reading and writing of XML used by lighting_lights.
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))

    def test_01_Base0(self):
        """ Read the Base info - the device information
        """
        l_xml = self.m_xml.light_sect[0]
        # print(PrettyFormatAny.form(l_xml, 'B1-01-A  Base'))
        l_obj = LightingXML()._read_base_device(self.m_pyhouse_obj, l_xml)
        # print(PrettyFormatAny.form(l_obj, 'B1-1-B - Base'))
        self.assertEqual(l_obj.Name, TESTING_LIGHT_NAME_0)
        self.assertEqual(str(l_obj.Key), TESTING_LIGHT_KEY_0)
        self.assertEqual(str(l_obj.Active), TESTING_LIGHT_ACTIVE_0)
        self.assertEqual(l_obj.UUID, TESTING_LIGHT_UUID_0)

    def test_02_Base1(self):
        """ Read the Base info - the device information
        """
        l_xml = self.m_xml.light_sect[1]
        # print(PrettyFormatAny.form(l_xml, 'B1-02-A  Base'))
        l_obj = LightingXML()._read_base_device(self.m_pyhouse_obj, l_xml)
        # print(PrettyFormatAny.form(l_obj, 'B1-02-B - Base'))
        self.assertEqual(l_obj.Name, TESTING_LIGHT_NAME_1)
        self.assertEqual(str(l_obj.Key), TESTING_LIGHT_KEY_1)
        self.assertEqual(str(l_obj.Active), TESTING_LIGHT_ACTIVE_1)
        self.assertEqual(l_obj.UUID, TESTING_LIGHT_UUID_1)

    def test_03_LightData0(self):
        """ Read the light information.
        """
        l_xml = self.m_xml.light_sect[0]
        # print(PrettyFormatAny.form(l_xml, 'B1-03-A - Light Data'))
        l_obj = LightingXML()._read_base_device(self.m_pyhouse_obj, l_xml)
        # print(PrettyFormatAny.form(l_obj, 'B1-03-B - Light Data'))
        lightsXML()._read_light_data(l_obj, l_xml)
        # print(PrettyFormatAny.form(l_obj, 'B1-03-C - Light Data'))
        self.assertEqual(str(l_obj.BrightnessPct), TESTING_LIGHT_CUR_LEVEL_0)
        self.assertEqual(str(l_obj.IsDimmable), TESTING_LIGHT_IS_DIMMABLE_0)
        self.assertEqual(l_obj.Comment, TESTING_LIGHT_COMMENT_0)
        self.assertEqual(l_obj.DeviceFamily, TESTING_LIGHT_DEVICE_FAMILY_0)
        self.assertEqual(str(l_obj.DeviceType), TESTING_LIGHT_DEVICE_TYPE_0)
        self.assertEqual(str(l_obj.DeviceSubType), TESTING_LIGHT_DEVICE_SUBTYPE_0)
        self.assertEqual(l_obj.RoomName, TESTING_LIGHT_ROOM_NAME_0)
        self.assertEqual(str(l_obj.RoomCoords.X_Easting), TESTING_LIGHT_ROOM_X0)
        self.assertEqual(str(l_obj.RoomCoords.Y_Northing), TESTING_LIGHT_ROOM_Y0)
        self.assertEqual(str(l_obj.RoomCoords.Z_Height), TESTING_LIGHT_ROOM_Z0)

    def test_04_LightData1(self):
        """ Read the light information.
        """
        l_xml = self.m_xml.light_sect[1]
        l_obj = LightingXML()._read_base_device(self.m_pyhouse_obj, l_xml)
        l_obj = lightsXML()._read_light_data(l_obj, l_xml)
        # print(PrettyFormatAny.form(l_xml, 'B1-04-A - Light Data XML'))
        # print(PrettyFormatAny.form(l_obj, 'B1-04-B - Light Data Obj'))
        self.assertEqual(str(l_obj.BrightnessPct), TESTING_LIGHT_CUR_LEVEL_1)
        self.assertEqual(str(l_obj.IsDimmable), TESTING_LIGHT_IS_DIMMABLE_1)
        self.assertEqual(l_obj.Comment, TESTING_LIGHT_COMMENT_1)
        self.assertEqual(l_obj.DeviceFamily, TESTING_LIGHT_DEVICE_FAMILY_1)
        self.assertEqual(str(l_obj.DeviceType), TESTING_LIGHT_DEVICE_TYPE_1)
        self.assertEqual(str(l_obj.DeviceSubType), TESTING_LIGHT_DEVICE_SUBTYPE_1)
        self.assertEqual(l_obj.RoomName, TESTING_LIGHT_ROOM_NAME_1)
        self.assertEqual(l_obj.RoomUUID, TESTING_LIGHT_ROOM_UUID_1)
        # self.assertEqual(str(l_obj.RoomCoords), TESTING_LIGHT_ROOM_COORDS_1)

    def test_05_FamilyData0(self):
        """ Read the Insteon family data info.
        """
        l_xml = self.m_xml.light_sect[0]
        l_obj = LightingXML()._read_base_device(self.m_pyhouse_obj, l_xml)
        LightingXML()._read_family_data(self.m_pyhouse_obj, l_obj, self.m_xml.light)
        # print(PrettyFormatAny.form(l_obj, 'B1-05-A - Base'))
        self.assertEqual(l_obj.InsteonAddress, convert.dotted_hex2int(TESTING_INSTEON_ADDRESS_0))

    def test_06_FamilyData1(self):
        """ Read the family data info.
        """
        l_xml = self.m_xml.light_sect[1]
        l_obj = LightingXML()._read_base_device(self.m_pyhouse_obj, l_xml)
        LightingXML()._read_family_data(self.m_pyhouse_obj, l_obj, self.m_xml.light)
        # print(PrettyFormatAny.form(l_obj, 'B1-06-A - Base'))
        self.assertEqual(str(l_obj.UPBAddress), TESTING_UPB_ADDRESS)

    def test_07_OneLight0(self):
        """ Read everything about one light.
        """
        l_xml = self.m_xml.light_sect[0]
        l_obj = lightsXML()._read_one_light_xml(self.m_pyhouse_obj, l_xml)
        # print(PrettyFormatAny.form(l_obj, 'B1-07-A - One Light'))
        # print(PrettyFormatAny.form(l_obj.RoomCoords, 'B1-4-B - One Light'))
        self.assertEqual(l_obj.Name, TESTING_LIGHT_NAME_0)
        self.assertEqual(str(l_obj.Key), TESTING_LIGHT_KEY_0)
        self.assertEqual(str(l_obj.Active), TESTING_LIGHT_ACTIVE_0)
        self.assertEqual(l_obj.UUID, TESTING_LIGHT_UUID_0)
        self.assertEqual(l_obj.Comment, TESTING_LIGHT_COMMENT_0)
        self.assertEqual(l_obj.DeviceFamily, TESTING_DEVICE_FAMILY_INSTEON)
        self.assertEqual(l_obj.RoomName, TESTING_LIGHT_ROOM_NAME_0)
        self.assertEqual(l_obj.InsteonAddress, convert.dotted_hex2int(TESTING_INSTEON_ADDRESS_0))

    def test_08_OneLight1(self):
        """ Read everything about one light.
        """
        l_xml = self.m_xml.light_sect[1]
        l_obj = lightsXML()._read_one_light_xml(self.m_pyhouse_obj, l_xml)
        # print(PrettyFormatAny.form(l_obj, 'B1-08-A - One Light'))
        # print(PrettyFormatAny.form(l_obj.RoomCoords, 'B1-4-B - One Light'))
        self.assertEqual(l_obj.Name, TESTING_LIGHT_NAME_1)
        self.assertEqual(str(l_obj.Key), TESTING_LIGHT_KEY_1)
        self.assertEqual(str(l_obj.Active), TESTING_LIGHT_ACTIVE_1)
        self.assertEqual(l_obj.UUID, TESTING_LIGHT_UUID_1)
        self.assertEqual(l_obj.Comment, TESTING_LIGHT_COMMENT_1)
        self.assertEqual(l_obj.DeviceFamily, TESTING_LIGHT_DEVICE_FAMILY_1)
        self.assertEqual(l_obj.RoomName, TESTING_LIGHT_ROOM_NAME_1)
        self.assertEqual(str(l_obj.UPBAddress), TESTING_UPB_ADDRESS)

    def test_09_AllLights(self):
        """Read everything for all lights.
        """
        l_objs = lightsXML().read_all_lights_xml(self.m_pyhouse_obj)
        # print(PrettyFormatAny.form(l_objs, 'B1-09-A - All Lights'))
        # print(PrettyFormatAny.form(l_objs[0], 'B1-5-B - All Lights'))
        # print(PrettyFormatAny.form(l_objs[0].RoomCoords, 'B1-5-c - All Lights'))
        self.assertEqual(len(l_objs), 3)


class B2_XmlWrite(SetupMixin, unittest.TestCase):
    """
    This section tests the reading and writing of XML used by lighting_lights.
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))
        self.m_obj = lightsXML().read_all_lights_xml(self.m_pyhouse_obj)

    def test_01_Base0(self):
        """Test the write for proper XML Base elements
        """
        l_xml = LightingXML()._write_base_device('Light', self.m_obj[0])
        # print(PrettyFormatAny.form(l_xml, 'B2-01-A - ML'))
        self.assertEqual(l_xml.attrib['Name'], TESTING_LIGHT_NAME_0)
        self.assertEqual(l_xml.attrib['Key'], TESTING_LIGHT_KEY_0)
        self.assertEqual(l_xml.attrib['Active'], TESTING_LIGHT_ACTIVE_0)
        self.assertEqual(l_xml.find('UUID').text, TESTING_LIGHT_UUID_0)
        self.assertEqual(l_xml.find('Comment').text, TESTING_LIGHT_COMMENT_0)
        self.assertEqual(l_xml.find('DeviceFamily').text, TESTING_DEVICE_FAMILY_INSTEON)
        self.assertEqual(l_xml.find('RoomName').text, TESTING_LIGHT_ROOM_NAME_0)
        self.assertEqual(l_xml.find('RoomUUID').text, TESTING_LIGHT_ROOM_UUID_0)

    def test_02_Base1(self):
        """Test the write for proper XML Base elements
        """
        l_xml = LightingXML()._write_base_device('Light', self.m_obj[1])
        # print(PrettyFormatAny.form(l_xml, 'B2-02-A - ML'))
        self.assertEqual(l_xml.attrib['Name'], TESTING_LIGHT_NAME_1)
        self.assertEqual(l_xml.attrib['Key'], TESTING_LIGHT_KEY_1)
        self.assertEqual(l_xml.attrib['Active'], TESTING_LIGHT_ACTIVE_1)
        self.assertEqual(l_xml.find('UUID').text, TESTING_LIGHT_UUID_1)
        self.assertEqual(l_xml.find('Comment').text, TESTING_LIGHT_COMMENT_1)
        self.assertEqual(l_xml.find('DeviceFamily').text, TESTING_DEVICE_FAMILY_UPB)
        self.assertEqual(l_xml.find('RoomName').text, TESTING_LIGHT_ROOM_NAME_1)
        self.assertEqual(l_xml.find('RoomUUID').text, TESTING_LIGHT_ROOM_UUID_1)

    def test_03_LightData0(self):
        """ Write
        """
        l_xml = LightingXML()._write_base_device('Light', self.m_obj[0])
        lightsXML()._write_light_data(self.m_obj[0], l_xml)
        # print(PrettyFormatAny.form(l_xml, 'B2-03-A - XML'))
        self.assertEqual(l_xml.find('Brightness').text, TESTING_LIGHT_CUR_LEVEL_0)
        self.assertEqual(l_xml.find('IsDimmable').text, TESTING_LIGHT_IS_DIMMABLE_0)

    def test_04_LightData1(self):
        """ Write
        """
        l_xml = LightingXML()._write_base_device('Light', self.m_obj[1])
        lightsXML()._write_light_data(self.m_obj[1], l_xml)
        # print(PrettyFormatAny.form(l_xml, 'B2-04-A - XML'))
        self.assertEqual(l_xml.find('Brightness').text, TESTING_LIGHT_CUR_LEVEL_1)
        self.assertEqual(l_xml.find('IsDimmable').text, TESTING_LIGHT_IS_DIMMABLE_1)

    def test_05_LightFamily0(self):
        """ Write Family Info
        """
        l_obj = self.m_obj[0]
        l_xml = LightingXML()._write_base_device('Light', l_obj)
        lightsXML()._write_light_data(l_obj, l_xml)
        LightingXML()._write_family_data(self.m_pyhouse_obj, l_obj, l_xml)
        # print(PrettyFormatAny.form(l_obj, 'B2-05-A - Obj'))
        # print(PrettyFormatAny.form(l_xml, 'B2-05-B - XML'))
        self.assertEqual(l_xml.find('InsteonAddress').text, TESTING_INSTEON_ADDRESS_0)
        self.assertEqual(l_xml.find('DevCat').text, TESTING_INSTEON_DEVCAT_0)
        self.assertEqual(l_xml.find('GroupList').text, TESTING_INSTEON_GROUP_LIST_0)
        self.assertEqual(l_xml.find('GroupNumber').text, TESTING_INSTEON_GROUP_NUM_0)
        self.assertEqual(l_xml.find('ProductKey').text, TESTING_INSTEON_PRODUCT_KEY_0)

    def test_06_LightFamily1(self):
        """ Write family info
        """
        l_xml = LightingXML()._write_base_device('Light', self.m_obj[1])
        lightsXML()._write_light_data(self.m_obj[1], l_xml)
        LightingXML()._write_family_data(self.m_pyhouse_obj, self.m_obj[1], l_xml)
        # print(PrettyFormatAny.form(l_obj, 'B2-06-A - Obj'))
        # print(PrettyFormatAny.form(l_xml, 'B2-06-B - XML'))
        self.assertEqual(l_xml.find('UPBAddress').text, TESTING_UPB_ADDRESS)
        self.assertEqual(l_xml.find('UPBNetworkID').text, TESTING_UPB_NETWORK)
        self.assertEqual(l_xml.find('UPBPassword').text, TESTING_UPB_PASSWORD)

    def test_07_OneLight0(self):
        """ Write out the XML file for the location secWriteXmltion
        """
        l_xml = lightsXML()._write_one_light_xml(self.m_pyhouse_obj, self.m_obj[0])
        print(PrettyFormatAny.form(l_xml, 'B2-07-A - XML'))
        self.assertEqual(l_xml.attrib['Name'], TESTING_LIGHT_NAME_0)
        self.assertEqual(l_xml.attrib['Key'], TESTING_LIGHT_KEY_0)
        self.assertEqual(l_xml.attrib['Active'], TESTING_LIGHT_ACTIVE_0)
        self.assertEqual(l_xml.find('UUID').text, TESTING_LIGHT_UUID_0)
        self.assertEqual(l_xml.find('Comment').text, TESTING_LIGHT_COMMENT_0)
        self.assertEqual(l_xml.find('DeviceFamily').text, TESTING_DEVICE_FAMILY_INSTEON)
        self.assertEqual(l_xml.find('RoomName').text, TESTING_LIGHT_ROOM_NAME_0)
        self.assertEqual(l_xml.find('RoomUUID').text, TESTING_LIGHT_ROOM_UUID_0)
        self.assertEqual(l_xml.find('Brightness').text, TESTING_LIGHT_CUR_LEVEL_0)
        self.assertEqual(l_xml.find('IsDimmable').text, TESTING_LIGHT_IS_DIMMABLE_0)
        self.assertEqual(l_xml.find('InsteonAddress').text, TESTING_INSTEON_ADDRESS_0)
        self.assertEqual(l_xml.find('DevCat').text, TESTING_INSTEON_DEVCAT_0)
        self.assertEqual(l_xml.find('GroupList').text, TESTING_INSTEON_GROUP_LIST_0)
        self.assertEqual(l_xml.find('GroupNumber').text, TESTING_INSTEON_GROUP_NUM_0)
        self.assertEqual(l_xml.find('ProductKey').text, TESTING_INSTEON_PRODUCT_KEY_0)

    def test_08_OneLight1(self):
        """ Write out the XML file for the location section
        """
        l_xml = lightsXML()._write_one_light_xml(self.m_pyhouse_obj, self.m_obj[1])
        # print(PrettyFormatAny.form(l_xml, 'B2-08-A - XML'))
        self.assertEqual(l_xml.attrib['Name'], TESTING_LIGHT_NAME_1)
        self.assertEqual(l_xml.attrib['Key'], TESTING_LIGHT_KEY_1)
        self.assertEqual(l_xml.attrib['Active'], TESTING_LIGHT_ACTIVE_1)
        self.assertEqual(l_xml.find('UUID').text, TESTING_LIGHT_UUID_1)
        self.assertEqual(l_xml.find('Comment').text, TESTING_LIGHT_COMMENT_1)
        self.assertEqual(l_xml.find('DeviceFamily').text, TESTING_LIGHT_DEVICE_FAMILY_1)
        self.assertEqual(l_xml.find('RoomName').text, TESTING_LIGHT_ROOM_NAME_1)
        self.assertEqual(l_xml.find('RoomUUID').text, TESTING_LIGHT_ROOM_UUID_1)
        self.assertEqual(l_xml.find('Brightness').text, TESTING_LIGHT_CUR_LEVEL_1)
        self.assertEqual(l_xml.find('IsDimmable').text, TESTING_LIGHT_IS_DIMMABLE_1)
        self.assertEqual(l_xml.find('UPBAddress').text, TESTING_UPB_ADDRESS)
        self.assertEqual(l_xml.find('UPBNetworkID').text, TESTING_UPB_NETWORK)
        self.assertEqual(l_xml.find('UPBPassword').text, TESTING_UPB_PASSWORD)

    def test_09_AllLights(self):
        l_objs = lightsXML().read_all_lights_xml(self.m_pyhouse_obj)
        self.m_pyhouse_obj.House.Lighting = LightingData()
        self.m_pyhouse_obj.House.Lighting.Lights = l_objs
        l_xml = lightsXML().write_all_lights_xml(self.m_pyhouse_obj)
        # print(PrettyFormatAny.form(l_xml, 'W1-05-A - Lights XML'))
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
        l_obj = lightsXML().read_all_lights_xml(self.m_pyhouse_obj)
        # print(PrettyFormatAny.form(l_obj, 'Z1-01-A - Lights'))
        l_json = json_tools.encode_json(l_obj)
        # print(PrettyFormatAny.form(l_json, 'Z1-01-B - JSON'))
        self.assertEqual(l_json[0], '{')

#  ## END DBK
