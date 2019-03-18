"""
@name:      PyHouse/Project/src/Modules/Housing/Lighting/test/test_lighting_xml.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2019-2019 by D. Brian Kimmel
@license:   MIT License
@note:      Created on Jan 21, 2019
@summary:   Test

Passed all 21 tests - DBK - 2019-01-21

"""

__updated__ = '2019-03-18'

#  Import system type stuff
import xml.etree.ElementTree as ET
from twisted.trial import unittest

#  Import PyMh files and modules.
from test.xml_data import XML_LONG, TESTING_PYHOUSE
from test.testing_mixin import SetupPyHouseObj
from Modules.Core.data_objects import ButtonData
from Modules.Housing.Lighting.lighting_lights import LightData, XML as lightsXML
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
    TESTING_LIGHTING_SECTION, \
    XML_LIGHTING
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
from Modules.Housing.Lighting.test.xml_buttons import \
    TESTING_LIGHTING_BUTTON_NAME_0, \
    TESTING_LIGHTING_BUTTON_KEY_0, \
    TESTING_LIGHTING_BUTTON_ACTIVE_0, \
    TESTING_LIGHTING_BUTTON_UUID_0, \
    TESTING_LIGHTING_BUTTON_NAME_1, \
    TESTING_LIGHTING_BUTTON_KEY_1, \
    TESTING_LIGHTING_BUTTON_ACTIVE_1, \
    TESTING_LIGHTING_BUTTON_UUID_1, \
    XML_BUTTON_SECTION, \
    L_BUTTON_SECTION_START, \
    TESTING_BUTTON_SECTION
from Modules.Housing.Lighting.test.xml_controllers import \
    XML_CONTROLLER_SECTION, \
    L_CONTROLLER_SECTION_START, \
    TESTING_CONTROLLER_SECTION
from Modules.Core.Utilities.debug_tools import PrettyFormatAny


class SetupMixin(object):
    """
    """

    def setUp(self, p_root):
        self.m_pyhouse_obj = SetupPyHouseObj().BuildPyHouseObj(p_root)
        self.m_xml = SetupPyHouseObj().BuildXml(p_root)
        self.m_family = familyAPI(self.m_pyhouse_obj).LoadFamilyTesting()
        self.m_pyhouse_obj.FamilyInformation = self.m_family


class A0(unittest.TestCase):

    def setUp(self):
        pass

    def test_00_Print(self):
        print('Id: test_lighting_xml')


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
        l_raw = XML_BUTTON_SECTION
        # print('A2-01-A - Raw\n{}'.format(l_raw))
        self.assertEqual(l_raw[:15], L_BUTTON_SECTION_START)

    def test_02_Raw(self):
        l_raw = XML_CONTROLLER_SECTION
        # print('A2-02-A - Raw\n{}'.format(l_raw))
        self.assertEqual(l_raw[:19], L_CONTROLLER_SECTION_START)

    def test_03_Raw(self):
        l_raw = XML_LIGHT_SECTION
        # print('A2-03-A - Raw\n{}'.format(l_raw))
        self.assertEqual(l_raw[:14], L_LIGHT_SECTION_START)

    def test_11_Parsed(self):
        l_xml = ET.fromstring(XML_BUTTON_SECTION)
        # print('A2-11-A - Parsed\n{}'.format(PrettyFormatAny.form(l_xml, 'Parsed')))
        self.assertEqual(l_xml.tag, TESTING_BUTTON_SECTION)

    def test_12_Parsed(self):
        l_xml = ET.fromstring(XML_CONTROLLER_SECTION)
        # print('A2-12-A - Parsed\n{}'.format(PrettyFormatAny.form(l_xml, 'Parsed')))
        self.assertEqual(l_xml.tag, TESTING_CONTROLLER_SECTION)

    def test_13_Parsed(self):
        l_xml = ET.fromstring(XML_LIGHT_SECTION)
        # print('A2-13-A - Parsed\n{}'.format(PrettyFormatAny.form(l_xml, 'Parsed')))
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


class B1_ReadButton(SetupMixin, unittest.TestCase):
    """
    This section tests the reading and writing of XML used by lighting_lights.
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))
        self.m_xml_but = self.m_xml.button_sect[0]
        self.m_obj = ButtonData()

    def test_01_Base0(self):
        """ Read the Base info - the device information
        """
        l_xml = self.m_xml.button_sect[0]
        # print(PrettyFormatAny.form(l_xml, 'B1-01-A  Base'))
        l_obj = LightingXML()._read_base_device(self.m_obj, l_xml)
        # print(PrettyFormatAny.form(l_obj, 'B1-1-B - Base'))
        self.assertEqual(l_obj.Name, TESTING_LIGHTING_BUTTON_NAME_0)
        self.assertEqual(str(l_obj.Key), TESTING_LIGHTING_BUTTON_KEY_0)
        self.assertEqual(str(l_obj.Active), TESTING_LIGHTING_BUTTON_ACTIVE_0)
        self.assertEqual(l_obj.UUID, TESTING_LIGHTING_BUTTON_UUID_0)

    def test_02_Base1(self):
        """ Read the Base info - the device information
        """
        l_xml = self.m_xml.button_sect[1]
        # print(PrettyFormatAny.form(l_xml, 'B1-02-A  Base'))
        l_obj = LightingXML()._read_base_device(self.m_obj, l_xml)
        # print(PrettyFormatAny.form(l_obj, 'B1-02-B - Base'))
        self.assertEqual(l_obj.Name, TESTING_LIGHTING_BUTTON_NAME_1)
        self.assertEqual(str(l_obj.Key), TESTING_LIGHTING_BUTTON_KEY_1)
        self.assertEqual(str(l_obj.Active), TESTING_LIGHTING_BUTTON_ACTIVE_1)
        self.assertEqual(l_obj.UUID, TESTING_LIGHTING_BUTTON_UUID_1)


class B2_ReadController(SetupMixin, unittest.TestCase):
    """
    This section tests the reading and writing of XML used by lighting_lights.
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))

    def test_01_Base0(self):
        """ Read the Base info - the device information
        """
        l_xml = self.m_xml.light_sect[0]
        l_obj = LightData()
        # print(PrettyFormatAny.form(l_xml, 'B1-01-A  Base'))
        l_obj = LightingXML()._read_base_device(l_obj, l_xml)
        # print(PrettyFormatAny.form(l_obj, 'B1-1-B - Base'))
        self.assertEqual(l_obj.Name, TESTING_LIGHT_NAME_0)
        self.assertEqual(str(l_obj.Key), TESTING_LIGHT_KEY_0)
        self.assertEqual(str(l_obj.Active), TESTING_LIGHT_ACTIVE_0)
        self.assertEqual(l_obj.UUID, TESTING_LIGHT_UUID_0)

    def test_02_Base1(self):
        """ Read the Base info - the device information
        """
        l_xml = self.m_xml.light_sect[1]
        l_obj = LightData()
        # print(PrettyFormatAny.form(l_xml, 'B1-02-A  Base'))
        l_obj = LightingXML()._read_base_device(l_obj, l_xml)
        # print(PrettyFormatAny.form(l_obj, 'B1-02-B - Base'))
        self.assertEqual(l_obj.Name, TESTING_LIGHT_NAME_1)
        self.assertEqual(str(l_obj.Key), TESTING_LIGHT_KEY_1)
        self.assertEqual(str(l_obj.Active), TESTING_LIGHT_ACTIVE_1)
        self.assertEqual(l_obj.UUID, TESTING_LIGHT_UUID_1)


class B3_ReadLight(SetupMixin, unittest.TestCase):
    """
    This section tests the reading and writing of XML used by lighting_lights.
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))

    def test_01_Base0(self):
        """ Read the Base info - the device information
        """
        l_xml = self.m_xml.light_sect[0]
        l_obj = LightData()
        # print(PrettyFormatAny.form(l_xml, 'B3-01-A  Base'))
        l_obj = LightingXML()._read_base_device(l_obj, l_xml)
        # print(PrettyFormatAny.form(l_obj, 'B3-1-B - Base'))
        self.assertEqual(l_obj.Name, TESTING_LIGHT_NAME_0)
        self.assertEqual(str(l_obj.Key), TESTING_LIGHT_KEY_0)
        self.assertEqual(str(l_obj.Active), TESTING_LIGHT_ACTIVE_0)
        self.assertEqual(l_obj.UUID, TESTING_LIGHT_UUID_0)

    def test_02_Base1(self):
        """ Read the Base info - the device information
        """
        l_xml = self.m_xml.light_sect[1]
        l_obj = LightData()
        # print(PrettyFormatAny.form(l_xml, 'B3-02-A  Base'))
        l_obj = LightingXML()._read_base_device(l_obj, l_xml)
        # print(PrettyFormatAny.form(l_obj, 'B3-02-B - Base'))
        self.assertEqual(l_obj.Name, TESTING_LIGHT_NAME_1)
        self.assertEqual(str(l_obj.Key), TESTING_LIGHT_KEY_1)
        self.assertEqual(str(l_obj.Active), TESTING_LIGHT_ACTIVE_1)
        self.assertEqual(l_obj.UUID, TESTING_LIGHT_UUID_1)


class C1_Write(SetupMixin, unittest.TestCase):
    """
    This section tests the reading and writing of XML used by lighting_lights.
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))
        self.m_obj = LightData()
        self.m_lights = lightsXML().read_all_lights_xml(self.m_pyhouse_obj)

    def test_01_Base0(self):
        """Test the write for proper XML Base elements
        """
        l_xml = LightingXML()._write_base_device('Light', self.m_lights[0])
        # print(PrettyFormatAny.form(l_xml, 'C1-01-A - ML'))
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
        l_xml = LightingXML()._write_base_device('Light', self.m_lights[1])
        # print(PrettyFormatAny.form(l_xml, 'C1-02-A - ML'))
        self.assertEqual(l_xml.attrib['Name'], TESTING_LIGHT_NAME_1)
        self.assertEqual(l_xml.attrib['Key'], TESTING_LIGHT_KEY_1)
        self.assertEqual(l_xml.attrib['Active'], TESTING_LIGHT_ACTIVE_1)
        self.assertEqual(l_xml.find('UUID').text, TESTING_LIGHT_UUID_1)
        self.assertEqual(l_xml.find('Comment').text, TESTING_LIGHT_COMMENT_1)
        self.assertEqual(l_xml.find('DeviceFamily').text, TESTING_DEVICE_FAMILY_UPB)
        self.assertEqual(l_xml.find('RoomName').text, TESTING_LIGHT_ROOM_NAME_1)
        self.assertEqual(l_xml.find('RoomUUID').text, TESTING_LIGHT_ROOM_UUID_1)


class C2_Write(SetupMixin, unittest.TestCase):
    """
    This section tests the reading and writing of XML used by lighting_lights.
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))
        self.m_obj = LightData()
        self.m_lights = lightsXML().read_all_lights_xml(self.m_pyhouse_obj)

    def test_01_Base0(self):
        """Test the write for proper XML Base elements
        """
        l_xml = LightingXML()._write_base_device('Light', self.m_lights[0])
        # print(PrettyFormatAny.form(l_xml, '22-01-A - ML'))
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
        l_xml = LightingXML()._write_base_device('Light', self.m_lights[1])
        # print(PrettyFormatAny.form(l_xml, 'B2-02-A - ML'))
        self.assertEqual(l_xml.attrib['Name'], TESTING_LIGHT_NAME_1)
        self.assertEqual(l_xml.attrib['Key'], TESTING_LIGHT_KEY_1)
        self.assertEqual(l_xml.attrib['Active'], TESTING_LIGHT_ACTIVE_1)
        self.assertEqual(l_xml.find('UUID').text, TESTING_LIGHT_UUID_1)
        self.assertEqual(l_xml.find('Comment').text, TESTING_LIGHT_COMMENT_1)
        self.assertEqual(l_xml.find('DeviceFamily').text, TESTING_DEVICE_FAMILY_UPB)
        self.assertEqual(l_xml.find('RoomName').text, TESTING_LIGHT_ROOM_NAME_1)
        self.assertEqual(l_xml.find('RoomUUID').text, TESTING_LIGHT_ROOM_UUID_1)


class C3_Write(SetupMixin, unittest.TestCase):
    """
    This section tests the reading and writing of XML used by lighting_lights.
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))
        self.m_obj = LightData()
        self.m_lights = lightsXML().read_all_lights_xml(self.m_pyhouse_obj)

    def test_01_Base0(self):
        """Test the write for proper XML Base elements
        """
        l_xml = LightingXML()._write_base_device('Light', self.m_lights[0])
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
        l_xml = LightingXML()._write_base_device('Light', self.m_lights[1])
        # print(PrettyFormatAny.form(l_xml, 'B2-02-A - ML'))
        self.assertEqual(l_xml.attrib['Name'], TESTING_LIGHT_NAME_1)
        self.assertEqual(l_xml.attrib['Key'], TESTING_LIGHT_KEY_1)
        self.assertEqual(l_xml.attrib['Active'], TESTING_LIGHT_ACTIVE_1)
        self.assertEqual(l_xml.find('UUID').text, TESTING_LIGHT_UUID_1)
        self.assertEqual(l_xml.find('Comment').text, TESTING_LIGHT_COMMENT_1)
        self.assertEqual(l_xml.find('DeviceFamily').text, TESTING_DEVICE_FAMILY_UPB)
        self.assertEqual(l_xml.find('RoomName').text, TESTING_LIGHT_ROOM_NAME_1)
        self.assertEqual(l_xml.find('RoomUUID').text, TESTING_LIGHT_ROOM_UUID_1)


class C1_WriteButton(SetupMixin, unittest.TestCase):
    """
    This section tests the reading and writing of XML used by lighting_lights.
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))
        self.m_obj = LightData()
        self.m_lights = lightsXML().read_all_lights_xml(self.m_pyhouse_obj)

    def test_01_Base0(self):
        """Test the write for proper XML Base elements
        """
        l_xml = LightingXML()._write_base_device('Light', self.m_lights[0])
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
        l_xml = LightingXML()._write_base_device('Light', self.m_lights[1])
        # print(PrettyFormatAny.form(l_xml, 'B2-02-A - ML'))
        self.assertEqual(l_xml.attrib['Name'], TESTING_LIGHT_NAME_1)
        self.assertEqual(l_xml.attrib['Key'], TESTING_LIGHT_KEY_1)
        self.assertEqual(l_xml.attrib['Active'], TESTING_LIGHT_ACTIVE_1)
        self.assertEqual(l_xml.find('UUID').text, TESTING_LIGHT_UUID_1)
        self.assertEqual(l_xml.find('Comment').text, TESTING_LIGHT_COMMENT_1)
        self.assertEqual(l_xml.find('DeviceFamily').text, TESTING_DEVICE_FAMILY_UPB)
        self.assertEqual(l_xml.find('RoomName').text, TESTING_LIGHT_ROOM_NAME_1)
        self.assertEqual(l_xml.find('RoomUUID').text, TESTING_LIGHT_ROOM_UUID_1)


class C2_WriteController(SetupMixin, unittest.TestCase):
    """
    This section tests the reading and writing of XML used by lighting_lights.
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))
        self.m_obj = LightData()
        self.m_lights = lightsXML().read_all_lights_xml(self.m_pyhouse_obj)

    def test_01_Base0(self):
        """Test the write for proper XML Base elements
        """
        l_xml = LightingXML()._write_base_device('Light', self.m_lights[0])
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
        l_xml = LightingXML()._write_base_device('Light', self.m_lights[1])
        # print(PrettyFormatAny.form(l_xml, 'B2-02-A - ML'))
        self.assertEqual(l_xml.attrib['Name'], TESTING_LIGHT_NAME_1)
        self.assertEqual(l_xml.attrib['Key'], TESTING_LIGHT_KEY_1)
        self.assertEqual(l_xml.attrib['Active'], TESTING_LIGHT_ACTIVE_1)
        self.assertEqual(l_xml.find('UUID').text, TESTING_LIGHT_UUID_1)
        self.assertEqual(l_xml.find('Comment').text, TESTING_LIGHT_COMMENT_1)
        self.assertEqual(l_xml.find('DeviceFamily').text, TESTING_DEVICE_FAMILY_UPB)
        self.assertEqual(l_xml.find('RoomName').text, TESTING_LIGHT_ROOM_NAME_1)
        self.assertEqual(l_xml.find('RoomUUID').text, TESTING_LIGHT_ROOM_UUID_1)


class C3_WriteLight(SetupMixin, unittest.TestCase):
    """
    This section tests the reading and writing of XML used by lighting_lights.
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))
        self.m_obj = LightData()
        self.m_lights = lightsXML().read_all_lights_xml(self.m_pyhouse_obj)

    def test_01_Base0(self):
        """Test the write for proper XML Base elements
        """
        l_xml = LightingXML()._write_base_device('Light', self.m_lights[0])
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
        l_xml = LightingXML()._write_base_device('Light', self.m_lights[1])
        # print(PrettyFormatAny.form(l_xml, 'B2-02-A - ML'))
        self.assertEqual(l_xml.attrib['Name'], TESTING_LIGHT_NAME_1)
        self.assertEqual(l_xml.attrib['Key'], TESTING_LIGHT_KEY_1)
        self.assertEqual(l_xml.attrib['Active'], TESTING_LIGHT_ACTIVE_1)
        self.assertEqual(l_xml.find('UUID').text, TESTING_LIGHT_UUID_1)
        self.assertEqual(l_xml.find('Comment').text, TESTING_LIGHT_COMMENT_1)
        self.assertEqual(l_xml.find('DeviceFamily').text, TESTING_DEVICE_FAMILY_UPB)
        self.assertEqual(l_xml.find('RoomName').text, TESTING_LIGHT_ROOM_NAME_1)
        self.assertEqual(l_xml.find('RoomUUID').text, TESTING_LIGHT_ROOM_UUID_1)

# ## END DBK
