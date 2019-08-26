"""
@name:      PyHouse/Project/src/Modules/Housing/_test/test_rooms.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2013-2019 by D. Brian Kimmel
@license:   MIT License
@note:      Created on Apr 10, 2013
@summary:   Test handling the rooms information for a house.

Passed all 18 tests - DBK 2019-06-2

"""
__updated__ = '2019-07-29'

# Import system type stuff
import xml.etree.ElementTree as ET
from twisted.trial import unittest
from datetime import datetime

# Import PyMh files
from test.xml_data import XML_LONG
from test.testing_mixin import SetupPyHouseObj
from Modules.Housing.rooms import \
    Api as roomsApi, \
    Config as roomsConfig
from Modules.Core.data_objects import HouseInformation, PyHouseInformation
from Modules.Core.Utilities import config_tools

from Modules.Core.Utilities.debug_tools import PrettyFormatAny


class SetupMixin:

    def setUp(self):
        self.m_pyhouse_obj = SetupPyHouseObj().BuildPyHouseObj()
        self.m_api = roomsApi(self.m_pyhouse_obj)
        self.m_filename = 'rooms.yaml'


class A0(unittest.TestCase):

    def test_00_Print(self):
        _x = PrettyFormatAny.form('_test', 'title', 190)  # so it is defined when printing is cleaned up.
        print('Id: test_rooms')


class A1_Setup(SetupMixin, unittest.TestCase):
    """Test that we have set up properly for the rest of the testing classes.
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))

    def test_01_BuildObjects(self):
        """ Test to be sure the compound object was built correctly.
        """
        # print(PrettyFormatAny.form(self.m_pyhouse_obj, 'A1-01-A - PyHouse'))
        # print(PrettyFormatAny.form(self.m_pyhouse_obj.House, 'A1-01-B - House'))
        # print(PrettyFormatAny.form(self.m_pyhouse_obj.House.Rooms, 'A1-01-C - Rooms'))
        self.assertIsInstance(self.m_pyhouse_obj, PyHouseInformation)
        self.assertIsInstance(self.m_pyhouse_obj.House, HouseInformation)
        self.assertEqual(self.m_pyhouse_obj.House.Rooms.Room, {})


class A2_XML(SetupMixin, unittest.TestCase):
    """ Now we _test that the xml_xxxxx have set up the XML_LONG tree properly.
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))

    def test_01_HouseDiv(self):
        """ Test
        """
        l_xml = self.m_xml.house_div


class B1_XmlRead(SetupMixin, unittest.TestCase):
    """ Test that we read in the Test XML config properly.
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))

    def test_01_OneRoom(self):
        """ Read the xml and fill in the first room's dict
        """
        l_xml = roomsXml().LoadXmlConfig(self.m_pyhouse_obj)
        # print(PrettyFormatAny.form(l_xml, 'B1-01-A - Room Xml'))
        _l_room = l_xml[0]
        # print(PrettyFormatAny.form(_l_room, 'B1-01-B - Room Xml'))

    def test_02_AllRooms(self):
        """ Read the xml and fill in the first room's dict
        """
        l_rooms = roomsXml().LoadXmlConfig(self.m_pyhouse_obj)
        # print(json_tools.encode_json(l_rooms[0]))
        # print(PrettyFormatAny.form(l_rooms, 'B1-2-A - All Rooms'))
        # print(PrettyFormatAny.form(l_rooms[0], 'B1-2-A - All Rooms'))
        # print(PrettyFormatAny.form(self.m_pyhouse_obj, 'B1-2-b - PyHouse_Obj'))
        self.assertEqual(len(l_rooms), 4)
        # print(l_rooms[0].Name)


class B2_XMLWrite(SetupMixin, unittest.TestCase):
    """ Test that we write out the XML config properly.
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))

    def test_01_OneRoom(self):
        """ Write out the XML file for the location section
        """
        l_filename = 'rooms.yaml'
        _l_node = config_tools.Yaml(self.m_pyhouse_obj).read_yaml(l_filename)
        _l_xml = self.m_xml.room
        # print(PrettyFormatAny.form(_l_node, 'B2-01-A - Room Xml'))


class C1_YamlRead(SetupMixin, unittest.TestCase):
    """ Read the YAML config files.
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))
        self.m_yaml = roomsConfig()
        self.m_working_rooms = self.m_pyhouse_obj.House.Rooms

    def test_01_Build(self):
        """ The basic read info as set up
        """
        print(PrettyFormatAny.form(self.m_working_rooms, 'C1-01-A - WorkingRooms'))
        print(PrettyFormatAny.form(self.m_pyhouse_obj.House, 'C1-01-B - House'))
        print(PrettyFormatAny.form(self.m_pyhouse_obj.House.Rooms, 'C1-01-C - Rooms'))

    def test_02_ReadFile(self):
        """ Read the rooms.yaml config file
        """
        l_node = config_tools.Yaml(self.m_pyhouse_obj).read_yaml(self.m_filename)
        l_yaml = l_node.Yaml
        l_yamlrooms = l_yaml['Rooms']
        print(PrettyFormatAny.form(l_node, 'C1-02-A - Node'))
        print(PrettyFormatAny.form(l_yaml, 'C1-02-B - Yaml'))
        print(PrettyFormatAny.form(l_yamlrooms, 'C1-02-C - YamlRooms'))
        self.assertEqual(l_yamlrooms[0]['Name'], 'Outside')
        self.assertEqual(len(l_yamlrooms), 5)

    def test_03_ExtractRoom(self):
        """ Extract one room info from the yaml
        """
        l_node = config_tools.Yaml(self.m_pyhouse_obj).read_yaml(self.m_filename)
        l_yamlrooms = l_node.Yaml['Rooms'][0]
        l_obj = self.m_yaml._extract_room_config(l_yamlrooms)
        # print(PrettyFormatAny.form(l_yamlrooms, 'C1-03-A'))
        # print(PrettyFormatAny.form(l_obj, 'C1-03-B'))
        self.assertEqual(l_obj.Name, 'Outside')
        self.assertEqual(l_obj.Active, 'True')
        self.assertEqual(l_obj.Comment, 'The initial comment')
        self.assertEqual(l_obj.LastUpdate, datetime(2010, 1, 1, 1, 2, 3))
        self.assertEqual(l_obj.Corner, [0.0, 0.0, 0.0])
        self.assertEqual(l_obj.Floor, 0)
        self.assertEqual(l_obj.RoomType, 'OutsideType')
        self.assertEqual(l_obj.Size, [0.0, 0.0, 0.0])
        self.assertEqual(l_obj.Trigger, 'None')
        self.assertEqual(l_obj.UUID, 'room....-0001-11e6-953b-74da3859e09a')

    def test_04_AllRooms(self):
        """ build the entire rooms structures
        """
        _l_node = config_tools.Yaml(self.m_pyhouse_obj).read_yaml(self.m_filename)
        _l_loc = self.m_yaml._update_rooms_from_yaml(self.m_pyhouse_obj, _l_node.Yaml)
        # print(PrettyFormatAny.form(_l_loc, 'C1-04-A - Loc'))
        # print(PrettyFormatAny.form(self.m_pyhouse_obj.House.Rooms, 'C1-04-B - Rooms'))
        self.assertEqual(len(self.m_pyhouse_obj.House.Rooms), 5)

    def test_05_LoadConfig(self):
        """ Test that pyhouse_obj has been loaded by the 'load_yaml_config' method.
        """
        _l_rooms = self.m_yaml.load_yaml_config(self.m_pyhouse_obj)
        # print(PrettyFormatAny.form(self.m_pyhouse_obj.House, 'C1-05-A'))
        # print(PrettyFormatAny.form(self.m_pyhouse_obj.House.Rooms, 'C1-05-B'))
        # print(PrettyFormatAny.form(_l_rooms, 'C1-04-C'))
        self.assertEqual(self.m_pyhouse_obj.House.Rooms[0].Comment, 'The initial comment')


class C2_YamlWrite(SetupMixin, unittest.TestCase):
    """ Write the YAML config files.
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))
        self.m_yaml = roomscinfig()
        self.m_rooms = self.m_yaml.load_yaml_config(self.m_pyhouse_obj)
        self.m_working_rooms = self.m_pyhouse_obj.House.Rooms

    def test_01_Read(self):
        """ Basic _test to read in data and update it so we can check for new data in output.
        """
        self.m_working_rooms[0].Comment = 'After mods'
        print(PrettyFormatAny.form(self.m_working_rooms[0], 'C2-01-A - WorkingRooms'))
        print(PrettyFormatAny.form(self.m_rooms[0], 'C2-01-B - ReadRooms'))
        self.assertEqual(self.m_working_rooms[0].Comment, 'After mods')

    def test_02_Prep(self):
        """
        """
        self.m_working_rooms[0].Comment = 'After mods'
        l_ret = self.m_yaml._copy_to_yaml(self.m_pyhouse_obj)
        print(PrettyFormatAny.form(self.m_working_rooms[0], 'C2-02-A - Working Obj'))
        print(PrettyFormatAny.form(l_ret, 'C2-02-B - yaml staging'))

    def test_03_Add(self):
        """ Add a new o the config K,V
        """
        print(PrettyFormatAny.form(self.m_rooms, 'C2-03-A - Rooms', 190))
        print(PrettyFormatAny.form(self.m_rooms[4], 'C2-03-B - Room4', 190))
        setattr(self.m_rooms[4], 'NewKey', 'A new value')
        print(PrettyFormatAny.form(self.m_rooms[4], 'C2-03-C - Room4', 190))
        l_data = config_tools.Yaml(self.m_pyhouse_obj).dump_string(self.m_rooms)
        print(l_data)
        pass


class D1_Maint(SetupMixin, unittest.TestCase):
    """
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))

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
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))

    def test_01_ByName(self):
        """ Create a JSON object for Rooms.
        """

    def test_02_ByUuid(self):
        """ Create a JSON object for Rooms.
        """


class Y1_Yaml(SetupMixin, unittest.TestCase):

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))

    def test_01_ByName(self):
        """ Create a JSON object for Rooms.
        """

# ## END DBK
