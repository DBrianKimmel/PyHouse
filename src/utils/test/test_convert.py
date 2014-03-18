'''
Created on Apr 4, 2013

@author: briank
'''
from twisted.trial import unittest

from utils.convert import ConvertEthernet


class Test(unittest.TestCase):


    def setUp(self):
        self.eth = ConvertEthernet()

    def _test(self, oper, a, r):
        result = oper(a)
        self.assertEqual(result, r)

    def test_ethernet_2dotted(self):
        self._test(self.eth.dotted_quad2long, '192.168.1.65', 3232235841L)

    def test_ethernet_2long(self):
        self._test(self.eth.long2dotted_quad, 3232235841L, '192.168.1.65')

# ## END
