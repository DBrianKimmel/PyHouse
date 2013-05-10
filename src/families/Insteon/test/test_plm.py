'''
Created on Apr 5, 2013

@author: briank
'''
from twisted.trial import unittest

from families.Insteon.Insteon_PLM import API
from families.Insteon.Insteon_constants import *

ADDR_NOOK = bytearray(b'\x17\xc2\x72')
ADDR_DR_SLAVE = bytearray(b'\x16\xc9\xd0')
ADDR_NOOK_DOT = '17.C2.72'
ADDR_DR_SLAVE_DOT = '16.C9.D0'
MSG_50 = bytearray(b'\x02\x50\x16\xc9\xd0\x1b\x47\x81\x27\x09\x00')
MSG_62 = bytearray(b'\x02\x62\x17\xc2\x72\x0f\x19\x00\x06')

class Test(unittest.TestCase):

    def setUp(self):
        self.api = API()


    def tearDown(self):
        pass


    def test_001_get_message_length(self):
        self.assertEqual(self.api._get_message_length(0x50), 11)
        self.assertEqual(self.api._get_message_length(0x62), 9)
        self.assertEqual(self.api._get_message_length(0x99), 1)

    def test_002_extract_address(self):
        self.assertEqual(self.api._get_addr_from_message(MSG_50, 2), ADDR_DR_SLAVE_DOT)
        self.assertEqual(self.api._get_addr_from_message(MSG_62, 2), ADDR_NOOK_DOT)

    def test_003_queue_command(self):
        l_ret_1 = self.api._queue_command('insteon_send')
        self.assertEqual(len(l_ret_1), 8)
        self.assertEqual(l_ret_1[0], STX)

# ## END
