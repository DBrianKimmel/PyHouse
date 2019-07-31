"""
@name:      Modules/House/Schedules/schedule.py
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

__updated__ = '2019-07-31'
__version_info__ = (19, 5, 1)
__version__ = '.'.join(map(str, __version_info__))

#  Import system type stuff
import datetime
import aniso8601

#  Import PyMh files
from Modules.Core.Utilities import convert, extract_tools, config_tools
from Modules.Core.data_objects import ScheduleBaseData
from Modules.House.Hvac.hvac_actions import API as hvacActionsAPI
from Modules.House.Irrigation.irrigation_action import API as irrigationActionsAPI
from Modules.House.Lighting.lighting_actions import API as lightActionsAPI
from Modules.House.Lighting.lighting_utility import Utility as lightingUtility
from Modules.House.Schedule import sunrisesunset

from Modules.Core.Utilities.debug_tools import PrettyFormatAny

from Modules.Core import logging_pyh as Logger
LOG = Logger.getLogger('PyHouse.Schedule       ')

SECONDS_IN_MINUTE = 60
SECONDS_IN_HOUR = SECONDS_IN_MINUTE * 60  # 3600
SECONDS_IN_DAY = SECONDS_IN_HOUR * 24  # 86400
SECONDS_IN_WEEK = SECONDS_IN_DAY * 7  # 604800

INITIAL_DELAY = 5  # Must be from 5 to 30 seconds.
PAUSE_DELAY = 5
MINIMUM_TIME = 30  # We will not schedule items less than this number of seconds.  Avoid race conditions.
CONFIG_FILE_NAME = 'schedule.yaml'


class ScheduleInformation:
    """
    """

    def __init__(self):
        self.Name = None
        self.Comment = None
        self.DayOfWeek = None  # a bitmask (0-127) of days the time is valid {mon=1, tue=2, wed=4, thu=8, fri=16, sat=32, sun=64}
        self.Occupancy = 'Always'  # Always, Home, Away, Vacation, ...
        self.Type = ''  # Valid Schedule Type
        self.Time = None
        self.Light = None


class ScheduleLightInformation:
    """
    """

    def __init__(self):
        self.Brightness = 0
        self.Name = None
        self.Rate = 0
        self.Duration = None
        self.RoomName = None


class RiseSet:

    def __init__(self):
        self.SunRise = None
        self.SunSet = None


class MqttActions:
    """ Schedule will react to some mqtt messages.
    Messages with the topic:
        ==> pyhouse/<housename>/house/schedule/<action>
    where <action> is:
        control:
    """

    def __init__(self, p_pyhouse_obj):
        self.m_pyhouse_obj = p_pyhouse_obj

    def _add_schedule(self, p_message):
        """ A (remote) node has published a schedule - Add it to our schedules.
        """
        l_sender = extract_tools.get_mqtt_field(p_message, 'Sender')
        l_msg_obj = (p_message)
        # LOG.debug('Sched: {}\n{}'.format(p_message, PrettyFormatAny.form(l_msg_obj, 'Schedule', 190)))
        LOG.debug('Sched: {}\n{}'.format(p_message, l_msg_obj))
        if l_sender == self.m_pyhouse_obj.Computer.Name:
            return
        l_name = extract_tools.get_mqtt_field(p_message, 'LightName')
        l_light_obj = lightingUtility().get_object_by_id(self.m_pyhouse_obj.House.Lighting.Lights, name=l_name)
        if l_light_obj == None:
            return
        l_key = len(self.m_pyhouse_obj.House.Schedules)
        l_sched = ScheduleBaseData()
        l_sched.Name = l_name
        l_sched.Key = l_key
        l_sched.Active = True
        l_sched.Comment = extract_tools.get_mqtt_field(p_message, 'Comment')
        l_sched.LastUpdate = datetime.datetime.now()
        l_sched.UUID = extract_tools.get_mqtt_field(p_message, 'UUID')
        l_sched.DayOfWeek = extract_tools.get_mqtt_field(p_message, 'DayOfWeek')
        l_sched.ScheduleMode = extract_tools.get_mqtt_field(p_message, 'ScheduleMode')
        l_sched.ScheduleType = extract_tools.get_mqtt_field(p_message, 'ScheduleType')
        l_sched.Time = extract_tools.get_mqtt_field(p_message, 'Time')
        l_sched.Level = extract_tools.get_mqtt_field(p_message, 'Level')
        l_sched.LightName = extract_tools.get_mqtt_field(p_message, 'LightName')
        l_sched.LightUUID = extract_tools.get_mqtt_field(p_message, 'LightUUID')
        l_sched.Rate = extract_tools.get_mqtt_field(p_message, 'Rate')
        l_sched.RoomName = extract_tools.get_mqtt_field(p_message, 'RoomName')
        l_sched.RoomUUID = extract_tools.get_mqtt_field(p_message, 'RoomUUID')
        LOG.debug('Schedule added locally: {}'.format(PrettyFormatAny.form(l_sched, 'Schedule', 190)))

    def decode(self, p_topic, p_message, p_logmsg):
        """
        --> pyhouse/<housename>/house/schedule/...
        """
        p_logmsg += ''
        l_schedule_type = extract_tools.get_mqtt_field(p_message, 'ScheduleType')
        l_light_name = extract_tools.get_mqtt_field(p_message, 'LightName')
        l_light_level = extract_tools.get_mqtt_field(p_message, 'Level')
        if len(p_topic) > 0:
            if p_topic[0] == 'control':
                p_logmsg += '\tExecute:\n'
                p_logmsg += '\tType: {}\n'.format(l_schedule_type)
                p_logmsg += '\tLight: {}\n'.format(l_light_name)
                p_logmsg += '\tLevel: {}'.format(l_light_level)
                self._add_schedule(p_message)
            elif p_topic[0] == 'status':
                p_logmsg += '\tStatus:\n'
                p_logmsg += '\tType: {}\n'.format(l_schedule_type)
                p_logmsg += '\tLight: {}\n'.format(l_light_name)
                p_logmsg += '\tLevel: {}'.format(l_light_level)
            elif p_topic[0] == 'control':
                p_logmsg += '\tControl:\n'
            elif p_topic[0] == 'delete':
                pass
            elif p_topic[0] == 'update':
                pass
            else:
                p_logmsg += '\tUnknown sub-topic: {}; - {}'.format(p_topic, p_message)
                LOG.warn('Unknown Schedule Topic: {}'.format(p_topic[0]))
        return p_logmsg


class TimeField:
    """ This class deals with the Time Field parsing.

        Possible valid formats are:
        hh
        hh:mm
        hh:mm:ss
        sunrise
        sunrise + hh
        sunrise + hh:mm
        sunrise + hh:mm:ss
        sunrise - hh
        sunrise - hh:mm
        sunrise - hh:mm:ss
    """

    m_seconds = 0

    def _rise_set(self, p_timefield, p_rise_set):
        """
        """
        l_seconds = 0
        l_timefield = p_timefield.lower().strip()
        if 'dawn' in l_timefield:
            l_seconds = convert.datetime_to_seconds(p_rise_set.Dawn)
            l_timefield = l_timefield[4:].strip()
        elif 'sunrise' in l_timefield:
            l_seconds = convert.datetime_to_seconds(p_rise_set.SunRise)
            l_timefield = l_timefield[7:].strip()
        elif 'noon' in l_timefield:
            # print('Noon - {}'.format(l_timefield))
            l_seconds = convert.datetime_to_seconds(p_rise_set.Noon)
            l_timefield = l_timefield[4:].strip()
        elif 'sunset' in l_timefield:
            # print('SunSet - {}'.format(l_timefield))
            l_seconds = convert.datetime_to_seconds(p_rise_set.SunSet)
            l_timefield = l_timefield[6:].strip()
        elif 'dusk' in l_timefield:
            # print('Dusk - {}'.format(l_timefield))
            l_seconds = convert.datetime_to_seconds(p_rise_set.Dusk)
            l_timefield = l_timefield[4:].strip()
        else:
            l_seconds = 0
        self.m_seconds = l_seconds
        return l_timefield, l_seconds

    def _extract_sign(self, p_timefield):
        """
        """
        l_timefield = p_timefield.strip()
        l_subflag = False
        if '-' in l_timefield:
            l_subflag = True
            l_timefield = l_timefield[1:]
        elif '+' in l_timefield:
            l_subflag = False
            l_timefield = l_timefield[1:]
        l_timefield = l_timefield.strip()
        return l_timefield, l_subflag

    def _extract_time_part(self, p_timefield):
        """
        """
        try:
            l_time = aniso8601.parse_time(p_timefield)
        except Exception:
            l_time = datetime.time(0)
        return convert.datetime_to_seconds(l_time)

    def parse_timefield(self, p_timefield, p_rise_set):
        """
        """
        l_timefield, l_seconds = self._rise_set(p_timefield, p_rise_set)
        l_timefield, l_subflag = self._extract_sign(l_timefield)
        l_offset = self._extract_time_part(l_timefield)
        if l_subflag:
            l_seconds -= l_offset
        else:
            l_seconds += l_offset
        return l_seconds

    def get_timefield_seconds(self):
        return self.m_seconds


class SchedTime:
    """
    Get the when scheduled time.  It may be from about a minute to about 1 week.
    If the schedule is not active return a None
    This class deals with extracting information from the time and DayOfWeek fields of a schedule.

    DayOfWeek        mon=1, tue=2, wed=4, thu=8, fri=16, sat=32, sun=64
    weekday    mon=0, tue=1, wed=2, thu=3, fri=4,  sat=5,  sun=6

    The time field may be:
        HH:MM or HH:MM:SS
        sunrise/sunset/dawn/dusk  +/-  offset HH:MM:SS or HH:MM
    """

    @staticmethod
    def _extract_days(p_schedule_obj, p_now):
        """ Get the number of days until the next DayOfWeek in the schedule.

        DayOfWeek        mon=1, tue=2, wed=4, thu=8, fri=16, sat=32, sun=64
        weekday()  mon=0, tue=1, wed=2, thu=3, fri=4,  sat=5,  sun=6

        @param p_schedule_obj: is the schedule object we are working on
        @param p_now: is a datetime.datetime.now()
        @return: the number of days till the next DayOfWeek - 0..6, 10 if never
        """
        l_dow = p_schedule_obj.DayOfWeek
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
        l_sched_seconds = TimeField().parse_timefield(p_schedule_obj.Time, p_rise_set)
        l_sched_secs = l_dow_seconds + l_sched_seconds
        l_now_seconds = convert.datetime_to_seconds(p_now)
        l_seconds = l_sched_secs - l_now_seconds
        if l_seconds < 0:
            l_seconds += SECONDS_IN_DAY
        return l_seconds


class ScheduleExecution():

    def dispatch_one_schedule(self, p_pyhouse_obj, p_schedule_obj):
        """
        Send information to one device to execute a schedule.
        """
        l_topic = 'house/schedule/control'
        l_obj = p_schedule_obj
        p_pyhouse_obj._APIs.Core.MqttAPI.MqttPublish(l_topic, l_obj)
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
            LOG.info('Execute_one_schedule type = Irrigation')
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


class Utility():
    """
    """

    @staticmethod
    def _setup_components(p_pyhouse_obj):
        # p_pyhouse_obj.House.Schedules = {}
        pass

    @staticmethod
    def fetch_sunrise_set(p_pyhouse_obj):
        _l_topic = 'house/schedule/sunrise_set'
        l_riseset = p_pyhouse_obj.House.Location._RiseSet  # RiseSetData()
        LOG.info('Got Sunrise: {};   Sunset: {}'.format(l_riseset.SunRise, l_riseset.SunSet))
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
        l_runID = p_pyhouse_obj._Twisted.Reactor.callLater(p_delay, ScheduleExecution.execute_schedules_list, p_pyhouse_obj, p_list)
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

    def find_all_schedule_entries(self, p_pyhouse_obj, p_type=None):
        """ Find all the schedule entry using any of several criteria.
        Type (required)
        Mode (required)

        @return: a list schedule objects, None if error or no matches.
        """
        l_sched_list = []
        l_scheds = p_pyhouse_obj.House.Schedules
        for l_sched in  l_scheds.values():
            # print('sched', l_sched.Name)
            if l_sched.ScheduleType == p_type:
                # print('sched', l_sched.Name)
                l_sched_list.append(l_sched)
        if len(l_sched_list) == 0:
            return None
        return l_sched_list

    def find_schedule_entry(self, _p_pyhouse_obj, p_type=None):
        """ Find the schedule entry using any of several criteria.
        Type (required)
        Mode (required)

        @return: a schedule object, None if error
        """
        self.find_all_schedule_entries(p_type)
        return None


class Timers(object):
    """
    """

    def __init__(self, p_pyhouse_obj):
        self.m_pyhouse_obj = p_pyhouse_obj
        self.m_timers = {}
        self.m_count = 0

    def set_one(self, p_pyhouse_obj, p_delay, p_list):
        l_callback = ScheduleExecution.execute_schedules_list
        l_runID = p_pyhouse_obj._Twisted.Reactor.callLater(p_delay, l_callback, p_pyhouse_obj, p_list)
        l_datetime = datetime.datetime.fromtimestamp(l_runID.getTime())
        LOG.info('Scheduled {} after delay of {} - Time: {}'.format(p_list, p_delay, l_datetime))
        return l_runID


class Config:
    """Read in and possibly save the scheduling data.
    """
    m_pyhouse_obj = None
    m_schedule_altered = False

    def __init__(self, p_pyhouse_obj):
        self.m_pyhouse_obj = p_pyhouse_obj
        self.m_schedule_altered = False

    def _extract_entertainment_schedule(self):
        """
        """

    def _extract_irrigation_schedule(self):
        """
        """

    def _extract_light_schedule(self, p_config):
        """
        """
        l_obj = ScheduleLightInformation()
        for l_key, l_value in p_config.items():
            print('Light Sched Key:{}; Value:{}'.format(l_key, l_value))
            setattr(l_obj, l_key, l_value)
        return l_obj

    def _extract_thermostat_schedule(self):
        """
        """

    def _extract_one_schedule(self, p_config):
        """
        """
        l_required = ['Name', 'Occupancy', 'DOW', 'Time']
        l_obj = ScheduleInformation()
        for l_key, l_value in p_config.items():
            if l_key == 'Entertainment':
                pass
            elif l_key == 'Irrigation':
                pass
            elif l_key == 'Light':
                l_obj.Type = 'Light'
                l_ret = self._extract_light_schedule(l_value)
                l_obj.Light = l_ret
            elif l_key == 'Thermostat':
                pass
            else:
                setattr(l_obj, l_key, l_value)
        # Check for data missing from the config file.
        for l_key in [l_attr for l_attr in dir(l_obj) if not l_attr.startswith('_') and not callable(getattr(l_obj, l_attr))]:
            if getattr(l_obj, l_key) == None and l_key in l_required:
                LOG.warn('Schedule config file is missing an entry for "{}"'.format(l_key))
        return l_obj

    def _extract_all_schedules(self, p_config):
        """
        """
        l_scheds = {}
        for l_ix, l_value in enumerate(p_config):
            l_obj = self._extract_one_schedule(l_value)
            l_scheds.update({l_ix:l_obj})
            LOG.debug('Loaded Schedule {}'.format(l_obj.Name))
        self.m_pyhouse_obj.House.Schedules = l_scheds
        return l_scheds  # For testing.

    def LoadYamlConfig(self):
        """
        """
        self.m_pyhouse_obj.House.Schedules = None
        try:
            l_node = config_tools.Yaml(self.m_pyhouse_obj).read_yaml(CONFIG_FILE_NAME)
        except:
            return None
        try:
            l_yaml = l_node.Yaml['Schedules']
        except:
            LOG.warn('The schedules.yaml file does not start with "Schedules:"')
            return None
        l_scheds = self._extract_all_schedules(l_yaml)
        self.m_pyhouse_obj.House.Schedules = l_scheds
        return l_scheds  # for testing purposes

# ----------

    def SaveYamlConfig(self):
        """
        """


class API():

    m_pyhouse_obj = None
    m_config = None

    def __init__(self, p_pyhouse_obj):
        self.m_pyhouse_obj = p_pyhouse_obj
        self.m_config = Config(p_pyhouse_obj)
        LOG.info("Initialized.")

    def LoadConfig(self):
        """ Load the Schedule from the Config info.
        """
        self.m_pyhouse_obj.House.Schedules = {}
        l_schedules = self.m_config.LoadYamlConfig()
        self.m_pyhouse_obj.House.Schedules = l_schedules
        LOG.info('Loaded Schedules Config')
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

    def SaveConfig(self):
        """
        """
        self.m_config.SaveYamlConfig()
        LOG.info('Saved Schedules Config.')

    def RestartSchedule(self):
        """ Anything that alters the schedules should call this to cause the new schedules to take effect.
        """
        self.m_pyhouse_obj._Twisted.Reactor.callLater(INITIAL_DELAY, Utility.schedule_next_event, self.m_pyhouse_obj)

# ## END DBK
