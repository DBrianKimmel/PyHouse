"""
-*- test-case-name: PyHouse.src.Modules.Scheduling.test.test_sunrisesunset -*-

@name: PyHouse/src/Modules/Scheduling/sunrisesunset.py
@author: D. Brian Kimmel
@contact: D.BrianKimmel@gmail.com
@copyright: 2011-2014 by D. Brian Kimmel
@note: Created on Mar 6, 2011
@license: MIT License
@summary: Calculate the suns location at local noon, then calculate sunrise and sunset for the day.

    In order to avoid loss of precision, all calculations are based on 2000 year epoch called J2K.

    All angles are in radians internally.

    Heliocentric means that the Earth position is calculated with respect to the center of the sun.
    Geocentric means that the sun position is calculated with respect to the Earth center.
    Topocentric means that the sun position is calculated with respect to the observer local position at the Earth surface.


TODO:Round sunset and sunrise to the nearest minute.
"""

# Import system type stuff
import datetime
import dateutil.parser as dparser
from dateutil.tz import *
import math
from math import pi

# Import PyMh files
from Modules.Computer import logging_pyh as Logger
# from Modules.Utilities.tools import PrettyPrintAny

g_debug = 0
LOG = Logger.getLogger('PyHouse.Sunrise        ')

RAD2DEG = 180.0 / pi
DEG2RAD = pi / 180.0

JDATE2000_9 = 2451545.0009  # convert Julian Date to Epoch 2000 (J2K)
JDATE2000 = 2451545  # convert Julian Date to Epoch 2000 (J2K)

ZERO = datetime.timedelta(0)
HOUR = datetime.timedelta(hours = 1)
HOUR_4 = datetime.timedelta(hours = -4)
HOUR_5 = datetime.timedelta(hours = -5)



class JulianParameters(object):
    """
    Day is integer number of days since Jan 1, 4713 BCE GMT
    Date is floating number of days since Noon, Jan 1 4713 BCE GMT

    """

    def __init__(self):
        self.GregorianDate = None
        # Julian - Jan 1 4713 BCE
        self.JulianDate = None  # (float) Number of days since Noon UT Jan 1, 4713 BC.
        self.JulianDayNumber = None  # (integer) Number of days since Jan 1, 4713 BC.
        # J2000 - Jan 1 2000 CE
        self.J2K = None  # Julian Date since Noon Jan 1, 2000.
        self.J2KCycle = None  # (floor float) Julian cycle since Jan 1st, 2000
        self.J2KTransit = None


class EarthParameters(object):
    """
    """

    def __init__(self):
        self.Latitude = 0.0
        self.Longitude = 0.0
        self.Sunrise = None
        self.Sunset = None
        self.TimeZoneName = None
        self.TimeZoneOffset = None
        self.DaylightSavingsTime = None


class SolarParameters(object):
    """The ecliptic coordinate system is a celestial coordinate system that uses the ecliptic for its fundamental plane.
        The ecliptic is the path that the sun appears to follow across the celestial sphere over the course of a year.
        It is also the intersection of the Earth's orbital plane and the celestial sphere.
        The latitudinal angle is called the ecliptic latitude or celestial latitude, measured positive towards the north.
        The longitudinal angle is called the ecliptic longitude or celestial longitude, measured eastwards from 0 to 360.
        Like right ascension in the equatorial coordinate system, 0deg ecliptic longitude is pointing towards the Sun from the Earth at the Northern hemisphere vernal equinox.
        This choice makes the coordinates of the fixed stars subject to shifts due to the precession, so that always a reference epoch should be specified.
        Usually epoch J2K.0 is taken, but the instantaneous equinox of the day (called the epoch of date) is possible too.
    """
    def __init__(self):
        self.EclipticLatitude = 0.0
        self.EclipticLongitude = 0.0
        self.EquationCenter = 0.0
        self.MeanAnomaly = 0.0
        self.MeanLongitude = 0.0  # The mean longitude of the Sun, corrected for the aberration of light (Ecliptic coord).
        self.SolarDeclination = 0.0
        self.SolarHourAngle = 0.0
        self.SolarTransit = 0.0  # The hour angle for solar transit (or solar noon)


class LocationTz(datetime.tzinfo):
    """
    The timezone in effect at our location.
    """

    def utcoffset(self, _dt):
        return datetime.timedelta(hours = -5)

    def tzname(self, _dt):
        return "USA/Eastern"

    def dst(self, _dt):
        return datetime.timedelta(hours = -5)


class Util(object):
    """
    StaticMethods to convert/normalize data
    """

    @staticmethod
    def _revolution(p_degrees):
        """
        This function reduces any angle to within the first revolution
        by subtracting or adding even multiples of 360.0 until the
        result is >= 0.0 and < 360.0

        Reduce angle to within 0..360 degrees
        """
        return (p_degrees - 360.0 * math.floor(p_degrees / 360.0))

    @staticmethod
    def _normalize_hours(p_hours):
        """
        Put hours in the range of 0..24
        """
        while p_hours > 24.0:
            p_hours -= 24.0
        while p_hours < 0.0:
            p_hours += 24.0
        return p_hours

    @staticmethod
    def _convert_to_datetime(p_hours):
        """
        Convert a time in hours (float) to a datetime.datetime object.
        Round to the nearest whole second.

        @return: a datetime.time object containing the time.
        """
        l_days = int(p_hours) // 24
        l_seconds = int((p_hours - (l_days * 24)) * 3600 + .5)
        l_time = datetime.timedelta(l_days, l_seconds)
        return l_time


class JDate(object):
    """
    Calculate the various Julian parameters for the given date.
    A loss of precision occurs when the actual Julian dates are uses so we
    usually work with a modified Julian date obtained by using the year 2000 as a starting point.
    This reduces the Julain date by 2451545 days.
    """

    @staticmethod
    def _is_jan_feb(p_date):
        """
        Returns 1 if month is Jan or Feb, 0 otherwise (NOT True/False but arithmetic value)
        """
        return (14 - p_date.month) // 12

    @staticmethod
    def _julian_day(p_julian):
        """
        The (int) number of days since Jan 1, 4713 BCE
        """
        l_date = p_julian.GregorianDate
        l_year = l_date.year + 4800 - JDate._is_jan_feb(l_date)
        l_month = l_date.month + (12 * JDate._is_jan_feb(l_date)) - 3
        l_day = (l_date.day + \
                 (((153 * l_month) + 2) // 5) + \
                 (365 * l_year) + \
                 (l_year // 4) - \
                 (l_year // 100) + \
                 (l_year // 400) - \
                 (87 * 365) - \
                 290)  # integer
        return l_day

    @staticmethod
    def _julian_date(p_julian):
        """
        The astronomical julian date starts at Noon, Jan 1st 4713 BC
        This is a floating point number 1/2 day less than the julian day
        """
        return p_julian.JulianDayNumber - 0.5

    @staticmethod
    def _j2k(p_julian):
        return p_julian.JulianDate - JDATE2000  # - 0.0009

    @staticmethod
    def _j2k_cycle(p_julian, p_earth):
        """
        The Julian cycle since Jan 1st, 2000.
        Symbol 'n'
        """
        l_date = p_julian.JulianDate
        l_long = p_earth.Longitude / 360.0
        l_cycle = l_date - JDATE2000 - .0009 - l_long
        return round(l_cycle)

    @staticmethod
    def _j2k_transit(p_julian, p_earth):
        """
        The Julian cycle since Jan 1st, 2000.
        Symbol 'n'
        """
        l_cycle = p_julian.J2KCycle
        l_long = p_earth.Longitude / 360.0
        l_transit = l_cycle - l_long + 0.0009
        return l_transit

    @staticmethod
    def _convert_julian_to_datetime(p_julian):
        """
        Convert days since Noon Jan 1 4000  to YMD-HMS.

        Remember that Julian here starts at noon so subtract 0.5 days

        @return: a datetime.date object
        """
        l_jd = int(p_julian - 0.5 + 730121)  # Days from 0 AD to 2000 AD
        l_date = datetime.date.fromordinal(l_jd)
        # print('Date = {}'.format(l_date))
        l_tm = ((p_julian - 0.5) % 1.0)
        l_hr = int(l_tm * 24)
        l_min = int(l_tm * 1440 % 60)
        l_sec = int(l_tm * 86400 % 60)
        l_time = datetime.time(l_hr, l_min, l_sec, 0, tzinfo = LocationTz())
        l_dt = datetime.datetime.combine(l_date, l_time)
        l_dt = l_dt + l_time.utcoffset()
        # print('DT {}'.format(l_dt))
        return l_dt

    @staticmethod
    def calculate_all_julian_dates(p_gregorian_date, p_earth):
        """
        Calculate once per calendar day.
        the .0009 is (I Think!) accumulated errors since 4713 BC.
        That amounts to 77.76 seconds of correction.
        """
        l_julian = JulianParameters()
        l_julian.GregorianDate = p_gregorian_date
        l_julian.JulianDayNumber = JDate._julian_day(l_julian)
        l_julian.JulianDate = JDate._julian_date(l_julian)
        l_julian.J2K = JDate._j2k(l_julian)
        l_julian.J2KCycle = JDate._j2k_cycle(l_julian, p_earth)
        l_julian.J2KTransit = JDate._j2k_transit(l_julian, p_earth)
        return l_julian


class SunCalcs(object):
    """
    Using the Ecliptic Coordinate system.

    n = the number of days since solar Noon on Jan 1, 2000
    L = 280.460Deg + 0.9856474Deg * n  (Mean Longitude)
    """

    @staticmethod
    def _calc_ecliptic_latitude():
        """
        Calculate the Ecliptic Latitude - always 0.0
        Symbol Beta
        """
        l_elatitude = 0.0
        return l_elatitude

    @staticmethod
    def _calc_mean_anomaly(p_julian):
        """
        The position that the planet would have relative to its perihelion if the orbit of the planet
         were a circle is called the mean anomaly.
        Calculate the mean anomaly.
        Symbol g

        l_j_star2k = JDATE2000_9 - (l_e_long / 360.0) + p_julian.J2KCycle - JDATE2000
        l_j_star2k = p_julian.J2KCycle + JDATE2000_9 - JDATE2000 - (l_e_long / 360.0)

        """
        l_c1 = p_julian.J2KTransit
        l_mean_anomaly = Util._revolution(357.5291 + (0.98560028 * (l_c1))) * DEG2RAD
        # print('CalcMeanAnomaly = {} >> {}'.format(l_c1, l_mean_anomaly * RAD2DEG))
        return l_mean_anomaly

    @staticmethod
    def _calc_equation_of_center(p_solar):
        """
        The orbits of the planets are not perfect circles but rather ellipses, so the speed of the planet
         in its orbit varies, and therefore the apparent speed of the Sun along the ecliptic also varies
          throughout the planet's year.

        The true anomaly is the angular distance of the planet from the perihelion of
         the planet, as seen from the Sun.
        For a circular orbit, the mean anomaly and the true anomaly are the same.
        The difference between the true anomaly and the mean anomaly is called the Equation of Center,
         written here as C:

        Calculate the equation of center.
        Symbol C.
        """
        l_mean_anomaly = p_solar.MeanAnomaly
        l_equation_of_center = 1.91480 * math.sin(l_mean_anomaly) + \
               0.02000 * math.sin(2.0 * l_mean_anomaly) + \
               0.00030 * math.sin(3.0 * l_mean_anomaly)
        l_equation_of_center = l_equation_of_center * DEG2RAD
        return l_equation_of_center

    @staticmethod
    def _calc_ecliptic_longitude(p_solar):
        """
        Calculate the Ecliptic Longitude.
        Symbol 'lambda'.
        This is the position of the earth in its orbit around the sun with 0 degrees being the vernal equinox.
        """
        l_mean_anomaly = p_solar.MeanAnomaly
        l_equation_of_center = p_solar.EquationCenter
        l_lambda = Util._revolution((l_mean_anomaly * RAD2DEG) + \
                    102.9372 + (l_equation_of_center * RAD2DEG) + 180.0) * DEG2RAD
        return l_lambda

    @staticmethod
    def _calc_solar_transit(p_julian, p_solar):
        """
        Calculate solar transit.
        """
        l_jstar = p_julian.J2KTransit
        l_mean_anomaly = p_solar.MeanAnomaly
        l_lambda = p_solar.EclipticLongitude
        l_c1 = 0.0053 * math.sin(l_mean_anomaly)
        l_c2 = 0.0069 * math.sin(2.0 * l_lambda)
        l_transit = l_jstar + l_c1 - l_c2
        # print l_c1, l_c2
        return l_transit

    @staticmethod
    def _calc_declination_of_sun(p_solar):
        """
        Calculate the Declination of the Sun.
        Symbol delta
        """
        l_lambda = p_solar.EclipticLongitude
        l_delta = math.asin(math.sin(l_lambda) * math.sin(23.45 * DEG2RAD))
        return l_delta

    @staticmethod
    def _calc_hour_angle(p_earth, p_solar):
        """
        Calculate the solar Hour Angle.
        Symbol H
        """
        l_latitude = p_earth.Latitude
        l_declination = p_solar.SolarDeclination
        l_x = (math.sin(-0.83 * DEG2RAD) - \
                (math.sin(l_latitude) * math.sin(l_declination))) / \
                (math.cos(l_latitude) * math.cos(l_declination))
        l_ha = math.acos(l_x)
        return l_ha


class SunriseSet(SunCalcs):
    """
    """

    def _recursive_calcs(self, p_julian, p_solar):
        p_solar.MeanAnomaly = self._calc_mean_anomaly(p_julian)
        p_solar.EquationCenter = self._calc_equation_of_center(p_solar)
        p_solar.EclipticLongitude = self._calc_ecliptic_longitude(p_solar)
        p_solar.SolarTransit = self._calc_solar_transit(p_julian, p_solar)
        p_julian.J2KTransit = p_solar.SolarTransit
        return p_solar

    def _recursive_loop(self, p_julian, p_solar, p_ix):
        for _l_ix in range(p_ix):
            l_test = p_solar.MeanAnomaly
            p_solar = self._recursive_calcs(p_julian, p_solar)
            # print('iteration of recursive {}'.format(_l_ix))
            # PrettyPrintAny(p_solar, 'After Recursive')
            if p_solar.MeanAnomaly == l_test:
                return p_solar
        l_msg = 'Ran out of iterations without converging.'
        # print('{}'.format(l_msg))
        LOG.info(l_msg)
        return p_solar

    def calcSolarNoonParams(self, p_earth, p_julian):
        """
        """
        l_sun = SolarParameters()
        l_sun.EclipticLatitude = self._calc_ecliptic_latitude()
        l_sun.MeanAnomaly = self._calc_mean_anomaly(p_julian)
        l_sun.EquationCenter = self._calc_equation_of_center(l_sun)
        l_sun.EclipticLongitude = self._calc_ecliptic_longitude(l_sun)
        l_sun.SolarTransit = self._calc_solar_transit(p_julian, l_sun)
        l_sun = self._recursive_calcs(p_julian, l_sun)
        l_sun = self._recursive_calcs(p_julian, l_sun)
        l_sun = self._recursive_calcs(p_julian, l_sun)
        l_sun.SolarDeclination = self._calc_declination_of_sun(l_sun)
        l_sun.SolarHourAngle = self._calc_hour_angle(p_earth, l_sun)
        self._calcSolarTransit(p_earth, p_julian, l_sun)
        return l_sun

    def _calcSolarTransit(self, p_earth, p_julian, p_sun):
        """
        """
        l_transit = p_sun.SolarTransit
        l_N = p_julian.J2KCycle
        l_j_starstar = ((-p_earth.Longitude + p_sun.SolarHourAngle * RAD2DEG) / 360.0) + l_N + 0.0009
        l_set = l_j_starstar + (0.0053 * math.sin(p_sun.MeanAnomaly)) - (0.0069 * math.sin(2.0 * p_sun.EclipticLongitude))
        l_rise = l_transit - (l_set - l_transit)
        # print('xxxx', l_rise, l_set, l_transit)
        p_earth.Sunrise = l_rise
        p_earth.Sunset = l_set
        p_sun.Sunrise = l_rise
        p_sun.Sunset = l_set


class SSAPI(object):

    m_earth_data = {}

    def get_sunrise_datetime(self):
        """Returns a sunrise time as a datetime.time object.
        """
        l_rise = JDate._convert_julian_to_datetime(self.m_earth_data.Sunrise)
        return l_rise

    def get_sunset_datetime(self):
        """Returns a sunset time as a datetime.time object.
        """
        l_set = JDate._convert_julian_to_datetime(self.m_earth_data.Sunset)
        return l_set


JDATE2000_9 = 2451545.0009  # convert Julian Date to Epoch 2000 (J2K)

class Utility(SSAPI, SunriseSet):
    """
    """

    def _calculate_solar_params(self):
        l_solar_data = SolarParameters()
        l_solar_data.EclipticLatitude = self._calc_ecliptic_latitude()
        return l_solar_data

    def _get_zone_time(self, p_field):
        l_dt = dparser.parse(p_field, fuzzy = True)
        l_time = datetime.time(l_dt.hour, l_dt.minute, l_dt.second)
        return l_time

    def _load_location(self, p_pyhouse_obj, p_gregorian_date):
        l_earth_data = EarthParameters()
        l_earth_data.Latitude = p_pyhouse_obj.House.RefOBJs.Location.Latitude
        l_earth_data.Longitude = p_pyhouse_obj.House.RefOBJs.Location.Longitude
        l_earth_data.TimeZoneName = p_pyhouse_obj.House.RefOBJs.Location.TimeZoneName
        self._get_tz_params(l_earth_data, p_gregorian_date)
        return l_earth_data

    def _get_tz_params(self, p_earth_data, p_gregorian_date):
        l_tz_name = p_earth_data.TimeZoneName
        l_zone = gettz(l_tz_name)
        l = p_gregorian_date
        l_dst = datetime.datetime(l.year, l.month, l.day, 12, 0, 0).dst > 0
        p_earth_data._IsDaylightSavingsTime = l_dst
        p_earth_data._TimeZoneOffset = None  # l_zone._ttinfo_before
        # if l_dst:
        #    p_earth_data._TimeZoneOffset = l_zone._dstoffset
        l_ret = tzlocal()
        return p_earth_data, l_zone



class API(Utility):

    def Start(self, p_pyhouse_obj, p_gregorian_date = datetime.date.today()):
        self.m_pyhouse_obj = p_pyhouse_obj
        self.m_earth_data = self._load_location(p_pyhouse_obj, p_gregorian_date)
        self.m_julian_data = JDate.calculate_all_julian_dates(p_gregorian_date, self.m_earth_data)
        self.m_solar_data = self._calculate_solar_params()
        self.m_solar_data = self.calcSolarNoonParams(self.m_earth_data, self.m_julian_data)
        p_pyhouse_obj.House.RefOBJs.Location._Sunrise = self.m_solar_data.Sunrise
        p_pyhouse_obj.House.RefOBJs.Location._Sunset = self.m_solar_data.Sunset
        LOG.info('Started.')

    def Stop(self):
        pass

def moon_phase(mDay, mMonth, mYear):
    r = mYear % 100
    r %= 19
    if r > 9:
        r -= 19
    r = ((r * 11) % 30) + mMonth + mDay
    if mMonth < 3:
        r += 2
    s = 4 if mYear < 2000 else 8.3
    r -= s
    r = (math.floor(r + 0.5) % 30)
    return r + 30 if r < 0 else r

# ## END
