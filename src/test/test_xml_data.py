"""
@name: PyHouse/src/test/test_xml_data.py
@author: D. Brian Kimmel
@contact: <d.briankimmel@gmail.com
@Copyright (c) 2010-2014 by D. Brian Kimmel
@license: MIT License
@note: Created on May 4, 2014
@summary: Test the XML data for integrity.

This test should always be run as the very first test.
It will check the XML file for being fundamentally correct for all other tests that use the XML data.
"""

# Import system type stuff
import xml.etree.ElementTree as ET
from twisted.trial import unittest

# Import PyMh files and modules.
from src.test import xml_data


class Test_01_XML(unittest.TestCase):
    """
    This section will verify the XML in the 'Modules.test.xml_data' file is correct and what the log module can read/write.
    """

    def setUp(self):
        self.m_root_element = ET.fromstring(xml_data.XML_LONG)

    def test_0101_parse_xml(self):
        l_pyhouse = self.m_root_element
        self.assertEqual(l_pyhouse.tag, 'PyHouse')

    def test_0102_read_xml(self):
        l_pyhouse = self.m_root_element
        self.assertEqual(l_pyhouse.tag, 'PyHouse')

    def test_0103_Logs(self):
        self.m_root_element = ET.fromstring(xml_data.XML_LONG)
        l_logs = self.m_root_element.find('Logs')
        self.assertEqual(l_logs.tag, 'Logs')

    def test_0104_LogsDebug(self):
        self.m_root_element = ET.fromstring(xml_data.XML_LONG)
        l_logs = self.m_root_element.find('Logs')
        l_debug = l_logs.find('Debug')
        self.assertEqual(l_debug.text, '/var/log/pyhouse/debug')

    def test_0105_Nodes(self):
        l_nodes = self.m_root_element.find('Nodes')
        l_node = l_nodes.find('Node')
        l_uuid = l_node.find('UUID')
        self.assertEqual(l_uuid.text, '87654321-1001-11e3-b583-082e5f899999')
# ## END DBK
