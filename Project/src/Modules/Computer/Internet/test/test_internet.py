"""
@name:      PyHouse/src/Computer/Internet/test/test_internet.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2013-2017 by D. Brian Kimmel
@license:   MIT License
@note:      Created on Apr 8, 2013
@summary:   Test handling the internet information for a computer.

Passed all 5 tests - DBK - 2015-09-12
"""

__updated__ = '2019-07-05'

# Import system type stuff
import xml.etree.ElementTree as ET
from twisted.trial import unittest

# Import PyMh files
from Modules.Core.data_objects import InternetConnectionInformation
from Modules.Computer.Internet.internet import API as internetAPI
from Modules.Computer.Internet.test.xml_internet import TESTING_INTERNET_IPv4_0
from Modules.Core.Utilities import convert
from test.xml_data import XML_LONG
from test.testing_mixin import SetupPyHouseObj


class SetupMixin(object):

    def setUp(self, p_root):
        self.m_pyhouse_obj = SetupPyHouseObj().BuildPyHouseObj(p_root)
        self.m_xml = SetupPyHouseObj().BuildXml(p_root)


class A0(unittest.TestCase):

    def setUp(self):
        pass

    def test_00_Print(self):
        print('Id: test_internet')


class C01_Util(SetupMixin, unittest.TestCase):
    """ This section tests the reading and writing of XML used by inernet.
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))
        self.m_internet_obj = InternetConnectionInformation()
        self.m_api = internetAPI(self.m_pyhouse_obj)

    def test_01_Config(self):
        # l_config = self.m_api._read_xml_configuration(self.m_pyhouse_obj)
        # self.assertEqual(l_config.ExternalIPv4, convert.str_to_long(TESTING_INTERNET_IPv4_0))
        pass

    def test_02_WriteConfig(self):
        # _l_config = self.m_api._read_xml_configuration(self.m_pyhouse_obj)
        # _l_xml = self.m_api._write_xml_config(self.m_pyhouse_obj)
        pass

    def test_03_SaveConfig(self):
        # self.m_api._save_pyhouse_obj(self.m_pyhouse_obj)
        # l_comp = ET.Element('ComputerSection')
        # _l_config = self.m_api._read_xml_configuration(self.m_pyhouse_obj)
        # _l_xml = self.m_api.SaveXml(l_comp)
        pass

    def test_11_CreateService(self):
        # self.m_api._create_internet_discovery_service(self.m_pyhouse_obj)
        pass

    def test_12_StartService(self):
        # self.m_api.UpdateDynDnsSites(self.m_pyhouse_obj)
        # self.m_api._start_internet_discovery(self.m_pyhouse_obj)
        pass

# ## END DBK
