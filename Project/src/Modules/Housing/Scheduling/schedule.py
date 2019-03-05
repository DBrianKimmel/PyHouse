"""
-*- test-case-name: PyHouse.src.Modules.Scheduling.test.test_schedule -*-

@name:      PyHouse/src/Modules/Scheduling/schedule.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2013-2019 by D. Brian Kimmel
@license:   MIT License
@note:      Created on Apr 8, 2013
@summary:   Schedule events


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
    Security
    UPNP

Operation:

  Iterate thru the schedule tree and create a list of schedule events.
  Select the next event(s) from now, there may be more than one event scheduled for the same time.

  Create a twisted timer that goes off when the scheduled time arrives.
  We only create one timer (ATM) so that we do not have to cancel timers when the schedule is edited.
"""

__updated__ = '2019-02-25'

#  Import system type stuff
import datetime
import aniso8601

#  Import PyMh files
from Modules.Core.Utilities import convert, extract_tools
from Modules.Housing.Hvac.hvac_actions import API as hvacActionsAPI
from Modules.Housing.Irrigation.irrigation_action import API as irrigationActionsAPI
from Modules.Housing.Lighting.lighting_actions import API as lightActionsAPI
from Modules.Housing.Scheduling.schedule_xml import Xml as scheduleXml
from Modules.Housing.Scheduling import sunrisesunset

from Modules.Computer import logging_pyh as Logger
LOG = Logger.getLogger('PyHouse.Schedule       ')

SECONDS_IN_MINUTE = 60
SECONDS_IN_HOUR = SECONDS_IN_MINUTE * 60  # 3600
SECONDS_IN_DAY = SECONDS_IN_HOUR * 24  # 86400
SECONDS_IN_WEEK = SECONDS_IN_DAY * 7  # 604800

INITIAL_DELAY = 5  # Must be from 5 to 30 seconds.
PAUSE_DELAY = 5
MINIMUM_TIME = 30  # We will not schedule items less than this number of seconds.  Avoid race conditions.


class MqttActions(object):
    """
    """

    def __init__(self, p_pyhouse_obj):
        self.m_pyhouse_obj = p_pyhouse_obj

    def decode(self, p_topic, p_message):
        """
        --> pyhouse/housename/schedule/...
        """
        l_logmsg = ''
        l_schedule_type = extract_tools.get_mqtt_field(p_message, 'ScheduleType')
        l_light_name = extract_tools.get_mqtt_field(p_message, 'LightName')
        l_light_level = extract_tools.get_mqtt_field(p_message, 'Level')
        if len(p_topic) > 0:
            if p_topic[0] == 'execute':
                l_logmsg += '\tExecute:\n'
                l_logmsg += '\tType: {}\n'.format(l_schedule_type)
                # l_logmsg += '\tRoom: {}\n'.format(self.m_room_name)
                l_logmsg += '\tLight: {}\n'.format(l_light_name)
                l_logmsg += '\tLevel: {}'.format(l_light_level)
            elif p_topic[0] == 'status':
                l_logmsg += '\tStatus:\n'
                l_logmsg += '\tType: {}\n'.format(l_schedule_type)
                l_logmsg += '\tLight: {}\n'.format(l_light_name)
                l_logmsg += '\tLevel: {}'.format(l_light_level)
            elif p_topic[0] == 'control':
                l_logmsg += '\tControl:\n'
            else:
                l_logmsg += '\tUnknown sub-topic: {}; - {}'.format(p_topic, p_message)
        return l_logmsg


class RiseSet(object):

    def __init__(self):
        self.SunRise = None
        self.SunSet = None


class SchedTime:
    """
    Get the when scheduled time.  It may be from about a minute to about 1 week.
    If the schedule is not active return a None
    This class deals with extracting information from the time and DOW fields of a schedule.

    DOW        mon=1, tue=2, wed=4, thu=8, fri=16, sat=32, sun=64
    weekday    mon=0, tue=1, wed=2, thu=3, fri=4,  sat=5,  sun=6

    The time field may be:
        HH:MM or HH:MM:SS
        sunrise/sunset/dawn/dusk  +/-  offset HH:MM:SS or HH:MM
    """

    @staticmethod
    def _extract_days(p_schedule_obj, p_now):
        """ Get the number of days until the next DOW in the schedule.

        DOW        mon=1, tue=2, wed=4, thu=8, fri=16, sat=32, sun=64
        weekday()  mon=0, tue=1, wed=2, thu=3, fri=4,  sat=5,  sun=6

        @param p_schedule_obj: is the schedule object we are working on
        @param p_now: is a datetime.datetime.now()
        @return: the number of days till the next DOW - 0..6, 10 if never
        """
        l_dow = p_schedule_obj.DOW
        l_now_day = p_now.weekday()
        l_day = 2 ** l_now_day
        l_is_in_dow = (l_dow & l_day) != 0
        if l_is_in_dow:
            return 0
        l_days = 1
        for _l_ix in range(0, 7):
            l_now_day = (l_now_day + 1) % 7
            l_day = 2 ** l_now_day
            l_is_in_dow = (l_dow & l_day) != 0
            if l_is_in_dow:
                return l_days
            l_days += 1
        return 10

    @staticmethod
    def _extract_time_part(p_timefield):
        """
        """
        try:
            l_time = aniso8601.parse_time(p_timefield)
        except Exception:
            l_time = datetime.time(0)
        return convert.datetime_to_seconds(l_time)

    @staticmethod
    def _extract_schedule_time(p_schedule_obj, p_rise_set):
        """ Find the number of minutes from midnight until the schedule time for action.

        Possible valid formats are:
            hh:mm:ss
            hh:mm
            sunrise
            sunrise + hh:mm
            sunrise - hh:mm
        @return: the number of seconds
        """
        l_timefield = p_schedule_obj.Time.lower()
        if 'dawn' in l_timefield:
            # print('Dawn - {}'.format(l_timefield))
            l_base = convert.datetime_to_seconds(p_rise_set.Dawn)
            l_timefield = l_timefield[4:]
        elif 'sunrise' in l_timefield:
            # print('SunRise - {}'.format(l_timefield))
            l_base = convert.datetime_to_seconds(p_rise_set.SunRise)
            l_timefield = l_timefield[7:]
        elif 'noon' in l_timefield:
            # print('Noon - {}'.format(l_timefield))
            l_base = convert.datetime_to_seconds(p_rise_set.Noon)
            l_timefield = l_timefield[4:]
        elif 'sunset' in l_timefield:
            # print('SunSet - {}'.format(l_timefield))
            l_base = convert.datetime_to_seconds(p_rise_set.SunSet)
            l_timefield = l_timefield[6:]
        elif 'dusk' in l_timefield:
            # print('Dusk - {}'.format(l_timefield))
            l_base = convert.datetime_to_seconds(p_rise_set.Dusk)
            l_timefield = l_timefield[4:]
        else:
            l_base = 0
        l_timefield = l_timefield.strip()
        l_subflag = False
        if '-' in l_timefield:
            l_subflag = True
            l_timefield = l_timefield[1:]
        elif '+' in l_timefield:
            l_subflag = False
            l_timefield = l_timefield[1:]
        # l_timefield = l_timefield.strip()

        l_offset = SchedTime._extract_time_part(l_timefield)
        #
        #
        if l_subflag:
            l_seconds = l_base - l_offset
        else:
            l_seconds = l_base + l_offset
        #
        return l_seconds

    @staticmethod
    def extract_time_to_go(_p_pyhouse_obj, p_schedule_obj, p_now, p_rise_set):
        """ Compute the seconds to go from now to the next scheduled time.
        May be from 30 seconds to a full week.

        @param p_pyhouse_obj: Not used yet
        @param p_schedule_obj: is the schedule object we are working on.
        @param p_now: is the datetime for now.
        @param p_rise_set: is the sunrise/sunset structure.
        @return: The number of seconds from now to the scheduled time.
        """
        l_dow_seconds = SchedTime._extract_days(p_schedule_obj, p_now) * 24 * 60 * 60
        l_sched_seconds = SchedTime._extract_schedule_time(p_schedule_obj, p_rise_set)
        l_sched_secs = l_dow_seconds + l_sched_seconds
        l_now_seconds = convert.datetime_to_seconds(p_now)
        l_seconds = l_sched_secs - l_now_seconds
        if l_seconds < 0:
            l_seconds += SECONDS_IN_DAY
        return l_seconds


class ScheduleExecution:

    def dispatch_one_schedule(self, p_pyhouse_obj, p_schedule_obj):
        """
        Send information to one device to execute a schedule.
        """
        l_topic = 'schedule/execute/{}'.format(p_schedule_obj.ScheduleType)
        l_obj = p_schedule_obj
        p_pyhouse_obj.APIs.Computer.MqttAPI.MqttPublish(l_topic, l_obj)
        #
        if p_schedule_obj.ScheduleType == 'Lighting':
            LOG.info('Execute_one_schedule type = Lighting')
            lightActionsAPI().DoSchedule(p_pyhouse_obj, p_schedule_obj)
        #
        elif p_schedule_obj.ScheduleType == 'Hvac':
            LOG.info('Execute_one_schedule type = Hvac')
            hvacActionsAPI().DoSchedule(p_pyhouse_obj, p_schedule_obj)
        #
        elif p_schedule_obj.ScheduleType == 'Irrigation':
            LOG.info('Execute_one_schedule type = Hvac')
            irrigationActionsAPI().DoSchedule(p_pyhouse_obj, p_schedule_obj)
        #
        elif p_schedule_obj.ScheduleType == 'TeStInG14159':  # To allow a path for unit tests
            LOG.info('Execute_one_schedule type = Testing')
            #  scheduleActionsAPI().DoSchedule(p_pyhouse_obj, p_schedule_obj)
        #
        else:
            LOG.error('Unknown schedule type: {}'.format(p_schedule_obj.ScheduleType))
            irrigationActionsAPI().DoSchedule(p_pyhouse_obj, p_schedule_obj)

    @staticmethod
    def execute_schedules_list(p_pyhouse_obj, p_key_list=[]):
        """ The timer calls this with a list of schedules to be executed.

        For each Schedule in the list, call the dispatcher for that type of schedule.

        Delay before generating the next schedule to avoid a race condition
         that duplicates an event if it completes before the clock goes to the next second.

        @param p_key_list: a list of schedule keys in the next time schedule to be executed.
        """
        LOG.info("About to execute - Schedule Items:{}".format(p_key_list))
        for l_slot in range(len(p_key_list)):
            l_schedule_obj = p_pyhouse_obj.House.Schedules[p_key_list[l_slot]]
            ScheduleExecution().dispatch_one_schedule(p_pyhouse_obj, l_schedule_obj)
        Utility.schedule_next_event(p_pyhouse_obj)


class Utility(object):
    """
    """

    @staticmethod
    def _setup_components(p_pyhouse_obj):
        # p_pyhouse_obj.House.Schedules = {}
        pass

    @staticmethod
    def fetch_sunrise_set(p_pyhouse_obj):
        _l_topic = 'schedule/sunrise_set'
        l_riseset = p_pyhouse_obj.House.Location.RiseSet  # RiseSetData()
        LOG.info('Got Sunrise: {};   Sunset: {}'.format(l_riseset.SunRise, l_riseset.SunSet))
        # p_pyhouse_obj.APIs.Computer.MqttAPI.MqttPublish(l_topic, l_riseset)
        return l_riseset

    @staticmethod
    def find_next_scheduled_events(p_pyhouse_obj, p_now):
        """ Go thru all the schedules and find the next schedule list to run.
        Note that there may be several scheduled events for that time

        @param p_now: is a datetime that we are searching for.
        @return: a delay time to the next event chain, and a list of events in the chain.
        """
        l_schedule_key_list = []
        l_min_seconds = SECONDS_IN_WEEK
        l_riseset = Utility.fetch_sunrise_set(p_pyhouse_obj)
        # Loop through the possible scheduled events.
        for l_key, l_schedule_obj in p_pyhouse_obj.House.Schedules.items():
            if not l_schedule_obj.Active:
                continue  # Skip inactive schedules.
            l_seconds = SchedTime.extract_time_to_go(p_pyhouse_obj, l_schedule_obj, p_now, l_riseset)
            if l_seconds < MINIMUM_TIME:
                continue
            if l_min_seconds == l_seconds:  # Add to lists for the given time.
                l_schedule_key_list.append(l_key)
            elif l_seconds < l_min_seconds:  # earlier schedule - start new list
                l_min_seconds = l_seconds
                l_schedule_key_list = []
                l_schedule_key_list.append(l_key)
        l_debug_msg = "Delaying {} for list {}".format(l_min_seconds, l_schedule_key_list)
        LOG.info("find next scheduled events complete. {}".format(l_debug_msg))
        return l_min_seconds, l_schedule_key_list

    @staticmethod
    def run_after_delay(p_pyhouse_obj, p_delay, p_list):
        """
        """
        l_runID = p_pyhouse_obj.Twisted.Reactor.callLater(p_delay, ScheduleExecution.execute_schedules_list, p_pyhouse_obj, p_list)
        l_datetime = datetime.datetime.fromtimestamp(l_runID.getTime())
        LOG.info('Scheduled {} after delay of {} - Time: {}'.format(p_list, p_delay, l_datetime))
        return l_runID

    @staticmethod
    def schedule_next_event(p_pyhouse_obj, p_delay=0):
        """ Find the list of schedules to run, call the timer to run at the time in the schedules.

        This is the main schedule loop.
        It may be restarted if the schedules change.

        Scans through the list of scheduled events.
        Picks out all the events next to perform (there may be several).
        Puts all the events in a list.
        Schedules an execution event on the list of scheduled events.

        @param p_pyhouse_obj: is the grand repository of information
        @param p_delay: is the (forced) delay time for the timer.
        """
        l_now = datetime.datetime.now()  # Freeze the current time so it is the same for every event in the list.
        l_delay, l_list = Utility.find_next_scheduled_events(p_pyhouse_obj, l_now)
        if p_delay != 0:
            l_delay = p_delay
        Utility.run_after_delay(p_pyhouse_obj, l_delay, l_list)


class Timers(object):
    """
    """

    def __init__(self, p_pyhouse_obj):
        self.m_pyhouse_obj = p_pyhouse_obj
        self.m_timers = {}
        self.m_count = 0

    def set_one(self, p_pyhouse_obj, p_delay, p_list):
        l_callback = ScheduleExecution.execute_schedules_list
        l_runID = p_pyhouse_obj.Twisted.Reactor.callLater(p_delay, l_callback, p_pyhouse_obj, p_list)
        l_datetime = datetime.datetime.fromtimestamp(l_runID.getTime())
        LOG.info('Scheduled {} after delay of {} - Time: {}'.format(p_list, p_delay, l_datetime))
        return l_runID


class API:

    m_pyhouse_obj = None

    def __init__(self, p_pyhouse_obj):
        self.m_pyhouse_obj = p_pyhouse_obj
        Utility._setup_components(p_pyhouse_obj)
        LOG.info("Initialized.")

    def LoadXml(self, p_pyhouse_obj):
        """ Load the Schedule from the XML info.
        """
        p_pyhouse_obj.House.Schedules = {}
        l_schedules = scheduleXml.read_schedules_xml(p_pyhouse_obj)
        p_pyhouse_obj.House.Schedules = l_schedules
        LOG.info('Loaded {} Schedules XML'.format(len(l_schedules)))
        return l_schedules  # for testing

    def Start(self):
        """
        Extracts all from XML so an update will write correct info back out to the XML file.
        """
        sunrisesunset.API(self.m_pyhouse_obj).Start()
        self.RestartSchedule()
        LOG.info("Started.")

    def Stop(self):
        """Stop everything.
        """
        LOG.info("Stopped.")

    def SaveXml(self, p_xml):
        """
        """
        l_xml, l_count = scheduleXml.write_schedules_xml(self.m_pyhouse_obj.House.Schedules)
        p_xml.append(l_xml)
        LOG.info('Saved {} Schedules XML.'.format(l_count))
        return l_xml  # for testing

    def RestartSchedule(self):
        """ Anything that alters the schedules should call this to cause the new schedules to take effect.
        """
        self.m_pyhouse_obj.Twisted.Reactor.callLater(INITIAL_DELAY, Utility.schedule_next_event, self.m_pyhouse_obj)

    def DecodeMqtt(self, p_topic, p_message):
        """ Decode messages sent to the house module.
        """
        l_logmsg = MqttActions(self.m_pyhouse_obj).decode(p_topic, p_message)
        return l_logmsg

# ## END DBK
