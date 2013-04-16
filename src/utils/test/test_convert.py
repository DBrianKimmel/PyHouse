'''
Created on Apr 4, 2013

@author: briank
'''
from twisted.trial import unittest

from utils.convert import ConvertEthernet, ConvertInsteon


class Test(unittest.TestCase):


    def setUp(self):
        self.eth = ConvertEthernet()
        self.inst = ConvertInsteon()

    def _test(self, oper, a, r):
        result = oper(a)
        self.assertEqual(result, r)

    def test_ethernet_2dotted(self):
        self._test(self.eth.dotted_quad2long, '192.168.1.65', 3232235841L)

    def test_ethernet_2long(self):
        self._test(self.eth.long2dotted_quad, 3232235841L, '192.168.1.65')

    def test_insteon_2dotted(self):
        self._test(self.inst.long2dotted_hex, 10597059L, 'A1.B2.C3')

    def test_insteon_2long(self):
        self._test(self.inst.dotted_hex2long, 'A1.B2.C3', 10597059L)


if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    # unittest.main()
    pass
