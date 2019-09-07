"""
@name:      Modules/Housing/Security/_test/test_security.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2016-2019 by D. Brian Kimmel
@license:   MIT License
@note:      Created on Nov 1, 2016
@summary:   Test

Passed all 13 tests - DBK - 2018-02-13

"""

__updated__ = '2019-08-10'

# Import system type stuff
import xml.etree.ElementTree as ET
from twisted.trial import unittest

# Import PyMh files and modules.
from Modules.Core.data_objects import GarageDoorData
from Modules.House.Security.security import Utility, API as securityAPI
from Modules.House.Family.family import API as familyAPI
from Modules.Core.Utilities import convert, json_tools
from _test.testing_mixin import SetupPyHouseObj
# from Modules.Core.Utilities.debug_tools import PrettyFormatAny


class SetupMixin(object):

    def setUp(self):
        self.m_pyhouse_obj = SetupPyHouseObj().BuildPyHouseObj()
        self.m_xml = SetupPyHouseObj().BuildXml()
        self.m_family = familyAPI(self.m_pyhouse_obj).LoadFamilyTesting()
        self.m_pyhouse_obj.House.Family = self.m_family
        self.m_api = securityAPI
        self.m_garage_door_obj = GarageDoorData()


class A0(unittest.TestCase):

    def setUp(self):
        pass

    def test_00_Print(self):
        print('Id: test_security')


class A1(SetupMixin, unittest.TestCase):
    """ This section tests the reading and writing of XML used by lighting_controllers.
    """

    def setUp(self):
        SetupMixin.setUp(self)

    def test_01_FindXml(self):
        """ Be sure that the XML contains the right stuff.
        """
        # print(PrettyFormatAny.form(self.m_xml, 'A1-01-A - Tags'))
        self.assertEqual(self.m_xml.root.tag, TESTING_PYHOUSE)
        self.assertEqual(self.m_xml.security_sect.tag, 'SecuritySection')
        self.assertEqual(self.m_xml.garagedoor_sect.tag, 'GarageDoorSection')
        self.assertEqual(self.m_xml.garagedoor.tag, 'GarageDoor')
        self.assertEqual(self.m_xml.motiondetector_sect.tag, 'MotionDetectorSection')
        self.assertEqual(self.m_xml.motiondetector.tag, 'Motion')

    def test_02_Xml(self):
        # print(PrettyFormatAny.form(self.m_pyhouse_obj._Config.XmlRoot))
        pass

    def test_03_Family(self):
        self.assertEqual(self.m_family['Insteon'].Name, 'Insteon')


class B1_Read(SetupMixin, unittest.TestCase):
    """ This section tests the reading and writing of XML used by lighting_garage_doors.
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))

    def test_01_DoorBaseData(self):
        """ Read in the xml file and fill in the lights
        """
        l_door = Utility._read_base_device(self.m_pyhouse_obj, self.m_xml.garagedoor)
        # print(PrettyFormatAny.form(l_door, 'B1-01-A - Gafrage Door'))
        self.assertEqual(str(l_door.Name), TESTING_GARAGE_DOOR_NAME_0)
        self.assertEqual(str(l_door.Active), TESTING_GARAGE_DOOR_ACTIVE_0)
        self.assertEqual(str(l_door.Key), TESTING_GARAGE_DOOR_KEY_0)
        self.assertEqual(str(l_door.UUID), TESTING_GARAGE_DOOR_UUID_0)
        self.assertEqual(str(l_door.Comment), TESTING_GARAGE_DOOR_COMMENT_0)
        self.assertEqual(str(l_door.DeviceFamily), TESTING_DEVICE_FAMILY_INSTEON)
        self.assertEqual(str(l_door.DeviceType), TESTING_GARAGE_DOOR_DEVICE_TYPE_0)
        self.assertEqual(str(l_door.DeviceSubType), TESTING_GARAGE_DOOR_DEVICE_SUBTYPE_0)
        self.assertEqual(str(l_door.RoomName), TESTING_GARAGE_DOOR_ROOM_NAME_0)
        self.assertEqual(str(l_door.RoomUUID), TESTING_GARAGE_DOOR_ROOM_UUID_0)

    def test_02_OneDoor(self):
        """ Read in the xml file and fill in the lights
        """
        l_door = Utility._read_one_door_xml(self.m_pyhouse_obj, self.m_xml.garagedoor)
        # print(PrettyFormatAny.form(l_door, 'B1-02-A - Button'))
        self.assertEqual(str(l_door.Name), TESTING_GARAGE_DOOR_NAME_0)
        self.assertEqual(str(l_door.Active), TESTING_GARAGE_DOOR_ACTIVE_0)
        self.assertEqual(str(l_door.Key), TESTING_GARAGE_DOOR_KEY_0)
        self.assertEqual(l_door.DevCat, convert.dotted_hex2int(TESTING_INSTEON_DEVCAT_0))
        self.assertEqual(str(l_door.EngineVersion), TESTING_INSTEON_ENGINE_VERSION_0)
        self.assertEqual(l_door.InsteonAddress, convert.dotted_hex2int(TESTING_INSTEON_ADDRESS_0))

    def test_03_AllDoors(self):
        l_doors = XML().read_all_GarageDoors_xml(self.m_pyhouse_obj)
        # print(PrettyFormatAny.form(l_doors, 'B1-03-A - Doors'))
        self.assertEqual(len(l_doors), 1)

    def test_04_MotionBaseData(self):
        """ Read in the xml file and fill in the lights
        """
        l_door = Utility._read_base_motion_device(self.m_pyhouse_obj, self.m_xml.motiondetector)
        # print(PrettyFormatAny.form(l_door, 'B1-01-A - Motion Detector'))
        self.assertEqual(str(l_door.Name), TESTING_MOTION_SENSOR_NAME_0)
        self.assertEqual(str(l_door.Active), TESTING_MOTION_SENSOR_ACTIVE_0)
        self.assertEqual(str(l_door.Key), TESTING_MOTION_SENSOR_KEY_0)
        self.assertEqual(str(l_door.UUID), TESTING_MOTION_SENSOR_UUID_0)
        self.assertEqual(str(l_door.Comment), TESTING_MOTION_SENSOR_COMMENT_0)
        self.assertEqual(str(l_door.DeviceFamily), TESTING_DEVICE_FAMILY_INSTEON)
        self.assertEqual(str(l_door.DeviceType), TESTING_MOTION_SENSOR_DEVICE_TYPE_0)
        self.assertEqual(str(l_door.DeviceSubType), TESTING_MOTION_SENSOR_DEVICE_SUBTYPE_0)
        self.assertEqual(str(l_door.RoomName), TESTING_MOTION_SENSOR_ROOM_NAME_0)
        self.assertEqual(str(l_door.RoomUUID), TESTING_MOTION_SENSOR_ROOM_UUID_0)

    def test_05_OneMotion(self):
        """ Read in the xml file and fill in the lights
        """
        l_dev = Utility._read_one_motion_xml(self.m_pyhouse_obj, self.m_xml.motiondetector)
        # print(PrettyFormatAny.form(l_dev, 'B1-05-A - Motion Detector'))
        self.assertEqual(str(l_dev.Name), TESTING_MOTION_SENSOR_NAME_0)
        self.assertEqual(str(l_dev.Active), TESTING_MOTION_SENSOR_ACTIVE_0)
        self.assertEqual(str(l_dev.Key), TESTING_MOTION_SENSOR_KEY_0)
        self.assertEqual(l_dev.DevCat, convert.dotted_hex2int(TESTING_MOTION_SENSOR_DEVCAT_0))
        self.assertEqual(str(l_dev.EngineVersion), TESTING_INSTEON_ENGINE_VERSION_0)
        self.assertEqual(l_dev.InsteonAddress, convert.dotted_hex2int(TESTING_MOTION_SENSOR_ADDRESS_0))

    def test_06_AllMotion(self):
        l_all = XML().read_all_MotionSensors_xml(self.m_pyhouse_obj)
        # print(PrettyFormatAny.form(l_all, 'B1-06-A - Motion Sensors'))
        self.assertEqual(len(l_all), 1)


class B2_Write(SetupMixin, unittest.TestCase):
    """ This section tests the reading and writing of XML used by lighting_controllers.
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))
        l_doors = XML().read_all_GarageDoors_xml(self.m_pyhouse_obj)
        self.m_pyhouse_obj.House.Security.GarageDoors = l_doors

    def test_01_OneDoor(self):
        """ Write out the XML file for the button section
        """
        l_xml = Utility._write_one_door_xml(self.m_pyhouse_obj, self.m_pyhouse_obj.House.Security.GarageDoors[0])
        # print(PrettyFormatAny.form(l_xml, 'B2-01-A - One Door'))
        self.assertEqual(l_xml.attrib['Name'], TESTING_GARAGE_DOOR_NAME_0)
        self.assertEqual(str(l_xml.attrib['Active']), TESTING_GARAGE_DOOR_ACTIVE_0)
        self.assertEqual(l_xml.find('UUID').text, TESTING_GARAGE_DOOR_UUID_0)
        self.assertEqual(l_xml.find('Comment').text, TESTING_GARAGE_DOOR_COMMENT_0)
        self.assertEqual(l_xml.find('DeviceFamily').text, TESTING_DEVICE_FAMILY_INSTEON)
        self.assertEqual(l_xml.find('DeviceType').text, TESTING_GARAGE_DOOR_DEVICE_TYPE_0)
        self.assertEqual(l_xml.find('DeviceSubType').text, TESTING_GARAGE_DOOR_DEVICE_SUBTYPE_0)
        self.assertEqual(l_xml.find('RoomName').text, TESTING_GARAGE_DOOR_ROOM_NAME_0)
        self.assertEqual(l_xml.find('RoomUUID').text, TESTING_GARAGE_DOOR_ROOM_UUID_0)

    def test_02_AllDoors(self):
        """ Write out the XML file for the Buttons section
        """
        l_xml = XML().write_all_GarageDoors_xml(self.m_pyhouse_obj)
        # print(PrettyFormatAny.form(l_xml, 'B2-02-A - All Doors'))
        self.assertEqual(l_xml[0].attrib['Name'], TESTING_GARAGE_DOOR_NAME_0)
        self.assertEqual(str(l_xml[0].attrib['Active']), TESTING_GARAGE_DOOR_ACTIVE_0)
        self.assertEqual(l_xml[0].find('UUID').text, TESTING_GARAGE_DOOR_UUID_0)
        self.assertEqual(l_xml[0].find('Comment').text, TESTING_GARAGE_DOOR_COMMENT_0)
        self.assertEqual(l_xml[0].find('DeviceFamily').text, TESTING_DEVICE_FAMILY_INSTEON)
        self.assertEqual(l_xml[0].find('DeviceType').text, TESTING_GARAGE_DOOR_DEVICE_TYPE_0)
        self.assertEqual(l_xml[0].find('DeviceSubType').text, TESTING_GARAGE_DOOR_DEVICE_SUBTYPE_0)
        self.assertEqual(l_xml[0].find('RoomName').text, TESTING_GARAGE_DOOR_ROOM_NAME_0)
        self.assertEqual(l_xml[0].find('RoomUUID').text, TESTING_GARAGE_DOOR_ROOM_UUID_0)


class J1_Json(SetupMixin, unittest.TestCase):
    """ This section tests the reading and writing of XML used by lighting_controllers.
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))
        l_doors = XML().read_all_GarageDoors_xml(self.m_pyhouse_obj)
        self.m_pyhouse_obj.House.Security.GarageDoors = l_doors

    def test_06_CreateJson(self):
        """ Create a JSON object for Buttons.
        """
        # print('ButtonsS: {}'.format(l_doors))
        # print('Button 0: {}'.format(vars(l_doors[0])))
        l_json = json_tools.encode_json(self.m_pyhouse_obj.House.Security.GarageDoors)
        # print('JSON: {}'.format(l_json))

# ## END DBK
