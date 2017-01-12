"""
@name:      PyHouse/src/Modules/Core/test/test_setup_pyhouse.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2014-2017 by D. Brian Kimmel
@note:      Created on Mar 2, 2014
@license:   MIT License
@summary:   This module sets up the Core part of PyHouse.

Passed all 14 tests - DBK - 2017-01-10
"""
from Modules.Core import setup_pyhouse

__updated__ = '2017-01-10'

# Import system type stuff
from twisted.trial import unittest
import xml.etree.ElementTree as ET

# Import PyMh files and modules.
from test.xml_data import XML_LONG
from test.testing_mixin import SetupPyHouseObj
# from Modules.Core import setup_pyhouse
from Modules.Utilities.config_file import API as configAPI
from Modules.Utilities.debug_tools import PrettyFormatAny
from Modules.Core.data_objects import \
    PyHouseAPIs, \
    XmlInformation, \
    ComputerInformation, \
    HouseInformation, \
    TwistedInformation, \
    ComputerAPIs, \
    HouseAPIs


class SetupMixin(object):
    """
    """

    def setUp(self, p_root):
        self.m_pyhouse_obj = SetupPyHouseObj().BuildPyHouseObj(p_root)
        self.m_xml = SetupPyHouseObj().BuildXml(p_root)


class A0(unittest.TestCase):
    def setUp(self):
        pass
    def test_00_Print(self):
        print('Id: test_setup_pyhouse')
    def XXX_test_01_Print(self):
        print(XML_LONG)
        pass


class A1_Setup(SetupMixin, unittest.TestCase):
    """
    This section tests the setup of the test
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))

    def test_01_PyHouseObj(self):
        # print(PrettyFormatAny.form(self.m_pyhouse_obj.Xml, 'A1-01-A - PyHouse.Xml'))
        self.assertNotEqual(self.m_pyhouse_obj.Xml, None)

    def test_02_Tags(self):
        # print(PrettyFormatAny.form(self.m_xml, 'A1-02-A - Tags'))
        self.assertEqual(self.m_xml.root.tag, 'PyHouse')
        self.assertEqual(self.m_xml.computer_div.tag, 'ComputerDivision')
        self.assertEqual(self.m_xml.node_sect.tag, 'NodeSection')


class B1_UUIDs(SetupMixin, unittest.TestCase):
    """
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))

    def test_01_Xml(self):
        l_xml = self.m_pyhouse_obj.Xml
        print(PrettyFormatAny.form(l_xml, 'PyHouse,Xml'))
        self.assertEqual(l_xml.XmlConfigDir, '/etc/pyhouse/')

    def test_02_build(self):
        """
        """
        l_file = setup_pyhouse._build_file(self.m_pyhouse_obj, 'Computer.uuid')
        self.assertEqual(l_file, '/etc/pyhouse/Computer.uuid')

    def test_03_Read(self):
        l_uuid = setup_pyhouse._read_file(self.m_pyhouse_obj, 'Computer.uuid')
        print('B1-03-A - UUID: {}'.format(l_uuid))

    def test_04_Write(self):
        l_uuid = '222ec0e9-d76e-11e6-b40f-74dfbfae5aed'
        l_ret = setup_pyhouse._write_file(self.m_pyhouse_obj, 'Computer.uuid', l_uuid)
        print('B1-03-A - UUID: {}'.format(l_ret))


class C1_Structures(SetupMixin, unittest.TestCase):
    """
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))

    def test_01_PyHouse(self):
        """ Test every component of PyHouseData()
        """
        # print(PrettyFormatAny.form(self.m_pyhouse_obj, 'C1-1-A PyHouse obj'))
        self.assertIsInstance(self.m_pyhouse_obj.APIs, PyHouseAPIs)
        self.assertIsInstance(self.m_pyhouse_obj.Computer, ComputerInformation)
        self.assertIsInstance(self.m_pyhouse_obj.House, HouseInformation)
        self.assertIsInstance(self.m_pyhouse_obj.Twisted, TwistedInformation)
        self.assertEqual(self.m_pyhouse_obj.Uuids.All, {})
        self.assertIsInstance(self.m_pyhouse_obj.Xml, XmlInformation)

    def test_02_APIs(self):
        # print(PrettyFormatAny.form(self.m_pyhouse_obj.APIs, 'C1-2-A PyHouse APIs'))
        self.assertIsInstance(self.m_pyhouse_obj.APIs.Computer, ComputerAPIs)
        self.assertIsInstance(self.m_pyhouse_obj.APIs.House, HouseAPIs)

    def test_03_Computer(self):
        print(PrettyFormatAny.form(self.m_pyhouse_obj.Computer, 'C1-3-A PyHouse.Computer obj'))
        pass

    def test_04_House(self):
        print(PrettyFormatAny.form(self.m_pyhouse_obj.House, 'C1-4-A PyHouse.House obj'))
        pass

    def test_05_Services(self):
        # print(PrettyFormatAny.form(self.m_pyhouse_obj, 'C1-1-A PyHouse obj'))
        pass

    def test_06_Twisted(self):
        print(PrettyFormatAny.form(self.m_pyhouse_obj.Twisted, 'C1-6-A PyHouse.Twisted obj'))
        pass

    def test_07_Uuids(self):
        print(PrettyFormatAny.form(self.m_pyhouse_obj.Uuids, 'C1-7-A PyHouse.Uuids obj'))
        pass

    def test_08_Xml(self):
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
