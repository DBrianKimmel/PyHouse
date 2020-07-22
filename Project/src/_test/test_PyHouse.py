"""
@name:      PyHouse/src/_test/test_PyHouse.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2015-2019 by D. Brian Kimmel
@license:   MIT License
@note:      Created on May 29, 2014
@Summary:

"""

__updated__ = '2019-10-08'

# Import system type stuff
from twisted.trial import unittest

# Import PyMh files and modules.
# from Modules.House._test import test_house
import PyHouse
from _test.testing_mixin import SetupPyHouseObj


class SetupMixin(object):
    """
    """

    def setUp(self):
        self.m_pyhouse_obj = SetupPyHouseObj().BuildPyHouseObj()


class A0(unittest.TestCase):

    def setUp(self):
        pass

    def test_00_Print(self):
        print('Id: test_PyHouse')


class Test_01_Api(SetupMixin, unittest.TestCase):

    def setUp(self):
        SetupMixin.setUp(self)

    def test_0101_Init(self):
        l_api = PyHouse.Api()

# ## END DBK
