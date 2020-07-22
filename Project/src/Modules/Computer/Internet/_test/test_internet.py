"""
@name:      Modules/Computer/Internet/_test/test_internet.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2013-2020 by D. Brian Kimmel
@license:   MIT License
@note:      Created on Apr 8, 2013
@summary:   Test handling the internet information for a computer.

Passed all 5 tests - DBK - 2015-09-12
"""
from Modules.Core.Utilities.debug_tools import PrettyFormatAny

__updated__ = '2020-01-02'

# Import system type stuff
from twisted.trial import unittest

# Import PyMh files
from _test.testing_mixin import SetupPyHouseObj
from Modules.Core.data_objects import InternetConnectionInformation
from Modules.Computer.Internet.internet import Api as internetApi


class SetupMixin(object):

    def setUp(self):
        self.m_pyhouse_obj = SetupPyHouseObj().BuildPyHouseObj()


class A0(unittest.TestCase):

    def test_00_Print(self):
        _x = PrettyFormatAny.form('_test', 'title')  # so it is defined when printing is cleaned up.
        print('Id: test_internet')


class C01_Util(SetupMixin, unittest.TestCase):
    """ This section tests the reading and writing of XML used by inernet.
    """

    def setUp(self):
        SetupMixin.setUp(self)
        self.m_internet_obj = InternetConnectionInformation()
        self.m_api = internetApi(self.m_pyhouse_obj)

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
