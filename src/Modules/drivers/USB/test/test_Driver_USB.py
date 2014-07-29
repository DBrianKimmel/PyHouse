"""
@name: PyHouse/src/Modules/drivers/test/test_Driver_USB.py
@author: briank
@contact: <d.briankimmel@gmail.com>
@Copyright: (c)  2014 by briank
@license: MIT License
@note: Created on Jul 22, 2014
@Summary:

"""
# Import system type stuff
from twisted.trial import unittest

# Import PyMh files and modules.
from Modules.drivers import Driver_USB
from test import xml_data
from Modules.Core.data_objects import ControllerData
from Modules.utils.tools import PrintBytes  # , PrettyPrintAny

RAW_01 = bytearray(b'\xF7\x50\x45\x0d\x45\x0d\x50\x45')
RAW_02 = bytearray(b'\xF4\x0D\x50\x45\x0d\x00\x00\x00')
RAW_03 = bytearray(b'\xF0\x00\x00\x00\x00\x00\x00\x00')
RAW_04 = bytearray(0)

class Test_01(unittest.TestCase):

    def setUp(self):
        self.m_api = Driver_USB.API()
        pass

    def test_0101_Extract(self):
        l_ba = self.m_api._extract_hid_report(RAW_01)
        print('Test_0101 A ', PrintBytes(l_ba))
        self.assertEqual(l_ba, b'\x50\x45\x0d\x45\x0d\x50\x45')
        self.assertEqual(type(l_ba), bytearray)
        l_ba = self.m_api._extract_hid_report(RAW_02)
        print('Test_0101 B ', PrintBytes(l_ba))
        self.assertEqual(l_ba, b'\x0D\x50\x45\x0d')
        l_ba = self.m_api._extract_hid_report(RAW_03)
        print('Test_0101 C ', PrintBytes(l_ba))
        self.assertEqual(l_ba, b'')
        l_ba = self.m_api._extract_hid_report(RAW_04)
        print('Test_0101 D ', PrintBytes(l_ba))
        self.assertEqual(l_ba, b'')

# ## END DBK
