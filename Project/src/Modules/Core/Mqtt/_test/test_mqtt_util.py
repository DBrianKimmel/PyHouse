"""
@name:      Modules/Core/Mqtt/_test/test_mqtt_util.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2017-2019 by D. Brian Kimmel
@license:   MIT License
@note:      Created on Mar 31, 2017
@summary:   Test

Passed all 9 tests - DBK - 2019-08-15

"""
__updated__ = '2019-08-15'

# Import system type stuff
from twisted.trial import unittest

# Import PyMh files
from _test.testing_mixin import SetupPyHouseObj
from Modules.Core.Mqtt import mqtt_util
from Modules.Core.Utilities.debug_tools import PrettyFormatAny


class SetupMixin(object):

    def setUp(self):
        self.m_pyhouse_obj = SetupPyHouseObj().BuildPyHouseObj()


class A0(unittest.TestCase):

    def test_00_Print(self):
        _x = PrettyFormatAny.form('_test', 'title', 190)  # so it is defined when printing is cleaned up.
        print('Id: test_mqtt_util')


class C1_Encode(SetupMixin, unittest.TestCase):
    """
    """

    def setUp(self):
        SetupMixin.setUp(self)
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
        SetupMixin.setUp(self)
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
        SetupMixin.setUp(self)
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
