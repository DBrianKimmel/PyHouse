"""
-*- test-case-name: PyHouse.src.Modules.families.Insteon.test.test_Insteon_PLM -*-

@name: PyHouse/src/Modules/families/Insteon/Insteon_PLM.py
@author: D. Brian Kimmel
@contact: <d.briankimmel@gmail.com
@copyright: 2013-2014 by D. Brian Kimmel
@note: Created on Apr 8, 2013
@license: MIT License
@summary: This module is for driving serial devices


"""

# Import system type stuff
import xml.etree.ElementTree as ET
from twisted.trial import unittest

# Import PyMh files
# from Modules.lights.lighting import LightData
from Modules.Core.data_objects import PyHouseData
from Modules.families.Insteon import Insteon_PLM
from src.test import xml_data


ADDR_NOOK = bytearray(b'\x17\xc2\x72')
ADDR_DR_SLAVE = bytearray(b'\x16\xc9\xd0')
ADDR_NOOK_DOT = '17.C2.72'
ADDR_DR_SLAVE_DOT = '16.C9.D0'
MSG_50 = bytearray(b'\x02\x50\x16\xc9\xd0\x1b\x47\x81\x27\x09\x00')
MSG_62 = bytearray(b'\x02\x62\x17\xc2\x72\x0f\x19\x00\x06')
MSG_99 = bytearray(b'No Such Message')
STX = 0x02


class Test_01(unittest.TestCase):

    def setUp(self):
        self.m_pyhouse_obj = PyHouseData()
        self.m_api = Insteon_PLM.API()
        pass

    def test_0101_get_message_length(self):
        self.assertEqual(self.m_api._get_message_length(MSG_50), 11)
        self.assertEqual(self.m_api._get_message_length(MSG_62), 9)

    def test_0102_extract_address(self):
        self.assertEqual(self.m_api._get_addr_from_message(MSG_50, 2), ADDR_DR_SLAVE_DOT)
        self.assertEqual(self.m_api._get_addr_from_message(MSG_62, 2), ADDR_NOOK_DOT)

    def test_0103_queue_command(self):
        l_ret_1 = self.m_api._queue_command('insteon_send')
        self.assertEqual(len(l_ret_1), 8)
        self.assertEqual(l_ret_1[0], STX)


class Test_02(unittest.TestCase):

    def setUp(self):
        self.m_pyhouse_obj = PyHouseData()
        self.m_api = Insteon_PLM. API()
        pass

    def test_0201_get_message_length(self):
        self.assertEqual(self.m_api._get_message_length(MSG_50), 11)
        self.assertEqual(self.m_api._get_message_length(MSG_62), 9)
        self.assertEqual(self.m_api._get_message_length(MSG_99), 1)

    def test_0201_getBytes(self):
        self.assertEqual(self.m_api._extract_bytes_from_message(MSG_50, 5, 3), bytearray(b'x1b\x47\x81'))
# ## END DBK
