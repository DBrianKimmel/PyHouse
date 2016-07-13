"""
@name:      PyHouse/src/Modules/Core/test/test_setup_pyhouse.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2014-2016 by D. Brian Kimmel
@note:      Created on Mar 2, 2014
@license:   MIT License
@summary:   This module sets up the Core part of PyHouse.

Passed all 9 tests - DBK - 2016-07-12
"""
from bs4.builder._lxml import LXML

__updated__ = '2016-07-12'

# Import system type stuff
from twisted.trial import unittest
import xml.etree.ElementTree as ET

# Import PyMh files and modules.
# from Modules.Core import setup_pyhouse
from Modules.Utilities.config_file import API as configAPI
from Modules.Utilities.debug_tools import PrettyFormatAny
from Modules.Computer.computer import API as computerApi
from Modules.Housing.house import API as houseApi
from Modules.Core.data_objects import \
    PyHouseAPIs, \
    XmlInformation, \
    ComputerInformation, \
    HouseInformation, \
    CoreServicesInformation, \
    TwistedInformation, \
    ComputerAPIs, \
    HouseAPIs
from test.xml_data import XML_LONG
from test.testing_mixin import SetupPyHouseObj


class SetupMixin(object):
    """
    """

    def setUp(self, p_root):
        self.m_pyhouse_obj = SetupPyHouseObj().BuildPyHouseObj(p_root)
        self.m_xml = SetupPyHouseObj().BuildXml(p_root)


class C1_Structures(SetupMixin, unittest.TestCase):
    """
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))

    def test_1_PyHouse(self):
        """ Test every component of PyHouseData()
        """
        # print(PrettyFormatAny.form(self.m_pyhouse_obj, 'C1-1-A PyHouse obj'))
        self.assertIsInstance(self.m_pyhouse_obj.APIs, PyHouseAPIs)
        self.assertIsInstance(self.m_pyhouse_obj.Computer, ComputerInformation)
        self.assertIsInstance(self.m_pyhouse_obj.House, HouseInformation)
        self.assertIsInstance(self.m_pyhouse_obj.Services, CoreServicesInformation)
        self.assertIsInstance(self.m_pyhouse_obj.Twisted, TwistedInformation)
        self.assertEqual(self.m_pyhouse_obj.Uuids, {})
        self.assertIsInstance(self.m_pyhouse_obj.Xml, XmlInformation)

    def test_2_APIs(self):
        # print(PrettyFormatAny.form(self.m_pyhouse_obj.APIs, 'C1-2-A PyHouse APIs'))
        self.assertIsInstance(self.m_pyhouse_obj.APIs.Computer, ComputerAPIs)
        self.assertIsInstance(self.m_pyhouse_obj.APIs.House, HouseAPIs)

    def test_3_Computer(self):
        print(PrettyFormatAny.form(self.m_pyhouse_obj.Computer, 'C1-3-A PyHouse.Computer obj'))
        pass

    def test_4_House(self):
        print(PrettyFormatAny.form(self.m_pyhouse_obj.House, 'C1-4-A PyHouse.House obj'))
        pass

    def test_5_Services(self):
        # print(PrettyFormatAny.form(self.m_pyhouse_obj, 'C1-1-A PyHouse obj'))
        pass

    def test_6_Twisted(self):
        print(PrettyFormatAny.form(self.m_pyhouse_obj.Twisted, 'C1-6-A PyHouse.Twisted obj'))
        pass

    def test_7_Uuids(self):
        print(PrettyFormatAny.form(self.m_pyhouse_obj.Uuids, 'C1-7-A PyHouse.Uuids obj'))
        pass

    def test_8_Xml(self):
        print(PrettyFormatAny.form(self.m_pyhouse_obj.Xml, 'C1-8-A PyHouse.Xml obj'))
        pass


class C2_XML(SetupMixin, unittest.TestCase):
    """
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))

    def test_1_ReadLongXml(self):
        self.m_pyhouse_obj.XmlRoot = ET.fromstring(XML_LONG)


class D1_Write(SetupMixin, unittest.TestCase):
    """
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))

    def test_1_Xml(self):
        l_xml = configAPI(self.m_pyhouse_obj).create_xml_config_foundation(self.m_pyhouse_obj)
        # computerApi(self.m_pyhouse_obj).SaveXml(l_xml)
        # houseApi(self.m_pyhouse_obj).SaveXml(l_xml)
        print(PrettyFormatAny.form(l_xml, 'D1-1-A PyHouse.Twisted obj'))

# ## END DBK
