"""
@name: PyHouse/src/Modules/housing/test/test_houses.py
@author: D. Brian Kimmel
@contact: <d.briankimmel@gmail.com
@Copyright (c) 2013-2014 by D. Brian Kimmel
@license: MIT License
@note: Created on Apr 8, 2013
@summary: Test handling the information for all houses.

"""

# Import system type stuff
import xml.etree.ElementTree as ET
from twisted.trial import unittest

# Import PyMh files and modules.
from Modules.Core.data_objects import PyHousesData, HousesData, HouseData
from Modules.housing import houses
from Modules.utils import xml_tools
from src.test import xml_data


class Test_01_EmptyXML(unittest.TestCase):
    """
    This section will verify the XML in the 'Modules.text.xml_data' file is correct and what the houses module can read/write.
    """

    def setUp(self):
        self.m_root_element = ET.fromstring(xml_data.XML_EMPTY)
        self.m_util = xml_tools.PutGetXML()

    def test_0101_read_xml(self):
        l_pyhouse = self.m_root_element
        self.assertEqual(l_pyhouse.tag, 'PyHouse')

    def test_0102_find_houses(self):
        l_houses = self.m_root_element.find('Houses')
        self.assertEqual(l_houses, None)


class Test_02_FullXML(unittest.TestCase):
    """
    This section will verify the XML in the 'Modules.text.xml_data' file is correct and what the houses module can read/write.
    """

    def setUp(self):
        self.m_root_element = ET.fromstring(xml_data.XML_LONG)
        self.m_util = xml_tools.PutGetXML()

    def test_0101_read_xml(self):
        l_pyhouse = self.m_root_element
        self.assertEqual(l_pyhouse.tag, 'PyHouse')

    def test_0102_find_houses(self):
        l_houses = self.m_root_element.find('Houses')
        self.assertEqual(l_houses.tag, 'Houses')


class Test_03_ReadEmptyXML(unittest.TestCase):

    def setUp(self):
        self.m_pyhouses_obj = PyHousesData()
        self.m_pyhouses_obj.XmlRoot = ET.fromstring(xml_data.XML_EMPTY)
        self.m_api = houses.API()

    def test_0201_singleton(self):
        self.api2 = houses.API()
        self.assertEqual(self.m_api, self.api2, 'Not a singleton.')

    def test_0202_start(self):
        self.m_api.Start(self.m_pyhouses_obj)


class Test_04_ReadFullXML(unittest.TestCase):

    def setUp(self):
        self.m_pyhouses_obj = PyHousesData()
        self.m_pyhouses_obj.XmlRoot = self.m_root = ET.fromstring(xml_data.XML_LONG)
        self.m_pyhouses_obj.HousesData[0] = HousesData()
        self.m_pyhouses_obj.HousesData[0].HouseObject = HouseData()
        self.m_pyhouses_obj.HouseIndex = 0
        self.m_api = houses.API()

    def test_0201_singleton(self):
        l_api2 = houses.API()
        self.assertEqual(self.m_api, l_api2, 'Not a singleton.')

    def test_0202_start(self):
        self.m_api.Start(self.m_pyhouses_obj)

# ## END
