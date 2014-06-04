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
from Modules.housing import house
from Modules.utils import xml_tools
from src.test import xml_data
from src.Modules.utils.tools import PrettyPrintAny


class Test_01_EmptyXML(unittest.TestCase):
    """
    This section will verify the XML in the 'Modules.text.xml_data' file is correct and what the houses module can read/write.
    """

    def setUp(self):
        self.m_root_element = ET.fromstring(xml_data.XML_EMPTY)
        self.m_util = xml_tools.PutGetXML()

    def test_0101_readXML(self):
        l_pyhouse = self.m_root_element
        self.assertEqual(l_pyhouse.tag, 'PyHouse')

    def test_0102_findHousesXML(self):
        l_houses = self.m_root_element.find('Houses')
        self.assertEqual(l_houses, None)


class Test_02_FullXML(unittest.TestCase):
    """
    This section will verify the XML in the 'Modules.text.xml_data' file is correct and what the houses module can read/write.
    """

    def setUp(self):
        self.m_root_element = ET.fromstring(xml_data.XML_LONG)
        self.m_util = xml_tools.PutGetXML()

    def test_0101_readXML(self):
        l_pyhouse = self.m_root_element
        self.assertEqual(l_pyhouse.tag, 'PyHouse')

    def test_0102_findHousesXML(self):
        l_houses = self.m_root_element.find('Houses')
        self.assertEqual(l_houses.tag, 'Houses')


class Test_03_ReadEmptyXML(unittest.TestCase):

    def setUp(self):
        self.m_pyhouses_obj = PyHousesData()
        self.m_pyhouses_obj.XmlRoot = ET.fromstring(xml_data.XML_EMPTY)
        self.m_api = house.API()

    def test_0301_singleton(self):
        self.api2 = house.API()
        self.assertEqual(self.m_api, self.api2, 'Not a singleton.')

    def test_0302_start(self):
        self.m_api.Start(self.m_pyhouses_obj)


class Test_04_ReadFullXML(unittest.TestCase):

    def setUp(self):
        self.m_pyhouses_obj = PyHousesData()
        self.m_pyhouses_obj.XmlRoot = self.m_root_xml = ET.fromstring(xml_data.XML_LONG)
        self.m_pyhouses_obj.HouseData = HouseData()
        # self.m_pyhouses_obj.HouseIndex = 0
        self.m_api = house.API()

    def test_0402_start(self):
        self.m_api.Start(self.m_pyhouses_obj)



class Test_05_TestUtilities(unittest.TestCase):

    def setUp(self):
        self.m_pyhouses_obj = PyHousesData()
        self.m_pyhouses_obj.XmlRoot = self.m_root_xml = ET.fromstring(xml_data.XML_LONG)
        self.m_pyhouses_obj.HouseData = HouseData()
        # self.m_pyhouses_obj.HouseIndex = 0
        self.m_api = house.API()

    def test_0501_HouseList(self):
        l_list = self.m_api.get_house_list(self.m_pyhouses_obj)
        PrettyPrintAny(l_list)

    def test_0502_StartAllHouses(self):
        l_list = self.m_api.get_house_list(self.m_pyhouses_obj)

# ## END DBK
