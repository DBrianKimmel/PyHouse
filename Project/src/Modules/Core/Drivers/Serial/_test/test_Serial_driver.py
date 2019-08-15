"""
@name:      Modules/Core/Drivers/Serial/_test/test_Serial_driver.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2013_2019 by D. Brian Kimmel
@license:   MIT License
@note:      Created on May 4, 2013
@summary:   This module is for testing local node data.

Passed all 4 tests - DBK - 2019-08-15

"""

__updated__ = '2019-08-15'

# Import system type stuff
from twisted.trial import unittest

# Import PyMh files and modules.
from _test.testing_mixin import SetupPyHouseObj
from Modules.Core.Utilities import config_tools
from Modules.Core.Drivers.Serial import Serial_driver
from Modules.Core.Utilities.debug_tools import PrettyFormatAny

YAML_FILENAME = 'serial.yaml'


class SetupMixin:
    """
    """

    def setUp(self):
        self.m_pyhouse_obj = SetupPyHouseObj().BuildPyHouseObj()

    def GetNode(self):
        """
        """
        l_node = config_tools.Yaml(self.m_pyhouse_obj).read_yaml(YAML_FILENAME)
        return l_node

    def GetYaml(self):
        return self.GetNode().Yaml


class A0(unittest.TestCase):

    def test_00_Print(self):
        _x = PrettyFormatAny.form('_test', 'title', 190)  # so it is defined when printing is cleaned up.
        print('Id: test_Serial_driver')


class A1(SetupMixin, unittest.TestCase):
    """ Test SetupMixin
    """

    def test_01_node(self):
        l_node = self.GetNode()
        # print(PrettyFormatAny.form(l_node, 'A1-01-A - Node'))
        self.assertEqual(l_node.FileName, YAML_FILENAME)

    def test_02_yaml(self):
        l_yaml = self.GetYaml()
        # print('A1-02-A - Yaml: {}'.format(l_yaml))
        self.assertIsNotNone(l_yaml)


class B1_Config(SetupMixin, unittest.TestCase):
    """
    """

    def setUp(self):
        SetupMixin.setUp(self)
        self.m_config = self.GetYaml()

    def test_01_Interface(self):
        """ Test we have Interface: section
        """
        l_yaml = self.GetYaml()['Interface']
        # print('B1-01-A - Yaml {}'.format(l_yaml))
        self.assertIsNotNone(l_yaml)

    def test_02_Baud(self):
        """
        """
        l_yaml = self.GetYaml()['Interface']['Baud']
        print('B1-02-A - Yaml {}'.format(l_yaml))
        self.assertIsNotNone(l_yaml)

    def test_03_Rate(self):
        """
        """
        l_obj = Serial_driver.SerialInformation()
        print(PrettyFormatAny.form(l_obj, 'B1-03-A - Serial'))
        l_yaml = self.GetYaml()['Interface']['Baud']
        print('B1-03-B - Yaml {}'.format(l_yaml))
        l_ret = Serial_driver.Config()._extract_baud(l_yaml, l_obj)
        print(PrettyFormatAny.form(l_ret, 'B1-03-C - Serial'))

# ## END
