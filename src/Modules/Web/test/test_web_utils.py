"""
@name: PyHouse/src/Modules/web/test/test_web_clock.py
@author: briank
@contact: D.BrianKimmel@gmail.com>
@Copyright: (c)  2014 by briank
@license: MIT License
@note: Created on Jun 29, 2013
@Summary:  Test web utilities module

"""

# Import system type stuff
import xml.etree.ElementTree as ET
from twisted.trial import unittest

# Import PyMh files and modules.
from Modules.Core.data_objects import PyHouseData, HouseObjs, RoomData
from Modules.Web import web_utils
from Modules.Housing import rooms
from test import xml_data
from test.testing_mixin import SetupPyHouseObj
from Modules.Utilities.tools import PrettyPrintAny


PY_DATA = [ { 'a123': u'A', 'b': (2, 4), 'c': 3.0 }, 'def D E F' ]
JS_DATA = '{' + '}'


class SetupMixin(object):

    def setUp(self, p_root):
        self.m_pyhouse_obj = SetupPyHouseObj().BuildPyHouseObj(p_root)
        self.m_xml = SetupPyHouseObj().BuildXml(p_root)


class Attribs(object):
    def_attr = 'Hello World!'


class Test_01_Json(SetupMixin, unittest.TestCase):

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(xml_data.XML_LONG))
        self.m_house_obj = HouseObjs()
        self.m_room_obj = RoomData()
        self.m_api = rooms.ReadWriteConfigXml()

    def test_0101_encode(self):
        y = web_utils.JsonUnicode().convert_to_unicode('abc')
        PrettyPrintAny(y, 'Y')
        self.assertEquals(y, u'abc', "Convert to unicode failed.")

    def test_0102_dencode(self):
        y = web_utils.JsonUnicode().convert_from_unicode(u'ABC')
        PrettyPrintAny(y, 'Y')
        self.assertEquals(y, 'ABC', "Convert from unicode failed.")

    def test_0103_json_encode(self):
        x = PY_DATA
        y = web_utils.JsonUnicode().encode_json(x)
        PrettyPrintAny(y, 'Y')

    def test_0104_json_decode(self):
        x = "{'de4' : 'D E F'}"
        y = web_utils.JsonUnicode().decode_json(x)
        PrettyPrintAny(y, 'Y')

    def test_0111_Room(self):
        l_rooms = self.m_api.read_one_room(self.m_xml.room)
        PrettyPrintAny(l_rooms, 'Room')
        l_json = unicode(web_utils.JsonUnicode().encode_json(l_rooms))
        PrettyPrintAny(l_json, 'JSON')

    def test_0112_Rooms(self):
        l_rooms = self.m_api.read_rooms_xml(self.m_xml.house_div)
        PrettyPrintAny(l_rooms, 'Rooms')
        l_json = unicode(web_utils.JsonUnicode().encode_json(l_rooms))
        PrettyPrintAny(l_json, 'JSON')

# ## END DBK
