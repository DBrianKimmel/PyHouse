"""
@name:      PyHouse/Project/src/Modules/Core/Utilities/test/test_convert.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: 2013-2019 by D. Brian Kimmel
@license:   MIT License
@note:      Created on Apr 4, 2013
@summary:   This module is for testing conversion tools.

Passed all 5 tests - DBK - 2017-04-29
"""
__updated__ = '2019-01-13'

# Import system type stuff
# import xml.etree.ElementTree as ET
from twisted.trial import unittest
import datetime

# Import PyMh files and modules.
from Modules.Core.Utilities import convert
# from test.xml_data import XML_LONG
# from test.testing_mixin import SetupPyHouseObj
# from Modules.Core.Utilities.debug_tools import PrettyFormatAnySetupMixin.setUp(self, ET.fromstring(XML_LONG))

STR_IPV4 = '192.168.1.54'
LONG_IPV4 = 3232235830
STR_IPV6 = '2001:db8::1'
LONG_IPV6 = 42540766411282592856903984951653826561

T_TODAY = datetime.datetime(2015, 6, 6, 12, 34, 56)
TESTING_SCHEDULE_DATE_0 = datetime.datetime(2015, 6, 21)
TESTING_SCHEDULE_DAWN_0 = datetime.datetime(2016, 6, 21, 6, 4, 52)
TESTING_SCHEDULE_SUNRISE_0 = datetime.datetime(2016, 6, 21, 6, 31, 56)
TESTING_SCHEDULE_NOON_0 = datetime.datetime(2016, 6, 21, 13, 31, 41)
TESTING_SCHEDULE_SUNSET_0 = datetime.datetime(2016, 6, 21, 20, 31, 25)
TESTING_SCHEDULE_DUSK_0 = datetime.datetime(2016, 6, 21, 20, 58, 30)


class A0(unittest.TestCase):

    def setUp(self):
        pass

    def test_00_Print(self):
        print('Id: test_convert')


class B1_Pow(unittest.TestCase):

    def setUp(self):
        pass

    def test_01_Str2Long(self):
        l_str = STR_IPV4
        l_long = convert.str_to_long(l_str)
        self.assertEqual(l_long, LONG_IPV4)


class C1_Convert(unittest.TestCase):

    def setUp(self):
        pass

    def test_01_Str2Long(self):
        l_str = STR_IPV4
        l_long = convert.str_to_long(l_str)
        # print('C1-01-A - ', l_str, l_long)
        self.assertEqual(l_long, LONG_IPV4)

    def test_02_Str2Long(self):
        l_str = STR_IPV6
        l_long = convert.str_to_long(l_str)
        # print('C1-02-A - ', l_str, l_long)
        self.assertEqual(l_long, LONG_IPV6)

    def test_03_Long2Str(self):
        l_str = LONG_IPV4
        l_long = convert.long_to_str(l_str)
        print('C1-03-A - ', l_str, l_long)
        self.assertEqual(l_long, STR_IPV4)

    def test_04_Long2Str(self):
        l_str = LONG_IPV6
        l_long = convert.long_to_str(l_str)
        # print('C1-04-A - ', l_str, l_long)
        self.assertEqual(l_long, STR_IPV6)


class D1_Utility(unittest.TestCase):
    """
    Testing conversion and extraction
    """

    def setUp(self):
        pass

    def test_01_Mins(self):
        """ Convert a datetime to Minutes
        """
        l_seconds = convert.datetime_to_seconds(T_TODAY)
        self.assertEqual(l_seconds, (12 * 60 + 34) * 60 + 56)
        #
        l_seconds = convert.datetime_to_seconds(TESTING_SCHEDULE_DAWN_0)
        self.assertEqual(l_seconds, (TESTING_SCHEDULE_DAWN_0.hour * 60 + TESTING_SCHEDULE_DAWN_0.minute) * 60 + TESTING_SCHEDULE_DAWN_0.second)
        #
        l_seconds = convert.datetime_to_seconds(TESTING_SCHEDULE_SUNRISE_0)
        self.assertEqual(l_seconds, (TESTING_SCHEDULE_SUNRISE_0.hour * 60 + TESTING_SCHEDULE_SUNRISE_0.minute) * 60 + TESTING_SCHEDULE_SUNRISE_0.second)
        #
        l_seconds = convert.datetime_to_seconds(TESTING_SCHEDULE_NOON_0)
        self.assertEqual(l_seconds, (TESTING_SCHEDULE_NOON_0.hour * 60 + TESTING_SCHEDULE_NOON_0.minute) * 60 + TESTING_SCHEDULE_NOON_0.second)
        #
        l_seconds = convert.datetime_to_seconds(TESTING_SCHEDULE_SUNSET_0)
        self.assertEqual(l_seconds, (TESTING_SCHEDULE_SUNSET_0.hour * 60 + TESTING_SCHEDULE_SUNSET_0.minute) * 60 + TESTING_SCHEDULE_SUNSET_0.second)
        #
        l_seconds = convert.datetime_to_seconds(TESTING_SCHEDULE_DUSK_0)
        self.assertEqual(l_seconds, (TESTING_SCHEDULE_DUSK_0.hour * 60 + TESTING_SCHEDULE_DUSK_0.minute) * 60 + TESTING_SCHEDULE_DUSK_0.second)

    def test_02_seconds(self):
        """
        """
        l_seconds = convert.datetime_to_seconds(T_TODAY)
        self.assertEqual(l_seconds, (12 * 60 + 34) * 60 + 56)

# ## END
