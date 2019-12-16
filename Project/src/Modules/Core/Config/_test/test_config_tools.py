"""
@name:      Modules/Core/Config/_test/test_config_tools.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com>
@copyright: (c) 2014-2019 by D. Brian Kimmel
@license:   MIT License
@note:      Created on Jul 15, 2014
@Summary:

Passed all 18 tests - DBK - 2019-10-17

"""

__updated__ = '2019-12-15'

# Import system type stuff
import os
from _collections import OrderedDict
from twisted.trial import unittest
from ruamel.yaml import YAML

# Import PyMh files and modules.
from _test.testing_mixin import SetupPyHouseObj
from Modules.Core.Config import config_tools
from Modules.Core.Config.config_tools import Yaml as configYaml
from Modules.House.Lighting.lights import LightInformation

from Modules.Core.Utilities.debug_tools import PrettyFormatAny

CONFIG_FILE_NAME = 'Yaml/test.yaml'
REQUIRED_FIELDS = [
    'Latitude',
    'Longitude',
    'Elevation',
    'TimeZone'
    ]
ALLOWED_FIELDS = [
    'Street',
    'City',
    'State',
    'ZipCode',
    'PostalCode',
    'Phone',
    'Telephone',
    'Country'
    ]
COMPOUND_FIELDS = [
    ]


class TestInfo:

    def __init__(self):
        self.Street = None
        self.City = None
        self.State = None
        self.ZipCode = None
        self.Country = None
        self.Phone = None
        self.Latitude = None
        self.Longitude = None
        self.Elevation = None
        self.TimeZone = None


class SetupMixin(object):

    def setUp(self):
        self.m_pyhouse_obj = SetupPyHouseObj().BuildPyHouseObj()

    def dump_to_file(self, p_yaml):
        """ For debugging to see a new _test.yaml file.
        Only do this once in the entire suite.  It overwrites any previous output.
        """
        self.m_yamlconf.write_yaml(p_yaml, self.m_filename, addnew=True)


class A0(unittest.TestCase):
    """ Identity
    """

    def test_00_Print(self):
        _x = PrettyFormatAny.form('_test', 'title')  # so it is defined when printing is cleaned up.
        print('Id: test_config_tools')


class A1_Config(SetupMixin, unittest.TestCase):
    """
    Be sure the infrastructure for testing is set up properly.
    """

    def setUp(self):
        SetupMixin.setUp(self)

    def test_01_Setup(self):
        """ Be sure pyhouse_obj._Config is properly set up.
        """
        # print(PrettyFormatAny.form(self.m_pyhouse_obj, 'A1-01-A - PyHouse'))
        l_config = self.m_pyhouse_obj._Config
        print(PrettyFormatAny.form(l_config, 'A1-01-B - _Config'))
        # self.assertIsNotNone(l_config.ConfigDir)
        # self.assertDictEqual(l_config.YamlTree, {})


class B1_Tools(SetupMixin, unittest.TestCase):
    """
    """

    def setUp(self):
        SetupMixin.setUp(self)
        self.m_config = config_tools.Yaml(self.m_pyhouse_obj)

    def test_01_ConfigDir(self):
        """ Test getting the config directory
        """
        l_dir = self.m_config._get_config_dir()
        print('B1-01-A - ConfigDir: {}'.format(l_dir))
        self.assertIsNotNone(l_dir)

    def test_02_FindFile(self):
        """
        """
        l_dir = self.m_config._get_config_dir()
        l_file = self.m_config._find_file('test.yaml', l_dir)
        print('B1-02-A - Configfile: {}'.format(l_file))
        l_path = os.path.split(l_file)
        print('B1-02-B - Path: {}'.format(l_path))
        self.assertIsNotNone(l_dir)

    def Xtest_03_ConfigFile(self):
        """
        """
        l_dir = self.m_config._get_config_dir()
        l_file = self.m_config._find_file('Yaml/test.yaml', l_dir)
        print('B1-03-A - Configfile: {}'.format(l_file))


class B7_YamlCreate(SetupMixin, unittest.TestCase):
    """
    This section will _test various Yaml structure creations
    """

    def setUp(self):
        SetupMixin.setUp(self)
        # self.m_node = self.m_yamlconf.read_config(self.m_filename)

    def test_01_create(self):
        """ _test the creation of a yaml structure
        This will create an almost empty yaml config structure
        """
        LIGHTS = 'Lights'
        l_yaml = self.m_yamlconf._create_yaml(LIGHTS)
        print('B7-01-A - Yaml: {}'.format(l_yaml))
        l_tag = self.m_yamlconf.find_first_element(l_yaml)
        # print('B7-01-B - Tag: {}'.format(l_tag))
        # print('B7-01-C - Yaml[\'Lights\']: {}'.format(l_yaml['Lights']))
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
        # print('B1-02-A - Log error')
        LIGHTS = None
        l_yaml = self.m_yamlconf._create_yaml(LIGHTS)
        l_tag = self.m_yamlconf.find_first_element(l_yaml)
        print('B7-02-A - Yaml: {}'.format(l_yaml))
        # self.dump_to_file(l_yaml)
        self.assertIsInstance(l_yaml, OrderedDict)
        self.assertEqual(l_tag, "ERROR_TAG")


class B8_YamlLoad(SetupMixin, unittest.TestCase):
    """
    This section will _test various Yaml structure creations
    """

    def setUp(self):
        SetupMixin.setUp(self)
        self.m_filename = 'test.yaml'
        # self.m_node = self.m_yamlconf.read_config(self.m_filename)

    def test_01_load(self):
        """ _test the creation of a yaml structure by reading in a yaml file.
        """
        # print('B2-01-A - Node: {}'.format(self.m_node))
        # print(PrettyFormatAny.form(self.m_node, 'B2-01-B - Find', 190))
        # print('B2-01-C - Yaml: {}'.format(self.m_node.Yaml))
        # self.dump_to_file(l_yaml)
        # self.assertEqual(self.m_node.FileName, self.m_filename)
        # self.assertIsInstance(self.m_node.Yaml, OrderedDict)

    def test_02_load(self):
        """ _test the creation of a yaml structure by reading in a yaml file.
        """
        # l_yaml = self.m_node.Yaml
        # l_testing = l_yaml['Testing']
        # _l_incl = l_testing['Include1']
        # print('B2-02-A - Yaml: {}'.format(l_yaml))
        # print('B2-02-B - Testing: {}'.format(l_testing))
        # print('B2-02-C - Include: {}'.format(l_incl))
        # print(PrettyFormatAny.form(l_incl, 'B2-02-D - Include', 190))
        # self.dump_to_file(l_yaml)
        # self.assertIsInstance(l_incl, TaggedScalar)
        _x = 1


class C1_YamlFind(SetupMixin, unittest.TestCase):
    """
    This section will _test various Yaml functions
    """

    def setUp(self):
        SetupMixin.setUp(self)

    def Xtest_01_find(self):
        """ _find_config_node()

        This will find the Yaml file in one of the sub-directories of the configured root.
        """
        l_filename = 'test.yaml'
        l_node = configYaml(self.m_pyhouse_obj)._find_config_node(l_filename)
        # print(PrettyFormatAny.form(l_node, 'C1-01-A - Find', 190))
        # self.dump_to_file(l_yaml)
        self.assertEqual(l_node.FileName, l_filename)
        self.assertIsNotNone(l_node.YamlPath)
        self.assertIsNone(l_node._Error)

    def Xtest_02_NoFind(self):
        """ _find_config_node()

        This will find the Yaml file in one of the sub-dirs of the config'ed root.
        """
        l_filename = 'testxxx.yaml'
        l_node = configYaml(self.m_pyhouse_obj)._find_config_node(l_filename)
        # print(PrettyFormatAny.form(l_node, 'C1-02-A - Find', 190))
        # self.dump_to_file(l_yaml)
        self.assertEqual(l_node.FileName, l_filename)
        self.assertIsNone(l_node.YamlPath)
        self.assertIsNotNone(l_node._Error)

    def Xtest_03_BadExtension(self):
        """ _find_config_node()

        This will find the Yaml file in one of the sub-dirs of the config'ed root.
        """
        l_filename = 'test.yml'
        l_node = configYaml(self.m_pyhouse_obj)._find_config_node(l_filename)
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
        SetupMixin.setUp(self)
        self.m_filename = 'test.yaml'
        # self.m_node = configYaml(self.m_pyhouse_obj).read_config(self.m_filename)

    def test_01_find(self):
        """ _find_config_node()

        This will find the Yaml file in one of the sub-dirs of the config'ed root.
        """
        # l_node = configYaml(self.m_pyhouse_obj)._find_config_node(self.m_filename)
        # print(PrettyFormatAny.form(l_node, 'C2-01-A - Find', 190))
        # self.dump_to_file(l_yaml)
        # self.assertEqual(l_node.FileName, self.m_filename)
        # self.assertIsNotNone(l_node.YamlPath)

    def Xtest_02_Load(self):
        """
        """
        l_node = configYaml(self.m_pyhouse_obj).read_config(self.m_filename)
        # print(PrettyFormatAny.form(l_node, 'C2-02-A - Find', 190))
        # print(PrettyFormatAny.form(l_node.Yaml, 'C2-02-B - Yaml', 190))
        # print('C2-02-C - Yaml {}'.format(l_node))
        # self.dump_to_file(l_node.Yaml)
        self.assertIsNotNone(l_node.Yaml)
        self.assertEqual(l_node.FileName, self.m_filename)

    def Xtest_03_Save(self):
        """
        """
        l_yaml = self.m_node.Yaml
        l_yaml['Testing']['Street'] = 'This is a new street'
        # print(PrettyFormatAny.form(l_node, 'C2-03-A - Find', 190))
        # print(PrettyFormatAny.form(l_node.Yaml, 'C2-03-B - Yaml', 190))
        # print('C2-03-C - {}'.format(self.m_node.Yaml))
        # self.dump_to_file(l_yaml)
        self.assertEqual(l_yaml['Testing']['Street'], 'This is a new street')

    def Xtest_04_Add_K_V(self):
        """
        """
        l_yaml = self.m_node.Yaml['Testing']
        l_key = 'NewKeyABC'
        l_value = 'This is a new value'
        configYaml(self.m_pyhouse_obj).add_key_value_to_map(l_yaml['Testing'], l_key, l_value)
        # print('C2-04-A - {}'.format(l_yaml))
        self.dump_to_file(l_yaml)
        # self.assertEqual(l_yaml['Testing']['Street'], 'This is a new street')

    def Xtest_05_AddDict(self):
        """ Test adding a key,Value pair to a map
        Test:
           Key: Value
           New Key: New Value  <== Added
        """
        l_node = configYaml(self.m_pyhouse_obj).read_config(self.m_filename)
        l_yaml = l_node.Yaml['Testing']
        # print('C2-05-A - Yaml {}'.format(l_yaml))
        l_ret = configYaml(self.m_pyhouse_obj).add_dict(l_yaml, 'Host', {'DictAddition-1': 'Test add dict'})
        # print('C2-05-B - Yaml {}'.format(l_ret))
        l_node.Yaml['Testing'] = l_ret
        # print('C2-05-C - Yaml {}'.format(l_node.Yaml))
        self.dump_to_file(l_yaml)

    def Xtest_06_AddList(self):
        """
        """
        l_node = configYaml(self.m_pyhouse_obj).read_config(self.m_filename)
        l_yaml = l_node.Yaml['Testing']
        l_list = [('Adding 1', 'abc'), 'wxyz']
        # print('C2-06-A - Yaml Frag: {}'.format(l_yaml))
        # print(PrettyFormatAny.form(l_yaml, 'C1-06-B - AddOn1', 190))
        _l_ret = configYaml(self.m_pyhouse_obj).add_list(l_yaml, 'TEST', l_list)
        # print('C2-06-C - Yaml {}'.format(l_ret))
        # print('C2-06-D - Yaml {}'.format(l_node.Yaml))
        # self.dump_to_file(l_yaml)

    def Xtest_07_addObj(self):
        """
        """
        l_node = configYaml(self.m_pyhouse_obj).read_config(self.m_filename)
        l_yaml = l_node.Yaml['Testing']
        l_obj = LightInformation()
        # print('C2-07-A - Yaml Frag: {}'.format(l_yaml))
        # print(PrettyFormatAny.form(l_obj, 'C1-07-A - Light', 190))
        _l_ret = configYaml(self.m_pyhouse_obj).add_obj(l_yaml, 'Host', l_obj)


class C3_Fetch(SetupMixin, unittest.TestCase):
    """
    This section will _test various Yaml Fetch functions
    """

    def setUp(self):
        SetupMixin.setUp(self)
        # self.m_node = configYaml(self.m_pyhouse_obj).read_config(self.m_filename)

    def test_01_Host(self):
        """
        """
        # l_yaml = self.m_node.Yaml['Testing']
        # l_host = l_yaml['Host']
        # l_obj = configYaml(self.m_pyhouse_obj).fetch_host_info(l_host)
        # print('C3-01-A - Yaml: {}'.format(l_yaml))
        # print(PrettyFormatAny.form(l_host, 'C2-01-B - Yaml', 190))
        # print(PrettyFormatAny.form(l_obj, 'C2-01-C - Obj', 190))
        # self.assertEqual(l_obj.Name, 'Host-name-xxx')
        # self.assertEqual(l_obj.Port, 12345)

    def Xtest_02_Login(self):
        """
        """
        l_yaml = self.m_node.Yaml['Testing']
        l_login = l_yaml['Access']
        _l_obj = configYaml(self.m_pyhouse_obj).fetch_login_info(l_login)
        # print('C3-02-A - Yaml: {}'.format(l_yaml))
        # print(PrettyFormatAny.form(l_login, 'C2-02-B - Yaml', 190))
        # print(PrettyFormatAny.form(l_obj, 'C2-02-C - Obj', 190))
        _x = 1


class C4_Add(SetupMixin, unittest.TestCase):
    """
    """

    def setUp(self):
        SetupMixin.setUp(self)
        # self.m_node = configYaml(self.m_pyhouse_obj).read_config(self.m_filename)

    def test_01_Host(self):
        """
        """


class C5_FindConfig(SetupMixin, unittest.TestCase):
    """
    """

    def setUp(self):
        SetupMixin.setUp(self)
        # self.m_node = configYaml(self.m_pyhouse_obj).read_config(self.m_filename)

    def test_01_x(self):
        """
        """


class D1_Extract(SetupMixin, unittest.TestCase):
    """
    """
    test_str = """\
Host:
    Name: pandora-ct
    Port: 12345
    """

    def setUp(self):
        SetupMixin.setUp(self)
        # self.m_node = configYaml(self.m_pyhouse_obj).read_config(self.m_filename)

    def test_01_Host(self):
        """
        """
        # print('D1-01')
        l_yaml = YAML()
        l_data = l_yaml.load(self.test_str)
        # print('D1-01-A - {}'.format(l_data))
        l_ret = self.m_api.extract_host_group(l_data['Host'])
        # print(PrettyFormatAny.form(l_ret, 'D1-01-B - Host'))
        self.assertEqual(l_ret.Name, 'pandora-ct')
        self.assertEqual(l_ret.Port, 12345)


class ClsE1:

    def __init__(self):
        self.A = None
        self.B = None


ClsE1_str = """\
# example YAML document
abc: All Strings are Equal  # but some Strings are more Equal then others
klm: Flying Blue
xYz: the End                # for now
"""


class E1_Extract(SetupMixin, unittest.TestCase):
    """ Text extraction routine
    """

    def setUp(self):
        SetupMixin.setUp(self)

    def Xtest_01_Host(self):
        """
        """
        l_yaml = YAML(typ='rt')
        l_yaml.allow_duplicate_keys = True
        l_data = l_yaml.load(ClsE1_str)
        print(l_data)

        l_obj = TestInfo()
        _xx = config_tools.Tools().extract_fields(l_obj, l_data, allowed_list=[])
        print(PrettyFormatAny.form(_xx, 'E1-01-A - Test'))


class F1_Tools(SetupMixin, unittest.TestCase):
    """
    """

    def setUp(self):
        SetupMixin.setUp(self)
        self.m_tools = config_tools.Tools(self.m_pyhouse_obj)

    def test_00(self):
        print('F1-00')
        pass

    def test_01_FindFile(self):
        """
        """
        l_ret = self.m_tools._find_file('pyhouse.yaml', '/etc/pyhouse')
        # print('F1-01-A ', l_ret)
        self.assertEqual(l_ret, '/etc/pyhouse/pyhouse.yaml')

    def test_02_FindConfig(self):
        """
        """
        l_ret = self.m_tools.find_config_file('pyhouse')
        print('F1-02-A ', l_ret)
        # self.assertEqual(l_ret, '/etc/pyhouse/pyhouse.yaml')
        self.assertIsNotNone(l_ret)

# ## END DBK
