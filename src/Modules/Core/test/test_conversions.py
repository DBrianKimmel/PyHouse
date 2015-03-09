"""
@name: PyHouse/src/Modules/Core/test/test_conversions.py
@author: briank
@contact: D.BrianKimmel@gmail.com>
@Copyright: (c)  2014 by briank
@license: MIT License
@note: Created on Jul 14, 2014
@Summary:


Tests all working OK - DBK 2014-07-114
"""

# Import system type stuff
from twisted.trial import unittest

# Import PyMh files and modules.
from Modules.Core import conversions
from test import xml_data

XML = xml_data.XML_LONG

ADDR_DR_SLAVE_MSG = bytearray(b'\x16\xc9\xd0')
ADDR_DR_SLAVE_DOT = '16.C9.D0'
ADDR_DR_SLAVE_INT = 1493456

ADDR_NOOK_MSG = bytearray(b'\x17\xc2\x72')
ADDR_NOOK_DOT = '17.C2.72'
ADDR_NOOK_INT = 1557106

MSG_50 = bytearray(b'\x02\x50\x16\xc9\xd0\x1b\x47\x81\x27\x09\x00')
MSG_62 = bytearray(b'\x02\x62\x17\xc2\x72\x0f\x19\x00\x06')


class Test_01_Cvrt(unittest.TestCase):


    def setUp(self):
        self.inst = conversions
        pass

    def _test(self, oper, p_args, r):
        l_result = oper(p_args)
        self.assertEqual(l_result, r)

    def test_0101_GetFactor(self):
        self.assertEqual(self.inst._get_factor(1), 0)
        self.assertEqual(self.inst._get_factor(2), 256)
        self.assertEqual(self.inst._get_factor(3), 256 * 256)
        self.assertEqual(self.inst._get_factor(4), 256 * 256 * 256)
        self.assertEqual(self.inst._get_factor(-1), 0)

    def test_0102_int2dotted(self):
        l_res = self.inst.int2dotted_hex(10597059, 3)
        self.assertEqual(l_res, 'A1.B2.C3')
        l_res = self.inst.int2dotted_hex(ADDR_DR_SLAVE_INT, 3)
        self.assertEqual(l_res, ADDR_DR_SLAVE_DOT)
        l_res = self.inst.int2dotted_hex(ADDR_NOOK_INT, 3)
        self.assertEqual(l_res, ADDR_NOOK_DOT)
        l_res = self.inst.int2dotted_hex(41394, 2)
        self.assertEqual(l_res, 'A1.B2')

    def test_0103_dotted2int(self):
        self._test(self.inst.dotted_hex2int, 'A1.B2.C3', 10597059)
        self._test(self.inst.dotted_hex2int, ADDR_DR_SLAVE_DOT, ADDR_DR_SLAVE_INT)
        self._test(self.inst.dotted_hex2int, ADDR_NOOK_DOT, ADDR_NOOK_INT)
        self._test(self.inst.dotted_hex2int, 'A1.B2', 41394)
        self._test(self.inst.dotted_hex2int, 'A1.B2.C3', 10597059)

    def test_0110_GetFactor(self):
        self._test(self.inst.dotted_hex2int, 'A1.oB2.C3', 10551491)
        self._test(self.inst.dotted_hex2int, 'A1.0.C3', 10551491)

        pass

# ## END DBL
