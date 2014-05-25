"""
@name: PyHouse/Modules/housing/test/test_houses.py

Created on Apr 8, 2013

@author: D. Brian Kimmel
@contact: <d.briankimmel@gmail.com
@Copyright (c) 2010-2014 by D. Brian Kimmel
@license: MIT License
"""

import xml.etree.ElementTree as ET
from twisted.trial import unittest

from Modules.housing import houses
from Modules.utils import xml_tools
from test import xml_data
from Modules.Core.data_objects import PyHouseData

XML = xml_data.XML_LONG


class Test_01_XML(unittest.TestCase):
    """
    This section will verify the XML in the 'Modules.text.xml_data' file is correct and what the houses module can read/write.
    """

    def setUp(self):
        self.m_root_element = ET.fromstring(XML)
        self.m_util = xml_tools.PutGetXML()

    def test_0101_read_xml(self):
        l_pyhouse = self.m_root_element
        self.assertEqual(l_pyhouse.tag, 'PyHouse')

    def test_0102_find_houses(self):
        l_houses = self.m_root_element.find('Houses')
        self.assertEqual(l_houses.tag, 'Houses')


class Test_02_ReadXML(unittest.TestCase):

    def setUp(self):
        self.m_pyhouses_obj = PyHouseData()
        self.m_pyhouses_obj.XmlRoot = ET.fromstring(XML)
        self.api = houses.API()

    def test_0201_singleton(self):
        self.api2 = houses.API()
        self.assertEqual(self.api, self.api2, 'Not a singleton.')

    def test_0202_start(self):
        self.api.Start(self.m_pyhouses_obj)

# ## END
