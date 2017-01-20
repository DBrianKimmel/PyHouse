"""
@name:      PyHouse/src/Modules/Drivers/USB/test/test_USB_driver.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com>
@copyright: (c) 2014-2017 by briank
@license:   MIT License
@note:      Created on Jul 22, 2014
@Summary:

Passed all 1 tests - DBK - 2015-08-15

"""

__updated__ = '2017-01-20'


# Import system type stuff
from twisted.trial import unittest

# Import PyMh files and modules.
from Modules.Drivers.USB import USB_driver

from test.xml_data import XML_LONG
from test.testing_mixin import SetupPyHouseObj

RAW_01 = bytearray(b'\xF7\x50\x45\x0d\x45\x0d\x50\x45')
RAW_02 = bytearray(b'\xF4\x0D\x50\x45\x0d\x00\x00\x00')
RAW_03 = bytearray(b'\xF0\x00\x00\x00\x00\x00\x00\x00')
RAW_04 = bytearray(0)


class SetupMixin(object):
    """
    """

    def setUp(self, p_root):
        self.m_pyhouse_obj = SetupPyHouseObj().BuildPyHouseObj(p_root)
        self.m_xml = SetupPyHouseObj().BuildXml(p_root)
        self.m_version = '1.4.0'


class A01_API(SetupMixin, unittest.TestCase):
    """
    """

class B1(unittest.TestCase):

    def setUp(self):
        self.m_api = USB_driver.API()
        pass

    def test_01_Extract(self):
        l_ba = self.m_api._extract_hid_report(RAW_01)
        # print('Test_0101 A ', PrintBytes(l_ba))
        self.assertEqual(l_ba, b'\x50\x45\x0d\x45\x0d\x50\x45')
        self.assertEqual(type(l_ba), bytearray)
        l_ba = self.m_api._extract_hid_report(RAW_02)
        # print('Test_0101 B ', PrintBytes(l_ba))
        self.assertEqual(l_ba, b'\x0D\x50\x45\x0d')
        l_ba = self.m_api._extract_hid_report(RAW_03)
        # print('Test_0101 C ', PrintBytes(l_ba))
        self.assertEqual(l_ba, b'')
        l_ba = self.m_api._extract_hid_report(RAW_04)
        # print('Test_0101 D ', PrintBytes(l_ba))
        self.assertEqual(l_ba, b'')

# ## END DBK
