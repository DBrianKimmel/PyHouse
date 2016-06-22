"""
@name:       PyHouse/src/Modules/Utilities/test/test_coordinate_tools.py
@author:     D. Brian Kimmel
@contact:    d.briankimmel@gmail.com
@copyright:  2016-2016 by D. Brian Kimmel
@date:       Created on Jun 21, 2016
@licencse:   MIT License
@summary:

All 3 tests ran OK - DBK 2016-06-21

"""

# Import system type stuff
import xml.etree.ElementTree as ET
from twisted.trial import unittest

# Import PyMh files
from test.xml_data import XML_LONG
from test.testing_mixin import SetupPyHouseObj
from Modules.Utilities.coordinate_tools import Coords
from Modules.Utilities import json_tools
from Modules.Utilities.debug_tools import PrettyFormatAny
from Modules.Housing.test.xml_rooms import \
    TESTING_ROOM_NAME_3, \
    TESTING_ROOM_KEY_3, \
    TESTING_ROOM_ACTIVE_3, \
    TESTING_ROOM_UUID_3, \
    TESTING_ROOM_COMMENT_3, \
    TESTING_ROOM_CORNER_3, \
    TESTING_ROOM_FLOOR_3, \
    TESTING_ROOM_SIZE_3, \
    TESTING_ROOM_TYPE_3

JSON = {
        'Name': TESTING_ROOM_NAME_3,
        'Key': TESTING_ROOM_KEY_3,
        'Active': TESTING_ROOM_ACTIVE_3,
        'UUID': TESTING_ROOM_UUID_3,
        'Comment': TESTING_ROOM_COMMENT_3,
        'Corner': TESTING_ROOM_CORNER_3,
        'Floor': TESTING_ROOM_FLOOR_3,
        'Size': TESTING_ROOM_SIZE_3,
        'RoomType': TESTING_ROOM_TYPE_3,
        'Add': True,
        'Delete': False
        }


class SetupMixin(object):

    def setUp(self, p_root):
        self.m_pyhouse_obj = SetupPyHouseObj().BuildPyHouseObj(p_root)
        self.m_xml = SetupPyHouseObj().BuildXml(p_root)
        self.m_api = Coords


class A1_Setup(SetupMixin, unittest.TestCase):

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))

    def test_1_BuildObjects(self):
        """ Test to be sure the compound object was built correctly - Rooms is an empty dict.
        """
        # print(PrettyFormatAny.form(self.m_xml, 'Tags'))
        self.assertEqual(self.m_pyhouse_obj.House.Rooms, {}, 'No Rooms{}')


class C1_Coords(SetupMixin, unittest.TestCase):

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))

    def test_1_Corner(self):
        """
        """
        # print(PrettyFormatAny.form(JSON, 'C1-1 A - Corner'))
        # print(PrettyFormatAny.form(JSON['Corner'], 'C1-1 B - Corner'))
        l_ret = self.m_api._get_coords(JSON['Corner'])
        # print(PrettyFormatAny.form(l_ret, 'C1-1 C - Corner'))
        self.assertEqual(l_ret.X_Easting, float(12.0))
        self.assertEqual(l_ret.Y_Northing, float(14.0))
        self.assertEqual(l_ret.Z_Height, float(0.5))

    def test_2_Size(self):
        """
        """
        l_ret = self.m_api._get_coords(JSON['Size'])
        # print(PrettyFormatAny.form(l_ret, 'Size'))


# ## END DBK
