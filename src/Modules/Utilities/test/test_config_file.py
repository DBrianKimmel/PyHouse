"""
@name:      PyHouse/src/Modules/utils/test/test_config_file.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com>
@copyright: (c) 2014-2015 by D. Brian Kimmel
@license:   MIT License
@note:      Created on Jul 15, 2014
@Summary:

Passed all 7 tests - DBK - 2015-08-07

"""

# Import system type stuff
import xml.etree.ElementTree as ET
from twisted.trial import unittest

# Import PyMh files and modules.
from Modules.Utilities.config_file import Util, API as configAPI
from test.xml_data import XML_LONG, XML_LONG_1_3
from test.testing_mixin import SetupPyHouseObj


class SetupMixin(object):

    def setUp(self, p_root):
        self.m_pyhouse_obj = SetupPyHouseObj().BuildPyHouseObj(p_root)
        self.m_xml = SetupPyHouseObj().BuildXml(p_root)


class A1_XML(SetupMixin, unittest.TestCase):
    """
    This section will verify the XML in the 'Modules.test.xml_data' file is correct and what the node_local module can read/write.
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG_1_3))
        SetupPyHouseObj().BuildXml(self.m_xml.root)
        self.m_api = configAPI(self.m_pyhouse_obj)

    def test_01_File(self):
        l_file = Util._open_config_file(self.m_pyhouse_obj)
        # print('File: {}\n'.format(l_file.name))

    def test_02_OpenConfig(self):
        l_file = Util._open_config_file(self.m_pyhouse_obj)

    def test_03_ReadConfig(self):
        Util._open_config_file(self.m_pyhouse_obj)
        l_xml = self.m_pyhouse_obj.Xml.XmlRoot
        l_pyh = self.m_api.read_xml_config_file(self.m_pyhouse_obj)

    def test_04_Version(self):
        l_pyh = self.m_api.read_xml_config_file(self.m_pyhouse_obj)
        l_ret = self.m_api.get_xml_config_file_version(self.m_pyhouse_obj)

    def test_05_WriteConfig(self):
        Util._open_config_file(self.m_pyhouse_obj)
        l_xml = self.m_pyhouse_obj.Xml.XmlRoot
        self.m_api.write_xml_config_file(self.m_pyhouse_obj, l_xml)

class B1_1_3(SetupMixin, unittest.TestCase):
    """
    This section will verify the XML in the 'Modules.test.xml_data' file is correct and what the node_local module can read/write.
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG_1_3))
        SetupPyHouseObj().BuildXml(self.m_xml.root)
        self.m_api = configAPI(self.m_pyhouse_obj)

    def test_01_Version1_3(self):
        l_pyh = self.m_api.read_xml_config_file(self.m_pyhouse_obj)
        l_ret = self.m_api.get_xml_config_file_version(self.m_pyhouse_obj)
        self.assertEqual(l_ret, '1.3.2')

class B2_1_4(SetupMixin, unittest.TestCase):
    """
    This section will verify the XML in the 'Modules.test.xml_data' file is correct and what the node_local module can read/write.
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))
        SetupPyHouseObj().BuildXml(self.m_xml.root)
        self.m_api = configAPI(self.m_pyhouse_obj)

    def test_01_Version1_4(self):
        l_pyh = self.m_api.read_xml_config_file(self.m_pyhouse_obj)
        l_ret = self.m_api.get_xml_config_file_version(self.m_pyhouse_obj)
        self.assertEqual(l_ret, '1.3.2')

# ## END DBK
