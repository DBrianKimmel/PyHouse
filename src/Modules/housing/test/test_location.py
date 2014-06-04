"""
@name: PyHouse/src/Modules/housing/test/test_location.py
@author: D. Brian Kimmel
@contact: <d.briankimmel@gmail.com
@Copyright (c) 2013-2014 by D. Brian Kimmel
@license: MIT License
@note: Created on Apr 10, 2013
@summary: Test handling the rooms information for a house.


Tests all working OK - DBK 2014-05-22
"""

# Import system type stuff
import xml.etree.ElementTree as ET
from twisted.trial import unittest

# Import PyMh files and modules.
from Modules.Core.data_objects import PyHousesData, HouseData, LocationData
from Modules.housing import location
from Modules.web import web_utils
from Modules.utils.xml_tools import PrettifyXML
from src.test import xml_data

XML = xml_data.XML_LONG


class Test_02_XML(unittest.TestCase):

    def _pyHouses(self):
        self.m_pyhouses_obj = PyHousesData()
        self.m_pyhouses_obj.HouseData = HouseData()
        self.m_pyhouses_obj.XmlRoot = self.m_root = ET.fromstring(XML)
        self.m_houses = self.m_root.find('Houses')
        self.m_house_xml = self.m_houses.find('House')
        self.m_house_obj = LocationData()
        self.m_api = location.ReadWriteConfig()

    def setUp(self):
        self._pyHouses()

    def test_0201_find_xml(self):
        """ Be sure that the XML contains the right stuff.
        """
        self.assertEqual(self.m_root.tag, 'PyHouse', 'Invalid XML - not a PyHouse XML config file')
        self.assertEqual(self.m_houses.tag, 'Houses', 'XML - No Houses section')
        self.assertEqual(self.m_house_xml.tag, 'House', 'XML - No House section')

    def test_0202_ReadXml(self):
        """ Read in the xml file and fill in the location dict
        """
        l_location = self.m_api.read_location_xml(self.m_house_xml)
        self.assertEqual(l_location.City, 'Test City 1', 'Bad city')

    def test_0203_WriteXml(self):
        """ Write out the XML file for the location section
        """
        l_location = self.m_api.read_location_xml(self.m_house_xml)
        l_xml = self.m_api.write_location_xml(l_location)
        print('XML: {0:}'.format(PrettifyXML(l_xml)))


    def test_0221_CreateJson(self):
        """ Create a JSON object for Location.
        """
        l_location = self.m_api.read_location_xml(self.m_house_xml)
        l_json = unicode(web_utils.JsonUnicode().encode_json(l_location))
        print('JSON: {0:}'.format(l_json))

# ## END DBK
