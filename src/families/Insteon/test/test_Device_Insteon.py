'''
Created on Apr 8, 2013

@author: briank
'''

from twisted.trial import unittest

from families.Insteon import Device_Insteon


class ControllerData(object):

    def __init__(self):
        self.Active = True
        self.Name = 'Test Controller 1'

class HouseData(object):

    def __init__(self):
        self.Active = True
        self.Name = 'Test House'
        self.Controllers = {}
        #[0] = ControllerData()


class Test(unittest.TestCase):

    def setUp(self):
        self.api = Device_Insteon.API()
        self.house_obj = HouseData()

    def tearDown(self):
        pass

    def test_start(self):
        self.todo = True
        result = self.api.Start(self.house_obj)
        self.assertEqual(result, None)

### END
