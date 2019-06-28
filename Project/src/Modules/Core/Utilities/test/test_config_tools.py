"""
@name:      PyHouse/src/Modules/utils/test/test_config_file.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com>
@copyright: (c) 2014-2018 by D. Brian Kimmel
@license:   MIT License
@note:      Created on Jul 15, 2014
@Summary:

Passed all 7 tests - DBK - 2019-06-24

"""

__updated__ = '2019-06-24'

# Import system type stuff
import xml.etree.ElementTree as ET
from twisted.trial import unittest

# Import PyMh files and modules.
from Modules.Core.Utilities.config_tools import \
    API as configAPI, \
    Yaml as configYaml
from test.xml_data import XML_LONG
from test.testing_mixin import SetupPyHouseObj

from Modules.Core.Utilities.debug_tools import PrettyFormatAny


class SetupMixin(object):

    def setUp(self, p_root):
        self.m_pyhouse_obj = SetupPyHouseObj().BuildPyHouseObj(p_root)
        self.m_xml = SetupPyHouseObj().BuildXml(p_root)
        self.m_pyhouse_obj._Config.ConfigDir


class A0(unittest.TestCase):

    def test_00_Print(self):
        _x = PrettyFormatAny.form('test', 'title', 190)  # so it is defined when printing is cleaned up.
        print('Id: test_config_file')


class A1_Config(SetupMixin, unittest.TestCase):
    """
    This section will verify the XML in the 'Modules.test.xml_data' file is correct
    and what the node_local module can read/write.
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))
        SetupPyHouseObj().BuildXml(self.m_xml.root)
        self.m_api = configAPI(self.m_pyhouse_obj)

    def test_01_Setup(self):
        """ Be sure _Config is properly set up.
        """
        l_config = self.m_pyhouse_obj._Config
        # print(PrettyFormatAny.form(l_config, '_Config', 190))
        self.assertIsNotNone(l_config.ConfigDir)
        self.assertEqual(l_config.YamlTree, {})


class A2_XML(SetupMixin, unittest.TestCase):
    """
    This section will verify the XML in the 'Modules.test.xml_data' file is correct
    and what the node_local module can read/write.
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))
        SetupPyHouseObj().BuildXml(self.m_xml.root)
        self.m_api = configAPI(self.m_pyhouse_obj)


class B1_XML(SetupMixin, unittest.TestCase):
    """
    This section will verify the XML in the 'Modules.test.xml_data' file is correct and what the node_local module can read/write.
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))
        SetupPyHouseObj().BuildXml(self.m_xml.root)
        self.m_api = configAPI(self.m_pyhouse_obj)


class C1_Yaml(SetupMixin, unittest.TestCase):
    """
    This section will verify the XML in the 'Modules.test.xml_data' file is correct and what the node_local module can read/write.
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))
        SetupPyHouseObj().BuildXml(self.m_xml.root)
        self.m_api = configAPI(self.m_pyhouse_obj)

    def test_01_find(self):
        """
        """
        l_filename = 'mqtt.yaml'
        l_node = configYaml(self.m_pyhouse_obj)._find_config_file(l_filename)
        # print(PrettyFormatAny.form(l_node, 'Find', 190))
        self.assertEqual(l_node.FileName, l_filename)
        self.assertIsNotNone(l_node.YamlPath)

    def test_02_Load(self):
        """
        """
        l_filename = 'mqtt.yaml'
        l_node = configYaml(self.m_pyhouse_obj).read_yaml(l_filename)
        # print(PrettyFormatAny.form(l_node, 'Find', 190))
        # print(PrettyFormatAny.form(l_node.Yaml, 'Yaml', 190))
        self.assertIsNotNone(l_node.Yaml)

    def test_03_Save(self):
        """
        """
        l_filename = 'mqtt.yaml'
        l_node = configYaml(self.m_pyhouse_obj).read_yaml(l_filename)
        # print(PrettyFormatAny.form(l_node, 'Find', 190))
        # print(PrettyFormatAny.form(l_node.Yaml, 'Yaml', 190))
        l_data = l_node.Yaml
        configYaml(self.m_pyhouse_obj).write_yaml(l_data, l_filename, addnew=True)

# ## END DBK
