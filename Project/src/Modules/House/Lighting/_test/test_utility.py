"""
@name:      Modules/House/Lighting/_test/test_utility.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2019-2019 by D. Brian Kimmel
@license:   MIT License
@note:      Created on Jan 20, 2019
@summary:   Test

"""

__updated__ = '2019-12-08'

# Import system type stuff
from twisted.trial import unittest
from ruamel.yaml import YAML

# Import PyMh files and modules.
from _test.testing_mixin import SetupPyHouseObj
from Modules.House.Lighting.utility import lightingUtility
from Modules.House.Lighting.lights import LocalConfig as lightsConfig
from Modules.House.Lighting.outlets import LocalConfig as outletsConfig

from Modules.Core.Utilities.debug_tools import PrettyFormatAny

TEST_LIGHTS = """\
Lights:
    - Name: Front Door
      Room: Outside
      Family:
          Name: Insteon
          Address: 11.11.11
    - Name: Garage
      Room: Outside
      Dimmable: true
      Family:
         Name: Insteon
         Address: 22.22.22
    - Name: Buffet
      Comment: x
      Room: Dining Room
      Family:
          Name: Insteon
          Address: 33.33.33
"""
TEST_OUTLETS = """\
Outlets:
    - Name: Musicroom Lamp
      Room: Music
      Family:
          Name: Insteon
          Address: 99.99.99

    - Name: Christmas
      Comment: ??
      Family:
          Name: Insteon
          Address: 88.88.88

    - Name: Gameroom Lamp
      Room: Game
      Comment: Fireplace end
      Family:
          Name: Insteon
          Address: 77.77.77

"""


class SetupMixin(object):

    def setUp(self):
        self.m_pyhouse_obj = SetupPyHouseObj().BuildPyHouseObj()
        l_yaml = YAML()
        self.m_test_config_lights = l_yaml.load(TEST_LIGHTS)['Lights']
        self.m_test_config_outlets = l_yaml.load(TEST_OUTLETS)['Outlets']


class A0(unittest.TestCase):

    def setUp(self):
        pass

    def test_00_Print(self):
        _x = PrettyFormatAny.form('_x', 'title')  # so it is defined when printing is cleaned up.
        print('Id: test_lighting_utility')


class B1_Test(SetupMixin, unittest.TestCase):
    """ This section tests lookup
    """

    def setUp(self):
        SetupMixin.setUp(self)
        self.m_lights = lightsConfig(self.m_pyhouse_obj)._extract_all_lights(self.m_test_config_lights)

    def test_01_Name0(self):
        """
        """
        l_obj = self.m_lights[0]
        # print(PrettyFormatAny.form(l_obj, 'B1-01-A - Light'))
        l_ret = lightingUtility()._test_object_by_id(l_obj, name='Front Door')
        # print(PrettyFormatAny.form(l_ret, 'B1-01-B - Light'))
        self.assertEqual(l_ret.Name, 'Front Door')

    def test_02_Name1(self):
        """
        """
        l_obj = self.m_lights[1]
        # print(PrettyFormatAny.form(l_obj, 'B1-02-A - Light'))
        l_ret = lightingUtility()._test_object_by_id(l_obj, name='Garage')
        # print(PrettyFormatAny.form(l_ret, 'B1-02-B - Light'))
        self.assertEqual(l_ret.Name, 'Garage')


class B2_Get(SetupMixin, unittest.TestCase):
    """ This section tests object lookup by some ID
    """

    def setUp(self):
        SetupMixin.setUp(self)
        self.m_lights = lightsConfig(self.m_pyhouse_obj)._extract_all_lights(self.m_test_config_lights)
        self.m_outlets = outletsConfig(self.m_pyhouse_obj)._extract_all_outlets(self.m_test_config_lights)
        self.m_pyhouse_obj.House.Lighting.Lights = self.m_lights
        self.m_pyhouse_obj.House.Lighting.Outlets = self.m_outlets

    def test_01_Light(self):
        """ Lookup by name
        """
        l_objs = self.m_pyhouse_obj.House.Lighting
        # print(PrettyFormatAny.form(l_objs, 'B2-01-A - Lights'))
        l_ret = lightingUtility().get_object_type_by_id(l_objs, name='Front Door')
        # print(PrettyFormatAny.form(l_ret, 'B2-01-B - Light'))
        self.assertEqual(l_ret.Name, 'Front Door')

    def test_02_Light(self):
        """ Lookup by name
        """
        l_objs = self.m_pyhouse_obj.House.Lighting
        # print(PrettyFormatAny.form(l_objs, 'B2-02-A - Lights'))
        l_ret = lightingUtility().get_object_type_by_id(l_objs, name='Garage')
        # print(PrettyFormatAny.form(l_ret, 'B2-02-B - Light'))
        self.assertEqual(l_ret.Name, 'Garage')

    def test_04_Outlet(self):
        """ Lookup by UUID
        """
        l_objs = self.m_pyhouse_obj.House.Lighting
        # print(PrettyFormatAny.form(l_objs, 'B2-04-A - Lights'))
        l_ret = lightingUtility().get_object_type_by_id(l_objs, name='Musicroom Lamp')
        # print(PrettyFormatAny.form(l_ret, 'B2-04-B - Light'))
        self.assertEqual(l_ret.Name, 'Musicroom Lamp')

    def test_05_Outlet(self):
        """ Lookup object by non-existant key (to _test failure
        Logs an error.
        """
        l_objs = self.m_pyhouse_obj.House.Lighting
        # print(PrettyFormatAny.form(l_objs, 'B2-01-A - Lights'))
        l_ret = lightingUtility().get_object_type_by_id(l_objs, name='')
        # print(PrettyFormatAny.form(l_ret, 'B2-01-B - Light'))
        self.assertEqual(l_ret.Name, 'Musicroom Lamp')


class C1_ByFamuly(SetupMixin, unittest.TestCase):
    """ This section tests lookup
    """

    def setUp(self):
        SetupMixin.setUp(self)

    def test_01_Name(self):
        """ Write out the XML file for the Base controller
        """
        l_objs = self.m_controllers
        # print(PrettyFormatAny.form(l_objs, 'C1-01-A - Controllers'))
        l_ret = lightingUtility().get_controller_objs_by_family(l_objs, 'Insteon')
        # print(PrettyFormatAny.form(l_ret, 'C1-01-B - Controller'))
        # self.assertEqual(l_ret.Name, TESTING_CONTROLLER_NAME_0)

# ## END DBK
