"""
@name:      PyHouse/src/Modules/Drivers/USB/_test/test_USB_driver.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com>
@copyright: (c) 2014-2017 by briank
@license:   MIT License
@note:      Created on Jul 22, 2014
@Summary:

Passed all 2 tests - DBK - 2018-02-13

"""

__updated__ = '2019-10-06'

# Import system type stuff
from twisted.trial import unittest
import xml.etree.ElementTree as ET

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


class A0(unittest.TestCase):

    def setUp(self):
        pass

    def test_00_Print(self):
        print('Id: test_USB_driver')


class B1(SetupMixin, unittest.TestCase):

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))
        self.m_api = USB_driver.Api(self.m_pyhouse_obj)

    def test_01_Extract(self):
        l_ba = self.m_api._extract_hid_report(RAW_01)
        # print('Test_0101 A ', FormatBytes(l_ba))
        self.assertEqual(l_ba, b'\x50\x45\x0d\x45\x0d\x50\x45')
        self.assertEqual(type(l_ba), bytearray)
        l_ba = self.m_api._extract_hid_report(RAW_02)
        # print('Test_0101 B ', FormatBytes(l_ba))
        self.assertEqual(l_ba, b'\x0D\x50\x45\x0d')
        l_ba = self.m_api._extract_hid_report(RAW_03)
        # print('Test_0101 C ', FormatBytes(l_ba))
        self.assertEqual(l_ba, b'')
        l_ba = self.m_api._extract_hid_report(RAW_04)
        # print('Test_0101 D ', FormatBytes(l_ba))
        self.assertEqual(l_ba, b'')

# ## END DBK
