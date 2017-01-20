"""
@name:      PyHouse/src/test/test_xml_data.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2010-2017 by D. Brian Kimmel
@license:   MIT License
@note:      Created on May 4, 2014
@summary:   Test the XML data for integrity.

This test should always be run as the very first test.
It will check the XML file for being fundamentally correct for all other tests that use the XML data.

Passed all 12 tests - DBK - 2017-01-18
"""

__updated__ = '2017-01-19'

# Import system type stuff
import xml.etree.ElementTree as ET
from twisted.trial import unittest

# Import PyMh files and modules.
from test.xml_data import XML_LONG, XML_EMPTY, TESTING_PYHOUSE
from Modules.Core.Utilities.debug_tools import PrettyFormatAny
from Modules.Computer.Nodes.test.xml_nodes import TESTING_NODES_NODE_UUID_0


class A0(unittest.TestCase):
    def setUp(self):
        pass
    def test_00_Print(self):
        print('Id: test_xml_data')


class A1_Raw(unittest.TestCase):
    """
    This section will verify the XML in the 'Modules.test.xml_data' file is correct and what the log module can read/write.
    """

    def setUp(self):
        pass

    def test_01_print(self):
        print(XML_EMPTY)
        print(PrettyFormatAny.form(XML_EMPTY, 'Root'))

    def test_02_print(self):
        print(XML_LONG)
        print(PrettyFormatAny.form(XML_LONG, 'Root'))

    def test_02_raw_1_4(self):
        l_str = XML_LONG.split('\n')


class A2_Parsed(unittest.TestCase):
    """
    This section will verify the XML in the 'Modules.test.xml_data' file is correct and what the log module can read/write.
    """

    def setUp(self):
        self.m_root_element = ET.fromstring(XML_LONG)

    def test_01_All(self):
        self.assertEqual(self.m_root_element.tag, TESTING_PYHOUSE)

    def test_02_Computer(self):
        l_div = self.m_root_element.find('ComputerDivision')
        self.assertEqual(self.m_root_element.tag, TESTING_PYHOUSE)

    def test_04_ComputerDivision(self):
        l_div = self.m_root_element.find('ComputerDivision')
        self.assertEqual(l_div.tag, 'ComputerDivision')

    def test_05_Nodes(self):
        l_div = self.m_root_element.find('ComputerDivision')
        l_nodes = l_div.find('NodeSection')
        l_node = l_nodes.find('Node')
        l_uuid = l_node.find('UUID')
        self.assertEqual(l_uuid.text, TESTING_NODES_NODE_UUID_0)

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
