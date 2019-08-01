"""
@name:      Modules/Core/Utilities/_test/test_config_tools.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com>
@copyright: (c) 2014-2019 by D. Brian Kimmel
@license:   MIT License
@note:      Created on Jul 15, 2014
@Summary:

Passed all 21 tests - DBK - 2019-07-08

"""
from pycurl import M_PIPELINING

__updated__ = '2019-07-31'

# Import system type stuff
from _collections import OrderedDict
import xml.etree.ElementTree as ET
from twisted.trial import unittest
from ruamel.yaml.comments import Tag, TaggedScalar

# Import PyMh files and modules.
from test.xml_data import XML_LONG
from test.testing_mixin import SetupPyHouseObj
from Modules.Core.Utilities.config_tools import \
    Yaml as configYaml
from Modules.House.Lighting.lighting_lights import LightData

from Modules.Core.Utilities.debug_tools import PrettyFormatAny


class SetupMixin(object):

    def setUp(self, p_xml_root):
        self.m_pyhouse_obj = SetupPyHouseObj().BuildPyHouseObj(p_xml_root)
        self.m_yaml = SetupPyHouseObj().BuildYaml(None)
        self.m_pyhouse_obj._Config.ConfigDir
        self.m_filename = '_test.yaml'
        self.m_yamlconf = configYaml(self.m_pyhouse_obj)

    def dump_to_file(self, p_yaml):
        """ For debugging to see a new _test.yaml file.
        Only do this once in the entire suite.  It overwrites any previous output.
        """
        self.m_yamlconf.write_yaml(p_yaml, self.m_filename, addnew=True)


class A0(unittest.TestCase):
    """ Identity
    """

    def test_00_Print(self):
        _x = PrettyFormatAny.form('_test', 'title', 190)  # so it is defined when printing is cleaned up.
        print('Id: test_config_file')


class A1_Config(SetupMixin, unittest.TestCase):
    """
    Be sure the infrastructure for testing is set up properly.
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))
        # self.m_xml = SetupPyHouseObj().BuildXml(self.m_xml_root)
        # SetupPyHouseObj().BuildXml(self.m_xml.root)

    def test_01_Setup(self):
        """ Be sure pyhouse_obj._Config is properly set up.
        """
        l_config = self.m_pyhouse_obj._Config
        # print(PrettyFormatAny.form(l_config, 'A1-01-A - _Config', 190))
        self.assertIsNotNone(l_config.ConfigDir)
        # self.assertEqual(l_config.YamlTree, {})


class B1_YamlCreate(SetupMixin, unittest.TestCase):
    """
    This section will _test various Yaml structure creations
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))
        self.m_node = self.m_yamlconf.read_yaml(self.m_filename)

    def test_01_create(self):
        """ _test the creation of a yaml structure
        This will create an almost empty yaml config structure
        """
        LIGHTS = 'Lights'
        l_yaml = self.m_yamlconf.create_yaml(LIGHTS)
        # print('B1-01-A - Yaml: {}'.format(l_yaml))
        l_tag = self.m_yamlconf.find_first_element(l_yaml)
        # print('B1-01-B - Tag: {}'.format(l_tag))
        # print('B1-01-C - Yaml[\'Lights\']: {}'.format(l_yaml['Lights']))
        # self.dump_to_file(l_yaml)
        self.assertIsInstance(l_yaml, OrderedDict)
        self.assertEqual(l_tag, 'Lights')
        self.assertEqual(l_tag, LIGHTS)
        self.assertIsNone(l_yaml[LIGHTS])

    def test_02_create(self):
        """ _test the creation of a yaml structure
        This will create an almost empty yaml config structure

        This will cause an ERROR log message to be printed!!!
        """
        print('B1-02-A - Log error')
        LIGHTS = None
        l_yaml = self.m_yamlconf.create_yaml(LIGHTS)
        l_tag = self.m_yamlconf.find_first_element(l_yaml)
        # print('B1-02-A - Yaml: {}'.format(l_yaml))
        # self.dump_to_file(l_yaml)
        self.assertIsInstance(l_yaml, OrderedDict)
        self.assertEqual(l_tag, "ERROR_TAG")

    def test_03_CreateNode(self):
        """ _test the creation of a yaml structure
        This will create an almost empty yaml config structure
        """
        l_node = self.m_yamlconf.create_yaml_node('Test3')
        # print(PrettyFormatAny.form(l_node, 'B1-03-a - Node', 190))
        # print('B1-03-B - Node: {}'.format(l_node.Yaml))
        self.assertEqual(l_node.FileName, 'test3.yaml')


class B2_YamlLoad(SetupMixin, unittest.TestCase):
    """
    This section will _test various Yaml structure creations
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))
        self.m_filename = '_test.yaml'
        self.m_node = self.m_yamlconf.read_yaml(self.m_filename)

    def test_01_load(self):
        """ _test the creation of a yaml structure by reading in a yaml file.
        """
        # print('B2-01-A - Node: {}'.format(self.m_node))
        # print(PrettyFormatAny.form(self.m_node, 'B2-01-B - Find', 190))
        # print('B2-01-C - Yaml: {}'.format(self.m_node.Yaml))
        # self.dump_to_file(l_yaml)
        self.assertEqual(self.m_node.FileName, self.m_filename)
        self.assertIsInstance(self.m_node.Yaml, OrderedDict)

    def test_02_load(self):
        """ _test the creation of a yaml structure by reading in a yaml file.
        """
        l_yaml = self.m_node.Yaml
        l_testing = l_yaml['Testing']
        l_incl = l_testing['Include1']
        # print('B2-02-A - Yaml: {}'.format(l_yaml))
        # print('B2-02-B - Testing: {}'.format(l_testing))
        # print('B2-02-C - Include: {}'.format(l_incl))
        # print(PrettyFormatAny.form(l_incl, 'B2-02-D - Include', 190))
        # self.dump_to_file(l_yaml)
        self.assertIsInstance(l_incl, TaggedScalar)


class C1_YamlFind(SetupMixin, unittest.TestCase):
    """
    This section will _test various Yaml functions
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))

    def test_01_find(self):
        """ find_config_node()

        This will find the Yaml file in one of the sub-directories of the configured root.
        """
        l_filename = '_test.yaml'
        l_node = configYaml(self.m_pyhouse_obj).find_config_node(l_filename)
        # print(PrettyFormatAny.form(l_node, 'C1-01-A - Find', 190))
        # self.dump_to_file(l_yaml)
        self.assertEqual(l_node.FileName, l_filename)
        self.assertIsNotNone(l_node.YamlPath)
        self.assertIsNone(l_node._Error)

    def test_02_NoFind(self):
        """ find_config_node()

        This will find the Yaml file in one of the sub-dirs of the config'ed root.
        """
        l_filename = 'testxxx.yaml'
        l_node = configYaml(self.m_pyhouse_obj).find_config_node(l_filename)
        # print(PrettyFormatAny.form(l_node, 'C1-02-A - Find', 190))
        # self.dump_to_file(l_yaml)
        self.assertEqual(l_node.FileName, l_filename)
        self.assertIsNone(l_node.YamlPath)
        self.assertIsNotNone(l_node._Error)

    def test_03_BadExtension(self):
        """ find_config_node()

        This will find the Yaml file in one of the sub-dirs of the config'ed root.
        """
        l_filename = '_test.yml'
        l_node = configYaml(self.m_pyhouse_obj).find_config_node(l_filename)
        # print(PrettyFormatAny.form(l_node, 'C1-03-A - Find', 190))
        # self.dump_to_file(l_yaml)
        self.assertEqual(l_node.FileName, l_filename)
        self.assertIsNone(l_node.YamlPath)
        self.assertIsNotNone(l_node._Error)


class C2_Yaml(SetupMixin, unittest.TestCase):
    """
    This section will _test various Yaml functions
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))
        self.m_filename = '_test.yaml'
        self.m_node = configYaml(self.m_pyhouse_obj).read_yaml(self.m_filename)

    def test_01_find(self):
        """ find_config_node()

        This will find the Yaml file in one of the sub-dirs of the config'ed root.
        """
        l_node = configYaml(self.m_pyhouse_obj).find_config_node(self.m_filename)
        # print(PrettyFormatAny.form(l_node, 'C2-01-A - Find', 190))
        # self.dump_to_file(l_yaml)
        self.assertEqual(l_node.FileName, self.m_filename)
        self.assertIsNotNone(l_node.YamlPath)

    def test_02_Load(self):
        """ read_yaml()
        """
        l_node = configYaml(self.m_pyhouse_obj).read_yaml(self.m_filename)
        # print(PrettyFormatAny.form(l_node, 'C2-02-A - Find', 190))
        # print(PrettyFormatAny.form(l_node.Yaml, 'C2-02-B - Yaml', 190))
        # print('C2-02-C - Yaml {}'.format(l_node))
        # self.dump_to_file(l_node.Yaml)
        self.assertIsNotNone(l_node.Yaml)
        self.assertEqual(l_node.FileName, self.m_filename)

    def test_03_Save(self):
        """
        """
        l_yaml = self.m_node.Yaml
        l_yaml['Testing']['Street'] = 'This is a new street'
        # print(PrettyFormatAny.form(l_node, 'C2-03-A - Find', 190))
        # print(PrettyFormatAny.form(l_node.Yaml, 'C2-03-B - Yaml', 190))
        print('C2-03-C - {}'.format(self.m_node.Yaml))
        # self.dump_to_file(l_yaml)
        self.assertEqual(l_yaml['Testing']['Street'], 'This is a new street')

    def test_04_Add_K_V(self):
        """
        """
        l_yaml = self.m_node.Yaml['Testing']
        l_key = 'NewKeyABC'
        l_value = 'This is a new value'
        configYaml(self.m_pyhouse_obj).add_key_value_to_map(l_yaml['Testing'], l_key, l_value)
        print('C2-04-A - {}'.format(l_yaml))
        self.dump_to_file(l_yaml)
        # self.assertEqual(l_yaml['Testing']['Street'], 'This is a new street')

    def test_05_AddDict(self):
        """ Test adding a key,Value pair to a map
        Test:
           Key: Value
           New Key: New Value  <== Added
        """
        l_node = configYaml(self.m_pyhouse_obj).read_yaml(self.m_filename)
        l_yaml = l_node.Yaml['Testing']
        # print('C2-05-A - Yaml {}'.format(l_yaml))
        l_ret = configYaml(self.m_pyhouse_obj).add_dict(l_yaml, 'Host', {'DictAddition-1': 'Test add dict'})
        print('C2-05-B - Yaml {}'.format(l_ret))
        l_node.Yaml['Testing'] = l_ret
        print('C2-05-C - Yaml {}'.format(l_node.Yaml))
        self.dump_to_file(l_yaml)

    def test_06_AddList(self):
        """
        """
        l_node = configYaml(self.m_pyhouse_obj).read_yaml(self.m_filename)
        l_yaml = l_node.Yaml['Testing']
        l_list = [('Adding 1', 'abc'), 'wxyz']
        print('C2-06-A - Yaml Frag: {}'.format(l_yaml))
        # print(PrettyFormatAny.form(l_yaml, 'C1-06-B - AddOn1', 190))
        l_ret = configYaml(self.m_pyhouse_obj).add_list(l_yaml, 'TEST', l_list)
        print('C2-06-C - Yaml {}'.format(l_ret))
        print('C2-06-D - Yaml {}'.format(l_node.Yaml))
        # self.dump_to_file(l_yaml)

    def test_07_addObj(self):
        """
        """
        l_node = configYaml(self.m_pyhouse_obj).read_yaml(self.m_filename)
        l_yaml = l_node.Yaml['Testing']
        l_obj = LightData()
        print('C2-07-A - Yaml Frag: {}'.format(l_yaml))
        print(PrettyFormatAny.form(l_obj, 'C1-07-A - Light', 190))
        l_ret = configYaml(self.m_pyhouse_obj).add_obj(l_yaml, 'Host', l_obj)


class C3_Fetch(SetupMixin, unittest.TestCase):
    """
    This section will _test various Yaml Fetch functions
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))
        self.m_node = configYaml(self.m_pyhouse_obj).read_yaml(self.m_filename)

    def test_01_Host(self):
        """
        """
        l_yaml = self.m_node.Yaml['Testing']
        l_host = l_yaml['Host']
        l_obj = configYaml(self.m_pyhouse_obj).fetch_host_info(l_host)
        print('C3-01-A - Yaml: {}'.format(l_yaml))
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
        print('C3-02-A - Yaml: {}'.format(l_yaml))
        print(PrettyFormatAny.form(l_login, 'C2-02-B - Yaml', 190))
        print(PrettyFormatAny.form(l_obj, 'C2-02-C - Obj', 190))


class C3_Add(SetupMixin, unittest.TestCase):
    """
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))
        self.m_node = configYaml(self.m_pyhouse_obj).read_yaml(self.m_filename)

    def test_01_Host(self):
        """
        """

# ## END DBK
