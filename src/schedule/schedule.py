#!/usr/bin/env python

"""Handle the home automation system schedule for one house.

The schedule is at the core of PyHouse.
Lighting events, entertainment events, etc. for one house are triggered by the schedule and are run by twisted.

Read/reread the schedule file at:
    1. Start up
    2. Midnight
    3. After each set of scheduled events.


Controls:
  Lighting
  HVAC
  Security
  Entertainment

Operation:

  Iterate thru the schedule tree and create a list of schedule events.
  Create a twisted timer that goes off when the scheduled time arrives.
  We only create one timer (ATM) so that we do not have to cancel timers when the schedule is edited.
  TODO: create a group of timers and cancel the changed ones when the schedules object is changed.
  Select the next event(s) from now, there may be more than one event scheduled for the same time.

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

g_debug = 3
g_logger = None

ScheduleCount = 0

callLater = reactor.callLater

# A list of valid schedule types.
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

    def extract_schedule_xml(self, p_entry_xml, p_schedule_obj):
        """Extract schedule information from a schedule xml element.
        """
        self.read_common(p_schedule_obj, p_entry_xml)
        p_schedule_obj.HouseName = self.m_house_obj.Name
        p_schedule_obj.Level = self.get_int(p_entry_xml, 'Level')
        p_schedule_obj.LightName = self.get_text(p_entry_xml, 'LightName')
        p_schedule_obj.LightNumber = self.get_int(p_entry_xml, 'LightNumber')
        p_schedule_obj.Rate = self.get_int(p_entry_xml, 'Rate')
        p_schedule_obj.RoomName = self.get_text(p_entry_xml, 'RoomName')
        p_schedule_obj.Time = self.get_text(p_entry_xml, 'Time')
        p_schedule_obj.Type = self.get_text(p_entry_xml, 'Type')
        if g_debug > 5:
            print "schedule.extract_schedule_xml()   Name:{0:}, Active:{1:}, Key:{2:}, Light:{3:}".format(
                    p_schedule_obj.Name, p_schedule_obj.Active, p_schedule_obj.Key, p_schedule_obj.LightName)
        return p_schedule_obj

    def read_schedules(self, p_house_obj, p_house_xml):
        """
        @param p_house_obj: is the text name of the House.
        @param p_house_xml: is the e-tree XML house object
        @return: a dict of the entry to be attached to a house object.
        """
        if g_debug > 3:
            print "schedule.read_schedules()"
        l_count = 0
        l_dict = {}
        l_sect = p_house_xml.find('Schedules')
        l_list = l_sect.iterfind('Schedule')
        for l_entry in l_list:
            l_obj = ScheduleData()
            self.extract_schedule_xml(l_entry, l_obj)
            l_dict[l_count] = l_obj
            l_count += 1
        p_house_obj.Schedule = l_dict
        if g_debug > 4:
            print "schedule.read_schedule()  loaded {0:} schedules for {1:}".format(l_count, p_house_obj.Name)
        return l_dict

    def write_schedules(self, p_parent, p_schedule_obj):
        """Replace all the data in the 'Schedules' section with the current data.
        @param p_parent: is the 'schedules' element
        """
        if g_debug > 3:
            print "schedule.write_schedules()"
        l_count = 0
        for l_obj in p_schedule_obj.itervalues():
            l_entry = self.build_common(p_parent, 'Schedule', l_obj)
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
            print "schedule.execute_schedules()  p_slot_list {0:}, House:{1:}".format(p_slot_list, self.m_house_obj.Name)
        for ix in range(len(p_slot_list)):
            l_sched_obj = self.m_house_obj.Schedule[p_slot_list[ix]]
            if l_sched_obj.Type == 'Device':
                pass
            elif l_sched_obj.Type == 'Scene':
                pass
            l_light_obj = tools.get_light_object(self.m_house_obj, name = l_sched_obj.LightName)
            if g_debug > 2:
                print "schedule.execute_schedules() ", l_sched_obj
                print "   on light", l_light_obj
            g_logger.info("Executing schedule Name:{0:}, Light:{1:}, Level:{2:}".format(l_sched_obj.Name, l_sched_obj.LightName, l_sched_obj.Level))
            self.m_lighting.change_light_setting(self.m_house_obj, l_light_obj, l_sched_obj.Level)
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
            print "schedule.get_next_sched() "
        l_now = datetime.datetime.now()
        l_time_now = datetime.time(l_now.hour, l_now.minute, l_now.second)
        self.m_sunrisesunset.Start(self.m_house_obj)
        self.m_sunset = self.m_sunrisesunset.get_sunset()
        self.m_sunrise = self.m_sunrisesunset.get_sunrise()
        if g_debug > 5:
            print "schedule.get_next_sched() - sunrise/sunset = ", self.m_sunrise, self.m_sunset
        g_logger.info("Sunrise:{0:}, Sunset:{1:}".format(self.m_sunrise, self.m_sunset))
        l_time_scheduled = l_now
        l_next = 100000.0
        l_list = []
        for l_key, l_obj in self.m_house_obj.Schedule.iteritems():
            if g_debug > 5:
                print "schedule.get_next_sched() sched=", l_obj
            # if not l_obj.Active:
            #    continue
            l_time_sch = self._extract_time(l_obj.Time)
            if g_debug > 5:
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
        global g_logger
        g_logger = logging.getLogger('PyHouse.Schedule')
        g_logger.info("Initializing house")
        g_logger.info("Initialized.")

    def Start(self, p_house_obj, p_house_xml):
        """Called once for each active house.

        @param p_house_obj: is a House object for the house being scheduled
        """
        self.m_house_obj = p_house_obj
        if g_debug > 0:
            print "schedule.API.Start() for House:{0:}".format(p_house_obj.Name)
        g_logger.info("Starting House {0:}.".format(self.m_house_obj.Name))
        self.read_schedules(self.m_house_obj, p_house_xml)
        self.m_sunrisesunset = sunrisesunset.API()
        self.m_lighting = lighting.API()
        self.m_entertainment = entertainment.API()
        p_house_obj.LightingAPI = self.m_lighting

        self.m_sunrisesunset.Start(self.m_house_obj)
        self.m_lighting.Start(self.m_house_obj, p_house_xml)
        self.m_entertainment.Start(self.m_house_obj, p_house_xml)

        self.get_next_sched()
        g_logger.info("Started.")

    def Stop(self, p_xml):
        """Stop everything under me and build xml to be appended to a house xml.
        """
        if g_debug > 0:
            print "schedule.API.Stop() - House:{0:}".format(self.m_house_obj.Name)
        g_logger.info("Stopping house {0:}.".format(self.m_house_obj.Name))
        l_schedules_xml = ET.Element('Schedules')
        self.write_schedules(l_schedules_xml, self.m_house_obj.Schedule)
        p_xml.append(l_schedules_xml)
        _l_lighting_xml = self.m_lighting.Stop(p_xml)
        _l_entertainment_xml = self.m_entertainment.Stop(p_xml)
        # p_xml.append(l_lighting_xml)
        # p_xml.append(l_entertainment_xml)
        if g_debug > 0:
            print "schedule.API.Stop() - 2 "
        g_logger.info("Stopped.\n\n\n")
        return p_xml

    def update_schedule(self, p_schedule):
        """Update the schedule as updated by the web server.
        """
        if g_debug > 5:
            print 'schedule.scheduleAPI.update_schedule({0:}'.format(p_schedule)
        pass

# ## END
