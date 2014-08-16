"""
@name: PyHouse/src/housing/test/test_rooms.py
@author: D. Brian Kimmel
@contact: <d.briankimmel@gmail.com
@Copyright (c) 2013-2014 by D. Brian Kimmel
@license: MIT License
@note: Created on Apr 10, 2013
@summary: Test handling the rooms information for a house.


Tests all working OK - DBK 2014-05-22
"""

# Import system type stuff
import xml.etree.ElementTree as ET
from twisted.trial import unittest

# Import PyMh files
from Modules.Core.data_objects import PyHouseData, RoomData
from Modules.housing import rooms
from Modules.housing import house
from Modules.web import web_utils
from Modules.Core import setup
from test import xml_data
from Modules.utils.tools import PrettyPrintAny


class SetupMixin(object):
    """
    """

    def setUp(self):
        self.m_pyhouse_obj = setup.build_pyhouse_obj(self)
        self.m_pyhouse_obj.Xml.XmlRoot = self.m_root_xml
        self.m_room_obj = RoomData()
        self.m_pyhouse_obj = house.API().update_pyhouse_obj(self.m_pyhouse_obj)
        return self.m_pyhouse_obj


class Test_02_XML(SetupMixin, unittest.TestCase):

    def _pyHouses(self):
        self.m_root_xml = ET.fromstring(xml_data.XML_LONG)
        self.m_pyhouse_obj = SetupMixin.setUp(self)
        house.API().update_pyhouse_obj(self.m_pyhouse_obj)
        self.m_house_div_xml = self.m_root_xml.find('HouseDivision')
        self.m_room_sect_xml = self.m_house_div_xml.find('RoomSection')
        self.m_room_xml = self.m_room_sect_xml.find('Room')
        self.m_room_obj = RoomData()
        self.m_api = rooms.ReadWriteConfigXml()

    def setUp(self):
        self._pyHouses()

    def test_0201_BuildObjects(self):
        """ Test to be sure the compound object was built correctly - Rooms is an empty dict.
        """
        self.assertEqual(self.m_pyhouse_obj.House.OBJs.Rooms, {}, 'No Rooms{}')

    def test_0202_FindXml(self):
        """ Be sure that the XML contains the right stuff.
        """
        self.assertEqual(self.m_root_xml.tag, 'PyHouse', 'Invalid XML - not a PyHouse XML config file')
        self.assertEqual(self.m_house_div_xml.tag, 'HouseDivision', 'XML - No Houses Division')
        self.assertEqual(self.m_room_sect_xml.tag, 'RoomSection', 'XML - No Rooms section')
        self.assertEqual(self.m_room_xml.tag, 'Room', 'XML - No Room')

    def test_0211_ReadOneRoom(self):
        """ Read in the xml file and fill in the first room's dict
        """
        l_room = self.m_api.read_one_room(self.m_room_xml)
        self.assertEqual(l_room.Name, 'Master Bath', 'Bad Name')
        self.assertEqual(l_room.Key, 0, 'Bad Key')
        self.assertEqual(l_room.Active, True, 'Bad Active')
        # self.assertEqual(l_room.UUID, '12341234-1003-11e3-82b3-082e5f8cdfd2', 'Bad UUID')
        self.assertEqual(l_room.Comment, 'Test Comment', 'Bad Comment')
        self.assertEqual(l_room.Corner, '0.50, 10.50', 'Bad Corner')
        self.assertEqual(l_room.Size, '14.00, 13.50', 'Bad Size')
        # print('Room: {0:}'.format(vars(l_room)))

    def test_0212_ReadAllRoomsXml(self):
        """ Read in the xml file and fill in the rooms dict
        """
        l_rooms = self.m_api.read_rooms_xml(self.m_room_xml)
        self.assertEqual(l_rooms[0].Name, 'Test Living Room', 'Bad Room')

    def test_0221_WriteOneRoomXml(self):
        """ Write out the XML file for the location section
        """
        l_room = self.m_api.read_one_room(self.m_house_xml)
        l_xml = self.m_api.write_one_room(l_room)
        PrettyPrintAny(l_xml, 'One Room', 120)


    def test_0222_WriteAllRoomsXml(self):
        """ Write out the XML file for the location section
        """
        l_rooms = self.m_api.read_rooms_xml(self.m_house_xml)
        l_xml = self.m_api.write_rooms_xml(l_rooms)
        PrettyPrintAny(l_xml, 'All Rooms', 120)


    def test_0231_CreateJson(self):
        """ Create a JSON object for Rooms.
        """
        self.m_pyhouse_obj.House.OBJs.Rooms = l_rooms = self.m_api.read_rooms_xml(self.m_house_xml)
        l_json = unicode(web_utils.JsonUnicode().encode_json(l_rooms))
        print('JSON: {0:}'.format(l_json))
        PrettyPrintAny(l_json, 'JSON', 120)

# ## END DBK
