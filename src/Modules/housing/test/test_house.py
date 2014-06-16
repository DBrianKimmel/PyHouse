"""
@name: PyHouse/src/Modules/housing/test/test_house.py
@author: D. Brian Kimmel
@contact: <d.briankimmel@gmail.com
@Copyright (c) 2013-2014 by D. Brian Kimmel
@license: MIT License
@note: Created on Apr 8, 2013
@summary: Test handling the information for a house.


Tests all working OK - DBK 2014-05-29
"""

# Import system type stuff
import xml.etree.ElementTree as ET
from twisted.trial import unittest

# Import PyMh files and modules.
from Modules.Core.data_objects import PyHouseData, HouseData, LocationData
from Modules.housing import house
from Modules.web import web_utils
from Modules.utils import xml_tools
from src.test import xml_data
from Modules.utils.tools import PrettyPrintAny


class Test_01_XML(unittest.TestCase):
    """
    This section will verify the XML in the 'Modules.text.xml_data' file is correct and what the node_local module can read/write.
    """

    def setUp(self):
        self.m_root_element = ET.fromstring(xml_data.XML_LONG)
        self.m_util = xml_tools.PutGetXML()
        self.m_api = house.API()

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
        self.m_pyhouse_obj = PyHouseData()
        self.m_pyhouse_obj.HouseData = HouseData()
        self.m_pyhouse_obj.XmlRoot = self.m_root_xml = ET.fromstring(xml_data.XML_LONG)
        self.m_houses_xml = self.m_root_xml.find('Houses')
        self.m_house_xml = self.m_houses_xml.find('House')
        self.m_house_obj = LocationData()
        self.m_api = house.API()

    def setUp(self):
        self._pyHouses()

    def test_0201_buildObjects(self):
        """ Test to be sure the compound object was built correctly - Rooms is an empty dict.
        """
        self.assertEqual(self.m_pyhouse_obj.HouseData.Rooms, {}, 'No Rooms{}')

    def test_0202_find_xml(self):
        """ Be sure that the XML contains the right stuff.
        """
        self.assertEqual(self.m_root_xml.tag, 'PyHouse', 'Invalid XML - not a PyHouse XML config file')
        self.assertEqual(self.m_houses_xml.tag, 'Houses', 'XML - No Houses section')
        self.assertEqual(self.m_house_xml.tag, 'House', 'XML - No House section')

    def test_0203_ReadXml(self):
        """ Read in the xml file and fill in x
        """
        l_house_obj = self.m_api.read_house_xml(self.m_house_xml)
        self.assertEqual(l_house_obj.Name, 'Test House 1', 'Bad Name')
        self.assertEqual(l_house_obj.Location.Street, 'Test Street 1', 'Bad Street')
        PrettyPrintAny(l_house_obj)

    def test_0204_write_house_xml(self):
        l_house_obj = self.m_api.read_house_xml(self.m_house_xml)
        l_xml = self.m_api.write_house_xml(l_house_obj)
        print('XML: {0:}'.format(xml_tools.PrettifyXML(l_xml)))

    def test_0221_CreateJson(self):
        """ Create a JSON object for Location.
        """
        l_house = self.m_api.read_house_xml(self.m_house_xml)
        print('House: {0:}'.format(l_house))
        l_json = unicode(web_utils.JsonUnicode().encode_json(l_house))
        print('JSON: {0:}'.format(l_json))


class Test_03_Utilities(unittest.TestCase):

    def setUp(self):
        self.m_pyhouse_obj = PyHouseData()
        self.m_pyhouse_obj.HouseData = HouseData()
        self.m_pyhouse_obj.XmlRoot = self.m_root_xml = ET.fromstring(xml_data.XML_LONG)
        self.m_houses_xml = self.m_root_xml.find('Houses')
        self.m_house_xml = self.m_houses_xml.find('House')
        self.m_house_obj = LocationData()
        self.m_api = house.API()

    def test_0301_HouseList(self):
        l_list = self.m_api.get_house_list(self.m_pyhouse_obj)
        PrettyPrintAny(l_list)

    def Xtest_0305_findXml(self):
        self.m_api.find_house_xml(self.m_pyhouse_obj)

# ## END DBK
