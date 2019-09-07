"""
@name:       Modules/Core/Utilities/_test/test_coordinate_tools.py
@author:     D. Brian Kimmel
@contact:    d.briankimmel@gmail.com
@copyright:  2016-2019 by D. Brian Kimmel
@date:       Created on Jun 21, 2016
@licencse:   MIT License
@summary:

Passed all 5 tests - DBK 2016-11-22

"""

__updated__ = '2019-09-07'

# Import system type stuff
import xml.etree.ElementTree as ET
from twisted.trial import unittest

# Import PyMh files
from _test.testing_mixin import SetupPyHouseObj
from Modules.Core.Utilities.coordinate_tools import Coords
from Modules.Core.Utilities.debug_tools import PrettyFormatAny


class SetupMixin(object):

    def setUp(self):
        self.m_pyhouse_obj = SetupPyHouseObj().BuildPyHouseObj()
        self.m_api = Coords


class A0(unittest.TestCase):

    def test_00_Print(self):
        _x = PrettyFormatAny.form('_test', 'title', 190)  # so it is defined when printing is cleaned up.
        print('Id: test_coordinate_tools')


class B1_Coords(SetupMixin, unittest.TestCase):

    def setUp(self):
        SetupMixin.setUp(self)

    def test_01_Corner(self):
        """
        """
        # print(PrettyFormatAny.form(JSON, 'B1-01 A - Corner'))
        # print(PrettyFormatAny.form(JSON['Corner'], 'B1-01 B - Corner'))
        l_ret = self.m_api._get_coords(JSON['Corner'])
        # print(PrettyFormatAny.form(l_ret, 'B1-01 C - Corner'))
        self.assertEqual(str(l_ret.X_Easting), TESTING_ROOM_CORNER_X_3)
        self.assertEqual(str(l_ret.Y_Northing), TESTING_ROOM_CORNER_Y_3)
        self.assertEqual(str(l_ret.Z_Height), TESTING_ROOM_CORNER_Z_3)

    def test_2_Size(self):
        """
        """
        l_ret = self.m_api._get_coords(JSON['Size'])
        # print(PrettyFormatAny.form(l_ret, 'B1-02-A - Size'))
        self.assertEqual(str(l_ret.X_Easting), TESTING_ROOM_SIZE_X_3)
        self.assertEqual(str(l_ret.Y_Northing), TESTING_ROOM_SIZE_Y_3)
        self.assertEqual(str(l_ret.Z_Height), TESTING_ROOM_SIZE_Z_3)

# ## END DBK
