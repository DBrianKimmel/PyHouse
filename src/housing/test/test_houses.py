'''
Created on Apr 8, 2013

@author: briank
'''

from twisted.trial import unittest

from housing import houses


class Test(unittest.TestCase):


    def setUp(self):
        self.api = houses.API()

    def tearDown(self):
        pass

    def test_singleton(self):
        self.api2 = houses.API()
        self.assertEqual(self.api, self.api2, 'Not a singleton.')

    def test_start(self):
        self.api.Start()

### END
