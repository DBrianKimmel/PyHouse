'''
Created on Jun 29, 2013

@author: briank
'''

# Import system type stuff
import xml.etree.ElementTree as ET
from twisted.trial import unittest

# Import PyMh files and modules.
from Modules.Core.data_objects import PyHouseData, HouseData, RoomData
from Modules.web import web_utils
from Modules.housing import rooms
from src.test import xml_data
from Modules.utils.xml_tools import PrettifyXML
from Modules.utils.tools import PrettyPrintAny


PY_DATA = [ { 'a123': u'A', 'b': (2, 4), 'c': 3.0 }, 'def D E F' ]
JS_DATA = '{' + '}'


class Attribs(object):
    def_attr = 'Hello World!'

class Test_01_Json(unittest.TestCase):

    def setUp(self):
        self.c_attr = Attribs()
        self.m_pyhouse_obj = PyHouseData()
        self.m_pyhouse_obj.HouseData = HouseData()
        self.m_pyhouse_obj.XmlRoot = self.m_root_xml = ET.fromstring(xml_data.XML_LONG)
        self.m_houses_xml = self.m_root_xml.find('Houses')
        self.m_house_xml = self.m_houses_xml.find('House')  # First house
        self.m_rooms_xml = self.m_house_xml.find('Rooms')
        self.m_room_xml = self.m_rooms_xml.find('Room')  # First room
        self.m_house_obj = HouseData()
        self.m_room_obj = RoomData()
        self.m_api = rooms.ReadWriteConfig()

    def tearDown(self):
        pass

    def test_0101_encode(self):
        y = web_utils.JsonUnicode().convert_to_unicode('abc')
        self.assertEquals(y, u'abc', "Convert to unicode failed.")

    def test_0102_dencode(self):
        y = web_utils.JsonUnicode().convert_from_unicode(u'ABC')
        self.assertEquals(y, 'ABC', "Convert from unicode failed.")

    def test_0103_json_encode(self):
        x = PY_DATA
        y = web_utils.JsonUnicode().encode_json(x)

    def test_0104_json_decode(self):
        x = "{'de4' : 'D E F'}"
        y = web_utils.JsonUnicode().decode_json(x)

    def test_0111_Room(self):
        l_rooms = self.m_api.read_one_room(self.m_room_xml)
        PrettyPrintAny(l_rooms, 'Room')
        l_json = unicode(web_utils.JsonUnicode().encode_json(l_rooms))
        PrettyPrintAny(l_json, 'JSON')
        print('JSON: {0:}'.format(l_json))

    def test_0112_Rooms(self):
        l_rooms = self.m_api.read_rooms_xml(self.m_house_xml)
        PrettyPrintAny(l_rooms, 'Rooms')
        l_json = unicode(web_utils.JsonUnicode().encode_json(l_rooms))
        PrettyPrintAny(l_json, 'JSON')
        print('JSON: {0:}'.format(l_json))

# ## END DBK
