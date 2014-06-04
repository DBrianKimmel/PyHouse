"""
@name: PyHouse/src/Modules/utils/test/test_xml_tools.py
@author: D. Brian Kimmel
@contact: <d.briankimmel@gmail.com
@copyright: 2013-2014 by D. Brian Kimmel
@license: MIT License
@note: Created on Apr 4, 2013
@summary: This module is for testing conversion tools.


Tests all working OK - DBK 2014-05-28
"""

# Import system type stuff
import xml.etree.ElementTree as ET
from twisted.trial import unittest

# Import PyMh files and modules.
from Modules.Core.data_objects import PyHousesData, HousesData, HouseData, BaseLightingData
from Modules.utils.convert import ConvertEthernet
from src.test import xml_data

XML = xml_data.XML_LONG

class Test_01_RawConvert(unittest.TestCase):
    """
    This series tests the PutGetXML class methods
    """

    def setUp(self):
        self.m_pyhouses_obj = PyHousesData()
        self.m_pyhouses_obj.HouseData = HouseData()
        self.m_pyhouses_obj.XmlRoot = self.m_root = ET.fromstring(XML)
        self.m_houses_xml = self.m_root.find('Houses')
        self.m_house_xml = self.m_houses_xml.find('House')  # First house
        self.m_nodes_xml = self.m_root.find('Nodes')
        self.m_node_xml = self.m_nodes_xml.find('Node')  # First house
        self.m_interfaces_xml = self.m_node_xml.find('Interfaces')
        self.m_interface_xml = self.m_interfaces_xml.find('Interface')  # First house
        self.m_api = ConvertEthernet()

    def _test(self, oper, a, r):
        result = oper(a)
        self.assertEqual(result, r)

    def test_0101_ethernet_2dotted(self):
        self._test(self.m_api.dotted_quad2long, '192.168.1.65', 3232235841L)

    def test_0102_ethernet_2long(self):
        self._test(self.m_api.long2dotted_quad, 3232235841L, '192.168.1.65')

# ## END
