'''
Created on Apr 27, 2013

@author: briank
'''

from twisted.trial import unittest

from Modules.families.Insteon import Insteon_utils

ADDR_DR_SLAVE_MSG = bytearray(b'\x16\xc9\xd0')
ADDR_DR_SLAVE_DOT = '16.C9.D0'
ADDR_DR_SLAVE_INT = 1493456

ADDR_NOOK_MSG = bytearray(b'\x17\xc2\x72')
ADDR_NOOK_DOT = '17.C2.72'
ADDR_NOOK_INT = 1557106

MSG_50 = bytearray(b'\x02\x50\x16\xc9\xd0\x1b\x47\x81\x27\x09\x00')
MSG_62 = bytearray(b'\x02\x62\x17\xc2\x72\x0f\x19\x00\x06')


class Test(unittest.TestCase):


    def setUp(self):
        self.inst = Insteon_utils
        pass

    def tearDown(self):
        pass

    def _test(self, oper, p_args, r):
        l_result = oper(p_args)
        self.assertEqual(l_result, r)

    def test_001_int2dotted(self):
        self._test(self.inst.int2dotted_hex, 10597059, 'A1.B2.C3')
        self._test(self.inst.int2dotted_hex, ADDR_DR_SLAVE_INT, ADDR_DR_SLAVE_DOT)
        self._test(self.inst.int2dotted_hex, ADDR_NOOK_INT, ADDR_NOOK_DOT)

    def test_002_dotted2int(self):
        self._test(self.inst.dotted_hex2int, 'A1.B2.C3', 10597059)
        self._test(self.inst.dotted_hex2int, ADDR_DR_SLAVE_DOT, ADDR_DR_SLAVE_INT)
        self._test(self.inst.dotted_hex2int, ADDR_NOOK_DOT, ADDR_NOOK_INT)

    def test_003_message2int(self):
        result = self.inst.message2int(MSG_50, 2)
        self.assertEqual(result, ADDR_DR_SLAVE_INT)
        result = self.inst.message2int(MSG_62, 2)
        self.assertEqual(result, ADDR_NOOK_INT)

    def test_004_int2message(self):
        l_msg = bytearray(11)
        l_msg[:] = MSG_50
        result = self.inst.int2message(ADDR_DR_SLAVE_INT, l_msg, 2)
        self.assertEqual(result, MSG_50)
        l_msg = bytearray(9)
        l_msg[:] = MSG_62
        result = self.inst.int2message(ADDR_NOOK_INT, l_msg, 2)
        self.assertEqual(result, MSG_62)

# ## END
