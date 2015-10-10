"""
@name:      PyHouse/src/Modules/Core/test/test_setup.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2014-2015 by D. Brian Kimmel
@note:      Created on Mar 2, 2014
@license:   MIT License
@summary:   This module sets up the Core part of PyHouse.

Passed all 9 tests - DBK - 2015-07-31
"""

# Import system type stuff
from twisted.trial import unittest
import xml.etree.ElementTree as ET

# Import PyMh files and modules.
from Modules.Core import setup_pyhouse
from Modules.Core.data_objects import PyHouseAPIs, XmlInformation, ComputerInformation, HouseInformation, \
    CoreServicesInformation, TwistedInformation
from test import xml_data
from test.testing_mixin import SetupPyHouseObj

XML = xml_data.XML_LONG



class SetupMixin(object):
    """
    """

    def setUp(self, p_root):
        self.m_pyhouse_obj = SetupPyHouseObj().BuildPyHouseObj(p_root)
        self.m_xml = SetupPyHouseObj().BuildXml(p_root)



class C01_Structures(SetupMixin, unittest.TestCase):
    """
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(xml_data.XML_LONG))

    def test_01_PyHouse(self):
        # PrettyPrintAny(self.m_pyhouse_obj, 'PyHouseObj')
        self.assertIsInstance(self.m_pyhouse_obj.APIs, PyHouseAPIs)
        self.assertIsInstance(self.m_pyhouse_obj.Computer, ComputerInformation)
        self.assertIsInstance(self.m_pyhouse_obj.House, HouseInformation)
        self.assertIsInstance(self.m_pyhouse_obj.Services, CoreServicesInformation)
        self.assertIsInstance(self.m_pyhouse_obj.Twisted, TwistedInformation)
        self.assertIsInstance(self.m_pyhouse_obj.Xml, XmlInformation)

    def test_02_Computer(self):
        # PrettyPrintAny(self.m_pyhouse_obj.Computer, 'Computer')
        pass

    def test_03_House(self):
        # PrettyPrintAny(self.m_pyhouse_obj.House, 'House')
        pass

    def test_04_Services(self):
        # PrettyPrintAny(self.m_pyhouse_obj.Services, 'Service')
        pass

    def test_05_Twisted(self):
        # PrettyPrintAny(self.m_pyhouse_obj.Twisted, 'Twisted')
        pass

    def test_06_Xml(self):
        # PrettyPrintAny(self.m_pyhouse_obj.Xml, 'Xml')
        pass


class C02_XML(SetupMixin, unittest.TestCase):
    """
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(xml_data.XML_LONG))

    def test_01_ReadEmptyXml(self):
        self.m_pyhouse_obj.XmlRoot = ET.fromstring(xml_data.XML_EMPTY)
        # PrettyPrintAny(self.m_pyhouse_obj.XmlRoot, 'Empty XmlRoot')

    def test_02_ReadShortXml(self):
        self.m_pyhouse_obj.XmlRoot = ET.fromstring(xml_data.XML_SHORT)
        # PrettyPrintAny(self.m_pyhouse_obj.XmlRoot, 'Short XmlRoot')

    def test_03_ReadLongXml(self):
        self.m_pyhouse_obj.XmlRoot = ET.fromstring(xml_data.XML_LONG)
        # PrettyPrintAny(self.m_pyhouse_obj.XmlRoot, 'Long XmlRoot')

# ## END DBK
