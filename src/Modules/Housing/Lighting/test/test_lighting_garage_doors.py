"""
@name:      /home/briank/PyHouse/src/Modules/Housing/Lighting/test/test_lighting_garage_door.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2016-2016 by D. Brian Kimmel
@license:   MIT License
@note:      Created on Oct 11, 2016
@summary:   Test

Passed all 9 tests - DBK - 2016-10-12

"""

__updated__ = '2016-10-12'

# Import system type stuff
import xml.etree.ElementTree as ET
from twisted.trial import unittest

# Import PyMh files and modules.
from Modules.Core.data_objects import GarageDoorData
from Modules.Core.test.xml_device import \
    TESTING_DEVICE_COMMENT_0, \
    TESTING_DEVICE_ROOM_NAME, \
    TESTING_DEVICE_FAMILY_INSTEON, \
    TESTING_DEVICE_TYPE
from Modules.Housing.Lighting.lighting_garagedoors import Utility, API as garageDoorAPI
from Modules.Housing.Lighting.test.xml_garagedoors import \
    TESTING_GARAGE_DOOR_NAME_0, \
    TESTING_GARAGE_DOOR_COMMENT_0, \
    TESTING_GARAGE_DOOR_DEVICE_TYPE_0, \
    TESTING_GARAGE_DOOR_DEVICE_SUBTYPE_0, \
    TESTING_GARAGE_DOOR_ROOM_NAME_0, \
    TESTING_GARAGE_DOOR_ROOM_UUID_0, \
    TESTING_GARAGE_DOOR_ACTIVE_0, \
    TESTING_GARAGE_DOOR_KEY_0
from Modules.Families.family import API as familyAPI
from Modules.Core import conversions
from test.xml_data import XML_LONG
from Modules.Families.Insteon.test.xml_insteon import \
    TESTING_INSTEON_ADDRESS_0, TESTING_INSTEON_DEVCAT_0, TESTING_INSTEON_ENGINE_VERSION_0
from test.testing_mixin import SetupPyHouseObj
from Modules.Utilities import json_tools
from Modules.Utilities.debug_tools import PrettyFormatAny


class SetupMixin(object):

    def setUp(self, p_root):
        self.m_pyhouse_obj = SetupPyHouseObj().BuildPyHouseObj(p_root)
        self.m_xml = SetupPyHouseObj().BuildXml(p_root)
        self.m_family = familyAPI(self.m_pyhouse_obj).LoadFamilyTesting()
        self.m_pyhouse_obj.House.FamilyData = self.m_family
        self.m_api = garageDoorAPI
        self.m_garage_door_obj = GarageDoorData()


class A1(SetupMixin, unittest.TestCase):
    """ This section tests the reading and writing of XML used by lighting_controllers.
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))

    def test_01_FindXml(self):
        """ Be sure that the XML contains the right stuff.
        """
        self.assertEqual(self.m_xml.root.tag, 'PyHouse')
        self.assertEqual(self.m_xml.garagedoor_sect.tag, 'GarageDoorSection')
        self.assertEqual(self.m_xml.garagedoor.tag, 'GarageDoor')

    def test_02_Xml(self):
        pass

    def test_03_Family(self):
        self.assertEqual(self.m_family['Insteon'].Name, 'Insteon')


class B1_Read(SetupMixin, unittest.TestCase):
    """ This section tests the reading and writing of XML used by lighting_garage_doors.
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))

    def test_01_ReadDoorBaseData(self):
        """ Read in the xml file and fill in the lights
        """
        l_door = Utility._read_base_device(self.m_pyhouse_obj, self.m_xml.garagedoor)
        # print(PrettyFormatAny.form(l_door, 'B1-01-A - Gafrage Door'))
        self.assertEqual(str(l_door.Name), TESTING_GARAGE_DOOR_NAME_0)
        self.assertEqual(str(l_door.Active), TESTING_GARAGE_DOOR_ACTIVE_0)
        self.assertEqual(str(l_door.Key), TESTING_GARAGE_DOOR_KEY_0)
        self.assertEqual(str(l_door.Comment), TESTING_GARAGE_DOOR_COMMENT_0)
        self.assertEqual(str(l_door.DeviceFamily), TESTING_DEVICE_FAMILY_INSTEON)
        self.assertEqual(str(l_door.DeviceType), TESTING_GARAGE_DOOR_DEVICE_TYPE_0)
        self.assertEqual(str(l_door.DeviceSubType), TESTING_GARAGE_DOOR_DEVICE_SUBTYPE_0)
        self.assertEqual(str(l_door.RoomName), TESTING_GARAGE_DOOR_ROOM_NAME_0)
        self.assertEqual(str(l_door.RoomUUID), TESTING_GARAGE_DOOR_ROOM_UUID_0)

    def test_02_ReadOneDoorXml(self):
        """ Read in the xml file and fill in the lights
        """
        l_door = Utility._read_one_door_xml(self.m_pyhouse_obj, self.m_xml.garagedoor)
        # print(PrettyFormatAny.form(l_door, 'B1-02-A - Button'))
        self.assertEqual(str(l_door.Name), TESTING_GARAGE_DOOR_NAME_0)
        self.assertEqual(str(l_door.Active), TESTING_GARAGE_DOOR_ACTIVE_0)
        self.assertEqual(str(l_door.Key), TESTING_GARAGE_DOOR_KEY_0)
        self.assertEqual(l_door.DevCat, conversions.dotted_hex2int(TESTING_INSTEON_DEVCAT_0))
        self.assertEqual(str(l_door.EngineVersion), TESTING_INSTEON_ENGINE_VERSION_0)
        self.assertEqual(l_door.InsteonAddress, conversions.dotted_hex2int(TESTING_INSTEON_ADDRESS_0))

    def test_03_ReadAllDoorsXml(self):
        l_doors = self.m_api.read_all_GarageDoors_xml(self.m_pyhouse_obj, self.m_xml.garagedoor_sect)
        print(PrettyFormatAny.form(l_doors, 'B1-03-A - Doors'))
        self.assertEqual(len(l_doors), 1)


class B2_Write(SetupMixin, unittest.TestCase):
    """ This section tests the reading and writing of XML used by lighting_controllers.
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))

    def test_01_OneButton(self):
        """ Write out the XML file for the button section
        """
        l_door = Utility._read_one_door_xml(self.m_pyhouse_obj, self.m_xml.button)
        l_xml = Utility._write_one_door_xml(self.m_pyhouse_obj, l_door)

    def test_02_AllButtons(self):
        """ Write out the XML file for the Buttons section
        """
        l_door = self.m_api.read_all_GarageDoors_xml(self.m_pyhouse_obj, self.m_xml.button_sect)
        l_xml = self.m_api.write_all_GarageDoors_xml(self.m_pyhouse_obj)


class J1_Json(SetupMixin, unittest.TestCase):
    """ This section tests the reading and writing of XML used by lighting_controllers.
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))

    def test_06_CreateJson(self):
        """ Create a JSON object for Buttons.
        """
        l_doors = self.m_api.read_all_GarageDoors_xml(self.m_pyhouse_obj, self.m_xml.button_sect)
        # print('ButtonsS: {}'.format(l_doors))
        # print('Button 0: {}'.format(vars(l_doors[0])))
        l_json = json_tools.encode_json(l_doors)
        # print('JSON: {}'.format(l_json))

# ## END DBK
