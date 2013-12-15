'''
Created on Apr 7, 2013

@author: briank
'''

import datetime
from twisted.trial import unittest

from scheduling import sunrisesunset


class LocationObj():

    def __init__(self):
        self.Latitude = 28.938448
        self.Longitude = -82.517208
        self.TimeZone = '-5:00'
        self.SavingTime = '-4:00'


class HouseObj(object):

    def __init__(self):
        self.Active = True
        self.Name = 'Test House (Pink Poppy)'
        self.Location = LocationObj()


class Test(unittest.TestCase):

    def setUp(self):
        self.house_obj = HouseObj()
        self.api = sunrisesunset.API(self.house_obj)
        # Pink Poppy Fall
        # self.now = datetime.date(2013, 11, 22)
        # self.sunrise = datetime.time(7, 00, 41)
        # self.sunset = datetime.time(17, 34, 52)
        # Pink Poppy Summer
        self.now = datetime.date(2013, 6, 6)
        self.sunrise = datetime.time(6, 32, 30)
        self.sunset = datetime.time(20, 27, 59)

    def tearDown(self):
        pass

    def test_001_name(self):
        print '     Name:', self.house_obj.Name
        print ' Latitude:', self.house_obj.Location.Latitude
        print 'Longitude:', self.house_obj.Location.Longitude
        print '     Time:', self.now

    def test_002_start(self):
        self.api.Start(self.house_obj)

    def test_011_sunrise(self):
        self.api.Start(self.house_obj, self.now)
        result = self.api.get_sunrise()
        print 'result', result, self.sunrise
        self.assertEqual(result, self.sunrise)

    def test_022_sunset(self):
        self.api.Start(self.house_obj, self.now)
        result = self.api.get_sunset()
        self.assertEqual(result, self.sunset)

# ## END
