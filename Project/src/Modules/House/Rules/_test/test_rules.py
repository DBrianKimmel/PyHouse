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

__updated__ = '2019-08-01'

#  Import system type stuff
from twisted.trial import unittest

#  Import PyMh files and modules.
from test.testing_mixin import SetupPyHouseObj
from Modules.Core.Utilities.config_tools import Yaml as configYaml

from Modules.Core.Utilities.debug_tools import PrettyFormatAny


class SetupMixin(object):
    """
    """

    def setUp(self):
        self.m_pyhouse_obj = SetupPyHouseObj().BuildPyHouseObj()
        self.m_yaml = SetupPyHouseObj().BuildYaml(None)


class A0(unittest.TestCase):

    def test_00_Print(self):
        _x = PrettyFormatAny.form('_test', 'title', 190)  # so it is defined when printing is cleaned up.
        print('Id: test_rules')


class C1_ConfigRead:
    """
    """

# ## END DBK
