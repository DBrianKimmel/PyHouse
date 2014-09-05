"""
-*- test-case-name: PyHouse.src.Modules.Scheduling.test.test_schedule -*-

@name: PyHouse/src/Modules/Scheduling/schedule.py
@author: D. Brian Kimmel
@contact: D.BrianKimmel@gmail.com
@Copyright (c) 2013-2014 by D. Brian Kimmel
@license: MIT License
@note: Created on Apr 8, 2013
@summary: Schedule events


Handle the home automation system schedule for a house.

The schedule is at the Core of PyHouse.
Lighting events, entertainment events, etc. for one house are triggered by the schedule and are run by twisted.

Read/reread the schedule file at:
    1. Start up
    2. Midnight
    3. After each set of scheduled events.


Controls:
    Communication
    Entertainment
    HVAC
    Irrigation
    Lighting
    Pool
    Remote
    Security
    UPNP

Operation:

  Iterate thru the schedule tree and create a list of schedule events.
  Select the next event(s) from now, there may be more than one event scheduled for the same time.

  Create a twisted timer that goes off when the scheduled time arrives.
  We only create one timer (ATM) so that we do not have to cancel timers when the schedule is edited.

  TODO: create a group of timers and cancel the changed ones when the schedules object is changed.
        Keep all times as UTC - display them as local time for editing.
"""

# Import system type stuff
import datetime
import dateutil.parser as dparser

# Import PyMh files
from Modules.Core.data_objects import ScheduleBaseData
from Modules.Scheduling import sunrisesunset
from Modules.Scheduling import schedule_xml
from Modules.Lighting import lighting
from Modules.Hvac import thermostat
from Modules.Irrigation import irrigation
from Modules.Utilities import tools
from Modules.Utilities.tools import GetPyhouse, PrettyPrintAny
from Modules.Computer import logging_pyh as Logger
# from Modules.Utilities.tools import PrettyPrintAny

g_debug = 1
LOG = Logger.getLogger('PyHouse.Schedule    ')
SECONDS_IN_DAY = 86400
SECONDS_IN_WEEK = 604800  # 7 * 24 * 60 ^ 60

class ScheduleExecution(ScheduleBaseData):

    def dispatch_schedule(self, p_slot):
        """
        TODO: We need a small dispatch for the various schedule types (hvac, security, entertainment, lights, ...)
        """
        l_schedule_obj = GetPyhouse(self.m_pyhouse_obj).Schedules[p_slot]
        if l_schedule_obj.ScheduleType == 'LightingDevice':
            pass
        elif l_schedule_obj.ScheduleType == 'Scene':
            pass
        pass

    def execute_one_schedule(self, p_slot):
        """
        Send information to one device to execute a schedule.
        """
        l_schedule_obj = self.m_pyhouse_obj.House.OBJs.Schedules[p_slot]
        # PrettyPrintAny(l_schedule_obj, 'Schedule - ExecuteOneSchedule - ScheduleObject', 120)
        # PrettyPrintAny(self.m_pyhouse_obj.House.OBJs, 'Schedule - ExecuteOneSchedule - PyHouseObj', 120)
        # TODO: We need a small dispatch for the various schedule types (hvac, security, entertainment, lights, ...)
        if l_schedule_obj.ScheduleType == 'LightingDevice':
            LOG.debug('Execute_one_schedule type = LightingDevice')
            pass
        elif l_schedule_obj.ScheduleType == 'Scene':
            LOG.debug('Execute_one_schedule type = Scene')
            pass
        l_light_obj = tools.get_light_object(self.m_pyhouse_obj, name = l_schedule_obj.LightName)
        LOG.info("Name:{0:}, Light:{1:}, Level:{2:}, Slot:{3:}".format(l_schedule_obj.Name, l_schedule_obj.LightName, l_schedule_obj.Level, p_slot))
        self.m_pyhouse_obj.APIs.LightingAPI.ChangeLight(l_light_obj, l_schedule_obj.Level)

    def execute_schedules_list(self, p_slot_list = []):
        """
        For each SlotName in the passed in list, execute the scheduled event for the house.
        Delay before generating the next schedule to avoid a race condition
         that duplicates an event if it completes before the clock goes to the next second.

        @param p_slot_list: a list of Slots in the next time schedule to be executed.
        """
        LOG.info("About to execute - Schedule:{0:}".format(p_slot_list))
        for l_slot in range(len(p_slot_list)):
            self.execute_one_schedule(p_slot_list[l_slot])
        self.m_pyhouse_obj.Twisted.Reactor.callLater(5, self.run_schedule, None)

    def run_schedule(self, _ignore):
        """Find out what schedules need to be done and how long to delay before they are due to be run.
        """
        l_seconds_to_delay, l_schedule_list = self.get_next_sched(self.m_pyhouse_obj)
        if g_debug >= 1:
            LOG.info('Delay: {0:} - List: {1:}'.format(l_seconds_to_delay, l_schedule_list))
        self.m_pyhouse_obj.Twisted.Reactor.callLater(l_seconds_to_delay, self.execute_schedules_list, l_schedule_list)


class ScheduleTime(object):

    m_now = None

    def _extract_time_or_offset(self, p_timefield):
        """
        Extract the time or offset time from the timefield

        """
        l_time = dparser.parse(p_timefield, fuzzy = True)
        l_time2 = datetime.timedelta(0, l_time.second, 0, 0, l_time.minute, l_time.hour)
        # PrettyPrintAny(l_time2, 'Time')
        l_field = p_timefield
        return l_time2, l_field

    def _is_offset(self, p_timefield):
        return ('+' in p_timefield) | ('-' in p_timefield)

    def _is_rise_set(self, p_timefield):
        return ('sunrise' in p_timefield.lower()) | ('sunset' in p_timefield.lower())

    def _now_daytime(self):
        """
        Freeze the current time into self.m_now.
        This used in all calculations to avoid time jitter (seconds changing during the course of calculations)
        """
        self.m_now = datetime.datetime.now()
        return self.m_now

    def _find_dow(self, p_datetime):
        """
        Find out the day of the week for a given date (in datetime)
        """
        return p_datetime.weekday()

    def _is_dow(self, p_schedule_obj, p_dow):
        """
        test to see if the p_dow bit is set in DOW
        """
        l_dow = p_schedule_obj.DOW
        l_is = 2 ** p_dow
        l_ret = (l_dow & l_is) != 0
        # print(l_dow, l_is, l_ret)
        return l_ret

    def _extract_time_of_day(self, p_schedule_obj, p_sunrise, p_sunset):
        """
        Get the time of day to execute the schedule.
        The time field may be HH:MM or HH:MM:SS
            sunrise/sunset  +/-  offset HH:MM:SS or HH:MM
        """
        l_datetime = datetime.datetime(2000, 1, 1)
        l_timefield = p_schedule_obj.Time
        l_offset, _ignore = self._extract_time_or_offset(l_timefield)
        if 'sunrise' in l_timefield.lower():
            print('Sunrise >>{0:}<<====>>{1:}<<'.format(p_sunrise, l_offset))
            l_datetime = p_sunrise
            if '-' in l_timefield:
                l_datetime -= l_offset
            else:
                l_datetime = l_datetime + l_offset
        if 'sunset' in l_timefield.lower():
            l_datetime = p_sunset
            if '-' in l_timefield:
                l_datetime -= l_offset
            else:
                l_datetime += l_offset
        else:
            l_datetime = l_offset
        return l_datetime

    def _get_days(self, p_schedule_obj, p_now = m_now):
        """
        get days till a DOW time is selected

        now = day 5

        """
        l_count = 0
        l_today_dow = p_now.weekday()
        for l_x in range(7):  # 0-6
            l_y = (l_x + l_today_dow) % 7
            if self._is_dow(p_schedule_obj, l_y):
                return l_count
            l_count += 1
        return None

    def _find_diff(self, p_sched, p_now):
        """
        @param p_sched: is a datetime of the schedule start time
        @param p_now: is a datetime of the chached current time.
        """
        l_diff = self._make_delta(p_sched).total_seconds() - self._make_delta(p_now).total_seconds()
        if l_diff < 0:
            l_diff = l_diff + 86400.0  # tomorrow
        return l_diff

    def _find_delay_seconds(self, p_schedule_obj):
        """
        Find the delay (number of seconds until the scheduled time)
        Use self.m_now to ease testing and also to avoid jitter in times.
        """
        if not p_schedule_obj.Active:
            return SECONDS_IN_WEEK
        l_time_sch = self._extract_time(p_schedule_obj.Time)
        return self._find_diff(l_time_sch, self.m_now)

    def _get_sunrise_sunset(self):
        """
        The unit tests for this is in the sunrisesunset module.
        this code just gets the values for this module
        """
        self.m_sunrisesunset_api.Start(self.m_pyhouse_obj)
        self.m_sunset = self.m_sunrisesunset_api.get_sunset()
        # self.m_sunrise = self.m_sunrisesunset_api.get_sunrise()
        l_rise = self.m_sunrisesunset_api.get_sunrise()
        self.m_sunrise = datetime.datetime(0, 0, 0, l_rise.hour, l_rise.minute, l_rise.second, 0, None)
        LOG.info("In get_next_sched - Sunrise:{0:}, Sunset:{1:}".format(self.m_sunrise, self.m_sunset))


class ScheduleUtility(ScheduleTime):

    def _substitute_time(self, p_timefield):
        """Substitute for names in timefield.
        Supported fields are: 'sunset'. 'sunrise'
        Return the string timefield.
        """
        if 'sunset' in p_timefield.lower():
            l_timefield = self.m_sunset.strftime('%H:%M')
            p_timefield = p_timefield.replace('sunset', l_timefield)
        elif 'sunrise' in p_timefield.lower():
            l_timefield = self.m_sunrise.strftime('%H:%M')
            p_timefield = p_timefield.replace('sunrise', l_timefield)
        return p_timefield

    def _extract_field(self, p_timefield):
        """Extract a time of HH:MM[:ss]
        @return: A datetime.time of the extracted time
        clears the timestring from p_timefield to allow for offset type timestrings
        returns 0 of no such field.
        """
        try:
            while p_timefield[0] == ' ':
                p_timefield = p_timefield[1:]
        except IndexError:
            pass
        if ':' in p_timefield:
            try :
                l_ret = datetime.datetime.strptime(p_timefield[0:8], '%H:%M:%S')
                p_timefield = p_timefield[8:]
            except ValueError:
                if g_debug >= 7:
                    print("ERROR - not HH:MM:SS - try shorter")
                try:
                    l_ret = datetime.datetime.strptime(p_timefield[0:5], '%H:%M')
                    p_timefield = p_timefield[5:]
                except ValueError:
                    if g_debug >= 7:
                        print("ERROR - not HH:MM - using 00:00:00")
                    l_ret = datetime.time(0, 0, 0)
            try:
                while p_timefield[0] == ' ':
                    p_timefield = p_timefield[1:]
            except IndexError:
                pass
            if g_debug >= 7:
                print("schedule._extract_field() Exit - {0:}, '{1:}'".format(l_ret, p_timefield))
        else:
            l_ret = datetime.time(0, 0, 0)
            if g_debug >= 7:
                print("schedule._extract_field() No ':' - Exit - {0:}, '{1:}'".format(l_ret, p_timefield))
        return l_ret, p_timefield

    def _make_delta(self, p_time):
        """Convert a datetime to a timedelta.

        @param p_time: is a datetime if a time to convert
        @return: a timedelta if the time to convert
        """
        return datetime.timedelta(0, p_time.second, 0, 0, p_time.minute, p_time.hour)

    def get_next_sched(self, p_pyhouse_obj):
        """
        Get the next schedule from the current time.

        Be sure to get the next in a chain of things happening at the same time.
        Establish a list of Names that have equal schedule times
        """
        self._get_sunrise_sunset()
        l_now = datetime.datetime.now()
        l_time_now = self._now_daytime()
        l_time_scheduled = l_now
        l_seconds_to_delay = 1000000.0
        l_schedule_list = []
        for l_key, l_schedule_obj in p_pyhouse_obj.House.OBJs.Schedules.iteritems():
            if not l_schedule_obj.Active:
                continue
            l_time_sch = self._extract_time(l_schedule_obj.Time)
            # now see if this is 1) part of a chain -or- 2) an earlier schedule
            l_diff = self._find_diff(l_time_sch, l_time_now)
            # earlier schedule upcoming.
            if l_diff < l_seconds_to_delay:
                l_seconds_to_delay = l_diff
                l_schedule_list = []
                l_time_scheduled = l_time_sch
            # add to a chain
            if l_diff == l_seconds_to_delay:
                l_schedule_list.append(l_key)
        l_debug_msg = "Delaying {0:} seconds until {1:} for list {2:}".format(l_seconds_to_delay, l_time_scheduled, l_schedule_list)
        LOG.info("Get_next_schedule complete. {0:}".format(l_debug_msg))
        return l_seconds_to_delay, l_schedule_list


class UpdatePyhouse(object):

    def add_api_references(self, p_pyhouse_obj):
        p_pyhouse_obj.APIs.LightingAPI = lighting.API()
        p_pyhouse_obj.APIs.HvacAPI = thermostat.API()
        p_pyhouse_obj.APIs.IrrigationAPI = irrigation.API()

    def start_scheduled_modules(self, p_pyhouse_obj):
        """
        TODO: Lighting must be first since it loads families etc.
        """
        p_pyhouse_obj.APIs.LightingAPI.Start(p_pyhouse_obj)
        p_pyhouse_obj.APIs.HvacAPI.Start(p_pyhouse_obj)
        p_pyhouse_obj.APIs.IrrigationAPI.Start(p_pyhouse_obj)

    def stop_scheduled_modules(self):
        self.m_pyhouse_obj.APIs.HvacAPI.Stop()
        self.m_pyhouse_obj.APIs.LightingAPI.Stop()
        self.m_pyhouse_obj.APIs.IrrigationAPI.Stop()

    def save_scheduled_modules(self, p_xml):
        self.m_pyhouse_obj.APIs.HvacAPI.SaveXml(p_xml)
        self.m_pyhouse_obj.APIs.LightingAPI.SaveXml(p_xml)
        self.m_pyhouse_obj.APIs.IrrigationAPI.SaveXml(p_xml)
        return p_xml


class API(ScheduleUtility, UpdatePyhouse):
    """Instantiated once for each house (active or not)
    """

    m_sunrisesunset_api = None
    m_pyhouse_obj = None

    def __init__(self):
        self.m_sunrisesunset_api = sunrisesunset.API()

    def Start(self, p_pyhouse_obj):
        """
        Extracts all from XML so an update will write correct info back out to the XML file.
        Does not schedule a next entry for inactive houses.

        @param p_house_obj: is a House object for the house being scheduled
        """
        LOG.info("Starting.")
        self.add_api_references(p_pyhouse_obj)
        self.m_pyhouse_obj = p_pyhouse_obj
        p_pyhouse_obj.House.OBJs.Schedules = schedule_xml.ReadWriteConfigXml().read_schedules_xml(p_pyhouse_obj)
        self.m_sunrisesunset_api.Start(p_pyhouse_obj)
        self.start_scheduled_modules(p_pyhouse_obj)
        if self.m_pyhouse_obj.House.Active:
            self.m_pyhouse_obj.Twisted.Reactor.callLater(5, self.run_schedule, None)
        else:
            LOG.warning('No Schedules will be run because the house is NOT active.')
        LOG.info("Started.")

    def Stop(self):
        """Stop everything under me.
        """
        self.stop_scheduled_modules()
        LOG.info("Stopped.")

    def SaveXml(self, p_xml):
        p_xml.append(schedule_xml.ReadWriteConfigXml().write_schedules_xml(self.m_pyhouse_obj.House.OBJs.Schedules))
        self.save_scheduled_modules(p_xml)
        # LOG.info("Saved XML.")

# ## END DBK
