'''
Created on Apr 5, 2013

@author: briank
'''
import unittest

from families.Insteon.Insteon_PLM import API

ADDR_NOOK = bytearray(b'\x17 \xc2 \x72')
ADDR_NOOK_DOT = '17.C2.72'
MSG_62 = bytearray(b'\x02 \x62 \x17 \xc2 \x72 \x0f \x19 \x00 \x06')

class Test(unittest.TestCase):

    def setUp(self):
        self.api = API()


    def tearDown(self):
        pass


    def testName(self):
        pass

    def test_extract_address(self):
        result = self.api._get_addr_from_message(MSG_62, 2)
        self.assertEqual(result, ADDR_NOOK_DOT)


if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
