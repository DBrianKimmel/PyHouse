"""
@name:      PyHouse/Project/src/Modules/Core/_test/test_setup_pyhouse.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2019-2019 by D. Brian Kimmel
@note:      Created on Oct 20, 2019
@license:   MIT License
@summary:   This

Passed all 19 tests - DBK - 2019-06-18
"""

__updated__ = '2019-10-21'

# Import system type stuff
from twisted.trial import unittest

# Import PyMh files and modules.
from _test.testing_mixin import SetupPyHouseObj
from Modules.Core.Utilities.debug_tools import PrettyFormatAny


class SetupMixin(object):
    """
    """

    def setUp(self):
        self.m_pyhouse_obj = SetupPyHouseObj().BuildPyHouseObj()


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

    def test_01_PyHouseObj(self):
        print(PrettyFormatAny.form(self.m_pyhouse_obj, 'A1-01-A - PyHouse'))
        print(PrettyFormatAny.form(self.m_pyhouse_obj._Config, 'A1-01-A - PyHouse.Xml'))
        self.assertNotEqual(self.m_pyhouse_obj._Config, None)

