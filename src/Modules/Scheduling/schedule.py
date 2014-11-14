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

        Have modules that want schedule events to register with us.
"""

# Import system type stuff
import datetime
import dateutil.parser as dparser

# Import PyMh files
from Modules.Scheduling import schedule_xml
from Modules.Lighting import lighting
from Modules.Hvac import thermostats
from Modules.Irrigation import irrigation
from Modules.Utilities import tools
from Modules.Utilities.tools import GetPyhouse
from Modules.Computer import logging_pyh as Logger



LOG = Logger.getLogger('PyHouse.Schedule    ')
SECONDS_IN_DAY = 86400
SECONDS_IN_WEEK = 604800  # 7 * 24 * 60 * 60
INITIAL_DELAY = 5
PAUSE_DELAY = 5



class Sch(object):

    @staticmethod
    def find_event(p_event):
        if not p_event.Active:
            return None
        if not p_event.ScheduleType == 'LightingDevice':
            return None
        return p_event


    @staticmethod
    def _make_timedelta(p_datetime):
        """Convert a datetime to a timedelta.

        @param p_datetime: is a datetime of a time to convert
        @return: a timedelta if the time to convert
        """
        return datetime.timedelta(0, p_datetime.second, 0, 0, p_datetime.minute, p_datetime.hour)




class ScheduleTimer(object):
    """The timer for the next schedule execution.
    """

    m_schedule_timer = None


    def start_schedule_timer(self, p_function, p_delay, p_list):
        """Find out what schedules need to be done and how long to delay before they are due to be run.
        """
        LOG.info('Delay: {0:} - List: {1:}'.format(p_delay, p_list))
        self.m_schedule_timer = self.m_pyhouse_obj.Twisted.Reactor.callLater(p_delay, p_function, p_list)


    def cancel_schedule_timer(self):
        """
        Stop the current schedule timer.
        """
        try:
            self.m_schedule_timer.cancel()
        except:
            pass
        self.m_schedule_timer = None



class RiseSetData(object):
    """
    These fields are each an "aware" datetime.datetime
    They were calculated by the sunrisesunset module for the house's location and timezone.
    They are therefore, the local time of sunrise and sunset.
    """
    def __init__(self):
        self.Sunrise = None
        self.Sunset = None


class ScheduleTime(object):
    """
    This class deals with extracting information from the time and dow fields of a schedule.

    """

    m_now = None

    def _now_daytime(self):
        """
        Freeze the current time into self.m_now.
        This used in all calculations to avoid time jitter (seconds changing during the course of calculations)

        @return: the current datetime.datetime local time.
        """
        self.m_now = datetime.datetime.now()
        return self.m_now

    def _extract_time_or_offset(self, p_timefield):
        """
        Extract the time or offset time from the timefield

        @return: a datetime.timedelta of the time portion of the field
        """
        l_time = dparser.parse(p_timefield, fuzzy = True)
        l_time2 = datetime.timedelta(0, l_time.second, 0, 0, l_time.minute, l_time.hour)
        return l_time2

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

    def _extract_time_of_day(self, p_schedule_obj, p_rise_set):
        """
        Get the time of day to execute the schedule.

        The time field may be HH:MM or HH:MM:SS
            sunrise/sunset  +/-  offset HH:MM:SS or HH:MM

        @param p_schedule_obj: is a reference to the schedule we are working on.
        @param p_rise_set: is a RiseSetData object containing sunrise and sunset datetime.datetimes
        @return: a datetime.datetime of when this schedule is to be executed.
        """
        l_timefield = p_schedule_obj.Time.lower()
        l_offset = self._extract_time_or_offset(l_timefield)
        if 'sunrise' in l_timefield:
            l_datetime = p_rise_set.Sunrise
            if '-' in l_timefield:
                l_datetime = l_datetime - l_offset
            else:
                l_datetime = l_datetime + l_offset
        elif 'sunset' in l_timefield:
            l_datetime = p_rise_set.Sunset
            if '-' in l_timefield:
                l_datetime = l_datetime - l_offset
            else:
                l_datetime = l_datetime + l_offset
        else:
            l_datetime = l_offset
        return l_datetime

    def _get_days(self, p_schedule_obj, p_now = m_now):
        """
        get days till a DOW time is selected

        now = day 5
        @return:the (int) number of days from now until an entry in the DOW is turned on.
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
        @return: the number of seconds from now till the schedule entry
        """
        if type(p_sched) == datetime.timedelta:
            l_sched = p_sched.total_seconds()
        else:
            l_sched = Sch._make_timedelta(p_sched).total_seconds()
        if type(p_now) == datetime.timedelta:
            l_now = p_now.total_seconds()
        else:
            l_now = Sch._make_timedelta(p_now).total_seconds()
        l_diff = l_sched - l_now
        if l_diff < 0:
            l_diff = l_diff + 86400.0  # tomorrow
        return l_diff

    def _seconds_to_wait(self, p_now, p_schedule_obj, p_riseset):
        """
        Find the delay (number of seconds until the scheduled time)
        Use self.m_now to ease testing and also to avoid jitter in times.
        """
        if not p_schedule_obj.Active:
            return SECONDS_IN_WEEK
        l_time_sch = self._extract_time_of_day(p_schedule_obj, p_riseset)
        return self._find_diff(l_time_sch, p_now)

    def _get_sunrise_sunset(self, p_pyhouse_obj):
        """
        The unit tests for this is in the sunrisesunset module.
        this code just gets the values for this module
        """
        l_riseset = RiseSetData()
        l_riseset.Sunrise = p_pyhouse_obj.House.OBJs.Location._Sunrise
        l_riseset.Sunset = p_pyhouse_obj.House.OBJs.Location._Sunset
        LOG.info("Sunrise:{0:}, Sunset:{1:}".format(l_riseset.Sunrise, l_riseset.Sunset))
        return l_riseset


class ScheduleExecution(object):

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
        self.m_schedule_timer = self.m_pyhouse_obj.Twisted.Reactor.callLater(PAUSE_DELAY, self.set_schedule_timer, None)

    def set_schedule_timer(self, _ignore):
        """Find out what schedules need to be done and how long to delay before they are due to be run.

        This is called by callLater so an ignored parameter is required.
        """
        l_seconds_to_delay, l_schedule_list = self.find_next_scheduled_events(self.m_pyhouse_obj)
        LOG.info('Delay: {0:} - List: {1:}'.format(l_seconds_to_delay, l_schedule_list))
        self.m_schedule_timer = self.m_pyhouse_obj.Twisted.Reactor.callLater(l_seconds_to_delay, self.execute_schedules_list, l_schedule_list)



class ScheduleUtility(ScheduleTime):

    def find_next_scheduled_events(self, p_pyhouse_obj):
        """
        Get the current time
        Go thru all the schedules and find the next schedules to run.
            Note that there may be several scheduled events for that time
        return the list and the delay time

        If the list is empty, wait a week.
        """
        l_riseset = self._get_sunrise_sunset(p_pyhouse_obj)
        l_now_daytime = self._now_daytime()  # Save value to avoid jitter
        l_time_scheduled = l_now_daytime
        # If nothing is found, use these defaults
        l_seconds_to_delay = SECONDS_IN_WEEK
        l_schedule_list = []

        for l_key, l_schedule_obj in p_pyhouse_obj.House.OBJs.Schedules.iteritems():
            if not l_schedule_obj.Active:
                continue
            l_time_sch = self._extract_time_of_day(l_schedule_obj, l_riseset)
            # now see if this is 1) part of a chain -or- 2) an earlier schedule
            l_diff = self._find_diff(l_time_sch, l_now_daytime)

            if l_diff == l_seconds_to_delay:  # Add to lists for the given time.
                l_schedule_list.append(l_key)
            elif l_diff < l_seconds_to_delay:  # earlier schedule upcoming.
                l_seconds_to_delay = l_diff
                l_schedule_list = []
                l_time_scheduled = l_time_sch
            # add to a chain

        l_debug_msg = "Delaying {0:} seconds until {1:} for list {2:}".format(l_seconds_to_delay, l_time_scheduled, l_schedule_list)
        LOG.info("find_next_scheduled_events complete. {0:}".format(l_debug_msg))
        return l_seconds_to_delay, l_schedule_list


class UpdatePyhouse(object):

    @staticmethod
    def add_api_references(p_pyhouse_obj):
        p_pyhouse_obj.APIs.LightingAPI = lighting.API()
        p_pyhouse_obj.APIs.HvacAPI = thermostats.API()
        p_pyhouse_obj.APIs.IrrigationAPI = irrigation.API()

    @staticmethod
    def start_scheduled_modules(p_pyhouse_obj):
        """
        TODO: Lighting must be first since it loads families etc.
        """
        p_pyhouse_obj.APIs.LightingAPI.Start(p_pyhouse_obj)
        p_pyhouse_obj.APIs.HvacAPI.Start(p_pyhouse_obj)
        p_pyhouse_obj.APIs.IrrigationAPI.Start(p_pyhouse_obj)

    @staticmethod
    def stop_scheduled_modules(p_pyhouse_obj):
        p_pyhouse_obj.APIs.HvacAPI.Stop()
        p_pyhouse_obj.APIs.LightingAPI.Stop()
        p_pyhouse_obj.APIs.IrrigationAPI.Stop()

    @staticmethod
    def save_scheduled_modules(p_pyhouse_obj, p_xml):
        p_pyhouse_obj.APIs.HvacAPI.SaveXml(p_xml)
        p_pyhouse_obj.APIs.LightingAPI.SaveXml(p_xml)
        p_pyhouse_obj.APIs.IrrigationAPI.SaveXml(p_xml)
        return p_xml


class API(ScheduleUtility, ScheduleExecution):
    """Instantiated once for each house (active or not)
    """

    m_sunrisesunset_api = None
    m_pyhouse_obj = None

    def _fetch_sunrise_set(self):
        l_sunrise = self.m_pyhouse_obj.House.OBJs.Location._Sunrise
        l_sunset = self.m_pyhouse_obj.House.OBJs.Location._Sunset
        LOG.info('Got Sunrise: {};   Sunset: {}'.format(l_sunrise, l_sunset))

    def Start(self, p_pyhouse_obj):
        """
        Extracts all from XML so an update will write correct info back out to the XML file.
        Does not schedule a next entry for inactive houses.

        @param p_house_obj: is a House object for the house being scheduled
        """
        LOG.info("Starting.")
        UpdatePyhouse.add_api_references(p_pyhouse_obj)
        self.m_pyhouse_obj = p_pyhouse_obj
        p_pyhouse_obj.House.OBJs.Schedules = schedule_xml.ReadWriteConfigXml().read_schedules_xml(p_pyhouse_obj)
        self._fetch_sunrise_set()
        UpdatePyhouse.start_scheduled_modules(p_pyhouse_obj)
        p_pyhouse_obj.Twisted.Reactor.callLater(INITIAL_DELAY, self.set_schedule_timer, None)

    def Stop(self):
        """Stop everything under me.
        """
        UpdatePyhouse.stop_scheduled_modules(self.m_pyhouse_obj)
        LOG.info("Stopped.")

    def RestartSchedule(self):
        LOG.info("Restart")
        self.find_next_scheduled_events(self.m_pyhouse_obj)
        pass

    def SaveXml(self, p_xml):
        p_xml.append(schedule_xml.ReadWriteConfigXml().write_schedules_xml(self.m_pyhouse_obj.House.OBJs.Schedules))
        UpdatePyhouse.save_scheduled_modules(self.m_pyhouse_obj, p_xml)

# ## END DBK
