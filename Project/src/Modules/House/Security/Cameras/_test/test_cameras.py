"""
@name:      /home/briank/workspace/PyHouse/Project/src/Modules/House/Security/Cameras/_test/test_cameras.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2020-2020 by D. Brian Kimmel
@note:      Created on Feb 2, 2020
@license:   MIT License
@summary:   This

Passed all 5 tests - DBK - 2019-12-29
"""

__updated__ = '2020-02-02'

# Import system type stuff
from twisted.trial import unittest
from ruamel.yaml import YAML

# Import PyMh files and modules.
from _test.testing_mixin import SetupPyHouseObj
from Modules.House.Security.Cameras.cameras import Api as camerasApi, LocalConfig as camerasConfig

from Modules.Core.Utilities.debug_tools import PrettyFormatAny

TEST_YAML = """\
Cameras:
    - Name: Camera-01
      Comment: Outside Garage
      Mac:  E8:AB:FA:8F:73:06
      Family:
          Name: reolink
          Address: camera-01-pp
      Access:
          Name: admin
          Password: blank

    - Name: Camera-02
      Comment: Front Walk
      Mac:  E8
      Family:
          Name: reolink
          Address: camera-02-pp
      Access:
          Name: admin
          Password: blank
"""


class SetupMixin(object):
    """
    """

    def setUp(self):
        self.m_pyhouse_obj = SetupPyHouseObj().BuildPyHouseObj()
        l_yaml = YAML()
        self.m_test_config = l_yaml.load(TEST_YAML)
        self.m_config = camerasConfig(self.m_pyhouse_obj)


class A0(unittest.TestCase):

    def test_00_Print(self):
        print('Id: test_setup_pyhouse')
        _x = PrettyFormatAny.form('_test', 'title', 190)  # so it is defined when printing is cleaned up.


class A1_Setup(SetupMixin, unittest.TestCase):
    """
    This section tests the above setup for things we will need further down in the tests.
    """

    def setUp(self):
        SetupMixin.setUp(self)
        self.m_api = camerasApi(self.m_pyhouse_obj)

    def test_01_Pyhouse(self):
        """
        """
        print(PrettyFormatAny.form(self.m_pyhouse_obj, 'A1-01-A - PyHouse'))
        self.assertIsNotNone(self.m_pyhouse_obj)

    def test_02_House(self):
        """
        """
        print(PrettyFormatAny.form(self.m_pyhouse_obj.House, 'A1-02-A - House'))
        self.assertIsNotNone(self.m_pyhouse_obj.House)

    def test_03_Security(self):
        """
        """
        print(PrettyFormatAny.form(self.m_pyhouse_obj.House.Security, 'A1-03-A - Security'))
        self.assertIsNotNone(self.m_pyhouse_obj.House.Security)

    def test_04_Cameras(self):
        """
        """
        print(PrettyFormatAny.form(self.m_pyhouse_obj.Security.Cameras, 'A1-04-A - Cameras'))
        self.assertIsNotNone(self.m_pyhouse_obj.House.Security.Cameras)

# ## END DBK
