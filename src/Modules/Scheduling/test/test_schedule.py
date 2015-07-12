"""
@name:      PyHouse/src/Modules/Scheduling/test/test_schedule.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2013-2015 by D. Brian Kimmel
@license:   MIT License
@note:      Created on Apr 8, 2013
@summary:   Test handling the schedule information for a house.

"""

# Import system type stuff
import datetime
import xml.etree.ElementTree as ET
from twisted.trial import unittest

# Import PyMh files and modules.
from Modules.Core.data_objects import ScheduleBaseData, RiseSetData
from Modules.Computer.Mqtt.mqtt_client import API as mqttAPI
from Modules.Scheduling.schedule import Sch, API as scheduleAPI
from Modules.Scheduling.schedule_xml import ScheduleXmlAPI
from test import xml_data
from test.testing_mixin import SetupPyHouseObj
from Modules.Utilities.tools import PrettyPrintAny


T_NOW = datetime.datetime(2014, 6, 6, 12, 34, 56)
T_SUNRISE = datetime.datetime(2014, 6, 6, 7, 12, 34)
T_SUNSET = datetime.datetime(2014, 6, 6, 20, 19, 18)



class MockupRiseSet(object):
    """
    A fake module to get sunrise and sunset.
    Replaces sunrisesunset.py for testing purposes.
    """
    def mock(self):
        l_ret = RiseSetData()
        l_ret.Sunrise = T_SUNRISE
        l_ret.Sunset = T_SUNSET
        return l_ret


class SetupMixin(object):
    """
    """

    def setUp(self, p_root):
        self.m_pyhouse_obj = SetupPyHouseObj().BuildPyHouseObj(p_root)
        self.m_xml = SetupPyHouseObj().BuildXml(p_root)
        self.m_api = scheduleAPI(self.m_pyhouse_obj)



class C1_Static(SetupMixin, unittest.TestCase):
    """
    Test Staticmethods
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(xml_data.XML_LONG))

    def test_01_MakeTimedelta(self):
        l_delta = Sch._make_timedelta(T_NOW)
        print('Now: {};   Delta: {}'.format(T_NOW, l_delta))
        self.assertEqual(l_delta, datetime.timedelta(0, 45296))



class C2_Time(SetupMixin, unittest.TestCase):
    """
    This section tests the schedule's time
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(xml_data.XML_LONG))
        self.m_schedule_obj = ScheduleBaseData()
        self.m_schedule_obj.Name = 'Test schedule'
        self.m_schedule_obj.Active = True
        self.m_schedule_obj.DOW = 0x7f
        self.m_schedule_obj.Key = 0
        self.m_schedule_obj.Mode = 0
        self.m_schedule_obj.ScheduleType = 'LightDevice'
        self.m_schedule_obj.Time = '16.54'
        self.m_now = T_NOW

    def test_01_Now(self):
        """Get the current date and time.
        """
        l_now = datetime.datetime.now()
        l_now2 = self.m_api._now_daytime()
        self.assertEqual(l_now, l_now2)
        print('Current time is {0:}'.format(l_now))

    def test_02_TimeOffset(self):
        """Get the time or the offset time from the timefield.
        """
        l_input = '01:02:03'
        l_time = self.m_api._extract_time_or_offset(l_input)
        print('Field: "{}";   TimeDelta: {}'.format(l_input, l_time))
        self.assertEqual(l_time, datetime.timedelta(0, 3723))

        l_input = '12:55'
        l_time = self.m_api._extract_time_or_offset(l_input)
        print('Field: "{}";   TimeDelta: {}'.format(l_input, l_time))
        self.assertEqual(l_time, datetime.timedelta(0, 46500))

        l_input = 'sunset'
        l_time = self.m_api._extract_time_or_offset(l_input)
        print('Field: "{}";   TimeDelta: {}'.format(l_input, l_time))
        self.assertEqual(l_time, datetime.timedelta(0, 0))

        l_input = 'sunset - 00:45'
        l_time = self.m_api._extract_time_or_offset(l_input)
        print('Field: "{}";   TimeDelta: {}'.format(l_input, l_time))
        self.assertEqual(l_time, datetime.timedelta(0, 2700))

        l_input = 'sunrise + 3:05'
        l_time = self.m_api._extract_time_or_offset(l_input)
        print('Field: "{}";   TimeDelta: {}'.format(l_input, l_time))
        self.assertEqual(l_time, datetime.timedelta(0, 11100))

    def test_03_FindDOW(self):
        """Test getting the Day of week (mon = 0)
        """
        l_dow = self.m_api._find_dow(datetime.datetime(2014, 6, 2))
        self.assertEqual(l_dow, 0)
        l_dow = self.m_api._find_dow(datetime.datetime(2014, 6, 6))
        self.assertEqual(l_dow, 4)
        l_dow = self.m_api._find_dow(datetime.datetime(2014, 6, 8))
        self.assertEqual(l_dow, 6)

    def test_04_isDow(self):
        """Test to see if the day bit is set in the DOW field of the schedule.
        """
        l_sched = self.m_pyhouse_obj
        l_sched.DOW = 127  # MTWTFSS all turned on
        l_is_dow = self.m_api._is_dow(l_sched, 0)
        self.assertTrue(l_is_dow)
        l_is_dow = self.m_api._is_dow(l_sched, 6)
        self.assertTrue(l_is_dow)
        l_sched.DOW = 0  # No days on
        l_is_dow = self.m_api._is_dow(l_sched, 0)
        self.assertFalse(l_is_dow)
        l_is_dow = self.m_api._is_dow(l_sched, 6)
        self.assertFalse(l_is_dow)
        l_sched.DOW = 1  # Monday is on
        l_is_dow = self.m_api._is_dow(l_sched, 0)
        self.assertTrue(l_is_dow)
        l_is_dow = self.m_api._is_dow(l_sched, 6)
        self.assertFalse(l_is_dow)
        l_sched.DOW = 64  #  Sunday is on
        l_is_dow = self.m_api._is_dow(l_sched, 0)
        self.assertFalse(l_is_dow)
        l_is_dow = self.m_api._is_dow(l_sched, 6)
        self.assertTrue(l_is_dow)

    def test_05_IsDayInDOW(self):
        """Is now in the DOW field
        """
        print("Now =", self.m_now)
        #
        l_days = self.m_api._get_days(self.m_schedule_obj, self.m_now)
        print(l_days)
        self.assertEqual(l_days, 0)
        #
        self.m_schedule_obj.DOW = 64
        l_days = self.m_api._get_days(self.m_schedule_obj, self.m_now)
        print(l_days)
        #
        self.m_schedule_obj.DOW = 32
        l_days = self.m_api._get_days(self.m_schedule_obj, self.m_now)
        print(l_days)
        self.m_schedule_obj.DOW = 16
        l_days = self.m_api._get_days(self.m_schedule_obj, self.m_now)
        print(l_days)
        self.m_schedule_obj.DOW = 8
        l_days = self.m_api._get_days(self.m_schedule_obj, self.m_now)
        print(l_days)
        self.m_schedule_obj.DOW = 4
        l_days = self.m_api._get_days(self.m_schedule_obj, self.m_now)
        print(l_days)
        self.m_schedule_obj.DOW = 2
        l_days = self.m_api._get_days(self.m_schedule_obj, self.m_now)
        print(l_days)
        self.m_schedule_obj.DOW = 1
        l_days = self.m_api._get_days(self.m_schedule_obj, self.m_now)
        print(l_days)

    def test_06_Diff(self):
        """Find the seconds of time difference
        """
        l_sched = T_NOW
        l_diff = self.m_api._find_diff(l_sched, self.m_now)
        self.assertEqual(l_diff, 0.0)

    def test_07_ExtractTimeOfDay(self):
        """Test the effective time using Timefield and DOW
        """
        l_riseset = MockupRiseSet().mock()
        #
        self.m_schedule_obj.Time = '12:34:56'
        l_time = self.m_api._extract_time_of_day(self.m_schedule_obj, l_riseset)
        print('Field: "{}";    Result: {}\n'.format(self.m_schedule_obj.Time, l_time))
        #
        self.m_schedule_obj.Time = '12:55'
        l_time = self.m_api._extract_time_of_day(self.m_schedule_obj, l_riseset)
        print('Field: "{}";    Result: {}\n'.format(self.m_schedule_obj.Time, l_time))
        #
        self.m_schedule_obj.Time = 'sunrise'
        l_time = self.m_api._extract_time_of_day(self.m_schedule_obj, l_riseset)
        print('Field: "{}";    Result: {}\n'.format(self.m_schedule_obj.Time, l_time))
        #
        self.m_schedule_obj.Time = 'sunset'
        l_time = self.m_api._extract_time_of_day(self.m_schedule_obj, l_riseset)
        print('Field: "{}";    Result: {}\n'.format(self.m_schedule_obj.Time, l_time))
        #
        self.m_schedule_obj.Time = 'sunrise + 00:34:26'
        l_time = self.m_api._extract_time_of_day(self.m_schedule_obj, l_riseset)
        print('Field: "{}";    Result: {}\n'.format(self.m_schedule_obj.Time, l_time))
        #
        self.m_schedule_obj.Time = 'sunset - 00:43:18'
        l_time = self.m_api._extract_time_of_day(self.m_schedule_obj, l_riseset)
        print('Field: "{}";    Result: {}\n'.format(self.m_schedule_obj.Time, l_time))
        PrettyPrintAny(l_time, 'ExtractTimeOdDay result')

    def test_09_Seconds2Wait(self):
        l_riseset = MockupRiseSet().mock()
        PrettyPrintAny(l_riseset, 'Mock RiseSet')
        l_delay = self.m_api._seconds_to_wait(self.m_now, self.m_schedule_obj, l_riseset)
        self.assertEqual(l_delay, 41104.0)

    def test_10_RiseSet(self):
        pass



class C3_Loc(SetupMixin, unittest.TestCase):
    """
    Test things to do with the house location.
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(xml_data.XML_LONG))
        self.m_schedule_obj = ScheduleBaseData()
        self.m_now = datetime.datetime(2014, 6, 6, 12, 15, 30)

    def test_01_LoadLocation(self):
        self.m_pyhouse_obj.House.RefOBJs.Location.RiseSet.SunRise = T_SUNRISE
        self.m_pyhouse_obj.House.RefOBJs.Location.RiseSet.Sunset = T_SUNSET
        PrettyPrintAny(self.m_pyhouse_obj.House.RefOBJs.Location.RiseSet, 'Location')



class C4_Setup(SetupMixin, unittest.TestCase):
    """
    This section tests the Building of a schedule list
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(xml_data.XML_LONG))
        self.m_pyhouse_obj.House.RefOBJs.Location.RiseSet.SunRise = T_SUNRISE
        self.m_pyhouse_obj.House.RefOBJs.Location.RiseSet.SunSet = T_SUNSET
        self.m_pyhouse_obj.House.RefOBJs.Schedules = ScheduleXmlAPI().read_schedules_xml(self.m_pyhouse_obj)
        self.m_pyhouse_obj.APIs.Computer.MqttAPI = mqttAPI(self.m_pyhouse_obj)

    def test_01_BuildSched(self):
        PrettyPrintAny(self.m_pyhouse_obj.House.RefOBJs, 'Schedules')

        l_delay, l_list = self.m_api.find_next_scheduled_events(self.m_pyhouse_obj, T_NOW)
        print('Delay: {}'.format(l_delay))
        PrettyPrintAny(l_list, 'List')

    def test_02_yyy(self):
        PrettyPrintAny(self.m_pyhouse_obj, 'PyHouse_obj')

    def Xtest_03_RunSchedule(self):
        PrettyPrintAny(self.m_pyhouse_obj.House.RefOBJs, 'Schedules')

    def Xtest_05_SchedulesList(self):
        pass

    def Xtest_07_OneSchedule(self):
        pass
        self.m_api.execute_one_schedule(3)

    def Xtest_09_DispatchSchedule(self):
        pass



class C5_Utility(SetupMixin, unittest.TestCase):
    """
    This section tests the Building of a schedule list
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(xml_data.XML_LONG))
        # self.m_pyhouse_obj.House.RefOBJs.Schedules = self.m_api.read_schedules_xml(self.m_pyhouse_obj)
        self.m_timefield = 0

    def test_01_SubstituteTime(self):
        # self.m_api._substitute_time(self.m_timefield)
        pass

    def test_55_Next(self):
        # l_delay, l_list = self.m_api.find_next_scheduled_event(self.m_pyhouse_obj)
        pass

# ## END
