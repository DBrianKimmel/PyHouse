"""
@name:      Modules/House/Lighting/_test/test_lighting_controllers.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2014-2019 by D. Brian Kimmel
@license:   MIT License
@note:      Created on Feb 21, 2014
@summary:   This module is for testing local node data.

Passed all 7 tests - DBK - 2019-07-20
"""

__updated__ = '2019-09-07'

#  Import system type stuff
from twisted.trial import unittest

#  Import PyMh files and modules.
from _test.testing_mixin import SetupPyHouseObj

# from Modules.Core.data_objects import ControllerInformation
from Modules.Core.Utilities import config_tools
from Modules.Core.Utilities.config_tools import Yaml as configYaml
from Modules.House.Family.family import API as familyAPI
from Modules.House.Lighting.controllers import \
    Config as controllerConfig, \
    CONFIG_FILE_NAME

from Modules.Core.Utilities.debug_tools import PrettyFormatAny


#  Import PyMh files and modules.
class SetupMixin(object):

    def setUp(self):
        self.m_pyhouse_obj = SetupPyHouseObj().BuildPyHouseObj()
        self.m_yaml = SetupPyHouseObj().BuildYaml(None)
        #
        self.m_family = familyAPI(self.m_pyhouse_obj).LoadFamilyTesting()
        self.m_pyhouse_obj._Families = self.m_family
        self.m_filename = CONFIG_FILE_NAME
        self.m_yamlconf = configYaml(self.m_pyhouse_obj)


class A0(unittest.TestCase):

    def test_00_Print(self):
        _x = PrettyFormatAny.form('_test', 'title', 190)  # so it is defined when printing is cleaned up.
        print('Id: test_lighting_controllers')


class A1_Setup(SetupMixin, unittest.TestCase):

    def setUp(self):
        SetupMixin.setUp(self)

    def test_01_PyHouse(self):
        """ Be sure that the XML contains the right stuff.
        """
        self.assertEqual(self.m_pyhouse_obj.House.Irrigation, {})

    def test_02_File(self):
        """ Be sure that the XML contains the right stuff.
        """
        self.assertEqual(CONFIG_FILE_NAME, 'controllers.yaml')


class C1_ConfigRead(SetupMixin, unittest.TestCase):
    """ This section tests the reading and writing of XML used by lighting_controllers.
    """

    def setUp(self):
        SetupMixin.setUp(self)

    def test_01_Build(self):
        """ The basic read info as set up
        """
        # print('C1-01')
        self.assertEqual(self.m_pyhouse_obj.House.Lighting.Controllers, None)

    def test_02_ReadFile(self):
        """ Read the rooms.yaml config file
        """
        # print('C1-02')
        l_node = config_tools.Yaml(self.m_pyhouse_obj).read_yaml(CONFIG_FILE_NAME)
        l_yaml = l_node.Yaml
        l_yamlcontrollers = l_yaml['Controllers']
        # print(PrettyFormatAny.form(l_node, 'C1-02-A - Node'))
        # print('C1-02-B - Yaml {}'.format(l_yaml['Controllers']))
        # print(PrettyFormatAny.form(l_yamlcontrollers, 'C1-02-C - YamlRooms'))
        self.assertEqual(l_yamlcontrollers[0]['Name'], 'Plm-1')
        self.assertEqual(len(l_yamlcontrollers), 3)

    def test_03_Load(self):
        """ Read the controller.yaml config file
        """
        # print('C1-03')
        _l_ret = controllerConfig(self.m_pyhouse_obj).load_yaml_config()
        # print(PrettyFormatAny.form(l_ret, 'C1-03-A - ret'))
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
