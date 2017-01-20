"""
@name:      PyHouse/src/Modules/scheduling/sunrisesunset.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2011-2017 by D. Brian Kimmel
@note:      Created on Mar 6, 2011
@license:   MIT License
@summary:   Calculate the suns location at local noon, then calculate sunrise and sunset for the day.

Passed all 9 tests - DBK - 2016-11-21

http://en.wikipedia.org/wiki/Sunrise_equation
"""

__updated__ = '2016-11-21'

# Import system type stuff
import datetime
import xml.etree.ElementTree as ET
from twisted.trial import unittest
from math import pi

# Import PyMh files
from Modules.Core.data_objects import LocationData
from Modules.Housing.Scheduling import sunrisesunset
from Modules.Housing.Scheduling.sunrisesunset import Util as AstralUtil
from test.testing_mixin import SetupPyHouseObj
from test.xml_data import XML_LONG
from Modules.Core.Utilities.debug_tools import PrettyFormatAny
from Modules.Housing.test.xml_location import \
    TESTING_LOCATION_REGION, \
    TESTING_LOCATION_LATITUDE, \
    TESTING_LOCATION_LONGITUDE, \
    TESTING_LOCATION_TIME_ZONE_NAME, \
    TESTING_LOCATION_ELEVATION
from Modules.Housing.test.xml_housing import TESTING_HOUSE_NAME

# Conversion constants.
RAD2DEG = 180.0 / pi
DEG2RAD = pi / 180.0


# Calcukated from http://www.calendar-updates.com for zip-code 34465 on 2016-07-16
T_DATE_0 = datetime.date(2016, 7, 16)
T_SUNRISE_0 = datetime.datetime(2016, 7, 16, 6, 42, 0, tzinfo=None)
T_SUNSET_0 = datetime.datetime(2016, 7, 16, 20, 30, 0, tzinfo=None)

#  http://www.esrl.noaa.gov/gmd/grad/solcalc/sunrise.html
T_DATE_1 = datetime.date(2014, 4, 22)
T_SUNRISE_1 = datetime.datetime(2014, 4, 22, 6, 57, 0)
T_SUNSET_1 = datetime.datetime(2014, 4, 22, 20, 00, 0)

T_DATE_2 = datetime.date(2015, 7, 23)
T_SUNRISE_2 = datetime.datetime(2015, 7, 23, 6, 46, 0)
T_SUNSET_2 = datetime.datetime(2015, 7, 23, 20, 27, 0)

T_DATE_3 = datetime.date(2015, 10, 24)
T_SUNRISE_3 = datetime.datetime(2015, 10, 24, 7, 37, 0)
T_SUNSET_3 = datetime.datetime(2015, 10, 24, 18, 51, 0)

T_DATE_4 = datetime.date(2015, 12, 22)
T_SUNRISE_4 = datetime.datetime(2015, 12, 22, 7, 20, 0)
T_SUNSET_4 = datetime.datetime(2015, 12, 22, 17, 38, 0)


class SetupMixin(object):
    """
    """

    def setUp(self, p_root):
        self.m_pyhouse_obj = SetupPyHouseObj().BuildPyHouseObj(p_root)
        self.m_xml = SetupPyHouseObj().BuildXml(p_root)
        self.test_date_1 = T_DATE_0

    @staticmethod
    def load_earth(p_pyhouse_obj):
        l_loc = LocationData()
        l_loc.Region = TESTING_LOCATION_REGION
        l_loc.Latitude = float(TESTING_LOCATION_LATITUDE)
        l_loc.Longitude = float(TESTING_LOCATION_LONGITUDE)
        l_loc.TimeZoneName = TESTING_LOCATION_TIME_ZONE_NAME
        l_loc.Elevation = float(TESTING_LOCATION_ELEVATION)
        p_pyhouse_obj.House.Location = l_loc
        p_pyhouse_obj.House.Name = TESTING_HOUSE_NAME
        return p_pyhouse_obj


class A0(unittest.TestCase):
    def setUp(self):
        pass
    def test_00_Print(self):
        print('Id: test_sunrisesunset')


class A1_Setup(SetupMixin, unittest.TestCase):
    """
    """
    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))

    def test_01_Earth(self):
        SetupMixin.load_earth(self.m_pyhouse_obj)
        l_loc = self.m_pyhouse_obj.House.Location
        # print(PrettyFormatAny.form(l_loc, 'A1-01-A - Loc'))
        self.assertEqual(l_loc.Latitude, float(TESTING_LOCATION_LATITUDE))


class B1_Astral(SetupMixin, unittest.TestCase):

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))
        self.m_pyhouse_obj = self.load_earth(self.m_pyhouse_obj)
        self.m_api = sunrisesunset.API(self.m_pyhouse_obj)

    def test_01_Loc(self):
        l_ret = AstralUtil.calc_solar_times(self.m_pyhouse_obj, T_DATE_0)
        # print('Sun Rise', l_ret.SunRise)
        self.assertEqual(l_ret.SunRise.hour, T_SUNRISE_0.hour)
        self.assertApproximates(l_ret.SunRise.minute, T_SUNRISE_0.minute, 1)
        # print('Sun Set', l_ret.SunSet)
        self.assertEqual(l_ret.SunSet.hour, T_SUNSET_0.hour)
        self.assertApproximates(l_ret.SunSet.minute, T_SUNSET_0.minute, 1)

    def test_02_Loc(self):
        l_ret = AstralUtil.calc_solar_times(self.m_pyhouse_obj, T_DATE_1)
        # print('Sun Rise', l_ret.SunRise)
        self.assertEqual(l_ret.SunRise.hour, T_SUNRISE_1.hour)
        self.assertApproximates(l_ret.SunRise.minute, T_SUNRISE_1.minute, 1)
        # print('Sun Set', l_ret.SunSet)
        self.assertEqual(l_ret.SunSet.hour, T_SUNSET_1.hour)
        self.assertApproximates(l_ret.SunSet.minute, T_SUNSET_1.minute, 1)

    def test_03_Loc(self):
        l_ret = AstralUtil.calc_solar_times(self.m_pyhouse_obj, T_DATE_2)
        # print('Sun Rise', l_ret.SunRise)
        self.assertEqual(l_ret.SunRise.hour, T_SUNRISE_2.hour)
        self.assertApproximates(l_ret.SunRise.minute, T_SUNRISE_2.minute, 1)
        # print('Sun Set', l_ret.SunSet)
        self.assertEqual(l_ret.SunSet.hour, T_SUNSET_2.hour)
        self.assertApproximates(l_ret.SunSet.minute, T_SUNSET_2.minute, 1)

    def test_04_Loc(self):
        l_ret = AstralUtil.calc_solar_times(self.m_pyhouse_obj, T_DATE_3)
        # print('Sun Rise', l_ret.SunRise)
        self.assertEqual(l_ret.SunRise.hour, T_SUNRISE_3.hour)
        self.assertApproximates(l_ret.SunRise.minute, T_SUNRISE_3.minute, 1)
        # print('Sun Set', l_ret.SunSet)
        self.assertEqual(l_ret.SunSet.hour, T_SUNSET_3.hour)
        self.assertApproximates(l_ret.SunSet.minute, T_SUNSET_3.minute, 1)

    def test_05_Loc(self):
        l_ret = AstralUtil.calc_solar_times(self.m_pyhouse_obj, T_DATE_4)
        # print('Sun Rise', l_ret.SunRise)
        self.assertEqual(l_ret.SunRise.hour, T_SUNRISE_4.hour)
        self.assertApproximates(l_ret.SunRise.minute, T_SUNRISE_4.minute, 1)
        # print('Sun Set', l_ret.SunSet)
        self.assertEqual(l_ret.SunSet.hour, T_SUNSET_4.hour)
        self.assertApproximates(l_ret.SunSet.minute, T_SUNSET_4.minute, 1)


class C1_Delay(SetupMixin, unittest.TestCase):
    """
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))
        self.m_pyhouse_obj = self.load_earth(self.m_pyhouse_obj)
        self.m_api = sunrisesunset.API(self.m_pyhouse_obj)

    def test_01_Loc(self):
        l_delay = sunrisesunset.Util._till_next()
        # print(PrettyFormatAny.form(l_delay, 'Next'))

    def test_02(self):
        pass

# ## END DBK
