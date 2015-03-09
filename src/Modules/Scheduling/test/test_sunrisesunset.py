"""
@name: PyHouse/src/Modules/scheduling/sunrisesunset.py
@author: D. Brian Kimmel
@contact: <d.briankimmel@gmail.com
@copyright: 2011-2014 by D. Brian Kimmel
@note: Created on Mar 6, 2011
@license: MIT License
@summary: Calculate the suns location at local noon, then calculate sunrise and sunset for the day.

"""

# Import system type stuff
import datetime
import xml.etree.ElementTree as ET
from twisted.trial import unittest

# Import PyMh files
from Modules.Core.data_objects import PyHouseData, HouseObjs, LocationData
from Modules.scheduling import sunrisesunset
from test.testing_mixin import SetupPyHouseObj
from test import xml_data
from Modules.utils.tools import PrettyPrintAny


class SetupMixin(object):
    """
    """

    def setUp(self, p_root):
        self.m_pyhouse_obj = SetupPyHouseObj().BuildPyHouseObj(p_root)
        self.m_xml = SetupPyHouseObj().BuildXml(p_root)


class LocationObj():

    def __init__(self):
        self.Latitude = 28.938448
        self.Longitude = -82.517208
        self.TimeZone = '-5:00'
        self.SavingTime = '-4:00'


class Test_02_XML(SetupMixin, unittest.TestCase):

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(xml_data.XML_LONG))
        self.m_api = sunrisesunset.API()

    def test_0201_buildObjects(self):
        """ Test to be sure the compound object was built correctly - Rooms is an empty dict.
        """
        self.assertEqual(self.m_pyhouse_obj.House.OBJs.Rooms, {}, 'No Rooms{}')
        PrettyPrintAny(self.m_pyhouse_obj.House.OBJs, 'OBJs', 120)

    def test_0202_find_xml(self):
        """ Be sure that the XML contains the right stuff.
        """
        self.assertEqual(self.m_xml.root.tag, 'PyHouse', 'Invalid XML - not a PyHouse XML config file')
        self.assertEqual(self.m_xml.house_div.tag, 'HouseDivision', 'XML - No House section')
        self.assertEqual(self.m_xml.location_sect.tag, 'LocationSection', 'XML - No Location section')
        PrettyPrintAny(self.m_xml, 'All Xml', 120)

class Test_03(SetupMixin, unittest.TestCase):

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(xml_data.XML_LONG))
        self.Latitude = 28.938448
        self.Longitude = -82.517208
        self.TimeZone = '-5:00'
        self.SavingTime = '-4:00'
        self.m_pyhouse_obj.House.OBJs.Location.Latitude = 28.938448
        self.m_api = sunrisesunset.API()
        self.m_loc = self.m_api._load_location(self.m_pyhouse_obj)
        self.date_2013_06_06 = datetime.date(2013, 6, 6)
        self.sunrise = datetime.time(6, 32, 36)  # 06:31:06
        self.sunset = datetime.time(20, 27, 32)  # 20:26:41


    def test_0301_Location(self):
        l_location = self.m_api._load_location(self.m_pyhouse_obj)
        PrettyPrintAny(l_location, 'Location', 120)
        self.assertEqual(l_location.Latitude, 28.938448)


    def test_0311_JanFeb(self):
        self.assertEqual(self.m_api._is_jan_feb(datetime.date(2013, 1, 1)), 1)
        self.assertEqual(self.m_api._is_jan_feb(datetime.date(2013, 2, 1)), 1)
        self.assertEqual(self.m_api._is_jan_feb(datetime.date(2013, 3, 1)), 0)
        self.assertEqual(self.m_api._is_jan_feb(datetime.date(2013, 12, 1)), 0)

    def test_0312_JulianDay(self):
        l_day = self.m_api._calculate_julian_day(self.date_2013_06_06)
        print l_day
        self.assertEqual(l_day, 2456450)

    def test_0313_JulianDate(self):
        l_day = self.m_api._calculate_julian_date(self.date_2013_06_06)
        print l_day
        self.assertEqual(l_day, 2456449.5)

    def test_0319_Julian(self):
        l_julian = self.m_api._calculate_all_julian_dates(self.date_2013_06_06, self.m_loc)
        PrettyPrintAny(l_julian, '0301 Julian', 120)
        self.assertEqual(l_julian.JulianDate, 2456449.500000)


    def test_0350_SolarEL(self):
        l_elong = self.m_api._calc_ecliptic_latitude()
        print('Ecliptic Longitude {0:}'.format(l_elong))
        self.assertEqual(l_elong, 0.0)

    def test_0351_SolarMA(self):
        l_loc = self.m_api._load_location(self.m_pyhouse_obj)
        l_jul = self.m_api._calculate_all_julian_dates(self.date_2013_06_06, l_loc)
        pass

    def test_0359_Solar(self):
        self.m_api._calculate_solar_params()
        pass


    def test_0390_SS(self):
        l_loc = self.m_api._load_location(self.m_pyhouse_obj)
        l_jul = self.m_api._calculate_all_julian_dates(self.date_2013_06_06, l_loc)
        l_sol = self.m_api._calculate_solar_params()
        l_ret = self.m_api._calcSolarNoonParams(l_loc, l_sol, l_jul)
        PrettyPrintAny(l_ret, 'Result', 120)

    def test_0391_start(self):
        self.m_api.Start(self.m_pyhouse_obj, self.date_2013_06_06)

    def test_0394_sunrise(self):
        self.m_api.Start(self.m_pyhouse_obj, self.date_2013_06_06)
        result = self.m_api.get_sunrise()
        print('  Sunrise: {0:}  {1:}'.format(result, self.sunrise))
        self.assertEqual(result, self.sunrise)

    def test_0395_sunset(self):
        self.m_api.Start(self.m_pyhouse_obj, self.date_2013_06_06)
        result = self.m_api.get_sunset()
        print('   Sunset: {0:}  {1:}'.format(result, self.sunset))
        self.assertEqual(result, self.sunset)

# ## END DBK
