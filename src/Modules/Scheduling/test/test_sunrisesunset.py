"""
@name:      PyHouse/src/Modules/scheduling/sunrisesunset.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2011-2015 by D. Brian Kimmel
@note:      Created on Mar 6, 2011
@license:   MIT License
@summary:   Calculate the suns location at local noon, then calculate sunrise and sunset for the day.

http://en.wikipedia.org/wiki/Sunrise_equation

http://users.electromagnetic.net/bu/astro/iyf-calc.php?lat=28.938464&long=82.51720
"""


# Import system type stuff
import datetime
import xml.etree.ElementTree as ET
from twisted.trial import unittest
from math import pi

# Import PyMh files
from Modules.Scheduling import sunrisesunset
from Modules.Scheduling.sunrisesunset import JDate, JulianParameters, JDATE2000

from test.testing_mixin import SetupPyHouseObj
from test import xml_data
from Modules.Utilities.tools import PrettyPrintAny

# Conversion constants.
RAD2DEG = 180.0 / pi
DEG2RAD = pi / 180.0

"""
        <LocationSection>
            <Street>5191 N Pink Poppy Dr</Street>
            <City>Beverly Hills</City>
            <State>Florida</State>
            <ZipCode>34465</ZipCode>
            <Phone>(352) 270-8096</Phone>
            <Latitude>28.938448</Latitude>
            <Longitude>-82.517208</Longitude>
            <TimeZoneName>America/New_York</TimeZoneName>
        </LocationSection>

"""

# All Tests - Location Information
T_LATITUDE = 19.925567
T_LONGITUDE = -155.867248
T_TIMEZONE_NAME = 'Pacific/Honolulu'
T_TIMEZONE_OFFSET = '-10:00'
T_DAYLIGHT_SAVINGS_TIME = '-10:00'
T_TZ = sunrisesunset.LocationTz()

T_DATE = datetime.date(2015, 4, 7)
T_JULIAN_DAY = JDATE2000 + 5575
T_JULIAN_DATE = (JDATE2000 - 0.5) + 5575
T_J2K_CYCLE = 5575.0
T_J2K_TRANSIT = 5575.4338646



T_MEAN_ANOMALY = 92.678278049237
T_EQUATION_CENTER = -1.6669235826461
T_ECLIPTIC_LONGITUDE = 162.82927835795
T_TRANSIT = 5574.7786501  # 2457093.7786501

T_MEAN_ANOMALY_1 = 66.400026917619
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
T_DECLINATION = 6.7471083756717
T_HOUR_ANGLE = 94.708153427328

# Test time 1
T_SUNRISE = datetime.datetime(2015, 3, 12, 7, 45, 15, 0, tzinfo = T_TZ)
T_SUNSET = datetime.datetime(2015, 3, 12, 19, 37, 15, 0, tzinfo = T_TZ)

T_DECLINATION = -3.5244685811301
T_HOUR_ANGLE = 88.998972939736


class SetupMixin(object):
    """
    """

    def setUp(self, p_root):
        self.m_pyhouse_obj = SetupPyHouseObj().BuildPyHouseObj(p_root)
        self.m_xml = SetupPyHouseObj().BuildXml(p_root)
        self.test_date_1 = T_DATE

    @staticmethod
    def load_earth(p_pyhouse_obj):
        l_loc = sunrisesunset.EarthParameters()
        l_loc.Latitude = T_LATITUDE
        l_loc.Longitude = T_LONGITUDE
        l_loc.TimeZoneName = T_TIMEZONE_NAME
        l_loc.TimeZoneOffset = T_TIMEZONE_OFFSET
        l_loc.DaylightSavingsTime = T_DAYLIGHT_SAVINGS_TIME
        p_pyhouse_obj.House.RefOBJs.Location.Latitude = T_LATITUDE
        p_pyhouse_obj.House.RefOBJs.Location.Longitude = T_LONGITUDE
        return l_loc



class A01_Utility(SetupMixin, unittest.TestCase):
    """
    Be sure all our conversion routines work.
    Test positive and negative conversions
    """

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



class A02_Time(SetupMixin, unittest.TestCase):
    """Testing time and timezone
    The user inputs a valid timezone and the web interface fills in the internal values
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(xml_data.XML_LONG))
        self.m_api = sunrisesunset.API()

    def test_01_TZ(self):
        pass



class E01_Results(SetupMixin, unittest.TestCase):
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
        self.m_earth = self.m_api._load_location(self.m_pyhouse_obj, T_DATE)
        l_result = self.m_api.get_sunrise_datetime()
        print('Sunrise for date {};  Calc: {};  S/B: {}'.format(T_DATE, l_result, T_SUNRISE))
        PrettyPrintAny(self.m_earth, 'T_01, t_01, Params')
        self.assertEqual(l_result, T_SUNRISE)

    def test_02_Sunset(self):
        """
        Given a date, we should get a correct sunset datetime
        """
        self.m_api.Start(self.m_pyhouse_obj, T_DATE)
        l_result = self.m_api.get_sunset_datetime()
        print('Sunset for date {};  Calc: {};  S/B: {}'.format(T_DATE, l_result, T_SUNSET))
        self.assertEqual(l_result, T_SUNSET)


class C01_ObserverEarth(SetupMixin, unittest.TestCase):
    """Be sure all location dependant items are correct.
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(xml_data.XML_LONG))
        self.m_earth = SetupMixin.load_earth(self.m_pyhouse_obj)
        self.m_api = sunrisesunset.API()

    def test_01_Location(self):
        l_location = self.m_api._load_location(self.m_pyhouse_obj, T_DATE)
        PrettyPrintAny(l_location, 'Location')
        self.assertEqual(l_location.Latitude, T_LATITUDE)
        self.assertEqual(l_location.Longitude, T_LONGITUDE)

    def test_02_TzParams(self):
        l_tz, l_x = self.m_api._get_tz_params(self.m_earth, T_DATE)
        l_ret = l_tz
        PrettyPrintAny(l_ret, 'Misc')
        PrettyPrintAny(l_tz, 'TZ')
        PrettyPrintAny(l_x, 'rAW')


class C02_Julian(SetupMixin, unittest.TestCase):
    """ Test all the calculations of the Julian Date are correct.
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(xml_data.XML_LONG))
        self.m_pyhouse_obj.House.RefOBJs.Location.Latitude = T_LATITUDE
        self.m_api = JDate
        self.m_earth = SetupMixin.load_earth(self.m_pyhouse_obj)
        self.m_julian = JulianParameters
        self.m_julian.GregorianDate = T_DATE

    def test_01_JanFeb(self):
        self.assertEqual(self.m_api._is_jan_feb(datetime.date(2013, 1, 1)), 1)
        self.assertEqual(self.m_api._is_jan_feb(datetime.date(2013, 2, 1)), 1)
        self.assertEqual(self.m_api._is_jan_feb(datetime.date(2013, 3, 1)), 0)
        self.assertEqual(self.m_api._is_jan_feb(datetime.date(2013, 12, 1)), 0)

    def test_02_JulianDayNumber(self):
        """ This is the int number of days since Jan 0, 4713 BCE.
        """
        self.m_julian.JulianDayNumber = self.m_api._julian_day(self.m_julian)
        PrettyPrintAny(self.m_julian, 'Julian')
        self.assertEqual(self.m_julian.JulianDayNumber, T_JULIAN_DAY)

    def test_03_JulianDate(self):
        """
        The astronomical julian date starts at Noon, Jan 1st 4713 BCE
        This is a floating point number 1/2 day less than the julian day
        """
        self.m_julian.JulianDayNumber = self.m_api._julian_day(self.m_julian)
        self.m_julian.JulianDate = self.m_api._julian_date(self.m_julian)
        PrettyPrintAny(self.m_julian, 'Julian')
        self.assertEqual(self.m_julian.JulianDate, T_JULIAN_DATE)

    def test_04_JulianCycle(self):
        """
        The Julian cycle since Jan 1st, 2000.
        """
        self.m_julian.JulianDayNumber = self.m_api._julian_day(self.m_julian)
        self.m_julian.JulianDate = self.m_api._julian_date(self.m_julian)
        self.m_julian.J2KCycle = self.m_api._j2k_cycle(self.m_julian, self.m_earth)
        PrettyPrintAny(self.m_julian, 'Julian')
        self.assertEqual(self.m_julian.J2KCycle, T_J2K_CYCLE)

    def test_05_JulianTransit(self):
        self.m_julian.JulianDayNumber = self.m_api._julian_day(self.m_julian)
        self.m_julian.JulianDate = self.m_api._julian_date(self.m_julian)
        self.m_julian.J2KCycle = self.m_api._j2k_cycle(self.m_julian, self.m_earth)
        self.m_julian.J2KTransit = self.m_api._j2k_transit(self.m_julian, self.m_earth)
        PrettyPrintAny(self.m_julian, 'Julian')
        self.assertAlmostEqual(self.m_julian.J2KTransit, T_J2K_TRANSIT, 6)

    def test_06_JulianParams(self):
        l_julian = self.m_api.calculate_all_julian_dates(self.test_date_1, self.m_earth)
        PrettyPrintAny(l_julian, 'Julian Parameters')
        self.assertEqual(l_julian.JulianDate, T_JULIAN_DATE)
        self.assertEqual(l_julian.JulianDayNumber, T_JULIAN_DAY)

    def test_07_ConvertJulianToDateTime(self):
        l_hours = 5360.9662685
        l_ret = self.m_api._convert_julian_to_datetime(l_hours)
        print('Sunrise Convert  {0:}->{1:}'.format(l_hours, l_ret))

        l_hours = 5361.4924249
        l_ret = self.m_api._convert_julian_to_datetime(l_hours)
        print('Sunset Convert  {0:}->{1:}'.format(l_hours, l_ret))


class D01_Sun(SetupMixin, unittest.TestCase):

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(xml_data.XML_LONG))
        self.m_api = sunrisesunset.API()
        self.m_earth = SetupMixin.load_earth(self.m_pyhouse_obj)
        self.m_julian = JDate.calculate_all_julian_dates(self.test_date_1, self.m_earth)
        self.m_solar = sunrisesunset.SolarParameters()
        self.m_solar.EclipticLatitude = self.m_api._calc_ecliptic_latitude()
        self.m_solar.MeanAnomaly = self.m_api._calc_mean_anomaly(self.m_julian, self.m_solar)
        self.m_solar.EquationCenter = self.m_api._calc_equation_of_center(self.m_solar)
        self.m_solar.EclipticLongitude = self.m_api._calc_ecliptic_longitude(self.m_solar)
        self.m_solar.SolarTransit = self.m_api._calc_solar_transit(self.m_julian, self.m_solar)

    def test_01_EclipticLLatitude(self):
        PrettyPrintAny(self.m_solar, 'Sun Parameters')
        PrettyPrintAny(self.m_earth, 'Earth Parameters')
        PrettyPrintAny(self.m_julian, 'Date Parameters')
        self.assertEqual(self.m_solar.EclipticLatitude, 0.0)

    def test_02_MeanAnomaly(self):
        print('Mean Anomaly: {}'.format(self.m_solar.MeanAnomaly * RAD2DEG))
        PrettyPrintAny(self.m_solar, 'Sun Parameters')
        PrettyPrintAny(self.m_julian, 'Date Parameters')
        self.assertAlmostEqual(self.m_solar.MeanAnomaly * RAD2DEG, T_MEAN_ANOMALY, 6)

    def test_03_EquationOfCenter(self):
        self.m_solar.EquationCenter = self.m_api._calc_equation_of_center(self.m_solar)
        print('Mean Anomaly: {}'.format(self.m_solar.MeanAnomaly * RAD2DEG))
        print('Equation of Center: {}'.format(self.m_solar.EquationCenter * RAD2DEG))
        PrettyPrintAny(self.m_solar, 'Sun Parameters')
        self.assertAlmostEqual(self.m_solar.EquationCenter * RAD2DEG, T_EQUATION_CENTER, 8)

    def test_04_EclipticLongitude(self):
        print('Mean Anomaly: {}'.format(self.m_solar.MeanAnomaly * RAD2DEG))
        print('Equation of Center: {}'.format(self.m_solar.EquationCenter * RAD2DEG))
        print('Ecliptic Longitude: {}'.format(self.m_solar.EclipticLongitude * RAD2DEG))
        PrettyPrintAny(self.m_solar, 'Sun Parameters')
        self.assertAlmostEqual(self.m_solar.EclipticLongitude * RAD2DEG, T_ECLIPTIC_LONGITUDE, 7)

    def test_05_Transit(self):
        print('Mean Anomaly: {}'.format(self.m_solar.MeanAnomaly * RAD2DEG))
        print('Equation of Center: {}'.format(self.m_solar.EquationCenter * RAD2DEG))
        print('Ecliptic Longitude: {}'.format(self.m_solar.EclipticLongitude * RAD2DEG))
        print('Solar Transit: {}'.format(self.m_solar.SolarTransit))
        PrettyPrintAny(self.m_solar, 'Sun Parameters')
        PrettyPrintAny(self.m_julian, 'Julian Parameters')
        self.assertAlmostEqual(self.m_solar.SolarTransit, T_TRANSIT, 6)

    def test_06_Iter1(self):
        l_solar = self.m_api._calc_initial_solar_params(self.m_julian)
        l_solar = self.m_api._recursive_calcs(self.m_julian, l_solar)
        print('Mean Anomaly: {}'.format(l_solar.MeanAnomaly * RAD2DEG))
        print('Equation of Center: {}'.format(l_solar.EquationCenter * RAD2DEG))
        print('Ecliptic Longitude: {}'.format(l_solar.EclipticLongitude * RAD2DEG))
        print('Solar Transit: {}'.format(l_solar.SolarTransit))
        PrettyPrintAny(l_solar, 'Sun Parameters 1')
        PrettyPrintAny(l_solar, 'Sun Parameters 2')
        self.assertAlmostEqual(l_solar.MeanAnomaly * RAD2DEG, T_MEAN_ANOMALY_1, 7)
        self.assertAlmostEqual(l_solar.EquationCenter * RAD2DEG, T_EQUATION_CENTER_1, 8)
        self.assertAlmostEqual(l_solar.EclipticLongitude * RAD2DEG, T_ECLIPTIC_LONGITUDE_1, 7)
        self.assertAlmostEqual(l_solar.SolarTransit, T_TRANSIT_1, 4)

    def test_07_Iter2(self):
        l_solar = self.m_api._calc_initial_solar_params(self.m_julian)
        l_solar = self.m_api._recursive_loop(self.m_julian, l_solar, 2)
        print('Mean Anomaly: {}'.format(l_solar.MeanAnomaly * RAD2DEG))
        print('Equation of Center: {}'.format(l_solar.EquationCenter * RAD2DEG))
        print('Ecliptic Longitude: {}'.format(l_solar.EclipticLongitude * RAD2DEG))
        print('Solar Transit: {}'.format(l_solar.SolarTransit))
        PrettyPrintAny(l_solar, 'Sun Params')
        self.assertAlmostEqual(l_solar.MeanAnomaly * RAD2DEG, T_MEAN_ANOMALY_2, 7)
        self.assertAlmostEqual(l_solar.EquationCenter * RAD2DEG, T_EQUATION_CENTER_2, 8)
        self.assertAlmostEqual(l_solar.EclipticLongitude * RAD2DEG, T_ECLIPTIC_LONGITUDE_2, 7)
        self.assertAlmostEqual(l_solar.SolarTransit, T_TRANSIT_2, 6)

    def test_08_Iter3(self):
        self.m_solar.SolarTransit = self.m_api._calc_solar_transit(self.m_julian, self.m_solar)
        self.m_solar = self.m_api._recursive_loop(self.m_julian, self.m_solar, 9)
        print('Mean Anomaly: {}'.format(self.m_solar.MeanAnomaly * RAD2DEG))
        print('Equation of Center: {}'.format(self.m_solar.EquationCenter * RAD2DEG))
        print('Ecliptic Longitude: {}'.format(self.m_solar.EclipticLongitude * RAD2DEG))
        print('Solar Transit: {}'.format(self.m_solar.SolarTransit))
        PrettyPrintAny(self.m_solar, 'Sun Params')
        self.assertAlmostEqual(self.m_solar.MeanAnomaly * RAD2DEG, T_MEAN_ANOMALY_3, 7)
        self.assertAlmostEqual(self.m_solar.EquationCenter * RAD2DEG, T_EQUATION_CENTER_3, 8)
        self.assertAlmostEqual(self.m_solar.EclipticLongitude * RAD2DEG, T_ECLIPTIC_LONGITUDE_3, 7)
        self.assertAlmostEqual(self.m_solar.SolarTransit, T_TRANSIT_3, 6)

    def test_09_Declination(self):
        self.m_solar.SolarTransit = self.m_api._calc_solar_transit(self.m_julian, self.m_solar)
        self.m_solar = self.m_api._recursive_calcs(self.m_julian, self.m_solar)
        self.m_solar = self.m_api._recursive_calcs(self.m_julian, self.m_solar)
        self.m_solar = self.m_api._recursive_calcs(self.m_julian, self.m_solar)
        self.m_solar.SolarDeclination = self.m_api._calc_declination_of_sun(self.m_solar)
        print('Mean Anomaly: {}'.format(self.m_solar.MeanAnomaly * RAD2DEG))
        print('Equation of Center: {}'.format(self.m_solar.EquationCenter * RAD2DEG))
        print('Ecliptic Longitude: {}'.format(self.m_solar.EclipticLongitude * RAD2DEG))
        print('Solar Transit: {}'.format(self.m_solar.SolarTransit))
        PrettyPrintAny(self.m_solar, 'Sun Params')
        self.assertAlmostEqual(self.m_solar.SolarDeclination * RAD2DEG, T_DECLINATION, 7)

    def test_10_HourAngle(self):
        self.m_solar.SolarTransit = self.m_api._calc_solar_transit(self.m_julian, self.m_solar)
        self.m_solar = self.m_api._recursive_calcs(self.m_julian, self.m_solar)
        self.m_solar = self.m_api._recursive_calcs(self.m_julian, self.m_solar)
        self.m_solar = self.m_api._recursive_calcs(self.m_julian, self.m_solar)
        self.m_solar.SolarDeclination = self.m_api._calc_declination_of_sun(self.m_solar)
        self.m_solar.SolarHourAngle = self.m_api._calc_hour_angle(self.m_earth, self.m_solar)
        PrettyPrintAny(self.m_solar, 'Sun Params')
        self.assertAlmostEqual(self.m_solar.SolarHourAngle * RAD2DEG, T_HOUR_ANGLE, 7)

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
