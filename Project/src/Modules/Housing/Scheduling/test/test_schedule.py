"""
@name:      PyHouse/src/Modules/Scheduling/test/test_schedule.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2013-2018 by D. Brian Kimmel
@license:   MIT License
@note:      Created on Apr 8, 2013
@summary:   Test handling the schedule information for a house.

Passed all 38 tests - DBK - 2018-02-13

There are some tests (Starting with XX) that I do not know how to do in twisted.

"""

__updated__ = '2018-02-13'

# Import system type stuff
import datetime
import xml.etree.ElementTree as ET
from twisted.trial import unittest
import time

# Import PyMh files and modules.
from Modules.Core.data_objects import RiseSetData
from Modules.Computer.Mqtt.mqtt import API as mqttAPI
from Modules.Housing.test.xml_housing import TESTING_HOUSE_DIVISION
from Modules.Housing.Scheduling import schedule
from Modules.Housing.Scheduling.schedule_xml import Xml as scheduleXml
from Modules.Housing.Scheduling.schedule import \
        SchedTime, ScheduleExecution, \
        API as scheduleAPI, \
        Utility as scheduleUtility
from Modules.Housing.Scheduling.test.xml_schedule import \
    TESTING_SCHEDULE_NAME_0, \
    TESTING_SCHEDULE_NAME_1, \
    TESTING_SCHEDULE_NAME_2, \
    TESTING_SCHEDULE_NAME_3, \
    TESTING_SCHEDULE_SUNRISE_0, \
    TESTING_SCHEDULE_SUNSET_0, \
    TESTING_SCHEDULE_SECTION, \
    TESTING_SCHEDULE, \
    TESTING_SCHEDULE_DAWN_0, \
    TESTING_SCHEDULE_DUSK_0, \
    TESTING_SCHEDULE_NOON_0
from test.xml_data import XML_LONG, TESTING_PYHOUSE
from test.testing_mixin import SetupPyHouseObj
from Modules.Core.Utilities.debug_tools import PrettyFormatAny

T_TODAY = datetime.datetime(2015, 6, 6, 12, 34, 56)
#
T_SUNDAY = datetime.datetime(2015, 6, 7, 1, 2, 3)
DOW_SUNDAY = 64
T_MONDAY = datetime.datetime(2015, 6, 8, 1, 2, 3)
DOW_MONDAY = 1
T_TUESDAY = datetime.datetime(2015, 6, 9, 1, 2, 3)
DOW_TUESDAY = 2
T_WEDNESDAY = datetime.datetime(2015, 6, 10, 1, 2, 3)
DOW_WEDNESDAY = 4
T_THURSDAY = datetime.datetime(2015, 6, 11, 1, 2, 3)
DOW_THURSDAY = 8
T_FRIDAY = datetime.datetime(2015, 6, 12, 1, 2, 3)
DOW_FRIDAY = 16
T_SATURDAY = datetime.datetime(2015, 6, 13, 1, 2, 3)
DOW_SATURDAY = 32


def get_seconds(p_datetime):
    l_ret = ((p_datetime.hour * 60) + p_datetime.minute) * 60
    return l_ret


class Mock(object):
    """
    A fake module to get sunrise and sunset.
    Replaces sunrisesunset.py for testing purposes.
    """

    @staticmethod
    def RiseSet():
        l_ret = RiseSetData()
        l_ret.Dawn = TESTING_SCHEDULE_DAWN_0
        l_ret.SunRise = TESTING_SCHEDULE_SUNRISE_0
        l_ret.Noon = TESTING_SCHEDULE_NOON_0
        l_ret.SunSet = TESTING_SCHEDULE_SUNSET_0
        l_ret.Dusk = TESTING_SCHEDULE_DUSK_0
        return l_ret


class SetupMixin(object):

    def setUp(self, p_root):
        self.m_pyhouse_obj = SetupPyHouseObj().BuildPyHouseObj(p_root)
        self.m_xml = SetupPyHouseObj().BuildXml(p_root)

        self.m_pyhouse_obj.House.Location.RiseSet = Mock.RiseSet()
        self.m_api = scheduleAPI(self.m_pyhouse_obj)
        self.m_schedules = scheduleXml.read_schedules_xml(self.m_pyhouse_obj)
        self.m_pyhouse_obj.House.Schedule = self.m_schedules
        self.m_schedule_obj = self.m_schedules[0]
        # twisted.internet.base.DelayedCall.debug = True
        # self.m_pyhouse_obj.House.FamilyData = familyAPI(self.m_pyhouse_obj).LoadFamilyTesting()
        # self.m_now = datetime.datetime(2016, 8, 13, 11, 12, 0)


class A0(unittest.TestCase):

    def setUp(self):
        pass

    def test_00_Print(self):
        print('Id: test_schedule')


class A1_Setup(SetupMixin, unittest.TestCase):
    """
    Uses DOW and todays delay to get delay time in minutes.
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))

    def test_01_Tags(self):
        """ Just to be sure the family data is loaded properly.
        """
        # print(PrettyFormatAny.form(self.m_xml, 'A1-01-A - Tags'))
        self.assertEqual(self.m_xml.root.tag, TESTING_PYHOUSE)
        self.assertEqual(self.m_xml.house_div.tag, TESTING_HOUSE_DIVISION)
        self.assertEqual(self.m_xml.schedule_sect.tag, TESTING_SCHEDULE_SECTION)
        self.assertEqual(self.m_xml.schedule.tag, TESTING_SCHEDULE)

    def test_02_FamilyData(self):
        """ Just to be sure the family data is loaded properly.
        """
        # print(PrettyFormatAny.form(self.m_pyhouse_obj.House.FamilyData, 'A1-2-A - FamilyData'))
        self.assertEqual(self.m_pyhouse_obj.House.FamilyData['Insteon'].Name, 'Insteon')
        self.assertEqual(self.m_pyhouse_obj.House.FamilyData['Null'].Name, 'Null')
        self.assertEqual(self.m_pyhouse_obj.House.FamilyData['UPB'].Name, 'UPB')
        self.assertEqual(self.m_pyhouse_obj.House.FamilyData['X10'].Name, 'X10')
        self.assertEqual(self.m_pyhouse_obj.House.FamilyData['Insteon'].Key, 1)
        self.assertEqual(self.m_pyhouse_obj.House.FamilyData['Null'].Key, 0)
        self.assertEqual(self.m_pyhouse_obj.House.FamilyData['UPB'].Key, 2)
        self.assertEqual(self.m_pyhouse_obj.House.FamilyData['X10'].Key, 3)
        self.assertEqual(self.m_pyhouse_obj.House.FamilyData['Null'].Active, True)

    def test_03_Dawn(self):
        pass


class A2_XML(SetupMixin, unittest.TestCase):
    """
    Be sure that we load the data properly as a whole test.
    Detailed test of xml is in the test_schedule_xml module.
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))
        self.m_api = scheduleAPI(self.m_pyhouse_obj)

    def test_1_Load(self):
        """ Test loading of schedule data.
        """
        l_obj = self.m_api.LoadXml(self.m_pyhouse_obj)
        # print(PrettyFormatAny.form(l_obj, 'A2-1-A - PyHouse'))
        self.assertEqual(l_obj[0].Name, TESTING_SCHEDULE_NAME_0)
        self.assertEqual(l_obj[1].Name, TESTING_SCHEDULE_NAME_1)
        self.assertEqual(l_obj[2].Name, TESTING_SCHEDULE_NAME_2)
        self.assertEqual(l_obj[3].Name, TESTING_SCHEDULE_NAME_3)


class A3_Utility(SetupMixin, unittest.TestCase):
    """
    Testing conversion and extraction
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))

    def test_01_Mins(self):
        """Convert a datetime to Minutes
        """
        l_minutes = schedule.to_minutes(T_TODAY)
        # print(PrettyFormatAny.form(l_minutes, 'A3-1-A - Minutes'))
        self.assertEqual(l_minutes, 12 * 60 + 34)
        l_minutes = schedule.to_minutes(TESTING_SCHEDULE_DAWN_0)
        self.assertEqual(l_minutes, TESTING_SCHEDULE_DAWN_0.hour * 60 + TESTING_SCHEDULE_DAWN_0.minute)
        l_minutes = schedule.to_minutes(TESTING_SCHEDULE_SUNRISE_0)
        self.assertEqual(l_minutes, TESTING_SCHEDULE_SUNRISE_0.hour * 60 + TESTING_SCHEDULE_SUNRISE_0.minute)
        l_minutes = schedule.to_minutes(TESTING_SCHEDULE_NOON_0)
        self.assertEqual(l_minutes, TESTING_SCHEDULE_NOON_0.hour * 60 + TESTING_SCHEDULE_NOON_0.minute)
        l_minutes = schedule.to_minutes(TESTING_SCHEDULE_SUNSET_0)
        self.assertEqual(l_minutes, TESTING_SCHEDULE_SUNSET_0.hour * 60 + TESTING_SCHEDULE_SUNSET_0.minute)
        l_minutes = schedule.to_minutes(TESTING_SCHEDULE_DUSK_0)
        self.assertEqual(l_minutes, TESTING_SCHEDULE_DUSK_0.hour * 60 + TESTING_SCHEDULE_DUSK_0.minute)

    def test_02_Mock(self):
        # print(PrettyFormatAny.form(Mock.RiseSet(), 'A3-02-A - Mock'))
        pass


class B1_Days(SetupMixin, unittest.TestCase):
    """ Using the DOW field, get the number of days until the next schedule occurrence.
    Tests _extract_days.
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))

    def test_01_0_Days(self):
        """ Date is within DOW value
        """
        self.m_schedule_obj.DOW = 127  # All 7 days in a bit mask
        l_days = SchedTime._extract_days(self.m_schedule_obj, T_WEDNESDAY)
        self.assertEqual(l_days, 0)
        self.m_schedule_obj.DOW = DOW_WEDNESDAY
        l_days = SchedTime._extract_days(self.m_schedule_obj, T_WEDNESDAY)
        # print(PrettyFormatAny.form(l_days, 'B1-01-A - Days'))
        self.assertEqual(l_days, 0)

    def test_02_1_Day(self):
        """ Date will be tomorrow
        """
        self.m_schedule_obj.DOW = DOW_THURSDAY
        l_days = SchedTime._extract_days(self.m_schedule_obj, T_WEDNESDAY)
        self.assertEqual(l_days, 1)
        self.m_schedule_obj.DOW = 127 - DOW_WEDNESDAY
        l_days = SchedTime._extract_days(self.m_schedule_obj, T_WEDNESDAY)
        # print(PrettyFormatAny.form(l_days, 'B1-02-A - Days'))
        self.assertEqual(l_days, 1)

    def test_03_2_Days(self):
        """ Date will be in 2 days
        """
        self.m_schedule_obj.DOW = DOW_FRIDAY
        l_days = SchedTime._extract_days(self.m_schedule_obj, T_WEDNESDAY)
        # print(PrettyFormatAny.form(l_days, 'B1-03-A - Days'))
        self.assertEqual(l_days, 2)

    def test_04_3_Days(self):
        """ Date will be in 3 days
        """
        self.m_schedule_obj.DOW = DOW_SATURDAY
        l_days = SchedTime._extract_days(self.m_schedule_obj, T_WEDNESDAY)
        # print(PrettyFormatAny.form(l_days, 'B1-04-A - Days'))
        self.assertEqual(l_days, 3)

    def test_05_4_Days(self):
        """ Date will be in 4 days
        """
        self.m_schedule_obj.DOW = DOW_SUNDAY
        l_days = SchedTime._extract_days(self.m_schedule_obj, T_WEDNESDAY)
        # print(PrettyFormatAny.form(l_days, 'B1-05-A - Days'))
        self.assertEqual(l_days, 4)

    def test_06_5_Days(self):
        """ Date will be in 5 days
        """
        self.m_schedule_obj.DOW = DOW_MONDAY
        l_days = SchedTime._extract_days(self.m_schedule_obj, T_WEDNESDAY)
        # print(PrettyFormatAny.form(l_days, 'B1-06-A - Days'))
        self.assertEqual(l_days, 5)

    def test_07_6_Days(self):
        """ Date will be in 6 days
        """
        self.m_schedule_obj.DOW = DOW_TUESDAY
        l_days = SchedTime._extract_days(self.m_schedule_obj, T_WEDNESDAY)
        # print(PrettyFormatAny.form(l_days, 'B1-07-A - Days'))
        self.assertEqual(l_days, 6)

    def test_08_7_PlusDays(self):
        """ Date will be Never
        """
        self.m_schedule_obj.DOW = 0
        l_days = SchedTime._extract_days(self.m_schedule_obj, T_WEDNESDAY)
        # print(PrettyFormatAny.form(l_days, 'B1-08-A - Days'))
        self.assertEqual(l_days, 10)


class B2_Extract(SetupMixin, unittest.TestCase):
    """
    The number of minutes from midnight to the scheduled time.
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))
        self.m_schedule_obj.DOW = 1 + 2 + 4 + 8 + 16 + 32 + 64
        self.m_riseset = Mock.RiseSet()

    def test_01_Time(self):
        """ Extract Minutes from Midnight to schedule time
        """
        self.m_schedule_obj.Time = '01:02'
        l_minutes = SchedTime._extract_schedule_time(self.m_schedule_obj, self.m_riseset)
        # print('B2-01-A - Minutes {}\n'.format(l_minutes))
        self.assertEqual(l_minutes, 1 * 60 + 2)

    def test_02_Dawn(self):
        """ Extract Minutes from Midnight to schedule time
        """
        self.m_schedule_obj.Time = 'dawn'
        l_minutes = SchedTime._extract_schedule_time(self.m_schedule_obj, self.m_riseset)
        # print('\nB2-02-A - Minutes {}\n'.format(l_minutes))
        self.assertEqual(l_minutes, 6 * 60 + 4)

    def test_03_DawnPlus(self):
        """ Extract Minutes from Midnight to schedule time
        """
        self.m_schedule_obj.Time = 'dawn + 0:10'
        l_minutes = SchedTime._extract_schedule_time(self.m_schedule_obj, self.m_riseset)
        # print('\nB2-03-A - Minutes {}\n'.format(l_minutes))
        self.assertEqual(l_minutes, 6 * 60 + 4 + 10)

    def test_04_DawnMinus(self):
        """ Extract Minutes from Midnight to schedule time
        """
        self.m_schedule_obj.Time = 'dawn - 0:10'
        l_minutes = SchedTime._extract_schedule_time(self.m_schedule_obj, self.m_riseset)
        # print('\nB2-04-A - Minutes {}\n'.format(l_minutes))
        self.assertEqual(l_minutes, 6 * 60 + 4 - 10)

    def test_05_Noon(self):
        """ Extract Minutes from Midnight to schedule time
        """
        self.m_schedule_obj.Time = 'noon'
        l_minutes = SchedTime._extract_schedule_time(self.m_schedule_obj, self.m_riseset)
        # print('\nB2-05-A - Minutes {}\n'.format(l_minutes))
        self.assertEqual(l_minutes, 13 * 60 + 31)

    def test_06_Sunset(self):
        """ Extract Minutes from Midnight to schedule time
        """
        self.m_schedule_obj.Time = 'sunset'
        l_minutes = SchedTime._extract_schedule_time(self.m_schedule_obj, self.m_riseset)
        # print('\nB2-06-A - Minutes {}\n'.format(l_minutes))
        self.assertEqual(l_minutes, 20 * 60 + 31)

    def test_07_Dusk(self):
        """ Extract Minutes from Midnight to schedule time
        """
        self.m_schedule_obj.Time = 'dusk'
        l_minutes = SchedTime._extract_schedule_time(self.m_schedule_obj, self.m_riseset)
        # print('\nB2-07-A - Minutes {}\n'.format(l_minutes))
        self.assertEqual(l_minutes, 20 * 60 + 58)

    def test_08_DawnPlus(self):
        """ Extract Minutes from Midnight to schedule time
        """
        self.m_schedule_obj.Time = 'dawn + 0:10'
        l_minutes = SchedTime._extract_schedule_time(self.m_schedule_obj, self.m_riseset)
        # print('\nB2-08-A - Minutes {}\n'.format(l_minutes))
        self.assertEqual(l_minutes, 6 * 60 + 4 + 10)


class B3_Time(SetupMixin, unittest.TestCase):
    """
    Test the time from now to the schedule time
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))
        self.m_schedule_obj.DOW = 1 + 2 + 4 + 8 + 16 + 32 + 64
        self.m_riseset = Mock.RiseSet()
        self.m_now = datetime.datetime(2016, 8, 13, 11, 12, 0)

    def test_01_ToGo(self):
        """ Time = 11:13
            Now  = 11:12
        """
        self.m_schedule_obj.Time = '11:13'
        l_seconds = SchedTime.extract_time_to_go(self.m_pyhouse_obj, self.m_schedule_obj, self.m_now, self.m_riseset)
        # print('\nB3-01-A - Minutes: {}'.format(l_seconds / 60))
        self.assertEqual(l_seconds, 60)

    def test_02_Sunset(self):
        """ Sunset = 20:31
            Now    = 11:12
        """
        self.m_schedule_obj.Time = 'Sunset'
        l_seconds = SchedTime.extract_time_to_go(self.m_pyhouse_obj, self.m_schedule_obj, self.m_now, self.m_riseset)
        # print('\nB3-02-A - Minutes: {}'.format(l_seconds / 60))
        self.assertEqual(l_seconds, 9 * 3600 + 19 * 60)

    def test_03_SunsetPlus(self):
        """ Sunset = 20:31:25
            Now    = 11:12
            Plus   = 00:21
        """
        self.m_schedule_obj.Time = 'sunset + 00:21'
        l_seconds = SchedTime.extract_time_to_go(self.m_pyhouse_obj, self.m_schedule_obj, self.m_now, self.m_riseset)
        # print('B3-03-A - Minutes: {}'.format(l_seconds / 60))
        self.assertEqual(l_seconds, 20 * 3600 - 11 * 3600 + 31 * 60 - 12 * 60 + 21 * 60)

    def test_04_Tomorrow(self):
        """ Test for tomorrow morning
            Tomorrow = 24:00
            Now      = 11:12
                       12:48
                       03:02
                       15:50

        """
        self.m_schedule_obj.DOW = 1 + 2 + 4 + 8 + 16 + 0 + 64  # Not today
        self.m_schedule_obj.Time = '03:02'
        l_seconds = SchedTime.extract_time_to_go(self.m_pyhouse_obj, self.m_schedule_obj, self.m_now, self.m_riseset)
        # print('B3-04-A - Minutes: {}'.format(self.m_now.weekday()))
        self.assertEqual(l_seconds, 15 * 3600 + 50 * 60)

    def test_05_ToGo(self):
        """ Test next day 45 mins from now
        """
        self.m_schedule_obj.Time = '11:10'
        l_seconds = SchedTime.extract_time_to_go(self.m_pyhouse_obj, self.m_schedule_obj, self.m_now, self.m_riseset)
        # print('B3-05-A - Minutes {}'.format(l_seconds / 60))
        self.assertEqual(l_seconds, 23 * 3600 + 58 * 60)


class B4_Dawn(SetupMixin, unittest.TestCase):
    """
    The number of minutes from midnight to the scheduled time.
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))
        self.m_schedule_obj.DOW = 1 + 2 + 4 + 8 + 16 + 32 + 64
        self.m_riseset = Mock.RiseSet()

    def test_01_TillSched(self):
        """ Extract Minutes from Midnight to schedule time

        20:58:30

        """
        self.m_schedule_obj.Time = 'Dusk'
        l_minutes = SchedTime._extract_schedule_time(self.m_schedule_obj, self.m_riseset)
        # print(PrettyFormatAny.form(l_minutes, 'B4-01-A - Minutes'))
        self.assertEqual(l_minutes, 20 * 60 + 58)

    def test_02_TillSched(self):
        self.m_schedule_obj.Time = 'dusk'
        l_minutes = SchedTime._extract_schedule_time(self.m_schedule_obj, self.m_riseset)
        # print(PrettyFormatAny.form(l_minutes, 'B4-02-A - Minutes'))
        self.assertEqual(l_minutes, TESTING_SCHEDULE_DUSK_0.hour * 60 + TESTING_SCHEDULE_DUSK_0.minute)

    def test_03_TillSched(self):
        self.m_schedule_obj.Time = 'sunrise'
        l_minutes = SchedTime._extract_schedule_time(self.m_schedule_obj, self.m_riseset)
        # print(PrettyFormatAny.form(l_minutes, 'B4-03-A - Minutes'))
        self.assertEqual(l_minutes, TESTING_SCHEDULE_SUNRISE_0.hour * 60 + TESTING_SCHEDULE_SUNRISE_0.minute)

    def test_04_TillSched(self):
        self.m_schedule_obj.Time = 'sunset + 0:10'
        l_minutes = SchedTime._extract_schedule_time(self.m_schedule_obj, self.m_riseset)
        # print(PrettyFormatAny.form(l_minutes, 'B4-04-A - Minutes'))
        self.assertEqual(l_minutes, TESTING_SCHEDULE_SUNSET_0.hour * 60 + TESTING_SCHEDULE_SUNSET_0.minute + 10)

    def test_05_TillSched(self):
        self.m_schedule_obj.Time = 'sunset - 0:17'
        l_minutes = SchedTime._extract_schedule_time(self.m_schedule_obj, self.m_riseset)
        # print(PrettyFormatAny.form(l_minutes, 'B4-05-A - Minutes'))
        self.assertEqual(l_minutes, TESTING_SCHEDULE_SUNSET_0.hour * 60 + TESTING_SCHEDULE_SUNSET_0.minute - 17)


class C1_Execute(SetupMixin, unittest.TestCase):
    """Testing class ScheduleExecution
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))
        self.m_pyhouse_obj.House.Schedules = scheduleXml.read_schedules_xml(self.m_pyhouse_obj)
        self.m_pyhouse_obj.APIs.Computer.MqttAPI = mqttAPI(self.m_pyhouse_obj)

    def test_01_one(self):
        """ No way to test the dispatch routine
        """
        self.m_pyhouse_obj.House.Schedules[0].ScheduleType = 'TeStInG14159'  # to set dispatch to testing
        l_schedule = self.m_pyhouse_obj.House.Schedules[0]
        # print(PrettyFormatAny.form(l_schedule, 'C1-01-A - Sched'))
        ScheduleExecution.dispatch_one_schedule(self.m_pyhouse_obj, l_schedule)
        self.assertEqual(True, True)

    def XXtest_02_All(self):
        """ No way to thest this either.
        """
        l_list = [0, 1]
        self.m_pyhouse_obj.House.Schedules[0].ScheduleType = 'TeStInG14159'
        self.m_pyhouse_obj.House.Schedules[1].ScheduleType = 'TeStInG14159'
        ScheduleExecution.execute_schedules_list(self.m_pyhouse_obj, l_list)
        self.assertEqual(True, True)


class C2_List(SetupMixin, unittest.TestCase):
    """
    This section tests the Building of a schedule list
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))
        self.m_pyhouse_obj.House.Schedules = scheduleXml.read_schedules_xml(self.m_pyhouse_obj)
        self.m_pyhouse_obj.APIs.Computer.MqttAPI = mqttAPI(self.m_pyhouse_obj)
        # twisted.internet.base.DelayedCall.debug = True

    def test_01_BuildSched(self):
        """ Testing the build of a schedule list.
        We should end up with 2 schedules in the list.
        """
        l_riseset = Mock.RiseSet()
        l_delay, l_list = scheduleUtility.find_next_scheduled_events(self.m_pyhouse_obj, T_TODAY)
        l_now_sec = schedule.to_minutes(T_TODAY) * 60
        l_obj = self.m_pyhouse_obj.House.Schedules[l_list[0]]
        l_sched_sec = SchedTime._extract_schedule_time(l_obj, l_riseset) * 60
        # print('C2-01-A - Delay: {}; List: {}; Now: {}; Sched: {}'.format(l_delay, l_list, l_now_sec, l_sched_sec))
        self.assertEqual(len(l_list), 2)
        self.assertEqual(l_delay, l_sched_sec - l_now_sec)
        self.assertEqual(l_list[0], 0)
        self.assertEqual(l_list[1], 1)

    def test_02_Load(self):
        """ Test ???
        """
        SetupPyHouseObj().LoadHouse(self.m_pyhouse_obj)
        # print(PrettyFormatAny.form(self.m_pyhouse_obj.House, 'C2-02-A - PyHouse.House 1'))

    def XXtest_03_Sched(self):
        SetupPyHouseObj().LoadHouse(self.m_pyhouse_obj)
        # print(PrettyFormatAny.form(self.m_pyhouse_obj.House, 'C2-03-A - PyHouse.House 1'))
        l_delay = 1
        _l_list = [0, 1]
        _l_id = scheduleUtility.schedule_next_event(self.m_pyhouse_obj, l_delay)
        time.sleep(2 * l_delay)
        # l_id.cancel()

    def Xtest_04_RunSchedule(self):
        pass

    def Xtest_05_SchedulesList(self):
        pass

    def Xtest_07_OneSchedule(self):
        pass
        self.m_api.dispatch_one_schedule(3)

    def Xtest_09_DispatchSchedule(self):
        pass


class C5_Full(SetupMixin, unittest.TestCase):
    """
    This section tests the Building of a schedule list
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))
        # self.m_pyhouse_obj.House.Schedules = scheduleXml.read_schedules_xml(self.m_pyhouse_obj)
        self.m_timefield = 0

    def test_01_SubstituteTime(self):
        # self.m_api._substitute_time(self.m_timefield)
        pass

    def test_55_Next(self):
        # l_delay, l_list = self.m_api.find_next_scheduled_event(self.m_pyhouse_obj)
        pass

# ## END
