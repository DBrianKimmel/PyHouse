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
import house as house

RAD2DEG = 180.0 / pi
DEG2RAD = pi / 180.0
JDATE2000_9 = 2451545.0009  # convert Julian Date to Epoch 2000 (J2000)
JDATE2000 = 2451545  # convert Julian Date to Epoch 2000 (J2000)

Earth_Data = {}
Solar_Data = {}
g_debug = 9
g_logger = None


class SunriseMathd(object):
    """
    """

    m_date = None
    m_timezone = 0.0

    def acosd(self, x):
        """Returns the arc cos in degrees"""
        return math.acos(x) * RAD2DEG

    def atan2d(self, y, x):
        """Returns the atan2 in degrees"""
        return math.atan2(y, x) * RAD2DEG

    def radians2dms(self, pRadians):
        """Convert Radians to dms - mostly for printing"""
        mins, sec = divmod(pRadians * 3600 * RAD2DEG, 60)
        deg, mins = divmod(mins, 60)
        return deg, mins, sec

    def radians2hms(self, pRadians):
        mins, sec = divmod(pRadians * 3600 / 15 * RAD2DEG, 60)
        hour, mins = divmod(mins, 60)
        return hour, mins, sec

    def formatRadians2dms(self, pRadians):
        d, m, s = self.radians2dms(pRadians)
        return " {0:} Deg, {1:} Min, {2:} Sec ".format(int(d), int(m), s)

    def formatRadians2hms(self, pRadians):
        h, m, s = self.radians2hms(pRadians)
        return " {0:} Hour, {1:} Min, {2:} Sec ".format(int(h), int(m), s)

class EarthParameters(object):
    """
    """

    def __init__(self):
        self.Date = None
        self.DayOfLocalMeanSolarNoon = None
        self.DST = False
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
    def get_dst(self):
        return self.__DST
    def get_j_2000(self):
        return self.__J2000
    def get_julian_date(self):
        return self.__JulianDate
    def get_latitude(self):
        return self.__Latitude
    def get_longitude(self):
        return self.__Longitude
    def get_sunrise(self):
        return self.__Sunrise
    def get_sunset(self):
        return self.__Sunset
    def get_time_zone(self):
        return self.__TimeZone
    def set_dst(self, value):
        self.__DST = value
    def get_julian_cycle(self):
        return self.__JulianCycle
    def set_julian_cycle(self, value):
        self.__JulianCycle = value
    def set_j_2000(self, value):
        self.__J2000 = value
    def set_julian_date(self, value):
        self.__JulianDate = value
    def set_latitude(self, value):
        self.__Latitude = value
    def set_longitude(self, value):
        self.__Longitude = value
    def set_sunrise(self, value):
        self.__Sunrise = value
    def set_sunset(self, value):
        self.__Sunset = value
    def set_time_zone(self, value):
        self.__TimeZone = value
    def get_date(self):
        return self.__Date
    def set_date(self, value):
        self.__Date = value

    Date = property(get_date, set_date, None, "The current date we are working with.")
    TimeZone = property(get_time_zone, set_time_zone, None, "TimeZone of observer in Minutes.")
    DST = property(get_dst, set_dst, None, "Correction for Daylight Saving Time in observers timezone")

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
        # Ecliptic
        self.MeanAnomaly = 0.0
        self.MeanLongitude = 0.0
        self.EclipticLongitude = 0.0
        self.EclipticLatitude = 0.0
        self.SolarDistance = 0.0
        # Equitorial
        self.ObliquityOfEcliptic = 0.0
        self.SolarHourAngle = 0.0
        self.SolarDeclination = 0.0
        #
        self.ArgumentOfPerihelion = 0.0
        self.EccentricAnomaly = 0.0
        self.Eccentricity = 0.0
        self.HourAngle = 0.0
        self.SolarLatitude = 0.0
        self.SolarLongitude = .0
        self.SolarNoonHrs = 0.0
        self.SolarRadius = 0.0
        self.SolarTransit = 0.0
        self.TrueAnomaly = 0.0

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
        # print "convert-to-time ", p_hours
        if p_hours > 24.0: p_hours -= 24.0
        if p_hours < 0.0: p_hours += 24.0
        l_hours = int(p_hours)
        l_minutes = int(60.0 * (p_hours - l_hours))
        l_seconds = int(60 * (60.0 * (p_hours - l_hours) - l_minutes))
        l_time = datetime.time(l_hours, l_minutes, l_seconds)
        return l_time

    def _convert_julian_to_time(self, p_julian, p_timezone = False):
        """Convert julian fraction day to HMS.

        @return: a datetime.time object
        """
        l_time = (p_julian % 1.0) * 24.0
        if p_timezone:
            l_time += -4.0
        return self._convert_to_time(l_time)

class SunCalcs(SSUtility, SunriseMathd, EarthParameters, SolarParameters):
    """
    """

    def _calcJulianDates(self, p_earth):
        """From Wikipedia.
        Julian date (JD) system of time measurement for scientific use by the astronomy community,
        presenting the interval of time in days and fractions of a day since January 1, 4713 BC Greenwich Noon.
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
        if g_debug > 2: print("            Calculating julian date:{0:}, JulianDayNumber:{1:}".format(p_earth.JulianDate, p_earth.JulianDayNumber))
        if g_debug > 2: print("n* n-round  Calculating     {0:} {1:} ".format(l_nstar, l_n))



    def _calc_ma(self, p_jstar):
        """Calculate the mean anomaly.
        """
        # print "ma - J* ", p_jstar
        l_ma = self._revolution(357.5291 + (0.98560028 * (p_jstar - JDATE2000))) * DEG2RAD
        if g_debug > 2: print("M           Calculating solar Mean Anomaly {0:}".format(l_ma * RAD2DEG))
        return l_ma

    def _calc_ec(self, p_ma):
        """Calc equation of center 'C'.
        """
        # print "EC - M ", p_ma * RAD2DEG
        l_ec = (1.9148 * math.sin(p_ma) + 0.02000 * math.sin(2.0 * p_ma) + 0.0003 * math.sin(3.0 * p_ma)) * DEG2RAD
        if g_debug > 2: print("C           Calculating solar Equation of Center {0:}".format(l_ec * RAD2DEG))
        return l_ec

    def _calc_lambda(self, p_ma, p_ec):
        """Calc ecliptic longitude 'lambda'.
        """
        # print "Lambda - ", p_ma * RAD2DEG, p_ec * RAD2DEG
        l_lambda = self._revolution((p_ma * RAD2DEG) + 102.9372 + (p_ec * RAD2DEG) + 180.0) * DEG2RAD
        if g_debug > 2: print("lambda      Calculating solar Ecliptic Longitude {0:}".format(l_lambda * RAD2DEG))
        return l_lambda

    def _calc_transit(self, p_jstar, p_ma, p_lambda):
        """Calc solar transit.
        """
        # print "p_jstar, p_ma, p_lambda ", p_jstar, p_ma * RAD2DEG, p_lambda * RAD2DEG
        l_transit = p_jstar + (0.0053 * math.sin(p_ma)) - (0.0069 * math.sin(2.0 * p_lambda))
        if g_debug > 2: print("J_transit   Calculating solar transit {0:}  {1:} ".format(l_transit, self._convert_julian_to_time(l_transit + 0.5, True)))
        return l_transit

    def _recursive_calcs(self, p_ma, p_ec, p_lambda, p_transit):
        print "J* ", p_transit
        l_ma = self._calc_ma(p_transit)
        l_ec = self._calc_ec(p_ma)
        l_lambda = self._calc_lambda(p_ma, p_ec)
        l_transit = self._calc_transit(p_transit, p_ma, p_lambda)
        if g_debug > 2: print
        return l_ma, l_ec, l_lambda, l_transit

    def _calcSolarNoonParams(self, p_earth, p_sun):
        """
        """
        # Approximate Solar Noon
        l_nstar = p_earth.JulianDayNumber - JDATE2000_9 + (p_earth.Longitude / 360.0)
        l_n = math.floor(l_nstar + 0.5)
        p_earth.J2000 = p_earth.JulianDate - JDATE2000_9
        # p_earth.JulianCycle = math.floor(p_earth.JulianDate - JDATE2000_9 + (p_earth.Longitude / 360.0) + 0.5)
        p_earth.DayOfLocalMeanSolarNoon = l_domsn = p_earth.J2000 - (p_earth.Longitude / 360.0) - 0.5
        l_jstar = JDATE2000_9 - (p_earth.Longitude / 360.0) + p_earth.JulianCycle
        l_jstar2k = l_jstar - JDATE2000
        if g_debug > 2: print("n*          Calculating the JDN(2000) of Local Mean Solar Noon {0:} at Longitude {1:}".format(p_earth.DayOfLocalMeanSolarNoon, p_earth.Longitude))
        if g_debug > 2: print("n           Calculating the JulianCycle(2000) of Local Mean Solar Noon {0:}".format(p_earth.JulianCycle))
        if g_debug > 2: print("J*          Calculating Approximate solar noon {0:} ({1:}) - {2:}".format(l_jstar, l_jstar2k, self._convert_julian_to_time(l_jstar + 0.5, True)))
        #
        l_transit = l_jstar
        l_ma = self._calc_ma(l_transit)
        l_ec = self._calc_ec(l_ma)
        l_lambda = self._calc_lambda(l_ma, l_ec)
        l_transit = self._calc_transit(l_transit, l_ma, l_lambda)
        print "----"
        # l_ma, l_ec, l_lambda, l_transit = self._recursive_calcs(l_ma, l_ec, l_lambda, l_transit)
        # l_ma, l_ec, l_lambda, l_transit = self._recursive_calcs(l_ma, l_ec, l_lambda, l_transit)
        # l_ma, l_ec, l_lambda, l_transit = self._recursive_calcs(l_ma, l_ec, l_lambda, l_transit)
        # l_ma, l_ec, l_lambda, l_transit = self._recursive_calcs(l_ma, l_ec, l_lambda, l_transit)
        # l_ma, l_ec, l_lambda, l_transit = self._recursive_calcs(l_ma, l_ec, l_lambda, l_transit)
        p_sun.MeanAnomaly = l_ma
        p_sun.EquationCenter = l_ec
        p_sun.EclipticLongitude = l_lambda
        p_sun.SolarTransit = l_transit


        p_sun.EclipticLatitude = 0.0  # very, very close at all times.
        if g_debug > 2: print("beta        Calculating solar Ecliptic Latitude {0:}".format(p_sun.EclipticLatitude * RAD2DEG))
        # Declination of the Sun
        p_sun.SolarDeclination = l_delta = math.asin(math.sin(p_sun.EclipticLongitude) * math.sin(23.45 * DEG2RAD))
        if g_debug > 2: print("delta       Calculating solar declination {0:}".format(p_sun.SolarDeclination * RAD2DEG))
        # Hour Angle
        l_x = (math.sin(p_earth.Latitude) * math.sin(l_delta)) / (math.cos(p_earth.Latitude) * math.cos(l_delta))
        p_sun.SolarHourAngle = math.acos(math.sin(-0.83 * DEG2RAD) - l_x)
        if g_debug > 2: print("H           Calculating solar hour angle {0:}".format(p_sun.SolarHourAngle * RAD2DEG))


        # These progress each day
        p_sun.Eccentricity = 0.016709 - (1.151E-9 * l_domsn)
        p_sun.ArgumentOfPerihelion = (282.9404 + 4.70935E-5 * l_domsn) * DEG2RAD
        if g_debug > 2: print("            Calculating solar Eccentricity {0:}".format(p_sun.Eccentricity * RAD2DEG))
        if g_debug > 2: print("            Calculating solar Argument of Perihelion {0:}".format(p_sun.ArgumentOfPerihelion * RAD2DEG))

    def _calcEclipticCoords(self, p_earth, p_sun):
        l_domsn = p_earth.DayOfLocalMeanSolarNoon
        p_sun.MeanLongitude = _l_ml = self._revolution(280.460 + (0.9856474 * l_domsn)) * DEG2RAD
        # p_sun.EclipticLongitude = l_ml + (1.915 * DEG2RAD * math.sin(l_ma)) + (0.020 * DEG2RAD * math.sin(2.0 * l_ma))
        # p_sun.SolarDistance = l_sd = 1.00014 - (0.01671 * math.cos(l_ma)) - (.00014 * math.cos(2.0 * l_ma))
        # p_sun.SolarRadius = 0.2666 / l_sd
        # g_logger.debug("J*2000  Using local solar noon {0:} Lon:{1:}, J2000:{2:}".format(l_domsn, p_earth.Longitude, p_earth.J2000))
        # g_logger.debug("L       Calculating solar Mean Longitude {0:}".format(p_sun.MeanLongitude * RAD2DEG))
        # g_logger.debug("R       Calculating solar Solar Distance {0:}".format(p_sun.SolarDistance))

    def _calcEquitorialCoords(self, p_earth, p_sun):
        l_domsn = p_earth.J2000 + 0.0009 - (p_earth.Longitude / 360.0) - 0.5
        p_sun.ObliquityOfEcliptic = (23.4393 - (3.563E-7 * l_domsn)) * DEG2RAD
        if g_debug > 2: print("            Calculating solar Obliquity of Ecliptic {0:}".format(p_sun.ObliquityOfEcliptic * RAD2DEG))

    def _calcSolarTransit(self, p_earth, p_sun):
        """
        """
        print "J** ", p_earth.Longitude, p_sun.SolarHourAngle * RAD2DEG, p_earth.J2000
        l_jstarstar = JDATE2000_9 + ((-p_earth.Longitude + p_sun.SolarHourAngle * RAD2DEG) / 360.0) + p_earth.N
        l_set = l_jstarstar + 0.0053 * math.sin(p_sun.MeanAnomaly) - 0.0069 * math.sin(2.0 * p_sun.EclipticLongitude)
        l_rise = p_sun.SolarTransit - (l_set - p_sun.SolarTransit)
        if g_debug > 2: print("J**         Calculating using hour angle {0:}".format(l_jstarstar))
        if g_debug > 2: print("J_set 1     Calculating sunset {0:}  {1:}".format(l_set, self._convert_julian_to_time(l_set + 0.5, True)))
        if g_debug > 2: print("J_rise 1    Calculating sunrise {0:}  {1:}".format(l_set, self._convert_julian_to_time(l_rise + 0.5, True)))

    def _calcSunRiseSet(self, p_earth, p_sun):
        """
        """
        p_earth.Sunset = JDATE2000_9 + ((p_sun.SolarHourAngle - p_earth.Longitude) / 360.0) * RAD2DEG + p_earth.JulianCycle + 0.0053 * math.sin(p_sun.MeanAnomaly) - 0.0069 * math.sin(2 * p_sun.EclipticLongitude)
        if g_debug > 2: print("J_set  2    Sunset {0:}   {1:}".format(p_earth.Sunset, self._convert_julian_to_time(p_earth.Sunset, False)))
        p_earth.Sunrise = p_sun.SolarTransit - (p_earth.Sunset - p_sun.SolarTransit)
        if g_debug > 2: print("J_rise      Sunrise {0:}   {1:}".format(p_earth.Sunrise, self._convert_julian_to_time(p_earth.Sunrise, False)))

    def calc_sunrise_sunset(self):
        """Trigger all calculations.
        Calculate the coordinates of the Sun in the ecliptic coordinate system.
        Convert to the equatorial coordinate system.
        Convert to the horizontal coordinate system for the observer's local circumstances.
        """
        self._calcJulianDates(Earth_Data[0])
        self._calcSolarNoonParams(Earth_Data[0], Solar_Data[0])
        self._calcEclipticCoords(Earth_Data[0], Solar_Data[0])
        self._calcEquitorialCoords(Earth_Data[0], Solar_Data[0])
        self._calcSolarTransit(Earth_Data[0], Solar_Data[0])
        self._calcSunRiseSet(Earth_Data[0], Solar_Data[0])
        g_logger.info("Calculating sunrise/sunset now. Rise={0:}, Set={1:}".format(Earth_Data[0].Sunrise, Earth_Data[0].Sunset))


class SSAPI(SunCalcs):

    def get_sunrise(self):
        """Returns a sunrise time as a datetime.time object.
        """
        return self._convert_julian_to_time(Earth_Data[0].Sunrise, False)

    def get_sunset(self):
        """Returns a sunset time as a datetime.time object.
        """
        return self._convert_julian_to_time(Earth_Data[0].Sunset, False)

    def load_location(self):
        """Extract from houde information"""
        l_date = datetime.date.today()
        Earth_Data[0] = EarthParameters()
        Solar_Data[0] = SolarParameters()
        for l_obj in house.Location_Data.itervalues():
            if l_obj.Active != True: continue
            Earth_Data[0].Latitude = l_obj.Latitude
            Earth_Data[0].Longitude = l_obj.Longitude
            Earth_Data[0].TimeZone = l_obj.TimeZone
            Earth_Data[0].Name = l_obj.Name
            Earth_Data[0].Date = l_date

def Init():
    global g_logger
    g_logger = logging.getLogger('PyHouse.SunriseSunset')
    g_logger.info("Initializing.")
    SSAPI().load_location()
    g_logger.info("Initialized.")

def Start(p_date = datetime.date.today()):
    Earth_Data[0].Date = p_date
    SSAPI().calc_sunrise_sunset()

# ## END
