"""
@name:      Modules/Core/_test/test_core.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2019-2020 by D. Brian Kimmel
@note:      Created on Oct 20, 2019
@license:   MIT License
@summary:   This

Passed all 5 tests - DBK - 2019-12-29
"""

__updated__ = '2019-12-29'

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

    def test_01_PyHouse(self):
        print(PrettyFormatAny.form(self.m_pyhouse_obj, 'A1-01-A - PyHouse'))
        self.assertNotEqual(self.m_pyhouse_obj, None)

    def test_02_Core(self):
        print(PrettyFormatAny.form(self.m_pyhouse_obj.Core, 'A1-02-A - Core'))
        self.assertNotEqual(self.m_pyhouse_obj.Core, None)

    def test_03_Comuter(self):
        print(PrettyFormatAny.form(self.m_pyhouse_obj.Computer, 'A1-03-A - Comouter'))
        self.assertNotEqual(self.m_pyhouse_obj.Computer, None)

    def test_04_House(self):
        print(PrettyFormatAny.form(self.m_pyhouse_obj.House, 'A1-04-A - House'))
        self.assertNotEqual(self.m_pyhouse_obj.House, None)

# ## END DBK
