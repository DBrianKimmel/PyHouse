"""
@name:      Modules/Housing/Schedules/sunrisesunset.py
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

__updated__ = '2019-09-09'

# Import system type stuff
import datetime
import astral
import pytz

# Import PyMh files
from Modules.Core.data_objects import RiseSetData
from Modules.Core import logging_pyh as Logger
# from Modules.Core.Utilities.debug_tools import PrettyFormatAny

LOG = Logger.getLogger('PyHouse.Sunrise        ')

CALC_TIME = 11 * 60 * 60  # 10:00:00 AM


class Times:
    """
    """

    def __init__(self):
        self.LastUpdate = None


class LocatTzinfo(datetime.tzinfo):
    """
    """

    def __init__(self):
        pass

    def utcoffset(self, dt):
        pass

    def dst(self, dt):
        pass

    def tzname(self, dt):
        pass


class Utility(object):

    def __init__(self):
        self.m_tz = pytz.timezone('America/New_York')

    def get_seconds_to_recalc(self, p_time=None):
        """
        """
        if p_time is None:
            p_time = datetime.datetime.now(self.m_tz)
        l_now = p_time
        l_ten = datetime.datetime(l_now.year, l_now.month, l_now.day, 10, 0, 0, tzinfo=self.m_tz)
        l_togo = (l_now - l_ten).total_seconds()
        # print('Now    ', l_now)
        # print('Recalc ', l_ten)
        # print('ToGo   ', l_togo)
        if l_togo < 0:
            l_togo += (24 * 60 * 60)
            pass
        return l_togo

    def _till_next(self, p_time=datetime.datetime.today()):
        """
        Get the number of seconds until we calculate sunrise again

        @param p_time:
        @return: the number of seconds to go.
        """
        l_recalc = datetime.timedelta(days=1, seconds=(12 * 60 + 12)).total_seconds()
        l_current = p_time
        l_seconds = (((l_current.hour * 60) + l_current.minute) * 60 + l_current.second)
        # print('xxx', l_recalc, l_seconds)
        l_delay = datetime.timedelta(seconds=(l_recalc - l_seconds)).total_seconds()
        return l_delay

    def calc_solar_times(self, p_pyhouse_obj, p_date=datetime.date.today()):
        """
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
        LOG.info('Sunrise/Sunset Calculation')
        return l_ret


class API(Utility):

    def __init__(self, p_pyhouse_obj):
        self.m_pyhouse_obj = p_pyhouse_obj
        self.m_tz = pytz.timezone('America/New_York')

    def Start(self):
        self.calc_solar_times(self.m_pyhouse_obj)
        self._loop()

    def Stop(self):
        pass

    def _loop(self):
        l_delay = self._till_next()
        self.m_pyhouse_obj._Twisted.Reactor.callLater(l_delay, self.calc_solar_times, self.m_pyhouse_obj)

# ## END
