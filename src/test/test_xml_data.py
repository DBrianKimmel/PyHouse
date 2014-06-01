"""
@name: PyHouse/test/test_xml_data.py
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

XML = xml_data.XML_LONG


class Test_01_XML(unittest.TestCase):
    """
    This section will verify the XML in the 'Modules.test.xml_data' file is correct and what the log module can read/write.
    """

    def setUp(self):
        self.m_root_element = None

    def test_0101_parse_xml(self):
        self.m_root_element = ET.fromstring(XML)
        l_pyhouse = self.m_root_element
        self.assertEqual(l_pyhouse.tag, 'PyHouse')

    def test_0102_read_xml(self):
        self.m_root_element = ET.fromstring(XML)
        l_pyhouse = self.m_root_element
        self.assertEqual(l_pyhouse.tag, 'PyHouse')

    def test_0103_find_logs(self):
        self.m_root_element = ET.fromstring(XML)
        l_logs = self.m_root_element.find('Logs')
        self.assertEqual(l_logs.tag, 'Logs')

    def test_0104_uuid(self):
        self.m_root_element = ET.fromstring(XML)
        l_logs = self.m_root_element.find('Logs')
        l_debug = l_logs.find('Debug')
        self.assertEqual(l_debug.text, '/var/log/pyhouse/debug')

# ## END DBK
