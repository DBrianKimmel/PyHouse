"""
@name:      PyHouse/src/Housing/test/test_rooms.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2013-2016 by D. Brian Kimmel
@license:   MIT License
@note:      Created on Apr 10, 2013
@summary:   Test handling the rooms information for a house.

Passed all 11 tests - DBK 2016-06-16
"""


# Import system type stuff
import xml.etree.ElementTree as ET
from twisted.trial import unittest

# Import PyMh files
from Modules.Housing.rooms import Xml as roomsXml
from Modules.Housing.rooms import Maint as roomsMaint
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
    TESTING_ROOM_SIZE_X_0
from Modules.Utilities.debug_tools import PrettyFormatAny

JSON = {
        'Comment': 'cmt',
        'RoomType': 'Room',
        'UUID': '25130b18-eeb6-4642-9aaf-e3012fc8ed69',
        'Floor': '1',
        'Add': True,
        'Key': '1',
        'Active': True,
        'Corner': [1, 2, 3],
        'Name': 'Room 1',
        'Delete': False,
        'Size': [0.1, 2.3, 4.5]
        }


class SetupMixin(object):

    def setUp(self, p_root):
        self.m_pyhouse_obj = SetupPyHouseObj().BuildPyHouseObj(p_root)
        self.m_xml = SetupPyHouseObj().BuildXml(p_root)
        self.m_api = roomsXml


class A1_Setup(SetupMixin, unittest.TestCase):

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))

    def test_1_BuildObjects(self):
        """ Test to be sure the compound object was built correctly - Rooms is an empty dict.
        """
        # print(PrettyFormatAny.form(self.m_xml, 'Tags'))
        self.assertEqual(self.m_pyhouse_obj.House.Rooms, {}, 'No Rooms{}')

    def test_2_FindXml(self):
        """ Be sure that the XML contains the right stuff.
        """
        # print(PrettyFormatAny.form(self.m_xml, 'Tags'))
        self.assertEqual(self.m_xml.root.tag, 'PyHouse')
        self.assertEqual(self.m_xml.house_div.tag, 'HouseDivision')
        self.assertEqual(self.m_xml.room_sect.tag, 'RoomSection')
        self.assertEqual(self.m_xml.room.tag, 'Room', 'XML - No Room')


class A2_XML(SetupMixin, unittest.TestCase):

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))

    def test_1_Rooms(self):
        """ Test to be sure the compound object was built correctly - Rooms is an empty dict.
        """
        l_xml = self.m_xml.room_sect
        # print(PrettyFormatAny.form(l_xml, 'Rooms'))
        self.assertEqual(l_xml[0].attrib['Name'], TESTING_ROOM_NAME_0)
        self.assertEqual(l_xml[0].attrib['Name'], TESTING_ROOM_NAME_0)

    def test_2_Room0(self):
        """ Be sure that the XML contains the right stuff.
        """
        l_xml = self.m_xml.room
        # print(PrettyFormatAny.form(self.m_xml.room, 'Room'))
        self.assertEqual(l_xml.attrib['Name'], TESTING_ROOM_NAME_0)
        self.assertEqual(l_xml.attrib['Key'], TESTING_ROOM_KEY_0)
        self.assertEqual(l_xml.attrib['Active'], TESTING_ROOM_ACTIVE_0)
        self.assertEqual(l_xml[0].text, TESTING_ROOM_UUID_0)
        self.assertEqual(l_xml[1].text, TESTING_ROOM_COMMENT_0)
        self.assertEqual(l_xml[2].text, TESTING_ROOM_CORNER_0)
        self.assertEqual(l_xml[3].text, TESTING_ROOM_FLOOR_0)
        self.assertEqual(l_xml[4].text, TESTING_ROOM_SIZE_0)
        self.assertEqual(l_xml[5].text, TESTING_ROOM_TYPE_0)


class B1_Read(SetupMixin, unittest.TestCase):

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))

    def test_1_OneRoom(self):
        """ Read in the xml file and fill in the first room's dict
        """
        l_room = self.m_api.read_one_room(self.m_xml.room)
        # print(PrettyFormatAny.form(l_room, 'One Room'))
        self.assertEqual(l_room.Name, TESTING_ROOM_NAME_0)
        self.assertEqual(l_room.Key, int(TESTING_ROOM_KEY_0))
        self.assertEqual(l_room.Active, bool(TESTING_ROOM_ACTIVE_0))
        self.assertEqual(l_room.Comment, TESTING_ROOM_COMMENT_0)
        self.assertEqual(l_room.Corner.X_Easting, float(TESTING_ROOM_CORNER_X_0))
        self.assertEqual(l_room.Floor, TESTING_ROOM_FLOOR_0)
        self.assertEqual(l_room.Size.X_Easting, float(TESTING_ROOM_SIZE_X_0))
        self.assertEqual(l_room.RoomType, TESTING_ROOM_TYPE_0)
        self.assertEqual(l_room.UUID, TESTING_ROOM_UUID_0)

    def test_2_AllRooms(self):
        """ Read in the xml file and fill in the rooms dict
        """
        l_rooms = self.m_api.read_rooms_xml(self.m_xml.house_div)
        # print(PrettyFormatAny.form(l_rooms, 'All Room'))
        self.assertEqual(l_rooms[0].Name, TESTING_ROOM_NAME_0)
        self.assertEqual(l_rooms[1].Name, TESTING_ROOM_NAME_1)


class B2_Write(SetupMixin, unittest.TestCase):

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))

    def test_1_OneRoom(self):
        """ Write out the XML file for the location section
        """
        l_xml = self.m_xml.room
        # print(PrettyFormatAny.form(l_xml, 'Room Xml'))
        l_room = self.m_api.read_one_room(l_xml)
        # print(PrettyFormatAny.form(l_room, 'One Room'))
        l_xml = self.m_api.write_one_room(l_room)
        # print(PrettyFormatAny.form(l_xml, 'One Room'))
        self.assertEqual(l_xml.attrib['Name'], TESTING_ROOM_NAME_0)
        self.assertEqual(l_xml.attrib['Key'], TESTING_ROOM_KEY_0)
        self.assertEqual(l_xml.attrib['Active'], TESTING_ROOM_ACTIVE_0)
        self.assertEqual(l_xml[0].text, TESTING_ROOM_UUID_0)
        self.assertEqual(l_xml[1].text, TESTING_ROOM_COMMENT_0)
        self.assertEqual(l_xml[2].text, TESTING_ROOM_CORNER_0)
        self.assertEqual(l_xml[3].text, TESTING_ROOM_FLOOR_0)
        self.assertEqual(l_xml[4].text, TESTING_ROOM_SIZE_0)
        self.assertEqual(l_xml[5].text, TESTING_ROOM_TYPE_0)

    def test_2_AllRooms(self):
        """ Write out the XML file for the location section
        """
        l_rooms = self.m_api.read_rooms_xml(self.m_xml.house_div)
        l_xml = self.m_api.write_rooms_xml(l_rooms)
        # print(PrettyFormatAny.form(l_xml, 'All Room'))
        self.assertEqual(l_xml[0].attrib['Name'], TESTING_ROOM_NAME_0)
        self.assertEqual(l_xml[1].attrib['Name'], TESTING_ROOM_NAME_1)
        self.assertEqual(l_xml[2].attrib['Name'], TESTING_ROOM_NAME_2)
        self.assertEqual(l_xml[3].attrib['Name'], TESTING_ROOM_NAME_3)


class C1_Coords(SetupMixin, unittest.TestCase):

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))

    def test_1_Corner(self):
        """
        """
        l_ret = roomsMaint._get_coords(JSON['Corner'])
        print(PrettyFormatAny.form(l_ret, 'C1-1 B - Corner'))
        self.assertEqual(l_ret.X_Easting, float(1))
        self.assertEqual(l_ret.Y_Northing, float(2))
        self.assertEqual(l_ret.Z_Height, float(3))

    def test_2_Size(self):
        """
        """
        l_ret = roomsMaint._get_coords(JSON['Size'])
        print(PrettyFormatAny.form(l_ret, 'Size'))


class E1_Json(SetupMixin, unittest.TestCase):

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))

    def test_1_CreateJson(self):
        """ Create a JSON object for Rooms.
        """
        self.m_pyhouse_obj.House.Rooms = l_rooms = self.m_api.read_rooms_xml(self.m_xml.house_div)
        l_json = json_tools.encode_json(l_rooms)
        print(PrettyFormatAny.form(l_json, 'JSON'))

# ## END DBK
