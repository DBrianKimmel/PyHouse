"""
@name: PyHouse/src/Modules/Core/test/test_setup.py
@author: D. Brian Kimmel
@contact: <d.briankimmel@gmail.com
@copyright: 2014 by D. Brian Kimmel
@note: Created on Mar 2, 2014
@license: MIT License
@summary: This module sets up the Core part of PyHouse.

"""

# Import system type stuff
from twisted.trial import unittest
import xml.etree.ElementTree as ET

# Import PyMh files and modules.
from Modules.Core import setup
from src.test import xml_data
from Modules.Core.data_objects import PyHouseData, CoreServicesData

XML = xml_data.XML_LONG


class Test_01_XML(unittest.TestCase):
    """
    This section will verify the XML in the 'Modules.text.xml_data' file is correct and what the setup module can read/write.
    """

    def setUp(self):
        self.m_pyhouse_obj = PyHouseData()

    def test_0101_ReadEmptyXml(self):
        self.m_pyhouse_obj.XmlRoot = ET.fromstring(xml_data.XML_EMPTY)

    def test_0102_ReadShortXml(self):
        self.m_pyhouse_obj.XmlRoot = ET.fromstring(xml_data.XML_SHORT)

    def test_0103_ReadLongXml(self):
        self.m_pyhouse_obj.XmlRoot = ET.fromstring(xml_data.XML_LONG)


class Test_02_ReadXML(unittest.TestCase):
    """
    This section tests the reading and writing of XML used by setup.
    """
    def setUp(self):
        self.m_pyhouse_obj = PyHouseData()
        self.m_pyhouse_obj.XmlRoot = ET.fromstring(XML)
        self.m_pyhouse_obj.CoreServicesData = CoreServicesData()
        self.m_api = setup.API()


# ## END DBK
