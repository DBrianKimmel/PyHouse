"""
@name:      PyHouse/src/Modules/Scheduling/test/test_schedule.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2013-2019 by D. Brian Kimmel
@license:   MIT License
@note:      Created on Apr 8, 2013
@summary:   Test handling the schedule information for a house.

Passed all 44 tests - DBK - 2019-01-26

There are some tests (starting with 'X') that I do not know how to do in twisted.

"""
from Modules.Core.Utilities import convert

__updated__ = '2019-03-07'

# Import system type stuff
import datetime
import xml.etree.ElementTree as ET
from twisted.trial import unittest
import time
import twisted
# from twisted.test import proto_helpers

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
    TESTING_SCHEDULE_NOON_0, \
    XML_SCHEDULE, \
    L_SCHEDULE_SECTION_START, \
    TESTING_SCHEDULE_DOW_0
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


def to_dhms(p_seconds):
    """ Convert seconds to a datetime
    Mostly used for testing to allow seconds to be displayed more clearly.
    """
    l_ret = datetime.datetime(1970, 1, 1, 0, tzinfo=None)
    l_ret = l_ret.fromtimestamp(p_seconds)
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
        # self.m_schedules = scheduleXml.read_schedules_xml(self.m_pyhouse_obj)
        # self.m_pyhouse_obj.House.Schedule = self.m_schedules
        # self.m_schedule_obj = self.m_schedules
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
        # print(PrettyFormatAny.form(self.m_pyhouse_obj.House.FamilyData, 'A1-02-A - FamilyData'))
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
        """ Test that dusk dawn loaded properly
        """
        # print(PrettyFormatAny.form(self.m_pyhouse_obj.House.Location.RiseSet, 'A1-03-A - Dusk Dawn'))
        self.assertEqual(self.m_pyhouse_obj.House.Location.RiseSet.Dawn, TESTING_SCHEDULE_DAWN_0)


class A2_SetupXml(SetupMixin, unittest.TestCase):
    """ Test that the XML contains no syntax errors.
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring('<x />'))
        pass

    def test_01_Raw(self):
        l_raw = XML_SCHEDULE
        # print('A2-01-A - Raw\n{}'.format(l_raw))
        self.assertEqual(l_raw[:16], L_SCHEDULE_SECTION_START[:16])

    def test_02_Parsed(self):
        l_xml = ET.fromstring(XML_SCHEDULE)
        # print('A2-02-A - Parsed\n{}'.format(PrettyFormatAny.form(l_xml, 'A2-02-A - Parsed')))
        self.assertEqual(l_xml.tag, TESTING_SCHEDULE_SECTION)


class A3_Utility(SetupMixin, unittest.TestCase):
    """
    Testing conversion and extraction
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))
        self.m_schedules = scheduleXml.read_schedules_xml(self.m_pyhouse_obj)
        self.m_pyhouse_obj.House.Schedule = self.m_schedules
        self.m_schedule_obj = self.m_schedules[0]

    def test_02_Mock(self):
        # print(PrettyFormatAny.form(Mock.RiseSet(), 'A3-02-A - Mock'))
        pass

    def test_03_schedules(self):
        # print(PrettyFormatAny.form(self.m_schedules, 'A3-03-A - schedules'))
        # print(PrettyFormatAny.form(self.m_schedules[0], 'A3-03-B - schedules[0]'))
        # print(PrettyFormatAny.form(self.m_schedule_obj, 'A3-03-C - schedule_obj'))
        self.assertEqual(str(self.m_schedules[0].DOW), TESTING_SCHEDULE_DOW_0)
        self.assertEqual(str(self.m_schedule_obj.DOW), TESTING_SCHEDULE_DOW_0)


class B1_Global(SetupMixin, unittest.TestCase):
    """ Using the DOW field, get the number of days until the next schedule occurrence.
    Tests _extract_days.
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))
        self.m_schedules = scheduleXml.read_schedules_xml(self.m_pyhouse_obj)
        self.m_pyhouse_obj.House.Schedule = self.m_schedules
        self.m_schedule_obj = self.m_schedules[0]

    def test_01_Seconds(self):
        """ Testing time conversion to seconds
        """
        l_datetime = datetime.datetime(2018, 11, 25, 0, 0, 1)
        l_seconds = convert.datetime_to_seconds(l_datetime)
        self.assertEqual(l_seconds, 1)
        #
        l_datetime = datetime.datetime(2018, 11, 25, 0, 1, 2)
        l_seconds = convert.datetime_to_seconds(l_datetime)
        self.assertEqual(l_seconds, 62)
        #
        l_datetime = datetime.datetime(2018, 11, 25, 1, 2, 3)
        l_seconds = convert.datetime_to_seconds(l_datetime)
        self.assertEqual(l_seconds, 3723)
        #
        l_datetime = datetime.datetime(2018, 11, 25, 23, 59, 59)
        l_seconds = convert.datetime_to_seconds(l_datetime)
        self.assertEqual(l_seconds, 86399)


class B2_Days(SetupMixin, unittest.TestCase):
    """ Using the DOW field, get the number of days until the next schedule occurrence.
    Tests _extract_days.
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))
        self.m_schedules = scheduleXml.read_schedules_xml(self.m_pyhouse_obj)
        self.m_pyhouse_obj.House.Schedule = self.m_schedules
        self.m_schedule_obj = self.m_schedules[0]

    def test_01_0_Days(self):
        """ Date is within DOW value
        """
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


class B3_Extract(SetupMixin, unittest.TestCase):
    """
    The number of minutes from midnight to the scheduled time.
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))
        self.m_schedules = scheduleXml.read_schedules_xml(self.m_pyhouse_obj)
        self.m_pyhouse_obj.House.Schedule = self.m_schedules
        self.m_schedule_obj = self.m_schedules[0]

        self.m_schedule_obj.DOW = 1 + 2 + 4 + 8 + 16 + 32 + 64
        self.m_riseset = Mock.RiseSet()

    def test_01_Time(self):
        """ Extract Minutes from Midnight to schedule time
        3720
        """
        self.m_schedule_obj.Time = '01:02'
        l_seconds = SchedTime._extract_schedule_time(self.m_schedule_obj, self.m_riseset)
        # print('\nB3-01-A - Minutes {}\n'.format(l_seconds))
        self.assertEqual(l_seconds, (1 * 60 + 2) * 60)

    def test_02_Dawn(self):
        """ Extract Minutes from Midnight to schedule time
        """
        self.m_schedule_obj.Time = 'dawn'
        l_seconds = SchedTime._extract_schedule_time(self.m_schedule_obj, self.m_riseset)
        print('\nB3-02-A - Minutes {}\n'.format(l_seconds))
        self.assertEqual(l_seconds, (6 * 60 + 4) * 60 + 52)

    def test_03_DawnPlus(self):
        """ Extract Minutes from Midnight to schedule time
        """
        self.m_schedule_obj.Time = 'dawn + 0:10'
        l_seconds = SchedTime._extract_schedule_time(self.m_schedule_obj, self.m_riseset)
        # print('\nB3-03-A - Minutes {}\n'.format(l_seconds))
        self.assertEqual(l_seconds, (6 * 60 + 4) * 60 + 52) + (10 * 60)

    def test_04_DawnMinus(self):
        """ Extract Minutes from Midnight to schedule time
        """
        self.m_schedule_obj.Time = 'dawn - 0:10'
        l_seconds = SchedTime._extract_schedule_time(self.m_schedule_obj, self.m_riseset)
        # print('\nB3-04-A - Minutes {}\n'.format(l_seconds))
        self.assertEqual(l_seconds, (6 * 60 + 4) * 60 + 52) - (10 * 60)

    def test_05_Noon(self):
        """ Extract Minutes from Midnight to schedule time
        """
        self.m_schedule_obj.Time = 'noon'
        l_seconds = SchedTime._extract_schedule_time(self.m_schedule_obj, self.m_riseset)
        # print('\nB3-05-A - Minutes {}\n'.format(l_seconds))
        self.assertEqual(l_seconds, (13 * 60 + 31) * 60 + 41)

    def test_06_Sunset(self):
        """ Extract Minutes from Midnight to schedule time
        """
        self.m_schedule_obj.Time = 'sunset'
        l_seconds = SchedTime._extract_schedule_time(self.m_schedule_obj, self.m_riseset)
        print('\nB3-06-A - Minutes {}\n'.format(l_seconds))
        self.assertEqual(l_seconds, (20 * 60 + 31) * 60 + 25)

    def test_07_Dusk(self):
        """ Extract Minutes from Midnight to schedule time
        """
        self.m_schedule_obj.Time = 'dusk'
        l_seconds = SchedTime._extract_schedule_time(self.m_schedule_obj, self.m_riseset)
        # print('\nB3-07-A - Minutes {}\n'.format(l_seconds))
        self.assertEqual(l_seconds, (20 * 60 + 58) * 60 + 30)

    def test_08_DawnPlus(self):
        """ Extract Minutes from Midnight to schedule time
        22492
        """
        self.m_schedule_obj.Time = 'dawn + 0:10'
        l_seconds = SchedTime._extract_schedule_time(self.m_schedule_obj, self.m_riseset)
        # print('\nB3-08-A - Minutes {}\n'.format(l_seconds))
        self.assertEqual(l_seconds, (6 * 60 + 4) * 60 + 52) + (10 * 60)


class B4_Time(SetupMixin, unittest.TestCase):
    """
    Test the time from now to the schedule time
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))
        self.m_schedules = scheduleXml.read_schedules_xml(self.m_pyhouse_obj)
        self.m_pyhouse_obj.House.Schedule = self.m_schedules
        self.m_schedule_obj = self.m_schedules[0]
        self.m_schedule_obj.DOW = 1 + 2 + 4 + 8 + 16 + 32 + 64
        self.m_riseset = Mock.RiseSet()
        self.m_now = datetime.datetime(2016, 8, 13, 11, 12, 0)

    def test_01_ToGo(self):
        """ Time = 11:13
            Now  = 11:12:00
        60
        """
        self.m_schedule_obj.Time = '11:13:00'
        l_seconds = SchedTime.extract_time_to_go(self.m_pyhouse_obj, self.m_schedule_obj, self.m_now, self.m_riseset)
        # print('\nB4-01-A - Seconds:{} {}'.format(l_seconds, to_dhms(l_seconds)))
        self.assertEqual(l_seconds, 60)

    def test_02_Sunset(self):
        """ Sunset = 20:31:25
            Now    = 11:12:00
        33565
        """
        self.m_schedule_obj.Time = 'Sunset'
        l_seconds = SchedTime.extract_time_to_go(self.m_pyhouse_obj, self.m_schedule_obj, self.m_now, self.m_riseset)
        print('\nB4-02-A - Seconds:{}  {}'.format(l_seconds, to_dhms(l_seconds)))
        self.assertEqual(l_seconds, (((20 - 11) * 60 + (31 - 12)) * 60) + 25)

    def test_03_SunsetPlus(self):
        """ Sunset = 20:31:25
            Now    = 11:12:00
            Plus   = 00:21
        33565 + 1260 = 34825
        """
        self.m_schedule_obj.Time = 'sunset + 00:21'
        l_seconds = SchedTime.extract_time_to_go(self.m_pyhouse_obj, self.m_schedule_obj, self.m_now, self.m_riseset)
        print('B3-03-A - Seconds:{}  {}'.format(l_seconds, to_dhms(l_seconds)))
        self.assertEqual(l_seconds, (((20 - 11) * 60 + (31 - 12)) * 60) + 25) + (21 * 60)

    def test_04_Tomorrow(self):
        """ Test for tomorrow morning
            Tomorrow = 24:00
            Now      = 11:12:00
                       12:48
                       03:02
                       15:50

        """
        self.m_schedule_obj.DOW = 1 + 2 + 4 + 8 + 16 + 0 + 64  # Not today
        self.m_schedule_obj.Time = '03:02'
        l_seconds = SchedTime.extract_time_to_go(self.m_pyhouse_obj, self.m_schedule_obj, self.m_now, self.m_riseset)
        # print('B3-04-A - Minutes: {}'.format(self.m_now.weekday()))
        self.assertEqual(l_seconds, ((15 * 60 + 50) * 60))

    def test_05_ToGo(self):
        """ Test next day 45 mins from now
        """
        self.m_schedule_obj.Time = '11:10'
        l_seconds = SchedTime.extract_time_to_go(self.m_pyhouse_obj, self.m_schedule_obj, self.m_now, self.m_riseset)
        # print('B4-05-A - Seconds{}  {}'.format(l_seconds, to_dhms(l_seconds)))
        self.assertEqual(l_seconds, ((23 * 60 + 58) * 60))


class B5_Extract(SetupMixin, unittest.TestCase):
    """
    The number of minutes from midnight to the scheduled time.
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))
        self.m_schedules = scheduleXml.read_schedules_xml(self.m_pyhouse_obj)
        self.m_pyhouse_obj.House.Schedule = self.m_schedules
        self.m_schedule_obj = self.m_schedules[0]
        self.m_schedule_obj.DOW = 1 + 2 + 4 + 8 + 16 + 32 + 64
        self.m_riseset = Mock.RiseSet()

    def test_01_Dusk(self):
        """ Extract Minutes from Midnight to schedule time

        Dusk = 20:58:30
        75510
        """
        self.m_schedule_obj.Time = 'Dusk'
        l_seconds = SchedTime._extract_schedule_time(self.m_schedule_obj, self.m_riseset)
        # print('B5-01-A - Seconds {}'.format(l_seconds))
        self.assertEqual(l_seconds, (20 * 60 + 58) * 60 + 30)

    def test_02_dusk(self):
        """
        Dusk = 20:58:30
        75510
        """
        self.m_schedule_obj.Time = 'dusk'
        l_seconds = SchedTime._extract_schedule_time(self.m_schedule_obj, self.m_riseset)
        print(PrettyFormatAny.form(l_seconds, 'B4-02-A - Minutes'))
        self.assertEqual(l_seconds, (TESTING_SCHEDULE_DUSK_0.hour * 60 + TESTING_SCHEDULE_DUSK_0.minute) * 60 + TESTING_SCHEDULE_DUSK_0.second)

    def test_03_Sunrise(self):
        """
        Sunrise = 06:31:56
        23516
        """
        self.m_schedule_obj.Time = 'sunrise'
        l_seconds = SchedTime._extract_schedule_time(self.m_schedule_obj, self.m_riseset)
        print(PrettyFormatAny.form(l_seconds, 'B4-03-A - Minutes'))
        self.assertEqual(l_seconds, (6 * 60 + 31) * 60 + 56)

    def test_04_TillSched(self):
        """
        Sunset = 20:31:25 (73885)
        Plus   = 00:10    (  600)
        73885 + 600 = 74485
        """
        self.m_schedule_obj.Time = 'sunset + 0:10'
        l_seconds = SchedTime._extract_schedule_time(self.m_schedule_obj, self.m_riseset)
        print(PrettyFormatAny.form(l_seconds, 'B4-04-A - Minutes'))
        self.assertEqual(l_seconds, (20 * 60 + 31) * 60 + 25) + (10 * 60)

    def test_05_TillSched(self):
        """
        Sunset = 20:31:25 (73885)
        Minus  = 00:17    ( 1020)
        73885 - 1020 = 72865
        """
        self.m_schedule_obj.Time = 'sunset - 0:17'
        l_seconds = SchedTime._extract_schedule_time(self.m_schedule_obj, self.m_riseset)
        print(PrettyFormatAny.form(l_seconds, 'B4-05-A - Minutes'))
        self.assertEqual(l_seconds, (20 * 60 + 31) * 60 + 25) - (17 * 60)


class C1_Execute(SetupMixin, unittest.TestCase):
    """Testing class ScheduleExecution
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))
        self.m_schedules = scheduleXml.read_schedules_xml(self.m_pyhouse_obj)
        self.m_pyhouse_obj.House.Schedule = self.m_schedules
        self.m_schedule_obj = self.m_schedules[0]
        # self.m_pyhouse_obj.APIs.Computer.MqttAPI = mqttAPI(self.m_pyhouse_obj)

    def test_01_one(self):
        """ No way to test the dispatch routine
        """
        self.m_pyhouse_obj.House.Schedule[0].ScheduleType = 'TeStInG14159'  # to set dispatch to testing
        l_schedule = self.m_pyhouse_obj.House.Schedule[0]
        # print(PrettyFormatAny.form(l_schedule, 'C1-01-A - Sched'))
        # ScheduleExecution().dispatch_one_schedule(self.m_pyhouse_obj, l_schedule)
        # self.assertEqual(True, True)


class C2_List(SetupMixin, unittest.TestCase):
    """
    This section tests the Building of a schedule list
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))
        self.m_pyhouse_obj.House.Schedules = scheduleXml.read_schedules_xml(self.m_pyhouse_obj)
        self.m_pyhouse_obj.APIs.Computer.MqttAPI = mqttAPI(self.m_pyhouse_obj)
        twisted.internet.base.DelayedCall.debug = True

    def test_01_BuildSched(self):
        """ Testing the build of a schedule list.
        We should end up with 2 schedules in the list.
        """
        l_riseset = Mock.RiseSet()
        l_delay, l_list = scheduleUtility.find_next_scheduled_events(self.m_pyhouse_obj, T_TODAY)
        l_now_sec = convert.datetime_to_seconds(T_TODAY)
        l_obj = self.m_pyhouse_obj.House.Schedules[0]
        l_sched_sec = SchedTime._extract_schedule_time(l_obj, l_riseset)
        # print('C2-01-A - Delay: {}; List: {}; Now: {}; Sched: {}'.format(l_delay, l_list, l_now_sec, l_sched_sec))
        self.assertEqual(len(l_list), 2)
        self.assertEqual(l_delay, l_sched_sec - l_now_sec)
        self.assertEqual(l_list[0], 0)
        self.assertEqual(l_list[1], 1)

    def test_02_Load(self):
        """ Test ???
        """
        SetupPyHouseObj().LoadHouse(self.m_pyhouse_obj)
        # print(PrettyFormatAny.form(self.m_pyhouse_obj.House.Schedules, 'C2-02-A - Schedules'))
        # print(PrettyFormatAny.form(self.m_pyhouse_obj.House.Schedules[0], 'C2-02-B - Schedules 0'))
        # print(PrettyFormatAny.form(self.m_pyhouse_obj.House.Schedules[1], 'C2-02-C - Schedules 1'))
        # print(PrettyFormatAny.form(self.m_pyhouse_obj.House.Schedules[2], 'C2-02-D - Schedules 2'))
        # print(PrettyFormatAny.form(self.m_pyhouse_obj.House.Schedules[3], 'C2-02-E - Schedules 3'))
        # print(PrettyFormatAny.form(self.m_pyhouse_obj.House.Schedules[4], 'C2-02-F - Schedules 4'))

    def Xtest_03_Sched(self):
        """
        """
        SetupPyHouseObj().LoadHouse(self.m_pyhouse_obj)
        print(PrettyFormatAny.form(self.m_pyhouse_obj.House, 'C2-03-A - PyHouse.House 1'))
        l_delay = 1
        _l_list = [0, 1]
        _l_id = scheduleUtility.schedule_next_event(self.m_pyhouse_obj, l_delay)
        time.sleep(2 * l_delay)
        # l_id.cancel()

    def test_04_RunSchedule(self):
        pass

    def test_05_SchedulesList(self):
        pass

    def test_07_OneSchedule(self):
        pass
        # dispatch_one_schedule(3)

    def test_09_DispatchSchedule(self):
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
