"""
@name:      PyHouse/src/Modules/Computer/Web/test/test_web_utils.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com>
@copyright: (c) 2014-2017 by D. Brian Kimmel
@license:   MIT License
@note:      Created on Jun 29, 2013
@Summary:   Test web utilities module

Passed all 7 tests - DBK - 2017-01-12

"""

__updated__ = '2017-01-19'

# Import system type stuff
import xml.etree.ElementTree as ET
from twisted.trial import unittest
import jsonpickle

# Import PyMh files and modules.
from test.xml_data import XML_LONG
from test.testing_mixin import SetupPyHouseObj
from Modules.Computer.Web import web_utils
from Modules.Housing.rooms import Xml as roomsXML
from Modules.Core.Utilities import json_tools
from Modules.Housing.test.xml_housing import \
    TESTING_HOUSE_NAME, \
    TESTING_HOUSE_KEY, \
    TESTING_HOUSE_ACTIVE
from Modules.Core.Utilities.debug_tools import PrettyFormatAny

PY_DATA = [ { 'a123': u'A', 'b': (2, 4), 'c': 3.0 }, 'def D E F' ]
JS_DATA = '{' + '}'


class SetupMixin(object):

    def setUp(self, p_root):
        self.m_pyhouse_obj = SetupPyHouseObj().BuildPyHouseObj(p_root)
        self.m_xml = SetupPyHouseObj().BuildXml(p_root)

    def jsonPair(self, p_json, p_key):
        """ Extract key, value from json
        """
        l_json = json_tools.decode_json_unicode(p_json)
        try:
            l_val = l_json[p_key]
        except (KeyError, ValueError) as e_err:
            l_val = 'ERRor on JsonPair for key "{}"  {} {}'.format(p_key, e_err, l_json)
            print(l_val)
        return l_val


class Attribs(object):
    def_attr = 'Hello World!'


class A0(unittest.TestCase):
    def setUp(self):
        pass
    def test_00_Print(self):
        print('Id: test_web_utils')


class C1_Rooms(SetupMixin, unittest.TestCase):

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))
        self.m_api = roomsXML()

    def test_01_Room(self):
        l_rooms = self.m_api.read_rooms_xml(self.m_pyhouse_obj)
        l_json = unicode(json_tools.encode_json(l_rooms))
        # print(PrettyFormatAny.form(l_json, 'C1-01-A - Decode'))
        # self.assertEqual(self.jsonPair(l_json, 0), l_rooms)

    def test_02_Rooms(self):
        l_rooms = self.m_api.read_rooms_xml(self.m_pyhouse_obj)
        l_json = unicode(json_tools.encode_json(l_rooms))
        # print(PrettyFormatAny.form(l_json, 'C1-02-A - Decode'))


class C2_House(SetupMixin, unittest.TestCase):

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))

    def test_01_Before(self):
        l_house = self.m_pyhouse_obj.House
        # print(PrettyFormatAny.form(l_house, 'C2-01-A - House'))
        l_house2 = {}


class D1_Json(SetupMixin, unittest.TestCase):

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))

    def test_01_HouseInfo(self):
        l_json = web_utils.GetJSONHouseInfo(self.m_pyhouse_obj)
        l_obj = jsonpickle.decode(l_json)
        # print(PrettyFormatAny.form(l_obj, 'D1-01-A - House'))
        self.assertEquals(l_obj['Name'], TESTING_HOUSE_NAME)
        self.assertEquals(l_obj['Key'], TESTING_HOUSE_KEY)
        self.assertEquals(l_obj['Active'], TESTING_HOUSE_ACTIVE)
        self.assertEquals(l_obj['Controllers'], {})

    def test_02_ComputerInfo(self):
        l_json = web_utils.GetJSONComputerInfo(self.m_pyhouse_obj)
        _l_obj = jsonpickle.decode(l_json)


class E1_Json(SetupMixin, unittest.TestCase):

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))

    def test_01_RoomInfo(self):
        l_json = web_utils.GetJSONHouseInfo(self.m_pyhouse_obj)
        l_obj = jsonpickle.decode(l_json)
        # print(PrettyFormatAny.form(l_obj, 'E1-01-A - Decode'))

# ## END DBK
