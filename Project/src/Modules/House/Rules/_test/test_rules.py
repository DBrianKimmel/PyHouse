"""
@name:      Modules/House/Rules/_test/test_rules.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2019-2019 by D. Brian Kimmel
@license:   MIT License
@note:      Created on Aug  1, 2019
@Summary:

Passed all 2 tests - DBK - 2019-08-01

"""

__updated__ = '2019-12-20'

#  Import system type stuff
from twisted.trial import unittest
from ruamel.yaml import YAML

#  Import PyMh files and modules.
from _test.testing_mixin import SetupPyHouseObj
from Modules.House.Rules.rules import CONFIG_NAME

from Modules.Core.Utilities.debug_tools import PrettyFormatAny

TEST_YAML_1 = """\
Rules:
    - Name: rule-01
      Comment: Test comment
      Trigger:
          Type: Security
          Device: Garage Door
          Event: Open
      Action:
          Type: Lighting
          Device: Garage Outside
          Event: On
          Set: GarageOpen
"""


class SetupMixin(object):
    """
    """

    def setUp(self):
        self.m_pyhouse_obj = SetupPyHouseObj().BuildPyHouseObj()
        self.m_yaml = SetupPyHouseObj().BuildYaml(None)
        l_yaml = YAML()
        self.m_test_config = l_yaml.load(TEST_YAML_1)


class A0(unittest.TestCase):

    def test_00_Print(self):
        _x = PrettyFormatAny.form('_test', 'title', 190)  # so it is defined when printing is cleaned up.
        print('Id: test_rules')


class B1_Config(SetupMixin, unittest.TestCase):
    """ Test converting a datetime to seconds
    """

    def setUp(self):
        SetupMixin.setUp(self)
        self.m_sched_config = self.m_test_config['Schedules']

    def test_01_Name0(self):
        """ Sched 0 Name extraction
        """
        # print('B1-01-A C', self.m_sched_config[0])
        l_ret = scheduleConfig(self.m_pyhouse_obj)._extract_one_schedule(self.m_sched_config[0])
        # print(PrettyFormatAny.form(l_ret, 'B1-01-B - Schedule'))
        self.assertEqual(l_ret.Name, 'Livingroom Ceiling On')


class C1_ConfigRead:
    """
    """

# ## END DBK
