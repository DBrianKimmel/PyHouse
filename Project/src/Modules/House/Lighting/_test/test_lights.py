"""
@name:      Modules/House/Lighting/_test/test_lights.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2014-2019 by D. Brian Kimmel
@note:      Created on May 23, 2014
@license:   MIT License
@summary:   This module is for testing lighting data.

Passed all 21 tests - DBK - 2019-07-19

"""

__updated__ = '2019-08-01'

#  Import system type stuff
from twisted.trial import unittest

#  Import PyMh files and modules.
from test.testing_mixin import SetupPyHouseObj
from Modules.Core.Utilities.config_tools import Yaml as configYaml
from Modules.House.Lighting.lights import Config as lightsConfig, CONFIG_FILE_NAME
from Modules.House.Family.family import API as familyAPI

from Modules.Core.Utilities.debug_tools import PrettyFormatAny


class SetupMixin(object):
    """
    """

    def setUp(self):
        self.m_pyhouse_obj = SetupPyHouseObj().BuildPyHouseObj()
        self.m_yaml = SetupPyHouseObj().BuildYaml(None)
        self.m_yamlconf = configYaml(self.m_pyhouse_obj)
        self.m_family = familyAPI(self.m_pyhouse_obj).LoadFamilyTesting()
        self.m_pyhouse_obj._Families = self.m_family


class A0(unittest.TestCase):

    def test_00_Print(self):
        _x = PrettyFormatAny.form('_test', 'title', 190)  # so it is defined when printing is cleaned up.
        print('Id: test_lights')


class A1_Setup(SetupMixin, unittest.TestCase):
    """
    This section tests the above setup for things we will need further down in the tests.
    """

    def setUp(self):
        SetupMixin.setUp(self)

    def test_02_Family(self):
        """ Be sure that the XML contains the right stuff.
        """
        # print(PrettyFormatAny.form(self.m_pyhouse_obj, 'A1-02-A -PyHouse'))
        # # print(PrettyFormatAny.form(self.m_pyhouse_obj.House, 'PyHouse House'))
        self.assertNotEqual(self.m_pyhouse_obj, None)
        # self.assertEqual(self.m_pyhouse_obj.House.Name, TESTING_HOUSE_NAME)


class C1_YamlRead(SetupMixin, unittest.TestCase):
    """
    This section tests the reading and writing of XML used by lighting_lights.
    """

    def setUp(self):
        self.m_node = self.m_yamlconf.read_yaml(self.m_filename)

    def Xtest_01_LightFamily(self):
        """ Test reading the family portion of the light config
        """
        l_yaml = self.m_node.Yaml['Lights'][0]
        l_device = l_yaml['Device']
        l_family = l_device['Family']
        # print(PrettyFormatAny.form(l_yaml, 'C1-01-A - Yaml'))
        # print('C1-01-B - Device: ', l_device)
        # print('C1-01-C - Family: ', l_family)
        l_obj = lightsConfig()._extract_device_config(l_family)
        # print(PrettyFormatAny.form(l_obj, 'C1-01-E - Light'))
        self.assertEqual(l_obj.Name, 'Insteon')
        self.assertEqual(l_obj.Address, '12.34.56')
        self.assertEqual(l_obj.Dimmable, True)

    def Xtest_02_LightDevice(self):
        """ Test reading the device portion of the config.
        """
        l_yaml = self.m_node.Yaml['Lights'][0]
        l_device = l_yaml['Device']
        l_family = l_device['Family']
        # print('C1-02-A - Yaml {}'.format(l_family))
        # print('C1-02-B - Device: ', l_device)
        # print('C1-02-C - Family: ', l_family)
        l_obj = lightsConfig()._extract_device_config(l_family)
        # print(PrettyFormatAny.form(l_obj, 'C1-02-E - Light'))

    def Xtest_03_LightRoom(self):
        """ Test reading the Room portion of the config.
        """
        l_yaml = self.m_node.Yaml['Lights'][0]['Room']
        # l_room = l_yaml['Room']
        # print('C1-03-A - Yaml {}'.format(l_yaml))
        # print(PrettyFormatAny.form(l_yaml, 'C1-01-B - Yaml'))
        l_obj = lightsConfig()._extract_room_location_config(l_yaml)
        # print(PrettyFormatAny.form(l_obj, 'C1-03-E - Room'))
        self.assertEqual(l_obj.Name, 'Living Room')

    def Xtest_04_LightController(self):
        """ Test reading the Controller portion of the config.
        """
        l_yaml = self.m_node.Yaml['Lights'][0]['Controller']
        # print('C1-04-A - Yaml {}'.format(l_yaml))
        # print(PrettyFormatAny.form(l_yaml, 'C1-04-B - Yaml'))
        l_obj = lightsConfig()._extract_controller_config(l_yaml)
        # print(PrettyFormatAny.form(l_obj, 'C1-04-E - Node'))

    def test_05_Light(self):
        """ Test reading one light portion of the config.
        """
        l_yaml = self.m_node.Yaml['Lights'][0]
        # print('C1-05-A - Yaml {}'.format(l_yaml))
        # print(PrettyFormatAny.form(l_yaml, 'C1-01-B - Yaml'))
        l_obj = lightsConfig()._load_one_light(l_yaml)
        # print(PrettyFormatAny.form(l_obj, 'C1-05-E - Node'))
        self.assertEqual(l_obj.Name, 'Light 1')
        self.assertEqual(l_obj.Comment, 'This is _test light 1')

    def test_06_Lights(self):
        """ Test reading of the Lights config file.
        """
        l_yaml = self.m_node.Yaml['Lights']
        # print(PrettyFormatAny.form(l_yaml, 'C1-01-A - Yaml'))
        l_obj = lightsConfig()._load_all_lights(l_yaml)
        print(PrettyFormatAny.form(l_obj, 'C1-06-E - Node'))

    def test_07_Load(self):
        """ Test reading of the Lights config file.
        """
        l_lights = lightsConfig().LoadYamlConfig(self.m_pyhouse_obj)
        # print(PrettyFormatAny.form(self.m_pyhouse_obj.House.Lighting.Lights, 'C1-07-A - Node'))
        self.assertEqual(len(l_lights), 3)


class C2_YamlWrite(SetupMixin, unittest.TestCase):
    """
    This section tests the reading and writing of the Yaml config file  used by lighting_lights.
    """

    def setUp(self):
        SetupMixin.setUp(self)
        # self.m_obj = lightsXML().read_all_lights_xml(self.m_pyhouse_obj)
        lightsConfig().LoadYamlConfig(self.m_pyhouse_obj)

    def test_01_(self):
        """Test the write for proper XML Base elements
        """
        print(PrettyFormatAny.form(self.m_pyhouse_obj.House.Lighting.Lights, 'C2-01-A - Node'))

#  ## END DBK
