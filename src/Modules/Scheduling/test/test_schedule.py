"""
@name:      PyHouse/src/Modules/Scheduling/test/test_schedule.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2013-2015 by D. Brian Kimmel
@license:   MIT License
@note:      Created on Apr 8, 2013
@summary:   Test handling the schedule information for a house.

Passed all 18 tests - DBK - 2015-09-10

"""

# Import system type stuff
import datetime
import xml.etree.ElementTree as ET
from twisted.trial import unittest
import twisted
import time

# Import PyMh files and modules.
from Modules.Core.data_objects import RiseSetData
from Modules.Computer.Mqtt.mqtt_client import API as mqttAPI
from Modules.Families.family import API as familyAPI
from Modules.Scheduling.schedule import \
        SchedTime, ScheduleExecution, \
        API as scheduleAPI, \
        Utility as scheduleUtility
from Modules.Scheduling.schedule_xml import Xml as scheduleXml
from test.xml_data import XML_LONG
from test.testing_mixin import SetupPyHouseObj
from Modules.Utilities.debug_tools import PrettyFormatAny
# from Modules.Utilities.debug_tools import PrettyFormatAny


T_NOW = datetime.datetime(2015, 6, 6, 12, 34, 56)
T_SUNRISE = datetime.datetime(2015, 6, 6, 7, 12, 34)
T_SUNSET = datetime.datetime(2015, 6, 6, 20, 19, 18)
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


class Mock(object):
    """
    A fake module to get sunrise and sunset.
    Replaces sunrisesunset.py for testing purposes.
    """

    @staticmethod
    def RiseSet():
        l_ret = RiseSetData()
        l_ret.SunRise = T_SUNRISE
        l_ret.SunSet = T_SUNSET
        return l_ret


class SetupMixin(object):

    def setUp(self, p_root):
        self.m_pyhouse_obj = SetupPyHouseObj().BuildPyHouseObj(p_root)
        self.m_pyhouse_obj.House.Location.RiseSet = Mock.RiseSet()
        self.m_xml = SetupPyHouseObj().BuildXml(p_root)
        self.m_api = scheduleAPI(self.m_pyhouse_obj)
        self.m_schedules = scheduleXml.read_schedules_xml(self.m_pyhouse_obj)
        self.m_pyhouse_obj.House.Schedule = self.m_schedules
        self.m_schedule_obj = self.m_schedules[0]
        twisted.internet.base.DelayedCall.debug = True
        self.m_pyhouse_obj.House.FamilyData = familyAPI(self.m_pyhouse_obj).LoadFamilyTesting()


class A1_Setup(SetupMixin, unittest.TestCase):
    """
    Uses DOW and todays delay to get delay time in minutes.
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))

    def test_01_FamilyData(self):
        """Date is in DOW
        """
        # print(PrettyFormatAny.form(self.m_pyhouse_obj.House.FamilyData, 'FamilyData'))
        self.assertEqual(self.m_pyhouse_obj.House.FamilyData['Null'].Name, 'Null')
        self.assertEqual(self.m_pyhouse_obj.House.FamilyData['Null'].Key, 0)
        self.assertEqual(self.m_pyhouse_obj.House.FamilyData['Null'].Active, True)


class A2_Utility(SetupMixin, unittest.TestCase):
    """
    Uses DOW and todays delay to get delay time in minutes.
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))

    def test_01_Mins(self):
        """Date is in DOW
        """
        l_minutes = scheduleUtility.to_mins(T_NOW)
        self.assertEqual(l_minutes, 12 * 60 + 34)
        l_minutes = scheduleUtility.to_mins(T_SUNRISE)
        self.assertEqual(l_minutes, 7 * 60 + 12)
        l_minutes = scheduleUtility.to_mins(T_SUNSET)
        self.assertEqual(l_minutes, 20 * 60 + 19)


class B1_Days(SetupMixin, unittest.TestCase):
    """Get days till next schedule
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))

    def test_01_0_Days(self):
        """Date is in DOW
        """
        self.m_schedule_obj.DOW = 127
        l_days = SchedTime._extract_days(self.m_schedule_obj, T_WEDNESDAY)
        self.assertEqual(l_days, 0)
        self.m_schedule_obj.DOW = DOW_WEDNESDAY
        l_days = SchedTime._extract_days(self.m_schedule_obj, T_WEDNESDAY)
        self.assertEqual(l_days, 0)

    def test_02_1_Day(self):
        """Date will be tomorrow
        """
        self.m_schedule_obj.DOW = DOW_THURSDAY
        l_days = SchedTime._extract_days(self.m_schedule_obj, T_WEDNESDAY)
        self.assertEqual(l_days, 1)
        self.m_schedule_obj.DOW = 127 - DOW_WEDNESDAY
        l_days = SchedTime._extract_days(self.m_schedule_obj, T_WEDNESDAY)
        self.assertEqual(l_days, 1)

    def test_03_2_Days(self):
        """Date will be in 2 days
        """
        self.m_schedule_obj.DOW = DOW_FRIDAY
        l_days = SchedTime._extract_days(self.m_schedule_obj, T_WEDNESDAY)
        self.assertEqual(l_days, 2)

    def test_04_3_Days(self):
        """Date will be in 3 days
        """
        self.m_schedule_obj.DOW = DOW_SATURDAY
        l_days = SchedTime._extract_days(self.m_schedule_obj, T_WEDNESDAY)
        self.assertEqual(l_days, 3)

    def test_05_4_Days(self):
        """Date will be in 4 days
        """
        self.m_schedule_obj.DOW = DOW_SUNDAY
        l_days = SchedTime._extract_days(self.m_schedule_obj, T_WEDNESDAY)
        self.assertEqual(l_days, 4)

    def test_06_5_Days(self):
        """Date will be in 5 days
        """
        self.m_schedule_obj.DOW = DOW_MONDAY
        l_days = SchedTime._extract_days(self.m_schedule_obj, T_WEDNESDAY)
        self.assertEqual(l_days, 5)

    def test_07_6_Days(self):
        """Date will be in 6 days
        """
        self.m_schedule_obj.DOW = DOW_TUESDAY
        l_days = SchedTime._extract_days(self.m_schedule_obj, T_WEDNESDAY)
        self.assertEqual(l_days, 6)

    def test_08_7_PlusDays(self):
        """Date will be Never
        """
        self.m_schedule_obj.DOW = 0
        l_days = SchedTime._extract_days(self.m_schedule_obj, T_WEDNESDAY)
        self.assertEqual(l_days, 10)


class B2_Time(SetupMixin, unittest.TestCase):
    """
    The number of minutes from midnight to the scheduled .
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))
        self.m_schedule_obj.DOW = 1 + 2 + 4 + 8 + 16 + 32 + 64

    def test_01_TillSched(self):
        """Date is
        """
        l_riseset = Mock.RiseSet()
        self.m_schedule_obj.Time = '01:02'
        l_minutes = SchedTime._extract_schedule_time(self.m_schedule_obj, l_riseset)
        self.assertEqual(l_minutes, 1 * 60 + 2)
        #
        self.m_schedule_obj.Time = 'dusk'
        l_minutes = SchedTime._extract_schedule_time(self.m_schedule_obj, l_riseset)
        self.assertEqual(l_minutes, 20 * 60 + 19)
        #
        self.m_schedule_obj.Time = 'sunrise'
        l_minutes = SchedTime._extract_schedule_time(self.m_schedule_obj, l_riseset)
        self.assertEqual(l_minutes, 7 * 60 + 12)
        #
        self.m_schedule_obj.Time = 'sunset + 0:10'
        l_minutes = SchedTime._extract_schedule_time(self.m_schedule_obj, l_riseset)
        self.assertEqual(l_minutes, 20 * 60 + 19 + 10)
        #
        self.m_schedule_obj.Time = 'sunset - 0:17'
        l_minutes = SchedTime._extract_schedule_time(self.m_schedule_obj, l_riseset)
        self.assertEqual(l_minutes, 20 * 60 + 19 - 17)

    def test_02_ToGo(self):
        """Date is
        """
        self.m_schedule_obj.DOW = 1 + 2 + 4 + 8 + 16 + 32 + 64
        l_riseset = Mock.RiseSet()
        self.m_schedule_obj.Time = '01:02'
        l_minutes = SchedTime.extract_time_to_go(self.m_schedule_obj, T_NOW, l_riseset)
        self.assertEqual(l_minutes, (1 * 60 + 2) * 60)
        #
        self.m_schedule_obj.Time = 'dawn'
        l_minutes = SchedTime.extract_time_to_go(self.m_schedule_obj, T_NOW, l_riseset)
        self.assertEqual(l_minutes, (7 * 60 + 12) * 60)
        #
        self.m_schedule_obj.DOW = 1 + 2 + 4 + 8 + 16 + 0 + 64
        l_riseset = Mock.RiseSet()
        self.m_schedule_obj.Time = '01:02'
        l_minutes = SchedTime.extract_time_to_go(self.m_schedule_obj, T_NOW, l_riseset)
        self.assertEqual(l_minutes, (1 * 60 + 2 + 1440) * 60)


class C1_Execute(SetupMixin, unittest.TestCase):

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))
        self.m_pyhouse_obj.House.Schedules = scheduleXml.read_schedules_xml(self.m_pyhouse_obj)
        self.m_pyhouse_obj.APIs.Computer.MqttAPI = mqttAPI(self.m_pyhouse_obj)

    def test_01_one(self):
        self.assertEqual(True, True)

    def test_01_All(self):
        l_list = [1, 2]
        self.m_pyhouse_obj.House.Schedule[1].ScheduleType = 'TeStInG14159'
        self.m_pyhouse_obj.House.Schedule[2].ScheduleType = 'TeStInG14159'
        ScheduleExecution.execute_schedules_list(self.m_pyhouse_obj, l_list)
        self.assertEqual(True, True)


class C2_Setup(SetupMixin, unittest.TestCase):
    """
    This section tests the Building of a schedule list
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))
        self.m_pyhouse_obj.House.Schedules = scheduleXml.read_schedules_xml(self.m_pyhouse_obj)
        self.m_pyhouse_obj.APIs.Computer.MqttAPI = mqttAPI(self.m_pyhouse_obj)
        twisted.internet.base.DelayedCall.debug = True

    def tearDown(self):
        pass

    def test_01_BuildSched(self):
        l_delay, l_list = scheduleUtility.find_next_scheduled_events(self.m_pyhouse_obj, T_NOW)
        # print('Delay: {} {}'.format(l_delay, l_list))
        self.assertEqual(len(l_list), 2)
        self.assertEqual(l_delay, 50220)
        self.assertEqual(l_list[0], 0)
        self.assertEqual(l_list[1], 1)

    def test_02_Load(self):
        SetupPyHouseObj().LoadHouse(self.m_pyhouse_obj)
        print(PrettyFormatAny.form(self.m_pyhouse_obj.House, 'PyHouse.House 1'))

    def test_03_Sched(self):
        SetupPyHouseObj().LoadHouse(self.m_pyhouse_obj)
        # print(PrettyFormatAny.form(self.m_pyhouse_obj.House, 'PyHouse.House 1'))
        l_delay = 1
        l_list = [0, 1]
        l_id = scheduleUtility.schedule_next_event(self.m_pyhouse_obj, l_delay)
        time.sleep(2 * l_delay)
        # l_id.cancel()

    def Xtest_04_RunSchedule(self):
        pass

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
