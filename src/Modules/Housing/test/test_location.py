"""
@name:      PyHouse/src/Modules/housing/test/test_location.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2013-2016 by D. Brian Kimmel
@license:   MIT License
@note:      Created on Apr 10, 2013
@summary:   Test handling the rooms information for a house.

Passed all 12 tests - DBK - 2016-06-24
"""

# Import system type stuff
import xml.etree.ElementTree as ET
from twisted.trial import unittest

# Import PyMh files and modules.
from Modules.Core.data_objects import LocationData
from Modules.Housing import location
from Modules.Utilities.json_tools import encode_json, decode_json_unicode
from test.xml_data import XML_LONG, XML_EMPTY
from test.testing_mixin import SetupPyHouseObj
from Modules.Housing.test.xml_location import \
        TESTING_LOCATION_STREET, \
        TESTING_LOCATION_CITY, \
        TESTING_LOCATION_ZIP_CODE, \
        TESTING_LOCATION_PHONE, \
        TESTING_LOCATION_LATITUDE, \
        TESTING_LOCATION_LONGITUDE, \
        TESTING_LOCATION_STATE, \
        TESTING_LOCATION_TIME_ZONE_NAME, \
        TESTING_LOCATION_ELEVATION, \
        TESTING_LOCATION_REGION
from Modules.Utilities.debug_tools import PrettyFormatAny


class SetupMixin(object):

    def setUp(self, p_root):
        self.m_pyhouse_obj = SetupPyHouseObj().BuildPyHouseObj(p_root)
        self.m_xml = SetupPyHouseObj().BuildXml(p_root)

    def setUpObj(self, p_root):
        self.m_pyhouse_obj = SetupPyHouseObj().BuildPyHouseObj(p_root)

    def setUpXml(self, p_root):
        self.m_xml = SetupPyHouseObj().BuildXml(p_root)


class A1_XML(SetupMixin, unittest.TestCase):

    def _pyHouses(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))
        self.m_house_obj = LocationData()
        self.m_api = location.Xml()

    def setUp(self):
        self._pyHouses()

    def test_01_find_xml(self):
        """ Be sure that the XML contains the right stuff.
        """
        self.assertEqual(self.m_xml.root.tag, 'PyHouse', 'Invalid XML - not a PyHouse XML config file')
        self.assertEqual(self.m_xml.house_div.tag, 'HouseDivision', 'XML - No Houses Division')

    def test_02_ReadXml(self):
        """ Read in the xml file and fill in the location dict
        """
        l_location = self.m_api.read_location_xml(self.m_pyhouse_obj)
        self.assertEqual(l_location.Street, TESTING_LOCATION_STREET)
        self.assertEqual(l_location.City, TESTING_LOCATION_CITY)
        self.assertEqual(l_location.State, TESTING_LOCATION_STATE)
        self.assertEqual(l_location.ZipCode, TESTING_LOCATION_ZIP_CODE)
        self.assertEqual(l_location.Region, TESTING_LOCATION_REGION)
        self.assertEqual(l_location.Phone, TESTING_LOCATION_PHONE)
        self.assertEqual(l_location.Latitude, float(TESTING_LOCATION_LATITUDE))
        self.assertEqual(l_location.Longitude, float(TESTING_LOCATION_LONGITUDE))
        self.assertEqual(l_location.Elevation, float(TESTING_LOCATION_ELEVATION))
        self.assertEqual(l_location.TimeZoneName, TESTING_LOCATION_TIME_ZONE_NAME)

    def test_03_WriteXml(self):
        """ Write out the XML file for the location section
        """
        l_location = self.m_api.read_location_xml(self.m_pyhouse_obj)
        l_xml = self.m_api.write_location_xml(l_location)
        # print(PrettyFormatAny.form(l_xml, 'Location'))
        self.assertEqual(l_xml.find('Street').text, TESTING_LOCATION_STREET)
        self.assertEqual(l_xml.find('City').text, TESTING_LOCATION_CITY)
        self.assertEqual(l_xml.find('State').text, TESTING_LOCATION_STATE)
        self.assertEqual(l_xml.find('ZipCode').text, TESTING_LOCATION_ZIP_CODE)
        self.assertEqual(l_xml.find('Region').text, TESTING_LOCATION_REGION)
        self.assertEqual(l_xml.find('Phone').text, TESTING_LOCATION_PHONE)
        self.assertEqual(l_xml.find('Latitude').text, TESTING_LOCATION_LATITUDE)
        self.assertEqual(l_xml.find('Longitude').text, TESTING_LOCATION_LONGITUDE)
        self.assertEqual(l_xml.find('Elevation').text, TESTING_LOCATION_ELEVATION)
        self.assertEqual(l_xml.find('TimeZoneName').text, TESTING_LOCATION_TIME_ZONE_NAME)

    def test_21_CreateJson(self):
        """ Create a JSON object for Location.
        """
        l_location = self.m_api.read_location_xml(self.m_pyhouse_obj)
        l_json = encode_json(l_location)
        l_obj = decode_json_unicode(l_json)
        # print(PrettyFormatAny.form(l_obj, 'JSON', 80))
        self.assertEqual(l_obj['Street'], TESTING_LOCATION_STREET)
        self.assertEqual(l_obj['City'], TESTING_LOCATION_CITY)


class S1_PyHouse(SetupMixin, unittest.TestCase):

    def setUp(self):
        SetupMixin.setUpObj(self, ET.fromstring(XML_EMPTY))

    def test_01_Obj(self):
        print(PrettyFormatAny.form(self.m_pyhouse_obj, 'PyHouse_obj'))

    def test_02_House(self):
        print(PrettyFormatAny.form(self.m_pyhouse_obj.House, 'PyHouse_obj.House'))

    def test_03_Location(self):
        print(PrettyFormatAny.form(self.m_pyhouse_obj.House.Location, 'PyHouse_obj.House.Location'))

    def test_04_find_xml(self):
        """ Be sure that the XML contains the right stuff.
        """
        l_location = location.Xml().read_location_xml(self.m_pyhouse_obj)
        print(PrettyFormatAny.form(l_location, 'Location'))


class S2_PyHouse(SetupMixin, unittest.TestCase):

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_EMPTY))

    def test_01_Obj(self):
        print(PrettyFormatAny.form(self.m_pyhouse_obj, 'PyHouse_obj'))

    def test_02_House(self):
        print(PrettyFormatAny.form(self.m_pyhouse_obj.House, 'PyHouse_obj.House'))

    def test_03_Location(self):
        print(PrettyFormatAny.form(self.m_pyhouse_obj.House.Location, 'PyHouse_obj.House.Location'))

    def test_04_find_xml(self):
        """ Be sure that the XML contains the right stuff.
        """
        l_location = location.Xml().read_location_xml(self.m_pyhouse_obj)
        print(PrettyFormatAny.form(l_location, 'Location'))

# ## END DBK
