"""
@name:      PyHouse/Project/src/Modules/Core/Utilities/test/test_config_tools.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com>
@copyright: (c) 2014-2018 by D. Brian Kimmel
@license:   MIT License
@note:      Created on Jul 15, 2014
@Summary:

Passed all 7 tests - DBK - 2019-06-24

"""

__updated__ = '2019-06-29'

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
    """ Identity
    """

    def test_00_Print(self):
        _x = PrettyFormatAny.form('test', 'title', 190)  # so it is defined when printing is cleaned up.
        print('Id: test_config_file')


class A1_Config(SetupMixin, unittest.TestCase):
    """
    Be sure the infrastructure for testing is set up properly.
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))
        SetupPyHouseObj().BuildXml(self.m_xml.root)
        self.m_api = configAPI(self.m_pyhouse_obj)

    def test_01_Setup(self):
        """ Be sure pyhouse_obj._Config is properly set up.
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
    This section will test various Yaml functions
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))
        SetupPyHouseObj().BuildXml(self.m_xml.root)
        self.m_api = configAPI(self.m_pyhouse_obj)

    def test_01_find(self):
        """ _find_config_node()

        This will find the Yaml file in one of the subdirs of the configed root.
        """
        l_filename = 'test.yaml'
        l_node = configYaml(self.m_pyhouse_obj)._find_config_node(l_filename)
        # print(PrettyFormatAny.form(l_node, 'Find', 190))
        self.assertEqual(l_node.FileName, l_filename)
        self.assertIsNotNone(l_node.YamlPath)

    def test_02_Load(self):
        """ read_yaml()
        """
        l_filename = 'test.yaml'
        l_node = configYaml(self.m_pyhouse_obj).read_yaml(l_filename)
        # print(PrettyFormatAny.form(l_node, 'Find', 190))
        # print(PrettyFormatAny.form(l_node.Yaml, 'Yaml', 190))
        self.assertIsNotNone(l_node.Yaml)

    def test_03_Save(self):
        """
        """
        l_filename = 'test.yaml'
        l_node = configYaml(self.m_pyhouse_obj).read_yaml(l_filename)
        l_data = l_node.Yaml
        l_data['Testing']['Street'] = 'This is a new street'
        configYaml(self.m_pyhouse_obj).write_yaml(l_data, l_filename, addnew=True)
        print(PrettyFormatAny.form(l_node, 'C1-03-A - Find', 190))
        print(PrettyFormatAny.form(l_node.Yaml, 'C1-03-B - Yaml', 190))

# ## END DBK
