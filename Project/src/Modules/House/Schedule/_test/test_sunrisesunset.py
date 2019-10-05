"""
@name:      Modules/House/Schedule/_test/test_sunrisesunset.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2011-2019 by D. Brian Kimmel
@note:      Created on Mar 6, 2011
@license:   MIT License
@summary:   Calculate the suns location at local noon, then calculate sunrise and sunset for the day.

Passed 7 of 10 tests - DBK - 2019-09-30

"""

__updated__ = '2019-09-30'

# Import system type stuff
import datetime
from twisted.trial import unittest
from math import pi
from ruamel.yaml import YAML

# Import PyMh files
from Modules.House.location import LocationInformation
from Modules.House.Schedule import sunrisesunset
from Modules.House.Schedule.sunrisesunset import lightingUtility as astralUtil
from _test.testing_mixin import SetupPyHouseObj

from Modules.Core.Utilities.debug_tools import PrettyFormatAny

# Conversion constants.
RAD2DEG = 180.0 / pi
DEG2RAD = pi / 180.0

#  http://www.esrl.noaa.gov/gmd/grad/solcalc/sunrise.html
T_DATE_1 = datetime.date(2014, 4, 22)
T_SUNRISE_1 = datetime.datetime(2014, 4, 22, 6, 57, 32)
T_SUNSET_1 = datetime.datetime(2014, 4, 22, 20, 0, 16)

T_DATE_2 = datetime.date(2015, 7, 23)
T_SUNRISE_2 = datetime.datetime(2015, 7, 23, 6, 46, 0)
T_SUNSET_2 = datetime.datetime(2015, 7, 23, 20, 27, 0)

T_DATE_3 = datetime.date(2016, 10, 24)
T_SUNRISE_3 = datetime.datetime(2016, 10, 24, 7, 37, 0)
T_SUNSET_3 = datetime.datetime(2016, 10, 24, 18, 51, 0)

T_DATE_4 = datetime.date(2017, 12, 22)
T_SUNRISE_4 = datetime.datetime(2017, 12, 22, 7, 20, 0)
T_SUNSET_4 = datetime.datetime(2017, 12, 22, 17, 38, 0)

TEST_YAML = """\
Location:
   Street: 123456789 Some Street
   City: La Angelos
   State: Ga
   ZipCode: 44444
   Country: USA
   Phone: (800) 555-1212
   TimeZone: America/New_York
   Latitude: 29.12345
   Longitude: -82.555555
   Elevation: 345.0
   Date01: 2014-04-22
   Date02: 2015-07-23
   Date03: 2016-10-24
   Date04: 2017-12-27
"""


class LDI:

    def __init__(self):
        self.Date_01 = None
        self.Date_02 = None
        self.Date_03 = None
        self.Date_04 = None


class SetupMixin:
    """
    """

    def setUp(self):
        self.m_pyhouse_obj = SetupPyHouseObj().BuildPyHouseObj()
        l_yaml = YAML()
        self.m_test_config = l_yaml.load(TEST_YAML)['Location']

    def load_earth(self, p_loc):
        l_loc = LocationInformation()
        l_loc.Latitude = p_loc['Latitude']
        l_loc.Longitude = p_loc['Longitude']
        l_loc.TimeZone = p_loc['TimeZone']
        l_loc.Elevation = p_loc['Elevation']
        l_dates = LDI()
        l_dates.Date_01 = p_loc['Date01']
        l_dates.Date_02 = p_loc['Date02']
        l_dates.Date_03 = p_loc['Date03']
        l_dates.Date_04 = p_loc['Date04']
        return l_loc, l_dates


class A0(unittest.TestCase):

    def test_00_Print(self):
        _x = PrettyFormatAny.form('_test', 'title', 190)  # so it is defined when printing is cleaned up.
        print('Id: test_sunrisesunset')


class A1_Setup(SetupMixin, unittest.TestCase):
    """
    """

    def setUp(self):
        SetupMixin.setUp(self)

    def test_01_Earth(self):
        l_loc, l_dates = SetupMixin().load_earth(self.m_test_config)
        # l_loc = self.m_pyhouse_obj.House.Location
        print(PrettyFormatAny.form(l_loc, 'A1-01-A - Loc'))
        print(PrettyFormatAny.form(l_dates, 'A1-01-A - Loc'))
        # print(PrettyFormatAny.form(self.m_test_config.Location, 'A1-01-B - Loc'))
        print('A1-01-C - Dawn', self.m_test_config)
        # self.assertEqual(l_loc.Latitude, float(TESTING_LOCATION_LATITUDE))


class B1_Astral(SetupMixin, unittest.TestCase):

    def setUp(self):
        SetupMixin.setUp(self)
        self.m_api = sunrisesunset.API(self.m_pyhouse_obj)
        l_loc, l_dates = SetupMixin().load_earth(self.m_test_config)
        self.m_pyhouse_obj.House.Location = l_loc

    def test_01_Date_0(self):
        l_ret = astralUtil().calc_solar_times(self.m_pyhouse_obj)
        print('B1-01-A - Dawn', l_ret.Dawn)
        print('B1-01-B - Sun Rise', l_ret.SunRise)
        print('B1-01-C - Noon', l_ret.Noon)
        print('B1-01-D - Sun Set', l_ret.SunSet)
        print('B1-01-E - Dusk', l_ret.Dusk)
        # self.assertEqual(l_ret.Dawn.hour, TESTING_SCHEDULE_DAWN_0.hour)
        # self.assertApproximates(l_ret.Dawn.minute, TESTING_SCHEDULE_DAWN_0.minute, 1)
        # self.assertEqual(l_ret.SunRise.hour, TESTING_SCHEDULE_SUNRISE_0.hour)
        # self.assertApproximates(l_ret.SunRise.minute, TESTING_SCHEDULE_SUNRISE_0.minute, 1)
        # self.assertEqual(l_ret.Noon.hour, TESTING_SCHEDULE_NOON_0.hour)
        # self.assertApproximates(l_ret.Noon.minute, TESTING_SCHEDULE_NOON_0.minute, 1)
        # self.assertEqual(l_ret.SunSet.hour, TESTING_SCHEDULE_SUNSET_0.hour)
        # self.assertApproximates(l_ret.SunSet.minute, TESTING_SCHEDULE_SUNSET_0.minute, 1)
        # self.assertEqual(l_ret.Dusk.hour, TESTING_SCHEDULE_DUSK_0.hour)
        # self.assertApproximates(l_ret.Dusk.minute, TESTING_SCHEDULE_DUSK_0.minute, 1)

    def test_02_Loc(self):
        l_ret = astralUtil().calc_solar_times(self.m_pyhouse_obj, T_DATE_1)
        print('B1-02-A - Sun Rise', l_ret.SunRise)
        print('B1-02-B - Sun Set', l_ret.SunSet)
        self.assertEqual(l_ret.SunRise.hour, T_SUNRISE_1.hour)
        self.assertApproximates(l_ret.SunRise.minute, T_SUNRISE_1.minute, 1)
        self.assertEqual(l_ret.SunSet.hour, T_SUNSET_1.hour)
        self.assertApproximates(l_ret.SunSet.minute, T_SUNSET_1.minute, 1)

    def test_03_Loc(self):
        l_ret = astralUtil().calc_solar_times(self.m_pyhouse_obj, T_DATE_2)
        print('B1-03-A - Sun Rise', l_ret.SunRise)
        print('B1-03-B - Sun Set', l_ret.SunSet)
        self.assertEqual(l_ret.SunRise.hour, T_SUNRISE_2.hour)
        self.assertApproximates(l_ret.SunRise.minute, T_SUNRISE_2.minute, 1)
        self.assertEqual(l_ret.SunSet.hour, T_SUNSET_2.hour)
        self.assertApproximates(l_ret.SunSet.minute, T_SUNSET_2.minute, 1)

    def test_04_Loc(self):
        l_ret = astralUtil().calc_solar_times(self.m_pyhouse_obj, T_DATE_3)
        print('B1-04-A - Sun Rise', l_ret.SunRise)
        print('B1-04-B - Sun Set', l_ret.SunSet)
        self.assertEqual(l_ret.SunRise.hour, T_SUNRISE_3.hour)
        self.assertApproximates(l_ret.SunRise.minute, T_SUNRISE_3.minute, 1)
        self.assertEqual(l_ret.SunSet.hour, T_SUNSET_3.hour)
        self.assertApproximates(l_ret.SunSet.minute, T_SUNSET_3.minute, 1)

    def test_05_Loc(self):
        """ Nearly the shortest day of the year.
        Also, Standard time.
        """
        l_ret = astralUtil().calc_solar_times(self.m_pyhouse_obj, T_DATE_4)
        print('Sun Rise', l_ret.SunRise)
        print('Sun Set', l_ret.SunSet)
        self.assertEqual(l_ret.SunRise.hour, T_SUNRISE_4.hour)
        self.assertApproximates(l_ret.SunRise.minute, T_SUNRISE_4.minute, 1)
        self.assertEqual(l_ret.SunSet.hour, T_SUNSET_4.hour)
        self.assertApproximates(l_ret.SunSet.minute, T_SUNSET_4.minute, 1)


class C1_Delay(SetupMixin, unittest.TestCase):
    """
    """

    def setUp(self):
        SetupMixin.setUp(self)
        l_loc, l_dates = SetupMixin().load_earth(self.m_test_config)
        self.m_pyhouse_obj.House.Location = l_loc
        self.m_api = sunrisesunset.API(self.m_pyhouse_obj)

    def test_01_Loc(self):
        l_delay = astralUtil()._till_next()
        print(PrettyFormatAny.form(l_delay, 'Next'))

    def test_02(self):
        pass


class D1_Now(SetupMixin, unittest.TestCase):
    """
    """

    def setUp(self):
        SetupMixin.setUp(self)
        l_loc, l_dates = SetupMixin().load_earth(self.m_test_config)
        self.m_pyhouse_obj.House.Location = l_loc
        self.m_api = sunrisesunset.API(self.m_pyhouse_obj)

    def test_01_Loc(self):
        l_now = astralUtil().get_seconds_to_recalc()
        print(PrettyFormatAny.form(l_now, 'Next'))

# ## END DBK
