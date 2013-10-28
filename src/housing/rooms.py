"""
Created on Apr 10, 2013

@author: briank

Handle the rooms information for a house.
"""

# Import system type stuff
import xml.etree.ElementTree as ET
import uuid

# Import PyMh files
from src.utils import xml_tools


g_debug = 0
# 0 = off
# 1 = log extra info
# 2 = major routine entry
# 3 = Config file handling
# + = NOT USED HERE
m_logger = None


class RoomData(object):

    def __init__(self):
        self.Name = ''
        self.Key = 0
        self.Active = False
        self.Comment = ''
        self.Corner = ''
        self.Size = ''
        self.Type = 'Room'
        self.UUID = None

    def __str__(self):
        l_ret = ' Room:: '
        l_ret += 'Name:{0:}, \t '.format(self.Name)
        l_ret += "Size:{0:}, \t ".format(self.Size)
        l_ret += "Corner:{0:}, \t".format(self.Corner)
        l_ret += "UUID:{0:}\n".format(self.UUID)
        return l_ret

    def reprJSON(self):
        l_ret = dict(Name = self.Name, Key = self.Key, Active = self.Active,
                    Comment = self.Comment, Corner = self.Corner, Size = self.Size,
                    Type = self.Type, UUID = self.UUID)
        return l_ret


class ReadWriteConfig(xml_tools.ConfigTools):

    def read_rooms_xml(self, p_house_obj, p_house_xml):
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
