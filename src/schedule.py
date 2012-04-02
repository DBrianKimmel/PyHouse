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
import pprint
import time
#from twisted.internet.defer import Deferred

# Import PyMh files
import configure_mh
import entertainment
import lighting
import sunrisesunset


"""A dict of data about each schedule entry (slot).
Schedule_Data[Slot]{'Time': 'xxx', 'Type':'xxx', ... }

Slot = schedule number/name to identify the slot (may change on save).
Type = Device | Scene
Name = light or scene name
Time = Sunrise or sunset + optional offset -or- time
Level = 0 (off), 100 (on) or 1-99 (dim if supported)
Rate = Optional - 0 (predefined) -or- 1-9 (if supported)
"""
Schedule_Data = {} # hold the internal dict of dicts of all the schedule slots configured.


class ScheduleData(object):

    Scheduled_Slotlist = []


class ScheduleExecution(ScheduleData):

    def _get_slot_info(self, p_slot, p_dict):
        """Be sure we get values in case someone misedit's the config file.
        """
        try:
            l_device = p_dict['Name']
        except:
            l_device = '**no-such-device**'
            l_message = 'Schedule for slot {0:} has no Name/Device entry'.format(p_slot)
            self.m_logger.error(l_message)

        try:
            l_type = p_dict['Type']
        except:
            l_type = '**no-such-Type**'
            l_message = 'Schedule for slot {0:} has no Type entry'.format(p_slot)
            self.m_logger.error(l_message)

        try:
            l_level = int(p_dict['Level'])
        except:
            l_level = 0

        try:
            l_rate = int(p_dict['Rate'])
        except:
            l_rate = 0

        l_message = 'For slot={0:}, Device={1:}, Type={2:}, Level={3:}, Rate={4:}'.format(p_slot, l_device, l_type, l_level, l_rate)
        self.m_logger.info(l_message)
        return (l_device, l_type, l_level, l_rate)

    def execute_schedule(self, p_slot = []):
        for ix in range(len(p_slot)):
            l_slot = self.Scheduled_Slotlist[ix]
            l_dict = Schedule_Data[l_slot]
            (l_device, _l_type, l_level, _l_rate) = self._get_slot_info(l_slot, l_dict)
            self.m_lighting.change_light_setting(l_device, l_level)
        time.sleep(10)
        self.get_next_sched()

    def create_timer(self, p_seconds):
        l_slot = self.execute_schedule
        self.m_reactor.callLater(p_seconds, l_slot, self.Scheduled_Slotlist)


class ScheduleUtility(ScheduleExecution):

    def load_schedule(self):
        """Load all the schedule entries.
        """
        l_config = self.m_config.get_value()
        if 'Schedule' in l_config:
            p_dict = l_config['Schedule']
            for l_slot, l_dict in p_dict.iteritems():
                Schedule_Data[l_slot] = {}
                Schedule_Data[l_slot]['Type'] = 'None'
                Schedule_Data[l_slot]['Name'] = 'NoName'
                Schedule_Data[l_slot]['Time'] = 0
                Schedule_Data[l_slot]['Level'] = 0
                Schedule_Data[l_slot]['Rate'] = 0
                for l_key, l_value in l_dict.iteritems():
                    l_kl = l_key.lower()
                    if l_kl == 'device':
                        Schedule_Data[l_slot]['Name'] = l_value
                        Schedule_Data[l_slot]['Type'] = 'Device'
                    elif l_kl == 'link':
                        Schedule_Data[l_slot]['Name'] = l_value
                        Schedule_Data[l_slot]['Type'] = 'Scene'
                    elif l_kl == 'name':
                        Schedule_Data[l_slot]['Name'] = l_value
                    elif l_kl == 'type':
                        Schedule_Data[l_slot]['Type'] = l_value
                    elif l_kl == 'time':
                        Schedule_Data[l_slot]['Time'] = l_value
                    elif l_kl == 'level':
                        Schedule_Data[l_slot]['Level'] = l_value
                    elif l_kl == 'rate':
                        Schedule_Data[l_slot]['Rate'] = l_value
                    elif l_kl == 'state':
                        if l_value.lower() == 'off':
                            Schedule_Data[l_slot]['Level'] = 0
                    else:
                        Schedule_Data[l_slot][l_key] = l_value
        return Schedule_Data

    def updateSchedule(self, p_schedule):
        """Update the schedule as updated by the web server.
        """
        #pprint.pprint(p_schedule, width = 40, indent = 4)
        Schedule_Data = p_schedule
        configure_mh.write_module(self, Dict = Schedule_Data, Section = 'Schedule')
        #self.load_schedule()

    def _extract_time(self, p_timefield):
        """Convert the schedule time to an actual time of day.
        Sunset and sunrise are converted.
        Arithmetic is performed.
        seconds are forced to 00.
        Returns a datetime.time of the slot information.  Be careful of date wrapping!
        
        WIP
        """
        l_timefield = p_timefield
        if 'sunset' in l_timefield:
            l_timefield = self.m_sun.get_sunset()
        elif 'sunrise' in l_timefield:
            l_timefield = self.m_sun.get_sunrise()
        else:
            l_time = time.strptime(p_timefield, '%H:%M')
            l_timefield = datetime.time(l_time.tm_hour, l_time.tm_min)
        if '+' in p_timefield:
            pass
        if '-' in p_timefield:
            pass
        return l_timefield

    def dump_schedule(self):
        """Print out the schedule in a nice format for debugging.
        """
        print "\n   Schedule_Data follows:"
        pprint.pprint(Schedule_Data, width = 40, indent = 4)
        print "   Schedule_Slotlist follows:"
        pprint.pprint(self.Scheduled_Slotlist, width = 40, indent = 4)
        print "------------------"

    def _make_delta(self, p_time):
        """Convert a date time to a timedelta.
        Notice that seconds are truncated to be 0.
        """
        return datetime.timedelta(0, p_time.second, 0, 0, p_time.minute, p_time.hour)

    def get_next_sched(self):
        """Get the next schedule from the current time.
        Be sure to get the next in a chain of things happening at the same time.
        Establish a list of slots that have equal schedule times
        """
        l_now = datetime.datetime.now()
        l_time_now = datetime.time(l_now.hour, l_now.minute, l_now.second)
        l_date = datetime.date(l_now.year, l_now.month, l_now.day)
        l_time_scheduled = l_now
        self.m_sun.set_date(l_date)
        l_next = 100000.0
        self.Scheduled_Slotlist = []
        for l_key, l_value in Schedule_Data.iteritems():
            if 'Time' in l_value:
                l_time = l_value['Time']
            else:
                l_time = '23:59'
            l_time_sch = self._extract_time(l_time)
            # now see if this is 1) part of a chain -or- 2) an earlier schedule
            l_diff = self._make_delta(l_time_sch).total_seconds() - self._make_delta(l_time_now).total_seconds()
            if l_diff < 0:
                l_diff = l_diff + 86400.0 # tomorrow
            # earlier schedule upcoming.
            if l_diff < l_next:
                l_next = l_diff
                self.Scheduled_Slotlist = []
                l_time_scheduled = l_time_sch
            # add to a chain
            if l_diff == l_next:
                self.Scheduled_Slotlist.append(l_key)
        l_message = "Get_next_schedule complete. Delaying {0:} seconds until {1:}, Slotlist = {2:}".format(l_next, l_time_scheduled, self.Scheduled_Slotlist)
        self.m_logger.info(l_message)
        self.create_timer(l_next)
        return l_next


class ScheduleAPI(ScheduleUtility):
    """ All the external methods.
    """

    def get_all_schedule_slots(self):
        """
        """
        self.m_logger.info("Retrieving Schedule Info")
        return Schedule_Data


Singletons = {}

class ScheduleMain(ScheduleAPI):

    def __new__(cls, *args, **kwargs):
        """Create a singleton.
        """
        if cls in Singletons:
            return Singletons[cls]
        self = object.__new__(cls)
        cls.__init__(self, *args, **kwargs)
        Singletons[cls] = self
        #print " = ScheduleMain 1"
        self.m_logger = logging.getLogger('PyHouse.Schedule')
        self.m_logger.info("Initializing.")
        #print " = ScheduleMain 2"
        self.m_config = configure_mh.ConfigureMain()
        self.m_sun = sunrisesunset.SunriseSunsetMain()
        #print " = ScheduleMain 3"
        self.m_entertainment = entertainment.EntertainmentMain()
        #print " = ScheduleMain 4"
        self.m_lighting = lighting.LightingMain()
        self.load_schedule()
        self.m_logger.info("Initialized.")
        return self

    def __init__(self):
        """Constructor for the schedule.
        Schedule controls lighting and entertainment modules.
        """

    def configure(self):
        """Set up the proper schedules according to the config files.
        """
        self.m_logger.info("Configured.")

    def start(self, p_reactor):
        """
        """
        self.m_reactor = p_reactor
        self.m_lighting.lighting_startup()
        self.m_delay = self.m_next = self.get_next_sched()
        self.m_logger.info("Started.")

### END
