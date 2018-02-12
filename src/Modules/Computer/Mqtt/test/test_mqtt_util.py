"""
@name:      /home/briank/workspace/PyHouse/src/Modules/Computer/Mqtt/test/test_mqtt_util.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2017-2018 by D. Brian Kimmel
@license:   MIT License
@note:      Created on Mar 31, 2017
@summary:   Test

Passed all 10 tests - DBK - 2018-02-12

"""
__updated__ = '2018-02-12'

# Import system type stuff
import xml.etree.ElementTree as ET
from twisted.trial import unittest

# Import PyMh files
from test.xml_data import XML_LONG, TESTING_PYHOUSE
from test.testing_mixin import SetupPyHouseObj
from Modules.Computer.Mqtt import mqtt_util
from Modules.Computer.test.xml_computer import TESTING_COMPUTER_DIVISION
from Modules.Computer.Mqtt.test.xml_mqtt import TESTING_MQTT_SECTION, TESTING_MQTT_BROKER
from Modules.Core.Utilities.debug_tools import PrettyFormatAny


class SetupMixin(object):

    def setUp(self, p_root):
        self.m_pyhouse_obj = SetupPyHouseObj().BuildPyHouseObj(p_root)
        self.m_xml = SetupPyHouseObj().BuildXml(p_root)


class A0(unittest.TestCase):

    def setUp(self):
        pass

    def test_00_Print(self):
        print('Id: test_mqtt_util')


class A1_XML(SetupMixin, unittest.TestCase):

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))

    def test_01_Tags(self):
        """ Be sure that the XML contains the right stuff.
        """
        # print(PrettyFormatAny.form(self.m_xml, 'A1-01-A - Tags'))
        self.assertEqual(self.m_xml.root.tag, TESTING_PYHOUSE)
        self.assertEqual(self.m_xml.computer_div.tag, TESTING_COMPUTER_DIVISION)
        self.assertEqual(self.m_xml.mqtt_sect.tag, TESTING_MQTT_SECTION)
        self.assertEqual(self.m_xml.broker.tag, TESTING_MQTT_BROKER)


class C1_Encode(SetupMixin, unittest.TestCase):
    """
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))
        self.m_api = mqtt_util.EncodeDecode()

    def test_01_string(self):
        """
        """
        l_str = 'Abc'
        l_bytearray = self.m_api._encodeString(l_str)
        l_res = str(l_bytearray[2:])
        # print(PrettyFormatAny.form(l_bytearray, 'string'))
        self.assertEqual(l_bytearray[0], 0)
        self.assertEqual(l_bytearray[1], 3)
        self.assertEqual(str(l_bytearray[2:]), l_res)

    def test_02_string(self):
        """
        """
        l_str = u'Abc'
        l_bytearray = self.m_api._encodeString(l_str)
        l_res = str(l_bytearray[2:])
        # print(PrettyFormatAny.form(l_bytearray, 'string'))
        self.assertEqual(l_bytearray[0], 0)
        self.assertEqual(l_bytearray[1], 3)
        self.assertEqual(str(l_bytearray[2:]), l_res)

    def test_03_string(self):
        """
        """
        l_str = "Now is the time for quick brown fox to jump over the lazy dog's back."
        l_bytearray = self.m_api._encodeString(l_str)
        l_res = str(l_bytearray[2:])
        # print(PrettyFormatAny.form(l_bytearray, 'string', 300))
        self.assertEqual(l_bytearray[0], 0)
        self.assertEqual(l_bytearray[1], 69)
        self.assertEqual(str(l_bytearray[2:]), l_res)


class C2_Decode(SetupMixin, unittest.TestCase):
    """
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))
        self.m_api = mqtt_util.EncodeDecode()

    def test_01_string(self):
        """
        """
        l_bytes = bytearray(b'\x00\x03Abc')
        # print(PrettyFormatAny.form(l_bytes, 'C2-01-A - ByteArray'))
        l_str = self.m_api._decodeString(l_bytes)
        # print(PrettyFormatAny.form(l_str, 'C2-01-B - String'))
        self.assertEqual(l_bytes[0], 0)
        self.assertEqual(l_bytes[1], 3)
        self.assertEqual(l_str, 'Abc')


class D1_EncLen(SetupMixin, unittest.TestCase):
    """
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))
        self.m_api = mqtt_util.EncodeDecode()

    def test_01_string(self):
        """
        """
        l_bytes = 127
        l_ba = self.m_api._encodeLength(l_bytes)
        # print(PrettyFormatAny.form(l_ba, 'D1-01-A - string'))
        self.assertEqual(l_ba[0], 127)

    def test_02_string(self):
        """
        """
        l_bytes = 133
        l_ba = self.m_api._encodeLength(l_bytes)
        # print(PrettyFormatAny.form(l_ba, 'D1-02-A - string'))
        self.assertEqual(l_ba[0], 0x85)
        self.assertEqual(l_ba[1], 1)

    def test_03_string(self):
        """
        """
        l_bytes = 732
        l_ba = self.m_api._encodeLength(l_bytes)
        # print(PrettyFormatAny.form(l_ba, 'D1-03-A - string'))
        self.assertEqual(l_ba[0], 220)
        self.assertEqual(l_ba[1], 5)

    def test_04_string(self):
        """
        """
        l_bytes = 88500
        l_ba = self.m_api._encodeLength(l_bytes)
        # print(PrettyFormatAny.form(l_ba, 'D1-04-A - string'))
        self.assertEqual(l_ba[0], 180)
        self.assertEqual(l_ba[1], 179)
        self.assertEqual(l_ba[2], 5)

# ## END DBK
