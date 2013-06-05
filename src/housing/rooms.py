"""
Created on Apr 10, 2013

@author: briank

Handle the rooms information for a house.
"""

# Import system type stuff
import xml.etree.ElementTree as ET

# Import PyMh files
from src.utils import xml_tools

g_debug = 0
m_logger = None


class RoomData(object):

    def __init__(self):
        self.Active = False
        self.Comment = ''
        self.Corner = ''
        self.Key = 0
        self.Name = ''
        self.Size = ''

    def __repr__(self):
        l_ret = ' Room:: '
        l_ret += 'Name:{0:} \t '.format(self.Name)
        l_ret += "Size:{0:} \t ".format(self.Size)
        l_ret += "Corner:{0:}\n".format(self.Corner)
        return l_ret


class ReadWriteConfig(xml_tools.ConfigTools):

    def read_rooms(self, p_house_obj, p_house_xml):
        l_count = 0
        l_rooms_xml = p_house_xml.find('Rooms')
        l_list = l_rooms_xml.iterfind('Room')
        for l_room_xml in l_list:
            l_room_obj = RoomData()
            self.xml_read_common_info(l_room_obj, l_room_xml)
            l_room_obj.Key = l_count
            l_room_obj.Comment = self.get_text_element(l_room_xml, 'Comment')
            l_room_obj.Corner = l_room_xml.findtext('Corner')
            l_room_obj.Size = l_room_xml.findtext('Size')
            p_house_obj.Rooms[l_count] = l_room_obj
            l_count += 1
            if g_debug > 6:
                print "house.read_rooms()   Name:{0:}, Active:{1:}, Key:{2:}".format(l_room_obj.Name, l_room_obj.Active, l_room_obj.Key)
        if g_debug > 4:
            print "house.read_rooms()  loaded {0:} rooms".format(l_count)

    def write_rooms(self, p_rooms_obj):
        l_count = 0
        l_rooms_xml = ET.Element('Rooms')
        for l_room_obj in p_rooms_obj.itervalues():
            l_entry = self.xml_create_common_element('Room', l_room_obj)
            ET.SubElement(l_entry, 'Comment').text = l_room_obj.Comment
            ET.SubElement(l_entry, 'Corner').text = l_room_obj.Corner
            ET.SubElement(l_entry, 'Size').text = l_room_obj.Size
            l_rooms_xml.append(l_entry)
            l_count += 1
        if g_debug > 2:
            print "house.write_rooms() - Wrote {0:} rooms".format(l_count)
        return l_rooms_xml

# ## END DBK