"""
@name:      PyHouse/src/Modules/web/test/test_web_clock.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com>
@copyright: (c) 2014-2015 by D. Brian Kimmel
@license:   MIT License
@note:      Created on Jun 29, 2013
@Summary:   Test web utilities module

Passed 14 of 15 tests - DBK - 2015-22-02

"""

# Import system type stuff
import xml.etree.ElementTree as ET
from twisted.trial import unittest
import jsonpickle

# Import PyMh files and modules.
from Modules.Computer.Web import web_utils
from Modules.Housing.rooms import Xml as roomsXML
from test.xml_data import XML_LONG
from test.testing_mixin import SetupPyHouseObj
from Modules.Utilities import json_tools

PY_DATA = [ { 'a123': u'A', 'b': (2, 4), 'c': 3.0 }, 'def D E F' ]
JS_DATA = '{' + '}'


class SetupMixin(object):

    def setUp(self, p_root):
        self.m_pyhouse_obj = SetupPyHouseObj().BuildPyHouseObj(p_root)
        self.m_xml = SetupPyHouseObj().BuildXml(p_root)


class Attribs(object):
    def_attr = 'Hello World!'


class A1_EncodeDecode(SetupMixin, unittest.TestCase):

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))

    def test_01_Encode(self):
        y = web_utils.JsonUnicode().convert_to_unicode('abc')
        self.assertEquals(y, u'abc')

    def test_02_Decode(self):
        y = web_utils.JsonUnicode().convert_from_unicode(u'ABC')
        self.assertEquals(y, 'ABC', "Convert from unicode failed.")


class C01_Json(SetupMixin, unittest.TestCase):

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))

    def test_01_Json_Encode(self):
        x = PY_DATA
        _y = json_tools.encode_json(x)

    def test_11_Json_Decode(self):
        x = '{"de4" : "D E F"}'
        y = web_utils.JsonUnicode().decode_json(x)
        self.assertNotEqual(y, None)

    def test_12_Json_Decode(self):
        x = '[{"de4" : "D E F"}]'
        y = web_utils.JsonUnicode().decode_json(x)
        self.assertNotEqual(y, None)

    def test_13_Json_Decode(self):
        """
        Expect this to fail and return None (missing ']')
        """
        x = '[{"de4" : "D E F"}'
        y = web_utils.JsonUnicode().decode_json(x)
        self.assertEqual(y, None)


class C02_Rooms(SetupMixin, unittest.TestCase):

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))
        self.m_api = roomsXML()

    def test_01_Room(self):
        l_rooms = self.m_api.read_one_room(self.m_xml.room)
        _l_json = unicode(json_tools.encode_json(l_rooms))

    def test_02_Rooms(self):
        l_rooms = self.m_api().read_rooms_xml(self.m_xml.house_div)
        _l_json = unicode(json_tools.encode_json(l_rooms))


class C03_House(SetupMixin, unittest.TestCase):

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))

    def test_01_Before(self):
        pass

    def test_02_Base(self):
        _l_data = web_utils.UtilJson._getHouseBase(self.m_pyhouse_obj)

    def test_03_LocRoom(self):
        l_data = web_utils.UtilJson._getHouseBase(self.m_pyhouse_obj)
        web_utils.UtilJson._get_LocRoom(self.m_pyhouse_obj, l_data)

    def test_04_Modules(self):
        l_data = web_utils.UtilJson._getHouseBase(self.m_pyhouse_obj)
        web_utils.UtilJson._get_LocRoom(self.m_pyhouse_obj, l_data)
        web_utils.UtilJson._get_Modules(self.m_pyhouse_obj, l_data)

    def test_05_All(self):
        _l_data = web_utils.UtilJson._get_AllHouseObjs(self.m_pyhouse_obj)


class C04_Json(SetupMixin, unittest.TestCase):

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))

    def test_01_HouseInfo(self):
        l_json = web_utils.GetJSONHouseInfo(self.m_pyhouse_obj)
        l_obj = jsonpickle.decode(l_json)
        self.assertEquals(l_obj['Name'], 'Test House')
        self.assertEquals(l_obj['Key'], 0)
        self.assertEquals(l_obj['Active'], True)
        self.assertEquals(l_obj['Controllers'], {})

    def test_02_ComputerInfo(self):
        l_json = web_utils.GetJSONComputerInfo(self.m_pyhouse_obj)
        _l_obj = jsonpickle.decode(l_json)

# ## END DBK
