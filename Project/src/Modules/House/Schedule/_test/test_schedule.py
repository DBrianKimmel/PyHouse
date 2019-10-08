"""
@name:      Modules/Schedules/_test/test_schedule.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2013-2019 by D. Brian Kimmel
@license:   MIT License
@note:      Created on Apr 8, 2013
@summary:   Test handling the schedule information for a house.

Passed all 49 tests - DBK - 2019-05-12

There are some tests (starting with 'X') that I do not know how to do in twisted.

"""

__updated__ = '2019-10-06'

# Import system type stuff
import datetime
from twisted.trial import unittest
import time
import twisted

# Import PyMh files and modules.
from Modules.Core.data_objects import RiseSetData
from Modules.Core.Utilities import convert, config_tools
from Modules.Core.Mqtt.mqtt import Api as mqttApi
from Modules.House.Schedule.schedule import \
    Config as scheduleConfig, \
    SchedTime, \
    Api as scheduleApi, \
    lightingUtility as scheduleUtility, \
    TimeField, CONFIG_FILE_NAME
from _test.testing_mixin import SetupPyHouseObj
from Modules.Core.Utilities.debug_tools import PrettyFormatAny

T_TODAY = datetime.datetime(2015, 6, 6, 12, 34, 56)
#
T_SUNDAY = datetime.datetime(2015, 6, 7, 1, 2, 3)
DayOfWeek_SUNDAY = 64
T_MONDAY = datetime.datetime(2015, 6, 8, 1, 2, 3)
DayOfWeek_MONDAY = 1
T_TUESDAY = datetime.datetime(2015, 6, 9, 1, 2, 3)
DayOfWeek_TUESDAY = 2
T_WEDNESDAY = datetime.datetime(2015, 6, 10, 1, 2, 3)
DayOfWeek_WEDNESDAY = 4
T_THURSDAY = datetime.datetime(2015, 6, 11, 1, 2, 3)
DayOfWeek_THURSDAY = 8
T_FRIDAY = datetime.datetime(2015, 6, 12, 1, 2, 3)
DayOfWeek_FRIDAY = 16
T_SATURDAY = datetime.datetime(2015, 6, 13, 1, 2, 3)
DayOfWeek_SATURDAY = 32

DOW_ALL = 'SMTWTFS'


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
        l_ret.Dawn = 0
        l_ret.SunRise = 0
        l_ret.Noon = 0
        l_ret.SunSet = 0
        l_ret.Dusk = 0
        return l_ret


class SetupMixin(object):

    def setUp(self):
        self.m_pyhouse_obj = SetupPyHouseObj().BuildPyHouseObj()
        self.m_pyhouse_obj.House.Location._RiseSet = Mock.RiseSet()
        self.m_api = scheduleApi(self.m_pyhouse_obj)
        self.m_filename = 'schedule.yaml'


class A0(unittest.TestCase):

    def test_00_Print(self):
        _x = PrettyFormatAny.form('_test', 'title', 190)  # so it is defined when printing is cleaned up.
        print('Id: test_schedule')


class B1_Global(SetupMixin, unittest.TestCase):
    """ Test converting a datetime to seconds
    """

    def setUp(self):
        SetupMixin.setUp(self)

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


class B2_DayOfWeek(SetupMixin, unittest.TestCase):
    """ Using the DayOfWeek field, get the number of days until the next schedule occurrence.
    Tests _extract_days.
    """

    def setUp(self):
        SetupMixin.setUp(self)

    def test_01_0_Days(self):
        """ Date is within DayOfWeek value
        """
        l_days = SchedTime._extract_days(self.m_schedule_obj, T_WEDNESDAY)
        self.assertEqual(l_days, 0)
        self.m_schedule_obj.DayOfWeek = DayOfWeek_WEDNESDAY
        l_days = SchedTime._extract_days(self.m_schedule_obj, T_WEDNESDAY)
        # print(PrettyFormatAny.form(l_days, 'B1-01-A - Days'))
        self.assertEqual(l_days, 0)

    def test_02_1_Day(self):
        """ Date will be tomorrow
        """
        self.m_schedule_obj.DayOfWeek = DayOfWeek_THURSDAY
        l_days = SchedTime._extract_days(self.m_schedule_obj, T_WEDNESDAY)
        self.assertEqual(l_days, 1)
        self.m_schedule_obj.DayOfWeek = 127 - DayOfWeek_WEDNESDAY
        l_days = SchedTime._extract_days(self.m_schedule_obj, T_WEDNESDAY)
        # print(PrettyFormatAny.form(l_days, 'B1-02-A - Days'))
        self.assertEqual(l_days, 1)

    def test_03_2_Days(self):
        """ Date will be in 2 days
        """
        self.m_schedule_obj.DayOfWeek = DayOfWeek_FRIDAY
        l_days = SchedTime._extract_days(self.m_schedule_obj, T_WEDNESDAY)
        # print(PrettyFormatAny.form(l_days, 'B1-03-A - Days'))
        self.assertEqual(l_days, 2)

    def test_04_3_Days(self):
        """ Date will be in 3 days
        """
        self.m_schedule_obj.DayOfWeek = DayOfWeek_SATURDAY
        l_days = SchedTime._extract_days(self.m_schedule_obj, T_WEDNESDAY)
        # print(PrettyFormatAny.form(l_days, 'B1-04-A - Days'))
        self.assertEqual(l_days, 3)

    def test_05_4_Days(self):
        """ Date will be in 4 days
        """
        self.m_schedule_obj.DayOfWeek = DayOfWeek_SUNDAY
        l_days = SchedTime._extract_days(self.m_schedule_obj, T_WEDNESDAY)
        # print(PrettyFormatAny.form(l_days, 'B1-05-A - Days'))
        self.assertEqual(l_days, 4)

    def test_06_5_Days(self):
        """ Date will be in 5 days
        """
        self.m_schedule_obj.DayOfWeek = DayOfWeek_MONDAY
        l_days = SchedTime._extract_days(self.m_schedule_obj, T_WEDNESDAY)
        # print(PrettyFormatAny.form(l_days, 'B1-06-A - Days'))
        self.assertEqual(l_days, 5)

    def test_07_6_Days(self):
        """ Date will be in 6 days
        """
        self.m_schedule_obj.DayOfWeek = DayOfWeek_TUESDAY
        l_days = SchedTime._extract_days(self.m_schedule_obj, T_WEDNESDAY)
        # print(PrettyFormatAny.form(l_days, 'B1-07-A - Days'))
        self.assertEqual(l_days, 6)

    def test_08_7_PlusDays(self):
        """ Date will be Never
        """
        self.m_schedule_obj.DayOfWeek = 0
        l_days = SchedTime._extract_days(self.m_schedule_obj, T_WEDNESDAY)
        # print(PrettyFormatAny.form(l_days, 'B1-08-A - Days'))
        self.assertEqual(l_days, 10)


class C1_Execute(SetupMixin, unittest.TestCase):
    """Testing class ScheduleExecution
    """

    def setUp(self):
        SetupMixin.setUp(self)

    def test_01_one(self):
        """ No way to _test the dispatch routine
        """
        self.m_pyhouse_obj.House.Schedules[0].Sched.Type = 'TeStInG14159'  # to set dispatch to testing
        _l_schedule = self.m_pyhouse_obj.House.Schedules[0]
        # print(PrettyFormatAny.form(l_schedule, 'C1-01-A - Sched'))
        # ScheduleExecution().dispatch_one_schedule(self.m_pyhouse_obj, l_schedule)
        # self.assertEqual(True, True)
        pass


class C2_List(SetupMixin, unittest.TestCase):
    """
    This section tests the Building of a schedule list
    """

    def setUp(self):
        SetupMixin.setUp(self)
        self.m_pyhouse_obj._Apis.Core.MqttApi = mqttApi(self.m_pyhouse_obj)
        twisted.internet.base.DelayedCall.debug = True

    def test_01_BuildSched(self):
        """ Testing the build of a schedule list.
        We should end up with 2 schedules in the list.
        """
        l_riseset = Mock.RiseSet()
        l_delay, l_list = scheduleUtility.find_next_scheduled_events(self.m_pyhouse_obj, T_TODAY)
        l_now_sec = convert.datetime_to_seconds(T_TODAY)
        l_obj = self.m_pyhouse_obj.House.Schedules[0]
        l_sched_sec = TimeField().parse_timefield(l_obj.Time, l_riseset)
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
        SetupMixin.setUp(self)
        # self.m_pyhouse_obj.House.Schedules = scheduleXml.read_schedules_xml(self.m_pyhouse_obj)
        self.m_timefield = 0

    def test_01_SubstituteTime(self):
        # self.m_api._substitute_time(self.m_timefield)
        pass

    def test_55_Next(self):
        # l_delay, l_list = self.m_api.find_next_scheduled_event(self.m_pyhouse_obj)
        pass


class D1_Time_Sun(SetupMixin, unittest.TestCase):
    """
    These "D" classes will _test the parsing of the "Time" attribute of the Schedule.

    D1 will _test the sun related part - the words: Dawn etc

        Dawn    = 06:04:52
        SunRise = 06:31:56
        Noon    = 13:31:41
        SunSet  = 20:31:25
        Dusk    = 20:58:30
    """

    def setUp(self):
        SetupMixin.setUp(self)
        # self.m_schedules = scheduleXml.read_schedules_xml(self.m_pyhouse_obj)
        # self.m_pyhouse_obj.House.Schedules = self.m_schedules
        self.m_schedule_obj = self.m_schedules[0]
        self.m_schedule_obj.DayOfWeek = 1 + 2 + 4 + 8 + 16 + 32 + 64
        self.m_riseset = Mock.RiseSet()

    def test_01_Dawn(self):
        """ Extract Minutes from Midnight to schedule time
        """
        l_time = 'dawn'
        l_time, l_seconds = TimeField()._rise_set(l_time, self.m_riseset)
        # print('D1-01-A - Seconds {} - "{}"\n'.format(l_seconds, l_time))
        self.assertEqual(l_seconds, (6 * 60 + 4) * 60 + 52)

    def test_02_Sunrise(self):
        """ Extract Minutes from Midnight to schedule time
        """
        l_time = 'sunrise'
        l_time, l_seconds = TimeField()._rise_set(l_time, self.m_riseset)
        # print('D1-02-A - Seconds {} - "{}"\n'.format(l_seconds, l_time))
        self.assertEqual(l_seconds, (6 * 60 + 31) * 60 + 56)

    def test_03_Noon(self):
        """ Extract Minutes from Midnight to schedule time
        """
        l_time = 'Noon'
        l_time, l_seconds = TimeField()._rise_set(l_time, self.m_riseset)
        # print('D1-03-A - Seconds {} - "{}"\n'.format(l_seconds, l_time))
        self.assertEqual(l_seconds, (13 * 60 + 31) * 60 + 41)

    def test_04_Sunset(self):
        """ Extract Minutes from Midnight to schedule time
        """
        l_time = 'sunset'
        l_time, l_seconds = TimeField()._rise_set(l_time, self.m_riseset)
        # print('D1-04-A - Seconds {} - "{}"\n'.format(l_seconds, l_time))
        self.assertEqual(l_seconds, (20 * 60 + 31) * 60 + 25)

    def test_05_Dusk(self):
        """ Extract Minutes from Midnight to schedule time
        """
        l_time = 'dusk'
        l_time, l_seconds = TimeField()._rise_set(l_time, self.m_riseset)
        # print('D1-05-A - Seconds {} - "{}"\n'.format(l_seconds, l_time))
        self.assertEqual(l_seconds, (20 * 60 + 58) * 60 + 30)

    def test_06_DuskPlus(self):
        """ Extract Minutes from Midnight to schedule time
        """
        l_time = 'dusk + 00:21'
        l_time, l_seconds = TimeField()._rise_set(l_time, self.m_riseset)
        # print('D1-06-A - Seconds {} - "{}"\n'.format(l_seconds, l_time))
        self.assertEqual(l_seconds, (20 * 60 + 58) * 60 + 30)

    def test_07_DuskMinus(self):
        """ Extract Minutes from Midnight to schedule time
        """
        l_time = 'dusk - 00:21'
        l_time, l_seconds = TimeField()._rise_set(l_time, self.m_riseset)
        # print('D1-07-A - Seconds {} - "{}"\n'.format(l_seconds, l_time))
        self.assertEqual(l_seconds, (20 * 60 + 58) * 60 + 30)


class D2_Time_Sign(SetupMixin, unittest.TestCase):
    """
    These "D" classes will _test the parsing of the "Time" attribute of the Schedule.

    D2 will _test the sign portion:
        Possible valid formats are:
        "" (blank)
        +offset
        + offset
        -offset
        - offset

    """

    def setUp(self):
        SetupMixin.setUp(self)
        # self.m_schedules = scheduleXml.read_schedules_xml(self.m_pyhouse_obj)
        # self.m_pyhouse_obj.House.Schedules = self.m_schedules
        self.m_schedule_obj = self.m_schedules[0]
        self.m_schedule_obj.DayOfWeek = 1 + 2 + 4 + 8 + 16 + 32 + 64
        self.m_riseset = Mock.RiseSet()

    def test_01_Blank(self):
        """
        """
        l_time = ''
        l_time, l_flag = TimeField()._extract_sign(l_time)
        # print('D2-01-A - Flag {} - "{}"\n'.format(l_flag, l_time))
        self.assertEqual(l_flag, False)

    def test_02_Plus(self):
        """
        """
        l_time = '+17:01'
        l_time, l_flag = TimeField()._extract_sign(l_time)
        # print('D2-02-A - Flag {} - "{}"\n'.format(l_flag, l_time))
        self.assertEqual(l_flag, False)

    def test_03_PlusSpace(self):
        """
        """
        l_time = '+ 12:34:56'
        l_time, l_flag = TimeField()._extract_sign(l_time)
        # print('D2-03-A - Flag {} - "{}"\n'.format(l_flag, l_time))
        self.assertEqual(l_flag, False)

    def test_04_Minus(self):
        """
        """
        l_time = '-17:01'
        l_time, l_flag = TimeField()._extract_sign(l_time)
        # print('D2-04-A - Flag {} - "{}"\n'.format(l_flag, l_time))
        self.assertEqual(l_flag, True)

    def test_03_MinusSpace(self):
        """
        """
        l_time = '- 12:34:56'
        l_time, l_flag = TimeField()._extract_sign(l_time)
        # print('D2-05-A - Flag {} - "{}"\n'.format(l_flag, l_time))
        self.assertEqual(l_flag, True)


class D3_Time_Offset(SetupMixin, unittest.TestCase):
    """
    These "D" classes will _test the parsing of the "Time" attribute of the Schedule.

    D3 will _test the offset portion:
        Possible valid formats are:
        "" (Blank)
        hh
        hh:mm
        hh:mm:ss
        xxyyzz (Garbage)

    """

    def setUp(self):
        SetupMixin.setUp(self)
        # self.m_schedules = scheduleXml.read_schedules_xml(self.m_pyhouse_obj)
        # self.m_pyhouse_obj.House.Schedules = self.m_schedules
        self.m_schedule_obj = self.m_schedules[0]
        self.m_schedule_obj.DayOfWeek = 1 + 2 + 4 + 8 + 16 + 32 + 64
        self.m_riseset = Mock.RiseSet()

    def test_01_Blank(self):
        """
        """
        l_time = ''
        l_seconds = TimeField()._extract_time_part(l_time)
        # print('D3-01-A - Seconds {}\n'.format(l_seconds))
        self.assertEqual(l_seconds, 0)

    def test_02_Hours(self):
        """
        """
        l_time = '01'
        l_seconds = TimeField()._extract_time_part(l_time)
        # print('D3-02-A - Seconds {}\n'.format(l_seconds))
        self.assertEqual(l_seconds, (1 * 60) * 60)

    def test_03_H_M(self):
        """
        """
        l_time = '12:34'
        l_seconds = TimeField()._extract_time_part(l_time)
        # print('D3-03-A - Seconds {}\n'.format(l_seconds))
        self.assertEqual(l_seconds, (12 * 60 + 34) * 60)

    def test_04_H_M_S(self):
        """
        """
        l_time = '12:34:56'
        l_seconds = TimeField()._extract_time_part(l_time)
        # print('D3-04-A - Seconds {}\n'.format(l_seconds))
        self.assertEqual(l_seconds, (12 * 60 + 34) * 60 + 56)


class D4_Timefield(SetupMixin, unittest.TestCase):
    """
    These "D" classes will _test the parsing of the "Time" attribute of the Schedule.

    D4 will _test the entire field.

        Possible valid formats are:
        "" (Blank)
        hh
        hh:mm
        hh:mm:ss
        xxyyzz (Garbage)

        Dawn    = 06:04:52
        SunRise = 06:31:56
        Noon    = 13:31:41
        SunSet  = 20:31:25
        Dusk    = 20:58:30

    """

    def setUp(self):
        SetupMixin.setUp(self)
        # self.m_schedules = scheduleXml.read_schedules_xml(self.m_pyhouse_obj)
        # self.m_pyhouse_obj.House.Schedules = self.m_schedules
        self.m_schedule_obj = self.m_schedules[0]
        self.m_schedule_obj.DayOfWeek = 1 + 2 + 4 + 8 + 16 + 32 + 64
        self.m_riseset = Mock.RiseSet()

    def test_01_Blank(self):
        """
        """
        l_time = ''
        l_seconds = TimeField().parse_timefield(l_time, self.m_riseset)
        # print('D4-01-A - Seconds {}\n'.format(l_seconds))
        self.assertEqual(l_seconds, 0)

    def test_02_Sunrise(self):
        """
        """
        l_time = 'sunrise'
        l_seconds = TimeField().parse_timefield(l_time, self.m_riseset)
        # print('D4-02-A - Seconds {}\n'.format(l_seconds))
        self.assertEqual(l_seconds, (6 * 60 + 31) * 60 + 56)

    def test_03_Sunrise(self):
        """
        """
        l_time = 'sunrise + 00:10'
        l_seconds = TimeField().parse_timefield(l_time, self.m_riseset)
        # print('D4-03-A - Seconds {}\n'.format(l_seconds))
        self.assertEqual(l_seconds, (6 * 60 + 31) * 60 + 56 + (10 * 60))

    def test_04_Sunrise(self):
        """
        """
        l_time = 'sunrise - 00:12'
        l_seconds = TimeField().parse_timefield(l_time, self.m_riseset)
        # print('D4-04-A - Seconds {}\n'.format(l_seconds))
        self.assertEqual(l_seconds, (6 * 60 + 31) * 60 + 56 - (12 * 60))

    def test_05_Sunrise(self):
        """
        """
        l_time = 'sunrise-00:12:13'
        l_seconds = TimeField().parse_timefield(l_time, self.m_riseset)
        # print('D4-05-A - Seconds {}\n'.format(l_seconds))
        self.assertEqual(l_seconds, (6 * 60 + 31) * 60 + 56 - (12 * 60 + 13))

    def test_06_Sunrise(self):
        """
        """
        l_time = 'sunrise=garbage'
        l_seconds = TimeField().parse_timefield(l_time, self.m_riseset)
        # print('D4-06-A - Seconds {}\n'.format(l_seconds))
        self.assertEqual(l_seconds, (6 * 60 + 31) * 60 + 56)


class E1_Find(SetupMixin, unittest.TestCase):
    """ Test finding a schedule if one exists.
    """

    def setUp(self):
        SetupMixin.setUp(self)
        # self.m_pyhouse_obj.House.Schedules = self.m_schedules
        self.m_schedule_obj = self.m_schedules[0]
        self.m_schedule_obj.DayOfWeek = 1 + 2 + 4 + 8 + 16 + 32 + 64
        self.m_riseset = Mock.RiseSet()

    def test_01_basic(self):
        """
        """
        l_ret = scheduleUtility().find_all_schedule_entries(self.m_pyhouse_obj, p_type='Lighting')
        # print(PrettyFormatAny.form(l_ret, 'Schedule list', 190))
        self.assertEqual(len(l_ret), 4)
        #
        l_ret = scheduleUtility().find_all_schedule_entries(self.m_pyhouse_obj, p_type='Irrigation')
        # print(PrettyFormatAny.form(l_ret, 'Schedule list', 190))
        self.assertEqual(len(l_ret), 1)
        #
        l_ret = scheduleUtility().find_all_schedule_entries(self.m_pyhouse_obj, p_type='Hvac')
        # print(PrettyFormatAny.form(l_ret, 'Schedule list', 190))
        self.assertEqual(l_ret, None)


class F1_Config_Read(SetupMixin, unittest.TestCase):
    """
    """

    def setUp(self):
        SetupMixin.setUp(self)
        self.m_config = scheduleConfig(self.m_pyhouse_obj)
        self.m_working_sched = self.m_pyhouse_obj.House.Schedules

    def test_01_Build(self):
        """ The basic read info as set up
        """
        # print(PrettyFormatAny.form(self.m_working_sched, 'C1-01-A - WorkingSchedule'))
        # print(PrettyFormatAny.form(self.m_pyhouse_obj.House, 'C1-01-B - House'))
        print(PrettyFormatAny.form(self.m_pyhouse_obj.House.Schedules, 'C1-01-C - Schedules'))

    def test_02_ReadFile(self):
        """ Read the rooms.yaml config file
        """
        l_node = config_tools.Yaml(self.m_pyhouse_obj).read_yaml(CONFIG_FILE_NAME)
        l_yaml = l_node.Yaml
        l_yamlsched = l_yaml['Schedules']
        # print(PrettyFormatAny.form(l_node, 'F1-02-A - Node'))
        # print(PrettyFormatAny.form(l_yaml, 'F1-02-B - Yaml'))
        print(PrettyFormatAny.form(l_yamlsched, 'F1-02-C - YamlRooms'))
        self.assertEqual(l_yamlsched[0]['Name'], 'Base')
        self.assertEqual(len(l_yamlsched), 3)

    def test_03_ExtractSched(self):
        """ Extract one room info from the yaml
        """
        l_node = config_tools.Yaml(self.m_pyhouse_obj).read_yaml(CONFIG_FILE_NAME)
        l_yaml = l_node.Yaml
        l_sched = self.m_config._extract_light_schedule(l_yaml['Schedules'][0]['Light'])
        print(PrettyFormatAny.form(l_sched, 'F1-03-A - Sched', 190))

# ## END
