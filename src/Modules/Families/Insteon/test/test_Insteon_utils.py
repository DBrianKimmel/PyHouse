"""
@name: PyHouse/src/Modules/families/Insteon/test/test_Insteon_utils.py
@author: D. Brian Kimmel
@contact: <d.briankimmel@gmail.com
@Copyright (c) 2013-2014 by D. Brian Kimmel
@license: MIT License
@note: Created on Apr 27, 2013
@summary: This module is for testing Insteon conversion routines.


Tests all working OK - DBK 2014-05-22
"""

# Import system type stuff
from twisted.trial import unittest

# Import PyMh files and modules.
from Modules.Families.Insteon import Insteon_utils
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


class Test_01_Conversions(unittest.TestCase):


    def setUp(self):
        self.inst = Insteon_utils
        pass

    def _test(self, oper, p_args, r):
        l_result = oper(p_args)
        self.assertEqual(l_result, r)

    def test_0110_message2int(self):
        result = self.inst.message2int(MSG_50, 2)
        self.assertEqual(result, ADDR_DR_SLAVE_INT)
        result = self.inst.message2int(MSG_62, 2)
        self.assertEqual(result, ADDR_NOOK_INT)

    def test_0111_int2message(self):
        l_msg = bytearray(11)
        l_msg[:] = MSG_50
        result = self.inst.int2message(ADDR_DR_SLAVE_INT, l_msg, 2)
        self.assertEqual(result, MSG_50)
        l_msg = bytearray(9)
        l_msg[:] = MSG_62
        result = self.inst.int2message(ADDR_NOOK_INT, l_msg, 2)
        self.assertEqual(result, MSG_62)

def suite():
    l_suite = unittest.TestSuite()
    l_suite.addTest(Test_01_Conversions('test_0110_message2int'))
    return l_suite

# ## END
