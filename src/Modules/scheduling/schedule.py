"""


Handle the home automation system schedule for one house.

The schedule is at the Core of PyHouse.
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
  Select the next event(s) from now, there may be more than one event scheduled for the same time.

  Create a twisted timer that goes off when the scheduled time arrives.
  We only create one timer (ATM) so that we do not have to cancel timers when the schedule is edited.

  TODO: create a group of timers and cancel the changed ones when the schedules object is changed.
          Keep all times as UTC - display them as local time for editing.
"""

# Import system type stuff
import datetime
import xml.etree.ElementTree as ET
from twisted.internet import reactor

# Import PyMh files
from Modules.Core.data_objects import ScheduleData
from Modules.lights import lighting
from Modules.utils import xml_tools
from Modules.utils import tools
from Modules.scheduling import sunrisesunset
from Modules.utils import pyh_log


g_debug = 0
# 0 = off
# 1 = log extra info
LOG = pyh_log.getLogger('PyHouse.Schedule    ')

callLater = reactor.callLater


class ScheduleXML(xml_tools.ConfigTools):

    m_count = 0

    def read_one_schedule_xml(self, p_schedule_element):
        """Extract schedule information from a schedule xml element.
        """
        l_schedule_obj = ScheduleData()
        self.read_base_object_xml(l_schedule_obj, p_schedule_element)
        l_schedule_obj.Level = self.get_int_from_xml(p_schedule_element, 'Level')
        l_schedule_obj.LightName = self.get_text_from_xml(p_schedule_element, 'LightName')
        l_schedule_obj.LightNumber = self.get_int_from_xml(p_schedule_element, 'LightNumber')
        l_schedule_obj.Rate = self.get_int_from_xml(p_schedule_element, 'Rate')
        l_schedule_obj.RoomName = self.get_text_from_xml(p_schedule_element, 'RoomName')
        l_schedule_obj.Time = self.get_text_from_xml(p_schedule_element, 'Time')
        l_schedule_obj.Type = self.get_text_from_xml(p_schedule_element, 'Type')
        return l_schedule_obj

    def read_schedules_xml(self, p_schedules_xml):
        """
        @param p_house_xml: is the e-tree XML house object
        @return: a dict of the entry to be attached to a house object.
        """
        self.m_count = 0
        l_dict = {}
        try:
            l_list = p_schedules_xml.iterfind('Schedule')
            for l_entry in l_list:
                l_schedule_obj = self.read_one_schedule_xml(l_entry)
                # self.read_one_schedule_xml(l_entry)
                l_schedule_obj.Key = self.m_count  # Renumber
                l_dict[self.m_count] = l_schedule_obj
                self.m_count += 1
        except AttributeError:
            print('ERROR ')
        return l_dict

    def write_one_schedule_xml(self, p_schedule_obj):
        """
        """
        l_entry = self.write_base_object_xml('Schedule', p_schedule_obj)
        self.put_int_element(l_entry, 'Key', self.m_count)
        self.put_int_element(l_entry, 'Level', p_schedule_obj.Level)
        self.put_text_element(l_entry, 'LightName', p_schedule_obj.LightName)
        self.put_int_element(l_entry, 'LightNumber', p_schedule_obj.LightNumber)
        self.put_int_element(l_entry, 'Rate', p_schedule_obj.Rate)
        self.put_text_element(l_entry, 'RoomName', p_schedule_obj.RoomName)
        self.put_text_element(l_entry, 'Time', p_schedule_obj.Time)
        self.put_text_element(l_entry, 'Type', p_schedule_obj.Type)
        return l_entry

    def write_schedules_xml(self, p_schedules_obj):
        """Replace all the data in the 'Schedules' section with the current data.
        @param p_parent: is the 'schedules' element
        """
        self.m_count = 0
        l_xml = ET.Element('Schedules')
        for l_schedule_obj in p_schedules_obj.itervalues():
            l_entry = self.write_one_schedule_xml(l_schedule_obj)
            l_xml.append(l_entry)
            self.m_count += 1
        return l_xml



class ScheduleExecution(ScheduleData):

    def execute_schedule(self, p_slot_list = []):
        """
        For each SlotName in the passed in list, execute the scheduled event for the house.
        Delay before generating the next schedule to avoid a race condition
         that duplicates an event if it completes before the clock goes to the next second.

        @param p_slot_list: a list of Slots in the next time schedule to be executed.
        """
        LOG.info("About to execute - House:{0:}, Schedule:{1:}".format(self.m_house_obj.Name, p_slot_list))
        for ix in range(len(p_slot_list)):
            l_sched_obj = self.m_house_obj.Schedules[p_slot_list[ix]]
            # TODO: We need a small dispatch for the various schedule types (hvac, security, entertainment, lights, ...)
            if l_sched_obj.Type == 'Device':
                pass
            elif l_sched_obj.Type == 'Scene':
                pass
            l_light_obj = tools.get_light_object(self.m_house_obj, name = l_sched_obj.LightName)
            LOG.info("Executing schedule Name:{0:}, Light:{1:}, Level:{2:}".format(l_sched_obj.Name, l_sched_obj.LightName, l_sched_obj.Level))
            self.m_house_obj.LightingAPI.ChangeLight(l_light_obj, l_sched_obj.Level)
        callLater(5, self.get_next_sched)

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
        elif 'sunrise' in p_timefield:
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
                    print("schedule._extract_field() not HH:MM:SS - try shorter")
                try:
                    l_ret = datetime.datetime.strptime(p_timefield[0:5], '%H:%M')
                    p_timefield = p_timefield[5:]
                except ValueError:
                    if g_debug >= 7:
                        print("schedule._extract_field() ERROR not HH:MM - using 00:00:00")
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
            print("schedule._extract_time() - {0:}".format(p_timefield))
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
            print("schedule._extract_time({0:}) = {1:}".format(p_timefield, l_timefield))
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
        l_now = datetime.datetime.now()
        l_time_now = datetime.time(l_now.hour, l_now.minute, l_now.second)
        self.m_sunrisesunset.Start(self.m_pyhouse_obj, self.m_house_obj)
        self.m_sunset = self.m_sunrisesunset.get_sunset()
        self.m_sunrise = self.m_sunrisesunset.get_sunrise()
        LOG.info("In get_next_sched - Sunrise:{0:}, Sunset:{1:}".format(self.m_sunrise, self.m_sunset))
        l_time_scheduled = l_now
        l_next = 100000.0
        l_list = []
        for l_key, l_schedule_obj in self.m_house_obj.Schedules.iteritems():
            if not l_schedule_obj.Active:
                continue
            l_time_sch = self._extract_time(l_schedule_obj.Time)
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
        LOG.info("Get_next_schedule complete. {0:}".format(l_debug_msg))
        self.create_timer(l_next, l_list)

    def find_house(self):
        pass


class API(ScheduleUtility, ScheduleXML):
    """Instantiated once for each house (active or not)
    """

    m_house_obj = None
    m_sunrisesunset = None

    def __init__(self):
        self.m_sunrisesunset = sunrisesunset.API()

    def Start(self, p_pyhouse_obj):
        """Called once for each house.
        Extracts all from xml so an update will write correct info back out to the xml file.
        Does not schedule a next entry for inactive houses.

        @param p_house_obj: is a House object for the house being scheduled
        """
        self.m_house_obj = p_pyhouse_obj.HouseData
        self.m_house_xml = p_pyhouse_obj.XmlParsed
        self.m_pyhouse_obj = p_pyhouse_obj
        self.m_house_obj.LightingAPI = lighting.API()
        LOG.info("Starting House {0:}.".format(self.m_house_obj.Name))
        self.m_sunrisesunset.Start(p_pyhouse_obj, self.m_house_obj)
        self.m_house_obj.Schedules = self.read_schedules_xml(self.m_house_xml)
        self.m_house_obj.LightingAPI.Start(p_pyhouse_obj)
        if self.m_house_obj.Active:
            self.get_next_sched()

    def Stop(self, p_xml):
        """Stop everything under me and build xml to be appended to a house xml.
        """
        LOG.info("Stopping schedule for house:{0:}.".format(self.m_house_obj.Name))
        p_xml.append(self.write_schedules_xml(self.m_house_obj.Schedules))
        self.m_house_obj.LightingAPI.Stop(p_xml)
        LOG.info("Stopped.\n")

# ## END DBK
