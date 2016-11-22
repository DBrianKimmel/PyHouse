"""
@name:      PyHouse/src/Housing/test/test_rooms.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2013-2016 by D. Brian Kimmel
@license:   MIT License
@note:      Created on Apr 10, 2013
@summary:   Test handling the rooms information for a house.

Passed all 16 tests - DBK 2016-07-02
"""

__updated__ = '2016-11-21'

# Import system type stuff
import xml.etree.ElementTree as ET
from twisted.trial import unittest

# Import PyMh files
from Modules.Housing.rooms import RoomCls as roomsApi, Maint as roomsMaint
from test.xml_data import XML_LONG
from test.testing_mixin import SetupPyHouseObj
from Modules.Utilities import json_tools
from Modules.Housing.test.xml_rooms import \
    TESTING_ROOM_NAME_0, \
    TESTING_ROOM_COMMENT_0, \
    TESTING_ROOM_CORNER_0, \
    TESTING_ROOM_SIZE_0, \
    TESTING_ROOM_ACTIVE_0, \
    TESTING_ROOM_KEY_0, \
    TESTING_ROOM_NAME_1, \
    TESTING_ROOM_FLOOR_0, \
    TESTING_ROOM_TYPE_0, \
    TESTING_ROOM_UUID_0, \
    TESTING_ROOM_NAME_2, \
    TESTING_ROOM_NAME_3, \
    TESTING_ROOM_CORNER_X_0, \
    TESTING_ROOM_SIZE_X_0, \
    TESTING_ROOM_KEY_3, \
    TESTING_ROOM_ACTIVE_3, \
    TESTING_ROOM_COMMENT_3, \
    TESTING_ROOM_UUID_3, \
    TESTING_ROOM_FLOOR_3, \
    TESTING_ROOM_SIZE_3, \
    TESTING_ROOM_TYPE_3, \
    TESTING_ROOM_CORNER_3, \
    TESTING_ROOM_UUID_2, \
    TESTING_ROOM_UUID_1, \
    TESTING_ROOM_LAST_UPDATE_0
from Modules.Housing.test.xml_housing import \
    TESTING_HOUSE_NAME, TESTING_HOUSE_ACTIVE, TESTING_HOUSE_KEY, TESTING_HOUSE_UUID
from Modules.Utilities.debug_tools import PrettyFormatAny

JSON = {
        'Name': TESTING_ROOM_NAME_3,
        'Key': TESTING_ROOM_KEY_3,
        'Active': TESTING_ROOM_ACTIVE_3,
        'UUID': TESTING_ROOM_UUID_3,
        'Comment': TESTING_ROOM_COMMENT_3,
        'Corner': TESTING_ROOM_CORNER_3,
        'Floor': TESTING_ROOM_FLOOR_3,
        'Size': TESTING_ROOM_SIZE_3,
        'RoomType': TESTING_ROOM_TYPE_3,
        'Add': True,
        'Delete': False
        }


class SetupMixin(object):

    def setUp(self, p_root):
        self.m_pyhouse_obj = SetupPyHouseObj().BuildPyHouseObj(p_root)
        self.m_xml = SetupPyHouseObj().BuildXml(p_root)
        self.m_api = roomsApi
        self.m_maint = roomsMaint


class A0(unittest.TestCase):
    def setUp(self):
        pass
    def test_00_Print(self):
        print('Id: test_rooms')


class A1_Setup(SetupMixin, unittest.TestCase):
    """Test that we have set up properly for the rest of the testing classes.
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))

    def test_1_BuildObjects(self):
        """ Test to be sure the compound object was built correctly - Rooms is an empty dict.
        """
        # print(PrettyFormatAny.form(self.m_xml, 'Tags'))
        self.assertEqual(self.m_pyhouse_obj.House.Rooms, None)

    def test_2_FindXml(self):
        """ Be sure that the XML contains the right stuff.
        """
        # print(PrettyFormatAny.form(self.m_xml, 'Tags'))
        self.assertEqual(self.m_xml.root.tag, 'PyHouse')
        self.assertEqual(self.m_xml.house_div.tag, 'HouseDivision')
        self.assertEqual(self.m_xml.room_sect.tag, 'RoomSection')
        self.assertEqual(self.m_xml.room.tag, 'Room')

    def test_3_pyhouse(self):
        print(PrettyFormatAny.form(self.m_pyhouse_obj, 'Base'))
        print(PrettyFormatAny.form(self.m_pyhouse_obj.APIs, 'APIs'))
        print(PrettyFormatAny.form(self.m_pyhouse_obj.APIs.Computer, 'APIs.Computer'))
        print(PrettyFormatAny.form(self.m_pyhouse_obj.APIs.Computer.MqttAPI, 'MqttAPI'))


class A2_XML(SetupMixin, unittest.TestCase):
    """ Now we test that the xml_xxxxx have set up the XML_LONG tree properly.
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))

    def test_1_HouseDiv(self):
        """ Test
        """
        l_xml = self.m_xml.house_div
        # print(PrettyFormatAny.form(l_xml, 'House'))
        self.assertEqual(l_xml.attrib['Name'], TESTING_HOUSE_NAME)
        self.assertEqual(l_xml.attrib['Active'], TESTING_HOUSE_ACTIVE)
        self.assertEqual(l_xml.attrib['Key'], TESTING_HOUSE_KEY)
        self.assertEqual(l_xml.find('UUID').text, TESTING_HOUSE_UUID)

    def test_2_RoomCount(self):
        """ Test
        """
        l_xml = self.m_xml.room_sect
        # print(PrettyFormatAny.form(l_xml, 'Rooms'))
        self.assertEqual(len(l_xml), 3)
        self.assertEqual(l_xml[0].attrib['Name'], TESTING_ROOM_NAME_0)
        self.assertEqual(l_xml[1].attrib['Name'], TESTING_ROOM_NAME_1)
        self.assertEqual(l_xml[2].attrib['Name'], TESTING_ROOM_NAME_2)

    def test_3_Room0(self):
        """ Be sure that the XML contains everything in RoomData().
        """
        l_xml = self.m_xml.room
        # print(PrettyFormatAny.form(self.m_xml.room, 'Room'))
        self.assertEqual(l_xml.attrib['Name'], TESTING_ROOM_NAME_0)
        self.assertEqual(l_xml.attrib['Key'], TESTING_ROOM_KEY_0)
        self.assertEqual(l_xml.attrib['Active'], TESTING_ROOM_ACTIVE_0)
        self.assertEqual(l_xml.find('UUID').text, TESTING_ROOM_UUID_0)
        self.assertEqual(l_xml.find('Comment').text, TESTING_ROOM_COMMENT_0)
        self.assertEqual(l_xml.find('Corner').text, TESTING_ROOM_CORNER_0)
        self.assertEqual(l_xml.find('Floor').text, TESTING_ROOM_FLOOR_0)
        self.assertEqual(l_xml.find('LastUpdate').text, str(TESTING_ROOM_LAST_UPDATE_0))
        self.assertEqual(l_xml.find('Size').text, TESTING_ROOM_SIZE_0)
        self.assertEqual(l_xml.find('RoomType').text, TESTING_ROOM_TYPE_0)


class B1_Read(SetupMixin, unittest.TestCase):
    """ Test that we read in the XML config fproperly.
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))

    def test_1_OneRoom(self):
        """ Read the xml and fill in the first room's dict
        """
        l_room = self.m_api.read_one_room(self.m_xml.room)
        # print(PrettyFormatAny.form(l_room, 'B1-1-A - One Room'))
        self.assertEqual(l_room.Name, TESTING_ROOM_NAME_0)
        self.assertEqual(l_room.Key, int(TESTING_ROOM_KEY_0))
        self.assertEqual(l_room.Active, bool(TESTING_ROOM_ACTIVE_0))
        self.assertEqual(l_room.UUID, TESTING_ROOM_UUID_0)
        #
        self.assertEqual(l_room.Comment, TESTING_ROOM_COMMENT_0)
        self.assertEqual(l_room.Corner.X_Easting, float(TESTING_ROOM_CORNER_X_0))
        self.assertEqual(l_room.Floor, TESTING_ROOM_FLOOR_0)
        self.assertEqual(l_room.LastUpdate, TESTING_ROOM_LAST_UPDATE_0)
        self.assertEqual(l_room.Size.X_Easting, float(TESTING_ROOM_SIZE_X_0))
        self.assertEqual(l_room.RoomType, TESTING_ROOM_TYPE_0)
        self.assertEqual(l_room._AddFlag, False)
        self.assertEqual(l_room._DeleteFlag, False)

    def test_2_AllRooms(self):
        """ Read in the xml file and fill in the rooms dict
        """
        l_rooms = self.m_api(self.m_pyhouse_obj).read_rooms_xml(self.m_pyhouse_obj)
        # print(PrettyFormatAny.form(l_rooms, 'B1-2-A - All Rooms'))
        # print(PrettyFormatAny.form(self.m_pyhouse_obj, 'B1-2-b - PyHouse_Obj'))
        self.assertEqual(len(l_rooms), 3)
        self.assertEqual(l_rooms[0].Name, TESTING_ROOM_NAME_0)
        self.assertEqual(l_rooms[1].Name, TESTING_ROOM_NAME_1)
        self.assertEqual(l_rooms[2].Name, TESTING_ROOM_NAME_2)


class B2_Write(SetupMixin, unittest.TestCase):
    """ Test that we write out the XML config properly.
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))

    def test_1_OneRoom(self):
        """ Write out the XML file for the location section
        """
        l_xml = self.m_xml.room
        # print(PrettyFormatAny.form(l_xml, 'B2-1-A - Room Xml'))
        l_room = self.m_api.read_one_room(l_xml)
        # print(PrettyFormatAny.form(l_room, 'One Room'))
        l_xml = self.m_api.write_one_room(l_room)
        # print(PrettyFormatAny.form(l_xml, 'One Room'))
        self.assertEqual(l_xml.attrib['Name'], TESTING_ROOM_NAME_0)
        self.assertEqual(l_xml.attrib['Key'], TESTING_ROOM_KEY_0)
        self.assertEqual(l_xml.attrib['Active'], TESTING_ROOM_ACTIVE_0)
        self.assertEqual(l_xml.find('UUID').text, TESTING_ROOM_UUID_0)
        #
        self.assertEqual(l_xml.find('Comment').text, TESTING_ROOM_COMMENT_0)
        self.assertEqual(l_xml.find('Corner').text, TESTING_ROOM_CORNER_0)
        self.assertEqual(l_xml.find('Floor').text, TESTING_ROOM_FLOOR_0)
        self.assertEqual(l_xml.find('LastUpdate').text, str(TESTING_ROOM_LAST_UPDATE_0))
        self.assertEqual(l_xml.find('Size').text, TESTING_ROOM_SIZE_0)
        self.assertEqual(l_xml.find('RoomType').text, TESTING_ROOM_TYPE_0)

    def test_2_AllRooms(self):
        """ Write out the XML file for the location section
        """
        l_rooms = self.m_api(self.m_pyhouse_obj).read_rooms_xml(self.m_pyhouse_obj)
        l_xml = self.m_api.write_rooms_xml(l_rooms)
        # print(PrettyFormatAny.form(l_xml, 'B2-2-A - All Rooms'))
        # self.assertEqual(l_xml[0].attrib['Name'], TESTING_ROOM_NAME_0)
        self.assertEqual(l_xml[1].attrib['Name'], TESTING_ROOM_NAME_1)
        self.assertEqual(l_xml[2].attrib['Name'], TESTING_ROOM_NAME_2)


class D1_Maint(SetupMixin, unittest.TestCase):
    """
    """
    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))

    def _print(self, p_rooms):
        for l_obj in p_rooms.itervalues():
            print('D1-Print - Key:{}; Name:{}; UUID:{}; Update:{};'.format(
                    l_obj.Key, l_obj.Name, l_obj.UUID, l_obj.LastUpdate))
        print

    def test_1_Extract(self):
        """ Test extracting information passed back by the browser.
        The data comes in JSON format..
        """
        l_obj = self.m_maint()._json_2_obj(JSON)
        # print(PrettyFormatAny.form(l_obj, 'D1-1-A - Json'))
        self.assertEqual(l_obj.Name, TESTING_ROOM_NAME_3)
        self.assertEqual(l_obj.Key, int(TESTING_ROOM_KEY_3))
        self.assertEqual(l_obj.Active, TESTING_ROOM_ACTIVE_3)
        self.assertEqual(l_obj.UUID, TESTING_ROOM_UUID_3)
        self.assertEqual(l_obj.Comment, TESTING_ROOM_COMMENT_3)
        # self.assertEqual(l_obj.Corner, TESTING_ROOM_CORNER_3)
        self.assertEqual(l_obj.Floor, TESTING_ROOM_FLOOR_3)
        # self.assertEqual(l_obj.Size, TESTING_ROOM_SIZE_3)
        self.assertEqual(l_obj.RoomType, TESTING_ROOM_TYPE_3)

    def test_2_Add(self):
        """
        """
        l_rooms = self.m_api(self.m_pyhouse_obj).read_rooms_xml(self.m_pyhouse_obj)
        self.m_pyhouse_obj.House.Rooms = l_rooms
        l_obj = self.m_maint()._json_2_obj(JSON)
        self._print(l_rooms)
        # print(PrettyFormatAny.form(l_obj, 'D1-2-A - Json'))
        l_rooms = self.m_maint()._add_change_room(self.m_pyhouse_obj, l_obj)
        self._print(l_rooms)


class E1_Json(SetupMixin, unittest.TestCase):

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))

    def test_1_CreateJson(self):
        """ Create a JSON object for Rooms.
        """
        self.m_pyhouse_obj.House.Rooms = l_rooms = self.m_api(self.m_pyhouse_obj).read_rooms_xml(self.m_pyhouse_obj)
        l_json = json_tools.encode_json(l_rooms)
        l_obj = json_tools.decode_json_unicode(l_json)
        # print(PrettyFormatAny.form(l_json, 'JSON', 80))
        # print(PrettyFormatAny.form(l_obj, 'JSON', 80))
        self.assertEqual(len(l_obj), len(l_rooms))


class F1_Match(SetupMixin, unittest.TestCase):

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))

    def test_1_ByName(self):
        """ Create a JSON object for Rooms.
        """
        l_search = TESTING_ROOM_NAME_1
        self.m_pyhouse_obj.House.Rooms = self.m_api(self.m_pyhouse_obj).read_rooms_xml(self.m_pyhouse_obj)
        l_obj = self.m_api(self.m_pyhouse_obj).find_room_name(self.m_pyhouse_obj, l_search)
        # print(PrettyFormatAny.form(l_obj, 'F1-1-A - Room - {}'.format(l_search)))
        self.assertEqual(l_obj.Name, TESTING_ROOM_NAME_1)
        self.assertEqual(l_obj.UUID, TESTING_ROOM_UUID_1)

    def test_2_ByUuid(self):
        """ Create a JSON object for Rooms.
        """
        l_search = TESTING_ROOM_UUID_2
        self.m_pyhouse_obj.House.Rooms = self.m_api(self.m_pyhouse_obj).read_rooms_xml(self.m_pyhouse_obj)
        l_obj = self.m_api(self.m_pyhouse_obj).find_room_uuid(self.m_pyhouse_obj, l_search)
        # print(PrettyFormatAny.form(l_obj, 'F1-2-A - Room - {}'.format(l_search)))
        self.assertEqual(l_obj.Name, TESTING_ROOM_NAME_2)
        self.assertEqual(l_obj.UUID, TESTING_ROOM_UUID_2)

# ## END DBK
