'''
Created on Apr 7, 2013

@author: briank
'''

import datetime
from twisted.trial import unittest

from scheduling import sunrisesunset


class LocationObj():

    def __init__(self):
        self.Latitude = 29.0
        self.Longitude = -74.0
        self.TimeZone = 300


class HouseObj(object):

    def __init__(self):
        self.Active = True
        self.Name = 'Test House'
        self.Location = LocationObj()


class Test(unittest.TestCase):

    def setUp(self):
        self.house_obj = HouseObj()
        self.api = sunrisesunset.API(self.house_obj)
        self.now = datetime.date(2013, 6, 1)
        self.sunrise = datetime.time(5, 59, 3)
        self.sunset = datetime.time(19, 51, 39)

    def tearDown(self):
        pass

    def testName(self):
        pass

    def test_start(self):
        self.api.Start(self.house_obj)

    def test_sunrise(self):
        self.api.Start(self.house_obj, self.now)
        result = self.api.get_sunrise()
        self.assertEqual(result, self.sunrise)

    def test_sunset(self):
        self.api.Start(self.house_obj, self.now)
        result = self.api.get_sunset()
        self.assertEqual(result, self.sunset)

### END
