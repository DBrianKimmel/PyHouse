"""
@name:      PyHouse/src/Modules/Families/UPB/_test/test_UPB_xml.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com>
@copyright: (c) 2014-2019 by briank
@license:   MIT License
@note:       Created on Aug 6, 2014
@Summary:

Passed all 6 tests - DBK - 2019-01-22

"""
from Modules.Core.test.xml_device import TESTING_DEVICE_FAMILY_UPB

__updated__ = '2019-07-09'

# Import system type stuff
from twisted.trial import unittest
import xml.etree.ElementTree as ET

# Import PyMh files and modules.
from test.xml_data import XML_LONG, TESTING_PYHOUSE
from Modules.Families.UPB.UPB_xml import Xml as upbXML
from Modules.Families.UPB.test.xml_upb import \
    TESTING_UPB_ADDRESS, \
    TESTING_UPB_NETWORK, \
    TESTING_UPB_PASSWORD
from Modules.Housing.Lighting.test.xml_lights import \
    XML_LIGHT_SECTION, \
    TESTING_LIGHT_SECTION, \
    TESTING_LIGHT_NAME_1, \
    TESTING_LIGHT_KEY_1, \
    TESTING_LIGHT_ACTIVE_1, \
    TESTING_LIGHT_COMMENT_1, \
    TESTING_LIGHT_DEVICE_TYPE_1, \
    TESTING_LIGHT_DEVICE_SUBTYPE_1, \
    TESTING_LIGHT_ROOM_NAME_1, \
    TESTING_LIGHT_ROOM_UUID_1, \
    TESTING_LIGHT_UUID_1
from Modules.Core.data_objects import ControllerInformation, HouseInformation
from Modules.Housing.Lighting.lighting_lights import LightData
from test.testing_mixin import SetupPyHouseObj
from Modules.Core.Utilities.device_tools import XML as deviceXML
from Modules.Core.Utilities.debug_tools import PrettyFormatAny


class SetupMixin(object):
    """
    """

    def setUp(self, p_root):
        self.m_pyhouse_obj = SetupPyHouseObj().BuildPyHouseObj(p_root)
        self.m_xml = SetupPyHouseObj().BuildXml(p_root)
        self.m_api = deviceXML
        self.m_device = LightData()


class A1_XML(SetupMixin, unittest.TestCase):

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))

    def test_01_Read(self):
        l_list = list(self.m_xml.controller_sect.iterfind('Controller'))
        l_xml = l_list[1]
        l_dev = ControllerInformation()
        upbXML.ReadXml(l_dev, l_xml)
        self.assertEqual(l_dev.UPBAddress, int(TESTING_UPB_ADDRESS))
        self.assertEqual(l_dev.UPBNetworkID, int(TESTING_UPB_NETWORK))
        self.assertEqual(l_dev.UPBPassword, int(TESTING_UPB_PASSWORD))

    def test_02_Write(self):
        l_list = list(self.m_xml.controller_sect.iterfind('Controller'))
        l_xml = l_list[1]
        l_dev = ControllerInformation()
        upbXML.ReadXml(l_dev, l_xml)
        l_out = ET.Element('Testing')
        upbXML.WriteXml(l_out, l_dev)


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
        print('A2-02-A - Parsed\n{}'.format(PrettyFormatAny.form(l_xml, 'A2-02-A - Parsed')))
        self.assertEqual(l_xml.tag, TESTING_LIGHT_SECTION)


class C1_Read(SetupMixin, unittest.TestCase):
    """ This section tests the reading and writing of XML.
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))

    def test_01_Core(self):
        l_xml = self.m_xml.light_sect[1]
        l_light = self.m_api.read_base_device_object_xml(self.m_device, l_xml)
        # print(PrettyFormatAny.form(l_light, 'C1-01-A - Light'))
        self.assertEqual(l_light.Name, TESTING_LIGHT_NAME_1)
        self.assertEqual(l_light.Key, int(TESTING_LIGHT_KEY_1))
        self.assertEqual(l_light.Active, TESTING_LIGHT_ACTIVE_1 == 'True')
        self.assertEqual(l_light.Comment, TESTING_LIGHT_COMMENT_1)
        self.assertEqual(str(l_light.DeviceType), TESTING_LIGHT_DEVICE_TYPE_1)
        self.assertEqual(str(l_light.DeviceSubType), TESTING_LIGHT_DEVICE_SUBTYPE_1)
        self.assertEqual(l_light.RoomName, TESTING_LIGHT_ROOM_NAME_1)
        self.assertEqual(l_light.RoomUUID, TESTING_LIGHT_ROOM_UUID_1)
        self.assertEqual(l_light.UUID, TESTING_LIGHT_UUID_1)

    def test_05_UPBLight(self):
        l_light = self.m_api.read_base_device_object_xml(self.m_device, self.m_xml.light)
        insteonXml.ReadXml(l_light, self.m_xml.light)
        # print(PrettyFormatAny.form(l_light, 'C1-05-A - Insteon Light'))
        self.assertEqual(l_light.Name, TESTING_LIGHT_NAME_1)
        self.assertEqual(l_light.DeviceFamily, TESTING_DEVICE_FAMILY_UPB)


from Modules.Families.Insteon.Insteon_xml import Xml as insteonXml


class C2_Write(SetupMixin, unittest.TestCase):
    """ This section tests the reading and writing of XML used by node_local.
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))
        self.m_light = self.m_api.read_base_device_object_xml(self.m_device, self.m_xml.light)
        upbXML.ReadXml(self.m_light, self.m_xml.light)

    def test_01_setup(self):
        # print(PrettyFormatAny.form(self.m_light, 'C2-01-A - Light Device 2'))
        self.assertEqual(self.m_light.Name, TESTING_LIGHT_NAME_1)
        self.assertEqual(self.m_light.DeviceFamily, TESTING_DEVICE_FAMILY_UPB)

    def test_02_Core(self):
        l_xml = self.m_api.write_base_device_object_xml('Light', self.m_light)
        # print(PrettyFormatAny.form(l_xml, 'C2-02-A - Lights XML'))
        self.assertEqual(l_xml.attrib['Name'], TESTING_LIGHT_NAME_0)
        self.assertEqual(l_xml.attrib['Key'], TESTING_LIGHT_KEY_0)
        self.assertEqual(l_xml.attrib['Active'], TESTING_LIGHT_ACTIVE_0)
        self.assertEqual(l_xml.find('Comment').text, TESTING_LIGHT_COMMENT_0)
        self.assertEqual(l_xml.find('DeviceFamily').text, TESTING_LIGHT_DEVICE_FAMILY_0)
        self.assertEqual(l_xml.find('RoomName').text, TESTING_LIGHT_ROOM_NAME_0)

    def test_03_UpbLight(self):
        l_xml = self.m_api.write_base_device_object_xml('Light', self.m_light)
        insteonXml.WriteXml(l_xml, self.m_light)
        print(PrettyFormatAny.form(l_xml, 'C2_03-A - Lights XML'))
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

# ## END DBK
