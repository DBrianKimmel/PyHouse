"""
@name:      PyHouse/Project/src/Modules/Housing/test/test_rooms.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2019-2019 by D. Brian Kimmel
@license:   MIT License
@note:      Created on Jun 28, 2019
@summary:   Test handling the rooms information for a house.

Passed all 9 tests - DBK 2019-06-28

"""
__updated__ = '2019-06-28'

# Import system type stuff
import xml.etree.ElementTree as ET
from twisted.trial import unittest
from datetime import datetime

# Import PyMh files
from test.xml_data import XML_LONG
from test.testing_mixin import SetupPyHouseObj
from Modules.Housing.floors import \
    Api as floorsApi, \
    Yaml as floorsYaml
from Modules.Core.data_objects import HouseInformation, PyHouseInformation
from Modules.Core.Utilities import config_tools

from Modules.Core.Utilities.debug_tools import PrettyFormatAny


class SetupMixin:

    def setUp(self, p_root):
        self.m_pyhouse_obj = SetupPyHouseObj().BuildPyHouseObj(p_root)
        self.m_xml = SetupPyHouseObj().BuildXml(p_root)
        self.m_api = floorsApi(self.m_pyhouse_obj)
        self.m_filename = 'floors.yaml'


class A0(unittest.TestCase):

    def test_00_Print(self):
        print('Id: test_floors')
        _x = PrettyFormatAny.form('test', 'title', 190)  # so it is defined when printing is cleaned up.


class A1_Setup(SetupMixin, unittest.TestCase):
    """Test that we have set up properly for the rest of the testing classes.
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))
        pass

    def test_01_BuildObjects(self):
        """ Test to be sure the compound object was built correctly.
        """
        # print(PrettyFormatAny.form(self.m_pyhouse_obj, 'A1-01-A - PyHouse'))
        # print(PrettyFormatAny.form(self.m_pyhouse_obj.House, 'A1-01-B - House'))
        # print(PrettyFormatAny.form(self.m_pyhouse_obj.House.Floors, 'A1-01-C - Floors'))
        self.assertIsInstance(self.m_pyhouse_obj, PyHouseInformation)
        self.assertIsInstance(self.m_pyhouse_obj.House, HouseInformation)
        self.assertEqual(self.m_pyhouse_obj.House.Floors.Floor, {})


class C1_YamlRead(SetupMixin, unittest.TestCase):
    """ Read the YAML config files.
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))
        self.m_yaml = floorsYaml()
        self.m_working_floors = self.m_pyhouse_obj.House.Floors

    def test_01_Build(self):
        """ The basic read info as set up
        """
        # print(PrettyFormatAny.form(self.m_working_floors, 'C1-01-A - WorkingRooms'))
        # print(PrettyFormatAny.form(self.m_pyhouse_obj.House, 'C1-01-B - House'))
        # print(PrettyFormatAny.form(self.m_pyhouse_obj.House.Floors, 'C1-01-C - Floors'))

    def test_02_ReadFile(self):
        """ Read the rooms.yaml config file
        """
        l_node = config_tools.Yaml(self.m_pyhouse_obj).read_yaml(self.m_filename)
        l_yaml = l_node.Yaml
        l_yamlfloors = l_yaml['Floors']
        # print(PrettyFormatAny.form(l_node, 'C1-02-A - Node'))
        # print(PrettyFormatAny.form(l_yaml, 'C1-02-B - Yaml'))
        # print(PrettyFormatAny.form(l_yamlfloors, 'C1-02-C - YamlFloors'))
        # print(PrettyFormatAny.form(l_yamlfloors[0], 'C1-02-J - Floor-0'))
        # print(PrettyFormatAny.form(l_yamlfloors[3], 'C1-02-M - Floor-3'))
        self.assertEqual(l_yamlfloors[0]['Name'], 'Outside')
        self.assertEqual(l_yamlfloors[1]['Name'], 'Basement')
        self.assertEqual(l_yamlfloors[2]['Name'], '1st Floor')
        self.assertEqual(l_yamlfloors[3]['Name'], '2nd Floor')
        self.assertEqual(len(l_yamlfloors), 4)

    def test_03_ExtractFloor(self):
        """ Extract one room info from the yaml
        """
        l_node = config_tools.Yaml(self.m_pyhouse_obj).read_yaml(self.m_filename)
        l_yamlfloors = l_node.Yaml['Floors'][2]
        l_obj = self.m_yaml._extract_floor_config(l_yamlfloors)
        # print(PrettyFormatAny.form(l_yamlfloors, 'C1-03-A'))
        # print(PrettyFormatAny.form(l_obj, 'C1-03-B'))
        self.assertEqual(l_obj.Name, '1st Floor')
        self.assertEqual(l_obj.Active, 'True')
        self.assertEqual(l_obj.Comment, 'The first floor')
        self.assertEqual(l_obj.LastUpdate, datetime(2010, 1, 1, 1, 2, 3))
        self.assertEqual(l_obj.Description, 'This describes the first floor')

    def test_04_AllFloors(self):
        """ build the entire rooms structures
        """
        _l_node = config_tools.Yaml(self.m_pyhouse_obj).read_yaml(self.m_filename)
        _l_loc = self.m_yaml._update_floors_from_yaml(self.m_pyhouse_obj, _l_node.Yaml)
        # print(PrettyFormatAny.form(_l_loc, 'C1-04-A - Loc'))
        # print(PrettyFormatAny.form(self.m_pyhouse_obj.House.Floors, 'C1-04-B - Floors'))
        self.assertEqual(len(self.m_pyhouse_obj.House.Floors), 4)

    def test_05_LoadConfig(self):
        """ Test that pyhouse_obj has been loaded by the 'LoadYamlConfig' method.
        """
        _l_floors = self.m_yaml.LoadYamlConfig(self.m_pyhouse_obj)
        # print(PrettyFormatAny.form(self.m_pyhouse_obj.House, 'C1-05-A - House'))
        # print(PrettyFormatAny.form(self.m_pyhouse_obj.House.Floors, 'C1-05-B - House.Floors'))
        # print(PrettyFormatAny.form(_l_floors, 'C1-05-C - Load'))
        self.assertEqual(self.m_pyhouse_obj.House.Floors[0].Comment, 'Anything outside the house')


class C2_YamlWrite(SetupMixin, unittest.TestCase):
    """ Write the YAML config files.
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))
        self.m_yaml = floorsYaml()
        self.m_floors = self.m_yaml.LoadYamlConfig(self.m_pyhouse_obj)
        self.m_working_floors = self.m_pyhouse_obj.House.Floors

    def test_01_Basic(self):
        """ Basic test to read in data and update it so we can check for new data in output.
        """
        self.m_working_floors[0].Comment = 'After mods'
        # print(PrettyFormatAny.form(self.m_working_floors[0], 'C2-01-B'))
        # print(PrettyFormatAny.form(self.m_floors[0], 'C2-01-C'))
        self.assertEqual(self.m_working_floors[0].Comment, 'After mods')

    def test_02_Prep(self):
        """
        """
        self.m_working_floors[0].Comment = 'After mods'
        l_ret = self.m_yaml._copy_floors_to_yaml(self.m_pyhouse_obj)
        # print(PrettyFormatAny.form(self.m_working_floors[0], 'C2-02-A - Working Obj'))
        # print(PrettyFormatAny.form(l_ret, 'C2-02-B - yaml staging'))

    def test_03_Write(self):
        """
        """
        self.m_working_floors[0].Comment = 'After mods'
        l_ret = self.m_yaml._copy_floors_to_yaml(self.m_pyhouse_obj)
        self.m_yaml.SaveYamlConfig(self.m_pyhouse_obj)

# ## END DBK
