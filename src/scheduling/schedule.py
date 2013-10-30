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
from src.lights import lighting
from src.utils import xml_tools
from src.utils import tools
from src.scheduling import sunrisesunset
from src.scheduling import VALID_SCHEDULING_TYPES

g_debug = 0
# 0 = off
# 1 = log extra info
# 2 = major routine entry
# 3 - Config file handling
# 4 = schedule execution
# 5 = diagnostics
# 6
# 7 = extract time details
g_logger = logging.getLogger('PyHouse.Schedule    ')

callLater = reactor.callLater


class ScheduleData(object):

    def __init__(self):
        self.Name = ''
        self.Key = 0
        self.Active = False
        self.Level = 0
        self.LightName = None
        self.LightNumber = 0  # Depricated methinks
        self.Object = None  # a light (perhaps other) object
        self.Rate = 0
        self.RoomName = None
        self.Time = None
        self.Type = 'Device'  # For future expansion into scenes, entertainment etc.
        self.UUID = None
        # for use by web browser - not saved in xml
        self.HouseIx = None
        self.DeleteFlag = False

    def XX__str__(self):
        l_ret = "Schedule:: "
        l_ret += "Name:{0:}, ".format(self.Name)
        l_ret += "LightName:{0:}, ".format(self.LightName)
        l_ret += "Time:{0:}, ".format(self.Time)
        l_ret += "Level:{0:}, ".format(self.Level)
        l_ret += "Rate:{0:}, ".format(self.Rate)
        l_ret += "Type:{0:}, ".format(self.Type)
        l_ret += "Key:{0:}, ".format(self.Key)
        l_ret += "Active:{0:}, ".format(self.Active)
        l_ret += "Room:{0:}, ".format(self.RoomName)
        l_ret += "UUID:{0:}".format(self.UUID)
        l_ret += "; "
        return l_ret

    def reprJSON(self):
        l_ret = dict(Name = self.Name, Key = self.Key, Active = self.Active,
                    Level = self.Level,
                    LightName = self.LightName, LightNumber = self.LightNumber, Rate = self.Rate,
                    RoomName = self.RoomName, Time = self.Time, Type = self.Type,
                    UUID = self.UUID)
        return l_ret


class ScheduleXML(xml_tools.ConfigTools):

    def extract_schedule_xml(self, p_entry_xml, p_schedule_obj):
        """Extract schedule information from a schedule xml element.
        """
        self.xml_read_common_info(p_schedule_obj, p_entry_xml)
        p_schedule_obj.Level = self.get_int_from_xml(p_entry_xml, 'Level')
        p_schedule_obj.LightName = self.get_text_from_xml(p_entry_xml, 'LightName')
        p_schedule_obj.LightNumber = self.get_int_from_xml(p_entry_xml, 'LightNumber')
        p_schedule_obj.Rate = self.get_int_from_xml(p_entry_xml, 'Rate')
        p_schedule_obj.RoomName = self.get_text_from_xml(p_entry_xml, 'RoomName')
        p_schedule_obj.Time = self.get_text_from_xml(p_entry_xml, 'Time')
        p_schedule_obj.Type = self.get_text_from_xml(p_entry_xml, 'Type')
        p_schedule_obj.UUID = self.get_uuid_from_xml(p_entry_xml, 'UUID')
        if g_debug >= 7:
            print "schedule.extract_schedule_xml()   Name:{0:}, Active:{1:}, Key:{2:}, Light:{3:}".format(
                    p_schedule_obj.Name, p_schedule_obj.Active, p_schedule_obj.Key, p_schedule_obj.LightName)
            print '    UUID:{0:}'.format(p_schedule_obj.UUID)
        return p_schedule_obj

    def read_schedules_xml(self, p_house_obj, p_house_xml):
        """
        @param p_house_obj: is the text name of the House.
        @param p_house_xml: is the e-tree XML house object
        @return: a dict of the entry to be attached to a house object.
        """
        l_count = 0
        l_dict = {}
        l_sect = p_house_xml.find('Schedules')
        try:
            l_list = l_sect.iterfind('Schedule')
            for l_entry in l_list:
                l_schedule_obj = ScheduleData()
                self.extract_schedule_xml(l_entry, l_schedule_obj)
                l_schedule_obj.Key = l_count  # Renumber
                l_dict[l_count] = l_schedule_obj
                l_count += 1
        except AttributeError:
            pass
        p_house_obj.Schedules = l_dict
        g_logger.info("Loaded {0:} schedules for house:{1:}.".format(l_count, self.m_house_obj.Name))
        return l_dict

    def write_schedules_xml(self, p_schedules_obj):
        """Replace all the data in the 'Schedules' section with the current data.
        @param p_parent: is the 'schedules' element
        """
        l_count = 0
        l_schedules_xml = ET.Element('Schedules')
        for l_schedule_obj in p_schedules_obj.itervalues():
            l_schedule_obj.Key = l_count
            l_entry = self.xml_create_common_element('Schedule', l_schedule_obj)
            self.put_int_element(l_entry, 'Level', l_schedule_obj.Level)
            self.put_text_element(l_entry, 'LightName', l_schedule_obj.LightName)
            self.put_int_element(l_entry, 'LightNumber', l_schedule_obj.LightNumber)
            self.put_int_element(l_entry, 'Rate', l_schedule_obj.Rate)
            self.put_text_element(l_entry, 'RoomName', l_schedule_obj.RoomName)
            self.put_text_element(l_entry, 'Time', l_schedule_obj.Time)
            self.put_text_element(l_entry, 'Type', l_schedule_obj.Type)
            self.put_text_element(l_entry, 'UUID', l_schedule_obj.UUID)
            l_count += 1
            l_schedules_xml.append(l_entry)
        if g_debug >= 3:
            print "schedule.write_schedules_xml() - Wrote {0:} schedules".format(len(l_schedules_xml))
        return l_schedules_xml


class ScheduleExecution(ScheduleData):

    def execute_schedule(self, p_slot_list = []):
        """
        For each SlotName in the passed in list, execute the scheduled event for the house..
        Delay before generating the next schedule to avoid a race condition
         that duplicates an event if it completes before the clock goes to the next second.

        @param p_slot_list: a list of Slots in the next time schedule to be executed.
        """
        g_logger.info("About to execute - House:{0:}, Schedule:{1:}".format(self.m_house_obj.Name, p_slot_list))
        for ix in range(len(p_slot_list)):
            l_sched_obj = self.m_house_obj.Schedules[p_slot_list[ix]]
            # TODO: We need a small dispatch for the various schedule types (hvac, security, entertainment, lights, ...)
            if l_sched_obj.Type == 'Device':
                pass
            elif l_sched_obj.Type == 'Scene':
                pass
            l_light_obj = tools.get_light_object(self.m_house_obj, name = l_sched_obj.LightName)
            g_logger.info("Executing schedule Name:{0:}, Light:{1:}, Level:{2:}".format(l_sched_obj.Name, l_sched_obj.LightName, l_sched_obj.Level))
            self.m_house_obj.LightingAPI.change_light_setting(self.m_house_obj, l_light_obj, l_sched_obj.Level)
        callLater(2, self.get_next_sched)

    def create_timer(self, p_seconds, p_list):
        """Create a timer that will go off when the next schedule time comes up on the clock.
        """
        callLater(p_seconds, self.execute_schedule, p_list)


class ScheduleUtility(ScheduleExecution):

    def _substitute(self, p_timefield):
        """Substitute for names in timefield.
        Supported fields are: 'sunset'. 'sunrise'
        Return the string timefield.
        """
        if 'sunset' in p_timefield:
            l_timefield = self.m_sunset.strftime('%H:%M')
            p_timefield = p_timefield.replace('sunset', l_timefield)
            if g_debug >= 7:
                print"schedule._substitute() found sunset -  '{0:}'".format(p_timefield)
        elif 'sunrise' in p_timefield:
            l_timefield = self.m_sunrise.strftime('%H:%M')
            p_timefield = p_timefield.replace('sunrise', l_timefield)
            if g_debug >= 7:
                print"schedule._substitute() found sunrise - '{0:}'".format(p_timefield)
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
                    print "schedule._extract_field() not HH:MM:SS - try shorter"
                try:
                    l_ret = datetime.datetime.strptime(p_timefield[0:5], '%H:%M')
                    p_timefield = p_timefield[5:]
                except ValueError:
                    if g_debug >= 7:
                        print "schedule._extract_field() ERROR not HH:MM - using 00:00:00"
                    l_ret = datetime.time(0, 0, 0)
            try:
                while p_timefield[0] == ' ':
                    p_timefield = p_timefield[1:]
            except IndexError:
                pass
            if g_debug >= 7:
                print "schedule._extract_field() Exit - {0:}, '{1:}'".format(l_ret, p_timefield)
        else:
            l_ret = datetime.time(0, 0, 0)
            if g_debug >= 7:
                print "schedule._extract_field() No ':' - Exit - {0:}, '{1:}'".format(l_ret, p_timefield)
        return l_ret, p_timefield

    def _extract_time(self, p_timefield):
        """Parse the schedule's time field.

        Convert the schedule time to an actual time of day.
        Sunset and sunrise are converted.
        Arithmetic is performed.
        seconds are forced to 00.

        @param p_timefield: a text field containing time information.
        @return: datetime.time of the time information.  Be careful of date wrapping!
        """
        if g_debug >= 7:
            print "schedule._extract_time() - {0:}".format(p_timefield)
        l_sub = False
        p_timefield += ' '
        if '-' in p_timefield:
            l_sub = True
            p_timefield = p_timefield.replace('-', ' ')
        elif '+' in p_timefield:
            p_timefield = p_timefield.replace('+', ' ')
        p_timefield = self._substitute(p_timefield)
        l_maintime, p_timefield = self._extract_field(p_timefield)
        l_offsettime, p_timefield = self._extract_field(p_timefield)
        if l_sub:
            l_td = datetime.timedelta(hours = l_maintime.hour, minutes = l_maintime.minute) - datetime.timedelta(hours = l_offsettime.hour, minutes = l_offsettime.minute)
        else:
            l_td = datetime.timedelta(hours = l_maintime.hour, minutes = l_maintime.minute) + datetime.timedelta(hours = l_offsettime.hour, minutes = l_offsettime.minute)
        l_timefield = datetime.time(hour = int(l_td.seconds / 3600), minute = int((l_td.seconds % 3600) / 60))
        if g_debug >= 7:
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
        if g_debug >= 4:
            print "schedule.get_next_sched() "
        l_now = datetime.datetime.now()
        l_time_now = datetime.time(l_now.hour, l_now.minute, l_now.second)
        self.m_sunrisesunset.Start(self.m_house_obj)
        self.m_sunset = self.m_sunrisesunset.get_sunset()
        self.m_sunrise = self.m_sunrisesunset.get_sunrise()
        if g_debug >= 7:
            print "schedule.get_next_sched() - sunrise/sunset = ", self.m_sunrise, self.m_sunset
        g_logger.info("Sunrise:{0:}, Sunset:{1:}".format(self.m_sunrise, self.m_sunset))
        l_time_scheduled = l_now
        l_next = 100000.0
        l_list = []
        for l_key, l_schedule_obj in self.m_house_obj.Schedules.iteritems():
            if g_debug >= 7:
                print "schedule.get_next_sched() sched=", l_schedule_obj
            # if not l_schedule_obj.Active:
            #    continue
            l_time_sch = self._extract_time(l_schedule_obj.Time)
            if g_debug >= 7:
                print "schedule.get_next_sched() - Schedule  SlotName: {0:}, Light: {1:}, Level: {2:}, Time: {3:}".format(l_schedule_obj.Name, l_schedule_obj.LightName,
                                                                                                                           l_schedule_obj.Level, l_time_sch)
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
        l_debug_msg = "Schedule - House:{0:}, delaying {1:} seconds until {2:} for list {3:}".format(self.m_house_obj.Name, l_next, l_time_scheduled, l_list)
        g_logger.info("Get_next_schedule complete. {0:}".format(l_debug_msg))
        if g_debug >= 4:
            print "schedule.get_next_sched()  {0:}".format(l_debug_msg)
        self.create_timer(l_next, l_list)


class API(ScheduleUtility, ScheduleXML):
    """Instantiated once for each house (active or not)
    """

    m_house_obj = None
    m_sunrisesunset = None
    #m_entertainment = None

    def __init__(self, p_house_obj):
        self.m_house_obj = p_house_obj
        self.m_sunrisesunset = sunrisesunset.API(p_house_obj)
        self.m_house_obj.LightingAPI = lighting.API(p_house_obj)
        #self.m_entertainment = entertainment.API()

    def Start(self, p_house_obj, p_house_xml):
        """Called once for each house.
        Extracts all from xml so an update will write correct info back out to the xml file.
        Does not schedule a next entry for inactive houses.

        @param p_house_obj: is a House object for the house being scheduled
        """
        self.m_house_obj = p_house_obj
        g_logger.info("Starting House {0:}.".format(self.m_house_obj.Name))
        self.m_sunrisesunset.Start(p_house_obj)
        self.read_schedules_xml(p_house_obj, p_house_xml)
        self.m_house_obj.LightingAPI.Start(p_house_obj, p_house_xml)
        #self.m_entertainment.Start(p_house_obj, p_house_xml)
        if p_house_obj.Active:
            self.get_next_sched()
        g_logger.info("Started.")

    def Stop(self, p_xml, p_house_obj):
        """Stop everything under me and build xml to be appended to a house xml.
        """
        g_logger.info("Stopping schedule for house:{0:}.".format(self.m_house_obj.Name))
        self.m_house_obj.LightingAPI.Stop(p_xml, p_house_obj)
        #l_entertainment_xml = self.m_entertainment.Stop()
        if g_debug >= 2:
            print "schedule.API.Stop() - House:{0:}, {1:}".format(self.m_house_obj.Name, len(p_xml))
        g_logger.info("Stopped.\n")
        #return l_schedules_xml, l_lighting_xml, l_buttons_xml, l_controllers_xml  #, l_entertainment_xml

    def UpdateXml (self, p_xml):
        p_xml.append(self.write_schedules_xml(self.m_house_obj.Schedules))
        self.m_house_obj.LightingAPI.UpdateXml(p_xml)

# ## END DBK
