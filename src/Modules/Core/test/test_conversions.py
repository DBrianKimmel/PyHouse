"""
@name:      PyHouse/src/Modules/Core/test/test_conversions.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com>
@copyright: (c) 2014-2017 by D. Brian Kimmel
@license:   MIT License
@note:      Created on Jul 14, 2014
@Summary:


All 21 tests working OK - DBK - 2017-04-29
"""

__updated__ = '2017-05-05'


# Import system type stuff
from twisted.trial import unittest

# Import PyMh files and modules.
from Modules.Core import conversions
from test.xml_data import XML_LONG


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


class B1_Factor(unittest.TestCase):
    """
    """

    def setUp(self):
        pass

    def test_01_F1(self):
        l_int = 1
        l_pow = conversions._get_factor(l_int)
        # print('B1-01-A - ', l_int, l_pow)
        self.assertEqual(l_pow, 0)

    def test_02_F2(self):
        l_int = 2
        l_pow = conversions._get_factor(l_int)
        # print('B1-02-A - ', l_int, l_pow)
        self.assertEqual(l_pow, 256)

    def test_03_F3(self):
        l_int = 3
        l_pow = conversions._get_factor(l_int)
        # print('B1-03-A - ', l_int, l_pow)
        self.assertEqual(l_pow, 256 * 256)

    def test_04_F4(self):
        l_int = 4
        l_pow = conversions._get_factor(l_int)
        # print('B1-04-A - ', l_int, l_pow)
        self.assertEqual(l_pow, 256 * 256 * 256)


class B2_Int(unittest.TestCase):


    def setUp(self):
        self.inst = conversions
        pass

    def _test(self, oper, p_args, r):
        l_result = oper(p_args)
        self.assertEqual(l_result, r)

    def test_01_int(self):
        l_str = '01'
        l_int = self.inst._get_int(l_str)
        # print('B2-01-A - ', l_str, l_int)
        self.assertEqual(l_int, 1)

    def test_02_int(self):
        l_str = 'Ff'
        l_int = self.inst._get_int(l_str)
        # print('B2-02-A - ', l_str, l_int)
        self.assertEqual(l_int, 255)

    def test_03_int(self):
        l_str = 'a1'
        l_int = self.inst._get_int(l_str)
        # print('B2-03-A - ', l_str, l_int)
        self.assertEqual(l_int, 161)


class B3_Hex(unittest.TestCase):
    """
    """

    def setUp(self):
        pass

    def test_01_Hex(self):
        l_int = 1
        l_hex = conversions._makeHex(l_int)
        # print('B3-01-A - ', l_int, l_hex)
        self.assertEqual(l_hex, '01')

    def test_02_Hex(self):
        l_int = 31
        l_hex = conversions._makeHex(l_int)
        # print('B3-02-A - ', l_int, l_hex)
        self.assertEqual(l_hex, '1F')

    def test_03_Hex(self):
        l_int = 255
        l_hex = conversions._makeHex(l_int)
        # print('B3-03-A - ', l_int, l_hex)
        self.assertEqual(l_hex, 'FF')

    def test_04_Hex(self):
        l_int = 168
        l_hex = conversions._makeHex(l_int)
        # print('B3-04-A - ', l_int, l_hex)
        self.assertEqual(l_hex, 'A8')

    def test_05_Hex(self):
        l_int = 257
        l_hex = conversions._makeHex(l_int)
        # print('B3-05-A - ', l_int, l_hex)
        self.assertEqual(l_hex, '01')


class C1_dh2i(unittest.TestCase):


    def setUp(self):
        self.inst = conversions
        pass

    def test_01_A1(self):
        l_hex = 'A1.B2.C3'
        l_int = conversions.dotted_hex2int(l_hex)
        print('C1-01-A - ', l_hex, l_int)
        self.assertEqual(l_int, 10597059)

    def test_02_A1(self):
        l_hex = 'A1:B2:C3'
        l_int = conversions.dotted_hex2int(l_hex)
        print('C1-02-A - ', l_hex, l_int)
        self.assertEqual(l_int, 10597059)


class C2_i2dh(unittest.TestCase):


    def setUp(self):
        self.inst = conversions
        pass

    def _test(self, oper, p_args, r):
        l_result = oper(p_args)
        self.assertEqual(l_result, r)

    def test_01_A1B2C3(self):
        l_int = 10597059
        l_hex = conversions.int2dotted_hex(l_int, 3)
        print('C2-01-A - ', l_int, l_hex)
        self.assertEqual(l_hex, 'A1.B2.C3')

    def test_02_int2dotted(self):
        l_int = ADDR_DR_SLAVE_INT
        l_hex = self.inst.int2dotted_hex(l_int, 3)
        print('C2-02-A - ', l_int, l_hex)
        self.assertEqual(l_hex, ADDR_DR_SLAVE_DOT)

    def test_03_int2dotted(self):
        l_int = ADDR_NOOK_INT
        l_hex = self.inst.int2dotted_hex(l_int, 3)
        print('C2-03-A - ', l_int, l_hex)
        self.assertEqual(l_hex, ADDR_NOOK_DOT)

    def test_04_A1B2(self):
        l_int = 41394
        l_hex = self.inst.int2dotted_hex(l_int, 2)
        print('C2-04-A - ', l_int, l_hex)
        self.assertEqual(l_hex, 'A1.B2')

    def test_05_GetFactor(self):
        self._test(self.inst.dotted_hex2int, 'A1.oB2.C3', 10551491)
        self._test(self.inst.dotted_hex2int, 'A1.0.C3', 10551491)

    def test_06_Bool(self):
        self.assertEqual(self.inst.getbool('True'), True)
        self.assertEqual(self.inst.getbool('None'), False)
        self.assertEqual(self.inst.getbool('False'), False)

# ## END DBL
