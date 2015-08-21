"""
@name:      PyHouse/src/Modules/families/Insteon/test/test_Insteon_xml.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2014-2015 by D. Brian Kimmel
@note:      Created on Aug 5, 2014
@license:   MIT License
@summary:   This module test insteon xml

Passed all 13 tests - DBK - 2015-08-20

"""

# Import system type stuff
import xml.etree.ElementTree as ET
from twisted.trial import unittest

# Import PyMh files and modules.
from Modules.Core.data_objects import LightData, HouseInformation
from Modules.Families.Insteon.Insteon_xml import Xml as insteonXml
from Modules.Core import conversions
from Modules.Lighting.lighting_core import API as lightingCoreAPI
from test.xml_data import XML_LONG
from Modules.Lighting.test.xml_lights import \
        TESTING_LIGHTING_LIGHTS_NAME_1, \
        TESTING_LIGHTING_LIGHTS_KEY_1, \
        TESTING_LIGHTING_LIGHTS_ACTIVE_1
from Modules.Core.test.xml_device import \
        TESTING_DEVICE_FAMILY_INSTEON, \
        TESTING_DEVICE_COMMENT, \
        TESTING_DEVICE_ROOM_NAME, \
        TESTING_DEVICE_TYPE, \
        TESTING_DEVICE_SUBTYPE, \
        TESTING_DEVICE_UUID
from Modules.Families.Insteon.test.xml_insteon import \
        TESTING_INSTEON_ADDRESS, \
        TESTING_INSTEON_DEVCAT, \
        TESTING_INSTEON_GROUP_LIST, \
        TESTING_INSTEON_GROUP_NUM, \
        TESTING_INSTEON_PRODUCT_KEY
from test.testing_mixin import SetupPyHouseObj
from Modules.Utilities.debug_tools import PrettyFormatAny


class SetupMixin(object):
    """ Set up pyhouse object
    """

    def setUp(self, p_root):
        self.m_pyhouse_obj = SetupPyHouseObj().BuildPyHouseObj(p_root)
        self.m_xml = SetupPyHouseObj().BuildXml(p_root)
        self.m_core_api = lightingCoreAPI()
        self.m_device = LightData()
        self.m_version = '1.4.0'


class A1_Prep(SetupMixin, unittest.TestCase):
    """ This section tests the setup
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))
        self.m_device = None

    def test_01_PyHouse(self):
        """ Did we get everything set up for the rest of the tests of this class.
        """
        # PrettyPrintAny(self.m_pyhouse_obj, 'InsteonXML PyHouse')
        self.assertIsInstance(self.m_pyhouse_obj.House, HouseInformation)

    def test_02_Computer(self):
        """ Did we get everything set up for the rest of the tests of this class.
        """
        # PrettyPrintAny(self.m_pyhouse_obj.Computer, 'Computer')
        pass

    def test_03_House(self):
        """ Did we get everything set up for the rest of the tests of this class.
        """
        # PrettyPrintAny(self.m_pyhouse_obj.House, 'House')

    def test_04_Objs(self):
        """ Did we get everything set up for the rest of the tests of this class.
        """
        pass

    def test_05_XML(self):
        """ Did we get everything set up for the rest of the tests of this class.
        """
        # PrettyPrintAny(self.m_xml, 'XML')

    def test_06_Device(self):
        """ Be sure that the XML contains the right stuff.
        """
        self.assertEqual(self.m_xml.root.tag, 'PyHouse')
        self.assertEqual(self.m_xml.controller_sect.tag, 'ControllerSection')
        self.assertEqual(self.m_xml.controller.tag, 'Controller')


class B1_Read(SetupMixin, unittest.TestCase):
    """ This section tests the reading and writing of XML.
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))

    def test_01_ProductKey(self):
        l_product_key = insteonXml._read_product_key(self.m_xml.light)
        self.assertEqual(conversions.int2dotted_hex(l_product_key, 3), TESTING_INSTEON_PRODUCT_KEY)

    def test_02_Core(self):
        l_light = self.m_core_api.read_core_lighting_xml(self.m_device, self.m_xml.light, self.m_version)
        # print(PrettyFormatAny.form(l_light, 'Light'))
        self.assertEqual(l_light.Name, TESTING_LIGHTING_LIGHTS_NAME_1)
        self.assertEqual(l_light.Key, int(TESTING_LIGHTING_LIGHTS_KEY_1))
        self.assertEqual(l_light.Active, TESTING_LIGHTING_LIGHTS_ACTIVE_1 == 'True')
        self.assertEqual(l_light.Comment, TESTING_DEVICE_COMMENT)
        self.assertEqual(l_light.DeviceType, int(TESTING_DEVICE_TYPE))
        self.assertEqual(l_light.DeviceSubType, int(TESTING_DEVICE_SUBTYPE))
        self.assertEqual(l_light.RoomName, TESTING_DEVICE_ROOM_NAME)
        self.assertEqual(l_light.UUID, TESTING_DEVICE_UUID)

    def test_03_Insteon(self):
        """Read the Insteon specific information.
        """
        l_insteon = insteonXml._read_insteon(self.m_xml.light)
        self.assertEqual(conversions.int2dotted_hex(l_insteon.InsteonAddress, 3), TESTING_INSTEON_ADDRESS)
        self.assertEqual(conversions.int2dotted_hex(l_insteon.DevCat, 2), TESTING_INSTEON_DEVCAT)
        self.assertEqual(l_insteon.GroupList, TESTING_INSTEON_GROUP_LIST)
        self.assertEqual(l_insteon.GroupNumber, int(TESTING_INSTEON_GROUP_NUM))
        self.assertEqual(conversions.int2dotted_hex(l_insteon.ProductKey, 3), TESTING_INSTEON_PRODUCT_KEY)

    def test_04_InsteonLight(self):
        l_light = self.m_core_api.read_core_lighting_xml(self.m_device, self.m_xml.light, self.m_version)
        insteonXml.ReadXml(l_light, self.m_xml.light)
        self.assertEqual(l_light.Name, TESTING_LIGHTING_LIGHTS_NAME_1)
        self.assertEqual(l_light.DeviceFamily, TESTING_DEVICE_FAMILY_INSTEON)
        self.assertEqual(l_light.InsteonAddress, conversions.dotted_hex2int(TESTING_INSTEON_ADDRESS))


class C01_Write(SetupMixin, unittest.TestCase):
    """ This section tests the reading and writing of XML used by node_local.
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))
        self.m_light = self.m_core_api.read_core_lighting_xml(self.m_device, self.m_xml.light, self.m_version)
        insteonXml.ReadXml(self.m_light, self.m_xml.light)

    def test_01_setup(self):
        # print(PrettyFormatAny.form(self.m_light, 'Light Device 2'))
        self.assertEqual(self.m_light.Name, TESTING_LIGHTING_LIGHTS_NAME_1)
        self.assertEqual(self.m_light.DeviceFamily, TESTING_DEVICE_FAMILY_INSTEON)
        self.assertEqual(self.m_light.InsteonAddress, conversions.dotted_hex2int(TESTING_INSTEON_ADDRESS))

    def test_02_Core(self):
        l_xml = self.m_core_api.write_core_lighting_xml('Light', self.m_light)
        # print(PrettyFormatAny.form(l_xml, 'Lights XML'))
        self.assertEqual(l_xml.attrib['Name'], TESTING_LIGHTING_LIGHTS_NAME_1)
        self.assertEqual(l_xml.attrib['Key'], TESTING_LIGHTING_LIGHTS_KEY_1)
        self.assertEqual(l_xml.attrib['Active'], TESTING_LIGHTING_LIGHTS_ACTIVE_1)
        self.assertEqual(l_xml.find('Comment').text, TESTING_DEVICE_COMMENT)
        self.assertEqual(l_xml.find('DeviceFamily').text, TESTING_DEVICE_FAMILY_INSTEON)
        self.assertEqual(l_xml.find('RoomName').text, TESTING_DEVICE_ROOM_NAME)

    def test_03_InsteonLight(self):
        l_xml = self.m_core_api.write_core_lighting_xml('Light', self.m_light)
        insteonXml.WriteXml(l_xml, self.m_light)
        # print(PrettyFormatAny.form(l_xml, 'Lights XML'))
        self.assertEqual(l_xml.attrib['Name'], TESTING_LIGHTING_LIGHTS_NAME_1)
        self.assertEqual(l_xml.attrib['Key'], TESTING_LIGHTING_LIGHTS_KEY_1)
        self.assertEqual(l_xml.attrib['Active'], TESTING_LIGHTING_LIGHTS_ACTIVE_1)
        self.assertEqual(l_xml.find('Address').text, TESTING_INSTEON_ADDRESS)
        self.assertEqual(l_xml.find('DevCat').text, TESTING_INSTEON_DEVCAT)
        self.assertEqual(l_xml.find('GroupList').text, TESTING_INSTEON_GROUP_LIST)
        self.assertEqual(l_xml.find('GroupNumber').text, TESTING_INSTEON_GROUP_NUM)
        self.assertEqual(l_xml.find('ProductKey').text, TESTING_INSTEON_PRODUCT_KEY)

# ## END
