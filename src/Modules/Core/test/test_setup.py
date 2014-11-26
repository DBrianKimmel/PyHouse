"""
@name: PyHouse/src/Modules/Core/test/test_setup.py
@author: D. Brian Kimmel
@contact: D.BrianKimmel@gmail.com
@copyright: 2014 by D. Brian Kimmel
@note: Created on Mar 2, 2014
@license: MIT License
@summary: This module sets up the Core part of PyHouse.

Passed all 4 tests - DBK - 2014-07-18
"""

# Import system type stuff
from twisted.trial import unittest
import xml.etree.ElementTree as ET

# Import PyMh files and modules.
from Modules.Core import setup
from test import xml_data
from test.testing_mixin import SetupPyHouseObj
from Modules.Utilities.tools import PrettyPrintAny

XML = xml_data.XML_LONG


class SetupMixin(object):
    """
    """

    def setUp(self, p_root):
        self.m_pyhouse_obj = SetupPyHouseObj().BuildPyHouseObj(p_root)
        self.m_xml = SetupPyHouseObj().BuildXml(p_root)


class C01_XML(SetupMixin, unittest.TestCase):
    """
    This section will verify the XML in the 'Modules.text.xml_data' file is correct and what the setup module can
    read/write.
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(xml_data.XML_LONG))

    def test_01_ReadEmptyXml(self):
        self.m_pyhouse_obj.XmlRoot = ET.fromstring(xml_data.XML_EMPTY)

    def test_02_ReadShortXml(self):
        self.m_pyhouse_obj.XmlRoot = ET.fromstring(xml_data.XML_SHORT)

    def test_03_ReadLongXml(self):
        self.m_pyhouse_obj.XmlRoot = ET.fromstring(xml_data.XML_LONG)


class Test_02_XML(SetupMixin, unittest.TestCase):
    """
    This section tests the reading and writing of XML used by setup.
    """
    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(xml_data.XML_LONG))
        self.m_api = setup.API()

    def test_01_ReadXml(self):
        self.m_api.read_xml_config_info(self.m_pyhouse_obj)

    def test_02_WriteXml(self):
        pass

# ## END DBK
