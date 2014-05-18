"""
Created on Mar 2, 2014

@author: briank
"""

from Modules.Core import setup
from test import xml_data
from Modules.Core.data_objects import PyHouseData, CoreServicesData

from twisted.trial import unittest
import xml.etree.ElementTree as ET

XML = xml_data.XML


class Test_01_XML(unittest.TestCase):
    """
    This section will verify the XML in the 'Modules.text.xml_data' file is correct and what the setup module can read/write.
    """

    def setUp(self):
        self.m_pyhouses_obj = PyHouseData()

    def test_0101_errors(self):
        pass

class Test_02_ReadXML(unittest.TestCase):
    """
    This section tests the reading and writing of XML used by setup.
    """
    def setUp(self):
        self.m_pyhouses_obj = PyHouseData()
        self.m_pyhouses_obj.XmlRoot = ET.fromstring(XML)
        self.m_pyhouses_obj.CoreServicesData = CoreServicesData()
        self.m_api = setup.API()


# ## END DBK
