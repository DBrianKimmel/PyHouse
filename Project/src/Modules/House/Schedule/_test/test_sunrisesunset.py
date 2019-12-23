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

__updated__ = '2019-12-19'

# Import system type stuff
import datetime
from twisted.trial import unittest
from math import pi
from ruamel.yaml import YAML

# Import PyMh files
from Modules.House.location import LocationInformation
from Modules.House.Schedule import sunrisesunset
from Modules.House.Schedule.sunrisesunset import lightingUtilitySun as astralUtil
from _test.testing_mixin import SetupPyHouseObj

from Modules.Core.Utilities.debug_tools import PrettyFormatAny

# Conversion constants.
RAD2DEG = 180.0 / pi
DEG2RAD = pi / 180.0

#  http://www.esrl.noaa.gov/gmd/grad/solcalc/sunrise.html
T_DATE_1 = datetime.date(2014, 4, 22)
T_SUNRISE_1 = datetime.datetime(2014, 4, 22, 6, 57, 0)
T_SUNSET_1 = datetime.datetime(2014, 4, 22, 20, 13, 0)

T_DATE_2 = datetime.date(2015, 7, 23)
T_SUNRISE_2 = datetime.datetime(2015, 7, 23, 6, 41, 0)
T_SUNSET_2 = datetime.datetime(2015, 7, 23, 20, 44, 0)

T_DATE_3 = datetime.date(2016, 10, 24)
T_SUNRISE_3 = datetime.datetime(2016, 10, 24, 7, 48, 0)
T_SUNSET_3 = datetime.datetime(2016, 10, 24, 18, 51, 0)

T_DATE_4 = datetime.date(2017, 12, 22)
T_SUNRISE_4 = datetime.datetime(2017, 12, 22, 7, 38, 0)
T_SUNSET_4 = datetime.datetime(2017, 12, 22, 17, 31, 0)

TEST_YAML = """\
Location:
   Street: 123456789 Some Street
   City: La Angelos
   State: Ga
   ZipCode: 44444
   Country: USA
   Phone: (800) 555-1212
   TimeZone: America/New_York
   Latitude: 34.0
   Longitude: -84.0
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
        l_loc.City = p_loc['City']
        l_loc.Country = p_loc['Country']
        l_loc.Phone = p_loc['Phone']
        l_loc.State = p_loc['State']
        l_loc.Street = p_loc['Street']
        l_loc.ZipCode = p_loc['ZipCode']
        l_dates = LDI()
        l_dates.Date_01 = p_loc['Date01']
        l_dates.Date_02 = p_loc['Date02']
        l_dates.Date_03 = p_loc['Date03']
        l_dates.Date_04 = p_loc['Date04']
        return l_loc, l_dates

    def print_hms(self, p_seconds):
        l_d = int(p_seconds // (24 * 60 * 60))
        p_seconds %= 24 * 60 * 60
        l_h = int(p_seconds // (60 * 60))
        p_seconds %= 60 * 60
        l_m = int(p_seconds // 60)
        p_seconds %= 60
        l_s = int(p_seconds)
        return '{:d}D:{:02d}H:{:02d}M:{:02d}S'.format(l_d, l_h, l_m, l_s)


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
        # print(PrettyFormatAny.form(self.m_test_config, 'A1-01-A - TestConfig'))
        l_loc, _l_dates = SetupMixin().load_earth(self.m_test_config)
        # print(PrettyFormatAny.form(l_loc, 'A1-01-B - Loc'))
        # print(PrettyFormatAny.form(l_dates, 'A1-01-C - Dates'))
        self.assertEqual(l_loc.Latitude, 34.0)
        self.assertEqual(l_loc.Longitude, -84.0)

    def test_02_Location(self):
        """ Test loading of location
        """


class B1_Astral(SetupMixin, unittest.TestCase):
    """ Test Sunrise and Sunset for each season of the year
    """

    def setUp(self):
        SetupMixin.setUp(self)
        self.m_api = sunrisesunset.Api(self.m_pyhouse_obj)
        l_loc, _l_dates = SetupMixin().load_earth(self.m_test_config)
        self.m_pyhouse_obj.House.Location = l_loc

    def test_02_Loc(self):
        l_ret = astralUtil().calc_solar_times(self.m_pyhouse_obj, T_DATE_1)
        # print('B1-02-A - Sun Rise', l_ret.SunRise)
        # print('B1-02-B - Sun Set', l_ret.SunSet)
        self.assertEqual(l_ret.SunRise.hour, T_SUNRISE_1.hour)
        self.assertApproximates(l_ret.SunRise.minute, T_SUNRISE_1.minute, 3)
        self.assertEqual(l_ret.SunSet.hour, T_SUNSET_1.hour)
        self.assertApproximates(l_ret.SunSet.minute, T_SUNSET_1.minute, 3)

    def test_03_Loc(self):
        l_ret = astralUtil().calc_solar_times(self.m_pyhouse_obj, T_DATE_2)
        # print('B1-03-A - Sun Rise', l_ret.SunRise)
        # print('B1-03-B - Sun Set', l_ret.SunSet)
        self.assertEqual(l_ret.SunRise.hour, T_SUNRISE_2.hour)
        self.assertApproximates(l_ret.SunRise.minute, T_SUNRISE_2.minute, 3)
        self.assertEqual(l_ret.SunSet.hour, T_SUNSET_2.hour)
        self.assertApproximates(l_ret.SunSet.minute, T_SUNSET_2.minute, 3)

    def test_04_Loc(self):
        l_ret = astralUtil().calc_solar_times(self.m_pyhouse_obj, T_DATE_3)
        # print('B1-04-A - Sun Rise', l_ret.SunRise)
        # print('B1-04-B - Sun Set', l_ret.SunSet)
        self.assertEqual(l_ret.SunRise.hour, T_SUNRISE_3.hour)
        self.assertApproximates(l_ret.SunRise.minute, T_SUNRISE_3.minute, 3)
        self.assertEqual(l_ret.SunSet.hour, T_SUNSET_3.hour)
        self.assertApproximates(l_ret.SunSet.minute, T_SUNSET_3.minute, 3)

    def test_05_Loc(self):
        """ Nearly the shortest day of the year.
        Also, Standard time.
        """
        l_ret = astralUtil().calc_solar_times(self.m_pyhouse_obj, T_DATE_4)
        # print('Sun Rise', l_ret.SunRise)
        # print('Sun Set', l_ret.SunSet)
        self.assertEqual(l_ret.SunRise.hour, T_SUNRISE_4.hour)
        self.assertApproximates(l_ret.SunRise.minute, T_SUNRISE_4.minute, 3)
        self.assertEqual(l_ret.SunSet.hour, T_SUNSET_4.hour)
        self.assertApproximates(l_ret.SunSet.minute, T_SUNSET_4.minute, 3)


class C1_Delay(SetupMixin, unittest.TestCase):
    """
    """

    def setUp(self):
        SetupMixin.setUp(self)
        l_loc, _l_dates = SetupMixin().load_earth(self.m_test_config)
        self.m_pyhouse_obj.House.Location = l_loc
        self.m_api = sunrisesunset.Api(self.m_pyhouse_obj)

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
        l_loc, _l_dates = SetupMixin().load_earth(self.m_test_config)
        self.m_pyhouse_obj.House.Location = l_loc
        self.m_api = sunrisesunset.Api(self.m_pyhouse_obj)

    def test_01_Loc(self):
        l_now = astralUtil().get_seconds_to_recalc()
        print(PrettyFormatAny.form(l_now, 'Next'))
        print('D1-01-A - {}'.format(self.print_hms(l_now)))

# ## END DBK
