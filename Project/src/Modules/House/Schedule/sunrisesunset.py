"""
@name:      Modules/House/Schedules/sunrisesunset.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2011-2020 by D. Brian Kimmel
@note:      Created on Mar 6, 2011
@license:   MIT License
@summary:   Calculate the suns location at local noon, then calculate sunrise and sunset for the day.

"""

__updated__ = '2020-02-04'

# Import system type stuff
import datetime
import astral
import pytz

# Import PyMh files
from Modules.House.Schedule import RiseSetInformation
# from Modules.House import LocationInformation

# from Modules.Core.Utilities.debug_tools import PrettyFormatAny

from Modules.Core import logging_pyh as Logger
LOG = Logger.getLogger('PyHouse.Sunrise        ')


class Api:

    def __init__(self, p_pyhouse_obj):
        self.m_tz = pytz.timezone('America/New_York')
        self.m_pyhouse_obj = p_pyhouse_obj
        LOG.info('Initialized')

    def _get_seconds_to_recalc(self, p_time=None):
        """ Time (in seconds) till next recalc (10:00 AM)
        """
        if p_time is None:
            p_time = datetime.datetime.now(self.m_tz)
        l_now = p_time
        l_ten = datetime.datetime(l_now.year, l_now.month, l_now.day, 10, 0, 0, tzinfo=self.m_tz)
        l_togo = (l_ten - l_now).total_seconds()
        if l_togo < 0:
            l_togo += (24 * 60 * 60)
        LOG.info('Will recalculate sunrise/sunset in {} Seconds'.format(l_togo))
        return l_togo

    def _get_solar_times(self, p_date=datetime.date.today()):
        """ Calculate Sunrise / Sunset
        Store result in ==> pyhouse_obj.House.Location._RiseSet
        @param p_date: is the datetime.date that we want sunrise and sunset for
        """
        l_astral = astral.Location(info=(
                self.m_pyhouse_obj.House.Name,
                self.m_pyhouse_obj.House.Location.Country,
                self.m_pyhouse_obj.House.Location.Latitude,
                self.m_pyhouse_obj.House.Location.Longitude,
                self.m_pyhouse_obj.House.Location.TimeZone,
                self.m_pyhouse_obj.House.Location.Elevation
                )
            )
        l_astral.solar_depression = "civil"
        if (isinstance(p_date, datetime.datetime)):
            l_date = p_date.date()  # convert datetime.datetime to datetime.date
        else:
            l_date = p_date
        l_sun = l_astral.sun(date=l_date, local=True)
        l_ret = RiseSetInformation()
        l_ret.Dawn = l_sun['dawn']
        l_ret.SunRise = l_sun['sunrise']
        l_ret.Noon = l_sun['noon']
        l_ret.SunSet = l_sun['sunset']
        l_ret.Dusk = l_sun['dusk']
        self.m_pyhouse_obj.House.Location._RiseSet = l_ret
        LOG.info('Sunrise/Sunset Calculation Updated')
        return l_ret

    def Start(self):
        """
        @param p_location: is the location used for calcs
        """
        LOG.info('Starting')
        self._get_solar_times()
        l_delay = self._get_seconds_to_recalc()
        self.m_pyhouse_obj._Twisted.Reactor.callLater(l_delay, self._get_solar_times, self.m_pyhouse_obj)

# ## END
