"""
@name:       PyHouse/src/Modules/Utilities/test/test_coordinate_tools.py
@author:     D. Brian Kimmel
@contact:    d.briankimmel@gmail.com
@copyright:  2016-2016 by D. Brian Kimmel
@date:       Created on Jun 21, 2016
@licencse:   MIT License
@summary:

Passed all 5 tests - DBK 2016-11-22

"""

__updated__ = '2016-11-22'


# Import system type stuff
import xml.etree.ElementTree as ET
from twisted.trial import unittest

# Import PyMh files
from test.xml_data import XML_LONG
from test.testing_mixin import SetupPyHouseObj
from Modules.Utilities.coordinate_tools import Coords
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
    TESTING_ROOM_TYPE_3, \
    TESTING_ROOM_NAME_0, \
    TESTING_ROOM_CORNER_X_3, \
    TESTING_ROOM_CORNER_Y_3, \
    TESTING_ROOM_CORNER_Z_3, \
    TESTING_ROOM_SIZE_X_3, \
    TESTING_ROOM_SIZE_Y_3, \
    TESTING_ROOM_SIZE_Z_3

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


class A0(unittest.TestCase):
    def setUp(self):
        pass
    def test_00_Print(self):
        print('Id: test_coordinate_tools')


class A1_Setup(SetupMixin, unittest.TestCase):

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))

    def test_01_Tags(self):
        """ Be sure that the XML contains the right stuff.
        """
        self.assertEqual(self.m_xml.root.tag, 'PyHouse')
        self.assertEqual(self.m_xml.button_sect.tag, 'ButtonSection')
        self.assertEqual(self.m_xml.button.tag, 'Button')


class A2_XML(SetupMixin, unittest.TestCase):
    """
    This section tests the reading and writing of XML used by lighting_lights.
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))

    def test_01_Room(self):
        """ Be sure that the XML contains the right stuff.
        """
        l_xml = self.m_xml.room_sect
        # print(PrettyFormatAny.form(l_xml, 'A2-01-A - XML'))
        self.assertEqual(l_xml[0].attrib['Name'], TESTING_ROOM_NAME_0)


class B1_Coords(SetupMixin, unittest.TestCase):

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))

    def test_01_Corner(self):
        """
        """
        # print(PrettyFormatAny.form(JSON, 'B1-01 A - Corner'))
        # print(PrettyFormatAny.form(JSON['Corner'], 'B1-01 B - Corner'))
        l_ret = self.m_api._get_coords(JSON['Corner'])
        # print(PrettyFormatAny.form(l_ret, 'B1-01 C - Corner'))
        self.assertEqual(str(l_ret.X_Easting), TESTING_ROOM_CORNER_X_3)
        self.assertEqual(str(l_ret.Y_Northing), TESTING_ROOM_CORNER_Y_3)
        self.assertEqual(str(l_ret.Z_Height), TESTING_ROOM_CORNER_Z_3)

    def test_2_Size(self):
        """
        """
        l_ret = self.m_api._get_coords(JSON['Size'])
        # print(PrettyFormatAny.form(l_ret, 'B1-02-A - Size'))
        self.assertEqual(str(l_ret.X_Easting), TESTING_ROOM_SIZE_X_3)
        self.assertEqual(str(l_ret.Y_Northing), TESTING_ROOM_SIZE_Y_3)
        self.assertEqual(str(l_ret.Z_Height), TESTING_ROOM_SIZE_Z_3)

# ## END DBK
