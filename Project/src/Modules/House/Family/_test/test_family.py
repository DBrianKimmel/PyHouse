"""
@name:      Modules/House/Family/_test/test_family.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2013-2020 by D. Brian Kimmel
@note:      Created on May 17, 2013
@license:   MIT License
@summary:   This module is for testing family.

Passed all 2 tests.  DBK 2020-02-21
"""

__updated__ = '2020-02-21'

# Import system type stuff
from twisted.trial import unittest

# Import PyMh files and modules.
from _test.testing_mixin import SetupPyHouseObj
from Modules.House.Family.family import \
    FamilyModuleInformation

from Modules.Core.Utilities.debug_tools import PrettyFormatAny


class SetupMixin(object):

    def setUp(self):
        self.m_pyhouse_obj = SetupPyHouseObj().BuildPyHouseObj()
        self.m_yaml = SetupPyHouseObj().BuildYaml(None)
        self.m_filename = 'families.yaml'

    def createFamilyObj(self):
        l_family_obj = FamilyModuleInformation()
        l_family_obj.Name = 'Insteon'
        l_family_obj.Key = 0
        l_family_obj.Active = True
        l_family_obj.FamilyPackageName = 'Modules.House.Family.Insteon'
        return l_family_obj


class A0(unittest.TestCase):

    def test_00_Print(self):
        _x = PrettyFormatAny.form('_test', 'title', 190)  # so it is defined when printing is cleaned up.
        print('Id: test_family')


class A1_Validate(SetupMixin, unittest.TestCase):
    """ This section tests the _test environment to be valid before testing the "Real" stuff.
    """

    def setUp(self):
        SetupMixin.setUp(self)

    def test_01_Name(self):
        l_name = 'Insteon'
        print('Name: {}'.format(l_name))
        l_lc = l_name.lower()
        print('Name-lc: {}'.format(l_lc))
        l_cap = l_lc.capitalize()
        print('Name-cap: {}'.format(l_cap))

# ## END DBK
