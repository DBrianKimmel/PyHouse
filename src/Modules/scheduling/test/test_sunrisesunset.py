"""
@name: PyHouse/src/Modules/scheduling/sunrisesunset.py
@author: D. Brian Kimmel
@contact: <d.briankimmel@gmail.com
@copyright: 2011-2014 by D. Brian Kimmel
@note: Created on Mar 6, 2011
@license: MIT License
@summary: Calculate the suns location at local noon, then calculate sunrise and sunset for the day.

Created on Apr 7, 2013

@author: briank
"""

# Import system type stuff
import datetime
import xml.etree.ElementTree as ET
from twisted.trial import unittest

# Import PyMh files
from Modules.Core.data_objects import PyHousesData, HouseData, LocationData
from Modules.scheduling import sunrisesunset
from src.test import xml_data


class LocationObj():

    def __init__(self):
        self.Latitude = 28.938448
        self.Longitude = -82.517208
        self.TimeZone = '-5:00'
        self.SavingTime = '-4:00'


class Test_02_XML(unittest.TestCase):

    def setUp(self):
        self.m_pyhouses_obj = PyHousesData()
        self.m_pyhouses_obj.HouseData = HouseData()
        self.m_pyhouses_obj.XmlRoot = self.m_root_xml = ET.fromstring(xml_data.XML_LONG)
        self.m_houses_xml = self.m_root_xml.find('Houses')
        self.m_house_xml = self.m_houses_xml.find('House')  # First house
        self.m_location_xml = self.m_house_xml.find('Location')
        self.m_api = sunrisesunset.API()

    def test_0201_buildObjects(self):
        """ Test to be sure the compound object was built correctly - Rooms is an empty dict.
        """
        self.assertEqual(self.m_pyhouses_obj.HouseData.Rooms, {}, 'No Rooms{}')

    def test_0202_find_xml(self):
        """ Be sure that the XML contains the right stuff.
        """
        self.assertEqual(self.m_root_xml.tag, 'PyHouse', 'Invalid XML - not a PyHouse XML config file')
        self.assertEqual(self.m_houses_xml.tag, 'Houses', 'XML - No Houses section')
        self.assertEqual(self.m_house_xml.tag, 'House', 'XML - No House section')
        self.assertEqual(self.m_location_xml.tag, 'Location', 'XML - No Location section')

class Test_03(unittest.TestCase):

    def setUp(self):
        self.m_pyhouses_obj = PyHousesData()
        self.m_house_obj = HouseData()
        self.m_house_obj.Name = 'Test House (Pink Poppy)'
        self.m_house_obj.Location = LocationData()
        self.m_house_obj.Latitude = 28.938448
        self.m_house_obj.Longitude = -82.517208
        self.m_house_obj.TimeZone = '-5:00'
        self.m_house_obj.SavingTime = '-4:00'
        self.m_pyhouses_obj.HouseData = HouseData()
        self.m_pyhouses_obj.XmlRoot = self.m_root_xml = ET.fromstring(xml_data.XML_LONG)
        self.m_houses_xml = self.m_root_xml.find('Houses')
        self.m_house_xml = self.m_houses_xml.find('House')  # First house
        self.m_location_xml = self.m_house_xml.find('Location')
        self.m_api = sunrisesunset.API()
        # Pink Poppy Fall
        # self.now = datetime.date(2013, 11, 22)
        # self.sunrise = datetime.time(7, 00, 41)
        # self.sunset = datetime.time(17, 34, 52)
        # Pink Poppy Summer
        self.now = datetime.date(2013, 6, 6)
        self.sunrise = datetime.time(6, 32, 30)
        self.sunset = datetime.time(20, 27, 59)


    def test_0302_start(self):
        self.m_api.Start(self.m_pyhouses_obj, self.m_house_obj)

    def test_0310_julian(self):
        self.m_api.Start(self.m_pyhouses_obj, self.m_house_obj, self.now)
        l_j2000 = self.m_api.earth_data.J2000
        self.assertEqual(l_j2000, 4905.499100000132)

    def test_0331_sunrise(self):
        self.m_api.Start(self.m_pyhouses_obj, self.m_house_obj, self.now)
        result = self.m_api.get_sunrise()
        print('  Sunrise: {0:}  {1:}'.format(result, self.sunrise))
        self.assertEqual(result, self.sunrise)

    def test_0332_sunset(self):
        self.m_api.Start(self.m_pyhouses_obj, self.m_house_obj, self.now)
        result = self.m_api.get_sunset()
        print('   Sunset: {0:}  {1:}'.format(result, self.sunset))
        self.assertEqual(result, self.sunset)

# ## END DBK
