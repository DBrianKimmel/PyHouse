"""
@name:      Modules/House/_test/test_location.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2013-2019 by D. Brian Kimmel
@license:   MIT License
@note:      Created on Apr 10, 2013
@summary:   Test handling the rooms information for a house.

Passed all 11 tests - DBK - 2019-09-30

"""

__updated__ = '2019-10-06'

# Import system type stuff
from twisted.trial import unittest
from ruamel.yaml import YAML

# Import PyMh files and modules.
from _test.testing_mixin import SetupPyHouseObj
from Modules.Core.data_objects import PyHouseInformation
from Modules.Core.Config import config_tools
from Modules.House.house import HouseInformation
from Modules.House.location import Api as locationApi

from Modules.Core.Utilities.debug_tools import PrettyFormatAny

TEST_YAML = """\
Location:
   Street: 123456789 Some Street
   City: La Angelos
   State: Ga
   ZipCode: 44444
   Country: USA
   Phone: (800) 555-1212
   TimeZone: America/New_York
   Latitude: 29.12345
   Longitude: -82.555555
   Elevation: 345.0
   Date01: 2014-04-22
   Date02: 2015-07-23
   Date03: 2016-10-24
   Date04: 2017-12-27
"""


class SetupMixin:

    def setUp(self):
        self.m_pyhouse_obj = SetupPyHouseObj().BuildPyHouseObj()
        self.m_api = locationApi(self.m_pyhouse_obj)
        l_yaml = YAML()
        self.m_test_config = l_yaml.load(TEST_YAML)


class A0(unittest.TestCase):

    def test_00_Print(self):
        _x = PrettyFormatAny.form('_test', 'title', 190)  # so it is defined when printing is cleaned up.
        print('Id: test_location')


class A1_Setup(SetupMixin, unittest.TestCase):
    """
    This section tests the reading and writing of XML used by schedules.
    """

    def setUp(self):
        SetupMixin.setUp(self)

    def test_01_BuildObjects(self):
        """ Test to be sure the compound object was built correctly - Rooms is an empty dict.
        """
        # print(PrettyFormatAny.form(self.m_pyhouse_obj, 'A1-01-A - Main', 190))
        # print(PrettyFormatAny.form(self.m_pyhouse_obj.House, 'A1-02-B - House', 190))
        # print(PrettyFormatAny.form(self.m_pyhouse_obj.House.Location, 'A1-01-C - Location', 190))
        self.assertIsInstance(self.m_pyhouse_obj, PyHouseInformation)
        self.assertIsInstance(self.m_pyhouse_obj.House, HouseInformation)


class A3_SetupYaml(SetupMixin, unittest.TestCase):
    """
    This section tests the reading and writing of XML used by schedules.
    """

    def setUp(self):
        SetupMixin.setUp(self)
        self.m_api = locationApi(self.m_pyhouse_obj)

    def test_01_BuildObjects(self):
        """ Test to be sure the compound object was built correctly - Rooms is an empty dict.
        """
        # print(PrettyFormatAny.form(self.m_pyhouse_obj._Config, 'A3-01-A - Config', 190))
        # print(__file__)
        # print(PrettyFormatAny.form(self.m_pyhouse_obj._Config.YamlTree, 'Location', 190))
        # self.assertEqual(self.m_pyhouse_obj._Config.YamlConfigDir, '/etc/pyhouse/')


class C1_ConfigRead(SetupMixin, unittest.TestCase):

    def setUp(self):
        SetupMixin.setUp(self)
        self.m_config = locationConfig(self.m_pyhouse_obj)
        # print('C1-setup-A')

    def test_02_ReadFile(self):
        """ Read the location.yaml config file
        """
        l_node = config_tools.Yaml(self.m_pyhouse_obj).read_yaml('location')
        l_config = l_node.Yaml
        # print(PrettyFormatAny.form(l_node, 'C1-02-A'))
        # print(PrettyFormatAny.form(l_config, 'C1-02-B'))
        self.assertEqual(l_config['Location']['Street'], '1600 Pennsylvania Ave NW')
        self.assertEqual(len(l_config['Location']), 10)

    def test_03_extract(self):
        """ Create a JSON object for Location.
        """
        l_node = config_tools.Yaml(self.m_pyhouse_obj).read_yaml('location')
        l_obj = self.m_config._extract_location(l_node.Yaml['Location'])
        l_ret = self.m_pyhouse_obj.House.Location
        # print(PrettyFormatAny.form(l_node, 'C1-03-A'))
        # print(PrettyFormatAny.form(l_obj, 'C1-03-B'))
        # print(PrettyFormatAny.form(l_ret, 'C1-03-C'))
        self.assertEqual(l_obj.Street, '1600 Pennsylvania Ave NW')
        self.assertEqual(l_obj.City, 'Washington')

    def test_04_Load(self):
        """ Test complete load
        """
        l_obj = self.m_config.load_yaml_config()
        # print(PrettyFormatAny.form(l_obj, 'C1-04-A', 190))
        self.assertEqual(l_obj.Street, '1600 Pennsylvania Ave NW')
        self.assertEqual(l_obj.City, 'Washington')
        self.assertEqual(l_obj.State, 'DC')
        self.assertEqual(str(l_obj.ZipCode), '20500')
        self.assertEqual(l_obj.Country, 'USA')

    def test_99_Done(self):
        """ Test complete load
        """
        # print('C1-99-A Done\n')


class C2_YamlWrite(SetupMixin, unittest.TestCase):

    def setUp(self):
        SetupMixin.setUp(self)
        self.m_config = locationConfig(self.m_pyhouse_obj)
        self.m_location = self.m_config.load_yaml_config()
        self.m_working_location = self.m_pyhouse_obj.House.Location

    def test_01_(self):
        """
        """
        # print('C2-01-A')


class S2_PyHouse(SetupMixin, unittest.TestCase):

    def setUp(self):
        SetupMixin.setUp(self)

    def test_01_Obj(self):
        # print(PrettyFormatAny.form(self.m_pyhouse_obj, 'PyHouse_obj'))
        pass

    def test_02_House(self):
        # print(PrettyFormatAny.form(self.m_pyhouse_obj.House, 'PyHouse_obj.House'))
        pass

    def test_03_Location(self):
        # print(PrettyFormatAny.form(self.m_pyhouse_obj.House.Location, 'PyHouse_obj.House.Location'))
        pass

# ## END DBK
