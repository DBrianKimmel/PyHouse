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
import datetime

#  Import PyMh files
from Modules.Core.data_objects import RoomData, CoordinateData
from Modules.Utilities.coordinate_tools import Coords
from Modules.Utilities.xml_tools import PutGetXML, XmlConfigTools
from Modules.Computer import logging_pyh as Logger

LOG = Logger.getLogger('PyHouse.Rooms          ')


class Xml(object):

    @staticmethod
    def read_one_room(p_room_element):
        l_room_obj = RoomData()
        XmlConfigTools.read_base_object_xml(l_room_obj, p_room_element)
        l_room_obj.Comment = PutGetXML.get_text_from_xml(p_room_element, 'Comment')
        l_room_obj.Corner = PutGetXML.get_coords_from_xml(p_room_element, 'Corner')
        l_room_obj.Floor = PutGetXML.get_text_from_xml(p_room_element, 'Floor', '1')
        l_room_obj.Size = PutGetXML.get_coords_from_xml(p_room_element, 'Size')
        l_room_obj.RoomType = PutGetXML.get_text_from_xml(p_room_element, 'RoomType')
        return l_room_obj

    @staticmethod
    def write_one_room(p_room_object):
        l_entry = XmlConfigTools.write_base_object_xml('Room', p_room_object)
        PutGetXML.put_text_element(l_entry, 'Comment', p_room_object.Comment)
        PutGetXML.put_coords_element(l_entry, 'Corner', p_room_object.Corner)
        PutGetXML.put_text_element(l_entry, 'Floor', p_room_object.Floor)
        PutGetXML.put_coords_element(l_entry, 'Size', p_room_object.Size)
        PutGetXML.put_text_element(l_entry, 'RoomType', p_room_object.RoomType)
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
                LOG.info('Loaded room {}'.format(l_room_obj.Name))
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


class Maint(object):
    """ Maintain the room internal database.
    """

    @staticmethod
    def _extract_json(p_json):
        l_obj = RoomData()
        l_obj.Name = p_json['Name']
        l_obj.Active = p_json['Active']
        l_obj.Key = 0
        l_obj.UUID = p_json['UUID']
        l_obj.Comment = p_json['Comment']
        l_obj.Corner = Coords._get_coords(p_json['Corner'])
        l_obj.Floor = p_json['Floor']
        l_obj.Size = Coords._get_coords(p_json['Size'])
        l_obj.RoomType = p_json['RoomType']
        return l_obj

    def from_web(self, p_pyhouse_obj, p_json):
        LOG.warn('Room debug {}'.format(p_json))
        l_delete = p_json['Delete']
        if l_delete:
            self._delete_room(p_pyhouse_obj, p_json)
        else:
            l_rooms = self._add_room(p_pyhouse_obj, p_json)
            p_pyhouse_obj.House.Rooms = l_rooms

    def _add_room(self, p_pyhouse_obj, p_json):
        l_rooms = p_pyhouse_obj.House.Rooms
        l_len = len(l_rooms)
        l_obj = Maint._extract_json(p_json)
        for l_key, l_val in l_rooms.iteritems():
            if l_val.UUID == l_obj.UUID:
                LOG.info('Updating room {}'.format(l_obj.Name))
                l_rooms[l_key] = l_val
                l_rooms[l_key].LastUpda = datetime.datetime.now()
                return
        l_msg = 'Adding room {} {}'.format(l_obj.Name, l_obj.Key)
        l_obj.Key = l_len
        l_obj.LastUpdate = datetime.datetime.now()
        l_rooms[len(l_rooms)] = l_obj
        print l_msg
        LOG.info(l_msg)
        p_pyhouse_obj.House.Rooms = l_rooms
        # p_pyhouse_obj.APIs.Computer.MqttAPI.MqttPublish("room/add", l_obj)
        return l_rooms

    def _delete_room(self, p_pyhouse_obj, p_json):
        l_room_ix = int(p_json['Key'])
        try:
            del p_pyhouse_obj.House.Rooms[l_room_ix]
        except AttributeError:
            LOG.error("web_rooms - Failed to delete - JSON: {}".format(p_json))
        p_pyhouse_obj.APIs.Computer.MqttAPI.MqttPublish("room/delete", p_json)
        return

#  ## END DBK
