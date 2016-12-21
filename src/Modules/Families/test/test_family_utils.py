"""
@name:      PyHouse/src/Modules/Families/test/test_family_utils.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2014_2015 by D. Brian Kimmel
@license:   MIT License
@note:      Created on Nov 15, 2014
@Summary:

Passed all 17 tests.  DBK 2015-11-06
"""

__updated__ = '2016-11-06'

# Import system type stuff
import xml.etree.ElementTree as ET
from twisted.trial import unittest

# Import PyMh files and modules.
from test.xml_data import XML_LONG
from test.testing_mixin import SetupPyHouseObj
from Modules.Core.data_objects import LightData
from Modules.Core import conversions
from Modules.Families import VALID_FAMILIES
from Modules.Families.family import API as familyAPI
from Modules.Families.family_utils import FamUtil
from Modules.Utilities.device_tools import XML as deviceXML
from Modules.Housing.Lighting.test.xml_lights import \
    TESTING_LIGHT_NAME_0, \
    TESTING_LIGHT_ACTIVE_0, \
    TESTING_LIGHT_KEY_0, \
    TESTING_LIGHT_CUR_LEVEL_0, \
    TESTING_LIGHT_FAMILY_1, \
    TESTING_LIGHT_DEVICE_SUBTYPE_0, \
    TESTING_LIGHT_DEVICE_TYPE_0, \
    TESTING_LIGHT_ROOM_NAME_0
from Modules.Families.test.xml_family import \
    TESTING_FAMILY_NAME_1, TESTING_FAMILY_NAME_0, TESTING_FAMILY_NAME_2, TESTING_FAMILY_NAME_3
from Modules.Families.Insteon.test.xml_insteon import \
    TESTING_INSTEON_PRODUCT_KEY_0, \
    TESTING_INSTEON_ADDRESS_0, \
    TESTING_INSTEON_DEVCAT_0
from Modules.Core.test.xml_device import \
    TESTING_DEVICE_FAMILY_INSTEON, \
    TESTING_DEVICE_ROOM_COORDS, \
    TESTING_DEVICE_COMMENT_0, \
    TESTING_DEVICE_ROOM_UUID
from Modules.Utilities.debug_tools import PrettyFormatAny


class SetupMixin(object):

    def setUp(self, p_root):
        self.m_pyhouse_obj = SetupPyHouseObj().BuildPyHouseObj(p_root)
        self.m_pyhouse_obj.House.FamilyData = familyAPI(self.m_pyhouse_obj).m_family
        self.m_xml = SetupPyHouseObj().BuildXml(p_root)
        self.m_device_obj = LightData()
        self.m_device_obj.Name = TESTING_LIGHT_NAME_0
        self.m_device_obj.Key = TESTING_LIGHT_KEY_0
        self.m_device_obj.Active = TESTING_LIGHT_ACTIVE_0
        self.m_device_obj.Comment = TESTING_DEVICE_COMMENT_0
        self.m_device_obj.CurLevel = TESTING_LIGHT_CUR_LEVEL_0
        self.m_device_obj.DeviceFamily = TESTING_LIGHT_FAMILY_1
        self.m_device_obj.DeviceType = 1
        self.m_device_obj.DeviceSubType = 3
        self.m_device_obj.RoomCoords = TESTING_DEVICE_ROOM_COORDS
        self.m_device_obj.RoomName = TESTING_LIGHT_ROOM_NAME_0
        self.m_device_obj.RoomUID = TESTING_DEVICE_ROOM_UUID
        self.m_api = deviceXML()


class A0(unittest.TestCase):
    def setUp(self):
        pass
    def test_00_Print(self):
        print('Id: test_family_utils')


class A1_Setup(SetupMixin, unittest.TestCase):
    """ Test to see if we are set up properly
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))

    def test_01_Setup(self):
        """ Did we get everything set up for the rest of the tests of this class.
        """
        # print(PrettyFormatAny.form(VALID_FAMILIES, 'A1-01-A - Valid'))
        self.assertEqual(len(VALID_FAMILIES), len(self.m_pyhouse_obj.House.FamilyData))
        self.assertEqual(VALID_FAMILIES[0], TESTING_FAMILY_NAME_0)
        self.assertEqual(VALID_FAMILIES[1], TESTING_FAMILY_NAME_1)
        self.assertEqual(VALID_FAMILIES[2], TESTING_FAMILY_NAME_2)
        self.assertEqual(VALID_FAMILIES[3], TESTING_FAMILY_NAME_3)

    def test_02_Device(self):
        """ Did we get everything set up for the rest of the tests of this class.
        """
        # print(PrettyFormatAny.form(self.m_device_obj, 'A1-02-A - Device'))
        self.assertEqual(self.m_device_obj.Name, TESTING_LIGHT_NAME_0)


class B1_Utils(SetupMixin, unittest.TestCase):
    """ This section tests the reading and writing of XML used by node_local.
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))

    def test_01_GetDeviceName(self):
        """ Do we get back what we put in?
        """
        self.m_device_obj.Name = TESTING_FAMILY_NAME_0
        # print(PrettyFormatAny.form(self.m_device_obj, 'B1-01-A - Device'))
        l_name = FamUtil._get_device_name(self.m_device_obj)
        # print(PrettyFormatAny.form(l_name, 'B1-01-B - Family'))
        self.assertEqual(l_name, TESTING_FAMILY_NAME_0)

    def test_02_GetDeviceName(self):
        """ Do we get back what we put in?
        """
        self.m_device_obj.Name = TESTING_FAMILY_NAME_1
        # print(PrettyFormatAny.form(self.m_device_obj, 'B1-02-A - Device'))
        l_name = FamUtil._get_device_name(self.m_device_obj)
        # print(PrettyFormatAny.form(l_name, 'B1-02-B - Family'))
        self.assertEqual(l_name, TESTING_FAMILY_NAME_1)

    def test_03_GetFamilyObj(self):
        self.m_device_obj.DeviceFamily = TESTING_FAMILY_NAME_2
        # print(PrettyFormatAny.form(self.m_device_obj, 'B1-03-A - Device'))
        l_obj = FamUtil._get_family_obj(self.m_pyhouse_obj, self.m_device_obj)
        # print(PrettyFormatAny.form(l_obj, 'B1-03-B - Family'))
        self.assertEqual(l_obj.Name, TESTING_FAMILY_NAME_2)
        self.assertEqual(l_obj.Active, True)
        self.assertEqual(l_obj.Key, 2)
        self.assertEqual(l_obj.FamilyDeviceModuleName, 'UPB_device')
        self.assertEqual(l_obj.FamilyPackageName, 'Modules.Families.UPB')
        self.assertEqual(l_obj.FamilyXmlModuleName, 'UPB_xml')

    def test_04_GetFamilyObj(self):
        self.m_device_obj.DeviceFamily = TESTING_FAMILY_NAME_1
        # print(PrettyFormatAny.form(self.m_device_obj, 'B1-04-A - Device'))
        l_obj = FamUtil._get_family_obj(self.m_pyhouse_obj, self.m_device_obj)
        # print(PrettyFormatAny.form(l_obj, 'B1-04-B - Family'))
        self.assertEqual(l_obj.Name, TESTING_FAMILY_NAME_1)
        self.assertEqual(l_obj.Active, True)
        self.assertEqual(l_obj.Key, 1)
        self.assertEqual(l_obj.FamilyDeviceModuleName, 'Insteon_device')
        self.assertEqual(l_obj.FamilyPackageName, 'Modules.Families.Insteon')
        self.assertEqual(l_obj.FamilyXmlModuleName, 'Insteon_xml')

    def test_05_GetFamily(self):
        """ Did we get a family?
        """
        self.m_device_obj.DeviceFamily = TESTING_FAMILY_NAME_1
        l_family = FamUtil.get_family(self.m_device_obj)
        # print(PrettyFormatAny.form(l_family, 'B1-05-A - Family'))
        self.assertEqual(l_family, TESTING_FAMILY_NAME_1)

    def test_06_GetFamily(self):
        """ Did we get a family?
        """
        self.m_device_obj.DeviceFamily = TESTING_FAMILY_NAME_2
        l_family = FamUtil.get_family(self.m_device_obj)
        # print(PrettyFormatAny.form(l_family, 'B1-06-A - Family'))
        self.assertEqual(l_family, TESTING_FAMILY_NAME_2)

    def test_07_GetApi(self):
        self.m_device_obj.DeviceFamily = TESTING_FAMILY_NAME_1
        l_api = FamUtil._get_family_device_api(self.m_pyhouse_obj, self.m_device_obj)
        # print(PrettyFormatAny.form(l_api, 'B1-07-A - API'))
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
        print(PrettyFormatAny.form(l_xml, 'C1-01-A - XML'))
        self.assertEqual(l_xml.attrib['Name'], TESTING_LIGHT_NAME_0)
        self.assertEqual(l_xml.find('DeviceFamily').text, TESTING_DEVICE_FAMILY_INSTEON)

    def test_02_Device(self):
        """ Did we get the Device correctly
        """
        self.m_device_obj.DeviceFamily = TESTING_FAMILY_NAME_1
        l_device = self.m_device_obj
        print(PrettyFormatAny.form(l_device, 'C1-02-A - Device'))
        self.assertEqual(l_device.Name, TESTING_LIGHT_NAME_0)
        self.assertEqual(l_device.Key, TESTING_LIGHT_KEY_0)
        self.assertEqual(l_device.Active, TESTING_LIGHT_ACTIVE_0)
        self.assertEqual(l_device.DeviceFamily, TESTING_DEVICE_FAMILY_INSTEON)
        self.assertEqual(str(l_device.DeviceType), TESTING_LIGHT_DEVICE_TYPE_0)
        self.assertEqual(str(l_device.DeviceSubType), TESTING_LIGHT_DEVICE_SUBTYPE_0)
        self.assertEqual(l_device.RoomName, TESTING_LIGHT_ROOM_NAME_0)

    def test_03_Family(self):
        """ Did we get everything set up for the rest of the tests of this class.
        """
        l_xml = self.m_xml.light
        l_device = self.m_device_obj
        l_light = FamUtil.read_family_data(self.m_pyhouse_obj, l_device, l_xml)
        print(PrettyFormatAny.form(l_light, 'C1-03-A - Light'))
        self.assertEqual(l_light.InsteonAddress, conversions.dotted_hex2int(TESTING_INSTEON_ADDRESS_0))

    def test_04_Light(self):
        """ Did we get everything set up for the rest of the tests of this class.
        """
        l_xml = self.m_xml.light
        l_device = self.m_device_obj
        l_light = deviceXML.read_base_device_object_xml(self.m_pyhouse_obj, l_device, l_xml)
        print(PrettyFormatAny.form(l_light, 'C1-04-A - Light'))
        self.assertEqual(l_light.Name, TESTING_LIGHT_NAME_0)
        self.assertEqual(l_device.RoomName, TESTING_LIGHT_ROOM_NAME_0)

    def test_05_All(self):
        """ Did we get everything set up for the rest of the tests of this class.
        """
        l_xml = self.m_xml.light
        l_device = self.m_device_obj
        #
        l_light = deviceXML.read_base_device_object_xml(self.m_pyhouse_obj, l_device, l_xml)
        FamUtil.read_family_data(self.m_pyhouse_obj, l_light, l_xml)
        print(PrettyFormatAny.form(l_light, 'C1-05-A - Light'))
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
        self.m_light = deviceXML.read_base_device_object_xml(self.m_pyhouse_obj, self.m_device_obj, self.m_xml.controller)

    def test_01_Data(self):
        pass

    def test_02_All(self):
        """ Did we get everything set up for the rest of the tests of this class.
        """
        l_in_xml = self.m_xml.light
        l_device = self.m_device_obj
        l_light = deviceXML.read_base_device_object_xml(self.m_pyhouse_obj, l_device, l_in_xml)
        FamUtil.read_family_data(self.m_pyhouse_obj, l_light, l_in_xml)
        l_out_xml = deviceXML.write_base_device_object_xml('Light', l_light)
        FamUtil.write_family_data(self.m_pyhouse_obj, l_out_xml, l_light)
        self.assertEqual(l_light.Name, TESTING_LIGHT_NAME_0)
        self.assertEqual(l_light.DeviceFamily, TESTING_DEVICE_FAMILY_INSTEON)
        self.assertEqual(l_light.InsteonAddress, conversions.dotted_hex2int(TESTING_INSTEON_ADDRESS_0))

# ## END DBK
