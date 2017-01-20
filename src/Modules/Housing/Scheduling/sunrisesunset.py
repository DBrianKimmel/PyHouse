"""
-*- test-case-name: PyHouse.src.Modules.Scheduling.test.test_sunrisesunset -*-

@name:      PyHouse/src/Modules/Scheduling/sunrisesunset.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2011-2017 by D. Brian Kimmel
@note:      Created on Mar 6, 2011
@license:   MIT License
@summary:   Calculate the suns location at local noon, then calculate sunrise and sunset for the day.

    In order to avoid loss of precision, all calculations are based on 2000 year epoch called J2K.

    All angles are in radians internally.

    Heliocentric means that the Earth position is calculated with respect to the center of the sun.
    Geocentric means that the sun position is calculated with respect to the Earth center.
    Topocentric means that the sun position is calculated with respect to the observer local position at the Earth surface.

"""

__updated__ = '2016-07-16'

# Import system type stuff
import datetime
import astral

# Import PyMh files
from Modules.Core.data_objects import RiseSetData
from Modules.Computer import logging_pyh as Logger
# from Modules.Core.Utilities.debug_tools import PrettyFormatAny

LOG = Logger.getLogger('PyHouse.Sunrise        ')


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


class Util(object):

    @staticmethod
    def _till_next(p_time=datetime.datetime.today()):
        """
        Get the number of seconds until we calculate sunrise again
        @return: the numbere of seconds till 0:12:12
        """
        l_recalc = datetime.timedelta(days=1, seconds=(12 * 60 + 12)).total_seconds()
        l_current = p_time
        l_seconds = (((l_current.hour * 60) + l_current.minute) * 60 + l_current.second)
        # print('xxx', l_recalc, l_seconds)
        l_delay = datetime.timedelta(seconds=(l_recalc - l_seconds)).total_seconds()
        return l_delay

    @staticmethod
    def calc_solar_times(p_pyhouse_obj, p_date=datetime.date.today()):
        """
        @param p_date: is the datetime.date that we want sunrise and sunset for
        """
        l_a = astral.Location(info=(
                p_pyhouse_obj.House.Name,
                p_pyhouse_obj.House.Location.Region,
                p_pyhouse_obj.House.Location.Latitude,
                p_pyhouse_obj.House.Location.Longitude,
                p_pyhouse_obj.House.Location.TimeZoneName,
                p_pyhouse_obj.House.Location.Elevation
                )
            )
        l_a.solar_depression = "civil"
        if (isinstance(p_date, datetime.datetime)):
            l_date = p_date.date()  # convert datetime.datetime to datetime.date
        else:
            l_date = p_date
        # print(PrettyFormatAny.form('{}'.format(l_a), 'AA'))
        l_sun = l_a.sun(date=l_date, local=True)
        l_ret = RiseSetData()
        l_ret.Dawn = l_sun['dawn']
        l_ret.SunRise = l_sun['sunrise']
        l_ret.Noon = l_sun['noon']
        l_ret.SunSet = l_sun['sunset']
        l_ret.Dusk = l_sun['dusk']
        p_pyhouse_obj.House.Location.RiseSet = l_ret
        LOG.info('Sunrise/Sunset Calculation')
        return l_ret


class API(object):

    def __init__(self, p_pyhouse_obj):
        self.m_pyhouse_obj = p_pyhouse_obj

    def Start(self):
        Util.calc_solar_times(self.m_pyhouse_obj)
        self._loop()

    def Stop(self):
        pass

    def _loop(self):
        l_delay = Util._till_next()
        self.m_pyhouse_obj.Twisted.Reactor.callLater(l_delay, Util.calc_solar_times, self.m_pyhouse_obj)

# ## END
