#!/usr/bin/env python

"""Handle the home automation system schedule.
This is a Main Module - always present.

The schedule is at the core of PyMh.
Lighting events, entertainment events etc. are triggered by the schedule and are run by twisted.

Read/reread the schedule file at:
    1. Start up
    2. Midnight
    3. After each set of scheduled events.
"""

# Import system type stuff
import datetime
import logging
import time

# Import PyMh files
import configure
# from configure import config_xml
import entertainment.entertainment as entertainment
import lighting.lighting as lighting
import sunrisesunset


# Configure_Data = configure_mh.Configure_Data
Schedule_Data = {}

ScheduleCount = 0
Scheduled_Namelist = []
g_debug = 0
g_logger = None
g_reactor = None

VALID_TYPES = ['Device', 'Scene']

class ScheduleData(object):

    def __init__(self):
        global ScheduleCount
        ScheduleCount += 1
        self.Active = None
        self.Key = 0
        self.Level = 0
        self.LightName = None
        self.Rate = 0
        self.Name = 0
        self.Time = None
        self.Type = 'Device'

    def __repr__(self):
        l_ret = "Schedule Name:{0:}, LightName:{1:}, Time:{2:}, Level:{3:}, Rate:{4:}, Type:{5:}".format(
                self.Name, self.LightName, self.Time, self.Level, self.Rate, self.Type)
        return l_ret


class ScheduleAPI(ScheduleData):

    def get_ScheduleCount(self):
        return ScheduleCount

    def load_all_schedules(self, p_dict):
        for l_key, l_obj in p_dict.iteritems():
            self.load_schedule(l_key, l_obj)

    def load_schedule(self, p_Name, p_obj):
        l_key = self.get_ScheduleCount()
        l_sched = ScheduleData()
        l_sched.Active = p_obj.get('Active', False)
        l_sched.Key = l_key
        l_sched.Level = p_obj.get('Level', 0)
        l_sched.LightName = p_obj.get('Name', 'NoLightName')
        l_sched.Rate = p_obj.get('Rate', 0)
        l_sched.Name = p_Name
        l_sched.Time = p_obj.get('Time', None)
        l_sched.Type = p_obj.get('Type', None)
        Schedule_Data[l_key] = l_sched

    def load_schedules_xml(self):
        configure.config_xml.ReadConfig().read_schedules()

    def dump_all_schedules(self):
        if g_debug < 7: return
        print "***** All Schedules *****"
        for l_key, l_obj in Schedule_Data.iteritems():
            print "~~~Schedule: {0:}".format(l_key)
            print "     ", l_obj
        print

    def update_schedule(self, p_schedule):
        """Update the schedule as updated by the web server.
        """
        if g_debug > 5: print 'schedule.schedule.update_schedule({0:}'.format(p_schedule)
        Schedule_Data = p_schedule
        configure.config_xml.WriteConfig().write_schedules()


class ScheduleExecution(ScheduleAPI):

    def _get_Name_info(self, p_Name, p_obj):
        """Be sure we get values in case someone mis-edits the config file.
        """
        try:
            l_device = p_obj.LightName
        except AttributeError:
            l_device = '**no-such-device**'
            l_message = 'Schedule for Name {0:} has no LightName/Device entry'.format(p_Name)
            g_logger.error(l_message)

        try:
            l_type = p_obj.Type
        except AttributeError:
            l_type = '**no-such-Type**'
            l_message = 'Schedule for Name {0:} has no Type entry'.format(p_Name)
            g_logger.error('Schedule for Name {0:} has no Type entry'.format(p_Name))

        try:
            l_level = int(p_obj.Level)
        except AttributeError:
            l_level = 0

        try:
            l_rate = int(p_obj.Rate)
        except AttributeError:
            l_rate = 0

        l_message = 'For Name={0:}, Device={1:}, Type={2:}, Level={3:}, Rate={4:}'.format(p_Name, l_device, l_type, l_level, l_rate)
        g_logger.info(l_message)
        return (l_device, l_type, l_level, l_rate)

    def execute_schedule(self, p_Name = []):
        """
        For each Name in the passed in list, execute the scheduled event.
        Delay before generating the next schedule to avoid a race condition
        that duplicates an event if it completes before the clock goes to the next second.

        @param p_Name: a list of Names in the next time schedule
        """
        if g_debug > 3: print " Execute_schedule p_Name=>>{0:}<<".format(p_Name)
        for ix in range(len(p_Name)):
            l_Name = p_Name[ix]
            l_obj = Schedule_Data[l_Name]
            (l_device, _l_type, l_level, _l_rate) = self._get_Name_info(l_Name, l_obj)
            lighting.LightingUtility().change_light_setting(l_device, l_level)
        # TODO change this to a non blocking call.
        time.sleep(1)
        self.get_next_sched()

    def create_timer(self, p_seconds, p_list):
        """Create a timer that will go off when the next Name time comes up on the clock.
        """
        g_reactor.callLater(p_seconds, self.execute_schedule, p_list)


class ScheduleUtility(ScheduleExecution):

    def _extract_time(self, p_timefield):
        """Convert the schedule time to an actual time of day.
        Sunset and sunrise are converted.
        Arithmetic is performed.
        seconds are forced to 00.
        Returns a datetime.time of the Name information.  Be careful of date wrapping!

        WIP
        """
        l_timefield = p_timefield
        if 'sunset' in l_timefield:
            l_timefield = self.m_sunset
        elif 'sunrise' in l_timefield:
            l_timefield = self.m_sunrise
        else:
            l_time = time.strptime(p_timefield, '%H:%M')
            l_timefield = datetime.time(l_time.tm_hour, l_time.tm_min)
        if '+' in p_timefield:
            pass
        if '-' in p_timefield:
            pass
        return l_timefield

    def _make_delta(self, p_time):
        """Convert a date time to a timedelta.
        Notice that seconds are truncated to be 0.
        """
        return datetime.timedelta(0, p_time.second, 0, 0, p_time.minute, p_time.hour)

    def get_next_sched(self):
        """Get the next schedule from the current time.
        Be sure to get the next in a chain of things happening at the same time.
        Establish a list of Names that have equal schedule times
        """
        l_now = datetime.datetime.now()
        l_time_now = datetime.time(l_now.hour, l_now.minute, l_now.second)
        _l_date = datetime.date(l_now.year, l_now.month, l_now.day)
        # sunrisesunset.SSAPI().set_date(l_date)
        sunrisesunset.Start()
        self.m_sunset = sunrisesunset.SSAPI().get_sunset()
        self.m_sunrise = sunrisesunset.SSAPI().get_sunrise()
        if g_debug > 0: print "-Schedule - sunrise/sunset = ", self.m_sunrise, self.m_sunset
        g_logger.info("Sunrise:{0:}, Sunset:{1:}".format(self.m_sunrise, self.m_sunset))
        l_time_scheduled = l_now
        l_next = 100000.0
        l_list = []
        for l_key, l_obj in Schedule_Data.iteritems():
            if not l_obj.Active: continue
            l_time = l_obj.Time
            l_time_sch = self._extract_time(l_time)
            if g_debug > 1: print " - Schedule ", l_time_sch
            # now see if this is 1) part of a chain -or- 2) an earlier schedule
            l_diff = self._make_delta(l_time_sch).total_seconds() - self._make_delta(l_time_now).total_seconds()
            if l_diff < 0:
                l_diff = l_diff + 86400.0  # tomorrow
            # earlier schedule upcoming.
            if l_diff < l_next:
                l_next = l_diff
                l_list = []
                l_time_scheduled = l_time_sch
            # add to a chain
            if l_diff == l_next:
                l_list.append(l_key)
        g_logger.info("Get_next_schedule complete. Delaying {0:} seconds until {1:}, Namelist = {2:}".format(l_next, l_time_scheduled, l_list))
        self.create_timer(l_next, l_list)
        return l_next


def Init():
    """Set up the scheduled items initialization.
    """
    global g_logger
    g_logger = logging.getLogger('PyHouse.Schedule')
    g_logger.info("Initializing.")
    sunrisesunset.Init()
    entertainment.Init()
    lighting.Init()
    ScheduleAPI().load_schedules_xml()
    if g_debug > 2: ScheduleAPI().dump_all_schedules()
    g_logger.info("Initialized.")

def Start(p_reactor):
    global g_reactor
    g_reactor = p_reactor
    lighting.Start(g_reactor)
    Reload()
    g_logger.info("Started.")

def Reload():
    ScheduleUtility().get_next_sched()

def Stop():
    lighting.Stop()

# ## END
