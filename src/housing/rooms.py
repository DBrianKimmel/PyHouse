"""
-*- test-case-name: PyHouse.src.housing.test.test_rooms -*-

@name: PyHouse/src/housing/rooms.py
@author: D. Brian Kimmel
@contact: <d.briankimmel@gmail.com
@Copyright (c) 2013-2014 by D. Brian Kimmel
@license: MIT License
@note: Created on Apr 10, 2013
@summary: Handle the rooms information for a house.
"""

# Import system type stuff
import xml.etree.ElementTree as ET

# Import PyMh files
from src.utils import xml_tools
from src.core.data_objects import RoomData


g_debug = 0
# 0 = off
# 1 = log extra info
# + = NOT USED HERE
m_logger = None


class ReadWriteConfig(xml_tools.ConfigTools):

    def read_xml(self, p_house_obj, p_house_xml):
        l_count = 0
        l_rooms_xml = p_house_xml.find('Rooms')
        for l_room_xml in l_rooms_xml.iterfind('Room'):
            l_room_obj = RoomData()
            self.xml_read_common_info(l_room_obj, l_room_xml)
            l_room_obj.UUID = self.get_uuid_from_xml(l_room_xml, 'UUID')
            l_room_obj.Key = l_count  # Renumber
            l_room_obj.Comment = self.get_text_from_xml(l_room_xml, 'Comment')
            l_room_obj.Corner = self.get_text_from_xml(l_room_xml, 'Corner')
            l_room_obj.Size = self.get_text_from_xml(l_room_xml, 'Size')
            p_house_obj.Rooms[l_count] = l_room_obj
            l_count += 1
        return p_house_obj.Rooms

    def write_rooms_xml(self, p_house_obj):
        l_count = 0
        l_rooms_xml = ET.Element('Rooms')
        for l_room_obj in p_house_obj.Rooms.itervalues():
            l_entry = self.xml_create_common_element('Room', l_room_obj)
            self.put_text_element(l_entry, 'UUID', l_room_obj.UUID)
            self.put_text_element(l_entry, 'Comment', l_room_obj.Comment)
            self.put_text_element(l_entry, 'Corner', l_room_obj.Corner)
            self.put_text_element(l_entry, 'Size', l_room_obj.Size)
            l_rooms_xml.append(l_entry)
            l_count += 1
        return l_rooms_xml

# ## END DBK
