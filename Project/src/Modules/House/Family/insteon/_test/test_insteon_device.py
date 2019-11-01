"""
@name:      Modules/House/Family/insteon/_test/test_insteon_device.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2011-2019 by D. Brian Kimmel
@note:      Created on Apr 1, 2011
@license:   MIT License
@summary:   This module tests Insteon_device

Passed all 1 tests - DBK - 2015-07-26
"""

__updated__ = '2019-10-16'

# Import system type stuff
from twisted.trial import unittest

# Import PyMh files and modules.
from _test.testing_mixin import SetupPyHouseObj
from Modules.House.Family.insteon import insteon_device

from Modules.Core.Utilities.debug_tools import PrettyFormatAny


class SetupMixin(object):

    def setUp(self):
        self.m_pyhouse_obj = SetupPyHouseObj().BuildPyHouseObj()


class A0(unittest.TestCase):

    def test_00_Print(self):
        _x = PrettyFormatAny.form('_test', 'title', 190)  # so it is defined when printing is cleaned up.
        print('Id: test_Insteon_device')


class A1_Setup(SetupMixin, unittest.TestCase):
    """Test that we have set up properly for the rest of the testing classes.
    """

    def setUp(self):
        SetupMixin.setUp(self)

    def test_01_Build(self):
        """ The basic read info as set up
        """
        # print(PrettyFormatAny.form(self.m_pyhouse_obj, 'A1-01-A - PyHouse'))
        # print(PrettyFormatAny.form(self.m_pyhouse_obj.House, 'A1-01-B - House'))
        self.assertIsInstance(self.m_pyhouse_obj.House.Family, dict)


class C01_Api(SetupMixin, unittest.TestCase):
    """ This section tests the reading and writing of XML used by node_local.
    """

    def setUp(self):
        SetupMixin.setUp(self)
        self.m_api = insteon_device.Api(self.m_pyhouse_obj)

    def test_01_Init(self):
        """ Be sure that the XML contains the right stuff.
        """
        pass

# def suite():
#    suite = unittest.TestSuite()
#    # suite.addTest(Test_02_Api('test_0202_Init'))
#    return suite

# ## END
