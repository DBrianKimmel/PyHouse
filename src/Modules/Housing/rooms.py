"""
-*- test-case-name: PyHouse.src.Modules.Housing.test.test_rooms -*-

@name:      PyHouse/src/Modules/Housing/rooms.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2013-2016 by D. Brian Kimmel
@license:   MIT License
@note:      Created on Apr 10, 2013
@summary:   Handle the rooms information for a house.

"""

#  Import system type stuff
import xml.etree.ElementTree as ET

#  Import PyMh files
from Modules.Core.data_objects import RoomData
from Modules.Utilities.xml_tools import PutGetXML, XmlConfigTools
from Modules.Computer import logging_pyh as Logger

LOG = Logger.getLogger('PyHouse.Rooms          ')


class Xml(object):

    @staticmethod
    def read_one_room(p_room_element):
        l_room_obj = RoomData()
        XmlConfigTools.read_base_object_xml(l_room_obj, p_room_element)
        l_room_obj.Comment = PutGetXML.get_text_from_xml(p_room_element, 'Comment')
        l_room_obj.Corner = PutGetXML.get_text_from_xml(p_room_element, 'Corner')
        l_room_obj.Floor = PutGetXML.get_text_from_xml(p_room_element, 'Floor', '1')
        l_room_obj.Size = PutGetXML.get_text_from_xml(p_room_element, 'Size')
        return l_room_obj

    @staticmethod
    def write_one_room(p_room_object):
        l_entry = XmlConfigTools.write_base_object_xml('Room', p_room_object)
        PutGetXML.put_text_element(l_entry, 'Comment', p_room_object.Comment)
        PutGetXML.put_text_element(l_entry, 'Corner', p_room_object.Corner)
        PutGetXML.put_text_element(l_entry, 'Floor', p_room_object.Floor)
        PutGetXML.put_text_element(l_entry, 'Size', p_room_object.Size)
        return l_entry

    @staticmethod
    def read_rooms_xml(p_house_xml):
        """
        @param p_house_obj: is
        @param p_house_xml: is
        """
        l_ret = {}
        l_count = 0
        try:
            l_xml = p_house_xml.find('RoomSection')
            if l_xml is None:
                return l_ret
            for l_room_xml in l_xml.iterfind('Room'):
                l_room_obj = Xml.read_one_room(l_room_xml)
                l_room_obj.Key = l_count
                l_ret[l_count] = l_room_obj
                l_count += 1
        except AttributeError as e_err:
            LOG.error('ERROR if getting rooms Data - {}'.format(e_err))
        LOG.info('Loaded {} rooms.'.format(l_count))
        return l_ret

    @staticmethod
    def write_rooms_xml(p_rooms_obj):
        l_rooms_xml = ET.Element('RoomSection')
        l_count = 0
        for l_room_object in p_rooms_obj.itervalues():
            l_room_object.Key = l_count
            l_entry = Xml.write_one_room(l_room_object)
            l_rooms_xml.append(l_entry)
            l_count += 1
        LOG.info('Saved {} Rooms XML'.format(l_count))
        return l_rooms_xml

#  ## END DBK
