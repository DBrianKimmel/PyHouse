"""
@name:      PyHouse/src/Modules/housing/test/test_house.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2013-2015 by D. Brian Kimmel
@license:   MIT License
@note:      Created on Apr 8, 2013
@summary:   Test handling the information for a house.


Passed all 8 tests - DBK - 2015-09-23
"""

# Import system type stuff
import xml.etree.ElementTree as ET
from twisted.trial import unittest

# Import PyMh files and modules.
from Modules.Housing.house import API, Xml as houseXml
from Modules.Utilities import xml_tools, json_tools
from test import xml_data
from test.testing_mixin import SetupPyHouseObj
from Modules.Utilities.debug_tools import PrettyFormatAny
from Modules.Housing.test.xml_housing import TESTING_HOUSE_NAME, TESTING_HOUSE_KEY, TESTING_HOUSE_ACTIVE
from Modules.Housing.test.xml_location import TESTING_LOCATION_STREET
from Modules.Housing.test.xml_rooms import TESTING_ROOM_NAME_0


class SetupMixin(object):

    def setUp(self, p_root):
        self.m_pyhouse_obj = SetupPyHouseObj().BuildPyHouseObj(p_root)
        self.m_xml = SetupPyHouseObj().BuildXml(p_root)
        self.m_api = API(self.m_pyhouse_obj)


class A1_Setup(SetupMixin, unittest.TestCase):
    """
    This section will verify the XML in the 'Modules.text.xml_data' file is correct and what the node_local module can read/write.
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(xml_data.XML_LONG))

    def test_01_read_xml(self):
        l_pyhouse = self.m_xml.root
        self.assertEqual(l_pyhouse.tag, 'PyHouse')

    def test_02_find_houses(self):
        l_houses = self.m_xml.root.find('HouseDivision')
        self.assertEqual(l_houses.tag, 'HouseDivision')


class B1_Read(SetupMixin, unittest.TestCase):
    """
    This section tests the reading and writing of XML used by house.
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(xml_data.XML_LONG))

    def test_01_buildObjects(self):
        """ Test to be sure the compound object was built correctly - Rooms is an empty dict.
        """
        self.assertEqual(self.m_pyhouse_obj.House.Rooms, {})

    def test_02_Xml(self):
        l_xml = houseXml.read_house_xml(self.m_pyhouse_obj)
        # print(PrettyFormatAny.form(l_xml, 'XML'))
        self.assertEqual(l_xml.Name, TESTING_HOUSE_NAME)

    def test_03_Base(self):
        l_xml = houseXml.read_house_xml(self.m_pyhouse_obj)
        self.assertEqual(l_xml.Name, TESTING_HOUSE_NAME)
        self.assertEqual(l_xml.Key, int(TESTING_HOUSE_KEY))
        self.assertEqual(l_xml.Active, bool(TESTING_HOUSE_ACTIVE))

    def test_06_ReadXml(self):
        """ Read in the xml file and fill in x
        """
        l_house_obj = houseXml.read_house_xml(self.m_pyhouse_obj)
        self.assertEqual(l_house_obj.Name, TESTING_HOUSE_NAME)
        self.assertEqual(l_house_obj.Location.Street, TESTING_LOCATION_STREET)
        self.assertEqual(l_house_obj.Rooms[0].Name, TESTING_ROOM_NAME_0)


class C03_Write(SetupMixin, unittest.TestCase):
    """
    This section tests the reading and writing of XML used by house.
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(xml_data.XML_LONG))

    def test_01_write_house_xml(self):
        l_house_obj = houseXml.read_house_xml(self.m_pyhouse_obj)
        self.m_pyhouse_obj.House = l_house_obj
        l_xml = houseXml.write_house_xml(self.m_pyhouse_obj)
        print(PrettyFormatAny.form(l_xml, 'XML'))
        self.assertEqual(l_xml.tag, 'HouseDivision')
        self.assertEqual(l_xml.attrib['Name'], TESTING_HOUSE_NAME)


class C04_JSON(SetupMixin, unittest.TestCase):
    """
    This section tests the reading and writing of XML used by house.
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(xml_data.XML_LONG))

    def test_01_CreateJson(self):
        """ Create a JSON object for Location.5
        """
        l_house = houseXml.read_house_xml(self.m_pyhouse_obj)
        print('House: {0:}'.format(l_house))
        l_json = json_tools.encode_json(l_house)
        print('JSON: {0:}'.format(l_json))

# ## END DBK
