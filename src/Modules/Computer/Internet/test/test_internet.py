"""
@name:      PyHouse/src/Computer/Internet/test/test_internet.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2013-2014 by D. Brian Kimmel
@license:   MIT License
@note:      Created on Apr 8, 2013
@summary:   Test handling the internet information for a computer.

XML tests all run OK - DBK 2014-07-01
"""

# Import system type stuff
import xml.etree.ElementTree as ET
from twisted.trial import unittest

# Import PyMh files
from Modules.Core.data_objects import InternetConnectionData
from Modules.Computer.Internet import internet
from Modules.Utilities.tools import PrettyPrintAny
from test import xml_data
from test.testing_mixin import SetupPyHouseObj


class SetupMixin(object):

    def setUp(self, p_root):
        self.m_pyhouse_obj = SetupPyHouseObj().BuildPyHouseObj(p_root)
        self.m_xml = SetupPyHouseObj().BuildXml(p_root)



class C01_Util(SetupMixin, unittest.TestCase):
    """ This section tests the reading and writing of XML used by inernet.
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(xml_data.XML_LONG))
        self.m_internet_obj = InternetConnectionData()
        # self.m_dyn_dns_obj = InternetConnectionDynDnsData()
        self.m_api = internet.API()

    def test_01_Config(self):
        l_config = self.m_api._read_xml_configuration(self.m_pyhouse_obj)
        PrettyPrintAny(l_config, 'Config')

    def test_02_WriteConfig(self):
        _l_config = self.m_api._read_xml_configuration(self.m_pyhouse_obj)
        l_xml = self.m_api._write_xml_config(self.m_pyhouse_obj)
        PrettyPrintAny(l_xml, 'XML')

    def test_03_SaveConfig(self):
        self.m_api._save_pyhouse_obj(self.m_pyhouse_obj)
        l_comp = ET.Element('ComputerSection')
        _l_config = self.m_api._read_xml_configuration(self.m_pyhouse_obj)
        l_xml = self.m_api.SaveXml(l_comp)
        PrettyPrintAny(l_xml, 'XML')

    def test_11_CreateService(self):
        self.m_api._create_internet_discovery_service(self.m_pyhouse_obj)
        PrettyPrintAny(self.m_pyhouse_obj.Services, 'PyHouse')
        pass

    def test_12_StartService(self):
        self.m_api._create_internet_discovery_service(self.m_pyhouse_obj)
        self.m_api._start_internet_discovery(self.m_pyhouse_obj)

# ## END DBK
