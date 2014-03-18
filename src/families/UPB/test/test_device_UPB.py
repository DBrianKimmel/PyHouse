"""
Created on Apr 8, 2013

@author: briank
"""

from twisted.trial import unittest

from families.UPB import Device_UPB



class Test(unittest.TestCase):

    def setUp(self):
        self.api = Device_UPB.API()

    def tearDown(self):
        pass

    def test_load_device(self):
        result = self.api.load_device(p_dict, p_dev)
        self.assertEqual(result, 0)

    def test_controllers(self):
        pass

    def test_lights(self):
        pass

    def test_buttons(self):
        pass

# ## END DBK
