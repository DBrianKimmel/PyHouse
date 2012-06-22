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
import house

RAD2DEG = 180.0 / pi
DEG2RAD = pi / 180.0

Earth_Data = {}
Solar_Data = {}
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
        self.JulianDay = None
        self.Latitude = 0.0
        self.Longitude = 0.0
        self.Sunrise = None
        self.Sunset = None
        self.TimeZone = 0.0

    def get_date(self):
        return self.__Date
    def set_date(self, value):
        self.__Date = value

    Date = property(get_date, set_date, None, None)

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
        self.ArgumentOfPerihelion = 0.0
        self.EccentricAnomaly = 0.0
        self.Eccentricity = 0.0
        self.EclipticLongitude = 0.0
        self.EclipticLatitude = 0.0
        self.MeanAnomaly = 0.0
        self.MeanLongitude = 0.0
        self.ObliquityOfEcliptic = 0.0
        self.SolarDeclination = 0.0
        self.SolarDistance = 0.0
        self.SolarLatitude = 0.0
        self.SolarLongitude = .0
        self.SolarNoonHrs = 0.0
        self.SolarRadius = 0.0
        self.TrueAnomaly = 0.0

class SunCalcs(SunriseMathd, EarthParameters, SolarParameters):
    """
    """

    def _calcJulianDates(self, p_earth):
        """From Wikipedia.
        Julian date (JD) system of time measurement for scientific use by the astronomy community,
        presenting the interval of time in days and fractions of a day since January 1, 4713 BC Greenwich noon.
        """
        l_year = p_earth.Date.year
        l_month = p_earth.Date.month
        l_day = p_earth.Date.day
        l_a = (14 - l_month) // 12
        l_y = l_year + 4800 - l_a
        l_m = l_month + (12 * l_a) - 3
        l_jdn = (l_day + (((153 * l_m) + 2) // 5) + (365 * l_y) + (l_y // 4) - (l_y // 100) + (l_y // 400) - 32045)
        p_earth.JulianDay = l_jdn
        p_earth.J2000 = l_jdn - 2451545.0
        g_logger.debug("Calculating julian date {0:}".format(p_earth.JulianDay))
        g_logger.debug("Calculating j2000 day {0:}".format(p_earth.J2000))

    def _calcSolarNoonParams(self, p_earth, p_sun):
        """This is an Ecliptic calculations.  Taken from the wikipedia 'Position of the Sun' entry.
        First we get the JDN of the local solar noon (l_domsn)
        The mean longitude of the Sun, corrected for the aberration of light.
        The mean anomaly of the Sun (actually, of the Earth in its orbit around the Sun, but it is convenient here to assume the Sun orbits the Earth).
        Next, the ecliptic longitude of the Sun.
        Where the obliquity of the ecliptic is not obtained elsewhere, it can be approximated for use with these equations.
        The Earth's axial tilt (called the obliquity of the ecliptic by astronomers) is the angle between the Earth's axis and a line perpendicular to the Earth's orbit.
         """
        p_earth.DayOfLocalMeanSolarNoon = l_domsn = p_earth.J2000 - 0.0009 - (p_earth.Longitude / 360.0)
        g_logger.debug("Calculating the JDN(2000) of Local Mean Solar Noon {0:} at {1:}".format(l_domsn, p_earth.Longitude))
        # These progress each day
        p_sun.Eccentricity = 0.016709 - (1.151E-9 * l_domsn)
        p_sun.ObliquityOfEcliptic = (23.4393 - (3.563E-7 * l_domsn)) * DEG2RAD
        p_sun.MeanLongitude = self.revolution(280.460 + (0.9856474 * l_domsn)) * DEG2RAD
        p_sun.MeanAnomaly = l_ma = self.revolution(357.5291 + (0.9856002585 * l_domsn)) * DEG2RAD
        p_sun.ArgumentOfPerihelion = (282.9404 + 4.70935E-5 * l_domsn) * DEG2RAD
        g_logger.debug("Calculating solar Eccentricity {0:}".format(p_sun.Eccentricity * RAD2DEG))
        g_logger.debug("Calculating solar Obliquity of Ecliptic {0:}".format(p_sun.ObliquityOfEcliptic * RAD2DEG))
        g_logger.debug("Calculating solar Mean Longitude {0:}".format(p_sun.MeanLongitude * RAD2DEG))
        g_logger.debug("Calculating solar Mean Anomaly {0:}".format(p_sun.MeanAnomaly * RAD2DEG))
        g_logger.debug("Calculating solar Argument of Perihelion {0:}".format(p_sun.ArgumentOfPerihelion * RAD2DEG))
        # ecliptic formulae
        p_sun.EclipticLongitude = p_sun.MeanLongitude + (1.915 * DEG2RAD * math.sin(l_ma)) + (0.020 * DEG2RAD * math.sin(2.0 * l_ma))
        p_sun.EclipticLatitude = 0.0 # very, very close at all times.
        p_sun.SolarDistance = 1.00014 - (0.01671 * math.cos(l_ma)) - (.00014 * math.cos(2.0 * l_ma))
        p_sun.EquationCenter = 1.9148 * math.sin(l_ma) + 0.02000 * math.sin(2.0 * l_ma) + 0.0003 * math.sin(3.0 * l_ma)
        g_logger.debug("Calculating solar Ecliptic Longitude {0:}".format(p_sun.EclipticLongitude * RAD2DEG))
        g_logger.debug("Calculating solar Ecliptic Latitude {0:}".format(p_sun.EclipticLatitude * RAD2DEG))
        g_logger.debug("Calculating solar Ecliptic Distance {0:}".format(p_sun.SolarDistance))
        g_logger.debug("Calculating solar Equation of Cebnter {0:}".format(p_sun.EquationCenter))

    def _calcEccentricAnomaly(self, p_sun):
        """Is an angular parameter that defines the position of a body that is moving along an elliptic Kepler orbit.
        E = MeanAnom + e*(180/pi) * sin(MeanAnom) * ( 1.0 + e*cos(MeanAnom) )
        E = M + e * RADEG * sind(M) * ( 1.0 + e * cosd(M) );
        """
        lEA = p_sun.Eccentricity #* RAD2DEG
        lEA *= math.sin(p_sun.MeanAnomaly)
        lEA *= (1.0 + (p_sun.Eccentricity) * math.cos(p_sun.MeanAnomaly))
        lEA += p_sun.MeanAnomaly * DEG2RAD
        p_sun.EccentricAnomaly = lEA * DEG2RAD
        g_logger.debug("Calculating Eccentric Anomaly {0:}".format(p_sun.EccentricAnomaly))

    def _calcSolarLongitude(self, p_sun):
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
        l_solarLongitude = p_sun.TrueAnomaly + p_sun.ArgumentOfPerihelion * RAD2DEG       # True solar longitude
        if l_solarLongitude >= 360.0:
            l_solarLongitude = l_solarLongitude - 360.0   # Make it 0..360 degrees
        p_sun.SolarLongitude = l_solarLongitude
        g_logger.debug("Calculating Solar Longitude {0:}".format(p_sun.SolarLongitude))

    def _calcTrueAnomaly(self, p_sun):
        """
        """
        x = math.cos(p_sun.EccentricAnomaly) - p_sun.Eccentricity
        y = math.sqrt(1.0 - p_sun.Eccentricity * p_sun.Eccentricity) * math.sin(p_sun.EccentricAnomaly)
        p_sun.TrueAnomaly = self.atan2d(y, x)
        g_logger.debug("Calculating True Anomaly {0:}".format(p_sun.TrueAnomaly))

    def _calcSolarDistance(self, p_sun):
        """Computes the Sun's distance in AU at a given day.
        It varies between 0.9832898912 AU and 1.0167103335 AU.
        """
        l_Eccentricity = p_sun.Eccentricity
        E = p_sun.EccentricAnomaly
        x = math.cos(E) - l_Eccentricity
        y = math.sqrt(1.0 - l_Eccentricity * l_Eccentricity) * math.sin(E)
        l_solarDistance = math.sqrt(x * x + y * y)              #Solar distance
        p_sun.SolarDistance = l_solarDistance
        p_sun.SolarRadius = 0.2666 / l_solarDistance
        g_logger.debug("Calculating Solar Distance {0:}".format(p_sun.SolarDistance))

    def _2calcGMST0(self, p_earth):
        """ Sidtime at 0h UT = L (Sun's mean longitude) + 180.0 degr 
        L = M + w, as defined in sunpos().
        """
        sidtim0 = self.revolution((180.0 + 356.0470 + 282.9404) +
                          (0.9856002585 + 4.70935E-5) * p_earth.DayOfLocalMeanSolarNoon)
        return sidtim0

    def _2calcSolarRARadians(self, p_sun):
        """Returns the angle of the Sun (RA) in radians.
        """
        r = p_sun.SolarDistance
        x = r * math.cos(p_sun.SolarLongitude)
        y = r * math.sin(p_sun.SolarLongitude)
        y = y * math.cos(p_sun.ObliquityOfEcliptic)
        RA = math.atan2(y, x)
        return RA

    def _2calcSolarNoon(self, p_earth, p_sun):
        """When the sun crosses the meridian.
        Compute local sidereal time of this moment
        Compute Sun's RA + Decl at this moment
        Compute time when Sun is at south - in hours UT
        """
        l_SiderealTime = self.revolution(self._2calcGMST0(p_earth) + 180.0 + p_earth.Longitude)
        l_solarRA = self._2calcSolarRARadians(p_sun)
        tsouth = 12.0 - self.rev180(l_SiderealTime - l_solarRA * RAD2DEG) / 15.0;
        l_south = self._convert_to_time(tsouth)
        p_sun.SolarNoonHrs = tsouth
        g_logger.debug("Calculating Solar Noon {0:} {1:}".format(p_sun.SolarNoonHrs, l_south))
        return l_south

    def _2calcSolarDeclinationRadians(self, p_earth, p_sun):
        """Returns the declination of the sun(dec) for a given day d.
        """
        lon = p_sun.SolarLongitude
        r = p_sun.SolarDistance
        x = r * math.cos(lon)
        y = r * math.sin(lon)
        l_ObliquityOfEcliptic = p_sun.ObliquityOfEcliptic
        z = y * math.sin(l_ObliquityOfEcliptic)
        y = y * math.cos(l_ObliquityOfEcliptic)
        l_dec = self.atan2d(z, math.sqrt(x * x + y * y)) * DEG2RAD
        p_sun.SolarDeclination = l_dec
        g_logger.debug("Calculating Solar Declination {0:} @ Lon {1:}".format(l_dec * RAD2DEG, lon))
        l_sin_dec = math.sin(p_sun.EclipticLongitude) * math.sin(23.45 * DEG2RAD)
        l_dec2 = math.asin(l_sin_dec)
        g_logger.debug("Calculating Solar Declination # 2 {0:} @ Lon {1:}".format(l_dec2 * RAD2DEG, p_earth.Longitude))
        return l_dec2

    def _2calcCost(self, p_altit, p_earth, p_sun):
        """altit = the altitude which the Sun should cross.
         
        Cos HourAngle 
        cost = ( sind(altit) - sind(lat) * sind(sdec) ) /
                  ( cosd(lat) * cosd(sdec) );
        """
        l_AltRad = p_altit * DEG2RAD
        l_LatRad = p_earth.Latitude * DEG2RAD
        l_DecRad = self._2calcSolarDeclinationRadians(p_earth, p_sun)
        l_cost = ((math.sin(-l_AltRad) - (math.sin(l_LatRad) * math.sin(l_DecRad))) / \
                (math.cos(l_LatRad) * math.cos(l_DecRad)))
        l_ha = math.acos(l_cost)
        g_logger.debug("Calculating Solar COST {0:} {1:} {2:}".format(l_cost, l_ha, l_ha * RAD2DEG))
        return l_cost

    def _calcSunRiseSet(self, p_earth, p_sun):
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
        l_Altitude = -35.0 / 60.0
        self._2calcSolarNoon(p_earth, p_sun) # compute self.m_solar_noon_hrs
        tsouth = p_sun.SolarNoonHrs
        l_Altitude = l_Altitude - p_sun.SolarRadius
        cost = self._2calcCost(l_Altitude, p_earth, p_sun)
        if cost >= 1.0:
            t = 0.0           # Sun always below altit
        elif cost <= -1.0:
            t = 12.0;         # Sun always above altit
        else:
            t = self.acosd(cost) / 15.0   # The diurnal arc, hours
        g_logger.info("### {0:}, {1:}, {2:}".format(tsouth, t, p_earth.TimeZone))
        p_earth.Sunrise = self._convert_to_time(tsouth - t)# + p_earth.TimeZone)
        p_earth.Sunset = self._convert_to_time(tsouth + t) # + p_earth.TimeZone)
        g_logger.info("Sunrise / Sunset {0:}, {1:}".format(p_earth.Sunrise, p_earth.Sunset))
        j_set = 2451545.0009 + ((l_ha + l_w) / 360.0) + n + 0.0053 * sin(M) - 0.0069 * sin(2.0 * lam)

    def _convert_to_time(self, p_hours):
        """Convert a time in hours (float) to a datetime.time object.
        """
        #print "convert-to-time ", p_hours
        if p_hours > 24.0: p_hours -= 24.0
        if p_hours < 0.0: p_hours += 24.0
        l_hours = int(p_hours)
        l_minutes = int(60.0 * (p_hours - l_hours))
        l_seconds = int(60 * (60.0 * (p_hours - l_hours) - l_minutes))
        l_time = datetime.time(l_hours, l_minutes, l_seconds)
        return l_time

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

    def calc_sunrise_sunset(self):
        """Trigger all calculations.
        Calculate the coordinates of the Sun in the ecliptic coordinate system.
        Convert to the equatorial coordinate system.
        Convert to the horizontal coordinate system for the observer's local circumstances.
        """
        global g_logger
        self._calcJulianDates(Earth_Data[0])
        self._calcSolarNoonParams(Earth_Data[0], Solar_Data[0])
        self._calcEccentricAnomaly(Solar_Data[0])
        self._calcTrueAnomaly(Solar_Data[0])
        self._calcSolarLongitude(Solar_Data[0])
        self._calcSolarDistance(Solar_Data[0])
        self._calcSunRiseSet(Earth_Data[0], Solar_Data[0])
        g_logger.info("Calculating sunrise/sunset now. Rise={0:}, Set={1:}".format(Earth_Data[0].Sunrise, Earth_Data[0].Sunset))


class SSAPI(SunCalcs):

    def get_sunrise(self):
        """Returns a sunrise time as a datetime.time object.
        """
        return Earth_Data[0].Sunrise

    def get_sunset(self):
        """Returns a sunset time as a datetime.time object.
        """
        return Earth_Data[0].Sunset

    def set_date(self, p_date = datetime.date.today()):
        """Pass in the datetime date to calculate for.
        Using this will trigger a recalculation of Sunrise and Sunset.
        """
        Earth_Data[0].Date = p_date
        g_logger.info("Setting date to {0:}".format(Earth_Data[0].Date))
        self.calc_sunrise_sunset()

    def set_latitude_longitude(self, p_obj, p_latitude = 28.938464, p_longitude = -82.517208):
        """The lat and long in decimal degrees (-) for South and West.
        Using this will trigger a recalculation of Sunrise and Sunset.
        """
        g_logger.info("Loading location data for house {0:}".format(p_obj.Name))
        Earth_Data[0].Latitude = p_latitude
        Earth_Data[0].Longitude = p_longitude

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
            self.set_latitude_longitude(l_obj, Earth_Data[0].Latitude, Earth_Data[0].Longitude)
        self.set_date(l_date)

def Init():
    global g_logger
    g_logger = logging.getLogger('PyHouse.SunriseSunset')
    g_logger.info("Initializing.")
    SSAPI().load_location()
    g_logger.info("Initialized.")

### END
