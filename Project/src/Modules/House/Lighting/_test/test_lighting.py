"""
@name:      Modules/House/Lighting/_test/test_lighting.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2013-2020 by D. Brian Kimmel
@note:      Created on Apr 9, 2013
@license:   MIT License
@summary:   Test the home lighting system automation.

Passed all 6 tests.  DBK 2019-12-30

"""

__updated__ = '2019-12-30'

# Import system type stuff
from twisted.trial import unittest

# Import PyMh files and modules.
from _test.testing_mixin import SetupPyHouseObj

from Modules.Core.Utilities.debug_tools import PrettyFormatAny


class SetupMixin(object):

    def setUp(self):
        self.m_pyhouse_obj = SetupPyHouseObj().BuildPyHouseObj()


class A0(unittest.TestCase):

    def test_00_Id(self):
        _x = PrettyFormatAny.form('_test', 'title', 190)  # so it is defined when printing is cleaned up.
        print('Id: test_lighting')


class A1_Setup(SetupMixin, unittest.TestCase):
    """ This section tests the master setup above this.
    """

    def setUp(self):
        SetupMixin.setUp(self)

    def test_01_Pyhouse(self):
        """
        """
        # print(PrettyFormatAny.form(self.m_pyhouse_obj, 'A1-01-A - PyHouse'))
        self.assertIsNotNone(self.m_pyhouse_obj)

    def test_02_House(self):
        """
        """
        # print(PrettyFormatAny.form(self.m_pyhouse_obj.House, 'A1-02-A - House'))
        self.assertIsNotNone(self.m_pyhouse_obj.House)

    def test_03_Lighting(self):
        """
        """
        # print(PrettyFormatAny.form(self.m_pyhouse_obj.House.Lighting, 'A1-03-A - Lighting'))
        self.assertIsNotNone(self.m_pyhouse_obj.House.Lighting)


class C1_YamlRead(SetupMixin, unittest.TestCase):
    """ This section tests Yaml config reading
    """

    def setUp(self):
        SetupMixin.setUp(self)

    def test_01_Setup(self):
        """
        """


class C2_YamlWrite(SetupMixin, unittest.TestCase):
    """ This section tests the utility class
    """

    def setUp(self):
        SetupMixin.setUp(self)

    def test_01_lighting(self):
        """Write out the 'LightingSection' which contains the 'LightSection',
        """

# ## END DBK
