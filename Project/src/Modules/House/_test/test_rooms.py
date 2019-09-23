"""
@name:      Modules/House/_test/test_rooms.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2013-2019 by D. Brian Kimmel
@license:   MIT License
@note:      Created on Apr 10, 2013
@summary:   Test handling the rooms information for a house.

Passed all 10 tests - DBK 2019-09-17

"""
from Modules.House.house_data import RoomsInformation

__updated__ = '2019-09-17'

# Import system type stuff
from twisted.trial import unittest
from ruamel.yaml import YAML

# Import PyMh files
from _test.testing_mixin import SetupPyHouseObj
from Modules.House.rooms import Api as roomsApi, \
    Config as roomsConfig

from Modules.Core.Utilities.debug_tools import PrettyFormatAny

TEST_YAML = """\
Rooms:

   # Everything
   - Name: Outside
     Comment: Things outside the house
     Floor: 0
     RoomType: OutsideType
     Trigger: None

   # Minimum needed
   - Name: Garage

   - Name: Laundry
     Comment: The
     Floor: 1
     RoomType: Room

   - Name: Master Bath Room
     Comment: The
     Floor: 2
     RoomType: Room

"""


class SetupMixin:

    def setUp(self):
        self.m_pyhouse_obj = SetupPyHouseObj().BuildPyHouseObj()
        self.m_api = roomsApi(self.m_pyhouse_obj)
        self.m_config = roomsConfig(self.m_pyhouse_obj)
        l_yaml = YAML()
        self.m_test_config = l_yaml.load(TEST_YAML)


class A0(unittest.TestCase):

    def test_00_Print(self):
        _x = PrettyFormatAny.form('_test', 'title', 190)  # so it is defined when printing is cleaned up.
        print('Id: test_rooms')


class A1_Setup(SetupMixin, unittest.TestCase):
    """Test that we have set up properly for the rest of the testing classes.
    """

    def setUp(self):
        SetupMixin.setUp(self)
        self.m_working_rooms = self.m_pyhouse_obj.House.Rooms

    def test_01_Build(self):
        """ The basic read info as set up
        """
        # print(PrettyFormatAny.form(self.m_working_rooms, 'A1-01-A - WorkingRooms'))
        # print(PrettyFormatAny.form(self.m_pyhouse_obj.House, 'A1-01-B - House'))
        # print(PrettyFormatAny.form(self.m_pyhouse_obj.House.Rooms, 'A1-01-C - Rooms'))
        self.assertIsInstance(self.m_working_rooms, RoomsInformation)

    def test_02_Config(self):
        """ Be sure that the config contains the right stuff.
        """
        # print(PrettyFormatAny.form(self.m_test_config, 'A1-01-A - Config'))
        # print(PrettyFormatAny.form(self.m_pyhouse_obj.House, 'PyHouse House'))
        self.assertIsNotNone(self.m_test_config['Rooms'])


class C1_YamlRead(SetupMixin, unittest.TestCase):
    """ Read the YAML config files.
    """

    def setUp(self):
        SetupMixin.setUp(self)

    def test_01_Room0(self):
        """ Test reading the device portion of the config.
        """
        l_yaml = self.m_test_config['Rooms'][0]
        # print('C1-01-A - Yaml: ', l_yaml)
        l_room = self.m_config._extract_one_room(l_yaml)
        # print(PrettyFormatAny.form(l_room, 'C1-01-B - Room'))
        self.assertEqual(l_room.Name, 'Outside')
        self.assertEqual(l_room.Comment, 'Things outside the house')
        # self.assertEqual(l_room.Corner, [0.0, 0.0, 0.0])
        self.assertEqual(l_room.Floor, 0)
        self.assertEqual(l_room.RoomType, 'OutsideType')
        # self.assertEqual(l_room.Size, [0.0, 0.0, 0.0])
        self.assertEqual(l_room.Trigger, 'None')

    def test_02_Room1(self):
        """ Test reading the device portion of the config.
        """
        l_yaml = self.m_test_config['Rooms'][1]
        # print('C1-02-A - Yaml: ', l_yaml)
        l_room = self.m_config._extract_one_room(l_yaml)
        # print(PrettyFormatAny.form(l_room, 'C1-02-B - Room'))
        self.assertEqual(l_room.Name, 'Garage')

    def test_03_AllRooms(self):
        """ build the entire rooms structures
        """
        l_yaml = self.m_test_config['Rooms']
        l_rooms = self.m_config._extract_all_rooms(l_yaml)
        # print(PrettyFormatAny.form(l_rooms, 'C1-03-A - Loc'))
        # print(PrettyFormatAny.form(self.m_pyhouse_obj.House.Rooms, 'C1-04-B - Rooms'))
        self.assertEqual(len(l_rooms), 4)


class D1_Maint(SetupMixin, unittest.TestCase):
    """
    """

    def setUp(self):
        SetupMixin.setUp(self)

    def _print(self, p_rooms):
        # for l_obj in p_rooms.values():
        #    print('D1-Print - Key:{}; Name:{}; UUID:{}; Update:{};'.format(
        #            l_obj.Key, l_obj.Name, l_obj.UUID, l_obj.LastUpdate))
        # print
        pass

    def test_01_Extract(self):
        """ Test extracting information passed back by the browser.
        The data comes in JSON format..
        """


class F1_Match(SetupMixin, unittest.TestCase):

    def setUp(self):
        SetupMixin.setUp(self)

    def test_01_ByName(self):
        """ Create a JSON object for Rooms.
        """

    def test_02_ByUuid(self):
        """ Create a JSON object for Rooms.
        """


class Y1_Yaml(SetupMixin, unittest.TestCase):

    def setUp(self):
        SetupMixin.setUp(self)

    def test_01_ByName(self):
        """ Create a JSON object for Rooms.
        """

# ## END DBK
