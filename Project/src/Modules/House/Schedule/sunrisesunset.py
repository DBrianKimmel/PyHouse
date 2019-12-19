"""
@name:      Modules/House/Schedules/sunrisesunset.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2011-2019 by D. Brian Kimmel
@note:      Created on Mar 6, 2011
@license:   MIT License
@summary:   Calculate the suns location at local noon, then calculate sunrise and sunset for the day.

    In order to avoid loss of precision, all calculations are based on 2000 year epoch called J2K.

    All angles are in radians internally.

    Heliocentric means that the Earth position is calculated with respect to the center of the sun.
    Geocentric means that the sun position is calculated with respect to the Earth center.
    Topocentric means that the sun position is calculated with respect to the observer local position at the Earth surface.

"""

__updated__ = '2019-12-19'

# Import system type stuff
import datetime
import astral
import pytz

# Import PyMh files
from Modules.Core.data_objects import RiseSetData
from Modules.Core import logging_pyh as Logger
# from Modules.Core.Utilities.debug_tools import PrettyFormatAny

LOG = Logger.getLogger('PyHouse.Sunrise        ')


class lightingUtilitySun:

    def __init__(self):
        self.m_tz = pytz.timezone('America/New_York')

    def get_seconds_to_recalc(self, p_time=None):
        """ Time (in seconds) till next recalc (10:00 AM)
        """
        if p_time is None:
            p_time = datetime.datetime.now(self.m_tz)
        l_now = p_time
        l_ten = datetime.datetime(l_now.year, l_now.month, l_now.day, 10, 0, 0, tzinfo=self.m_tz)
        l_togo = (l_ten - l_now).total_seconds()
        # print('Now    ', l_now)
        # print('Recalc ', l_ten)
        # print('ToGo   ', l_togo)
        if l_togo < 0:
            l_togo += (24 * 60 * 60)
        LOG.info('Will recalculate sunrise/sunset in {} Seconds'.format(l_togo))
        return l_togo

    def calc_solar_times(self, p_pyhouse_obj, p_date=datetime.date.today()):
        """ Calculate Sunrise / Sunset
        Store result in ==> pyhouse_obj.House.Location._RiseSet
        @param p_date: is the datetime.date that we want sunrise and sunset for
        """
        l_a = astral.Location(info=(
                p_pyhouse_obj.House.Name,
                p_pyhouse_obj.House.Location.Country,
                p_pyhouse_obj.House.Location.Latitude,
                p_pyhouse_obj.House.Location.Longitude,
                p_pyhouse_obj.House.Location.TimeZone,
                p_pyhouse_obj.House.Location.Elevation
                )
            )
        l_a.solar_depression = "civil"
        if (isinstance(p_date, datetime.datetime)):
            l_date = p_date.date()  # convert datetime.datetime to datetime.date
        else:
            l_date = p_date
        l_sun = l_a.sun(date=l_date, local=True)
        l_ret = RiseSetData()
        l_ret.Dawn = l_sun['dawn']
        l_ret.SunRise = l_sun['sunrise']
        l_ret.Noon = l_sun['noon']
        l_ret.SunSet = l_sun['sunset']
        l_ret.Dusk = l_sun['dusk']
        p_pyhouse_obj.House.Location._RiseSet = l_ret
        LOG.info('Sunrise/Sunset Calculation Updated')
        return l_ret


class Api(lightingUtilitySun):

    def __init__(self, p_pyhouse_obj):
        self.m_pyhouse_obj = p_pyhouse_obj
        self.m_tz = pytz.timezone('America/New_York')

    def Start(self):
        self.calc_solar_times(self.m_pyhouse_obj)
        l_delay = self.get_seconds_to_recalc()
        self.m_pyhouse_obj._Twisted.Reactor.callLater(l_delay, self.calc_solar_times, self.m_pyhouse_obj)

    def Stop(self):
        pass

# ## END
