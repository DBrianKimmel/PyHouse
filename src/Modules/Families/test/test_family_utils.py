"""
@name:      PyHouse/src/Modules/Families/test/test_family_utils.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2014_2015 by D. Brian Kimmel
@license:   MIT License
@note:      Created on Nov 15, 2014
@Summary:

Passed all 12 tests.  DBK 2015-08-08
"""

# Import system type stuff
import xml.etree.ElementTree as ET
from twisted.trial import unittest

# Import PyMh files and modules.
from Modules.Core.data_objects import LightData
from Modules.Core import conversions
from Modules.Families import VALID_FAMILIES
from Modules.Families.family import API as familyAPI
from Modules.Families.family_utils import FamUtil
from Modules.Lighting.lighting_core import API as LightingCoreAPI
from test.xml_data import XML_LONG
from test.testing_mixin import SetupPyHouseObj
from Modules.Lighting.test.xml_lights import \
        TESTING_LIGHT_NAME_0, \
        TESTING_LIGHT_NAME_1
from Modules.Families.Insteon.test.xml_insteon import \
        TESTING_INSTEON_PRODUCT_KEY_0, \
        TESTING_INSTEON_ADDRESS_0, \
        TESTING_INSTEON_DEVCAT_0
from Modules.Core.test.xml_device import \
        TESTING_DEVICE_ROOM_NAME, \
        TESTING_DEVICE_FAMILY_INSTEON
from Modules.Utilities.debug_tools import PrettyFormatAny


class SetupMixin(object):

    def setUp(self, p_root):
        self.m_pyhouse_obj = SetupPyHouseObj().BuildPyHouseObj(p_root)
        self.m_pyhouse_obj.House.FamilyData = familyAPI(self.m_pyhouse_obj).m_family
        self.m_xml = SetupPyHouseObj().BuildXml(p_root)
        self.m_device_obj = LightData()
        self.m_device_obj.Name = TESTING_LIGHT_NAME_0
        self.m_device_obj.DeviceFamily = TESTING_DEVICE_FAMILY_INSTEON
        self.m_device_obj.Active = True
        self.m_device_obj.DeviceType = 1
        self.m_device_obj.DeviceSubType = 234
        self.m_version = '1.4.0'


class A1_Setup(SetupMixin, unittest.TestCase):
    """ Test to see if we are set up properly
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))

    def test_01_Setup(self):
        """ Did we get everything set up for the rest of the tests of this class.
        """
        # print(PrettyFormatAny.form(VALID_FAMILIES, 'Valid'))
        self.assertEqual(len(VALID_FAMILIES), len(self.m_pyhouse_obj.House.FamilyData))
        self.assertEqual(VALID_FAMILIES[0], 'Null')
        self.assertEqual(VALID_FAMILIES[1], 'Insteon')
        self.assertEqual(VALID_FAMILIES[2], 'UPB')
        self.assertEqual(VALID_FAMILIES[3], 'X10')


class B1_Utils(SetupMixin, unittest.TestCase):
    """ This section tests the reading and writing of XML used by node_local.
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))

    def test_01_GetDeviceName(self):
        l_device = FamUtil._get_device_name(self.m_device_obj)
        # print(PrettyFormatAny.form(l_device, 'Family'))
        self.assertEqual(l_device, TESTING_LIGHT_NAME_0)

    def test_03_GetFamilyObj(self):
        l_obj = FamUtil._get_family_obj(self.m_pyhouse_obj, self.m_device_obj)
        print(PrettyFormatAny.form(l_obj, 'Family'))
        self.assertEqual(l_obj.Name, TESTING_LIGHT_NAME_0)
        self.assertEqual(l_obj.Active, True)
        self.assertEqual(l_obj.Key, 1)
        self.assertEqual(l_obj.FamilyDeviceModuleName, 'Insteon_device')
        self.assertEqual(l_obj.FamilyPackageName, 'Modules.Families.Insteon')
        self.assertEqual(l_obj.FamilyXmlModuleName, 'Insteon_xml')

    def test_04_GetInsteon(self):
        """ Did we get a family?
        """
        l_family = FamUtil.get_family(self.m_device_obj)
        print(PrettyFormatAny.form(l_family, 'Family'))
        self.assertEqual(l_family, TESTING_DEVICE_FAMILY_INSTEON)
        self.m_device_obj.DeviceFamily = 'UPB'
        l_family = FamUtil.get_family(self.m_device_obj)
        self.assertEqual(l_family, 'UPB')

    def test_05_GetApi(self):
        l_api = FamUtil._get_family_device_api(self.m_pyhouse_obj, self.m_device_obj)
        print(PrettyFormatAny.form(l_api, 'API'))
        self.assertNotEqual(l_api, None)


class C1_Read(SetupMixin, unittest.TestCase):
    """ This section tests the reading and writing of XML used by node_local.
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))
        self.m_device_obj.DeviceFamily = TESTING_DEVICE_FAMILY_INSTEON
        self.m_api = FamUtil._get_family_device_api(self.m_pyhouse_obj, self.m_device_obj)

    def test_01_Xml(self):
        """ Did we get the XML correctly
        """
        l_xml = self.m_xml.light
        print(PrettyFormatAny.form(l_xml, 'XML'))
        self.assertEqual(l_xml.attrib['Name'], TESTING_LIGHT_NAME_0)
        self.assertEqual(l_xml.find('DeviceFamily').text, TESTING_DEVICE_FAMILY_INSTEON)

    def test_02_Device(self):
        """ Did we get the Device correctly
        """
        l_device = self.m_device_obj
        print(PrettyFormatAny.form(l_device, 'Device'))
        self.assertEqual(l_device.Name, TESTING_LIGHT_NAME_0)
        self.assertEqual(l_device.Key, 0)
        self.assertEqual(l_device.Active, True)
        self.assertEqual(l_device.DeviceFamily, TESTING_DEVICE_FAMILY_INSTEON)
        self.assertEqual(l_device.DeviceType, 1)
        self.assertEqual(l_device.DeviceSubType, 234)
        self.assertEqual(l_device.RoomName, '')

    def test_03_Family(self):
        """ Did we get everything set up for the rest of the tests of this class.
        """
        l_xml = self.m_xml.light
        l_device = self.m_device_obj
        l_light = FamUtil.read_family_data(self.m_pyhouse_obj, l_device, l_xml)
        print(PrettyFormatAny.form(l_light, 'Light'))
        self.assertEqual(l_light.InsteonAddress, conversions.dotted_hex2int(TESTING_INSTEON_ADDRESS_0))

    def test_04_Light(self):
        """ Did we get everything set up for the rest of the tests of this class.
        """
        l_xml = self.m_xml.light
        l_device = self.m_device_obj
        l_light = LightingCoreAPI.read_core_lighting_xml(self.m_pyhouse_obj, l_device, l_xml)
        print(PrettyFormatAny.form(l_light, 'Light'))
        self.assertEqual(l_light.Name, TESTING_LIGHT_NAME_0)
        self.assertEqual(l_device.RoomName, TESTING_DEVICE_ROOM_NAME)

    def test_05_All(self):
        """ Did we get everything set up for the rest of the tests of this class.
        """
        l_xml = self.m_xml.light
        l_device = self.m_device_obj
        #
        l_light = LightingCoreAPI.read_core_lighting_xml(self.m_pyhouse_obj, l_device, l_xml)
        FamUtil.read_family_data(self.m_pyhouse_obj, l_light, l_xml)
        print(PrettyFormatAny.form(l_light, 'Light'))
        self.assertEqual(l_light.Name, TESTING_LIGHT_NAME_0)
        self.assertEqual(l_light.DeviceFamily, TESTING_DEVICE_FAMILY_INSTEON)
        self.assertEqual(l_light.InsteonAddress, conversions.dotted_hex2int(TESTING_INSTEON_ADDRESS_0))
        self.assertEqual(l_light.DevCat, conversions.dotted_hex2int(TESTING_INSTEON_DEVCAT_0))
        self.assertEqual(conversions.int2dotted_hex(l_light.ProductKey, 3), TESTING_INSTEON_PRODUCT_KEY_0)


class D1_Write(SetupMixin, unittest.TestCase):
    """ This section tests the reading and writing of XML used by node_local.
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))
        self.m_device_obj.DeviceFamily = TESTING_DEVICE_FAMILY_INSTEON
        self.m_api = FamUtil._get_family_device_api(self.m_pyhouse_obj, self.m_device_obj)
        self.m_light = LightingCoreAPI.read_core_lighting_xml(self.m_pyhouse_obj, self.m_device_obj, self.m_xml.controller)

    def test_01_Data(self):
        pass

    def test_02_All(self):
        """ Did we get everything set up for the rest of the tests of this class.
        """
        l_in_xml = self.m_xml.light
        l_device = self.m_device_obj
        l_light = LightingCoreAPI.read_core_lighting_xml(self.m_pyhouse_obj, l_device, l_in_xml)
        FamUtil.read_family_data(self.m_pyhouse_obj, l_light, l_in_xml)
        l_out_xml = LightingCoreAPI.write_core_lighting_xml('Light', l_light)
        FamUtil.write_family_data(self.m_pyhouse_obj, l_out_xml, l_light)
        self.assertEqual(l_light.Name, TESTING_LIGHT_NAME_0)
        self.assertEqual(l_light.DeviceFamily, TESTING_DEVICE_FAMILY_INSTEON)
        self.assertEqual(l_light.InsteonAddress, conversions.dotted_hex2int(TESTING_INSTEON_ADDRESS_0))

# ## END DBK
