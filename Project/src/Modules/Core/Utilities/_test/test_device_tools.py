"""
@name:      PyHouse/src/Modules.Core.Utilities.test/test_device_tools.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2015-2018 by D. Brian Kimmel
@license:   MIT License
@note:      Created on Jun 26, 2015
@Summary:

Passed all 11 tests - DBK - 2018-02-12

"""

__updated__ = '2019-07-09'

# Import system type stuff
from twisted.trial import unittest
from xml.etree import ElementTree as ET

# Import PyMh files and modules.
from test.xml_data import XML_LONG, TESTING_PYHOUSE
from test.testing_mixin import SetupPyHouseObj
from Modules.Core.data_objects import LightData, ButtonData, ControllerInformation
from Modules.Core.test.xml_device import \
    TESTING_DEVICE_FAMILY_INSTEON, \
    TESTING_DEVICE_ROOM_NAME, \
    TESTING_DEVICE_ROOM_X, \
    TESTING_DEVICE_COMMENT_0, \
    TESTING_DEVICE_SUBTYPE, \
    TESTING_DEVICE_TYPE, \
    TESTING_DEVICE_ROOM_UUID
from Modules.Housing.Lighting.test.xml_lights import \
    TESTING_LIGHT_NAME_0, \
    TESTING_LIGHT_KEY_0, \
    TESTING_LIGHT_ACTIVE_0, \
    TESTING_LIGHT_UUID_0, \
    TESTING_LIGHT_COMMENT_0, \
    TESTING_LIGHT_DEVICE_SUBTYPE_0, \
    TESTING_LIGHT_DEVICE_TYPE_0, \
    TESTING_LIGHT_ROOM_COORDS_0, \
    TESTING_LIGHT_ROOM_NAME_0, \
    TESTING_LIGHT_ROOM_UUID_0, \
    TESTING_LIGHT_ROOM_X0, \
    TESTING_LIGHT_ROOM_Z0, \
    TESTING_LIGHT_ROOM_Y0
from Modules.Housing.Lighting.test.xml_controllers import \
    TESTING_CONTROLLER_NAME_0, \
    TESTING_CONTROLLER_ACTIVE_0, \
    TESTING_CONTROLLER_KEY_0, \
    TESTING_CONTROLLER_UUID_0
from Modules.Housing.Lighting.test.xml_buttons import \
    TESTING_LIGHTING_BUTTON_NAME_0, \
    TESTING_LIGHTING_BUTTON_COMMENT_0
from Modules.Core.Utilities.device_tools import XML as deviceXML
from Modules.Core.Utilities.debug_tools import PrettyFormatAny


class SetupMixin(object):
    """
    """

    def setUp(self, p_root):
        self.m_pyhouse_obj = SetupPyHouseObj().BuildPyHouseObj(p_root)
        self.m_xml = SetupPyHouseObj().BuildXml(p_root)
        self.m_api = deviceXML
        self.m_button_obj = ButtonData()
        self.m_controller_obj = ControllerInformation()
        self.m_light_obj = LightData()


class A0(unittest.TestCase):

    def setUp(self):
        pass

    def test_00_Print(self):
        print('Id: test_device_tools')


class A1_Setup(SetupMixin, unittest.TestCase):
    """ This section tests the reading and writing of XML used by node_local.
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))

    def test_01_Find(self):
        """ Be sure that the XML contains the right stuff.
        """
        # print(PrettyFormatAny.form(self.m_xml, 'A1-01-A - Tags'))
        self.assertEqual(self.m_xml.root.tag, TESTING_PYHOUSE)
        self.assertEqual(self.m_xml.house_div.tag, 'HouseDivision')
        self.assertEqual(self.m_xml.light_sect.tag, 'LightSection')
        self.assertEqual(self.m_xml.light.tag, 'Light')
        self.assertEqual(self.m_xml.controller_sect.tag, 'ControllerSection')
        self.assertEqual(self.m_xml.controller.tag, 'Controller')
        self.assertEqual(self.m_xml.button_sect.tag, 'ButtonSection')
        self.assertEqual(self.m_xml.button.tag, 'Button')

    def test_02_XML(self):
        """ Be sure that the XML contains the right stuff.
        """
        # print(PrettyFormatAny.form(self.m_xml.light, 'A1-02-A - Base'))
        pass


class A2_XML(SetupMixin, unittest.TestCase):
    """ This section tests the reading and writing of XML used by node_local.
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))

    def test_01_Light(self):
        """ Be sure that the XML contains the right stuff.
        """
        # print(PrettyFormatAny.form(self.m_xml.light, 'A2-01-A - Light'))
        pass


class B1_Read(SetupMixin, unittest.TestCase):
    """ This section tests the reading and writing of XML used by node_local.
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))

    def test_01_BaseLight(self):
        """ Read in the xml file and fill in the device info
        """
        l_obj = LightData()
        l_base = self.m_api.read_base_device_object_xml(l_obj, self.m_xml.light)
        # print(PrettyFormatAny.form(l_base, 'B1-01-A - Base'))
        # print(PrettyFormatAny.form(l_base.RoomCoords, 'B1-01-B - Base Coords'))
        self.assertEqual(l_base.Name, TESTING_LIGHT_NAME_0)
        self.assertEqual(l_base.Key, int(TESTING_LIGHT_KEY_0))
        self.assertEqual(l_base.Active, bool(TESTING_LIGHT_ACTIVE_0))
        self.assertEqual(l_base.UUID, TESTING_LIGHT_UUID_0)
        self.assertEqual(l_base.Comment, TESTING_LIGHT_COMMENT_0)
        self.assertEqual(l_base.DeviceFamily, TESTING_DEVICE_FAMILY_INSTEON)
        self.assertEqual(l_base.DeviceSubType, int(TESTING_LIGHT_DEVICE_SUBTYPE_0))
        self.assertEqual(l_base.DeviceType, int(TESTING_LIGHT_DEVICE_TYPE_0))
        self.assertEqual(str(l_base.RoomCoords.X_Easting), TESTING_LIGHT_ROOM_X0)
        self.assertEqual(str(l_base.RoomCoords.Y_Northing), TESTING_LIGHT_ROOM_Y0)
        self.assertEqual(str(l_base.RoomCoords.Z_Height), TESTING_LIGHT_ROOM_Z0)
        self.assertEqual(l_base.RoomName, TESTING_LIGHT_ROOM_NAME_0)
        self.assertEqual(l_base.RoomUUID, TESTING_LIGHT_ROOM_UUID_0)

    def test_02_BaseController(self):
        """ Read in the xml file and fill in the lights
        """
        l_obj = ControllerInformation()
        l_base = self.m_api.read_base_device_object_xml(l_obj, self.m_xml.controller)
        self.assertEqual(str(l_base.Name), TESTING_CONTROLLER_NAME_0)
        self.assertEqual(str(l_base.Key), TESTING_CONTROLLER_KEY_0)
        self.assertEqual(str(l_base.Active), TESTING_CONTROLLER_ACTIVE_0)
        self.assertEqual(l_base.Comment, TESTING_DEVICE_COMMENT_0)
        self.assertEqual(l_base.RoomCoords.X_Easting, float(TESTING_DEVICE_ROOM_X))
        self.assertEqual(l_base.DeviceFamily, TESTING_DEVICE_FAMILY_INSTEON)
        self.assertEqual(l_base.RoomName, TESTING_DEVICE_ROOM_NAME)

    def test_03_ReadBaseButton(self):
        """ Read in the xml file and fill in the lights
        """
        l_obj = ButtonData()
        l_base = self.m_api.read_base_device_object_xml(l_obj, self.m_xml.button)
        self.assertEqual(l_base.Name, TESTING_LIGHTING_BUTTON_NAME_0)
        self.assertEqual(l_base.Key, 0)
        self.assertEqual(l_base.Active, True)
        self.assertEqual(l_base.Comment, TESTING_LIGHTING_BUTTON_COMMENT_0)
        self.assertEqual(l_base.RoomCoords.X_Easting, float(TESTING_DEVICE_ROOM_X))
        self.assertEqual(l_base.DeviceFamily, TESTING_DEVICE_FAMILY_INSTEON)
        self.assertEqual(l_base.RoomName, TESTING_DEVICE_ROOM_NAME)


class C1_Write(SetupMixin, unittest.TestCase):
    """ This section tests the reading and writing of XML used by node_local.
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))

    def test_01_BaseLight(self):
        """ Read in the xml file and fill in the lights
        """
        l_obj = LightData()
        l_base = self.m_api.read_base_device_object_xml(l_obj, self.m_xml.light)
        l_xml = self.m_api.write_base_device_object_xml('Light', l_base)
        # print(PrettyFormatAny.form(l_xml, 'C1-01-A - Base'))
        self.assertEqual(l_xml.attrib['Name'], TESTING_LIGHT_NAME_0)
        self.assertEqual(l_xml.attrib['Key'], TESTING_LIGHT_KEY_0)
        self.assertEqual(l_xml.attrib['Active'], TESTING_LIGHT_ACTIVE_0)
        self.assertEqual(l_xml.find('UUID').text, TESTING_LIGHT_UUID_0)
        self.assertEqual(l_xml.find('Comment').text, TESTING_LIGHT_COMMENT_0)
        self.assertEqual(l_xml.find('DeviceSubType').text, TESTING_LIGHT_DEVICE_SUBTYPE_0)
        self.assertEqual(l_xml.find('DeviceType').text, TESTING_LIGHT_DEVICE_TYPE_0)
        self.assertEqual(l_xml.find('RoomCoords').text, TESTING_LIGHT_ROOM_COORDS_0)
        self.assertEqual(l_xml.find('RoomName').text, TESTING_LIGHT_ROOM_NAME_0)
        self.assertEqual(l_xml.find('RoomUUID').text, TESTING_LIGHT_ROOM_UUID_0)

    def test_02_BaseController(self):
        """ Read in the xml file and fill in the lights
        """
        l_obj = ControllerInformation()
        l_base = self.m_api.read_base_device_object_xml(l_obj, self.m_xml.controller)
        l_xml = self.m_api.write_base_device_object_xml('Light', l_base)
        # print(PrettyFormatAny.form(l_xml, 'C1-02-A - Base'))
        self.assertEqual(l_xml.attrib['Name'], TESTING_CONTROLLER_NAME_0)
        self.assertEqual(l_xml.attrib['Key'], TESTING_CONTROLLER_KEY_0)
        self.assertEqual(l_xml.attrib['Active'], TESTING_CONTROLLER_ACTIVE_0)
        self.assertEqual(l_xml.find('UUID').text, TESTING_CONTROLLER_UUID_0)
        self.assertEqual(l_xml.find('Comment').text, TESTING_DEVICE_COMMENT_0)
        self.assertEqual(l_xml.find('DeviceSubType').text, TESTING_DEVICE_SUBTYPE)
        self.assertEqual(l_xml.find('DeviceType').text, TESTING_DEVICE_TYPE)
        # self.assertEqual(l_xml.find('RoomCoords').text, TESTING_LIGHT_ROOM_COORDS_0)
        self.assertEqual(l_xml.find('RoomName').text, TESTING_DEVICE_ROOM_NAME)
        self.assertEqual(l_xml.find('RoomUUID').text, TESTING_DEVICE_ROOM_UUID)

    def test_03_BaseButton(self):
        """ Read in the xml file and fill in the lights
        """
        l_obj = ButtonData()
        l_base = self.m_api.read_base_device_object_xml(l_obj, self.m_xml.button)
        l_xml = self.m_api.write_base_device_object_xml('Light', l_base)
        # print(PrettyFormatAny.form(l_xml, 'C1-03-A - Base'))
        self.assertEqual(l_xml.attrib['Name'], TESTING_LIGHTING_BUTTON_NAME_0)
        self.assertEqual(l_xml.attrib['Key'], '0')
        self.assertEqual(l_xml.attrib['Active'], 'True')


class C2_EmptyXML(SetupMixin, unittest.TestCase):
    """ This section tests the reading and writing of XML before anything has been defined.
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))

    def test_01_FindXml(self):
        """ Be sure that the XML contains the right stuff.
        """

# ## END DBK
