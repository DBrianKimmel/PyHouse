"""
@name:      Modules/House/Family/sonoff/_test/test_sonoff_device.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2019-2019 by D. Brian Kimmel
@note:      Created on Aug 19, 2019
@license:   MIT License
@summary:   This module tests Insteon_device

Passed all 1 tests - DBK - 2019-08-19
"""

__updated__ = '2019-08-19'

# Import system type stuff
from twisted.trial import unittest

# Import PyMh files and modules.
from _test.testing_mixin import SetupPyHouseObj
from Modules.House.Family.sonoff import sonoff_device

from Modules.Core.Utilities.debug_tools import PrettyFormatAny


class SetupMixin(object):

    def setUp(self):
        self.m_pyhouse_obj = SetupPyHouseObj().BuildPyHouseObj()


class A0(unittest.TestCase):

    def test_00_Print(self):
        _x = PrettyFormatAny.form('_test', 'title')  # so it is defined when printing is cleaned up.
        print('Id: test_sonoff_device')

# ## END DBK
