"""
@name:      PyHouse/src/Modules.Core.Utilities.test_tools.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: 2013-2017 by D. Brian Kimmel
@note:      Created on Apr 11, 2013
@license:   MIT License
@summary:   Various functions and utility methods.

Passed all 3 tests - DBK - 2016-11-22

"""

__updated__ = '2020-02-17'

#  Import system type stuff
from twisted.trial import unittest

#  Import PyMh files
from Modules.Core.Utilities.obj_defs import GetPyhouse
from Modules.House.Lighting.Lights.lights import Api as lightsApi
from Modules.House.Family.family import Api as familyApi
from _test.testing_mixin import SetupPyHouseObj


class SetupMixin(object):
    """
    """

    def setUp(self, p_root):
        self.m_pyhouse_obj = SetupPyHouseObj().BuildPyHouseObj(p_root)
        self.m_xml = SetupPyHouseObj().BuildXml(p_root)
        self.m_version = '1.4.0'


class A0(unittest.TestCase):

    def setUp(self):
        pass

    def test_00_Print(self):
        print('Id: test_tools')


class C1_Find(SetupMixin, unittest.TestCase):

    def setUp(self):
        SetupMixin.setUp(self)
        self.m_api = GetPyhouse(self.m_pyhouse_obj)
        self.m_light_api = lightsApi()
        self.m_pyhouse_obj._Families = familyApi(self.m_pyhouse_obj).m_family
        self.m_pyhouse_obj.House.Lighting.Lights = self.m_light_api.read_all_lights_xml(self.m_pyhouse_obj)

    def test_01_Setup(self):
        _l_loc = self.m_api.Location().Latitude
        #  print(l_loc)

#  ## END DBK
