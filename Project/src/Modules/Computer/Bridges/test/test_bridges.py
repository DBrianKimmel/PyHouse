"""
@name:      PyHouse/Project/src/Modules/Computer/Bridges/test/test_bridges.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2017-2019 by D. Brian Kimmel
@note:      Created on Dec 23, 2017
@license:   MIT License
@summary:

Passed all 6 tests - DBK - 2018-02-12

"""
from Modules.Core.data_objects import PyHouseInformation, ComputerInformation

__updated__ = '2019-06-27'

# Import system type stuff
import xml.etree.ElementTree as ET
from twisted.trial import unittest

# Import PyMh files
from test.xml_data import XML_LONG, TESTING_PYHOUSE
from test.testing_mixin import SetupPyHouseObj
from Modules.Computer.Bridges.bridges import \
    API as bridgesAPI, \
    Yaml as bridgesYaml
from Modules.Computer.test.xml_computer import TESTING_COMPUTER_DIVISION
from Modules.Core.Utilities import json_tools, config_tools
from Modules.Computer.Bridges.test.xml_bridges import \
        XML_BRIDGES, \
        TESTING_BRIDGES_SECTION, \
        TESTING_BRIDGE_NAME_0, \
        TESTING_BRIDGE_NAME_1, \
        TESTING_BRIDGE_COMMENT_0
from Modules.Core.Utilities.debug_tools import PrettyFormatAny


class SetupMixin(object):

    def setUp(self, p_root):
        self.m_pyhouse_obj = SetupPyHouseObj().BuildPyHouseObj(p_root)
        self.m_xml = SetupPyHouseObj().BuildXml(p_root)
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
        print('Id: test_bridges')
        _x = PrettyFormatAny.form('test', 'title', 190)  # so it is defined when printing is cleaned up.


class A1_Setup(SetupMixin, unittest.TestCase):
    """Test that we have set up properly for the rest of the testing classes.
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))

    def test_01_BuildObjects(self):
        """ Test to be sure the compound object was built correctly.
        """
        # print(PrettyFormatAny.form(self.m_pyhouse_obj, 'A1-01-A - PyHouse'))
        # print(PrettyFormatAny.form(self.m_pyhouse_obj.Computer, 'A1-01-B - Computer'))
        # print(PrettyFormatAny.form(self.m_pyhouse_obj.Computer.Bridges, 'A1-01-C - Bridges'))
        self.assertIsInstance(self.m_pyhouse_obj, PyHouseInformation)
        self.assertIsInstance(self.m_pyhouse_obj.Computer, ComputerInformation)
        self.assertEqual(self.m_pyhouse_obj.Computer.Bridges, {})


class A2_XML(SetupMixin, unittest.TestCase):

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))
        self.m_pyhouse_obj.Computer.Mqtt.Prefix = "pyhouse/test_house/"

    def test_01_Tags(self):
        """ Be sure that the XML contains the right stuff.
        """
        # print(PrettyFormatAny.form(self.m_xml, 'A1-01-A - Tags'))
        self.assertEqual(self.m_xml.root.tag, TESTING_PYHOUSE)
        self.assertEqual(self.m_xml.computer_div.tag, TESTING_COMPUTER_DIVISION)


class A2_Xml(SetupMixin, unittest.TestCase):

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring('<x />'))
        pass

    def test_01_Raw(self):
        l_raw = XML_BRIDGES
        # print('A2-01-A - Raw', l_raw)
        self.assertEqual(l_raw[:16], '<BridgesSection>')

    def test_02_Parsed(self):
        l_xml = ET.fromstring(XML_BRIDGES)
        # print('A2-02-A - Parsed', l_xml)
        self.assertEqual(l_xml.tag, TESTING_BRIDGES_SECTION)


class C1_YamlRead(SetupMixin, unittest.TestCase):
    """ Read the YAML config files.
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))
        self.m_yaml = bridgesYaml()
        self.m_working_bridges = self.m_pyhouse_obj.Computer.Bridges

    def test_01_Build(self):
        """ The basic read info as set up
        """
        # print(PrettyFormatAny.form(self.m_working_bridges, 'C1-01-A - WorkingBridges'))
        # print(PrettyFormatAny.form(self.m_pyhouse_obj.Computer, 'C1-01-B - Computer'))
        # print(PrettyFormatAny.form(self.m_pyhouse_obj.Computer.Bridges, 'C1-01-C - Bridges'))

    def test_02_ReadFile(self):
        """ Read the rooms.yaml config file
        """
        l_node = config_tools.Yaml(self.m_pyhouse_obj).read_yaml(self.m_filename)
        l_yaml = l_node.Yaml
        l_yamlbridges = l_yaml['Bridges']
        print(PrettyFormatAny.form(l_node, 'C1-02-A - Node'))
        print(PrettyFormatAny.form(l_yaml, 'C1-02-B - Yaml'))
        print(PrettyFormatAny.form(l_yamlbridges, 'C1-02-C - YamlBridges'))
        # self.assertEqual(l_yamlbridges[0]['Name'], 'Outside')
        # self.assertEqual(len(l_yamlbridges), 5)
        pass

    def test_03_GetIncludes(self):
        """
        """
        l_node = config_tools.Yaml(self.m_pyhouse_obj).read_yaml(self.m_filename)
        l_ret = bridgesYaml()._get_bridge_plugin_config(self.m_pyhouse_obj, l_node)


class D1_API(SetupMixin, unittest.TestCase):

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))
        self.m_pyhouse_obj.Computer.Mqtt.Prefix = "pyhouse/test_house/"

# ## END DBK
