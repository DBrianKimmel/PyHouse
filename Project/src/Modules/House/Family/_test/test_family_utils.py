"""
@name:      PyHouse/src/Modules/Families/_test/test_family_utils.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2014_2019 by D. Brian Kimmel
@license:   MIT License
@note:      Created on Nov 15, 2014
@Summary:

Passed all 35 tests.  DBK 2019-02-21

"""

__updated__ = '2019-10-08'

# Import system type stuff
import xml.etree.ElementTree as ET
from twisted.trial import unittest

# Import PyMh files and modules.
from test.xml_data import XML_LONG, TESTING_PYHOUSE
from test.testing_mixin import SetupPyHouseObj
from Modules.Core.Utilities import convert
from Modules.House.Family import VALID_FAMILIES
from Modules.House.Family.family import Api as familyApi
from Modules.House.Family import family_utils
from Modules.House.Family.family_utils import FamUtil
from Modules.Core.Utilities.device_tools import XML as deviceXML
from Modules.House.Lighting.lighting_lights import LightData
from Modules.Core.Utilities.debug_tools import PrettyFormatAny


class SetupMixin(object):

    def createLightData(self):
        l_dev_obj = LightData()
        l_dev_obj.Name = TESTING_LIGHT_NAME_0
        l_dev_obj.Key = TESTING_LIGHT_KEY_0
        l_dev_obj.Active = TESTING_LIGHT_ACTIVE_0
        l_dev_obj.Comment = TESTING_DEVICE_COMMENT_0
        l_dev_obj.BrightnessPct = TESTING_LIGHT_CUR_LEVEL_0
        l_dev_obj.DeviceFamily = TESTING_LIGHT_DEVICE_FAMILY_0
        l_dev_obj.DeviceType = 1
        l_dev_obj.DeviceSubType = 3
        l_dev_obj.RoomCoords = TESTING_LIGHT_ROOM_COORDS_0
        l_dev_obj.RoomName = TESTING_LIGHT_ROOM_NAME_0
        l_dev_obj.RoomUID = TESTING_LIGHT_ROOM_UUID_0
        return l_dev_obj

    def setUp(self, p_root):
        self.m_pyhouse_obj = SetupPyHouseObj().BuildPyHouseObj(p_root)
        self.m_pyhouse_obj._Families = familyApi(self.m_pyhouse_obj).m_family
        self.m_xml = SetupPyHouseObj().BuildXml(p_root)
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
        self.m_device_obj = self.createLightData()

    def test_01_Setup(self):
        """ Did we get everything set up for the rest of the tests of this class.
        """
        # print(PrettyFormatAny.form(VALID_FAMILIES, 'A1-01-A - Valid'))
        self.assertEqual(len(VALID_FAMILIES), len(self.m_pyhouse_obj._Families))
        self.assertEqual(VALID_FAMILIES[0], TESTING_FAMILY_NAME_0)  # Null
        self.assertEqual(VALID_FAMILIES[1], TESTING_FAMILY_NAME_1)  # Insteon
        self.assertEqual(VALID_FAMILIES[2], TESTING_FAMILY_NAME_2)  # UPB
        self.assertEqual(VALID_FAMILIES[3], TESTING_FAMILY_NAME_3)  # X-10
        self.assertEqual(VALID_FAMILIES[4], TESTING_FAMILY_NAME_4)  # Hue

    def test_02_Device(self):
        """ Did we get everything set up for the rest of the tests of this class.
        """
        # print(PrettyFormatAny.form(self.m_device_obj, 'A1-02-A - Device'))
        self.assertEqual(self.m_device_obj.Name, TESTING_LIGHT_NAME_0)
        self.assertEqual(self.m_device_obj.Key, TESTING_LIGHT_KEY_0)
        self.assertEqual(self.m_device_obj.Active, TESTING_LIGHT_ACTIVE_0)
        self.assertEqual(self.m_device_obj.Comment, TESTING_DEVICE_COMMENT_0)
        self.assertEqual(self.m_device_obj.BrightnessPct, TESTING_LIGHT_CUR_LEVEL_0)

    def test_02_Tags(self):
        """ Be sure that m_xml is set up properly
        """
        # print(PrettyFormatAny.form(self.m_xml, 'Xml'))
        self.assertEqual(self.m_xml.root.tag, TESTING_PYHOUSE)
        self.assertEqual(self.m_xml.computer_div.tag, 'ComputerDivision')
        self.assertEqual(self.m_xml.house_div.tag, 'HouseDivision')
        self.assertEqual(self.m_xml.lighting_sect.tag, 'LightingSection')
        self.assertEqual(self.m_xml.button_sect.tag, 'ButtonSection')
        self.assertEqual(self.m_xml.button.tag, 'Button')
        self.assertEqual(self.m_xml.controller_sect.tag, 'ControllerSection')
        self.assertEqual(self.m_xml.controller.tag, 'Controller')
        self.assertEqual(self.m_xml.light_sect.tag, 'LightSection')
        self.assertEqual(self.m_xml.light.tag, 'Light')


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
        print('A2-02-A - Parsed\n{}'.format(PrettyFormatAny.form(l_xml, 'A2-02-A - Parsed')))
        self.assertEqual(l_xml.tag, TESTING_LIGHT_SECTION)


class B1_Name(SetupMixin, unittest.TestCase):
    """ This section tests utility name retrieval.
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))
        self.m_device_obj = self.createLightData()

    def test_01_GetDeviceName0(self):
        """ Do we get back what we put in?
        """
        self.m_device_obj.Name = TESTING_FAMILY_NAME_0
        # print(PrettyFormatAny.form(self.m_device_obj, 'B1-01-A - Device'))
        l_name = family_utils._get_device_name(self.m_device_obj)
        # print(PrettyFormatAny.form(l_name, 'B1-01-B - Family'))
        self.assertEqual(l_name, TESTING_FAMILY_NAME_0)

    def test_02_GetDeviceName1(self):
        """ Do we get back what we put in?
        """
        self.m_device_obj.Name = TESTING_FAMILY_NAME_1
        # print(PrettyFormatAny.form(self.m_device_obj, 'B1-02-A - Device'))
        l_name = family_utils._get_device_name(self.m_device_obj)
        # print(PrettyFormatAny.form(l_name, 'B1-02-B - Family'))
        self.assertEqual(l_name, TESTING_FAMILY_NAME_1)

    def test_03_GetDeviceName2(self):
        """ Do we get back what we put in?
        """
        self.m_device_obj.Name = TESTING_FAMILY_NAME_2
        # print(PrettyFormatAny.form(self.m_device_obj, 'B1-03-A - Device'))
        l_name = family_utils._get_device_name(self.m_device_obj)
        # print(PrettyFormatAny.form(l_name, 'B1-03-B - Family'))
        self.assertEqual(l_name, TESTING_FAMILY_NAME_2)

    def test_04_GetDeviceName3(self):
        """ Do we get back what we put in?
        """
        self.m_device_obj.Name = TESTING_FAMILY_NAME_3
        # print(PrettyFormatAny.form(self.m_device_obj, 'B1-04-A - Device'))
        l_name = family_utils._get_device_name(self.m_device_obj)
        # print(PrettyFormatAny.form(l_name, 'B1-04-B - Family'))
        self.assertEqual(l_name, TESTING_FAMILY_NAME_3)

    def test_05_GetDeviceName4(self):
        """ Do we get back what we put in?
        """
        self.m_device_obj.Name = TESTING_FAMILY_NAME_4
        # print(PrettyFormatAny.form(self.m_device_obj, 'B1-05-A - Device'))
        l_name = family_utils._get_device_name(self.m_device_obj)
        # print(PrettyFormatAny.form(l_name, 'B1-05-B - Family'))
        self.assertEqual(l_name, TESTING_FAMILY_NAME_4)


class B2_Obj(SetupMixin, unittest.TestCase):
    """ This section tests family object retrieval
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))
        self.m_device_obj = self.createLightData()

    def test_01_GetFamilyObj0(self):
        """ Do we get the correct family object (Null)
        """
        self.m_device_obj.DeviceFamily = TESTING_FAMILY_NAME_0
        l_obj = FamUtil._get_family_obj(self.m_pyhouse_obj, self.m_device_obj)
        # print(PrettyFormatAny.form(l_obj, 'B2-01-A - Family object'))
        self.assertEqual(l_obj.Name, TESTING_FAMILY_NAME_0)
        self.assertEqual(l_obj.Active, True)
        self.assertEqual(l_obj.Key, 0)
        self.assertEqual(l_obj.FamilyDevice_ModuleName, 'Null_device')
        self.assertEqual(l_obj.FamilyPackageName, 'Modules.Families.Null')
        self.assertEqual(l_obj.FamilyXml_ModuleName, 'Null_xml')

    def test_02_GetFamilyObj1(self):
        """ Do we get the correct family object (Insteon)
        """
        self.m_device_obj.DeviceFamily = TESTING_FAMILY_NAME_1
        l_obj = FamUtil._get_family_obj(self.m_pyhouse_obj, self.m_device_obj)
        # print(PrettyFormatAny.form(l_obj, 'B2-02-A - Family'))
        self.assertEqual(l_obj.Name, TESTING_FAMILY_NAME_1)
        self.assertEqual(l_obj.Active, True)
        self.assertEqual(l_obj.Key, 1)
        self.assertEqual(l_obj.FamilyDevice_ModuleName, 'Insteon_device')
        self.assertEqual(l_obj.FamilyPackageName, 'Modules.Families.Insteon')
        self.assertEqual(l_obj.FamilyXml_ModuleName, 'Insteon_xml')

    def test_03_GetFamilyObj2(self):
        """ Do we get the correct family object (UPB)
        """
        self.m_device_obj.DeviceFamily = TESTING_FAMILY_NAME_2
        l_obj = FamUtil._get_family_obj(self.m_pyhouse_obj, self.m_device_obj)
        # print(PrettyFormatAny.form(l_obj, 'B2-03-A - Family'))
        self.assertEqual(l_obj.Name, TESTING_FAMILY_NAME_2)
        self.assertEqual(l_obj.Active, True)
        self.assertEqual(l_obj.Key, 2)
        self.assertEqual(l_obj.FamilyDevice_ModuleName, 'UPB_device')
        self.assertEqual(l_obj.FamilyPackageName, 'Modules.Families.UPB')
        self.assertEqual(l_obj.FamilyXml_ModuleName, 'UPB_xml')

    def test_04_GetFamilyObj3(self):
        """ Do we get the correct family object (X10)
        """
        self.m_device_obj.DeviceFamily = TESTING_FAMILY_NAME_3
        l_obj = FamUtil._get_family_obj(self.m_pyhouse_obj, self.m_device_obj)
        # print(PrettyFormatAny.form(l_obj, 'B2-04-A - Family'))
        self.assertEqual(l_obj.Name, TESTING_FAMILY_NAME_3)
        self.assertEqual(l_obj.Active, True)
        self.assertEqual(l_obj.Key, 3)
        self.assertEqual(l_obj.FamilyDevice_ModuleName, 'X10_device')
        self.assertEqual(l_obj.FamilyPackageName, 'Modules.Families.X10')
        self.assertEqual(l_obj.FamilyXml_ModuleName, 'X10_xml')

    def test_05_GetFamilyObj4(self):
        """ Do we get the correct family object (X10)
        """
        self.m_device_obj.DeviceFamily = TESTING_FAMILY_NAME_4
        l_obj = FamUtil._get_family_obj(self.m_pyhouse_obj, self.m_device_obj)
        # print(PrettyFormatAny.form(l_obj, 'B2-05-A - Family'))
        self.assertEqual(l_obj.Name, TESTING_FAMILY_NAME_4)
        self.assertEqual(l_obj.Active, True)
        self.assertEqual(l_obj.Key, 4)
        self.assertEqual(l_obj.FamilyDevice_ModuleName, 'Hue_device')
        self.assertEqual(l_obj.FamilyPackageName, 'Modules.Families.Hue')
        self.assertEqual(l_obj.FamilyXml_ModuleName, 'Hue_xml')


class B3_Family(SetupMixin, unittest.TestCase):
    """ This section tests family retrieval
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))
        self.m_device_obj = self.createLightData()

    def test_01_GetFamily(self):
        """ Did we get a family name string
        """
        self.m_device_obj.DeviceFamily = TESTING_FAMILY_NAME_1
        l_family = FamUtil.get_family(self.m_device_obj)
        # print(PrettyFormatAny.form(l_family, 'B3-01-A - Family'))
        self.assertEqual(l_family, TESTING_FAMILY_NAME_1)

    def test_02_GetFamily(self):
        """ Did we get a family name string
        """
        self.m_device_obj.DeviceFamily = TESTING_FAMILY_NAME_2
        l_family = FamUtil.get_family(self.m_device_obj)
        # print(PrettyFormatAny.form(l_family, 'B3-02-A - Family'))
        self.assertEqual(l_family, TESTING_FAMILY_NAME_2)


class B4_FamilyApi(SetupMixin, unittest.TestCase):
    """ This section tests family Api retrieval
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))
        self.m_device_obj = self.createLightData()

    def test_01_GetApi0(self):
        self.m_device_obj.DeviceFamily = TESTING_FAMILY_NAME_0
        l_api = FamUtil._get_family_device_api(self.m_pyhouse_obj, self.m_device_obj)
        print(PrettyFormatAny.form(l_api, 'B4-01-A - Api'))
        self.assertNotEqual(l_api, None)
        # Note: We need proper testing here

    def test_02_GetApi1(self):
        self.m_device_obj.DeviceFamily = TESTING_FAMILY_NAME_1
        l_api = FamUtil._get_family_device_api(self.m_pyhouse_obj, self.m_device_obj)
        print(PrettyFormatAny.form(l_api, 'B4-02-A - Api'))
        self.assertNotEqual(l_api, None)
        # Note: We need proper testing here

    def test_03_GetApi(self):
        self.m_device_obj.DeviceFamily = TESTING_FAMILY_NAME_2
        l_api = FamUtil._get_family_device_api(self.m_pyhouse_obj, self.m_device_obj)
        # print(PrettyFormatAny.form(l_api, 'B4-03-A - Api'))
        self.assertNotEqual(l_api, None)
        # Note: We need proper testing here

    def test_04_GetApi(self):
        self.m_device_obj.DeviceFamily = TESTING_FAMILY_NAME_3
        l_api = FamUtil._get_family_device_api(self.m_pyhouse_obj, self.m_device_obj)
        # print(PrettyFormatAny.form(l_api, 'B4-04-A - Api'))
        self.assertNotEqual(l_api, None)
        # Note: We need proper testing here

    def test_05_GetApi(self):
        self.m_device_obj.DeviceFamily = TESTING_FAMILY_NAME_4
        l_api = FamUtil._get_family_device_api(self.m_pyhouse_obj, self.m_device_obj)
        # print(PrettyFormatAny.form(l_api, 'B4-05-A - Api'))
        self.assertNotEqual(l_api, None)
        # Note: We need proper testing here


class C1_Read(SetupMixin, unittest.TestCase):
    """ This section tests the reading of XML used by the family.
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))
        # self.m_device_obj.DeviceFamily = TESTING_DEVICE_FAMILY_INSTEON
        # self.m_api = FamUtil._get_family_device_api(self.m_pyhouse_obj, self.m_device_obj)

    def test_01_Xml0(self):
        """ Did we get the XML correctly
        """
        l_xml = self.m_xml.light_sect[0]
        print(PrettyFormatAny.form(l_xml, 'C1-01-A - XML'))
        self.assertEqual(l_xml.attrib['Name'], TESTING_LIGHT_NAME_0)
        self.assertEqual(l_xml.find('DeviceFamily').text, TESTING_DEVICE_FAMILY_INSTEON)

    def test_02_Xml1(self):
        """ Did we get the XML correctly
        """
        l_xml = self.m_xml.light_sect[1]
        print(PrettyFormatAny.form(l_xml, 'C1-02-A - XML'))
        self.assertEqual(l_xml.attrib['Name'], TESTING_LIGHT_NAME_1)
        self.assertEqual(l_xml.find('DeviceFamily').text, TESTING_DEVICE_FAMILY_UPB)


class C2_Read_Dev(SetupMixin, unittest.TestCase):
    """ This section tests the reading of XML used by the family.
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))
        self.m_device_obj = self.createLightData()
        # self.m_device_obj.DeviceFamily = TESTING_DEVICE_FAMILY_INSTEON
        # self.m_api = FamUtil._get_family_device_api(self.m_pyhouse_obj, self.m_device_obj)

    def test_01_Device0(self):
        """ Did we get the Device correctly (Insteon)
        """
        self.m_device_obj.DeviceFamily = TESTING_FAMILY_NAME_1
        l_device = self.m_device_obj
        print(PrettyFormatAny.form(l_device, 'C2-01-A - Device'))
        self.assertEqual(l_device.Name, TESTING_LIGHT_NAME_0)
        self.assertEqual(l_device.Key, TESTING_LIGHT_KEY_0)
        self.assertEqual(l_device.Active, TESTING_LIGHT_ACTIVE_0)
        self.assertEqual(l_device.DeviceFamily, TESTING_DEVICE_FAMILY_INSTEON)
        self.assertEqual(str(l_device.DeviceType), TESTING_LIGHT_DEVICE_TYPE_0)
        self.assertEqual(str(l_device.DeviceSubType), TESTING_LIGHT_DEVICE_SUBTYPE_0)
        self.assertEqual(l_device.RoomName, TESTING_LIGHT_ROOM_NAME_0)

    def test_02_Device1(self):
        """ Did we get the Device correctly (UPB)
        """
        self.m_device_obj.DeviceFamily = TESTING_FAMILY_NAME_2
        self.m_api = FamUtil._get_family_device_api(self.m_pyhouse_obj, self.m_device_obj)
        print(PrettyFormatAny.form(self.m_device_obj, 'C2-02-A - Device'))
        self.assertEqual(self.m_device_obj.Name, TESTING_LIGHT_NAME_1)
        self.assertEqual(self.m_device_obj.Key, TESTING_LIGHT_KEY_1)
        self.assertEqual(self.m_device_obj.Active, TESTING_LIGHT_ACTIVE_1)
        self.assertEqual(self.m_device_obj.DeviceFamily, TESTING_DEVICE_FAMILY_UPB)
        self.assertEqual(str(self.m_device_obj.DeviceType), TESTING_LIGHT_DEVICE_TYPE_0)
        self.assertEqual(str(self.m_device_obj.DeviceSubType), TESTING_LIGHT_DEVICE_SUBTYPE_0)
        self.assertEqual(self.m_device_obj.RoomName, TESTING_LIGHT_ROOM_NAME_0)


class C3_Read(SetupMixin, unittest.TestCase):
    """ This section tests the reading of XML used by the family.
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))
        self.m_device_obj = self.createLightData()
        # self.m_device_obj.DeviceFamily = TESTING_DEVICE_FAMILY_INSTEON
        # self.m_api = FamUtil._get_family_device_api(self.m_pyhouse_obj, self.m_device_obj)

    def test_01_Family(self):
        """ Did we get everything set up for the rest of the tests of this class.
        """
        l_xml = self.m_xml.light_sect[0]
        print(PrettyFormatAny.form(l_xml, 'C3-01-A - XML'))
        l_device = self.m_device_obj
        l_light = FamUtil.read_family_data(self.m_pyhouse_obj, l_device, l_xml)
        print(PrettyFormatAny.form(l_light, 'C3-01-B - Light'))
        self.assertEqual(l_device.Name, TESTING_LIGHT_NAME_0)
        self.assertEqual(l_light.InsteonAddress, convert.dotted_hex2int(TESTING_INSTEON_ADDRESS_0))

    def test_02_Light(self):
        """ Did we get everything set up for the rest of the tests of this class.
        """
        l_xml = self.m_xml.light_sect[1]
        print(PrettyFormatAny.form(l_xml, 'C3-02-A - XML'))
        l_device = self.m_device_obj
        l_light = deviceXML.read_base_device_object_xml(l_device, l_xml)
        print(PrettyFormatAny.form(l_light, 'C3-02-B - Light'))
        self.assertEqual(l_light.Name, TESTING_LIGHT_NAME_1)
        self.assertEqual(l_device.RoomName, TESTING_LIGHT_ROOM_NAME_1)
        self.assertEqual(l_light.UPBAddress, convert.dotted_hex2int(TESTING_INSTEON_ADDRESS_0))

    def test_03_All(self):
        """ Did we get everything set up for the rest of the tests of this class.
        """
        l_xml = self.m_xml.light
        l_device = self.m_device_obj
        #
        l_light = deviceXML.read_base_device_object_xml(l_device, l_xml)
        FamUtil.read_family_data(self.m_pyhouse_obj, l_light, l_xml)
        # print(PrettyFormatAny.form(l_light, 'C3-03-A - Light'))
        self.assertEqual(l_light.Name, TESTING_LIGHT_NAME_0)
        self.assertEqual(l_light.DeviceFamily, TESTING_DEVICE_FAMILY_INSTEON)
        self.assertEqual(l_light.InsteonAddress, convert.dotted_hex2int(TESTING_INSTEON_ADDRESS_0))
        self.assertEqual(convert.int2dotted_hex(l_light.ProductKey, 3), TESTING_INSTEON_PRODUCT_KEY_0)


class C4_Read(SetupMixin, unittest.TestCase):
    """ This section tests the reading and writing of XML used by UPB.
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))
        self.m_device_obj = self.createLightData()
        self.m_device_obj.DeviceFamily = TESTING_DEVICE_FAMILY_UPB
        self.m_api = FamUtil._get_family_device_api(self.m_pyhouse_obj, self.m_device_obj)

    def test_01_Xml(self):
        """ Did we get the XML correctly
        """
        l_xml = self.m_xml.light_sect[1]
        # print(PrettyFormatAny.form(l_xml, 'C4-01-A - XML'))
        self.assertEqual(l_xml.attrib['Name'], TESTING_LIGHT_NAME_1)
        self.assertEqual(l_xml.find('DeviceFamily').text, TESTING_DEVICE_FAMILY_UPB)

    def test_02_Device(self):
        """ Did we get the Device correctly
        """
        self.m_device_obj.DeviceFamily = TESTING_FAMILY_NAME_1
        l_device = self.m_device_obj
        # print(PrettyFormatAny.form(l_device, 'C4-02-A - Device'))
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
        # print(PrettyFormatAny.form(l_light, 'C4-03-A - Light'))
        self.assertEqual(str(l_light.UPBAddress), TESTING_UPB_ADDRESS)

    def test_04_Light(self):
        """ Did we get everything set up for the rest of the tests of this class.
        """
        l_xml = self.m_xml.light
        l_device = self.m_device_obj
        l_light = deviceXML.read_base_device_object_xml(l_device, l_xml)
        # print(PrettyFormatAny.form(l_light, 'C4-04-A - Light'))
        self.assertEqual(l_light.Name, TESTING_LIGHT_NAME_0)
        self.assertEqual(l_device.RoomName, TESTING_LIGHT_ROOM_NAME_0)

    def test_05_All(self):
        """ Did we get everything set up for the rest of the tests of this class.
        """
        l_xml = self.m_xml.light
        l_device = self.m_device_obj
        #
        l_light = deviceXML.read_base_device_object_xml(l_device, l_xml)
        FamUtil.read_family_data(self.m_pyhouse_obj, l_light, l_xml)
        # print(PrettyFormatAny.form(l_light, 'C4-05-A - Light'))
        self.assertEqual(l_light.Name, TESTING_LIGHT_NAME_0)
        self.assertEqual(l_light.DeviceFamily, TESTING_DEVICE_FAMILY_INSTEON)
        self.assertEqual(l_light.InsteonAddress, convert.dotted_hex2int(TESTING_INSTEON_ADDRESS_0))
        self.assertEqual(convert.int2dotted_hex(l_light.ProductKey, 3), TESTING_INSTEON_PRODUCT_KEY_0)

# ## END DBK
