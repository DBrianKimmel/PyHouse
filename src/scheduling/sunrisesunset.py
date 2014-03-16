#!/usr/bin/env  python

"""Calculate the suns location at local noon.
    Then calculate sunrise and sunset for the day.

    Heliocentric means that the Earth position is calculated with respect to the center of the sun.
    Geocentric means that the sun position is calculated with respect to the Earth center.
    Topocentric means that the sun position is calculated with respect to the observer local position at the Earth surface.
"""

# Import system type stuff
import datetime
import logging
import math
from math import pi

# Import PyMh files

g_debug = 0
g_logger = logging.getLogger('PyHouse.Sunrise     ')

RAD2DEG = 180.0 / pi
DEG2RAD = pi / 180.0
JDATE2000_9 = 2451545.0009  # convert Julian Date to Epoch 2000 (J2000)
JDATE2000 = 2451545  # convert Julian Date to Epoch 2000 (J2000)

Solar_Data = {}


class EarthParameters(object):
    """
    """

    def __init__(self):
        self.Date = None
        self.DayOfLocalMeanSolarNoon = None
        self.J2000 = None
        self.JulianCycle = 0.0
        self.JulianDate = 0.0
        self.JulianDayNumber = 0
        self.Latitude = 0.0
        self.Longitude = 0.0
        self.Sunrise = None
        self.Sunset = None
        self.TimeZone = 0.0

    def get_day_of_local_mean_solar_noon(self):
        return self.__DayOfLocalMeanSolarNoon

    def set_day_of_local_mean_solar_noon(self, value):
        self.__DayOfLocalMeanSolarNoon = value

    def get_julian_day_number(self):
        return self.__JulianDayNumber

    def set_julian_day_number(self, value):
        self.__JulianDayNumber = value

    def get_j_2000(self):
        return self.__J2000

    def set_j_2000(self, value):
        self.__J2000 = value

    def get_julian_date(self):
        return self.__JulianDate

    def set_julian_date(self, value):
        self.__JulianDate = value

    def get_latitude(self):
        return self.__Latitude

    def set_latitude(self, value):
        self.__Latitude = value

    def get_longitude(self):
        return self.__Longitude

    def set_longitude(self, value):
        self.__Longitude = value

    def get_sunrise(self):
        return self.__Sunrise

    def set_sunrise(self, value):
        self.__Sunrise = value

    def get_sunset(self):
        return self.__Sunset

    def set_sunset(self, value):
        self.__Sunset = value

    def get_time_zone(self):
        return self.__TimeZone

    def set_time_zone(self, value):
        self.__TimeZone = value

    def get_julian_cycle(self):
        return self.__JulianCycle

    def set_julian_cycle(self, value):
        self.__JulianCycle = value

    def get_date(self):
        return self.__Date

    def set_date(self, value):
        self.__Date = value

    Date = property(get_date, set_date, None, "The current date we are working with.")
    TimeZone = property(get_time_zone, set_time_zone, None, "TimeZone of observer in Minutes.")
    JulianDayNumber = property(get_julian_day_number, set_julian_day_number, None, "(integer) Number of days since Jan 1, 4713 BC.")
    JulianDate = property(get_julian_date, set_julian_date, None, "(real) Number of days since Noon UT Jan 1, 4713 BC.")
    J2000 = property(get_j_2000, set_j_2000, None, "Julian Date Epoch Jan 1, 2000.")
    DayOfLocalMeanSolarNoon = property(get_day_of_local_mean_solar_noon, set_day_of_local_mean_solar_noon, None, "J2000 + correction for observers Longitude")
    JulianCycle = property(get_julian_cycle, set_julian_cycle, None, "(floor float) Julian cycle since Jan 1st, 2000")
    Latitude = property(get_latitude, set_latitude, None, "Latitude of observer.")
    Longitude = property(get_longitude, set_longitude, None, "Longitude of observer.")
    Sunrise = property(get_sunrise, set_sunrise, None, "Time of Sunrise at observer's location.")
    Sunset = property(get_sunset, set_sunset, None, "Time of Sunset at observer's location.")

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
        self.MeanAnomaly = 0.0
        self.MeanLongitude = 0.0
        self.EclipticLongitude = 0.0
        self.EclipticLatitude = 0.0
        self.SolarHourAngle = 0.0
        self.SolarDeclination = 0.0
        self.SolarTransit = 0.0

    def get_mean_longitude(self):
        return self.__MeanLongitude

    def set_mean_longitude(self, value):
        self.__MeanLongitude = value

    def get_mean_anomaly(self):
        return self.__MeanAnomaly

    def set_mean_anomaly(self, value):
        self.__MeanAnomaly = value

    def get_solar_transit(self):
        return self.__SolarTransit

    def set_solar_transit(self, value):
        self.__SolarTransit = value

    MeanAnomaly = property(get_mean_anomaly, set_mean_anomaly, None, "MeanAnomaly's docstring")
    SolarTransit = property(get_solar_transit, set_solar_transit, None, "The hour angle for solar transit (or solar noon)")
    MeanLongitude = property(get_mean_longitude, set_mean_longitude, None, "The mean longitude of the Sun, corrected for the aberration of light (Ecliptic coord).")

class SSUtility(object):

    def _revolution(self, p_degrees):
        """
        This function reduces any angle to within the first revolution
        by subtracting or adding even multiples of 360.0 until the
        result is >= 0.0 and < 360.0

        Reduce angle to within 0..360 degrees
        """
        return (p_degrees - 360.0 * math.floor(p_degrees / 360.0))

    def _rev180(self, x):
        """Reduce angle to within +180..+180 degrees."""
        return (x - 360.0 * math.floor(x / 360.0 + 0.5))

    def _convert_to_time(self, p_hours):
        """Convert a time in hours (float) to a datetime.time object.

        @return: a datetime.time object containing the time.
        """
        if p_hours > 24.0:
            p_hours -= 24.0
        if p_hours < 0.0:
            p_hours += 24.0
        l_hours = int(p_hours)
        l_minutes = int(60.0 * (p_hours - l_hours))
        l_seconds = int(60 * (60.0 * (p_hours - l_hours) - l_minutes))
        l_time = datetime.time(l_hours, l_minutes, l_seconds)
        return l_time

    def _convert_julian_to_time(self, p_julian, p_timezone = False):
        """Convert julian fraction day to HMS.

        Remember that Julian here starts at noon so subtract 0.5 days

        @return: a datetime.time object
        """
        l_time = ((p_julian - 0.5) % 1.0) * 24.0
        if p_timezone:
            l_time += -4.0
        return self._convert_to_time(l_time)

class SunCalcs(SSUtility, EarthParameters, SolarParameters):
    """
    """
    earth_data = {}

    def _calc_mean_anomaly(self, p_jstar2K):
        """Calculate the mean anomaly.
        """
        l_ma = self._revolution(357.5291 + (0.98560028 * (p_jstar2K))) * DEG2RAD
        if g_debug >= 1:
            g_logger.debug("Calculating solar Mean Anomaly {0:}".format(l_ma * RAD2DEG))
        return l_ma

    def _calc_equation_of_center(self, p_ma):
        """Calc equation of center 'C'.
        """
        l_ec = (1.9148 * math.sin(p_ma) + 0.02000 * math.sin(2.0 * p_ma) + 0.0003 * math.sin(3.0 * p_ma)) * DEG2RAD
        if g_debug >= 1:
            g_logger.debug("C           Calculating solar Equation of Center {0:}".format(l_ec * RAD2DEG))
        return l_ec

    def _calc_ecliptic_longitude(self, p_ma, p_ec):
        """Calc ecliptic longitude 'lambda'.
        """
        l_lambda = self._revolution((p_ma * RAD2DEG) + 102.9372 + (p_ec * RAD2DEG) + 180.0) * DEG2RAD
        if g_debug >= 1:
            g_logger.debug("lambda      Calculating solar Ecliptic Longitude {0:}".format(l_lambda * RAD2DEG))
        return l_lambda

    def _calc_solar_transit(self, p_jstar, p_ma, p_lambda):
        """Calc solar transit.
        """
        l_transit = p_jstar + (0.0053 * math.sin(p_ma)) - (0.0069 * math.sin(2.0 * p_lambda))
        if g_debug >= 1:
            g_logger.debug("J* {0:}, 1:{1:}, 2:{2:}".format(p_jstar, 0.0053 * math.sin(p_ma), 0.0069 * math.sin(2.0 * p_lambda)))
            g_logger.debug("J_transit   Calculating solar transit {0:}  {1:} ".format(l_transit, self._convert_julian_to_time(l_transit, True)))
        return l_transit

    def _calc_declination_of_sun(self, p_lambda):
        """Calc Declination of the Sun - delta
        """
        l_delta = math.asin(math.sin(p_lambda) * math.sin(23.45 * DEG2RAD))
        if g_debug >= 1:
            g_logger.debug("delta       Calculating solar declination {0:}".format(l_delta * RAD2DEG))
        return l_delta

    def _calc_hour_angle(self, p_lat, p_delta):
        """Calc Hour Angle - H
        """
        l_x = (math.sin(-0.83 * DEG2RAD) - (math.sin(p_lat) * math.sin(p_delta))) / (math.cos(p_lat) * math.cos(p_delta))
        l_ha = math.acos(l_x)
        if g_debug >= 1:
            g_logger.debug("H           Calculating solar hour angle {0:}".format(l_ha * RAD2DEG))
        return l_ha

    def _calc_ecliptic_latitude(self):
        """Calc Ecliptic Latitude - always 0.0
        """
        l_el = 0.0
        return l_el


    def _recursive_calcs(self, p_jstar, p_ma, p_ec, p_lambda, p_transit):
        l_ma = self._calc_mean_anomaly(p_transit)
        l_ec = self._calc_equation_of_center(p_ma)
        l_lambda = self._calc_ecliptic_longitude(p_ma, p_ec)
        l_transit = self._calc_solar_transit(p_jstar, p_ma, p_lambda)
        return l_ma, l_ec, l_lambda, l_transit

    def _calcJulianDates(self, p_earth):
        """From Wikipedia.

        Julian date (JD) system of time measurement for scientific use by the astronomy community,
        presenting the interval of time in days and fractions of a day since Noon January 1, 4713 BC Greenwich.

        For higher precision, we will use the days since Jan 1, 2000
        """
        l_year = p_earth.Date.year
        l_month = p_earth.Date.month
        l_day = p_earth.Date.day
        l_a = (14 - l_month) // 12
        l_y = l_year + 4800 - l_a
        l_m = l_month + (12 * l_a) - 3
        p_earth.JulianDayNumber = (l_day + (((153 * l_m) + 2) // 5) + (365 * l_y) + (l_y // 4) - (l_y // 100) + (l_y // 400) - 32045)  # integer
        p_earth.JulianDate = p_earth.JulianDayNumber + 0.5  # Real - Noon
        l_nstar = p_earth.JulianDayNumber - JDATE2000_9 + (p_earth.Longitude / 360.0)
        p_earth.N = l_n = math.floor(l_nstar + 0.5)
        p_earth.JulianCycle = math.floor(p_earth.JulianDate - JDATE2000_9 + (p_earth.Longitude / 360.0) + 0.5)
        if g_debug >= 1:
            g_logger.debug("Calculating julian date:{0:}, JulianDayNumber:{1:}".format(p_earth.JulianDate, p_earth.JulianDayNumber))
            g_logger.debug("n* n-round  Calculating 2000 epoch dates     {0:} {1:} ".format(l_nstar, l_n))

    def _calcSolarNoonParams(self, p_earth, p_sun):
        """
        """
        l_e_long = p_earth.Longitude
        # Approximate Solar Noon
        l_n_star = p_earth.JulianDayNumber - JDATE2000_9 + (l_e_long / 360.0)
        _l_n = math.floor(l_n_star + 0.5)
        p_earth.J2000 = p_earth.JulianDate - JDATE2000_9
        l_domsn = p_earth.J2000 - (l_e_long / 360.0) - 0.5
        p_earth.DayOfLocalMeanSolarNoon = l_domsn
        l_j_star = JDATE2000_9 - (l_e_long / 360.0) + p_earth.JulianCycle
        l_j_star2k = l_j_star - JDATE2000
        if g_debug >= 1:
            g_logger.debug("n*          Calculating the JDN(2000) of Local Mean Solar Noon {0:} at Longitude {1:}".format(l_domsn, l_e_long))
            g_logger.debug("n           Calculating the JulianCycle(2000) of Local Mean Solar Noon {0:}".format(p_earth.JulianCycle))
            g_logger.debug("J* J*2K     Calculating Approximate solar noon {0:} ({1:}) - {2:}".format(l_j_star, l_j_star2k, self._convert_julian_to_time(l_j_star2k, True)))
        l_ma = self._calc_mean_anomaly(l_j_star2k)
        l_ec = self._calc_equation_of_center(l_ma)
        l_lambda = self._calc_ecliptic_longitude(l_ma, l_ec)
        l_transit = self._calc_solar_transit(l_j_star2k, l_ma, l_lambda)
        l_ma, l_ec, l_lambda, l_transit = self._recursive_calcs(l_j_star2k, l_ma, l_ec, l_lambda, l_transit)
        l_ma, l_ec, l_lambda, l_transit = self._recursive_calcs(l_j_star2k, l_ma, l_ec, l_lambda, l_transit)
        l_ma, l_ec, l_lambda, l_transit = self._recursive_calcs(l_j_star2k, l_ma, l_ec, l_lambda, l_transit)
        p_sun.MeanAnomaly = l_ma
        p_sun.EquationCenter = l_ec
        p_sun.EclipticLongitude = l_lambda
        p_sun.SolarTransit = l_transit
        l_delta = self._calc_declination_of_sun(l_lambda)
        l_ha = self._calc_hour_angle(p_earth.Latitude * DEG2RAD, l_delta)
        l_el = self._calc_ecliptic_latitude()
        p_sun.SolarDeclination = l_delta
        p_sun.SolarHourAngle = l_ha
        p_sun.EclipticLatitude = l_el

    def _calcSolarTransit(self, p_earth, p_sun):
        """
        """
        l_transit = p_sun.SolarTransit
        l_j_starstar = ((-p_earth.Longitude + p_sun.SolarHourAngle * RAD2DEG) / 360.0) + p_earth.N + 0.0009
        l_set = l_j_starstar + (0.0053 * math.sin(p_sun.MeanAnomaly)) - (0.0069 * math.sin(2.0 * p_sun.EclipticLongitude))
        l_rise = l_transit - (l_set - l_transit)
        p_earth.Sunrise = l_rise
        p_earth.Sunset = l_set
        if g_debug >= 1:
            g_logger.debug("J**         Calculating using hour angle {0:}".format(l_j_starstar))
            g_logger.debug(" Sunrise {0:}  {1:}".format(l_rise, self._convert_julian_to_time(l_rise, True)))
            g_logger.debug(" Transit {0:}  {1:}".format(l_transit, self._convert_julian_to_time(l_transit, True)))
            g_logger.debug(" Sunset  {0:}  {1:}".format(l_set, self._convert_julian_to_time(l_set, True)))

    def calc_sunrise_sunset(self, p_earth_data, p_solar_data):
        """Trigger all calculations.
        Calculate the coordinates of the Sun in the ecliptic coordinate system.
        Convert to the equatorial coordinate system.
        Convert to the horizontal coordinate system for the observer's local circumstances.
        """
        self._calcJulianDates(p_earth_data)
        self._calcSolarNoonParams(p_earth_data, p_solar_data)
        self._calcSolarTransit(p_earth_data, p_solar_data)


class SSAPI(SunCalcs):

    def get_sunrise(self):
        """Returns a sunrise time as a datetime.time object.
        """
        return self._convert_julian_to_time(self.earth_data.Sunrise, True)

    def get_sunset(self):
        """Returns a sunset time as a datetime.time object.
        """
        return self._convert_julian_to_time(self.earth_data.Sunset, True)

    def load_location(self, p_house_obj, p_earth_data, p_solar_data):
        """Extract from house information"""
        self.earth_data = p_earth_data
        self.solar_data = p_solar_data
        p_earth_data.Latitude = p_house_obj.Location.Latitude
        p_earth_data.Longitude = p_house_obj.Location.Longitude
        p_earth_data.TimeZone = p_house_obj.Location.TimeZone
        p_earth_data.Name = p_house_obj.Name


class API(SSAPI):

    def __init__(self, p_house_obj):
        self.m_house_obj = p_house_obj
        self.earth_data = EarthParameters()
        self.solar_data = SolarParameters()

    def Start(self, p_house_obj, p_date = datetime.date.today()):
        SSAPI().load_location(p_house_obj, self.earth_data, self.solar_data)
        self.earth_data.Date = p_date
        SSAPI().calc_sunrise_sunset(self.earth_data, self.solar_data)

    def Stop(self):
        pass

# ## END
