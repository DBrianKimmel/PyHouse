"""
@name: PyHouse/src/Modules/scheduling/sunrisesunset.py
@author: D. Brian Kimmel
@contact: <d.briankimmel@gmail.com
@copyright: 2011-2014 by D. Brian Kimmel
@note: Created on Mar 6, 2011
@license: MIT License
@summary: Calculate the suns location at local noon, then calculate sunrise and sunset for the day.


http://en.wikipedia.org/wiki/Sunrise_equation

http://users.electromagnetic.net/bu/astro/iyf-calc.php?lat=28.938464&long=82.51720

Find today's Julian date (days since Jan 1, 2000 + 2451545):
Julian date: 2456906

Now, calculate Jtransit at longitude 82.51720, start with n:
n* = (Jdate - 2451545 - 0.0009) - (lw/360)
n = round(n*)
n* = (2456906 - 2451545 - 0.0009) - (82.51720/360) = 5360.7698855556
n = round(5360.7698855556) = 5361

Now J*:
J* = 2451545 + 0.0009 + (lw/360) + n
J* = 2451545 + 0.0009 + (82.51720/360) + 5361 = 2456906.2301144

Using J*, calculate M (mean anomaly) and then use that to calculate C and <lambda>:
M = [357.5291 + 0.98560028 * (J* - 2451545)] mod 360
M = [357.5291 + 0.98560028 * (2456906.2301144 - 2451545)] mod 360 = 5641.5590019406 mod 360 = 241.55900194059

We need to calculate the equation of center, C:
C = (1.9148 * sin(M)) + (0.0200 * sin(2 * M)) + (0.0003 * sin(3 * M))
C = 1.9148 * sin(241.55900194059) + 0.0200 * sin(2 * 241.55900194059) + 0.0003 * sin(3 * 241.55900194059) = -1.6669235826461

We need <lambda> which is the ecliptical longitude of the sun:
<lambda> = (M + 102.9372 + C + 180) mod 360
<lambda> = (241.55900194059 + 102.9372 + -1.6669235826461 + 180) mod 360 = 522.82927835795 mod 360 = 162.82927835795

Finally, calculate Jtransit:
Jtransit = J* + (0.0053 * sin(M)) - (0.0069 * sin(2 * <lambda>))
Jtransit = 2456906.2301144 + (0.0053 * sin(241.55900194059)) - (0.0069 * sin(2 * 162.82927835795)) = 2456906.2293466

Now, to get an even more accurate number, recursively recalculate M using Jtransit until it stops changing. Notice how close the approximation was.
I1: M = 241.55824511682, C = -1.6669112599272, <lambda> = 162.82853385689, Jtransit = 2456906.2293467
I2: M = 241.55824529581, C = -1.6669112628416, <lambda> = 162.82853403297, Jtransit = 2456906.2293467
I3: M = 241.55824529581, C = -1.6669112628416, <lambda> = 162.82853403297, Jtransit = 2456906.2293467

Ok, translate this into something we understand. i.e. When is Solar Noon?
Jtransit = 2456906.2293467 = 09/05/2014 at 13:30:15 -0500

Alrighty, now calculate how long the sun is in the sky at latitude 28.938464:

Now we need to calculate <delta> which is the declination of the sun:
<delta> = arcsin( sin(<lambda>) * sin(23.45) )
<delta> = arcsin(sin(162.82853403297) * sin(23.45)) = 6.7471083756717

Now we can go about calculating H (Hour angle):
H = arccos( [sin(-0.83) - sin(ln) * sin(<delta>)] / [cos(ln) * cos(<delta>)] )
H = arccos((sin(-0.83) - sin(28.938464) * sin(6.7471083756717))/(cos(28.938464) * cos(6.7471083756717))) = 94.708153427328

Just as above, calculate J*, but this time using hour-angle:
J** = 2451545 + 0.0009 + ((H + lw)/360) + n
J** = 2451545 + 0.0009 + ((94.708153427328 + 82.51720)/360) + 5361 = 2456906.4931926

We can use M from above because it really doesn't change that much over the course of a day, calculate Jset in the same way:
Jset = J** + (0.0053 * sin(M)) - (0.0069 * sin(2 * <lambda>))
Jset = 2456906.4931926 + (0.0053 * sin(241.55824529581)) - (0.0069 * sin(2 * 162.82853403297)) = 2456906.4924249

Now I'm going to cheat and calculate Jrise:
Jrise = Jtransit - (Jset - Jtransit)
Jrise = 2456906.2293467 - (2456906.4924249 - 2456906.2293467) = 2456905.9662685

Using the same idea, figure out when sunrise and sunset are:
Jrise = 2456905.9662685 = 09/05/2014 at 07:11:25 -0500
Jset = 2456906.4924249 = 09/05/2014 at 19:49:05 -0500
"""

# Import system type stuff
import datetime
import xml.etree.ElementTree as ET
from twisted.trial import unittest
from math import pi

# Import PyMh files
# from Modules.Core.data_objects import PyHouseData, HouseObjs, LocationData
from Modules.Scheduling import sunrisesunset
from Modules.Scheduling.sunrisesunset import JDate
from test.testing_mixin import SetupPyHouseObj
from test import xml_data
from Modules.Utilities.tools import PrettyPrintAny
# from datetime import tzinfo
from Modules.Scheduling.sunrisesunset import JulianParameters


RAD2DEG = 180.0 / pi
DEG2RAD = pi / 180.0


# All Tests
T_LATITUDE = 28.938448
T_LONGITUDE = -82.517208  # lon/360 = -0.2292144666666667
T_TIMEZONE_NAME = 'US/Eastern'
T_TIMEZONE_OFFSET = '-5:00'
T_DAYLIGHT_SAVINGS_TIME = '-4:00'

"""
# Test time 0
T_DATE = datetime.date(2013, 6, 6)
T_JULIAN_DAY =
T_JULIAN_DATE =
"""

T_TZ = sunrisesunset.LocationTz()

# Test time 1
T_DATE = datetime.date(2014, 9, 5)
T_SUNRISE = datetime.datetime(2014, 9, 5, 7, 10, 55, 0, tzinfo = T_TZ)
T_SUNSET = datetime.datetime(2014, 9, 5, 19, 50, 15, 0, tzinfo = T_TZ)

T_JULIAN_DAY = 2456906
T_JULIAN_DATE = 2456905.5
T_JULIAN_CYCLE = 2456906.0
T_J2K = 5360.4491
T_J2K_CYCLE = 5361.0
T_J2K_TRANSIT = 5361.23011446666667


T_MEAN_ANOMALY = 241.55900194059
T_EQUATION_CENTER = -1.6669235826461
T_ECLIPTIC_LONGITUDE = 162.82927835795
T_TRANSIT = 5361.23011446667  # 2456906.2301144

T_MEAN_ANOMALY_1 = 241.55824511682
T_EQUATION_CENTER_1 = -1.6669112599272
T_ECLIPTIC_LONGITUDE_1 = 162.82853385689
T_TRANSIT_1 = 5361.2293465  # 2456906.2293467

T_MEAN_ANOMALY_2 = 241.55824529581
T_EQUATION_CENTER_2 = -1.6669112628416
T_ECLIPTIC_LONGITUDE_2 = 162.82853403297
T_TRANSIT_2 = 5361.2293467  # 2456906.2293467

T_MEAN_ANOMALY_3 = 241.55824529581
T_EQUATION_CENTER_3 = -1.6669112628416
T_ECLIPTIC_LONGITUDE_3 = 162.82853403297
T_TRANSIT_3 = 5361.22934672  # 456906.2293467


class SetupMixin(object):
    """
    """

    def setUp(self, p_root):
        self.m_pyhouse_obj = SetupPyHouseObj().BuildPyHouseObj(p_root)
        self.m_xml = SetupPyHouseObj().BuildXml(p_root)
        self.test_date_1 = T_DATE

    @staticmethod
    def load_earth():
        l_loc = sunrisesunset.EarthParameters()
        l_loc.Latitude = T_LATITUDE
        l_loc.Longitude = T_LONGITUDE
        l_loc.TimeZoneName = T_TIMEZONE_NAME
        l_loc.TimeZoneOffset = T_TIMEZONE_OFFSET
        l_loc.DaylightSavingsTime = T_DAYLIGHT_SAVINGS_TIME
        return l_loc


class Test_01_Results(SetupMixin, unittest.TestCase):
    """
    Overall test to see if sunrise and sunset are correct for any date.
    These tests should break if any other test is bad.
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(xml_data.XML_LONG))
        self.m_api = sunrisesunset.API()

    def test_01_Sunrise(self):
        """
        Given a date, we should get a correct sunrise datetime
        """
        self.m_api.Start(self.m_pyhouse_obj, T_DATE)
        l_result, l_earth = self.m_api.get_sunrise_datetime()
        print('Sunrise for date {};  Calc: {};  S/B: {}'.format(T_DATE, l_result, T_SUNRISE))
        PrettyPrintAny(l_earth, 'T_01, t_01, Params')
        self.assertEqual(l_result, T_SUNRISE)

    def test_02_Sunset(self):
        """
        Given a date, we should get a correct sunset datetime
        """
        self.m_api.Start(self.m_pyhouse_obj, T_DATE)
        l_result = self.m_api.get_sunset_datetime()
        print('Sunset for date {};  Calc: {};  S/B: {}'.format(T_DATE, l_result, T_SUNSET))
        self.assertEqual(l_result, T_SUNSET)


class Test_02_Utility(SetupMixin, unittest.TestCase):

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(xml_data.XML_LONG))
        self.m_api = sunrisesunset.Util

    def test_01_Degree360(self):
        l_ret = self.m_api._revolution(175.5)
        self.assertEqual(l_ret, 175.5)
        l_ret = self.m_api._revolution(1175.5)
        self.assertEqual(l_ret, 95.5)
        l_ret = self.m_api._revolution(12375.5)
        self.assertEqual(l_ret, 135.5)
        l_ret = self.m_api._revolution(-175.5)
        self.assertEqual(l_ret, 184.5)
        l_ret = self.m_api._revolution(-1175.5)
        self.assertEqual(l_ret, 264.5)
        l_ret = self.m_api._revolution(-12375.5)
        self.assertEqual(l_ret, 224.5)

    def test_02_NormalizeHours(self):
        l_ret = self.m_api._normalize_hours(2.5)
        self.assertEqual(l_ret, 2.5)
        l_ret = self.m_api._normalize_hours(102.5)
        self.assertEqual(l_ret, 6.5)
        l_ret = self.m_api._normalize_hours(1002.5)
        self.assertEqual(l_ret, 18.5)
        l_ret = self.m_api._normalize_hours(-2.5)
        self.assertEqual(l_ret, 21.5)
        l_ret = self.m_api._normalize_hours(-102.5)
        self.assertEqual(l_ret, 17.5)
        l_ret = self.m_api._normalize_hours(-1002.5)
        self.assertEqual(l_ret, 5.5)

    def test_03_Convert2DateTime(self):
        l_time = 32.55
        l_ret = self.m_api._convert_to_datetime(l_time)
        print('Convert to datetime  {0:}->{1:}'.format(l_time, l_ret))
        self.assertEqual(l_ret, datetime.timedelta(1, 30780))


class Test_03_ObserverEarth(SetupMixin, unittest.TestCase):

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(xml_data.XML_LONG))
        self.m_earth = SetupMixin.load_earth()
        self.m_api = sunrisesunset.API()

    def test_01_Location(self):
        l_location = self.m_api._load_location(self.m_pyhouse_obj)
        PrettyPrintAny(l_location, 'Location')
        self.assertEqual(l_location.Latitude, T_LATITUDE)


class Test_04_Julian(SetupMixin, unittest.TestCase):

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(xml_data.XML_LONG))
        self.m_pyhouse_obj.House.OBJs.Location.Latitude = T_LATITUDE
        self.m_api = JDate
        self.m_earth = SetupMixin.load_earth()
        self.m_julian = JulianParameters
        self.m_julian.GregorianDate = T_DATE

    def test_01_JulianDayNumber(self):
        self.m_julian.JulianDayNumber = self.m_api._julian_day(self.m_julian)
        PrettyPrintAny(self.m_julian, 'Julian')
        self.assertEqual(self.m_julian.JulianDayNumber, T_JULIAN_DAY)

    def test_02_JulianDate(self):
        self.m_julian.JulianDayNumber = self.m_api._julian_day(self.m_julian)
        self.m_julian.JulianDate = self.m_api._julian_date(self.m_julian)
        PrettyPrintAny(self.m_julian, 'Julian')
        self.assertEqual(self.m_julian.JulianDate, T_JULIAN_DATE)

    def test_03_JulianCycle(self):
        self.m_julian.JulianDayNumber = self.m_api._julian_day(self.m_julian)
        self.m_julian.JulianDate = self.m_api._julian_date(self.m_julian)
        self.m_julian.J2KCycle = self.m_api._j2k_cycle(self.m_julian, self.m_earth)
        PrettyPrintAny(self.m_julian, 'Julian')
        self.assertEqual(self.m_julian.J2KCycle, T_J2K_CYCLE)

    def test_04_JulianTransit(self):
        self.m_julian.JulianDayNumber = self.m_api._julian_day(self.m_julian)
        self.m_julian.JulianDate = self.m_api._julian_date(self.m_julian)
        self.m_julian.J2KCycle = self.m_api._j2k_cycle(self.m_julian, self.m_earth)
        self.m_julian.J2KTransit = self.m_api._j2k_transit(self.m_julian, self.m_earth)
        PrettyPrintAny(self.m_julian, 'Julian')
        self.assertAlmostEqual(self.m_julian.J2KTransit, T_TRANSIT, 6)

    def test_21_JulianParams(self):
        l_julian = self.m_api.calculate_all_julian_dates(self.test_date_1, self.m_earth)
        PrettyPrintAny(l_julian, '0301 Julian')
        self.assertEqual(l_julian.JulianDate, T_JULIAN_DATE)
        self.assertEqual(l_julian.JulianDayNumber, T_JULIAN_DAY)

    def test_90_ConvertJulianToDateTime(self):
        l_hours = 5360.9662685
        l_ret = self.m_api._convert_julian_to_datetime(l_hours)
        print('Sunrise Convert  {0:}->{1:}'.format(l_hours, l_ret))

        l_hours = 5361.4924249
        l_ret = self.m_api._convert_julian_to_datetime(l_hours)
        print('Sunset Convert  {0:}->{1:}'.format(l_hours, l_ret))

    def test_98_JanFeb(self):
        self.assertEqual(self.m_api._is_jan_feb(datetime.date(2013, 1, 1)), 1)
        self.assertEqual(self.m_api._is_jan_feb(datetime.date(2013, 2, 1)), 1)
        self.assertEqual(self.m_api._is_jan_feb(datetime.date(2013, 3, 1)), 0)
        self.assertEqual(self.m_api._is_jan_feb(datetime.date(2013, 12, 1)), 0)


class Test_05_Sun(SetupMixin, unittest.TestCase):

    def t1(self):
        self.m_solar.EclipticLatitude = self.m_api._calc_ecliptic_latitude()

    def t2(self):
        self.m_solar.EclipticLatitude = self.m_api._calc_ecliptic_latitude()
        self.m_solar.MeanAnomaly = self.m_api._calc_mean_anomaly(self.m_julian)

    def t4(self):
        self.m_solar.EclipticLatitude = self.m_api._calc_ecliptic_latitude()
        self.m_solar.MeanAnomaly = self.m_api._calc_mean_anomaly(self.m_julian)
        self.m_solar.EquationCenter = self.m_api._calc_equation_of_center(self.m_solar)
        self.m_solar.EclipticLongitude = self.m_api._calc_ecliptic_longitude(self.m_solar)

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(xml_data.XML_LONG))
        self.m_api = sunrisesunset.API()
        self.m_earth = SetupMixin.load_earth()
        self.m_julian = JDate.calculate_all_julian_dates(self.test_date_1, self.m_earth)
        self.m_solar = sunrisesunset.SolarParameters()

    def test_01_EclipticLLatitude(self):
        self.t1()
        PrettyPrintAny(self.m_solar, 'Sun Params')
        self.assertEqual(self.m_solar.EclipticLatitude, 0.0)

    def test_02_MeanAnomaly(self):
        self.t2()
        PrettyPrintAny(self.m_solar, 'Sun Params')
        self.assertAlmostEqual(self.m_solar.MeanAnomaly * RAD2DEG, T_MEAN_ANOMALY, 6)

    def test_03_EquationOfCenter(self):
        self.t2()
        self.m_solar.EquationCenter = self.m_api._calc_equation_of_center(self.m_solar)
        PrettyPrintAny(self.m_solar, 'Sun Params')
        self.assertAlmostEqual(self.m_solar.EquationCenter * RAD2DEG, T_EQUATION_CENTER, 8)

    def test_04_EclipticLongitude(self):
        self.t4()
        PrettyPrintAny(self.m_solar, 'Sun Params')
        self.assertAlmostEqual(self.m_solar.EclipticLongitude * RAD2DEG, T_ECLIPTIC_LONGITUDE, 7)

    def test_05_Transit(self):
        self.t4()
        self.m_solar.SolarTransit = self.m_api._calc_solar_transit(self.m_julian, self.m_solar)
        print('Ecliptic Longitude: {0:}'.format(self.m_solar.SolarTransit))
        PrettyPrintAny(self.m_solar, 'Sun Params')
        self.assertAlmostEqual(self.m_solar.SolarTransit, T_TRANSIT_1, 6)

    def test_06_Iter1(self):
        self.t4()
        self.m_solar.SolarTransit = self.m_api._calc_solar_transit(self.m_julian, self.m_solar)
        self.m_solar = self.m_api._recursive_calcs(self.m_julian, self.m_solar)
        PrettyPrintAny(self.m_solar, 'Sun Params')
        self.assertAlmostEqual(self.m_solar.MeanAnomaly * RAD2DEG, T_MEAN_ANOMALY_1, 7)
        self.assertAlmostEqual(self.m_solar.EquationCenter * RAD2DEG, T_EQUATION_CENTER_1, 8)
        self.assertAlmostEqual(self.m_solar.EclipticLongitude * RAD2DEG, T_ECLIPTIC_LONGITUDE_1, 7)
        self.assertAlmostEqual(self.m_solar.SolarTransit, T_TRANSIT_1, 6)

    def test_07_Iter2(self):
        self.t4()
        self.m_solar.SolarTransit = self.m_api._calc_solar_transit(self.m_julian, self.m_solar)
        self.m_solar = self.m_api._recursive_loop(self.m_julian, self.m_solar, 2)
        PrettyPrintAny(self.m_solar, 'Sun Params')
        self.assertAlmostEqual(self.m_solar.MeanAnomaly * RAD2DEG, T_MEAN_ANOMALY_2, 7)
        self.assertAlmostEqual(self.m_solar.EquationCenter * RAD2DEG, T_EQUATION_CENTER_2, 8)
        self.assertAlmostEqual(self.m_solar.EclipticLongitude * RAD2DEG, T_ECLIPTIC_LONGITUDE_2, 7)
        self.assertAlmostEqual(self.m_solar.SolarTransit, T_TRANSIT_2, 6)

    def test_08_Iter3(self):
        self.t4()
        self.m_solar.SolarTransit = self.m_api._calc_solar_transit(self.m_julian, self.m_solar)
        self.m_solar = self.m_api._recursive_loop(self.m_julian, self.m_solar, 9)
        PrettyPrintAny(self.m_solar, 'Sun Params')
        self.assertAlmostEqual(self.m_solar.MeanAnomaly * RAD2DEG, T_MEAN_ANOMALY_3, 7)
        self.assertAlmostEqual(self.m_solar.EquationCenter * RAD2DEG, T_EQUATION_CENTER_3, 8)
        self.assertAlmostEqual(self.m_solar.EclipticLongitude * RAD2DEG, T_ECLIPTIC_LONGITUDE_3, 7)
        self.assertAlmostEqual(self.m_solar.SolarTransit, T_TRANSIT_3, 6)

    def test_09_Declination(self):
        self.t4()
        self.m_solar.SolarTransit = self.m_api._calc_solar_transit(self.m_julian, self.m_solar)
        self.m_solar = self.m_api._recursive_calcs(self.m_julian, self.m_solar)
        self.m_solar = self.m_api._recursive_calcs(self.m_julian, self.m_solar)
        self.m_solar = self.m_api._recursive_calcs(self.m_julian, self.m_solar)
        self.m_solar.SolarDeclination = self.m_api._calc_declination_of_sun(self.m_solar)
        PrettyPrintAny(self.m_solar, 'Sun Params')
        self.assertAlmostEqual(self.m_solar.SolarDeclination * RAD2DEG, 6.7471083756717, 7)

    def test_10_HourAngle(self):
        self.t4()
        self.m_solar.SolarTransit = self.m_api._calc_solar_transit(self.m_julian, self.m_solar)
        self.m_solar = self.m_api._recursive_calcs(self.m_julian, self.m_solar)
        self.m_solar = self.m_api._recursive_calcs(self.m_julian, self.m_solar)
        self.m_solar = self.m_api._recursive_calcs(self.m_julian, self.m_solar)
        self.m_solar.SolarDeclination = self.m_api._calc_declination_of_sun(self.m_solar)
        self.m_solar.SolarHourAngle = self.m_api._calc_hour_angle(self.m_earth, self.m_solar)
        PrettyPrintAny(self.m_solar, 'Sun Params')
        self.assertAlmostEqual(self.m_solar.SolarDeclination * RAD2DEG, 6.7471083756717, 7)

    def test_19_Params(self):
        l_solar = self.m_api.calcSolarNoonParams(self.m_earth, self.m_julian)
        PrettyPrintAny(l_solar, 'Solar Params')

    def test_90_RiseSet(self):
        l_ret = self.m_api.calcSolarNoonParams(self.m_earth, self.m_julian)
        PrettyPrintAny(l_ret, 'Result')

    def test_91_start(self):
        self.m_api.Start(self.m_pyhouse_obj, self.test_date_1)

    def test_94_sunrise(self):
        self.m_api.Start(self.m_pyhouse_obj, self.test_date_1)
        result = self.m_api.get_sunrise_datetime()
        print('  Sunrise: {0:}'.format(result))
        self.assertEqual(result, T_SUNRISE)

    def test_95_sunset(self):
        self.m_api.Start(self.m_pyhouse_obj, self.test_date_1)
        result = self.m_api.get_sunset_datetime()
        print('   Sunset: {0:}  {1:}'.format(result, T_SUNSET))
        self.assertEqual(result, T_SUNSET)

# ## END DBK
