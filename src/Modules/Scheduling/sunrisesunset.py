"""
-*- test-case-name: PyHouse.src.Modules.scheduling.test.test_sunrisesunset -*-

@name: PyHouse/src/Modules/scheduling/sunrisesunset.py
@author: D. Brian Kimmel
@contact: <d.briankimmel@gmail.com
@copyright: 2011-2014 by D. Brian Kimmel
@note: Created on Mar 6, 2011
@license: MIT License
@summary: Calculate the suns location at local noon, then calculate sunrise and sunset for the day.

    Heliocentric means that the Earth position is calculated with respect to the center of the sun.
    Geocentric means that the sun position is calculated with respect to the Earth center.
    Topocentric means that the sun position is calculated with respect to the observer local position at the Earth surface.
"""

# Import system type stuff
import datetime
import math
from math import pi

# Import PyMh files
from Modules.Computer import logging_pyh as Logger
from Modules.Utilities.tools import GetPyhouse

g_debug = 0
LOG = Logger.getLogger('PyHouse.Sunrise     ')

RAD2DEG = 180.0 / pi
DEG2RAD = pi / 180.0
JDATE2000_9 = 2451545.0009  # convert Julian Date to Epoch 2000 (J2000)
JDATE2000 = 2451545  # convert Julian Date to Epoch 2000 (J2000)


class JulianParameters(object):

    def __init__(self):
        self.DayLocalMeanSolarNoon = None  # J2000 + correction for observers Longitude
        self.DaysNoon2K = 0  # the number of days (positive or negative) since Greenwich noon, Terrestrial Time, on 1 January 2000 (J2000.0).
        self.J2000 = None  # Julian Date Epoch Jan 1, 2000.
        self.JulianCycle = 0.0  # (floor float) Julian cycle since Jan 1st, 2000
        self.JulianDate = 0.0  # (real) Number of days since Noon UT Jan 1, 4713 BC.
        self.JulianDayNumber = 0  # (integer) Number of days since Jan 1, 4713 BC.
        self.GregorianDate = None


class EarthParameters(object):
    """
    """

    def __init__(self):
        self.Latitude = 0.0
        self.Longitude = 0.0
        self.Sunrise = None
        self.Sunset = None
        self.TimeZone = 0.0
        self.N = 0


class SolarParameters(object):
    """The ecliptic coordinate system is a celestial coordinate system that uses the ecliptic for its fundamental plane.
        The ecliptic is the path that the sun appears to follow across the celestial sphere over the course of a year.
        It is also the intersection of the Earth's orbital plane and the celestial sphere.
        The latitudinal angle is called the ecliptic latitude or celestial latitude, measured positive towards the north.
        The longitudinal angle is called the ecliptic longitude or celestial longitude, measured eastwards from 0 to 360.
        Like right ascension in the equatorial coordinate system, 0deg ecliptic longitude is pointing towards the Sun from the Earth at the Northern hemisphere vernal equinox.
        This choice makes the coordinates of the fixed stars subject to shifts due to the precession, so that always a reference epoch should be specified.
        Usually epoch J2000.0 is taken, but the instantaneous equinox of the day (called the epoch of date) is possible too.
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
    def _convert_to_time(p_hours):
        """Convert a time in hours (float) to a datetime.time object.

        @return: a datetime.time object containing the time.
        """
        p_hours = Util._normalize_hours(p_hours)
        l_hours = int(p_hours)
        l_minutes = int(60.0 * (p_hours - l_hours))
        l_seconds = int(60 * (60.0 * (p_hours - l_hours) - l_minutes))
        l_time = datetime.time(l_hours, l_minutes, l_seconds)
        return l_time


class JulianCalcs(object):
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

    def _calculate_julian_day(self, p_date):
        """
        days since Jan 1, 4713 BC

        32045 = (87 * 365) + 290
        """
        l_year = p_date.year + 4800 - JulianCalcs._is_jan_feb(p_date)
        l_month = p_date.month + (12 * JulianCalcs._is_jan_feb(p_date)) - 3
        l_day = (p_date.day + \
                 (((153 * l_month) + 2) // 5) + \
                 (365 * l_year) + \
                 (l_year // 4) - \
                 (l_year // 100) + \
                 (l_year // 400) - \
                 (87 * 365) - \
                 290)  # integer
        return l_day

    def _calculate_julian_date(self, p_date):
        """
        The astronomical julian date starts at Noon, Jan 1st 4713 BC
        This is a floating point number 1/2 day less than the julian day
        """
        l_day = self._calculate_julian_day(p_date)
        return l_day - 0.5

    def _convert_julian_to_time(self, p_julian, p_timezone = False):
        """Convert julian fraction day to HMS.

        Remember that Julian here starts at noon so subtract 0.5 days

        @return: a datetime.time object
        """
        l_time = ((p_julian - 0.5) % 1.0) * 24.0
        if p_timezone:
            l_time += -4.0
        return Util._convert_to_time(l_time)

    def _calculate_all_julian_dates(self, p_date, p_location):
        """
        Calculate once per calendar day.
        the .0009 is (I Think!) accumulated errors since 4713 BC.
        That amounts to 77.76 seconds of correction.
        """
        l_julian = JulianParameters()
        l_julian.GregorianDate = p_date
        l_julian.JulianDayNumber = self._calculate_julian_day(p_date)
        l_julian.JulianDate = self._calculate_julian_date(p_date)
        l_julian.J2000 = l_julian.JulianDate - JDATE2000_9
        l_julian.JulianCycle = math.floor(l_julian.J2000 + (p_location.Longitude / 360.0) + 0.5)
        l_julian.DayLocalMeanSolarNoon = l_julian.J2000 - (p_location.Longitude / 360.0) - 0.5
        # l_julian.N = math.floor(l_julian.J2000 + (p_location.Longitude / 360.0) + 0.5)
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
    def _calc_mean_anomaly(p_jstar2K):
        """
        Calculate the mean anomaly.
        Symbol g
        """
        l_mean_anomaly = Util._revolution(357.5291 + (0.98560028 * (p_jstar2K))) * DEG2RAD
        return l_mean_anomaly

    @staticmethod
    def _calc_equation_of_center(p_mean_anomaly):
        """
        Calculate the equation of center.
        Symbol C.
        """
        l_equation_of_center = 1.91480 * math.sin(p_mean_anomaly) + \
               0.02000 * math.sin(2.0 * p_mean_anomaly) + \
               0.00030 * math.sin(3.0 * p_mean_anomaly)
        l_equation_of_center = l_equation_of_center * DEG2RAD
        return l_equation_of_center

    @staticmethod
    def _calc_ecliptic_longitude(p_mean_anomaly, p_equation_of_center):
        """
        Calculate the Ecliptic Longitude.
        Symbol 'lambda'.
        This is the position of the earth in its orbit around the sun with 0 degrees being the vernal equinox.
        """
        l_lambda = Util._revolution((p_mean_anomaly * RAD2DEG) + \
                    102.9372 + (p_equation_of_center * RAD2DEG) + 180.0) * DEG2RAD
        return l_lambda

    @staticmethod
    def _calc_solar_transit(p_jstar, p_mean_anomaly, p_lambda):
        """
        Calculate solar transit.
        """
        l_transit = p_jstar + (0.0053 * math.sin(p_mean_anomaly)) - (0.0069 * math.sin(2.0 * p_lambda))
        return l_transit

    @staticmethod
    def _calc_declination_of_sun(p_lambda):
        """
        Calculate the Declination of the Sun.
        Symbol delta
        """
        l_delta = math.asin(math.sin(p_lambda) * math.sin(23.45 * DEG2RAD))
        return l_delta

    @staticmethod
    def _calc_hour_angle(p_earth_lat, p_solar_declination):
        """
        Calculate the solar Hour Angle.
        Symbol H
        """
        l_x = (math.sin(-0.83 * DEG2RAD) - (math.sin(p_earth_lat) * math.sin(p_solar_declination))) / \
                (math.cos(p_earth_lat) * math.cos(p_solar_declination))
        l_ha = math.acos(l_x)
        return l_ha


class SunriseSet(SunCalcs):
    """
    """

    def _recursive_calcs(self, p_jstar, p_mean_anomaly, p_equation_of_center, p_lambda, p_transit):
        l_mean_anomaly = self._calc_mean_anomaly(p_transit)
        l_equation_of_center = self._calc_equation_of_center(p_mean_anomaly)
        l_lambda = self._calc_ecliptic_longitude(p_mean_anomaly, p_equation_of_center)
        l_transit = self._calc_solar_transit(p_jstar, p_mean_anomaly, p_lambda)
        return l_mean_anomaly, l_equation_of_center, l_lambda, l_transit

    def _calcSolarNoonParams(self, p_earth, p_sun, p_julian):
        """
        """
        l_e_long = p_earth.Longitude
        l_j_star2k = JDATE2000_9 - (l_e_long / 360.0) + p_julian.JulianCycle - JDATE2000
        # print('JStar2000 = {0:}  Long {1:}'.format(l_j_star2k, l_e_long / 360.0))
        l_mean_anomaly = self._calc_mean_anomaly(l_j_star2k)
        l_equation_of_center = self._calc_equation_of_center(l_mean_anomaly)
        l_lambda = self._calc_ecliptic_longitude(l_mean_anomaly, l_equation_of_center)
        l_transit = self._calc_solar_transit(l_j_star2k, l_mean_anomaly, l_lambda)
        l_mean_anomaly, l_equation_of_center, l_lambda, l_transit = self._recursive_calcs(l_j_star2k, l_mean_anomaly, l_equation_of_center, l_lambda, l_transit)
        l_mean_anomaly, l_equation_of_center, l_lambda, l_transit = self._recursive_calcs(l_j_star2k, l_mean_anomaly, l_equation_of_center, l_lambda, l_transit)
        l_mean_anomaly, l_equation_of_center, l_lambda, l_transit = self._recursive_calcs(l_j_star2k, l_mean_anomaly, l_equation_of_center, l_lambda, l_transit)
        p_sun.MeanAnomaly = l_mean_anomaly
        p_sun.EquationCenter = l_equation_of_center
        p_sun.EclipticLongitude = l_lambda
        p_sun.SolarTransit = l_transit
        p_sun.SolarDeclination = self._calc_declination_of_sun(l_lambda)
        p_sun.SolarHourAngle = self._calc_hour_angle(p_earth.Latitude * DEG2RAD, p_sun.SolarDeclination)
        p_sun.EclipticLatitude = self._calc_ecliptic_latitude()
        return p_sun

    def _calcSolarTransit(self, p_earth, p_sun):
        """
        """
        l_transit = p_sun.SolarTransit
        l_j_starstar = ((-p_earth.Longitude + p_sun.SolarHourAngle * RAD2DEG) / 360.0) + p_earth.N + 0.0009
        l_set = l_j_starstar + (0.0053 * math.sin(p_sun.MeanAnomaly)) - (0.0069 * math.sin(2.0 * p_sun.EclipticLongitude))
        l_rise = l_transit - (l_set - l_transit)
        p_earth.Sunrise = l_rise
        p_earth.Sunset = l_set
        # print("J**         Calculating using hour angle {0:}".format(l_j_starstar))
        # print(" Sunrise {0:}  {1:}".format(l_rise, self._convert_julian_to_time(l_rise, True)))
        # print(" Transit {0:}  {1:}".format(l_transit, self._convert_julian_to_time(l_transit, True)))
        # print(" Sunset  {0:}  {1:}".format(l_set, self._convert_julian_to_time(l_set, True)))

    def calc_sunrise_sunset(self, p_earth_data, p_solar_data):
        """Trigger all calculations.
        Calculate the coordinates of the Sun in the ecliptic coordinate system.
        Convert to the equatorial coordinate system.
        Convert to the horizontal coordinate system for the observer's local circumstances.
        """
        # self._calcJulianDates(p_earth_data)
        self._calcSolarNoonParams(p_earth_data, p_solar_data)
        self._calcSolarTransit(p_earth_data, p_solar_data)


class SSAPI(JulianCalcs):

    m_earth_data = {}

    def get_sunrise(self):
        """Returns a sunrise time as a datetime.time object.
        """
        return self._convert_julian_to_time(self.m_earth_data.Sunrise, True)

    def get_sunset(self):
        """Returns a sunset time as a datetime.time object.
        """
        return self._convert_julian_to_time(self.m_earth_data.Sunset, True)


JDATE2000_9 = 2451545.0009  # convert Julian Date to Epoch 2000 (J2000)

class Utility(SSAPI):
    """
    """

    def _calculate_solar_params(self):
        l_solar_data = SolarParameters()
        l_solar_data.EclipticLatitude = self._calc_ecliptic_latitude()
        return l_solar_data

    def _load_location(self, p_pyhouse_obj):
        l_earth_data = EarthParameters()
        l_earth_data.Latitude = GetPyhouse(p_pyhouse_obj).Location().Latitude
        # l_earth_data.Latitude = p_pyhouse_obj.House.OBJs.Location.Latitude
        l_earth_data.Longitude = p_pyhouse_obj.House.OBJs.Location.Longitude
        l_earth_data.TimeZone = p_pyhouse_obj.House.OBJs.Location.TimeZone
        return l_earth_data


class API(Utility):

    def Start(self, p_pyhouse_obj, p_date = datetime.date.today()):
        self.m_pyhouse_obj = p_pyhouse_obj
        self.m_earth_data = self._load_location(p_pyhouse_obj)
        self.m_julian_data = self._calculate_all_julian_dates(p_date, self.m_earth_data)
        self.m_solar_data = self._calculate_solar_params()
        self._calcSolarNoonParams(self.m_earth_data, self.m_solar_data, self.m_julian_data)
        self._calcSolarTransit(self.m_earth_data, self.m_solar_data)

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
