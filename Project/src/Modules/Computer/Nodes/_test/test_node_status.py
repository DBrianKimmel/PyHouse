"""
@name:      Modules/Computer/Nodes/_test/test_node_status.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2016-2019 by D. Brian Kimmel
@license:   MIT License
@note:      Created on Jul 22, 2016
@summary:   Test

Passed all 1 tests - DBK - 2019-09-17

"""

__updated__ = '2019-09-16'

# Import system type stuff
from twisted.trial import unittest

# Import PyMh files
from _test.testing_mixin import SetupPyHouseObj
from Modules.Core.Utilities.debug_tools import PrettyFormatAny


class SetupMixin(object):

    def setUp(self):
        self.m_pyhouse_obj = SetupPyHouseObj().BuildPyHouseObj()


class A0(unittest.TestCase):

    def setUp(self):
        pass

    def test_00_Print(self):
        _x = PrettyFormatAny.form('_test', 'title')  # so it is defined when printing is cleaned up.
        print('Id: test_node_status')

# ## END DBK
