"""
@name:      PyHouse/Project/src/Modules/housing/test/test_location.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2013-2019 by D. Brian Kimmel
@license:   MIT License
@note:      Created on Apr 10, 2013
@summary:   Test handling the rooms information for a house.

Passed all 13 tests - DBK - 2018-02-13

"""
from Modules.Core.data_objects import PyHouseInformation, HouseInformation
from Modules.Core.Utilities import config_tools

__updated__ = '2019-07-02'

# Import system type stuff
import sys
import xml.etree.ElementTree as ET
from twisted.trial import unittest

# Import PyMh files and modules.
from Modules.Housing import location
from Modules.Core.Utilities.json_tools import encode_json, decode_json_unicode
from test.xml_data import XML_LONG, XML_EMPTY, TESTING_PYHOUSE
from test.testing_mixin import SetupPyHouseObj
from Modules.Housing.test.xml_housing import TESTING_HOUSE_DIVISION
from Modules.Housing.location import \
    LocationInformationPrivate, \
    Api as locationApi, \
    Xml as locationXml, \
    Yaml as locationYaml
from Modules.Housing.test.xml_location import \
        TESTING_LOCATION_STREET, \
        TESTING_LOCATION_CITY, \
        TESTING_LOCATION_STATE, \
        TESTING_LOCATION_ZIP_CODE, \
        TESTING_LOCATION_PHONE, \
        TESTING_LOCATION_LATITUDE, \
        TESTING_LOCATION_LONGITUDE, \
        TESTING_LOCATION_ELEVATION, \
        TESTING_LOCATION_TIME_ZONE_NAME

from Modules.Core.Utilities.debug_tools import PrettyFormatAny


class SetupMixin:

    def setUp(self, p_root):
        self.m_pyhouse_obj = SetupPyHouseObj().BuildPyHouseObj(p_root)
        self.m_xml = SetupPyHouseObj().BuildXml(p_root)
        self.m_api = locationApi(self.m_pyhouse_obj)
        self.m_filename = 'location.yaml'


class A0(unittest.TestCase):

    def test_00_Print(self):
        print('Id: test_location')
        _x = PrettyFormatAny.form('test', 'title', 190)  # so it is defined when printing is cleaned up.


class A1_Setup(SetupMixin, unittest.TestCase):
    """
    This section tests the reading and writing of XML used by schedules.
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))

    def test_01_BuildObjects(self):
        """ Test to be sure the compound object was built correctly - Rooms is an empty dict.
        """
        # print(PrettyFormatAny.form(self.m_pyhouse_obj, 'A1-01-A - Main', 190))
        # print(PrettyFormatAny.form(self.m_pyhouse_obj.House, 'A1-02-B - House', 190))
        # print(PrettyFormatAny.form(self.m_pyhouse_obj.House.Location, 'A1-01-C - Location', 190))
        self.assertIsInstance(self.m_pyhouse_obj, PyHouseInformation)
        self.assertIsInstance(self.m_pyhouse_obj.House, HouseInformation)
        self.assertIsInstance(self.m_pyhouse_obj.House.Location, LocationInformationPrivate)


class A2_SetupXml(SetupMixin, unittest.TestCase):
    """
    This section tests the reading and writing of XML used by schedules.
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))

    def test_01_BuildObjects(self):
        """ Test to be sure the compound object was built correctly - Rooms is an empty dict.
        """
        print(PrettyFormatAny.form(self.m_pyhouse_obj._Config, 'A2-01-A - Config', 190))

    def test_02_FindXML(self):
        """ Be sure that the XML contains the right stuff.
        """
        print(PrettyFormatAny.form(self.m_xml, 'A2-02-A - Tags'))
        self.assertEqual(self.m_xml.root.tag, TESTING_PYHOUSE)
        self.assertEqual(self.m_xml.house_div.tag, TESTING_HOUSE_DIVISION)


class A3_SetupYaml(SetupMixin, unittest.TestCase):
    """
    This section tests the reading and writing of XML used by schedules.
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))
        self.m_api = locationApi(self.m_pyhouse_obj)

    def test_01_BuildObjects(self):
        """ Test to be sure the compound object was built correctly - Rooms is an empty dict.
        """
        print(PrettyFormatAny.form(self.m_pyhouse_obj._Config, 'A3-01-A - Config', 190))
        print(__file__)
        print(PrettyFormatAny.form(self.m_pyhouse_obj._Config.YamlTree, 'Location', 190))
        # self.assertEqual(self.m_pyhouse_obj._Config.YamlConfigDir, '/etc/pyhouse/')


class A3_XML(SetupMixin, unittest.TestCase):

    def _pyHouses(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))
        self.m_house_obj = LocationInformationPrivate()
        self.m_api = location.Xml()

    def setUp(self):
        self._pyHouses()

    def test_01_find_xml(self):
        """ Be sure that the XML contains the right stuff.
        """
        self.assertEqual(self.m_xml.root.tag, TESTING_PYHOUSE)
        self.assertEqual(self.m_xml.house_div.tag, TESTING_HOUSE_DIVISION)


class A4_Yaml(SetupMixin, unittest.TestCase):

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_EMPTY))

    def test_01_find_yaml(self):
        """ Be sure that the XML contains the right stuff.
        """


class B1_XmlRead(SetupMixin, unittest.TestCase):

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))
        self.m_house_obj = LocationInformationPrivate()
        self.m_api = location.Xml()

    def test_01_find_xml(self):
        """ Be sure that the XML contains the right stuff.
        """
        self.assertEqual(self.m_xml.root.tag, TESTING_PYHOUSE)
        self.assertEqual(self.m_xml.house_div.tag, TESTING_HOUSE_DIVISION)

    def test_02_ReadXml(self):
        """ Read in the xml file and fill in the location dict
        """
        l_location = locationXml().LoadXmlConfig(self.m_pyhouse_obj)
        self.assertEqual(l_location.Street, TESTING_LOCATION_STREET)
        self.assertEqual(l_location.City, TESTING_LOCATION_CITY)
        self.assertEqual(l_location.State, TESTING_LOCATION_STATE)
        self.assertEqual(l_location.ZipCode, TESTING_LOCATION_ZIP_CODE)
        # self.assertEqual(l_location.Country, TESTING_LOCATION_Countru)
        self.assertEqual(l_location.Phone, TESTING_LOCATION_PHONE)
        self.assertEqual(l_location.Latitude, float(TESTING_LOCATION_LATITUDE))
        self.assertEqual(l_location.Longitude, float(TESTING_LOCATION_LONGITUDE))
        self.assertEqual(l_location.Elevation, float(TESTING_LOCATION_ELEVATION))
        self.assertEqual(l_location.TimeZoneName, TESTING_LOCATION_TIME_ZONE_NAME)


class B2_XmlWrite(SetupMixin, unittest.TestCase):

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))
        self.m_house_obj = LocationInformationPrivate()
        self.m_api = location.Xml()

    def test_01_find_xml(self):
        """ Be sure that the XML contains the right stuff.
        """
        self.assertEqual(self.m_xml.root.tag, TESTING_PYHOUSE)
        self.assertEqual(self.m_xml.house_div.tag, TESTING_HOUSE_DIVISION)

    def test_03_WriteXml(self):
        """ Write out the XML file for the location section
        """
        _l_location = locationXml().LoadXmlConfig(self.m_pyhouse_obj)
        l_xml = locationXml().SaveXmlConfig(self.m_pyhouse_obj)
        print(PrettyFormatAny.form(l_xml, 'Location'))
        self.assertEqual(l_xml.find('Street').text, TESTING_LOCATION_STREET)
        self.assertEqual(l_xml.find('City').text, TESTING_LOCATION_CITY)
        self.assertEqual(l_xml.find('State').text, TESTING_LOCATION_STATE)
        self.assertEqual(l_xml.find('ZipCode').text, TESTING_LOCATION_ZIP_CODE)
        self.assertEqual(l_xml.find('Phone').text, TESTING_LOCATION_PHONE)
        self.assertEqual(l_xml.find('Latitude').text, TESTING_LOCATION_LATITUDE)
        self.assertEqual(l_xml.find('Longitude').text, TESTING_LOCATION_LONGITUDE)
        self.assertEqual(l_xml.find('Elevation').text, TESTING_LOCATION_ELEVATION)
        self.assertEqual(l_xml.find('TimeZoneName').text, TESTING_LOCATION_TIME_ZONE_NAME)

    def test_21_CreateJson(self):
        """ Create a JSON object for Location.
        """
        l_location = locationXml().LoadXmlConfig(self.m_pyhouse_obj)
        l_json = encode_json(l_location)
        l_obj = decode_json_unicode(l_json)
        # print(PrettyFormatAny.form(l_obj, 'JSON', 80))
        self.assertEqual(l_obj['Street'], TESTING_LOCATION_STREET)
        self.assertEqual(l_obj['City'], TESTING_LOCATION_CITY)


class C1_YamlRead(SetupMixin, unittest.TestCase):

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_EMPTY))
        self.m_yaml = locationYaml()
        self.m_working_location = self.m_pyhouse_obj.House.Location

    def test_01_ReadFile(self):
        """ Read the location.yaml config file
        """
        # print(PrettyFormatAny.form(self.m_working_location, 'C1-01-A'))
        l_node = config_tools.Yaml(self.m_pyhouse_obj).read_yaml(self.m_filename)
        # print(PrettyFormatAny.form(l_node, 'C1-01-B'))
        l_yaml = l_node.Yaml
        # print(PrettyFormatAny.form(l_yaml, 'C1-01-C'))
        l_locat = l_yaml['Location']
        # print(PrettyFormatAny.form(l_locat, 'C1-01-D'))
        self.assertEqual(l_locat['Street'], '1600 Pennsylvania Ave NW')
        self.assertEqual(len(l_locat), 10)

    def test_02_Load(self):
        """ Create a JSON object for Location.
        """
        l_node = config_tools.Yaml(self.m_pyhouse_obj).read_yaml(self.m_filename)
        l_obj = locationYaml()._update_location_from_yaml(self.m_pyhouse_obj, l_node.Yaml)
        l_ret = self.m_pyhouse_obj.House.Location
        # print(PrettyFormatAny.form(l_node, 'C1-02-A'))
        # print(PrettyFormatAny.form(l_ret, 'C1-02-B'))
        self.assertEqual(l_ret.Street, '1600 Pennsylvania Ave NW')
        self.assertEqual(l_obj.City, 'Washington')


class C2_YamlWrite(SetupMixin, unittest.TestCase):

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_EMPTY))
        self.m_yaml = locationYaml()
        self.m_working_location = self.m_pyhouse_obj.House.Location

    def test_01_Dump(self):
        """ Create a JSON object for Location.
        """
        l_node = config_tools.Yaml(self.m_pyhouse_obj).read_yaml(self.m_filename)
        l_obj = locationYaml()._update_location_from_yaml(self.m_pyhouse_obj, l_node.Yaml)
        # l_obj = LocationInformationPrivate()
        l_obj.Street = 'test street'
        _l_ret = location.Api(self.m_pyhouse_obj).LoadConfig()
        _l_ret = location.Yaml().SaveYamlConfig(self.m_pyhouse_obj)
        # print(PrettyFormatAny.form(self.m_pyhouse_obj.House.Location, 'B4-02-A - Location', 190))
        # print(PrettyFormatAny.form(self.m_pyhouse_obj.House, 'B4-02-B - House', 190))
        # print(PrettyFormatAny.form(self.m_pyhouse_obj.House.Location, 'B4-02-C - Location', 190))
        print(PrettyFormatAny.form(l_obj, 'B4-02-D - Location', 190))
        self.assertEqual(l_obj.City, 'Washington')


class S2_PyHouse(SetupMixin, unittest.TestCase):

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_EMPTY))

    def test_01_Obj(self):
        # print(PrettyFormatAny.form(self.m_pyhouse_obj, 'PyHouse_obj'))
        pass

    def test_02_House(self):
        # print(PrettyFormatAny.form(self.m_pyhouse_obj.House, 'PyHouse_obj.House'))
        pass

    def test_03_Location(self):
        # print(PrettyFormatAny.form(self.m_pyhouse_obj.House.Location, 'PyHouse_obj.House.Location'))
        pass

    def test_04_find_xml(self):
        """ Be sure that the XML contains the right stuff.
        """
        _l_location = locationXml().LoadXmlConfig(self.m_pyhouse_obj)
        # print(PrettyFormatAny.form(l_location, 'Location'))
        pass

# ## END DBK
