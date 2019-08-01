"""
@name:      PyHouse/Project/src/Modules/Core/Utilities/_test/test_convert.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: 2013-2019 by D. Brian Kimmel
@license:   MIT License
@note:      Created on Apr 4, 2013
@summary:   This module is for testing conversion tools.

Passed all 14 tests - DBK - 2019-03-30
"""
__updated__ = '2019-03-31'

# Import system type stuff
# import xml.etree.ElementTree as ET
from twisted.trial import unittest
import datetime

# Import PyMh files and modules.
from Modules.Core.Utilities import convert
# from _test.xml_data import XML_LONG
# from _test.testing_mixin import SetupPyHouseObj
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
        # print('C1-03-A - ', l_str, l_long)
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

    def test_02_secondsW(self):
        """
        """
        l_seconds = convert.datetime_to_seconds(T_TODAY)
        self.assertEqual(l_seconds, (12 * 60 + 34) * 60 + 56)

    def test_03_secondsW(self):
        """
        """
        l_seconds = convert.datetime_to_seconds(T_TODAY)
        self.assertEqual(l_seconds, (12 * 60 + 34) * 60 + 56)


class D2_BigEnd(unittest.TestCase):
    """ Test fetching big endian byte strings
    """

    def test_01_zero1(self):
        """ Convert a datetime to Minutes
        """
        l_bytes = b'\x00'
        l_int = convert.bigend_2_int(l_bytes)
        self.assertEqual(l_int, 0)

    def test_02_zero4(self):
        """ Convert a datetime to Minutes
        """
        l_bytes = b'\x00\x00\x00\x00'
        l_int = convert.bigend_2_int(l_bytes)
        self.assertEqual(l_int, 0)

    def test_03_one3(self):
        """ Convert a datetime to Minutes
        """
        l_bytes = b'\x00\x00\x01'
        l_int = convert.bigend_2_int(l_bytes)
        self.assertEqual(l_int, 1)

    def test_04_16_3(self):
        """ Convert a datetime to Minutes
        """
        l_bytes = b'\x00\x00\x10'
        l_int = convert.bigend_2_int(l_bytes)
        self.assertEqual(l_int, 16)

    def test_05_272_4(self):
        """ Convert a datetime to Minutes
        """
        l_bytes = b'\x00\x00\x01\x10'
        l_int = convert.bigend_2_int(l_bytes)
        self.assertEqual(l_int, 272)


class D3_BigEnd(unittest.TestCase):
    """ Test fetching big endian byte strings
    """

    def test_01_zero4(self):
        """ Convert a datetime to Minutes
        """
        l_int = 0
        l_bytes = convert.int_2_bigend(l_int, 4)
        self.assertEqual(l_bytes, b'\x00\x00\x00\x00')

    def test_02_zero2(self):
        """ Convert a datetime to Minutes
        """
        l_int = 0
        l_bytes = convert.int_2_bigend(l_int, 2)
        self.assertEqual(l_bytes, b'\x00\x00')

    def test_03_15_4(self):
        """ Convert a datetime to Minutes
        """
        l_int = 15
        l_bytes = convert.int_2_bigend(l_int, 4)
        self.assertEqual(l_bytes, b'\x00\x00\x00\x0f')

    def test_04_15_2(self):
        """ Convert a datetime to Minutes
        """
        l_int = 15
        l_bytes = convert.int_2_bigend(l_int, 2)
        self.assertEqual(l_bytes, b'\x00\x0f')

    def test_05_987_4(self):
        """ Convert a datetime to Minutes
        """
        l_int = 987
        l_bytes = convert.int_2_bigend(l_int, 4)
        self.assertEqual(l_bytes, b'\x00\x00\x03\xdb')

    def test_06_987_2(self):
        """ Convert a datetime to Minutes
        """
        l_int = 987
        l_bytes = convert.int_2_bigend(l_int, 2)
        self.assertEqual(l_bytes, b'\x03\xdb')

# ## END
