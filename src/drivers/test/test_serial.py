'''
Created on May 4, 2013

@author: briank
'''

from twisted.trial import unittest
from drivers import Driver_Serial
from lights import lighting_controllers


class Test(unittest.TestCase):

    def setUp(self):
        self.m_controller_obj = lighting_controllers.ControllerData()
        self.m_controller_obj.Name = 'Test Name'
        self.m_controller_obj.Port = '/dev/ttyUSB0'
        print 'Set up controller_obj'

    def tearDown(self):
        pass

    def zest_001_API_init(self):
        l_api = Driver_Serial.API()
        self.assertNotEqual(l_api, None)

    def test_002_API_Start(self):
        self.m_controller_obj.DriverAPI = Driver_Serial.API()
        self.m_controller_obj.DriverAPI.Start(self.m_controller_obj)
        print self.m_controller_obj

# ## END
