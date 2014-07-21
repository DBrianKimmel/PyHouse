"""
@name: PyHouse/src/Modules/Core/node_local.py

# -*- test-case-name: PyHouse.Modules.Core.test.test_node_local -*-

Created on Apr 8, 2013

@author: D. Brian Kimmel
@contact: <d.briankimmel@gmail.com
@copyright: 2013-2014 by D. Brian Kimmel
@license: MIT License

@summary: Test the UPB controller.

"""

# Import system type stuff
from twisted.trial import unittest
import xml.etree.ElementTree as ET

# Import PyMh files and modules.
from Modules.families.UPB import UPB_Pim
from test import xml_data
from Modules.Core.data_objects import PyHouseData, HouseObjs, ControllerData
from Modules.utils.tools import PrintBytes, PrettyPrintAny

XML = xml_data.XML_LONG
CHG_REG_CMD = b'\x70\x03'


class Test_01_Utils(unittest.TestCase):

    def setUp(self):
        self.m_api = UPB_Pim.BuildCommand()
        self.m_controller_obj = ControllerData()

    def test_0101_Nibble2Hex(self):
        l_hex = self.m_api._nibble_to_hex(0x00)
        self.assertEqual(l_hex, 0x30)
        l_hex = self.m_api._nibble_to_hex(0x07)
        self.assertEqual(l_hex, 0x37)
        l_hex = self.m_api._nibble_to_hex(0x0A)
        self.assertEqual(l_hex, 0x41)
        l_hex = self.m_api._nibble_to_hex(0x0F)
        self.assertEqual(l_hex, 0x46)

    def test_0102_Byte2Hex(self):
        l_str = self.m_api._byte_to_2chars(0x00)
        self.assertEqual(l_str, b'\x30\x30')
        l_str = self.m_api._byte_to_2chars(0x08)
        self.assertEqual(l_str, '08')
        l_str = self.m_api._byte_to_2chars(0x0F)
        self.assertEqual(l_str, '0F')
        l_str = self.m_api._byte_to_2chars(0x80)
        self.assertEqual(l_str, '80')
        l_str = self.m_api._byte_to_2chars(0x77)
        self.assertEqual(l_str, '77')
        l_str = self.m_api._byte_to_2chars(0xff)
        self.assertEqual(l_str, 'FF')

    def test_0103_Checksum(self):
        l_ba = self.m_api._calculate_checksum(CHG_REG_CMD)
        self.assertEqual(l_ba, b'\x70\x03\x8D')
        print('W/ Checksum {0:}'.format(PrintBytes(l_ba)))
        l_ba = self.m_api._calculate_checksum(b'\x35\x23\x24')
        self.assertEqual(l_ba, b'\x35\x23\x24\x84')
        print('W/ Checksum {0:}'.format(PrintBytes(l_ba)))

    def test_0104_Register(self):
        l_cmd = self.m_api._calculate_checksum(CHG_REG_CMD)
        l_ba = self.m_api.change_register_command(self.m_controller_obj, l_cmd)

# ## END DBK
