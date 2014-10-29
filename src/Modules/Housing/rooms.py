"""
-*- test-case-name: PyHouse.src.Modules.housing.test.test_rooms -*-

@name: PyHouse/src/Modules/housing/rooms.py
@author: D. Brian Kimmel
@contact: D.BrianKimmel@gmail.com
@Copyright (c) 2013-2014 by D. Brian Kimmel
@license: MIT License
@note: Created on Apr 10, 2013
@summary: Handle the rooms information for a house.

"""

# Import system type stuff
import xml.etree.ElementTree as ET

# Import PyMh files
from Modules.Core.data_objects import RoomData
from Modules.Housing import VALID_FLOORS
from Modules.Utilities import xml_tools

g_debug = 0
m_logger = None



class ReadWriteConfigXml(xml_tools.XmlConfigTools):
    m_count = 0

    def read_one_room(self, p_room_element):
        l_room_obj = RoomData()
        self.read_base_object_xml(l_room_obj, p_room_element)
        l_room_obj.Key = self.m_count  # Renumber
        l_room_obj.Comment = self.get_text_from_xml(p_room_element, 'Comment')
        l_room_obj.Corner = self.get_text_from_xml(p_room_element, 'Corner')
        l_room_obj.Floor = self.get_text_from_xml(p_room_element, 'Floor', '1')
        l_room_obj.Size = self.get_text_from_xml(p_room_element, 'Size')
        return l_room_obj

    def read_rooms_xml(self, p_house_xml):
        """
        @param p_house_obj: is
        @param p_house_xml: is
        """
        l_ret = {}
        try:
            l_rooms_xml = p_house_xml.find('RoomSection')
            self.m_count = 0
            for l_room_xml in l_rooms_xml.iterfind('Room'):
                l_room_obj = self.read_one_room(l_room_xml)
                l_ret[self.m_count] = l_room_obj
                self.m_count += 1
        except AttributeError:
            pass
        return l_ret

    def write_one_room(self, p_room_object):
        l_entry = self.write_base_object_xml('Room', p_room_object)
        # self.put_text_element(l_entry, 'UUID', p_room_object.UUID)
        self.put_text_element(l_entry, 'Comment', p_room_object.Comment)
        self.put_text_element(l_entry, 'Corner', p_room_object.Corner)
        self.put_text_element(l_entry, 'Floor', p_room_object.Floor)
        self.put_text_element(l_entry, 'Size', p_room_object.Size)
        return l_entry


    def write_rooms_xml(self, p_rooms_obj):
        l_rooms_xml = ET.Element('RoomSection')
        self.m_count = 0
        for l_room_object in p_rooms_obj.itervalues():
            l_entry = self.write_one_room(l_room_object)
            l_rooms_xml.append(l_entry)
            self.m_count += 1
        return l_rooms_xml

# ## END DBK
