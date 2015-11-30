"""
@name:      PyHouse/src/Modules/scheduling/sunrisesunset.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2011-2015 by D. Brian Kimmel
@note:      Created on Mar 6, 2011
@license:   MIT License
@summary:   Calculate the suns location at local noon, then calculate sunrise and sunset for the day.

Passed all 6 tests - DBK - 2015-09-12

http://en.wikipedia.org/wiki/Sunrise_equation
"""

# Import system type stuff
import datetime
import xml.etree.ElementTree as ET
from twisted.trial import unittest
from math import pi

# Import PyMh files
from Modules.Core.data_objects import LocationData
from Modules.Scheduling import sunrisesunset
from Modules.Scheduling.sunrisesunset import Util as AstralUtil
from test.testing_mixin import SetupPyHouseObj
from test import xml_data
from Modules.Utilities.debug_tools import PrettyFormatAny

# Conversion constants.
RAD2DEG = 180.0 / pi
DEG2RAD = pi / 180.0


# All Tests - Location Information
T_NAME = 'Testing Location'
T_REGION = 'Seattle'
T_LATITUDE = 47.62
T_LONGITUDE = -122.33
T_TIMEZONE_NAME = 'America/Los_Angeles'
T_ELEVATION = 10
# T_TZ = sunrisesunset.LocationTz()

T_DATE_0 = datetime.date(2014, 1, 21)
T_SUNRISE_0 = datetime.datetime(2014, 1, 21, 7, 48, 0, tzinfo = None)
T_DATE_1 = datetime.date(2014, 4, 22)
T_SUNRISE_1 = datetime.datetime(2014, 4, 22, 6, 7, 0)
T_DATE_2 = datetime.date(2015, 7, 23)
T_SUNRISE_2 = datetime.datetime(2015, 7, 23, 5, 36, 0)
T_DATE_3 = datetime.date(2015, 10, 24)
T_SUNRISE_3 = datetime.datetime(2015, 10, 24, 7, 41, 0)
T_DATE_4 = datetime.date(2015, 12, 22)
T_SUNRISE_4 = datetime.datetime(2015, 12, 22, 7, 55, 0)


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
        l_loc.Region = T_REGION
        l_loc.Latitude = T_LATITUDE
        l_loc.Longitude = T_LONGITUDE
        l_loc.TimeZoneName = T_TIMEZONE_NAME
        l_loc.Elevation = T_ELEVATION
        p_pyhouse_obj.House.Location = l_loc
        p_pyhouse_obj.House.Name = T_NAME
        return p_pyhouse_obj


class A_Astral(SetupMixin, unittest.TestCase):

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(xml_data.XML_LONG))
        self.m_pyhouse_obj = self.load_earth(self.m_pyhouse_obj)
        self.m_api = sunrisesunset.API(self.m_pyhouse_obj)

    def test_00_Loc(self):
        print(PrettyFormatAny.form(self.m_pyhouse_obj, 'PyHouse '))
        print(PrettyFormatAny.form(self.m_pyhouse_obj.House, 'PyHouse.House '))
        print(PrettyFormatAny.form(self.m_pyhouse_obj.House.Location, 'PyHouse.Houe.Location '))

    def test_01_Loc(self):
        # locationXml.read_location_xml(self.m_pyhouse_obj)
        l_ret = AstralUtil.calc_solar_times(self.m_pyhouse_obj, T_DATE_0)
        print(' Calc:{}\n  Web:{}'.format(l_ret.SunRise, T_SUNRISE_0))
        print(l_ret.SunRise)
        self.assertEqual(l_ret.SunRise.hour, T_SUNRISE_0.hour)
        self.assertApproximates(l_ret.SunRise.minute, T_SUNRISE_0.minute, 1)

    def test_02_Loc(self):
        # locationXml.read_location_xml(self.m_pyhouse_obj)
        l_ret = AstralUtil.calc_solar_times(self.m_pyhouse_obj, T_DATE_1)
        print(' Calc:{}\n  Web:{}'.format(l_ret.SunRise, T_SUNRISE_1))
        print(l_ret.SunRise)
        self.assertEqual(l_ret.SunRise.hour, T_SUNRISE_1.hour)
        self.assertApproximates(l_ret.SunRise.minute, T_SUNRISE_1.minute, 1)

    def test_03_Loc(self):
        # locationXml.read_location_xml(self.m_pyhouse_obj)
        l_ret = AstralUtil.calc_solar_times(self.m_pyhouse_obj, T_DATE_2)
        print(' Calc:{}\n  Web:{}'.format(l_ret.SunRise, T_SUNRISE_2))
        print(l_ret.SunRise)
        self.assertEqual(l_ret.SunRise.hour, T_SUNRISE_2.hour)
        self.assertApproximates(l_ret.SunRise.minute, T_SUNRISE_2.minute, 1)

    def test_04_Loc(self):
        l_ret = AstralUtil.calc_solar_times(self.m_pyhouse_obj, T_DATE_3)
        print(' Calc:{}\n  Web:{}'.format(l_ret.SunRise, T_SUNRISE_3))
        print(l_ret.SunRise)
        self.assertEqual(l_ret.SunRise.hour, T_SUNRISE_3.hour)
        self.assertApproximates(l_ret.SunRise.minute, T_SUNRISE_3.minute, 1)

    def test_05_Loc(self):
        l_ret = AstralUtil.calc_solar_times(self.m_pyhouse_obj, T_DATE_4)
        print(' Calc:{}\n  Web:{}'.format(l_ret.SunRise, T_SUNRISE_4))
        print(l_ret.SunRise)
        self.assertEqual(l_ret.SunRise.hour, T_SUNRISE_4.hour)
        self.assertApproximates(l_ret.SunRise.minute, T_SUNRISE_4.minute, 1)

class B_Delay(SetupMixin, unittest.TestCase):
    """
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(xml_data.XML_LONG))
        self.m_pyhouse_obj = self.load_earth(self.m_pyhouse_obj)
        self.m_api = sunrisesunset.API(self.m_pyhouse_obj)

    def test_01_Loc(self):
        l_delay = sunrisesunset.Util._till_next()
        print(PrettyFormatAny.form(l_delay, 'Next'))

    def test_02(self):
        pass

# ## END DBK
