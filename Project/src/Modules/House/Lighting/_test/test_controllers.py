"""
@name:      Modules/Housing/Lighting/_test/test_lighting_controllers.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2014-2019 by D. Brian Kimmel
@license:   MIT License
@note:      Created on Feb 21, 2014
@summary:   This module is for testing local node data.

Passed all 6 tests - DBK - 2019-07-20
"""

__updated__ = '2019-07-21'

#  Import system type stuff
from twisted.trial import unittest
import xml.etree.ElementTree as ET

#  Import PyMh files and modules.
from test.testing_mixin import SetupPyHouseObj
from test.xml_data import XML_LONG

# from Modules.Core.data_objects import ControllerInformation
from Modules.Core.Utilities import config_tools
from Modules.Core.Utilities.config_tools import Yaml as configYaml
from Modules.Families.family import API as familyAPI
from Modules.Housing.Lighting.lighting_controllers import \
    Config as controllerConfig, \
    CONFIG_FILE_NAME

from Modules.Core.Utilities.debug_tools import PrettyFormatAny


#  Import PyMh files and modules.
class SetupMixin(object):

    def setUp(self, p_root):
        self.m_pyhouse_obj = SetupPyHouseObj().BuildPyHouseObj(p_root)
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
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))

    def test_01_PyHouse(self):
        """ Be sure that the XML contains the right stuff.
        """
        self.assertEqual(self.m_pyhouse_obj.House.Irrigation, {})


class C1_ConfigRead(SetupMixin, unittest.TestCase):
    """ This section tests the reading and writing of XML used by lighting_controllers.
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))
        # self.m_controllers = controllerXML().read_all_controllers_xml(self.m_pyhouse_obj)
        # self.m_working_controllers = self.m_pyhouse_obj.House.Lighting.Controllers

    def test_01_Build(self):
        """ The basic read info as set up
        """
        # print(PrettyFormatAny.form(self.m_working_controllers, 'C1-01-A - WorkingControllers'))
        # print(PrettyFormatAny.form(self.m_pyhouse_obj.House, 'C1-01-B - House'))
        # print(PrettyFormatAny.form(self.m_pyhouse_obj.House.Lighting, 'C1-01-C - Lighting'))
        # print(PrettyFormatAny.form(self.m_pyhouse_obj.House.Lighting.Controllers, 'C1-01-C - Controllers'))
        self.assertEqual(self.m_pyhouse_obj.House.Lighting.Controllers, None)

    def test_02_ReadFile(self):
        """ Read the rooms.yaml config file
        """
        l_node = config_tools.Yaml(self.m_pyhouse_obj).read_yaml(self.m_filename)
        l_yaml = l_node.Yaml
        l_yamlcontrollers = l_yaml['Controllers']
        # print(PrettyFormatAny.form(l_node, 'C1-02-A - Node'))
        # print('C1-02-B - Yaml {}'.format(l_yaml['Controllers']))
        # print(PrettyFormatAny.form(l_yamlcontrollers, 'C1-02-C - YamlRooms'))
        self.assertEqual(l_yamlcontrollers[0]['Name'], 'Plm-1')
        self.assertEqual(len(l_yamlcontrollers), 3)

    def test_03_Load(self):
        """ Read the rooms.yaml config file
        """
        controllerConfig().load_yaml_config(self.m_pyhouse_obj)
        l_test = self.m_pyhouse_obj.House.Lighting.Controllers
        # print(PrettyFormatAny.form(l_test, 'C1-03-A - Controllers'))
        # print(PrettyFormatAny.form(l_test[0], 'C1-03-B - Controllers'))
        # print(PrettyFormatAny.form(l_test[0].Family, 'C1-03-C - Controllers'))
        self.assertEqual(l_test[0].Name, 'Plm-1')
        self.assertEqual(l_test[0].Comment, 'A comment')
        self.assertEqual(l_test[0].Family.Name, 'Insteon')


class C2_YamlWrite(SetupMixin, unittest.TestCase):
    """ This section tests the reading and writing of XML used by lighting_controllers.
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))
        # self.m_controllers = controllerXML().read_all_controllers_xml(self.m_pyhouse_obj)

    def test_01_CreateJson(self):
        """ Create a JSON object for Location.
        """

#  ## END DBK
