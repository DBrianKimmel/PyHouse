"""
@name:      PyHouse/src/Modules/families/Insteon/test/test_Insteon_xml.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2014-2017 by D. Brian Kimmel
@note:      Created on Aug 5, 2014
@license:   MIT License
@summary:   This module test insteon xml

Passed all 15 tests - DBK - 2017-04-20

"""

__updated__ = '2017-04-28'

# Import system type stuff
import xml.etree.ElementTree as ET
from twisted.trial import unittest

# Import PyMh files and modules.
from test.testing_mixin import SetupPyHouseObj
from test.xml_data import XML_LONG, TESTING_PYHOUSE
from Modules.Core.data_objects import LightData, HouseInformation, ButtonData
from Modules.Families.Insteon.Insteon_xml import Xml as insteonXml
from Modules.Core import conversions
from Modules.Core.test.xml_device import \
    TESTING_DEVICE_FAMILY_INSTEON
from Modules.Families.Insteon.test.xml_insteon import \
    TESTING_INSTEON_ADDRESS_0, \
    TESTING_INSTEON_DEVCAT_0, \
    TESTING_INSTEON_GROUP_LIST_0, \
    TESTING_INSTEON_GROUP_NUM_0, \
    TESTING_INSTEON_PRODUCT_KEY_0, \
    TESTING_INSTEON_ENGINE_VERSION_0, \
    TESTING_INSTEON_FIRMWARE_VERSION_0
from Modules.Housing.Lighting.test.xml_lights import \
    TESTING_LIGHT_NAME_0, \
    TESTING_LIGHT_KEY_0, \
    TESTING_LIGHT_ACTIVE_0, \
    TESTING_LIGHT_COMMENT_0, \
    TESTING_LIGHT_DEVICE_SUBTYPE_0, \
    TESTING_LIGHT_UUID_0, \
    TESTING_LIGHT_DEVICE_FAMILY_0, \
    TESTING_LIGHT_DEVICE_TYPE_0, \
    TESTING_LIGHT_ROOM_NAME_0, \
    TESTING_LIGHT_ROOM_UUID_0, XML_LIGHT_SECTION, TESTING_LIGHT_SECTION
from Modules.Core.Utilities.device_tools import XML as deviceXML
from Modules.Core.Utilities.debug_tools import PrettyFormatAny


class SetupMixin(object):
    """ Set up pyhouse object
    """

    def setUp(self, p_root):
        self.m_pyhouse_obj = SetupPyHouseObj().BuildPyHouseObj(p_root)
        self.m_xml = SetupPyHouseObj().BuildXml(p_root)
        self.m_device = LightData()
        self.m_version = '1.4.0'
        self.m_api = deviceXML


class A0(unittest.TestCase):
    def setUp(self):
        pass
    def test_00_Print(self):
        print('Id: test_Insteon_xml')


class A1_Prep(SetupMixin, unittest.TestCase):
    """ This section tests the setup
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))
        self.m_device = None

    def test_01_PyHouse(self):
        """ Did we get everything set up for the rest of the tests of this class.
        """
        self.assertIsInstance(self.m_pyhouse_obj.House, HouseInformation)

    def test_02_FindXml(self):
        """ Did we get everything set up for the rest of the tests of this class.
        """
        self.assertEqual(self.m_xml.root.tag, TESTING_PYHOUSE)
        self.assertEqual(self.m_xml.house_div.tag, 'HouseDivision')
        self.assertEqual(self.m_xml.lighting_sect.tag, 'LightingSection')
        self.assertEqual(self.m_xml.light_sect.tag, 'LightSection')
        self.assertEqual(self.m_xml.button_sect.tag, 'ButtonSection')
        self.assertEqual(self.m_xml.controller_sect.tag, 'ControllerSection')

    def test_03_House(self):
        """ Did we get everything set up for the rest of the tests of this class.
        """
        pass

    def test_04_Objs(self):
        """ Did we get everything set up for the rest of the tests of this class.
        """
        pass

    def test_05_XML(self):
        """ Did we get everything set up for the rest of the tests of this class.
        """
        pass

    def test_06_Device(self):
        """ Be sure that the XML contains the right stuff.
        """


class A2_Xml(SetupMixin, unittest.TestCase):

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring('<x />'))
        pass

    def test_01_Raw(self):
        l_raw = XML_LIGHT_SECTION
        # print(l_raw)
        self.assertEqual(l_raw[:14], '<' + TESTING_LIGHT_SECTION + '>')

    def test_02_Parsed(self):
        l_xml = ET.fromstring(XML_LIGHT_SECTION)
        # print(l_xml)
        self.assertEqual(l_xml.tag, TESTING_LIGHT_SECTION)


class C1_Read(SetupMixin, unittest.TestCase):
    """ This section tests the reading and writing of XML.
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))

    def test_01_ProductKey(self):
        l_product_key = insteonXml._read_product_key(self.m_xml.light)
        self.assertEqual(conversions.int2dotted_hex(l_product_key, 3), TESTING_INSTEON_PRODUCT_KEY_0)

    def test_02_Core(self):
        l_light = self.m_api.read_base_device_object_xml(self.m_pyhouse_obj, self.m_device, self.m_xml.light)
        # print(PrettyFormatAny.form(l_light, 'C1-02-A - Light'))
        self.assertEqual(l_light.Name, TESTING_LIGHT_NAME_0)
        self.assertEqual(l_light.Key, int(TESTING_LIGHT_KEY_0))
        self.assertEqual(l_light.Active, TESTING_LIGHT_ACTIVE_0 == 'True')
        self.assertEqual(l_light.Comment, TESTING_LIGHT_COMMENT_0)
        self.assertEqual(str(l_light.DeviceType), TESTING_LIGHT_DEVICE_TYPE_0)
        self.assertEqual(str(l_light.DeviceSubType), TESTING_LIGHT_DEVICE_SUBTYPE_0)
        self.assertEqual(l_light.RoomName, TESTING_LIGHT_ROOM_NAME_0)
        self.assertEqual(l_light.RoomUUID, TESTING_LIGHT_ROOM_UUID_0)
        self.assertEqual(l_light.UUID, TESTING_LIGHT_UUID_0)

    def test_03_Insteon(self):
        """Read the Insteon specific information.
        """
        l_obj = insteonXml._read_insteon(self.m_xml.light)
        # print(PrettyFormatAny.form(l_obj, 'C1-03-A - Insteon (only)'))
        self.assertEqual(conversions.int2dotted_hex(l_obj.DevCat, 2), TESTING_INSTEON_DEVCAT_0)
        self.assertEqual(str(l_obj.EngineVersion), TESTING_INSTEON_ENGINE_VERSION_0)
        self.assertEqual(str(l_obj.FirmwareVersion), TESTING_INSTEON_FIRMWARE_VERSION_0)
        self.assertEqual(l_obj.GroupList, TESTING_INSTEON_GROUP_LIST_0)
        self.assertEqual(str(l_obj.GroupNumber), TESTING_INSTEON_GROUP_NUM_0)
        self.assertEqual(conversions.int2dotted_hex(l_obj.InsteonAddress, 3), TESTING_INSTEON_ADDRESS_0)
        self.assertEqual(conversions.int2dotted_hex(l_obj.ProductKey, 3), TESTING_INSTEON_PRODUCT_KEY_0)

    def test_04_Insteon(self):
        """Read the Insteon specific information.
        """
        l_dev = ButtonData()
        l_obj = insteonXml.ReadXml(l_dev, self.m_xml.light)
        # print(PrettyFormatAny.form(l_obj, 'C1-04-A - Insteon Device'))
        self.assertEqual(conversions.int2dotted_hex(l_obj.DevCat, 2), TESTING_INSTEON_DEVCAT_0)
        self.assertEqual(str(l_obj.EngineVersion), TESTING_INSTEON_ENGINE_VERSION_0)
        self.assertEqual(str(l_obj.FirmwareVersion), TESTING_INSTEON_FIRMWARE_VERSION_0)
        self.assertEqual(l_obj.GroupList, TESTING_INSTEON_GROUP_LIST_0)
        self.assertEqual(str(l_obj.GroupNumber), TESTING_INSTEON_GROUP_NUM_0)
        self.assertEqual(conversions.int2dotted_hex(l_obj.InsteonAddress, 3), TESTING_INSTEON_ADDRESS_0)
        self.assertEqual(conversions.int2dotted_hex(l_obj.ProductKey, 3), TESTING_INSTEON_PRODUCT_KEY_0)

    def test_05_InsteonLight(self):
        l_light = self.m_api.read_base_device_object_xml(self.m_pyhouse_obj, self.m_device, self.m_xml.light)
        insteonXml.ReadXml(l_light, self.m_xml.light)
        # print(PrettyFormatAny.form(l_light, 'C1-05-A - Insteon Light'))
        self.assertEqual(l_light.Name, TESTING_LIGHT_NAME_0)
        self.assertEqual(l_light.DeviceFamily, TESTING_DEVICE_FAMILY_INSTEON)
        self.assertEqual(l_light.InsteonAddress, conversions.dotted_hex2int(TESTING_INSTEON_ADDRESS_0))


class C2_Write(SetupMixin, unittest.TestCase):
    """ This section tests the reading and writing of XML used by node_local.
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))
        self.m_light = self.m_api.read_base_device_object_xml(self.m_pyhouse_obj, self.m_device, self.m_xml.light)
        insteonXml.ReadXml(self.m_light, self.m_xml.light)

    def test_01_setup(self):
        # print(PrettyFormatAny.form(self.m_light, 'C2-01-A - Light Device 2'))
        self.assertEqual(self.m_light.Name, TESTING_LIGHT_NAME_0)
        self.assertEqual(self.m_light.DeviceFamily, TESTING_DEVICE_FAMILY_INSTEON)
        self.assertEqual(self.m_light.InsteonAddress, conversions.dotted_hex2int(TESTING_INSTEON_ADDRESS_0))

    def test_02_Core(self):
        l_xml = self.m_api.write_base_device_object_xml('Light', self.m_light)
        # print(PrettyFormatAny.form(l_xml, 'C2-02-A - Lights XML'))
        self.assertEqual(l_xml.attrib['Name'], TESTING_LIGHT_NAME_0)
        self.assertEqual(l_xml.attrib['Key'], TESTING_LIGHT_KEY_0)
        self.assertEqual(l_xml.attrib['Active'], TESTING_LIGHT_ACTIVE_0)
        self.assertEqual(l_xml.find('Comment').text, TESTING_LIGHT_COMMENT_0)
        self.assertEqual(l_xml.find('DeviceFamily').text, TESTING_LIGHT_DEVICE_FAMILY_0)
        self.assertEqual(l_xml.find('RoomName').text, TESTING_LIGHT_ROOM_NAME_0)

    def test_03_InsteonLight(self):
        l_xml = self.m_api.write_base_device_object_xml('Light', self.m_light)
        insteonXml.WriteXml(l_xml, self.m_light)
        # print(PrettyFormatAny.form(l_xml, 'C2_03-A - Lights XML'))
        self.assertEqual(l_xml.attrib['Name'], TESTING_LIGHT_NAME_0)
        self.assertEqual(l_xml.attrib['Key'], TESTING_LIGHT_KEY_0)
        self.assertEqual(l_xml.attrib['Active'], TESTING_LIGHT_ACTIVE_0)
        self.assertEqual(l_xml.find('DevCat').text, TESTING_INSTEON_DEVCAT_0)
        self.assertEqual(l_xml.find('EngineVersion').text, TESTING_INSTEON_ENGINE_VERSION_0)
        self.assertEqual(l_xml.find('FirmwareVersion').text, TESTING_INSTEON_FIRMWARE_VERSION_0)
        self.assertEqual(l_xml.find('GroupList').text, TESTING_INSTEON_GROUP_LIST_0)
        self.assertEqual(l_xml.find('GroupNumber').text, TESTING_INSTEON_GROUP_NUM_0)
        self.assertEqual(l_xml.find('InsteonAddress').text, TESTING_INSTEON_ADDRESS_0)
        self.assertEqual(l_xml.find('ProductKey').text, TESTING_INSTEON_PRODUCT_KEY_0)

# ## END
