#!/usr/bin/env  python

"""Calculate the suns location at local noon.
    Then calculate sunrise and sunset for the day.
    
    Heliocentric means that the Earth position is calculated with respect to the center of the sun. 
    Geocentric means that the sun position is calculated with respect to the Earth center.
    Topocentric means that the sun position is calculated with respect to the observer local position at the Earth surface. 
"""

# Import system type stuff
import calendar
import configure_mh
import datetime
from datetime import date
import logging
import math
from math import pi

# Import PyMh files
import house


class SunriseMathd(object):
    """
    """

    m_date = None
    m_logger = None
    m_timezone = 0.0

    def acosd(self, x):
        """Returns the arc cos in degrees"""
        return math.acos(x) * 180.0 / pi

    def atan2d(self, y, x):
        """Returns the atan2 in degrees"""
        return math.atan2(y, x) * 180.0 / pi

    def radians2dms(self, pRadians):
        """Convert Radians to dms - mostly for printing"""
        mins, sec = divmod(pRadians * 3600 * 180.0 / pi, 60)
        deg, mins = divmod(mins, 60)
        return deg, mins, sec

    def radians2hms(self, pRadians):
        mins, sec = divmod(pRadians * 3600 / 15 * 180 / pi, 60)
        hour, mins = divmod(mins, 60)
        return hour, mins, sec

    def formatRadians2dms(self, pRadians):
        d, m, s = self.radians2dms(pRadians)
        return " {0:} Deg, {1:} Min, {2:} Sec ".format(int(d), int(m), s)

    def formatRadians2hms(self, pRadians):
        h, m, s = self.radians2hms(pRadians)
        return " {0:} Hour, {1:} Min, {2:} Sec ".format(int(h), int(m), s)

class SolarParameters(SunriseMathd):
    """The ecliptic coordinate system is a celestial coordinate system that uses the ecliptic for its fundamental plane.
        The ecliptic is the path that the sun appears to follow across the celestial sphere over the course of a year.
        It is also the intersection of the Earth's orbital plane and the celestial sphere.
        The latitudinal angle is called the ecliptic latitude or celestial latitude, measured positive towards the north.
        The longitudinal angle is called the ecliptic longitude or celestial longitude, measured eastwards from 0 to 360.
        Like right ascension in the equatorial coordinate system, 0deg ecliptic longitude is pointing towards the Sun from the Earth at the Northern hemisphere vernal equinox.
        This choice makes the coordinates of the fixed stars subject to shifts due to the precession, so that always a reference epoch should be specified.
        Usually epoch J2000.0 is taken, but the instantaneous equinox of the day (called the epoch of date) is possible too.
    """
    mSolarLongitude = 0.0
    mSolarLatitude = 0.0
    mObliquityOfEcliptic = 0.0
    mEccentricity = 0.0
    mTrueAnomaly = 0.0


class SunCalcs(SolarParameters):
    """
    """

    def _calcJulianDates(self):
        """This function is based on NREL/TP-560-34302 by Andreas and Reda
        This function does not accept years before 0 because of the bounds check
            on Python's datetime.year field.
        """
        lYear = self.getDate().year
        lMonth = self.getDate().month
        if(lMonth <= 2.0):        # shift to accomodate leap years?
            lYear = lYear - 1.0
            lMonth = lMonth + 12.0
        lGregorianOffset = 2.0 - (lYear // 100.0) + ((lYear // 100.0) // 4.0)
        lJulianDay = math.floor(365.25 * (lYear + 4716.0)) + math.floor(30.6001 * (lMonth + 1.0)) + self.getDate().day - 1524.5
        if (lJulianDay <= 2299160.0):
            lJulianDay += lGregorianOffset # after October 5, 1852
        self.setJulianDay(lJulianDay)

    def _calcDaysSinceJ2000(self):
        """Compute the number of days elapsed since 2000 Jan 0.0
           (which is equal to 1999 Dec 31, 0h UT = 2451544)
           2011 Jun 21 is 2455734 which is 4190 days since
        """
        lDatePython = (self.m_date - date(1999, 12, 31)).days
        lDateTest = (367 * (self.getDate().year) - ((7 * ((self.getDate().year) + (((self.getDate().month) + 9) / 12))) / 4) + ((275 * (self.getDate().month)) / 9) + (self.getDate().day) - 730530)
        assert (lDatePython == lDateTest)
        self.mJ2000 = lDatePython

    def _calcDayOfLocalMeanSolarNoon(self):
        self.mDayOfLocalMeanSolarNoon = self.getDaysSinceJ2000() + 0.5 - self.getLongitudeDegrees() / 360.0     # DaysOfGmtNoon - Longitude

    def _calcSolarNoonParams(self):
        self._calcDayOfLocalMeanSolarNoon()
        self.mEccentricity = 0.016709 - 1.151E-9 * self.getDayOfLocalMeanSolarNoon()
        self.mObliquityOfEcliptic = (23.4393 - 3.563E-7 * self.getDayOfLocalMeanSolarNoon()) * pi / 180.0
        self.mArgumentOfPerihelionRadians = (282.9404 + 4.70935E-5 * self.getDayOfLocalMeanSolarNoon()) * pi / 180.0
        self.mMeanAnomalyRadians = self.revolution(356.0470 + 0.9856002585 * self.getDayOfLocalMeanSolarNoon()) * pi / 180.0

    def _calcGMST0(self):
        """ Sidtime at 0h UT = L (Sun's mean longitude) + 180.0 degr 
        L = M + w, as defined in sunpos().
        """
        sidtim0 = self.revolution((180.0 + 356.0470 + 282.9404) +
                          (0.9856002585 + 4.70935E-5) * self.getDayOfLocalMeanSolarNoon())
        return sidtim0

    def _calcEccentricAnomalyRadians(self):
        """Is an angular parameter that defines the position of a body that is moving along an elliptic Kepler orbit.
        E = MeanAnom + e*(180/pi) * sin(MeanAnom) * ( 1.0 + e*cos(MeanAnom) )
        E = M + e * RADEG * sind(M) * ( 1.0 + e * cosd(M) );
        """
        lEA = self.getEccentricity()
        lEA *= (180.0 / pi)
        lEA *= math.sin(self.getMeanAnomalyRadians())
        lEA *= (1.0 + (self.getEccentricity()) * math.cos(self.getMeanAnomalyRadians()))
        lEA += self.getMeanAnomalyDegrees()
        self.mEccentricAnomalyRadians = lEA * pi / 180.0

    def _calcSolarLongitude(self):
        """Computes the Sun's ecliptic longitude at an instant given in d, number of days since 2000 Jan 0.0.
        The Sun's ecliptic latitude is not computed, since it's always very near 0.
        
        The ecliptic coordinate system is a celestial coordinate system that uses the ecliptic for its fundamental plane.
        The ecliptic is the path that the sun appears to follow across the celestial sphere over the course of a year.
        It is also the intersection of the Earth's orbital plane and the celestial sphere.
        The latitudinal angle is called the ecliptic latitude or celestial latitude, measured positive towards the north.
        The longitudinal angle is called the ecliptic longitude or celestial longitude, measured eastwards from 0 to 360.
        Like right ascension in the equatorial coordinate system, 0deg ecliptic longitude is pointing towards the Sun from the Earth at the Northern hemisphere vernal equinox.
        This choice makes the coordinates of the fixed stars subject to shifts due to the precession, so that always a reference epoch should be specified.
        Usually epoch J2000.0 is taken, but the instantaneous equinox of the day (called the epoch of date) is possible too.
        """
        solarLongitude = self.getTrueAnomaly() + self.getArgumentOfPerihelionDegrees()       # True solar longitude
        if solarLongitude >= 360.0:
            solarLongitude = solarLongitude - 360.0   # Make it 0..360 degrees
        self.mSolarLongitude = solarLongitude

    def _calcTrueAnomaly(self):
        """
        """
        x = math.cos(self.getEccentricAnomalyRadians()) - self.getEccentricity()
        y = math.sqrt(1.0 - self.getEccentricity() * self.getEccentricity()) * math.sin(self.getEccentricAnomalyRadians())
        self.mTrueAnomaly = self.atan2d(y, x)

    def _calcSolarDistance(self):
        """Computes the Sun's distance in AU at a given day.
        It varies between 0.9832898912 AU and 1.0167103335 AU.
        """
        lEccentricity = self.getEccentricity() #ok
        E = self.getEccentricAnomalyRadians()
        x = math.cos(E) - lEccentricity
        y = math.sqrt(1.0 - lEccentricity * lEccentricity) * math.sin(E)
        solarDistance = math.sqrt(x * x + y * y)              #Solar distance
        self.m_solar_distance = solarDistance
        self.m_solar_radius = 0.2666 / solarDistance

    def _calcSolarNoon(self):
        """When the sun crosses the meridian.
        Compute local sidereal time of this moment
        Compute Sun's RA + Decl at this moment
        Compute time when Sun is at south - in hours UT
        """
        lSiderealTime = self.revolution(self._calcGMST0() + 180.0 + self.getLongitudeDegrees())
        solarRA = self._calcSolarRARadians()
        tsouth = 12.0 - self.rev180(lSiderealTime - solarRA * 180 / pi) / 15.0;
        l_south = self._convert_to_time(tsouth)
        self.m_solar_noon_hrs = tsouth
        return l_south

    def _calcCost(self, altit):
        """altit = the altitude which the Sun should cross.
         
        cost = ( sind(altit) - sind(lat) * sind(sdec) ) /
                  ( cosd(lat) * cosd(sdec) );
        """
        lAltRad = altit * pi / 180.0
        lLatRad = self.getLatitudeRadians()
        lDecRad = self._calcSolarDeclinationRadians()
        cost = (math.sin(lAltRad) - \
                math.sin(lLatRad) * \
                  math.sin(lDecRad) / \
                (math.cos(lLatRad) * \
                 math.cos(lDecRad)))
        return cost

    def _calcSunRiseSet(self):
        """altit = the altitude which the Sun should cross
            Set to:
                -35/60 degrees for rise/set,
                -6 degrees for civil,
                -12 degrees for nautical and
                -18 degrees for astronomical twilight.
        upper_limb: non-zero -> upper limb, zero -> center
            Set to:
                1 when computing rise/set times and
                0 when computing start/end of twilight.
        """
        lAltitude = -35.0 / 60.0
        self._calcSolarNoon() # compute self.m_solar_noon_hrs
        tsouth = self.m_solar_noon_hrs
        lAltitude = lAltitude - self.m_solar_radius
        cost = self._calcCost(lAltitude)
        if cost >= 1.0:
            t = 0.0           # Sun always below altit
        elif cost <= -1.0:
            t = 12.0;         # Sun always above altit
        else:
            t = self.acosd(cost) / 15.0   # The diurnal arc, hours
        self.mSunrise = self._convert_to_time(tsouth - t + self.m_timezone)
        self.mSunset = self._convert_to_time(tsouth + t + self.m_timezone)
        return (tsouth - t, tsouth + t)

    def _calcSolarRARadians(self):
        """Returns the angle of the Sun (RA) in radians"""
        r = self.m_solar_distance
        x = r * math.cos(self.getSolarLongitudeRadians())
        y = r * math.sin(self.getSolarLongitudeRadians())
        y = y * math.cos(self.getObliquityOfEclipticRadians())
        RA = math.atan2(y, x)
        return RA

    def _calcSolarDeclinationRadians(self):
        """Returns the declination of the sun(dec) for a given day d."""
        lon = self.getSolarLongitudeRadians()
        r = self.m_solar_distance
        x = r * math.cos(lon)
        y = r * math.sin(lon)
        lObliquityOfEcliptic = self.getObliquityOfEclipticRadians()
        z = y * math.sin(lObliquityOfEcliptic)
        y = y * math.cos(lObliquityOfEcliptic)
        dec = self.atan2d(z, math.sqrt(x * x + y * y)) * pi / 180.0
        self.mSolarDeclinationRadians = dec
        return dec

    def revolution(self, p_degrees):
        """
        This function reduces any angle to within the first revolution 
        by subtracting or adding even multiples of 360.0 until the     
        result is >= 0.0 and < 360.0
        
        Reduce angle to within 0..360 degrees
        """
        return (p_degrees - 360.0 * math.floor(p_degrees / 360.0))

    def rev180(self, x):
        """Reduce angle to within +180..+180 degrees."""
        return (x - 360.0 * math.floor(x / 360.0 + 0.5))

    def getLatitudeRadians(self):
        return self.m_latitude * pi / 180.0

    def getLongitudeDegrees(self):
        return self.m_longitude

    def getLongitudeRadians(self):
        return self.m_longitude * pi / 180.0

    def getDate(self):
        return self.m_date

    def setJulianDay(self, pDate):
        self.mJulianDate = pDate

    def getDaysSinceJ2000(self):
        return self.mJ2000

    def isLeapYear(self, pYear):
        return calendar.isleap(pYear)

    def getDayOfLocalMeanSolarNoon(self):
        return self.mDayOfLocalMeanSolarNoon

    def getEccentricity(self):
        return self.mEccentricity

    def getObliquityOfEclipticRadians(self):
        return self.mObliquityOfEcliptic

    def getArgumentOfPerihelionRadians(self):
        return self.mArgumentOfPerihelionRadians

    def getArgumentOfPerihelionDegrees(self):
        return self.mArgumentOfPerihelionRadians * 180.0 / pi

    def getMeanAnomalyRadians(self):
        return self.mMeanAnomalyRadians

    def getMeanAnomalyDegrees(self):
        return self.mMeanAnomalyRadians * 180.0 / pi

    def _convert_to_time(self, p_hours):
        """Convert a time in hours (float) to a datetime.time object.
        """
        l_hours = int(p_hours)
        l_minutes = int(60.0 * (p_hours - l_hours))
        l_seconds = int(60 * (60.0 * (p_hours - l_hours) - l_minutes))
        l_time = datetime.time(l_hours, l_minutes, l_seconds)
        return l_time

    def getEccentricAnomalyRadians(self):
        return self.mEccentricAnomalyRadians

    def getTrueAnomaly(self):
        return self.mTrueAnomaly

    def getSolarLongitudeRadians(self):
        return self.mSolarLongitude * pi / 180.0

    def calc_sunrise_sunset(self):
        """Trigger all calculations.
        """
        self._calcDaysSinceJ2000()
        self._calcJulianDates()
        self._calcSolarNoonParams()
        self._calcEccentricAnomalyRadians()
        self._calcTrueAnomaly()
        self._calcSolarLongitude()
        self._calcSolarDistance()
        self._calcSunRiseSet()
        self.m_logger.info("Calculating sunrise/sunset now. Rise={0:}, Set={1:}".format(self.mSunrise, self.mSunset))


class SunriseSunsetAPI(SunCalcs):

    def get_sunrise(self):
        """Returns a sunrise time as a datetime.time object.
        """
        return self.mSunrise

    def get_sunset(self):
        """Returns a sunset time as a datetime.time object.
        """
        return self.mSunset

    def set_date(self, p_date = datetime.date.today()):
        """Pass in the datetime date to calculate for.
        Using this will trigger a recalculation of Sunrise and Sunset.
        """
        self.m_date = p_date
        self.m_logger.info("Setting date to {0:}".format(self.m_date))
        self.calc_sunrise_sunset()

    def set_latitude_longitude(self, p_latitude = 28.938464, p_longitude = -82.517208):
        """The lat and long in decimal degrees (-) for South and West.
        Using this will trigger a recalculation of Sunrise and Sunset.
        """
        self.m_latitude = p_latitude
        self.m_longitude = p_longitude

    def load_location(self):
        """Extract from houde information"""
        self.m_latitude = 0.0
        self.m_longitude = 0.0
        self.m_timezone = 0.0
        for l_key, l_obj in house.Location_Data.iteritems():
            #print " ..Sunrise/set ", l_key, l_obj
            l_active = l_obj.Active
            if l_active == True:
                self.m_latitude = float(l_obj.Latitude)
                self.m_longitude = float(l_obj.Longitude)
                self.m_timezone = float(l_obj.Timezone)


class SunriseSunsetMain(SunriseSunsetAPI):

    def __init__(self):
        self.m_logger = logging.getLogger('PyMh.SunriseSunset')
        self.m_logger.info("Initializing.")
        self.load_location()
        self.set_latitude_longitude(self.m_latitude, self.m_longitude)
        self.m_date = datetime.date.today()
        self.set_date(self.m_date)
        self.m_logger.info("Initialized.")

### END
