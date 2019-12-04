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

__updated__ = '2019-12-04'

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
          Address: 46.09.E7
    - Name: Garage
      Room: Outside
      Dimmable: true
      Family:
         Name: Insteon
         Address: 43.F9.AA
    - Name: Buffet
      Comment: x
      Room: Dining Room
      Family:
          Name: Insteon
          Address: 1D.26.6B
    - Name: Wet Bar
      Comment: This is the PP Wet bar in the livingroom
      Family:
          Name: Insteon
          Address: 18.C5.8F
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


class C1_YamlRead(SetupMixin, unittest.TestCase):
    """
    This section tests the reading and writing of config used by lighting_lights.
    """

    def setUp(self):
        SetupMixin.setUp(self)

    def test_01_LightFamily(self):
        """ Test reading the family portion of the light config
        """
        l_yaml = self.m_test_config['Lights'][0]['Family']
        # print('C1-01-A - Yaml: ', l_yaml)
        l_family = lightsConfig(self.m_pyhouse_obj)._extract_family(l_yaml)
        # print(PrettyFormatAny.form(l_family, 'C1-01-B - Family'))
        self.assertEqual(l_family.Name, 'insteon')
        self.assertEqual(l_family.Address, '11.22.33')

    def test_02_LightDevice(self):
        """ Test reading the device portion of the config.
        """
        l_yaml = self.m_test_config['Lights'][1]
        # print('C1-02-A - Yaml: ', l_yaml)
        l_light = lightsConfig(self.m_pyhouse_obj)._extract_one_light(l_yaml)
        # print(PrettyFormatAny.form(l_light, 'C1-02-B - Light'))
        self.assertEqual(l_light.Name, 'Garage')
        self.assertEqual(l_light.Comment, 'Outside, Downstairs')
        self.assertEqual(l_light.DeviceType, 'Lighting')
        self.assertEqual(l_light.DeviceSubType, 'Light')
        self.assertEqual(l_light.Family.Name, 'insteon')
        self.assertEqual(l_light.Family.Address, '12.34.56')

    def test_03_LightDevice(self):
        """ Test reading the device portion of the config.
        """
        l_yaml = self.m_test_config['Lights'][2]
        print('C1-03-A - Yaml: ', l_yaml)
        l_light = lightsConfig(self.m_pyhouse_obj)._extract_one_light(l_yaml)
        print(PrettyFormatAny.form(l_light, 'C1-03-B - Light'))
        self.assertEqual(l_light.Name, 'Dining Room')
        self.assertEqual(l_light.Comment, None)
        self.assertEqual(l_light.Family.Name, 'insteon')
        self.assertEqual(l_light.Family.Address, '11.33.AA')

    def test_04_LightDevice(self):
        """ Test reading the device portion of the config.
        """
        l_yaml = self.m_test_config['Lights'][3]
        print('C1-04-A - Yaml: ', l_yaml)
        l_light = lightsConfig(self.m_pyhouse_obj)._extract_one_light(l_yaml)
        print(PrettyFormatAny.form(l_light, 'C1-04-B - Light'))
        self.assertEqual(l_light.Name, 'Fireplace')
        self.assertEqual(l_light.Comment, 'This is the fireplace mantle lighting')
        self.assertEqual(l_light.Family.Name, 'insteon')
        self.assertEqual(l_light.Family.Address, '44.33.22')

    def test_05_LightDevice(self):
        """ Test reading the device portion of the config.
        """
        l_yaml = self.m_test_config['Lights'][4]
        print('C1-05-A - Yaml: ', l_yaml)
        l_light = lightsConfig(self.m_pyhouse_obj)._extract_one_light(l_yaml)
        print(PrettyFormatAny.form(l_light, 'C1-05-B - Light'))
        self.assertEqual(l_light.Name, 'TV Lights')
        self.assertIsNone(l_light.Comment)
        self.assertEqual(l_light.Family.Name, 'insteon')
        self.assertEqual(l_light.Family.Address, '11.33.AA')

    def Xtest_06_LightRoom(self):
        """ Test reading the Room portion of the config.
        """
        l_yaml = self.m_node.Yaml['Lights'][0]['Room']
        # l_room = l_yaml['Room']
        # print('C1-03-A - Yaml {}'.format(l_yaml))
        # print(PrettyFormatAny.form(l_yaml, 'C1-01-B - Yaml'))
        l_obj = lightsConfig()._extract_room_location_config(l_yaml)
        # print(PrettyFormatAny.form(l_obj, 'C1-03-E - Room'))
        self.assertEqual(l_obj.Name, 'Living Room')

    def Xtest_07_LightController(self):
        """ Test reading the Controller portion of the config.
        """
        l_yaml = self.m_node.Yaml['Lights'][0]['Controller']
        # print('C1-04-A - Yaml {}'.format(l_yaml))
        # print(PrettyFormatAny.form(l_yaml, 'C1-04-B - Yaml'))
        _l_obj = lightsConfig()._extract_controller_config(l_yaml)
        # print(PrettyFormatAny.form(l_obj, 'C1-04-E - Node'))

    def test_08_Light(self):
        """ Test reading one light portion of the config.
        """
        l_yaml = self.m_node.Yaml['Lights'][0]
        # print('C1-05-A - Yaml {}'.format(l_yaml))
        # print(PrettyFormatAny.form(l_yaml, 'C1-01-B - Yaml'))
        l_obj = lightsConfig()._load_one_light(l_yaml)
        # print(PrettyFormatAny.form(l_obj, 'C1-05-E - Node'))
        self.assertEqual(l_obj.Name, 'Light 1')
        self.assertEqual(l_obj.Comment, 'This is _test light 1')

    def test_09_Lights(self):
        """ Test reading of the Lights config file.
        """
        l_yaml = self.m_node.Yaml['Lights']
        # print(PrettyFormatAny.form(l_yaml, 'C1-01-A - Yaml'))
        l_obj = lightsConfig()._load_all_lights(l_yaml)
        print(PrettyFormatAny.form(l_obj, 'C1-06-E - Node'))

    def test_10_Load(self):
        """ Test reading of the Lights config file.
        """
        l_lights = lightsConfig().load_yaml_config(self.m_pyhouse_obj)
        # print(PrettyFormatAny.form(self.m_pyhouse_obj.House.Lighting.Lights, 'C1-07-A - Node'))
        self.assertEqual(len(l_lights), 3)


class C2_YamlWrite(SetupMixin, unittest.TestCase):
    """
    This section tests the reading and writing of the Yaml config file  used by lighting_lights.
    """

    def setUp(self):
        SetupMixin.setUp(self)
        # self.m_obj = lightsXML().read_all_lights_xml(self.m_pyhouse_obj)

    def test_01_(self):
        """Test the write for proper XML Base elements
        """
        print(PrettyFormatAny.form(self.m_pyhouse_obj.House.Lighting.Lights, 'C2-01-A - Node'))


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
