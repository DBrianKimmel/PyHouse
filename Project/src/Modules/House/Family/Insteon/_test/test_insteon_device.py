"""
@name:      Modules/House/Family/Insteon/_test/test_insteon_device.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2011-2020 by D. Brian Kimmel
@note:      Created on Apr 1, 2011
@license:   MIT License
@summary:   This module tests Insteon_device

Passed all 6 tests - DBK - 2020-02-21
"""

__updated__ = '2020-02-21'

# Import system type stuff
from twisted.trial import unittest

# Import PyMh files and modules.
from _test.testing_mixin import SetupPyHouseObj
from Modules.House.Family.Insteon import insteon_device

from Modules.Core.Utilities.debug_tools import PrettyFormatAny


class SetupMixin(object):

    def setUp(self):
        self.m_pyhouse_obj = SetupPyHouseObj().BuildPyHouseObj()


class A0(unittest.TestCase):

    def test_00_Print(self):
        _x = PrettyFormatAny.form('_test', 'title', 190)  # so it is defined when printing is cleaned up.
        print('Id: test_Insteon_device')


class A1_Setup(SetupMixin, unittest.TestCase):
    """
    This section tests the above setup for things we will need further down in the tests.
    """

    def setUp(self):
        SetupMixin.setUp(self)
        self.m_api = insteon_device.Api(self.m_pyhouse_obj)  # Must be done to setup module

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

    def test_03_Family(self):
        """
        """
        print(PrettyFormatAny.form(self.m_pyhouse_obj.House.Lighting, 'A1-03-A - Lighting'))
        self.assertIsNotNone(self.m_pyhouse_obj.House.Lighting)

    def test_04_Insteon(self):
        """
        """
        print(PrettyFormatAny.form(self.m_pyhouse_obj.House.Lighting.Lights, 'A1-04-A - Lights'))
        self.assertIsNotNone(self.m_pyhouse_obj.House.Lighting.Lights)

    def test_04_Device(self):
        """
        """
        print(PrettyFormatAny.form(self.m_pyhouse_obj.House.Lighting.Lights, 'A1-04-A - Lights'))
        self.assertIsNotNone(self.m_pyhouse_obj.House.Lighting.Lights)


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
