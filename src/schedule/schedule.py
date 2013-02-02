#!/usr/bin/env python

"""Handle the home automation system schedule for one house.

The schedule is at the core of PyHouse.
Lighting events, entertainment events, etc. for one house are triggered by the schedule and are run by twisted.

Read/reread the schedule file at:
    1. Start up
    2. Midnight
    3. After each set of scheduled events.
"""

# Import system type stuff
import datetime
import logging
import xml.etree.ElementTree as ET
from twisted.internet import reactor

# Import PyMh files
from entertainment import entertainment
from lighting import lighting
from configure import xml_tools
from main import tools
import sunrisesunset

g_debug = 0

g_logger = None
g_house_obj = None
g_lighting = None

ScheduleCount = 0

callLater = reactor.callLater

VALID_TYPES = ['Device', 'Scene']

class ScheduleData(object):

    def __init__(self):
        global ScheduleCount
        ScheduleCount += 1
        self.Active = None
        self.HouseName = None
        self.Key = 0
        self.Level = 0
        self.LightName = None
        self.LightNumber = 0
        self.Name = 0
        self.Object = None  # a light (perhaps other) object
        self.Rate = 0
        self.RoomName = None
        self.Time = None
        self.Type = 'Device'

    def __repr__(self):
        l_ret = "Schedule:: SlotName:{0:}, LightName:{1:}, Time:{2:}, Level:{3:}, Rate:{4:}, Type:{5:}, HouseName:{6:}, Key:{7:}, Active:{8:}, RoomName:{9:}".format(
                self.Name, self.LightName, self.Time, self.Level, self.Rate, self.Type, self.HouseName, self.Key, self.Active, self.RoomName)
        l_ret += "<<  "
        return l_ret


class ScheduleXML(xml_tools.ConfigTools):

    def read_schedules(self, p_entry, p_house):
        """
        @param p_entry: is the e-tree XML house object
        @param p_house: is the text name of the House.
        @return: a dict of the entry to be attached to a house object.
        """
        if g_debug > 7:
            print "schedule.read_schedules()"
        l_count = 0
        l_dict = {}
        l_sect = p_entry.find('Schedules')
        l_list = l_sect.iterfind('Schedule')
        for l_entry in l_list:
            l_obj = ScheduleData()
            self.read_common(l_obj, l_entry)
            l_obj.HouseName = p_house
            l_obj.Level = self.get_int(l_entry, 'Level')
            l_obj.LightName = self.get_text(l_entry, 'LightName')
            l_obj.LightNumber = self.get_int(l_entry, 'LightNumber')
            l_obj.Rate = self.get_int(l_entry, 'Rate')
            l_obj.RoomName = self.get_text(l_entry, 'RoomName')
            l_obj.Time = self.get_text(l_entry, 'Time')
            l_obj.Type = self.get_text(l_entry, 'Type')
            l_dict[l_count] = l_obj
            l_count += 1
            if g_debug > 7:
                print "schedule.read_schedules()   Name:{0:}, Active:{1:}, Key:{2:}, Light:{3:}".format(l_obj.Name, l_obj.Active, l_obj.Key, l_obj.LightName)
                # print "     ", l_obj
        if g_debug > 4:
            print "schedule.read_schedule()  loaded {0:} schedules for {1:}".format(l_count, p_house)
        return l_dict

    def write_schedules(self, p_parent, p_dict):
        """Replace all the data in the 'Schedules' section with the current data.
        """
        l_count = 0
        l_sect = ET.SubElement(p_parent, 'Schedules')
        for l_obj in p_dict.itervalues():
            l_entry = self.build_common(l_sect, 'Schedule', l_obj)
            ET.SubElement(l_entry, 'HouseName').text = str(l_obj.HouseName)
            ET.SubElement(l_entry, 'Level').text = str(l_obj.Level)
            ET.SubElement(l_entry, 'LightName').text = l_obj.LightName
            ET.SubElement(l_entry, 'LightNumber').text = str(l_obj.LightNumber)
            ET.SubElement(l_entry, 'Rate').text = str(l_obj.Rate)
            ET.SubElement(l_entry, 'RoomName').text = str(l_obj.RoomName)
            ET.SubElement(l_entry, 'Time').text = l_obj.Time
            ET.SubElement(l_entry, 'Type').text = l_obj.Type
            l_count += 1
        if g_debug > 4:
            print "schedule.write_schedules() - Wrote {0:} schedules".format(l_count)


class ScheduleExecution(ScheduleData):

    def execute_schedule(self, p_slot_list = []):
        """
        For each SlotName in the passed in list, execute the scheduled event for the house..
        Delay before generating the next schedule to avoid a race condition
        that duplicates an event if it completes before the clock goes to the next second.

        @param p_slot_list: a list of Slots in the next time schedule
        """
        if g_debug > 0:
            print "schedule.execute_schedules()  p_slot_list {0:}".format(p_slot_list), g_house_obj
        for ix in range(len(p_slot_list)):
            l_sched_obj = g_house_obj.Schedule[p_slot_list[ix]]
            l_light_obj = tools.get_light_object(g_house_obj, name = l_sched_obj.LightName)
            if g_debug > 2:
                print "schedule.execute_schedules() ", l_sched_obj
                print "                          ", l_light_obj
            g_lighting.change_light_setting(g_house_obj, l_sched_obj.LightNumber, l_sched_obj.Level)
        callLater(2, self.get_next_sched)

    def create_timer(self, p_seconds, p_list):
        """Create a timer that will go off when the next Name time comes up on the clock.
        """
        callLater(p_seconds, self.execute_schedule, p_list)


class ScheduleUtility(ScheduleExecution):

    def _find_numbers(self, p_field):
        pass

    def _extract_time(self, p_timefield):
        """Convert the schedule time to an actual time of day.
        Sunset and sunrise are converted.
        Arithmetic is performed.
        seconds are forced to 00.

        @param p_timefield: a text field containing time information.
        @return: datetime.time of the time information.  Be careful of date wrapping!
        """
        l_ptime = p_timefield
        l_timefield = datetime.time(0, 0, 0)
        if 'sunset' in p_timefield:
            l_timefield = self.m_sunset
            l_ptime = l_ptime[6:]
        elif 'sunrise' in p_timefield:
            l_timefield = self.m_sunrise
            l_ptime = l_ptime[7:]
        #
        if ':' in p_timefield:
            try:
                h, m = map(int, p_timefield.split(':'))
                l_ret = datetime.time(h, m, 0)
            except ValueError:
                h, m = map(int, l_ptime.split(':'))
                l_ret = datetime.time(h, m, 0)
        else:
            l_ret = datetime.time(0, 0, 0)
        #
        if '-' in p_timefield:
            l_td = datetime.timedelta(hours = l_timefield.hour, minutes = l_timefield.minute) - datetime.timedelta(hours = l_ret.hour, minutes = l_ret.minute)
        else:
            l_td = datetime.timedelta(hours = l_timefield.hour, minutes = l_timefield.minute) + datetime.timedelta(hours = l_ret.hour, minutes = l_ret.minute)
        l_timefield = datetime.time(hour = int(l_td.seconds / 3600), minute = int((l_td.seconds % 3600) / 60))
        if g_debug > 5:
            print "schedule._extract_time({0:}) = {1:}".format(p_timefield, l_timefield)
        return l_timefield

    def _make_delta(self, p_time):
        """Convert a date time to a timedelta.
        """
        return datetime.timedelta(0, p_time.second, 0, 0, p_time.minute, p_time.hour)

    def get_next_sched(self):
        """Get the next schedule from the current time.
        Be sure to get the next in a chain of things happening at the same time.
        Establish a list of Names that have equal schedule times
        """
        if g_debug > 1:
            print "schedule.get_next_sched() ", g_house_obj
        l_now = datetime.datetime.now()
        l_time_now = datetime.time(l_now.hour, l_now.minute, l_now.second)
        self.m_sunrisesunset.Start(g_house_obj)
        self.m_sunset = self.m_sunrisesunset.get_sunset()
        self.m_sunrise = self.m_sunrisesunset.get_sunrise()
        if g_debug > 3:
            print "schedule.get_next_sched() - sunrise/sunset = ", self.m_sunrise, self.m_sunset
        g_logger.info("Sunrise:{0:}, Sunset:{1:}".format(self.m_sunrise, self.m_sunset))
        l_time_scheduled = l_now
        l_next = 100000.0
        l_list = []
        for l_key, l_obj in g_house_obj.Schedule.iteritems():
            if g_debug > 4:
                print "schedule.get_next_sched() sched=", l_obj
            # if not l_obj.Active:
            #    continue
            l_time_sch = self._extract_time(l_obj.Time)
            if g_debug > 4:
                print "schedule.get_next_sched() - Schedule  SlotName: {0:}, Light: {1:}, Level: {2:}, Time: {3:}".format(l_obj.Name, l_obj.LightName, l_obj.Level, l_time_sch)
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
        if g_debug > 1:
            print "schedule.get_next_sched() - Complete. delaying {0:} seconds until {1:}".format(l_next, l_time_scheduled)
        self.create_timer(l_next, l_list)


class API(ScheduleUtility, ScheduleXML):
    """Instantiated once for each house (active or not)
    """


    def __init__(self):
        """
        """
        if g_debug > 0:
            print "schedule.__init__()"
        global g_logger, g_lighting
        g_logger = logging.getLogger('PyHouse.Schedule')
        g_logger.info("Initializing house")
        self.m_sunrisesunset = sunrisesunset.API()
        self.m_entertainment = entertainment.Init()
        self.m_lighting = lighting.API()
        g_lighting = self.m_lighting
        g_logger.info("Initialized.")

    def Start(self, p_obj):
        """Called once for each active house.

        @param p_obj: is a House object for the house being scheduled
        """
        if g_debug > 0:
            print "schedule.Start() for House:{0:}".format(p_obj.Name)
        global g_house_obj
        g_house_obj = p_obj
        g_logger.info("Starting.")
        self.m_sunrisesunset.Start(p_obj)
        self.get_next_sched()
        # self.m_entertainment.Start()
        self.m_lighting.Start(p_obj)
        g_logger.info("Started.")
        return self

    def Stop(self):
        if g_debug > 0:
            print "schedule.Stop()"
        g_logger.info("Stopping.")
        # self.m_entertainment.Stop()
        self.m_lighting.Stop()
        g_logger.info("Stopped.\n\n\n")

    def update_schedule(self, p_schedule):
        """Update the schedule as updated by the web server.
        """
        if g_debug > 5:
            print 'schedule.scheduleAPI.update_schedule({0:}'.format(p_schedule)
        pass

# ## END
