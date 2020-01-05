"""
@name:      Modules/Computer/Internet/_test/test_inet_update_dyn_dns.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com>
@copyright: (c) 2014-2020 by D. Brian Kimmel
@license:   MIT License
@note:      Created on Jun 27, 2014
@Summary:

Passed all 3 tests - DBK - 2020-01-02

"""

__updated__ = '2020-01-02'

# Import system type stuff
from twisted.trial import unittest

# Import PyMh files and modules.
from _test.testing_mixin import SetupPyHouseObj
from Modules.Core.Utilities.debug_tools import PrettyFormatAny


class SetupMixin(object):
    """
    Set up pyhouse_obj and xml element pointers
    """

    def setUp(self):
        self.m_pyhouse_obj = SetupPyHouseObj().BuildPyHouseObj()


class A0(unittest.TestCase):

    def setUp(self):
        pass

    def test_00_Print(self):
        _x = PrettyFormatAny.form('_test', 'title')  # so it is defined when printing is cleaned up.
        print('Id: test_inet_update_dyn_dns')


class A1_Setup(SetupMixin, unittest.TestCase):
    """
    This section will verify the XML in the 'Modules.text.xml_data' file is correct and what the node_local
        module can read/write.
    """

    def setUp(self):
        SetupMixin.setUp(self)

    def test_01_PyHouse(self):
        print(PrettyFormatAny.form(self.m_pyhouse_obj, 'A1-01-A - PyHouse'))
        self.assertNotEqual(self.m_pyhouse_obj, None)

    def test_02_Computer(self):
        print(PrettyFormatAny.form(self.m_pyhouse_obj.Computer, 'A1-02-A - House'))
        self.assertNotEqual(self.m_pyhouse_obj.Computer, None)

# ## END DBK
