"""
@name:      Modules/House/Lighting/Buttons/_test/test_buttons.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2014-2020 by D. Brian Kimmel
@license:   MIT License
@note:      Created on May 22, 2014
@summary:   This module is for testing lighting buttons data.

Passed all 13 tests - DBK - 2020-02-09
"""

__updated__ = '2020-02-09'

# Import system type stuff
from twisted.trial import unittest
from ruamel.yaml import YAML

# Import PyMh files and modules.
from _test.testing_mixin import SetupPyHouseObj
from Modules.House.Lighting.Buttons.buttons import Api as buttonsApi, LocalConfig as buttonsConfig

from Modules.Core.Utilities.debug_tools import PrettyFormatAny

TEST_YAML = """\
Buttons:
    - Name: Living Room mini remote
      Comment: For Garage Door
      Type: Remote
      Family:
          Name: Insteon
          Address: 11.11.11
          Model: 2342-2
      Button:
          - Name: GDO
            Comment: Garage Door Open/Close
            Group: 1
          - Name: B
            Group: 2
          - Name: C
            Group: 3
          - Name: Test
            Comment: Test Button
            Group: 4
    - Name: Breakfast Nook Slave
      Type: Slave
      Family:
          Name: Insteon
          Address: 11.CC.11
    - Name: Bedside mini remote
      Type: Remote
      Family:
          Name: Insteon
          Address: 22.22.22
          # Model: 2343-2
      Button:
          - Name: GDO
            Comment: TV Lights
            Group: 1
          - Name: B
            Comment: His Headboard
            Group: 2
          - Name: C
            Comment: Her Hedboard
            Group: 3
          - Name: D
            Group: 4
          - Name: E
            Group: 5
          - Name: F
            Group: 6
          - Name: G
            Group: 7
          - Name: H
            Group: 8
"""


class SetupMixin(object):

    def setUp(self):
        self.m_pyhouse_obj = SetupPyHouseObj().BuildPyHouseObj()
        l_yaml = YAML()
        self.m_test_config = l_yaml.load(TEST_YAML)
        self.m_config = buttonsConfig(self.m_pyhouse_obj)


class A0(unittest.TestCase):

    def setUp(self):
        pass

    def test_00_Print(self):
        _x = PrettyFormatAny.form('_x', 'title')  # so it is defined when printing is cleaned up.
        print('Id: test_buttons')


class A1_Setup(SetupMixin, unittest.TestCase):
    """
    This section tests the above setup for things we will need further down in the tests.
    """

    def setUp(self):
        SetupMixin.setUp(self)
        self.m_api = buttonsApi(self.m_pyhouse_obj)  # Must be done to setup module

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

    def test_04_Buttons(self):
        """
        """
        # print(PrettyFormatAny.form(self.m_pyhouse_obj.House.Lighting.Buttons, 'A1-04-A - Buttons'))
        self.assertIsNotNone(self.m_pyhouse_obj.House.Lighting.Buttons)


class C1_Read(SetupMixin, unittest.TestCase):
    """ This section tests loading Button config information
    """

    def setUp(self):
        SetupMixin.setUp(self)
        self.m_api = buttonsApi(self.m_pyhouse_obj)  # Must be done to setup module

    def test_01_Mini0(self):
        """ Read in the xml file and fill in the lights
        """
        l_yaml = self.m_test_config['Buttons'][0]
        print('C1-01-A - Yaml: ', l_yaml)
        l_button = buttonsConfig(self.m_pyhouse_obj)._extract_one_button_set(l_yaml)
        print(PrettyFormatAny.form(l_button, 'C1-01-B - Remote'))
        print(PrettyFormatAny.form(l_button.Family, 'C1-01-C - Family'))
        print(PrettyFormatAny.form(l_button.Buttons, 'C1-01-C - Buttons'))
        self.assertEqual(l_button.Name, 'Living Room mini remote')
        self.assertEqual(l_button.Comment, 'For Garage Door')
        self.assertEqual(l_button.Type, 'Remote')
        self.assertEqual(l_button.Family.Address, '11.11.11')
        self.assertEqual(l_button.DeviceType, 'Lighting')
        self.assertEqual(l_button.DeviceSubType, 'Button')

    def test_11_Mini1(self):
        """ Read in the xml file and fill in the lights
        """
        l_yaml = self.m_test_config['Buttons'][1]
        print('C1-02-A - Yaml: ', l_yaml)
        l_button = buttonsConfig(self.m_pyhouse_obj)._extract_one_button_set(l_yaml)
        print(PrettyFormatAny.form(l_button, 'C1-02-B - Family'))
        self.assertEqual(l_button.Name, 'Bedside mini remote')
        self.assertEqual(l_button.Family.Address, '22.22.22')

    def test_21_AllRemotes(self):
        l_yaml = self.m_test_config['Buttons']
        print('C1-21-A - Yaml: ', l_yaml)
        l_buttons = buttonsConfig(self.m_pyhouse_obj)._extract_all_button_sets(l_yaml)
        print(PrettyFormatAny.form(l_buttons, 'C1-21-B - Family'))


class D1_Write(SetupMixin, unittest.TestCase):
    """ This section tests the reading and writing of XML used by lighting_controllers.
    """

    def setUp(self):
        SetupMixin.setUp(self)

    def test_01_OneButton(self):
        """ Write out the XML file for the button section
        """

    def test_02_AllButtons(self):
        """ Write out the XML file for the Buttons section
        """


class M1_Mqtt(SetupMixin, unittest.TestCase):
    """
    This section tests the publishing of MQTT messages
    """

    def setUp(self):
        SetupMixin.setUp(self)
        self.m_api = buttonsApi(self.m_pyhouse_obj)  # Must be done to setup module
        self.m_yaml = self.m_test_config['Buttons']
        self.m_buttons = self.m_config._extract_all_button_sets(self.m_yaml)
        self.m_pyhouse_obj.House.Lighting.Buttons = self.m_buttons

    def test_01_base(self):
        """
        """
        l_ret = self.m_config._build_yaml()
        # print(PrettyFormatAny.form(l_ret, 'D1-01-A - base'))
        print(l_ret, 'D1-01-A - base')
        self.assertEqual(l_ret['Lights'], None)


class M2_Mqtt(SetupMixin, unittest.TestCase):
    """
    This section tests the dispatch of MQTT messages
    """

    def setUp(self):
        SetupMixin.setUp(self)
        self.m_api = buttonsApi(self.m_pyhouse_obj)  # Must be done to setup module
        self.m_yaml = self.m_test_config['Buttons']
        self.m_buttons = self.m_config._extract_all_button_sets(self.m_yaml)
        self.m_pyhouse_obj.House.Lighting.Buttons = self.m_buttons

    def test_01_base(self):
        """
        """
        l_ret = self.m_config._build_yaml()
        # print(PrettyFormatAny.form(l_ret, 'D1-01-A - base'))
        print(l_ret, 'D1-01-A - base')
        self.assertEqual(l_ret['Lights'], None)


class Z9_Emd(SetupMixin, unittest.TestCase):
    """
    This section tests the reading and writing of the Yaml config file  used by lighting_lights.
    """

    def setUp(self):
        SetupMixin.setUp(self)

    def test_01_End(self):
        """Test the write for proper XML Base elements
        """
        # print(PrettyFormatAny.form(self.m_pyhouse_obj.House.Lighting.Lights, 'C2-01-A - Node'))
        pass

# ## END DBK
