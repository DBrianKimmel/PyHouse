"""
@name: PyHouse/src/test/test_xml_data.py
@author: D. Brian Kimmel
@contact: D.BrianKimmel@gmail.com
@Copyright (c) 2010-2014 by D. Brian Kimmel
@license: MIT License
@note: Created on May 4, 2014
@summary: Test the XML data for integrity.

This test should always be run as the very first test.
It will check the XML file for being fundamentally correct for all other tests that use the XML data.

Tests all working OK - DBK 2014-06-22
"""

# Import system type stuff
import xml.etree.ElementTree as ET
from twisted.trial import unittest

# Import PyMh files and modules.
from Modules.Utilities.tools import PrettyPrintAny
from test.xml_data import XML_LONG


class C01_Raw(unittest.TestCase):
    """
    This section will verify the XML in the 'Modules.test.xml_data' file is correct and what the log module can read/write.
    """

    def s_compute(self):
        self.m_root_element = ET.fromstring(XML_LONG)
        self.m_division = self.m_root_element.find('ComputerDivision')

    def setUp(self):
        pass

    def test_01_raw(self):
        l_str = XML_LONG.split('\n')
        PrettyPrintAny(l_str, 'Raw XML', 50)



class C02_Parsed(unittest.TestCase):
    """
    This section will verify the XML in the 'Modules.test.xml_data' file is correct and what the log module can read/write.
    """

    def setUp(self):
        self.m_root_element = ET.fromstring(XML_LONG)

    def test_01_All(self):
        PrettyPrintAny(self.m_root_element, 'PyHouse')
        self.assertEqual(self.m_root_element.tag, 'PyHouse')

    def test_02_Computer(self):
        l_div = self.m_root_element.find('ComputerDivision')
        PrettyPrintAny(l_div, 'Computer Div')
        self.assertEqual(self.m_root_element.tag, 'PyHouse')

    def test_03_House(self):
        l_div = self.m_root_element.find('HouseDivision')
        PrettyPrintAny(l_div, 'House Div')
        self.assertEqual(self.m_root_element.tag, 'PyHouse')

    def test_03_ReadXML(self):
        l_pyhouse = self.m_root_element
        # PrettyPrintAny(self.m_root_element, 'Root Element', 120)
        self.assertEqual(l_pyhouse.tag, 'PyHouse')

    def test_04_ComputerDivision(self):
        l_div = self.m_root_element.find('ComputerDivision')
        self.assertEqual(l_div.tag, 'ComputerDivision')

    def test_05_Nodes(self):
        l_div = self.m_root_element.find('ComputerDivision')
        l_nodes = l_div.find('NodeSection')
        l_node = l_nodes.find('Node')
        l_uuid = l_node.find('UUID')
        self.assertEqual(l_uuid.text, '87654321-1001-11e3-b583-082e5f899999')

    def test_06_HouseDivision(self):
        l_div = self.m_root_element.find('HouseDivision')
        self.assertEqual(l_div.tag, 'HouseDivision')



class C02_Schema(unittest.TestCase):
    """
    Test XML to comply with XSD.
    """

    def setUp(self):
        pass

# ## END DBK
