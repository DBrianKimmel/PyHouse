"""
@name:      PyHouse/src/Modules/Core/test/test_conversions.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com>
@copyright: (c) 2014-2017 by D. Brian Kimmel
@license:   MIT License
@note:      Created on Jul 14, 2014
@Summary:


All 14 tests working OK - DBK - 2017-4-120
"""

__updated__ = '2017-04-20'


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


class A0(unittest.TestCase):
    def setUp(self):
        pass
    def test_00_Print(self):
        print('Id: test_conversions')


class B1_Hex(unittest.TestCase):
    """
    """

    def setUp(self):
        pass

    def test_01_Hex(self):
        l_int = 1
        l_hex = conversions.makeHex(l_int)
        self.assertEqual(l_hex, '01')

    def test_02_Hex(self):
        l_int = 31
        l_hex = conversions.makeHex(l_int)
        self.assertEqual(l_hex, '1F')

    def test_03_Hex(self):
        l_int = 255
        l_hex = conversions.makeHex(l_int)
        self.assertEqual(l_hex, 'FF')

    def test_04_Hex(self):
        l_int = 168
        l_hex = conversions.makeHex(l_int)
        self.assertEqual(l_hex, 'A8')

    def test_05_Hex(self):
        l_int = 257
        l_hex = conversions.makeHex(l_int)
        self.assertEqual(l_hex, '01')


class B2_Factor(unittest.TestCase):
    """
    """

    def setUp(self):
        pass

    def test_01_F1(self):
        l_int = 1
        l_pow = conversions._get_factor(1)
        self.assertEqual(l_pow, 0)

    def test_02_F2(self):
        l_int = 1
        l_pow = conversions._get_factor(2)
        self.assertEqual(l_pow, 256)

    def test_03_F3(self):
        l_int = 1
        l_pow = conversions._get_factor(3)
        self.assertEqual(l_pow, 256 * 256)


class B3_Cvrt(unittest.TestCase):


    def setUp(self):
        self.inst = conversions
        pass

    def _test(self, oper, p_args, r):
        l_result = oper(p_args)
        self.assertEqual(l_result, r)

    def test_01_GetFactor(self):
        self.assertEqual(self.inst._get_factor(1), 0)
        self.assertEqual(self.inst._get_factor(2), 256)
        self.assertEqual(self.inst._get_factor(3), 256 * 256)
        self.assertEqual(self.inst._get_factor(4), 256 * 256 * 256)
        self.assertEqual(self.inst._get_factor(-1), 0)

    def test_02_int2dotted(self):
        l_res = self.inst.int2dotted_hex(10597059, 3)
        self.assertEqual(l_res, 'A1.B2.C3')

        l_res = self.inst.int2dotted_hex(ADDR_DR_SLAVE_INT, 3)
        self.assertEqual(l_res, ADDR_DR_SLAVE_DOT)

        l_res = self.inst.int2dotted_hex(ADDR_NOOK_INT, 3)
        self.assertEqual(l_res, ADDR_NOOK_DOT)

        l_res = self.inst.int2dotted_hex(41394, 2)
        self.assertEqual(l_res, 'A1.B2')

    def test_03_dotted2int(self):
        self._test(self.inst.dotted_hex2int, 'A1.B2.C3', 10597059)
        self._test(self.inst.dotted_hex2int, ADDR_DR_SLAVE_DOT, ADDR_DR_SLAVE_INT)
        self._test(self.inst.dotted_hex2int, ADDR_NOOK_DOT, ADDR_NOOK_INT)
        self._test(self.inst.dotted_hex2int, 'A1.B2', 41394)
        self._test(self.inst.dotted_hex2int, 'A1.B2.C3', 10597059)

    def test_04_GetFactor(self):
        self._test(self.inst.dotted_hex2int, 'A1.oB2.C3', 10551491)
        self._test(self.inst.dotted_hex2int, 'A1.0.C3', 10551491)

    def test_05_Bool(self):
        self.assertEqual(self.inst.getbool('True'), True)
        self.assertEqual(self.inst.getbool('None'), False)
        self.assertEqual(self.inst.getbool('False'), False)

# ## END DBL
