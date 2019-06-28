"""
@name:      PyHouse/src/Modules.Core.Utilities.test/test_json_tools.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2015-2017 by D. Brian Kimmel
@license:   MIT License
@note:      Created on Jun 25, 2015
@Summary:

Passed all 5 tests - DBK - 2017-01-20

"""
from Modules.Core.Utilities.debug_tools import PrettyFormatAny, PrettyFormatObject

__updated__ = '2019-06-13'

# Import system type stuff
import xml.etree.ElementTree as ET
from twisted.trial import unittest

# Import PyMh files and modules.
from test.xml_data import XML_LONG
from test.testing_mixin import SetupPyHouseObj
from Modules.Core.Utilities  import json_tools

MSG_JSON = bytearray(b'{"Count": 0, \
    "ControllerTypes": [], \
    "Active": true, \
    "NodeId": null, \
    "Name": "briank-Laptop-3", \
    "DateTime": "2017-04-22 10:17:03.678333", \
    "NodeInterfaces": null, \
    "ConnectionAddr_IPv4": [], \
    "LastUpdate": "2017-04-22 10:16:48.676017", \
    "ConnectionAddr_IPv6": [["::1"], ["2604:8800:100:8268:8cca:e089:25e1:897a", "2604:8800:100:8268:2e04:b128:2c5c:ab0b", "fe80::9a42:15f0:6352:7d50%wlo1"]], \
    "Sender": "briank-Laptop-3", \
    "Comment": null, \
    "NodeRole": 0, \
    "UUID": "afd36665-df62-11e6-9b94-74dfbfae5aed", \
    "Key": 0}')
MSG_DICT = {
    "Street": "",
    "TimeZoneName": "America/New_York",
    "Elevation": 0.0,
    "_name": "",
    "Phone": ""}


class SetupMixin(object):

    def setUp(self, p_root):
        self.m_pyhouse_obj = SetupPyHouseObj().BuildPyHouseObj(p_root)
        self.m_xml = SetupPyHouseObj().BuildXml(p_root)


class A0(unittest.TestCase):

    def setUp(self):
        pass

    def test_00_Print(self):
        print('Id: test_json_tools')


class A1_Json(SetupMixin, unittest.TestCase):
    """
    This series tests the complex PutGetXML class methods
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))

    def test_01_Encode(self):
        l_json = json_tools.encode_json(MSG_DICT)
        print(PrettyFormatAny.form(l_json, 'A1-01-A - JSON'))
        print(PrettyFormatObject(l_json, 'A1-01-B - JSON'))
        self.assertSubstring('Street', l_json)
        self.assertSubstring('Elevation', l_json)

    def test_02_Decode(self):
        # l_json = json_tools.encode_json(self.m_pyhouse_obj.Computer)
        l_json = json_tools.encode_json(MSG_DICT)
        print(PrettyFormatAny.form(l_json, 'A1-02-A - Encoded Info'))
        l_dict = json_tools.decode_json_unicode(l_json)
        print(l_dict)
        print(PrettyFormatAny.form(l_dict, 'A1-02-B - Decoded Info'))
        # self.assertEqual(l_dict['Name'], self.m_pyhouse_obj.Computer.Name)

    def test_03_ByteArray(self):
        print(PrettyFormatAny.form(MSG_JSON, 'A1-03-A - byte array'))
        l_json = MSG_JSON.decode('utf-8')
        print(PrettyFormatAny.form(l_json, 'A1-03-B - Ascii String', 5000))
        l_dict = json_tools.decode_json_unicode(l_json)
        print(PrettyFormatAny.form(l_dict, 'A1-03-C - Decoded Info'))
        # self.assertEqual(l_dict['Name'], self.m_pyhouse_obj.Computer.Name)


class A2_Decode(SetupMixin, unittest.TestCase):

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))

    def test_01_Unicode(self):
        y = json_tools.convert_from_unicode(u'ABC')
        self.assertEquals(y, 'ABC')

    def test_02_Ascii(self):
        y = json_tools.convert_from_unicode('ABC')
        self.assertEquals(y, 'ABC')

    def test_03_BA(self):
        y = json_tools.convert_from_unicode(MSG_JSON)
        print(PrettyFormatAny.form(y, 'A2-03-A - Decoded Info'))
        print(PrettyFormatObject(y, 'A2-03-A - Decoded Info', suppressdoc=False))
        # self.assertEquals(y, 'ABC')

# ## END DBK
