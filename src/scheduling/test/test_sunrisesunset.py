'''
Created on Apr 7, 2013

@author: briank
'''

import datetime
from twisted.trial import unittest

from src.scheduling import sunrisesunset
from src.core.pyhouse_data import PyHouseData


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
        self.pyhouses_obj = PyHouseData()
        self.house_obj = self.pyhouses_obj.HousesData.HouseObject[0]
        self.api = sunrisesunset.API(self.house_obj)
        # Pink Poppy Fall
        # self.now = datetime.date(2013, 11, 22)
        # self.sunrise = datetime.time(7, 00, 41)
        # self.sunset = datetime.time(17, 34, 52)
        # Pink Poppy Summer
        self.now = datetime.date(2013, 6, 6)
        self.sunrise = datetime.time(6, 32, 30)
        self.sunset = datetime.time(20, 27, 59)
        print("Setup...")

    def tearDown(self):
        print("TearDown...")

    def test_001_name(self):
        print('     Name: {0:}'.format(self.pyhouses_obj.HousesData.HouseObject[0].Name))
        print(' Latitude: {0:}'.format(self.pyhouses_obj.HousesData.HouseObject[0].Location.Latitude))
        print('Longitude: {0:}'.format(self.house_obj.Location.Longitude))
        print('     Time: {0:}'.format(self.now))
        # print('  {0:}'.format(self.pyhouses_obj.HousesData.HouseObject[0].__dict__))

    def test_002_start(self):
        self.api.Start(self.house_obj)

    def test_010_julian(self):
        print("Test 010 Julian")
        print("House {0:}".format(self.house_obj))
        l_start = self.api.Start(self.house_obj, self.now)
        print("Now:{0:}".format(self.now))
        print("  API {0:}".format(self.api))
        l_j2000 = self.api.get_j_2000()
        print("J2000 {0:}".format(l_j2000))
        self.assertEqual(l_j2000, 12345)

    def test_301_sunrise(self):
        self.api.Start(self.house_obj, self.now)
        result = self.api.get_sunrise()
        print('  Sunrise: {0:}  {1:}'.format(result, self.sunrise))
        self.assertEqual(result, self.sunrise)

    def test_302_sunset(self):
        self.api.Start(self.house_obj, self.now)
        result = self.api.get_sunset()
        print('   Sunset: {0:}  {1:}'.format(result, self.sunset))
        self.assertEqual(result, self.sunset)

# ## END DBK
