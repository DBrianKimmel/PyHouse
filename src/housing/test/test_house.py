"""
@name: PyHouse/src/housing/test/test_house.py

Created on Apr 8, 2013

@author: D. Brian Kimmel
@contact: <d.briankimmel@gmail.com
@Copyright (c) 2010-2014 by D. Brian Kimmel
@license: MIT License
"""

import xml.etree.ElementTree as ET
from twisted.trial import unittest

from src.housing import house
from src.utils import xml_tools
from src.test import xml_data
from src.core.data_objects import PyHouseData, CoreData

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

    def setUp(self):
        self.m_pyhouses_obj = PyHouseData()
        self.m_pyhouses_obj.XmlRoot = ET.fromstring(XML)
        self.m_pyhouses_obj.CoreData = CoreData()
        self.m_api = house.API()

    def test_0201_read_xml(self):
        self.m_api.read_xml(self.m_pyhouses_obj)


# ## END DBK
