"""
@name:      /home/briank/workspace/PyHouse/Project/src/Modules/House/Lighting/_test/test_outlets.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2013-2019 by D. Brian Kimmel
@license:   MIT License
@note:      Created on Dec 7, 2019
@summary:

Passed all 8 tests - DBK - 2019-12-08

"""

__updated__ = '2019-12-08'

#  Import system type stuff
from twisted.trial import unittest
from ruamel.yaml import YAML

#  Import PyMh files and modules.
from _test.testing_mixin import SetupPyHouseObj
from Modules.House.Lighting.outlets import LocalConfig as outletsConfig

from Modules.Core.Utilities.debug_tools import PrettyFormatAny

TEST_YAML = """\
Outlets:
    - Name: Musicroom Lamp
      Room: Music
      Comment: This is the music room lamp
      Family:
          Name: Insteon
          Address: 11.11.11
    - Name: Christmas
      Comment: ??
      Family:
          Name: Insteon
          Address: 22.22.22
    - Name: Gameroom Lamp
      Room: Game
      Comment: Fireplace end
      Family:
          Name: Insteon
          Address: 33.33.33
    - Name: Curio
      Family:
          Name: Insteon
          Address: 44.44.44
    - Name: China Cabinet
      Family:
          Name: Insteon
          Address: 55.55.55
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
        print('Id: test_outlets')


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
        self.assertIsNotNone(self.m_test_config['Outlets'])


class C1_Read(SetupMixin, unittest.TestCase):
    """
    This section tests the reading and writing of config used by lighting_lights.
    """

    def setUp(self):
        SetupMixin.setUp(self)
        self.m_config = outletsConfig(self.m_pyhouse_obj)

    def test_01_Outlet0(self):
        """ Test loading outlet 0
        """
        l_yaml = self.m_test_config['Outlets'][0]
        # print('C1-01-A - Yaml: ', l_yaml)
        l_outlet = self.m_config._extract_one_outlet(l_yaml)
        # print(PrettyFormatAny.form(l_outlet, 'C1-01-B - Family'))
        # print(PrettyFormatAny.form(l_outlet.Family, 'C1-01-C - Family'))
        # print(PrettyFormatAny.form(l_outlet.Room, 'C1-01-d - Room'))
        self.assertEqual(l_outlet.Name, 'Musicroom Lamp')
        self.assertEqual(l_outlet.Comment, 'This is the music room lamp')
        self.assertEqual(l_outlet.DeviceType, 'Lighting')
        self.assertEqual(l_outlet.DeviceSubType, 'Outlet')
        self.assertEqual(l_outlet.Family.Name, 'insteon')
        self.assertEqual(l_outlet.Family.Address, '11.11.11')

    def test_02_Outlet1(self):
        """ Test loading outlet 1
        """
        l_yaml = self.m_test_config['Outlets'][1]
        # print('C1-02-A - Yaml: ', l_yaml)
        l_outlet = self.m_config._extract_one_outlet(l_yaml)
        # print(PrettyFormatAny.form(l_light, 'C1-02-B - Light'))
        self.assertEqual(l_outlet.Name, 'Christmas')
        self.assertEqual(l_outlet.Comment, '??')
        self.assertEqual(l_outlet.DeviceType, 'Lighting')
        self.assertEqual(l_outlet.DeviceSubType, 'Outlet')
        self.assertEqual(l_outlet.Family.Name, 'insteon')
        self.assertEqual(l_outlet.Family.Address, '22.22.22')

    def test_03_Outlet2(self):
        """ Test loading outlet 2
        """
        l_yaml = self.m_test_config['Outlets'][2]
        # print('C1-03-A - Yaml: ', l_yaml)
        l_outlet = self.m_config._extract_one_outlet(l_yaml)
        # print(PrettyFormatAny.form(l_outlet, 'C1-03-B - Outlet'))
        self.assertEqual(l_outlet.Name, 'Gameroom Lamp')
        self.assertEqual(l_outlet.Comment, 'Fireplace end')
        self.assertEqual(l_outlet.DeviceType, 'Lighting')
        self.assertEqual(l_outlet.DeviceSubType, 'Outlet')
        self.assertEqual(l_outlet.Family.Name, 'insteon')
        self.assertEqual(l_outlet.Family.Address, '33.33.33')

    def test_04_Outlets(self):
        """ Test loading all outlets
        """
        l_yaml = self.m_test_config['Outlets']
        # print('C1-04-A - Yaml: ', l_yaml)
        l_outlets = self.m_config._extract_all_outlets(l_yaml)
        # print(PrettyFormatAny.form(l_outlets, 'C1-04-B - Outlets'))
        self.assertEqual(l_outlets[0].Name, 'Musicroom Lamp')
        self.assertEqual(l_outlets[1].Name, 'Christmas')
        self.assertEqual(l_outlets[2].Name, 'Gameroom Lamp')


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

# ## END DBK
