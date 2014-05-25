"""
@name: PyHouse/src/Modules/lights/test/test_lighting_core.py
@author: D. Brian Kimmel
@contact: <d.briankimmel@gmail.com
@Copyright (c) 2014 by D. Brian Kimmel
@license: MIT License
@note: Created on May 4, 2014
@summary: This module is for testing lighting Core.

"""

# Import system type stuff
import xml.etree.ElementTree as ET
from twisted.trial import unittest

# Import PyMh files and modules.
from Modules.Core.data_objects import PyHouseData, HousesData, HouseData, BaseLightingData
from Modules.lights import lighting_core
from test import xml_data

XML = xml_data.XML_LONG


class Test_02_ReadXML(unittest.TestCase):
    """ This section tests the reading and writing of XML used by node_local.
    """

    def _pyHouses(self):
        self.m_pyhouses_obj = PyHouseData()
        self.m_pyhouses_obj.HousesData[0] = HousesData()
        self.m_pyhouses_obj.HousesData[0].HouseObject = HouseData()
        self.m_pyhouses_obj.XmlRoot = self.m_root = ET.fromstring(XML)
        self.m_houses = self.m_root.find('Houses')
        self.m_house = self.m_houses.find('House')

    def setUp(self):
        self._pyHouses()

    def test_0201_find_xml(self):
        """ Be sure that the XML contains the right stuff.
        """
        self.assertEqual(self.m_root.tag, 'PyHouse', 'Invalid XML - not a PyHouse XML config file')
        self.assertEqual(self.m_houses.tag, 'Houses', 'XML - No Houses section')
        self.assertEqual(self.m_house.tag, 'House', 'XML - No House section')

    def test_0202_ReadXml(self):
        """ Read in the xml file and fill in the rooms dict
        """
        l_location = self.m_api.read_location_xml(self.m_house)
        self.assertEqual(l_location.City, 'Test City 1', 'Bad city')

    def test_0201_read_xml(self):
        pass

# ## END DBK
