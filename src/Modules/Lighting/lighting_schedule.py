"""
@name:      PyHouse/src/Modules/Lighting/lighting_schedule.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2014-2015 by D. Brian Kimmel
@license:   MIT License
@note:      Created on Nov 11, 2014
@Summary:

"""

# Import system type stuff

# Import PyMh files
from Modules.Computer import logging_pyh as Logger


LOG = Logger.getLogger('PyHouse.LightSched  ')
SECONDS_IN_WEEK = 604800  # 7 * 24 * 60 * 60


class LightingSchedule(object):
    """
    """

    def _find_event(self, p_schedule):
        if not p_schedule.Active:
            return None
        if not p_schedule.ScheduleType == 'LightingEvent':
            return None
        return p_schedule


    def find_next_scheduled_event(self, p_pyhouse_obj):
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
        l_seconds_to_delay = SECONDS_IN_WEEK
        l_schedule_list = []

        for l_key, l_schedule_obj in p_pyhouse_obj.House.Schedules.iteritems():
            l_event = self._find_event(l_schedule_obj)
            if l_event == None:
                continue
            l_time_sch = self._extract_time_of_day(l_schedule_obj, l_riseset)
            # now see if this is 1) part of a chain -or- 2) an earlier schedule
            l_diff = self._find_diff(l_time_sch, l_now_daytime)
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




# ## END DBK
