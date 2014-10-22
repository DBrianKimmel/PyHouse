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


class C01_Json(SetupMixin, unittest.TestCase):

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(xml_data.XML_LONG))
        self.m_house_obj = HouseObjs()
        self.m_room_obj = RoomData()
        self.m_api = rooms.ReadWriteConfigXml()

    def test_01_Encode(self):
        y = web_utils.JsonUnicode().convert_to_unicode('abc')
        PrettyPrintAny(y, 'Y')
        self.assertEquals(y, u'abc', "Convert to unicode failed.")

    def test_02_Decode(self):
        y = web_utils.JsonUnicode().convert_from_unicode(u'ABC')
        PrettyPrintAny(y, 'Y')
        self.assertEquals(y, 'ABC', "Convert from unicode failed.")

    def test_03_Json_Encode(self):
        x = PY_DATA
        y = web_utils.JsonUnicode().encode_json(x)
        PrettyPrintAny(y, 'Y')

    def test_04_Json_Decode(self):
        x = "{'de4' : 'D E F'}"
        y = web_utils.JsonUnicode().decode_json(x)
        PrettyPrintAny(y, 'Y')

    def test_11_Room(self):
        l_rooms = self.m_api.read_one_room(self.m_xml.room)
        PrettyPrintAny(l_rooms, 'Room')
        l_json = unicode(web_utils.JsonUnicode().encode_json(l_rooms))
        PrettyPrintAny(l_json, 'JSON')

    def test_12_Rooms(self):
        l_rooms = self.m_api.read_rooms_xml(self.m_xml.house_div)
        PrettyPrintAny(l_rooms, 'Rooms')
        l_json = unicode(web_utils.JsonUnicode().encode_json(l_rooms))
        PrettyPrintAny(l_json, 'JSON')



class C02_Json(SetupMixin, unittest.TestCase):

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(xml_data.XML_LONG))
        self.m_house_obj = HouseObjs()
        self.m_room_obj = RoomData()
        self.m_api = rooms.ReadWriteConfigXml()

    def test_01_HouseInfo(self):
        l_json = web_utils.GetJSONHouseInfo(self.m_pyhouse_obj)
        PrettyPrintAny(l_json, 'JSON', 60)
        # self.assertEquals(l_json.Name, u'Test House')


# ## END DBK
