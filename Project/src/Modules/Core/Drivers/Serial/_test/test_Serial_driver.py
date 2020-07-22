"""
@name:      Modules/Core/Drivers/Serial/_test/test_Serial_driver.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2013_2019 by D. Brian Kimmel
@license:   MIT License
@note:      Created on May 4, 2013
@summary:   This module is for testing local node data.

Passed all 9 tests - DBK - 2019-10-13

"""

__updated__ = '2019-10-13'

# Import system type stuff
from twisted.trial import unittest
from ruamel.yaml import YAML

# Import PyMh files and modules.
from _test.testing_mixin import SetupPyHouseObj
from Modules.Core.Config.config_tools import Api as configApi
from Modules.House.Lighting.controllers import 
from Modules.Core.Drivers.Serial import Serial_driver

from Modules.Core.Utilities.debug_tools import PrettyFormatAny

TEST_YAML = """\
Controllers:
   - Name: TestPlm
     Comment: Portable, Goes where I do.
     Family:
        Name: Insteon
        Type: Plm
        Address: 49.F9.E7
     Interface:
        Type: Serial
        Baud: 19200,8,N,1
        Port: /dev/ttyUSB0
        Host: Laptop-05
"""


class SetupMixin:
    """
    """

    def setUp(self):
        self.m_pyhouse_obj = SetupPyHouseObj().BuildPyHouseObj()
        self.m_api = configApi(self.m_pyhouse_obj)
        l_yaml = YAML()
        self.m_test_config = l_yaml.load(TEST_YAML)


class A0(unittest.TestCase):

    def test_00_Print(self):
        _x = PrettyFormatAny.form('_test', 'title')  # so it is defined when printing is cleaned up.
        print('Id: test_Serial_driver')


class A1_setup(SetupMixin, unittest.TestCase):
    """ Test SetupMixin
    """

    def test_00(self):
        print('A1-00')
        pass

    def test_01_yaml(self):
        l_yaml = self.m_test_config
        # print('A1-01-A - Yaml: {}'.format(l_yaml))
        self.assertIsNotNone(l_yaml)


class B1_Config(SetupMixin, unittest.TestCase):
    """
    """

    def setUp(self):
        SetupMixin.setUp(self)
        self.m_yaml = self.m_test_config['Controllers'][0]['Interface']

    def test_00(self):
        print('B1-00')
        pass

    def test_01_Interface(self):
        """ Test we have Interface: section
        """
        # print('B1-01-A - Yaml {}'.format(self.m_yaml))
        self.assertEqual(self.m_yaml['Type'], 'Serial')

    def test_02_Baud(self):
        """
        """
        l_baud = self.m_yaml['Baud']
        print('B1-02-A - Yaml {}'.format(l_baud))
        self.assertEqual(l_baud, '19200,8,N,1')


class C1_Parsed(SetupMixin, unittest.TestCase):
    """
    """

    def setUp(self):
        SetupMixin.setUp(self)

    def test_00(self):
        print('C1-00')
        pass

    def test_01_Port(self):
        """ test find_port
        """
        l_port = Serial_driver.FindPort().get_port()
        print(PrettyFormatAny.form(l_port, 'Port'))


class D1_Driver(SetupMixin, unittest.TestCase):
    """
    """

    def setUp(self):
        SetupMixin.setUp(self)

    def test_00(self):
        print('D1-00')
        pass

# ## END
