"""
@name: PyHouse/src/housing/test/test_house.py

Created on Apr 8, 2013

@author: D. Brian Kimmel
@contact: <d.briankimmel@gmail.com
@Copyright (c) 2010-2014 by D. Brian Kimmel
@license: MIT License
"""

# Import system type stuff
import xml.etree.ElementTree as ET
from twisted.trial import unittest

# Import PyMh files and modules.
from src.housing import house
from src.utils import xml_tools
from src.test import xml_data
from src.core.data_objects import PyHouseData, HousesData, HouseData, LocationData

XML = xml_data.XML


class Test_01_XML(unittest.TestCase):
    """
    This section will verify the XML in the 'src.text.xml_data' file is correct and what the node_local module can read/write.
    """

    def setUp(self):
        self.m_root_element = ET.fromstring(XML)
        self.m_util = xml_tools.PutGetXML()
        self.api = house.API()

    def test_0101_read_xml(self):
        l_pyhouse = self.m_root_element
        self.assertEqual(l_pyhouse.tag, 'PyHouse')

    def test_0102_find_houses(self):
        l_houses = self.m_root_element.find('Houses')
        self.assertEqual(l_houses.tag, 'Houses')

    def test_0103_xml_find_house(self):
        l_houses = self.m_root_element.find('Houses')
        l_list = l_houses.findall('House')
        for l_house in l_list:
            print("House {0:}".format(l_house.get('Name')))

    def test_0104_xxx(self):
        pass

class Test_02_ReadXML(unittest.TestCase):
    """
    This section tests the reading and writing of XML used by house.
    """

    def _pyHouses(self):
        self.m_pyhouses_obj = PyHouseData()
        self.m_pyhouses_obj.HousesData[0] = HousesData()
        self.m_pyhouses_obj.HousesData[0].HouseObject = HouseData()
        self.m_pyhouses_obj.XmlRoot = self.m_root = ET.fromstring(XML)
        self.m_houses = self.m_root.find('Houses')
        self.m_house = self.m_houses.find('House')
        self.m_house_obj = LocationData()
        self.m_api = house.API()

    def setUp(self):
        self._pyHouses()

    def test_0201_buildObjects(self):
        """ Test to be sure the compound object was built correctly - Rooms is an empty dict.
        """
        self.assertEqual(self.m_pyhouses_obj.HousesData[0].HouseObject.Rooms, {}, 'No Rooms{}')

    def test_0202_find_xml(self):
        """ Be sure that the XML contains the right stuff.
        """
        self.assertEqual(self.m_root.tag, 'PyHouse', 'Invalid XML - not a PyHouse XML config file')
        self.assertEqual(self.m_houses.tag, 'Houses', 'XML - No Houses section')
        self.assertEqual(self.m_house.tag, 'House', 'XML - No House section')

    def test_0203_ReadXml(self):
        """ Read in the xml file and fill in x
        """
    def test_0201_read_xml(self):
        self.m_api.read_xml(self.m_pyhouses_obj, self.m_house)

# ## END DBK
