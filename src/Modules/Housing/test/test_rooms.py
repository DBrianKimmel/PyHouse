"""
@name:      PyHouse/src/Housing/test/test_rooms.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2013-2016 by D. Brian Kimmel
@license:   MIT License
@note:      Created on Apr 10, 2013
@summary:   Test handling the rooms information for a house.

Passed all 7 tests - DBK 2016-06-09
"""


# Import system type stuff
import xml.etree.ElementTree as ET
from twisted.trial import unittest

# Import PyMh files
from Modules.Housing import rooms
from test.xml_data import XML_LONG
from test.testing_mixin import SetupPyHouseObj
from Modules.Utilities import json_tools
from Modules.Housing.test.xml_rooms import TESTING_ROOM_NAME_0, TESTING_ROOM_COMMENT_0, TESTING_ROOM_CORNER_0, \
    TESTING_ROOM_SIZE_0, TESTING_ROOM_ACTIVE_0, TESTING_ROOM_KEY_0, TESTING_ROOM_NAME_1
from Modules.Utilities.debug_tools import PrettyFormatAny


class SetupMixin(object):

    def setUp(self, p_root):
        self.m_pyhouse_obj = SetupPyHouseObj().BuildPyHouseObj(p_root)
        self.m_xml = SetupPyHouseObj().BuildXml(p_root)


class A1_XML(SetupMixin, unittest.TestCase):

    def _pyHouses(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))
        self.m_api = rooms.Xml

    def setUp(self):
        self._pyHouses()

    def test_01_BuildObjects(self):
        """ Test to be sure the compound object was built correctly - Rooms is an empty dict.
        """
        self.assertEqual(self.m_pyhouse_obj.House.Rooms, {}, 'No Rooms{}')

    def test_02_FindXml(self):
        """ Be sure that the XML contains the right stuff.
        """
        self.assertEqual(self.m_xml.root.tag, 'PyHouse')
        self.assertEqual(self.m_xml.house_div.tag, 'HouseDivision')
        self.assertEqual(self.m_xml.room_sect.tag, 'RoomSection')
        self.assertEqual(self.m_xml.room.tag, 'Room', 'XML - No Room')

    def test_03_ReadOneRoom(self):
        """ Read in the xml file and fill in the first room's dict
        """
        l_room = self.m_api.read_one_room(self.m_xml.room)
        print(PrettyFormatAny.form(l_room, 'One Room'))
        self.assertEqual(l_room.Name, TESTING_ROOM_NAME_0)
        self.assertEqual(l_room.Key, int(TESTING_ROOM_KEY_0))
        self.assertEqual(l_room.Active, bool(TESTING_ROOM_ACTIVE_0))
        self.assertEqual(l_room.Comment, TESTING_ROOM_COMMENT_0)
        self.assertEqual(l_room.Corner, TESTING_ROOM_CORNER_0)
        self.assertEqual(l_room.Size, TESTING_ROOM_SIZE_0)

    def test_04_ReadAllRoomsXml(self):
        """ Read in the xml file and fill in the rooms dict
        """
        l_rooms = self.m_api.read_rooms_xml(self.m_xml.house_div)
        print(PrettyFormatAny.form(l_rooms, 'All Room'))
        self.assertEqual(l_rooms[0].Name, TESTING_ROOM_NAME_0)
        self.assertEqual(l_rooms[1].Name, TESTING_ROOM_NAME_1)

    def test_05_WriteOneRoomXml(self):
        """ Write out the XML file for the location section
        """
        l_room = self.m_api.read_one_room(self.m_xml.house_div)
        l_xml = self.m_api.write_one_room(l_room)
        print(PrettyFormatAny.form(l_xml, 'One Room'))

    def test_06_WriteAllRoomsXml(self):
        """ Write out the XML file for the location section
        """
        l_rooms = self.m_api.read_rooms_xml(self.m_xml.house_div)
        l_xml = self.m_api.write_rooms_xml(l_rooms)
        print(PrettyFormatAny.form(l_xml, 'All Room'))

    def test_07_CreateJson(self):
        """ Create a JSON object for Rooms.
        """
        self.m_pyhouse_obj.House.Rooms = l_rooms = self.m_api.read_rooms_xml(self.m_xml.house_div)
        l_json = json_tools.encode_json(l_rooms)
        print(PrettyFormatAny.form(l_json, 'JSON'))

# ## END DBK
