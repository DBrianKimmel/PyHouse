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
from Modules.Core.data_objects import HouseObjs, RoomData
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
        self.m_api = rooms.ReadWriteConfigXml()


    def test_01_Encode(self):
        y = web_utils.JsonUnicode().convert_to_unicode('abc')
        PrettyPrintAny(y, 'ABC')
        self.assertEquals(y, u'abc', "Convert to unicode failed.")


    def test_02_Decode(self):
        y = web_utils.JsonUnicode().convert_from_unicode(u'ABC')
        PrettyPrintAny(y, 'ABC')
        self.assertEquals(y, 'ABC', "Convert from unicode failed.")


    def test_03_Json_Encode(self):
        x = PY_DATA
        y = web_utils.JsonUnicode().encode_json(x)
        PrettyPrintAny(y, 'PY_DATA')


    def test_04_Json_Decode(self):
        x = "{'de4' : 'D E F'}"
        y = web_utils.JsonUnicode().decode_json(x)
        PrettyPrintAny(y, 'Def')



class C02_Rooms(SetupMixin, unittest.TestCase):

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(xml_data.XML_LONG))
        self.m_api = rooms.ReadWriteConfigXml()


    def test_01_Room(self):
        l_rooms = self.m_api.read_one_room(self.m_xml.room)
        PrettyPrintAny(l_rooms, 'Room')
        l_json = unicode(web_utils.JsonUnicode().encode_json(l_rooms))
        PrettyPrintAny(l_json, 'JSON')


    def test_02_Rooms(self):
        l_rooms = self.m_api.read_rooms_xml(self.m_xml.house_div)
        PrettyPrintAny(l_rooms, 'Rooms')
        l_json = unicode(web_utils.JsonUnicode().encode_json(l_rooms))
        PrettyPrintAny(l_json, 'JSON')



class C03_House(SetupMixin, unittest.TestCase):

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(xml_data.XML_LONG))
        self.m_api = rooms.ReadWriteConfigXml()


    def test_01_Before(self):
        PrettyPrintAny(self.m_pyhouse_obj.House, 'PyHouse.House Before')
        PrettyPrintAny(self.m_pyhouse_obj.House.OBJs, 'PyHouse.House.OBJs Before')
        pass

    def test_02_Base(self):
        l_data = web_utils.UtilJson._getHouseBase(self.m_pyhouse_obj)
        PrettyPrintAny(l_data, 'Base House')


    def test_03_LocRoom(self):
        l_data = web_utils.UtilJson._getHouseBase(self.m_pyhouse_obj)
        web_utils.UtilJson._get_LocRoom(self.m_pyhouse_obj, l_data)
        PrettyPrintAny(l_data, 'Base House')


    def test_04_Modules(self):
        l_data = web_utils.UtilJson._getHouseBase(self.m_pyhouse_obj)
        web_utils.UtilJson._get_LocRoom(self.m_pyhouse_obj, l_data)
        web_utils.UtilJson._get_Modules(self.m_pyhouse_obj, l_data)
        PrettyPrintAny(l_data, 'House')


    def test_05_All(self):
        l_data = web_utils.UtilJson._get_AllHouseObjs(self.m_pyhouse_obj)
        PrettyPrintAny(l_data, 'House')



class C04_Json(SetupMixin, unittest.TestCase):

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(xml_data.XML_LONG))
        self.m_api = rooms.ReadWriteConfigXml()


    def test_01_HouseInfo(self):
        l_json = web_utils.GetJSONHouseInfo(self.m_pyhouse_obj)
        PrettyPrintAny(l_json, 'JSON', 60)
        # self.assertEquals(l_json.Name, u'Test House')

# ## END DBK
