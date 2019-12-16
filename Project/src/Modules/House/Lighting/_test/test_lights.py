"""
@name:      Modules/House/Lighting/_test/test_lights.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2014-2019 by D. Brian Kimmel
@note:      Created on May 23, 2014
@license:   MIT License
@summary:   This module is for testing lighting data.

Passed all 11 tests - DBK - 2019-09-16

"""

__updated__ = '2019-12-16'

#  Import system type stuff
from twisted.trial import unittest
from ruamel.yaml import YAML

#  Import PyMh files and modules.
from _test.testing_mixin import SetupPyHouseObj
from Modules.House.Lighting.lights import LocalConfig as lightsConfig

from Modules.Core.Utilities.debug_tools import PrettyFormatAny

TEST_YAML = """\
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
    - Name: Wet Bar
      Comment: This is the PP Wet bar in the livingroom
      Family:
          Name: Insteon
          Address: 44.44.44
      Dimmable: true  # Optional
      Room: Living Room
"""


class SetupMixin(object):
    """
    """

    def setUp(self):
        self.m_pyhouse_obj = SetupPyHouseObj().BuildPyHouseObj()
        l_yaml = YAML()
        self.m_test_config = l_yaml.load(TEST_YAML)


class A0(unittest.TestCase):

    def test_00_Print(self):
        _x = PrettyFormatAny.form('_x', 'title')  # so it is defined when printing is cleaned up.
        print('Id: test_lights')


class A1_Setup(SetupMixin, unittest.TestCase):
    """
    This section tests the above setup for things we will need further down in the tests.
    """

    def setUp(self):
        SetupMixin.setUp(self)

    def test_01_Config(self):
        """ Be sure that the config contains the right stuff.
        """
        # print(PrettyFormatAny.form(self.m_test_config, 'A1-01-A - Config'))
        # print(PrettyFormatAny.form(self.m_pyhouse_obj.House, 'PyHouse House'))
        self.assertIsNotNone(self.m_test_config['Lights'])


class C1_Read(SetupMixin, unittest.TestCase):
    """
    This section tests the reading and writing of config used by lighting_lights.
    """

    def setUp(self):
        SetupMixin.setUp(self)

    def test_01_Light0(self):
        """ Test reading the device portion of the config.
        """
        l_yaml = self.m_test_config['Lights'][0]
        # print('C1-01-A - Yaml: ', l_yaml)
        l_light = lightsConfig(self.m_pyhouse_obj)._extract_one_light(l_yaml)
        # print(PrettyFormatAny.form(l_light, 'C1-01-B - Light'))
        self.assertEqual(l_light.Name, 'Front Door')
        self.assertEqual(l_light.Comment, '')
        self.assertEqual(l_light.DeviceType, 'Lighting')
        self.assertEqual(l_light.DeviceSubType, 'Light')
        self.assertEqual(l_light.Family.Name, 'insteon')
        self.assertEqual(l_light.Family.Address, '11.11.11')

    def test_02_Light1(self):
        """ Test reading the device portion of the config.
        """
        l_yaml = self.m_test_config['Lights'][1]
        # print('C1-02-A - Yaml: ', l_yaml)
        l_light = lightsConfig(self.m_pyhouse_obj)._extract_one_light(l_yaml)
        # print(PrettyFormatAny.form(l_light, 'C1-02-B - Light'))
        self.assertEqual(l_light.Name, 'Garage')
        self.assertEqual(l_light.Comment, '')
        self.assertEqual(l_light.Family.Name, 'insteon')
        self.assertEqual(l_light.Family.Address, '22.22.22')

    def test_03_Light2(self):
        """ Test reading the device portion of the config.
        """
        l_yaml = self.m_test_config['Lights'][2]
        # print('C1-03-A - Yaml: ', l_yaml)
        l_light = lightsConfig(self.m_pyhouse_obj)._extract_one_light(l_yaml)
        # print(PrettyFormatAny.form(l_light, 'C1-03-B - Light'))
        self.assertEqual(l_light.Name, 'Buffet')
        self.assertEqual(l_light.Comment, 'x')
        self.assertEqual(l_light.Family.Name, 'insteon')
        self.assertEqual(l_light.Family.Address, '33.33.33')

    def test_09_Lights(self):
        """ Test reading of the Lights config file.
        """
        l_yaml = self.m_test_config['Lights']
        # print(PrettyFormatAny.form(l_yaml, 'C1-09-A - Yaml'))
        l_lights = lightsConfig(self.m_pyhouse_obj)._extract_all_lights(l_yaml)
        print(PrettyFormatAny.form(l_lights, 'C1-09-B - Node'))
        self.assertEqual(l_lights[0].Name, 'Front Door')
        self.assertEqual(l_lights[1].Name, 'Garage')
        self.assertEqual(l_lights[2].Name, 'Buffet')


class C2_Write(SetupMixin, unittest.TestCase):
    """
    This section tests the reading and writing of the Yaml config file  used by lighting_lights.
    """

    def setUp(self):
        SetupMixin.setUp(self)
        self.m_yaml = self.m_test_config['Lights']
        self.m_lights = lightsConfig(self.m_pyhouse_obj)._extract_all_lights(self.m_yaml)
        self.m_pyhouse_obj.House.Lights = self.m_lights

    def test_01_Light0(self):
        """Test the write for proper XML Base elements
        """
        l_light = self.m_lights[0]
        print(PrettyFormatAny.form(l_light, 'C2-01-B - Light0'))
        l_config = lightsConfig(self.m_pyhouse_obj)._save_one_light(l_light)
        print(PrettyFormatAny.form(l_config, 'C2-01-D - Light'))

    def test_02_Light1(self):
        """Test the write for proper XML Base elements
        """
        l_light = self.m_yaml[1]
        print(PrettyFormatAny.form(l_light, 'C2-02-A - Light'))
        l_lights = lightsConfig(self.m_pyhouse_obj)._extract_all_lights(self.m_test_config['Lights'])
        print(PrettyFormatAny.form(l_lights, 'C2-01-A - Lights'))
        l_config = lightsConfig(self.m_pyhouse_obj)._save_all_lights()
        print(PrettyFormatAny.form(l_config, 'C2-01-A - Node'))

    def test_09_Lights(self):
        """Test the write for proper XML Base elements
        """
        l_lights = lightsConfig(self.m_pyhouse_obj)._extract_all_lights(self.m_test_config['Lights'])
        print(PrettyFormatAny.form(l_lights, 'C2-01-A - Lights'))
        l_config = lightsConfig(self.m_pyhouse_obj)._save_all_lights()
        print(PrettyFormatAny.form(l_config, 'C2-01-A - Node'))


class Z9_YamlWrite(SetupMixin, unittest.TestCase):
    """
    This section tests the reading and writing of the Yaml config file  used by lighting_lights.
    """

    def setUp(self):
        SetupMixin.setUp(self)

    def test_01_(self):
        """Test the write for proper XML Base elements
        """
        # print(PrettyFormatAny.form(self.m_pyhouse_obj.House.Lighting.Lights, 'C2-01-A - Node'))
        pass

#  ## END DBK
