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
from _collections import OrderedDict

__updated__ = '2019-07-04'

# Import system type stuff
import xml.etree.ElementTree as ET
from twisted.trial import unittest

# Import PyMh files and modules.
from test.xml_data import XML_LONG
from test.testing_mixin import SetupPyHouseObj
from Modules.Core.Utilities.config_tools import \
    Yaml as configYaml
from Modules.Housing.Lighting.lighting_lights import LightData

from Modules.Core.Utilities.debug_tools import PrettyFormatAny


class SetupMixin(object):

    def setUp(self, p_root):
        self.m_pyhouse_obj = SetupPyHouseObj().BuildPyHouseObj(p_root)
        self.m_xml = SetupPyHouseObj().BuildXml(p_root)
        self.m_pyhouse_obj._Config.ConfigDir
        self.m_filename = 'test.yaml'
        self.m_yaml = configYaml(self.m_pyhouse_obj)

    def dump_to_file(self, p_yaml):
        """ For debugging to see a new test.yaml file.
        Only do this once in the entire suite.  It overites any previous output.
        """
        self.m_yaml.write_yaml(p_yaml, self.m_filename, addnew=True)


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


class B1_Yaml(SetupMixin, unittest.TestCase):
    """
    This section will test various Yaml structure creations
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))
        SetupPyHouseObj().BuildXml(self.m_xml.root)
        self.m_node = self.m_yaml.read_yaml(self.m_filename)

    def test_01_create(self):
        """ test the creation of a yaml structure
        This will create an almost empty yaml config structure
        """
        LIGHTS = 'Lights'
        l_yaml = self.m_yaml.create_yaml(LIGHTS)
        l_tag = self.m_yaml.find_first_element(l_yaml)
        # print('C1-04-A - Yaml: {}'.format(l_yaml))
        self.assertIsInstance(l_yaml, OrderedDict)
        self.assertEqual(l_tag, LIGHTS)

        # self.dump_to_file(l_yaml)
    def test_02_create(self):
        """ test the creation of a yaml structure
        This will create an almost empty yaml config structure
        """
        LIGHTS = None
        l_yaml = self.m_yaml.create_yaml(LIGHTS)
        l_tag = self.m_yaml.find_first_element(l_yaml)
        # print('C1-04-A - Yaml: {}'.format(l_yaml))
        self.assertIsInstance(l_yaml, OrderedDict)
        self.assertEqual(l_tag, "ERROR_TAG")
        # self.dump_to_file(l_yaml)

    def test_03_addKV(self):
        """
        """
        l_yaml = self.m_yaml.create_yaml('Location')
        self.m_yaml.add_key_value_to_nested_map(l_yaml, 'Location', 'First key', 'first value')
        self.dump_to_file(l_yaml)


class C1_Yaml(SetupMixin, unittest.TestCase):
    """
    This section will test various Yaml functions
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))
        SetupPyHouseObj().BuildXml(self.m_xml.root)

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
        print(PrettyFormatAny.form(l_node, 'C1-02-A - Find', 190))
        print(PrettyFormatAny.form(l_node.Yaml, 'C1-02-B - Yaml', 190))
        print('C1-02-B - Yaml {}'.format(l_node.Yaml))
        self.assertIsNotNone(l_node.Yaml)

    def test_03_Save(self):
        """
        """
        l_node = configYaml(self.m_pyhouse_obj).read_yaml(self.m_filename)
        l_data = l_node.Yaml
        l_data['Testing']['Street'] = 'This is a new street'
        # self.dump_to_file(l_yaml)
        # print(PrettyFormatAny.form(l_node, 'C1-03-A - Find', 190))
        # print(PrettyFormatAny.form(l_node.Yaml, 'C1-03-B - Yaml', 190))
        print('C1-03-C - {}'.format(l_node.Yaml))

    def test_05_AddDict(self):
        """
        """
        l_node = configYaml(self.m_pyhouse_obj).read_yaml(self.m_filename)
        l_yaml = l_node.Yaml['Testing']
        print('C1-05-A - Yaml {}'.format(l_yaml))
        l_ret = configYaml(self.m_pyhouse_obj).add_dict(l_yaml, 'Host', {'DictAddition-1': 'Test add dict'})
        print('C1-05-B - Yaml {}'.format(l_ret))
        l_node.Yaml['Testing'] = l_ret
        print('C1-05-C - Yaml {}'.format(l_node.Yaml))
        # self.dump_to_file(l_yaml)

    def test_06_AddList(self):
        """
        """
        l_node = configYaml(self.m_pyhouse_obj).read_yaml(self.m_filename)
        l_yaml = l_node.Yaml['Testing']
        l_list = [('Adding 1', 'abc'), 'wxyz']
        print('C1-06-A - Yaml Frag: {}'.format(l_yaml))
        # print(PrettyFormatAny.form(l_yaml, 'C1-06-B - AddOn1', 190))
        l_ret = configYaml(self.m_pyhouse_obj).add_list(l_yaml, 'TEST', l_list)
        print('C1-06-C - Yaml {}'.format(l_ret))
        print('C1-06-D - Yaml {}'.format(l_node.Yaml))
        # self.dump_to_file(l_yaml)

    def test_07_addObj(self):
        """
        """
        l_node = configYaml(self.m_pyhouse_obj).read_yaml(self.m_filename)
        l_yaml = l_node.Yaml['Testing']
        l_obj = LightData()
        print('C1-07-A - Yaml Frag: {}'.format(l_yaml))
        print(PrettyFormatAny.form(l_obj, 'C1-07-A - Light', 190))
        l_ret = configYaml(self.m_pyhouse_obj).add_obj(l_yaml, 'Host', l_obj)


class C2_Fetch(SetupMixin, unittest.TestCase):
    """
    This section will test various Yaml Fetch functions
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))
        SetupPyHouseObj().BuildXml(self.m_xml.root)
        self.m_node = configYaml(self.m_pyhouse_obj).read_yaml(self.m_filename)

    def test_01_Host(self):
        """
        """
        l_yaml = self.m_node.Yaml['Testing']
        l_host = l_yaml['Host']
        l_obj = configYaml(self.m_pyhouse_obj).fetch_host_info(l_host)
        print('C2-01-A - Yaml: {}'.format(l_yaml))
        print(PrettyFormatAny.form(l_host, 'C2-01-B - Yaml', 190))
        print(PrettyFormatAny.form(l_obj, 'C2-01-C - Obj', 190))
        self.assertEqual(l_obj.Name, 'Host-name-xxx')
        self.assertEqual(l_obj.Port, 12345)

    def test_02_Login(self):
        """
        """
        l_yaml = self.m_node.Yaml['Testing']
        l_login = l_yaml['Login']
        l_obj = configYaml(self.m_pyhouse_obj).fetch_login_info(l_login)
        print('C2-02-A - Yaml: {}'.format(l_yaml))
        print(PrettyFormatAny.form(l_login, 'C2-02-B - Yaml', 190))
        print(PrettyFormatAny.form(l_obj, 'C2-02-C - Obj', 190))


class C3_Add(SetupMixin, unittest.TestCase):
    """
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))
        SetupPyHouseObj().BuildXml(self.m_xml.root)
        self.m_node = configYaml(self.m_pyhouse_obj).read_yaml(self.m_filename)

    def test_01_Host(self):
        """
        """

# ## END DBK
