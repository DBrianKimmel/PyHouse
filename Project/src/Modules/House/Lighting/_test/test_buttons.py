"""
@name:      PyHouse/src/Modules/lighting/_test/test_lighting_buttons.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2014-2019 by D. Brian Kimmel
@license:   MIT License
@note:      Created on May 22, 2014
@summary:   This module is for testing lighting buttons data.

Passed all 7 tests - DBK - 2019-12-11
"""

__updated__ = '2019-12-11'

# Import system type stuff
from twisted.trial import unittest
from ruamel.yaml import YAML

# Import PyMh files and modules.
from _test.testing_mixin import SetupPyHouseObj
from Modules.House.Lighting.buttons import LocalConfig as buttonsConfig

from Modules.Core.Utilities.debug_tools import PrettyFormatAny

TEST_YAML = """\
Buttons:
    - Name: Living Room mini remote
      Comment: For Garage Door
      Type: Remote
      Family:
          Name: Insteon
          Address: 11.11.11
          # Model: 2342-2
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


class A0(unittest.TestCase):

    def setUp(self):
        pass

    def test_00_Print(self):
        _x = PrettyFormatAny.form('_x', 'title')  # so it is defined when printing is cleaned up.
        print('Id: test_buttons')


class A1_Setup(SetupMixin, unittest.TestCase):

    def setUp(self):
        SetupMixin.setUp(self)

    def test_01_PyHouse(self):
        """ Be sure that the XML contains the right stuff.
        """
        self.assertEqual(self.m_pyhouse_obj.House.Name, None)


class C1_Load(SetupMixin, unittest.TestCase):
    """ This section tests loading Button config information
    """

    def setUp(self):
        SetupMixin.setUp(self)

    def test_01_Remote0(self):
        """ Read in the xml file and fill in the lights
        """
        l_yaml = self.m_test_config['Buttons'][0]
        # print('C1-01-A - Yaml: ', l_yaml)
        l_button = buttonsConfig(self.m_pyhouse_obj)._extract_one_button_set(l_yaml)
        print(PrettyFormatAny.form(l_button, 'C1-01-B - Remote'))
        print(PrettyFormatAny.form(l_button.Family, 'C1-01-C - Family'))
        print(PrettyFormatAny.form(l_button.Button, 'C1-01-C - Buttons'))
        self.assertEqual(l_button.Name, 'Living Room mini remote')
        self.assertEqual(l_button.Comment, 'For Garage Door')
        self.assertEqual(l_button.Type, 'Remote')
        self.assertEqual(l_button.Family.Address, '11.11.11')
        self.assertEqual(l_button.DeviceType, 'Lighting')
        self.assertEqual(l_button.DeviceSubType, 'Button')

    def test_02_Remote1(self):
        """ Read in the xml file and fill in the lights
        """
        l_yaml = self.m_test_config['Buttons'][1]
        print('C1-02-A - Yaml: ', l_yaml)
        l_button = buttonsConfig(self.m_pyhouse_obj)._extract_one_button_set(l_yaml)
        print(PrettyFormatAny.form(l_button, 'C1-02-B - Family'))
        self.assertEqual(l_button.Name, 'Bedside mini remote')
        self.assertEqual(l_button.Family.Address, '22.22.22')

    def test_03_AllRemotes(self):
        l_yaml = self.m_test_config['Buttons']
        print('C1-03-A - Yaml: ', l_yaml)
        l_buttons = buttonsConfig(self.m_pyhouse_obj)._extract_all_button_sets(l_yaml)
        print(PrettyFormatAny.form(l_buttons, 'C1-03-B - Family'))


class C2_Write(SetupMixin, unittest.TestCase):
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

# ## END DBK
