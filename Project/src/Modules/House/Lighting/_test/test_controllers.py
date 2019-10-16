"""
@name:      Modules/House/Lighting/_test/test_controllers.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2014-2019 by D. Brian Kimmel
@license:   MIT License
@note:      Created on Feb 21, 2014
@summary:   This module is for testing local node data.

Passed all 7 tests - DBK - 2019-10-13
"""

__updated__ = '2019-10-13'

#  Import system type stuff
from twisted.trial import unittest
from ruamel.yaml import YAML

#  Import PyMh files and modules.
from _test.testing_mixin import SetupPyHouseObj
from Modules.House.Lighting.controllers import Api as controllerApi

from Modules.Core.Utilities.debug_tools import PrettyFormatAny

TEST_YAML = """\
Controllers:
   # A list of all controllers follows

   - Name: TestPlm
     Comment: Portable, Goes where I do.
     Family:
        Name: insteon
        Type: Plm
        Address: 44.FF.11
     Interface:
        Type: Serial
        Baud: 19200,8,N,1
        Port: /dev/ttyUSB0
        Host: Laptop-01

   - Name: LaundryPlm
     Comment: Laundry Room Computers
     Family:
        Name: insteon
        Type: Plm
        Address: 44.EE.22
     Interface:
        Type: Serial
        Baud: 19200,8,N,1
        Port: /dev/ttyUSB0
        Host: pi-01

   - Name: Hue
     Comment: For philips hue lights
     Family:
        Name: hue
        Type: Hub
     Interface:
        Type: Ethernet
        Host: philios-hue
        Port: 443
     Access:
        Name: ABCDEFIGRYNKBlROabMWuABCDEFGSjBS2EWHoFYyz
        Password: !secret EncriptedPassword1
"""


class SetupMixin(object):

    def setUp(self):
        self.m_pyhouse_obj = SetupPyHouseObj().BuildPyHouseObj()
        self.m_controlApi = controllerApi(self.m_pyhouse_obj)
        l_yaml = YAML()
        self.m_test_config = l_yaml.load(TEST_YAML)


class A0(unittest.TestCase):

    def test_00_Print(self):
        _x = PrettyFormatAny.form('_test', 'title', 190)  # so it is defined when printing is cleaned up.
        print('Id: test_lighting_controllers')


class A1_Setup(SetupMixin, unittest.TestCase):

    def setUp(self):
        SetupMixin.setUp(self)

    def test_01_Config(self):
        """ Be sure that the config contains the right stuff.
        """
        # print(PrettyFormatAny.form(self.m_test_config, 'A1-01-A - Config'))
        # print(PrettyFormatAny.form(self.m_pyhouse_obj.House, 'PyHouse House'))
        self.assertIsNotNone(self.m_test_config['Controllers'])

    def test_02_PyHouse(self):
        """ Be sure that the XML contains the right stuff.
        """
        self.assertEqual(self.m_pyhouse_obj.House.Lighting.Controllers, None)


class C1_ConfigRead(SetupMixin, unittest.TestCase):
    """ This section tests the reading and writing of XML used by lighting_controllers.
    """

    def setUp(self):
        SetupMixin.setUp(self)

    def test_01_Controller0(self):
        """ Test reading the device portion of the config.
        """
        print('C1-01')
        l_yaml = self.m_test_config['Controllers'][0]
        # print('C1-01-A - Yaml: ', l_yaml)
        l_ret = self.m_controlApi.LocalConfig(self.m_pyhouse_obj)._extract_one_controller(l_yaml)
        print(PrettyFormatAny.form(l_ret, 'C1-01-B - Light'))
        self.assertEqual(l_ret.Name, 'TestPlm')
        self.assertEqual(l_ret.Comment, 'Portable, Goes where I do.')
        self.assertEqual(l_ret.DeviceType, 'Lighting')
        self.assertEqual(l_ret.DeviceSubType, 'Controller')
        self.assertEqual(l_ret.Family.Name, 'insteon')
        self.assertEqual(l_ret.Family.Address, '44.FF.11')

    def test_02_Interface(self):
        """ The basic read info as set up
        """
        print('C1-02')
        l_yaml = self.m_test_config['Controllers'][0]['Interface']
        print('C1-02-A - Yaml: ', l_yaml)
        self.assertEqual(self.m_pyhouse_obj.House.Lighting.Controllers, None)

    def test_03_Load(self):
        """ Read the controller.yaml config file
        """
        print('C1-03')
        _l_ret = self.m_controlApi.load_yaml_config()
        print(PrettyFormatAny.form(_l_ret, 'C1-03-A - ret'))
        l_test = self.m_pyhouse_obj.House.Lighting.Controllers
        # print(PrettyFormatAny.form(l_test, 'C1-03-B - Controllers'))
        # print(PrettyFormatAny.form(l_test, 'C1-03-C - Controllers'))
        # print(PrettyFormatAny.form(l_test.Family, 'C1-03-D - Controllers'))
        self.assertEqual(l_test[0].Name, 'Plm-1')
        self.assertEqual(l_test[1].Name, 'TestPlm')
        self.assertEqual(l_test[2].Name, 'InsteonHub')
        # self.assertEqual(l_test.Comment, 'A comment')
        # self.assertEqual(l_test.Family.Name, 'Insteon')


class C2_YamlWrite(SetupMixin, unittest.TestCase):
    """ This section tests the reading and writing of XML used by lighting_controllers.
    """

    def setUp(self):
        SetupMixin.setUp(self)
        # self.m_controllers = controllerXML().read_all_controllers_xml(self.m_pyhouse_obj)

    def test_01_CreateJson(self):
        """ Create a JSON object for Location.
        """
        print('C2-01')

#  ## END DBK
