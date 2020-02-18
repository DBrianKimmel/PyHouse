"""
@name:      Modules/Core/_test/test_core.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2019-2020 by D. Brian Kimmel
@note:      Created on Oct 20, 2019
@license:   MIT License
@summary:   This

Passed all 7 tests - DBK - 2020-02-13
"""

__updated__ = '2020-02-17'

# Import system type stuff
from twisted.trial import unittest
from ruamel.yaml import YAML

# Import PyMh files and modules.
from _test.testing_mixin import SetupPyHouseObj
from Modules.Core import core, MODULES
from Modules.Core.core import Api as coreApi

from Modules.Core.Utilities.debug_tools import PrettyFormatAny

TEST_YAML = """\
PyHouse:
   Name: PinkPoppy
   Units: metric
   Version: 2
"""


class SetupMixin(object):
    """
    """

    def setUp(self):
        self.m_pyhouse_obj = SetupPyHouseObj().BuildPyHouseObj()
        l_yaml = YAML()
        self.m_test_config = l_yaml.load(TEST_YAML)
        self.m_api = core.Api()
        self.m_util = core.Utility(self.m_pyhouse_obj)


class A0(unittest.TestCase):

    def test_00_Print(self):
        print('Id: test_setup_pyhouse')
        _x = PrettyFormatAny.form('_test', 'title', 190)  # so it is defined when printing is cleaned up.


class A1_Setup(SetupMixin, unittest.TestCase):
    """
    This section tests the setup of the _test
    """

    def setUp(self):
        SetupMixin.setUp(self)

    def test_01_PyHouse(self):
        # print(PrettyFormatAny.form(self.m_pyhouse_obj, 'A1-01-A - PyHouse'))
        self.assertNotEqual(self.m_pyhouse_obj, None)

    def test_02_Core(self):
        # print(PrettyFormatAny.form(self.m_pyhouse_obj.Core, 'A1-02-A - Core'))
        self.assertNotEqual(self.m_pyhouse_obj.Core, None)

    def test_03_Comuter(self):
        # print(PrettyFormatAny.form(self.m_pyhouse_obj.Computer, 'A1-03-A - Comouter'))
        self.assertNotEqual(self.m_pyhouse_obj.Computer, None)

    def test_04_House(self):
        # print(PrettyFormatAny.form(self.m_pyhouse_obj.House, 'A1-04-A - House'))
        self.assertNotEqual(self.m_pyhouse_obj.House, None)


class B1_Utility(SetupMixin, unittest.TestCase):
    """
    This section tests the setup of the _test
    """

    def setUp(self):
        SetupMixin.setUp(self)

    def test_01_One(self):
        l_item = self.m_util._initialize_one_item('Mqtt', 'Modules.Core.')
        print(PrettyFormatAny.form(self.m_pyhouse_obj, 'A1-01-A - PyHouse'))
        self.assertNotEqual(self.m_pyhouse_obj, None)


class C1_Config(SetupMixin, unittest.TestCase):
    """
    This section tests the setup of the _test
    """

    def setUp(self):
        SetupMixin.setUp(self)
        self.m_api = coreApi()  # Must be done to setup module

    def test_01_PyHouse(self):
        l_yaml = self.m_test_config['PyHouse']
        print('C1-01-A - Yaml: ', l_yaml)
        l_param = self.m_config._extract_pyhouse_info(l_yaml)
        print(PrettyFormatAny.form(l_param, 'C1-01-B - Partams'))


class E1_Setup(SetupMixin, unittest.TestCase):
    """
    This section tests the setup of the _test
    """

    def setUp(self):
        SetupMixin.setUp(self)

    def test_01_PyHouse(self):
        print(PrettyFormatAny.form(self.m_pyhouse_obj, 'A1-01-A - PyHouse'))
        self.assertNotEqual(self.m_pyhouse_obj, None)

# ## END DBK
