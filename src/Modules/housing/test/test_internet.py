"""
@name: PyHouse/src/housing/test/test_internet.py
@author: D. Brian Kimmel
@contact: <d.briankimmel@gmail.com
@Copyright (c) 2013-2014 by D. Brian Kimmel
@license: MIT License
@note: Created on Apr 8, 2013
@summary: Test handling the internet information for a house.

"""

# Import system type stuff
import xml.etree.ElementTree as ET
from twisted.trial import unittest

# Import PyMh files
from Modules.Core.data_objects import PyHousesData, HousesData, HouseData, InternetConnectionData, InternetConnectionDynDnsData
from Modules.housing import internet
from Modules.web import web_utils
from Modules.utils.xml_tools import prettify
from src.test import xml_data


class Test_02_XML(unittest.TestCase):

    def setUp(self):
        self.m_pyhouses_obj = PyHousesData()
        self.m_pyhouses_obj.HousesData[0] = HousesData()
        self.m_pyhouses_obj.HousesData[0].HouseObject = HouseData()
        self.m_pyhouses_obj.XmlRoot = self.m_root_xml = ET.fromstring(xml_data.XML_LONG)
        self.m_houses_xml = self.m_root_xml.find('Houses')
        self.m_house_xml = self.m_houses_xml.find('House')  # First house
        self.m_internet_xml = self.m_house_xml.find('Internet')
        self.m_dyn_dns_xml = self.m_internet_xml.find('DynamicDNS')
        self.m_house_obj = HouseData()
        self.m_internet_obj = InternetConnectionData()
        self.m_dyn_dns_obj = InternetConnectionDynDnsData()
        self.m_api = internet.API()

    def test_0201_buildObjects(self):
        """ Test to be sure the compound object was built correctly - Rooms is an empty dict.
        """
        self.assertEqual(self.m_pyhouses_obj.HousesData[0].HouseObject.Internet, {}, 'No Internet{}')

    def test_0202_find_xml(self):
        """ Be sure that the XML contains the right stuff.
        """
        self.assertEqual(self.m_root_xml.tag, 'PyHouse', 'Invalid XML - not a PyHouse XML config file')
        self.assertEqual(self.m_houses_xml.tag, 'Houses', 'XML - No Houses section')
        self.assertEqual(self.m_house_xml.tag, 'House', 'XML - No House section')
        self.assertEqual(self.m_internet_xml.tag, 'Internet', 'XML - No Internet section')
        self.assertEqual(self.m_dyn_dns_xml.tag, 'DynamicDNS', 'XML - No Internet section')

    def test_0211_read_one_dyn(self):
        l_dyn_obj = self.m_api.read_one_dyn_dns_xml(self.m_dyn_dns_xml)
        self.assertEqual(l_dyn_obj.Name, 'Afraid', 'Bad DynDns Name')

    def test_0212_read_all_dyn(self):
        l_dyn_obj = self.m_api.read_one_dyn_dns_xml(self.m_dyn_dns_xml)
        self.assertEqual(l_dyn_obj.Name, 'Afraid', 'Bad DynDns Name')

    def test_0213_ReadXML(self):
        """ Be sure that the XML contains the right stuff.
        """
        self.m_api.read_internet_xml(self.m_house_xml)
        self.assertEqual(self.m_root_xml.tag, 'PyHouse', 'Invalid XML - not a PyHouse XML config file')
        self.assertEqual(self.m_houses_xml.tag, 'Houses', 'XML - No Houses section')
        self.assertEqual(self.m_house_xml.tag, 'House', 'XML - No House section')
        self.assertEqual(self.m_internet_xml.tag, 'Internet', 'XML - No Internet section')

    def test_0221_write_one_dyn(self):
        l_dyn_obj = self.m_api.read_one_dyn_dns_xml(self.m_dyn_dns_xml)
        l_xml = self.m_api.write_one_dyn_dns_xml(l_dyn_obj)
        print('XML: {0:}'.format(prettify(l_xml)))
        self.assertEqual(l_dyn_obj.Name, 'Afraid', 'Bad DynDns Name')

    def test_0222_write_all_dyn(self):
        l_dyn_obj = self.m_api.read_dyn_dns_xml(self.m_dyn_dns_xml)
        l_xml = self.m_api.write_dyn_dns_xml(l_dyn_obj)
        print('XML: {0:}'.format(prettify(l_xml)))

    def test_0223_WriteXml(self):
        """ Write out the XML file for the location section
        """
        l_internet = self.m_api.read_internet_xml(self.m_house_xml)
        l_xml = self.m_api.write_internet_xml(l_internet)
        print('XML: {0:}'.format(prettify(l_xml)))

    def test_0231_CreateJson(self):
        """ Create a JSON object for Rooms.
        """
        l_internet = self.m_api.read_internet_xml(self.m_internet_xml)
        l_json = unicode(web_utils.JsonUnicode().encode_json(l_internet))
        print('JSON: {0:}'.format(l_json))


class Test_03_GetExternalIp(unittest.TestCase):


    def setUp(self):
        self.m_pyhouses_obj = PyHousesData()
        self.m_pyhouses_obj.HousesData[0] = HousesData()
        self.m_pyhouses_obj.HousesData[0].HouseObject = HouseData()
        self.m_pyhouses_obj.XmlRoot = self.m_root = ET.fromstring(xml_data.XML_LONG)
        self.m_houses_xml = self.m_root.find('Houses')
        self.m_house_xml = self.m_houses_xml.find('House')  # First house
        self.m_house_obj = HouseData()
        self.m_house_obj.Active = True
        self.m_api = internet.API()

    def test_0301_createClient(self):
        l_client = self.m_api.Start(self.m_pyhouses_obj, self.m_house_obj, self.m_house_xml)

# ## END DBK
