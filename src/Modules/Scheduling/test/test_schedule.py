"""
@name: PyHouse/src/Modules/Scheduling/test/test_schedule.py
@author: D. Brian Kimmel
@contact: d.briankimmel@gmail.com
@Copyright (c) 2013-2014 by D. Brian Kimmel
@license: MIT License
@note: Created on Apr 8, 2013
@summary: Test handling the schedule information for a house.

"""

# Import system type stuff
import datetime
import xml.etree.ElementTree as ET
from twisted.trial import unittest

# Import PyMh files and modules.
from Modules.Core.data_objects import ScheduleBaseData
from Modules.Scheduling import schedule, schedule_xml
from Modules.Scheduling import sunrisesunset
from test import xml_data
from test.testing_mixin import SetupPyHouseObj
from Modules.Utilities.tools import PrettyPrintAny


class SetupMixin(object):
    """
    """

    def setUp(self, p_root):
        self.m_pyhouse_obj = SetupPyHouseObj().BuildPyHouseObj(p_root)
        self.m_xml = SetupPyHouseObj().BuildXml(p_root)
        self.m_api = schedule.API()


class Test_01_Time(SetupMixin, unittest.TestCase):
    """
    This section tests the schedule's time
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(xml_data.XML_LONG))
        self.m_schedule_obj = ScheduleBaseData()
        self.m_now = datetime.datetime(2014, 6, 6, 12, 15, 30)
        self.m_sunrise = datetime.datetime(1900, 1, 1, 7, 51, 22)
        self.m_sunset = datetime.datetime(1900, 1, 1, 19, 43, 54)

    def test_0101_Now(self):
        l_now = datetime.datetime.now()
        l_now2 = self.m_api._now_daytime()
        self.assertEqual(l_now, l_now2)
        print('Current time is {0:}'.format(l_now))

    def test_0102_Diff(self):
        l_sched = datetime.datetime(2014, 6, 6, 12, 30, 00)
        l_diff = self.m_api._find_diff(l_sched, self.m_now)
        self.assertEqual(l_diff, 870.0)

    def test_0103_RiseSet(self):
        l_test = self.m_api._is_rise_set('01:02:03')
        print(l_test)
        self.assertFalse(l_test)
        self.assertTrue(self.m_api._is_rise_set('sunrise'))
        self.assertTrue(self.m_api._is_rise_set('sunrise + 1:25'))
        self.assertTrue(self.m_api._is_rise_set('sunrise - 2:15'))
        self.assertTrue(self.m_api._is_rise_set('sunset'))
        self.assertFalse(self.m_api._is_rise_set('sunrtime'))

    def test_0104_Offset(self):
        l_test = self.m_api._is_rise_set('01:02:03')
        print(l_test)
        self.assertFalse(l_test)
        self.assertFalse(self.m_api._is_offset('sunrise'))
        self.assertTrue(self.m_api._is_offset('sunrise + 1:25'))
        self.assertTrue(self.m_api._is_offset('sunrise - 2:15'))
        self.assertFalse(self.m_api._is_offset('sunset'))
        self.assertFalse(self.m_api._is_offset('sunrtime'))

    def test_0105_TimeOffset(self):
        l_input = '01:02:03'
        l_time, l_field = self.m_api._extract_time_or_offset(l_input)
        print('Field, time = {0:} -- {1:} - {2:}'.format(l_input, l_field, l_time))

        l_input = '12:55'
        l_time, l_field = self.m_api._extract_time_or_offset(l_input)
        print('Field, time = {0:} -- {1:} - {2:}'.format(l_input, l_field, l_time))

        l_input = 'sunset - 00:45'
        l_time, l_field = self.m_api._extract_time_or_offset(l_input)
        print('Field, time = {0:} -- {1:} - {2:}'.format(l_input, l_field, l_time))

        l_input = 'sunrise + 3:05'
        l_time, l_field = self.m_api._extract_time_or_offset(l_input)
        print('Field, time = {0:} -- {1:} - {2:}'.format(l_input, l_field, l_time))

    def test_0106_DOW(self):
        l_dow = self.m_api._find_dow(datetime.datetime(2014, 6, 2))
        self.assertEqual(l_dow, 0)
        l_dow = self.m_api._find_dow(datetime.datetime(2014, 6, 6))
        self.assertEqual(l_dow, 4)
        l_dow = self.m_api._find_dow(datetime.datetime(2014, 6, 8))
        self.assertEqual(l_dow, 6)

    def test_0107_TestDow(self):
        l_sched = self.m_pyhouse_obj
        l_sched.DOW = 127
        l_is_dow = self.m_api._is_dow(l_sched, 0)
        self.assertTrue(l_is_dow)
        l_is_dow = self.m_api._is_dow(l_sched, 6)
        self.assertTrue(l_is_dow)
        l_sched.DOW = 0
        l_is_dow = self.m_api._is_dow(l_sched, 0)
        self.assertFalse(l_is_dow)
        l_is_dow = self.m_api._is_dow(l_sched, 6)
        self.assertFalse(l_is_dow)
        l_sched.DOW = 1
        l_is_dow = self.m_api._is_dow(l_sched, 0)
        self.assertTrue(l_is_dow)
        l_is_dow = self.m_api._is_dow(l_sched, 6)
        self.assertFalse(l_is_dow)
        l_sched.DOW = 64
        l_is_dow = self.m_api._is_dow(l_sched, 0)
        self.assertFalse(l_is_dow)
        l_is_dow = self.m_api._is_dow(l_sched, 6)
        self.assertTrue(l_is_dow)

    def test_0108_Days(self):
        l_sched = self.m_pyhouse_obj
        l_sched.DOW = 127
        print("Now =", self.m_now)
        l_days = self.m_api._get_days(l_sched, self.m_now)
        print(l_days)
        l_sched.DOW = 64
        l_days = self.m_api._get_days(l_sched, self.m_now)
        print(l_days)
        l_sched.DOW = 32
        l_days = self.m_api._get_days(l_sched, self.m_now)
        print(l_days)
        l_sched.DOW = 16
        l_days = self.m_api._get_days(l_sched, self.m_now)
        print(l_days)
        l_sched.DOW = 8
        l_days = self.m_api._get_days(l_sched, self.m_now)
        print(l_days)
        l_sched.DOW = 4
        l_days = self.m_api._get_days(l_sched, self.m_now)
        print(l_days)
        l_sched.DOW = 2
        l_days = self.m_api._get_days(l_sched, self.m_now)
        print(l_days)
        l_sched.DOW = 1
        l_days = self.m_api._get_days(l_sched, self.m_now)
        print(l_days)

    def test_0109_ExtractTime(self):
        # self.m_api._get_sunrise_sunset()
        l_sched = self.m_schedule_obj
        l_sched.Time = '12:34:56'
        l_time = self.m_api._extract_time_of_day(l_sched, self.m_sunrise, self.m_sunset)
        print(l_time)
        l_sched.Time = '12:55'
        l_time = self.m_api._extract_time_of_day(l_sched, self.m_sunrise, self.m_sunset)
        print(l_time)
        l_sched.Time = 'sunrise + 00:34:56'
        l_time = self.m_api._extract_time_of_day(l_sched, self.m_sunrise, self.m_sunset)
        print(l_time)

    def test_0121_RiseSet(self):
        self.m_api._get_sunrise_sunset()
        print(self.m_sunrise)

    def test_0191_Delay(self):
        pass


class Test_02_Setup(SetupMixin, unittest.TestCase):
    """
    This section tests the Building of a schedule list
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(xml_data.XML_LONG))

    def test_0211_xxx(self):

        PrettyPrintAny(self.m_pyhouse_obj, 'PyHouse_obj')

    def Xtest_0303_RunSchedule(self):
        PrettyPrintAny(self.m_pyhouse_obj.House.OBJs, 'Schedules')

    def Xtest_0305_SchedulesList(self):
        pass

    def Xtest_0307_OneSchedule(self):
        pass
        self.m_api.execute_one_schedule(3)

    def Xtest_0309_DispatchSchedule(self):
        pass

class Test_04_Utility(SetupMixin, unittest.TestCase):
    """
    This section tests the Building of a schedule list
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(xml_data.XML_LONG))
        # self.m_pyhouse_obj.House.OBJs.Schedules = self.m_api.read_schedules_xml(self.m_pyhouse_obj)
        self.m_timefield = 0

    def Xtest_0401_SubstituteTime(self):
        self.m_api._substitute_time(self.m_timefield)

    def Xtest_0455_Next(self):
        self.m_api.get_next_sched()

# ## END
