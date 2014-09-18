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
# from Modules.utils.tools import PrettyPrintAny
from test import xml_data


class Test_01_XML(unittest.TestCase):
    """
    This section will verify the XML in the 'Modules.test.xml_data' file is correct and what the log module can read/write.
    """

    def s_compute(self):
        self.m_root_element = ET.fromstring(xml_data.XML_LONG)
        self.m_division = self.m_root_element.find('ComputerDivision')

    def setUp(self):
        pass

    def test_0101_ParseXML(self):
        self.m_root_element = ET.fromstring(xml_data.XML_LONG)
        l_pyhouse = self.m_root_element
        self.assertEqual(l_pyhouse.tag, 'PyHouse')

    def test_0102_ReadXML(self):
        self.m_root_element = ET.fromstring(xml_data.XML_LONG)
        l_pyhouse = self.m_root_element
        # PrettyPrintAny(self.m_root_element, 'Root Element', 120)
        self.assertEqual(l_pyhouse.tag, 'PyHouse')

    def test_0103_ComputerDivision(self):
        self.m_root_element = ET.fromstring(xml_data.XML_LONG)
        l_div = self.m_root_element.find('ComputerDivision')
        self.assertEqual(l_div.tag, 'ComputerDivision')

    def test_0104_Logs(self):
        self.s_compute()
        l_logs = self.m_division.find('LogSection')
        self.assertEqual(l_logs.tag, 'LogSection')

    def test_0105_LogsDebug(self):
        self.s_compute()
        l_logs = self.m_division.find('LogSection')
        l_debug = l_logs.find('Debug')
        self.assertEqual(l_debug.text, '/var/log/pyhouse/debug')

    def test_0106_Nodes(self):
        self.s_compute()
        l_nodes = self.m_division.find('NodeSection')
        l_node = l_nodes.find('Node')
        l_uuid = l_node.find('UUID')
        self.assertEqual(l_uuid.text, '87654321-1001-11e3-b583-082e5f899999')

    def test_0110_HouseDivision(self):
        self.m_root_element = ET.fromstring(xml_data.XML_LONG)
        l_div = self.m_root_element.find('HouseDivision')
        self.assertEqual(l_div.tag, 'HouseDivision')

# ## END DBK
