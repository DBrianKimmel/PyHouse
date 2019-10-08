"""
@name:      Modules/Computer/Bridges/_test/test_bridges.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2017-2019 by D. Brian Kimmel
@note:      Created on Dec 23, 2017
@license:   MIT License
@summary:

Passed all 6 tests - DBK - 2018-02-12

"""
# from ruamel.yaml.comments import CommentedMap

__updated__ = '2019-10-08'

# Import system type stuff
from twisted.trial import unittest

# Import PyMh files
from _test.testing_mixin import SetupPyHouseObj
from Modules.Computer.computer import ComputerInformation
from Modules.Computer.Bridges.bridges import Config as bridgesConfig
from Modules.Core.data_objects import PyHouseInformation
from Modules.Core.Utilities import json_tools, config_tools

from Modules.Core.Utilities.debug_tools import PrettyFormatAny


class SetupMixin(object):

    def setUp(self):
        self.m_pyhouse_obj = SetupPyHouseObj().BuildPyHouseObj()
        self.m_filename = 'bridges.yaml'

    def jsonPair(self, p_json, p_key):
        """ Extract key, value from json
        """
        l_json = json_tools.decode_json_unicode(p_json)
        try:
            l_val = l_json[p_key]
        except (KeyError, ValueError) as e_err:
            l_val = 'ERRor on JsonPair for key "{}"  {} {}'.format(p_key, e_err, l_json)
            print(l_val)
        return l_val


class A0(unittest.TestCase):

    def test_00_Print(self):
        _x = PrettyFormatAny.form('_test', 'title', 190)  # so it is defined when printing is cleaned up.
        print('Id: test_bridges')


class A1_Setup(SetupMixin, unittest.TestCase):
    """Test that we have set up properly for the rest of the testing classes.
    """

    def setUp(self):
        SetupMixin.setUp(self)

    def test_01_BuildObjects(self):
        """ Test to be sure the compound object was built correctly.
        """
        # print(PrettyFormatAny.form(self.m_pyhouse_obj, 'A1-01-A - PyHouse'))
        # print(PrettyFormatAny.form(self.m_pyhouse_obj.Computer, 'A1-01-B - Computer'))
        # print(PrettyFormatAny.form(self.m_pyhouse_obj.Computer.Bridges, 'A1-01-C - Bridges'))
        self.assertIsInstance(self.m_pyhouse_obj, PyHouseInformation)
        self.assertIsInstance(self.m_pyhouse_obj.Computer, ComputerInformation)
        self.assertEqual(self.m_pyhouse_obj.Computer.Bridges, {})


class C1_YamlRead(SetupMixin, unittest.TestCase):
    """ Read the YAML config files.
    """

    def setUp(self):
        SetupMixin.setUp(self)
        self.m_config = bridgesConfig(self.m_pyhouse_obj)
        self.m_working_bridges = self.m_pyhouse_obj.Computer.Bridges

    def test_01_Build(self):
        """ The basic read info as set up
        """
        # print(PrettyFormatAny.form(self.m_working_bridges, 'C1-01-A - WorkingBridges'))
        # print(PrettyFormatAny.form(self.m_pyhouse_obj.Computer, 'C1-01-B - Computer'))
        # print(PrettyFormatAny.form(self.m_pyhouse_obj.Computer.Bridges, 'C1-01-C - Bridges'))
        self.assertEqual(self.m_working_bridges, {})

    def test_02_ReadFile(self):
        """ Read the rooms.yaml config file
        """
        l_node = config_tools.Yaml(self.m_pyhouse_obj).read_yaml(self.m_filename)
        l_yaml = l_node.Yaml
        l_config = l_yaml['Bridges']
        # print(PrettyFormatAny.form(l_node, 'C1-02-A - Node'))
        # print(PrettyFormatAny.form(l_yaml, 'C1-02-B - Yaml'))
        print(PrettyFormatAny.form(l_config, 'C1-02-C - YamlBridges'))
        print('C1-02-D - Config: {}'.format(l_config))
        print('C1-02-E - Config: {}'.format(l_config.item()))
        self.assertEqual(l_config['Insteon']['Name'], 'Insteon')
        self.assertEqual(len(l_config), 3)

    def test_03_GetIncludes(self):
        """
        """
        l_node = config_tools.Yaml(self.m_pyhouse_obj).read_yaml(self.m_filename)
        l_ret = bridgesConfig(self.m_pyhouse_obj)._extract_all_bridges(l_node)


class D1_Api(SetupMixin, unittest.TestCase):

    def setUp(self):
        SetupMixin.setUp(self)
        self.m_pyhouse_obj.Core.Mqtt.Prefix = "pyhouse/test_house/"

# ## END DBK
