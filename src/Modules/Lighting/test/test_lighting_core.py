"""
@name:      PyHouse/src/Modules/lights/test/test_lighting_core.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2014-2015 by D. Brian Kimmel
@license:   MIT License
@note:      Created on May 4, 2014
@summary:   This module is for testing lighting Core.

Despite its name as "Lighting" this module is also capable of reading and writing
other devices such as thermostats, irrigation systems and pool systems to name a few.

Notice that devices have a lot of configuration entries is XML.  This module only deals with
the "Core" definitions.

All 17 tests working - DBK 2015-08-17
"""

#  Import system type stuff
import xml.etree.ElementTree as ET
from twisted.trial import unittest

#  Import PyMh files and modules.
from Modules.Core.data_objects import LightData, ButtonData, ControllerData
from Modules.Core.test.xml_device import TESTING_DEVICE_COMMENT, \
    TESTING_DEVICE_FAMILY_INSTEON, \
    TESTING_DEVICE_ROOM_X, \
    TESTING_DEVICE_ROOM_Y, \
    TESTING_DEVICE_ROOM_Z, \
    TESTING_DEVICE_UUID, \
    TESTING_DEVICE_TYPE, \
    TESTING_DEVICE_SUBTYPE, \
    TESTING_DEVICE_ROOM_NAME
from Modules.Lighting.lighting_core import API as LightingCoreAPI
from test.testing_mixin import SetupPyHouseObj
from test.xml_data import XML_LONG
#  from Modules.Utilities.debug_tools import PrettyFormatAny


class SetupMixin(object):
    """
    """

    def setUp(self, p_root):
        self.m_pyhouse_obj = SetupPyHouseObj().BuildPyHouseObj(p_root)
        self.m_xml = SetupPyHouseObj().BuildXml(p_root)
        self.m_button_obj = ButtonData()
        self.m_controller_obj = ControllerData()
        self.m_light_obj = LightData()
        self.m_api = LightingCoreAPI()
        self.m_version = '1.4.0'


class A1_Setup(SetupMixin, unittest.TestCase):
    """ This section tests the SetupMixin Class
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))

    def test_01_PyHouse(self):
        """ Be sure that the XML contains the right stuff.
        """
        self.assertNotEqual(self.m_pyhouse_obj.APIs, None)

    def test_02_FindXml(self):
        """ Be sure that the XML contains the right stuff.
        """
        self.assertEqual(self.m_xml.root.tag, 'PyHouse')
        self.assertEqual(self.m_xml.house_div.tag, 'HouseDivision')
        self.assertEqual(self.m_xml.lighting_sect.tag, 'LightingSection')
        self.assertEqual(self.m_xml.light_sect.tag, 'LightSection')
        self.assertEqual(self.m_xml.light.tag, 'Light', 'XML - No Light')
        self.assertEqual(self.m_xml.controller_sect.tag, 'ControllerSection')
        self.assertEqual(self.m_xml.controller.tag, 'Controller')
        self.assertEqual(self.m_xml.button_sect.tag, 'ButtonSection')
        self.assertEqual(self.m_xml.button.tag, 'Button')

    def test_03_LightXML(self):
        """ Be sure that the XML contains the right stuff.
        """
        l_xml = self.m_xml.light
        self.assertEqual(l_xml.attrib['Name'], 'Insteon Light')

    def test_04_Api(self):
        pass

    def test_05_CtlBtnLgt(self):
        pass

    def test_06_Family(self):
        pass


class B1_Parts_1_4(SetupMixin, unittest.TestCase):
    """ This section tests the reading and writing of XML.
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))

    def test_01_Base(self):
        """ Read in the xml file and fill in the lights
        """
        l_base = self.m_api._read_base(self.m_pyhouse_obj, self.m_light_obj, self.m_xml.light)
        self.assertEqual(l_base.Name, 'Insteon Light')
        self.assertEqual(l_base.Key, 0)
        self.assertEqual(l_base.Active, True)

    def test_03_Device(self):
        l_device = self.m_api._read_base(self.m_pyhouse_obj, self.m_light_obj, self.m_xml.light)
        l_device = self.m_api._read_versioned_device(self.m_pyhouse_obj, l_device, self.m_xml.light)
        self.assertEqual(l_device.Comment, TESTING_DEVICE_COMMENT)
        self.assertEqual(l_device.DeviceFamily, TESTING_DEVICE_FAMILY_INSTEON)
        self.assertEqual(l_device.DeviceType, int(TESTING_DEVICE_TYPE))
        self.assertEqual(l_device.DeviceSubType, int(TESTING_DEVICE_SUBTYPE))
        self.assertEqual(l_device.RoomName, TESTING_DEVICE_ROOM_NAME)
        self.assertEqual(l_device.RoomCoords.X_Easting, float(TESTING_DEVICE_ROOM_X))
        self.assertEqual(l_device.RoomCoords.Y_Northing, float(TESTING_DEVICE_ROOM_Y))
        self.assertEqual(l_device.RoomCoords.Z_Height, float(TESTING_DEVICE_ROOM_Z))


class B2_Parts_1_3(SetupMixin, unittest.TestCase):
    """ This section tests the reading and writing of XML used by node_local.
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))

    def test_01_Base(self):
        """ Read in the xml file and fill in the lights
        """
        l_base = self.m_api._read_base(self.m_pyhouse_obj, self.m_light_obj, self.m_xml.light)
        self.assertEqual(l_base.Name, 'Insteon Light')
        self.assertEqual(l_base.Key, 0)
        self.assertEqual(l_base.Active, True)

    def test_02_Device_1_3(self):
        l_device = self.m_api._read_base(self.m_pyhouse_obj, self.m_light_obj, self.m_xml.light)
        l_device = self.m_api._read_versioned_device(self.m_pyhouse_obj, l_device, self.m_xml.light)
        self.assertEqual(l_device.RoomName, TESTING_DEVICE_ROOM_NAME)


class C1_Read(SetupMixin, unittest.TestCase):
    """ This section tests the reading and writing of XML used by node_local.
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))

    def test_01_Core(self):
        l_core = self.m_api.read_core_lighting_xml(self.m_pyhouse_obj, self.m_light_obj, self.m_xml.light)
        self.assertEqual(l_core.Name, 'Insteon Light')
        self.assertEqual(l_core.Key, 0)
        self.assertEqual(l_core.Active, True)
        self.assertEqual(l_core.UUID, TESTING_DEVICE_UUID)
        self.assertEqual(l_core.Comment, TESTING_DEVICE_COMMENT)
        self.assertEqual(l_core.DeviceFamily, TESTING_DEVICE_FAMILY_INSTEON)
        self.assertEqual(l_core.DeviceType, int(TESTING_DEVICE_TYPE))
        self.assertEqual(l_core.DeviceSubType, int(TESTING_DEVICE_SUBTYPE))
        self.assertEqual(l_core.RoomName, TESTING_DEVICE_ROOM_NAME)
        self.assertEqual(l_core.RoomCoords.X_Easting, float(TESTING_DEVICE_ROOM_X))

    def test_02_BaseLight(self):
        """ Read in the xml file and fill in the lights
        """
        l_base = self.m_api.read_core_lighting_xml(self.m_pyhouse_obj, self.m_light_obj, self.m_xml.light)
        self.assertEqual(l_base.Name, 'Insteon Light')
        self.assertEqual(l_base.Key, 0)
        self.assertEqual(l_base.Active, True)
        self.assertEqual(l_base.Comment, TESTING_DEVICE_COMMENT)
        self.assertEqual(l_base.DeviceFamily, TESTING_DEVICE_FAMILY_INSTEON)
        self.assertEqual(l_base.RoomName, TESTING_DEVICE_ROOM_NAME)
        self.assertEqual(l_base.RoomCoords.X_Easting, float(TESTING_DEVICE_ROOM_X))

    def test_03_BaseController(self):
        """ Read in the xml file and fill in the lights
        """
        l_base = self.m_api.read_core_lighting_xml(self.m_pyhouse_obj, self.m_light_obj, self.m_xml.controller)
        self.assertEqual(l_base.Name, 'Insteon Serial Controller')
        self.assertEqual(l_base.Key, 0)
        self.assertEqual(l_base.Active, True)
        self.assertEqual(l_base.Comment, TESTING_DEVICE_COMMENT)
        self.assertEqual(l_base.RoomCoords.X_Easting, float(TESTING_DEVICE_ROOM_X))
        self.assertEqual(l_base.DeviceFamily, TESTING_DEVICE_FAMILY_INSTEON)
        self.assertEqual(l_base.RoomName, TESTING_DEVICE_ROOM_NAME)

    def test_04_BaseButton(self):
        """ Read in the xml file and fill in the lights
        """
        l_base = self.m_api.read_core_lighting_xml(self.m_pyhouse_obj, self.m_button_obj, self.m_xml.button)
        self.assertEqual(l_base.Name, 'Insteon Button')
        self.assertEqual(l_base.Key, 0)
        self.assertEqual(l_base.Active, True)
        self.assertEqual(l_base.Comment, TESTING_DEVICE_COMMENT)
        self.assertEqual(l_base.DeviceFamily, TESTING_DEVICE_FAMILY_INSTEON)
        self.assertEqual(l_base.RoomName, TESTING_DEVICE_ROOM_NAME)
        self.assertEqual(l_base.RoomCoords.X_Easting, float(TESTING_DEVICE_ROOM_X))


class D1_Write(SetupMixin, unittest.TestCase):
    """ This section tests the writing of XML used by Core Lighting
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))

    def test_01_BaseLight(self):
        """ Write the Core Light XML.
        """
        l_base = self.m_api.read_core_lighting_xml(self.m_pyhouse_obj, self.m_light_obj, self.m_xml.light)
        l_xml = self.m_api.write_core_lighting_xml('Light', l_base)
        #  print(PrettyFormatAny.form(l_xml, 'Lighting Core'))
        self.assertEqual(l_xml.attrib['Name'], 'Insteon Light')
        self.assertEqual(l_xml.attrib['Key'], '0')
        self.assertEqual(l_xml.attrib['Active'], 'True')
        self.assertEqual(l_xml.find('Comment').text, TESTING_DEVICE_COMMENT)
        self.assertEqual(l_xml.find('DeviceFamily').text, TESTING_DEVICE_FAMILY_INSTEON)
        self.assertEqual(l_xml.find('DeviceType').text, TESTING_DEVICE_TYPE)
        self.assertEqual(l_xml.find('DeviceSubType').text, TESTING_DEVICE_SUBTYPE)
        self.assertEqual(l_xml.find('RoomName').text, TESTING_DEVICE_ROOM_NAME)

    def test_02_BaseController(self):
        """ Write the Core Controller XML.
        """
        l_base = self.m_api.read_core_lighting_xml(self.m_pyhouse_obj, self.m_light_obj, self.m_xml.controller)
        l_xml = self.m_api.write_core_lighting_xml('Light', l_base)
        self.assertEqual(l_xml.attrib['Name'], 'Insteon Serial Controller')
        self.assertEqual(l_xml.attrib['Key'], '0')
        self.assertEqual(l_xml.attrib['Active'], 'True')
        self.assertEqual(l_xml.find('Comment').text, TESTING_DEVICE_COMMENT)
        self.assertEqual(l_xml.find('DeviceFamily').text, TESTING_DEVICE_FAMILY_INSTEON)
        self.assertEqual(l_xml.find('DeviceType').text, TESTING_DEVICE_TYPE)
        self.assertEqual(l_xml.find('DeviceSubType').text, TESTING_DEVICE_SUBTYPE)
        self.assertEqual(l_xml.find('RoomName').text, TESTING_DEVICE_ROOM_NAME)

    def test_03_BaseButton(self):
        """ Write the Core Button XML.
        """
        l_base = self.m_api.read_core_lighting_xml(self.m_pyhouse_obj, self.m_light_obj, self.m_xml.button)
        l_xml = self.m_api.write_core_lighting_xml('Light', l_base)
        self.assertEqual(l_xml.attrib['Name'], 'Insteon Button')
        self.assertEqual(l_xml.attrib['Key'], '0')
        self.assertEqual(l_xml.attrib['Active'], 'True')
        self.assertEqual(l_xml.find('Comment').text, TESTING_DEVICE_COMMENT)
        self.assertEqual(l_xml.find('DeviceFamily').text, TESTING_DEVICE_FAMILY_INSTEON)
        self.assertEqual(l_xml.find('DeviceType').text, TESTING_DEVICE_TYPE)
        self.assertEqual(l_xml.find('DeviceSubType').text, TESTING_DEVICE_SUBTYPE)
        self.assertEqual(l_xml.find('RoomName').text, TESTING_DEVICE_ROOM_NAME)

#  ## END DBK
