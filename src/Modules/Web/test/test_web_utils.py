"""
@name:      PyHouse/src/Modules/web/test/test_web_clock.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com>
@copyright: (c) 2014-2015 by D. Brian Kimmel
@license:   MIT License
@note:      Created on Jun 29, 2013
@Summary:   Test web utilities module

Passed all 12 tests - DBK - 2015-08-02

"""

# Import system type stuff
import xml.etree.ElementTree as ET
from twisted.trial import unittest
import jsonpickle

# Import PyMh files and modules.
from Modules.Web import web_utils
from Modules.Housing.rooms import Xml as roomsXML
from test.xml_data import XML_LONG
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


class A1_EncodeDecode(SetupMixin, unittest.TestCase):

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))

    def test_01_Encode(self):
        y = web_utils.JsonUnicode().convert_to_unicode('abc')
        # PrettyPrintAny(y, 'ABC')
        self.assertEquals(y, u'abc')

    def test_02_Decode(self):
        y = web_utils.JsonUnicode().convert_from_unicode(u'ABC')
        # PrettyPrintAny(y, 'ABC')
        self.assertEquals(y, 'ABC', "Convert from unicode failed.")


class C01_Json(SetupMixin, unittest.TestCase):

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))

    def test_01_Json_Encode(self):
        x = PY_DATA
        y = web_utils.JsonUnicode().encode_json(x)
        # PrettyPrintAny(y, 'PY_DATA')

    def test_11_Json_Decode(self):
        x = '{"de4" : "D E F"}'
        y = web_utils.JsonUnicode().decode_json(x)
        # PrettyPrintAny(y, 'Def')
        self.assertNotEqual(y, None)

    def test_12_Json_Decode(self):
        x = '[{"de4" : "D E F"}]'
        y = web_utils.JsonUnicode().decode_json(x)
        # PrettyPrintAny(y, 'Def')
        self.assertNotEqual(y, None)

    def test_13_Json_Decode(self):
        """
        Expect this to fail and return None (missing ']')
        """
        x = '[{"de4" : "D E F"}'
        y = web_utils.JsonUnicode().decode_json(x)
        # PrettyPrintAny(y, 'Def')
        self.assertEqual(y, None)


class C02_Rooms(SetupMixin, unittest.TestCase):

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))
        self.m_api = roomsXML()

    def test_01_Room(self):
        l_rooms = self.m_api.read_one_room(self.m_xml.room)
        # PrettyPrintAny(l_rooms, 'Room')
        l_json = unicode(web_utils.JsonUnicode().encode_json(l_rooms))
        # PrettyPrintAny(l_json, 'JSON')

    def test_02_Rooms(self):
        l_rooms = self.m_api.read_rooms_xml(self.m_xml.house_div)
        # PrettyPrintAny(l_rooms, 'Rooms')
        l_json = unicode(web_utils.JsonUnicode().encode_json(l_rooms))
        # PrettyPrintAny(l_json, 'JSON')


class C03_House(SetupMixin, unittest.TestCase):

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))

    def test_01_Before(self):
        # PrettyPrintAny(self.m_pyhouse_obj.House, 'PyHouse.House Before')
        # PrettyPrintAny(self.m_pyhouse_obj.House.RefOBJs, 'PyHouse.House.RefOBJs Before')
        pass

    def test_02_Base(self):
        l_data = web_utils.UtilJson._getHouseBase(self.m_pyhouse_obj)
        # PrettyPrintAny(l_data, 'Base House')

    def test_03_LocRoom(self):
        l_data = web_utils.UtilJson._getHouseBase(self.m_pyhouse_obj)
        web_utils.UtilJson._get_LocRoom(self.m_pyhouse_obj, l_data)
        # PrettyPrintAny(l_data, 'Base House')

    def test_04_Modules(self):
        l_data = web_utils.UtilJson._getHouseBase(self.m_pyhouse_obj)
        web_utils.UtilJson._get_LocRoom(self.m_pyhouse_obj, l_data)
        web_utils.UtilJson._get_Modules(self.m_pyhouse_obj, l_data)
        # PrettyPrintAny(l_data, 'House')

    def test_05_All(self):
        l_data = web_utils.UtilJson._get_AllHouseObjs(self.m_pyhouse_obj)
        # PrettyPrintAny(l_data, 'House')


class C04_Json(SetupMixin, unittest.TestCase):

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))

    def test_01_HouseInfo(self):
        l_json = web_utils.GetJSONHouseInfo(self.m_pyhouse_obj)
        l_obj = jsonpickle.decode(l_json)
        PrettyPrintAny(l_json, 'JSON', 60)
        PrettyPrintAny(l_obj, 'Decoded', 60)
        self.assertEquals(l_obj['Name'], 'Test House')
        self.assertEquals(l_obj['Key'], 0)
        self.assertEquals(l_obj['Active'], True)
        self.assertEquals(l_obj['Controllers'], {})

    def test_02_ComputerInfo(self):
        l_json = web_utils.GetJSONComputerInfo(self.m_pyhouse_obj)
        l_obj = jsonpickle.decode(l_json)
        PrettyPrintAny(l_json, 'JSON', 60)
        PrettyPrintAny(l_obj, 'Decoded', 60)

# ## END DBK
