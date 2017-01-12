"""
@name:      PyHouse/src/Modules/Housing/test/test_house.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2013-2017 by D. Brian Kimmel
@license:   MIT License
@note:      Created on Apr 8, 2013
@summary:   Test handling the information for a house.


Passed all 14 tests - DBK - 2017-01-12
"""

__updated__ = '2017-01-12'

# Import system type stuff
import xml.etree.ElementTree as ET
from twisted.trial import unittest

# Import PyMh files and modules.
from test import xml_data
from test.testing_mixin import SetupPyHouseObj
from Modules.Housing.house import \
    API as houseAPI, \
    Xml as houseXml, \
    Utility as houseUtil
from Modules.Housing.test.xml_location import \
    TESTING_LOCATION_LATITUDE
from Modules.Housing.test.xml_rooms import TESTING_ROOM_NAME_0
from Modules.Housing.test.xml_housing import \
    TESTING_HOUSE_NAME, \
    TESTING_HOUSE_KEY, \
    TESTING_HOUSE_ACTIVE, \
    TESTING_HOUSE_UUID
from Modules.Utilities import json_tools
from Modules.Utilities.debug_tools import PrettyFormatAny


class SetupMixin(object):

    def setUp(self, p_root):
        self.m_pyhouse_obj = SetupPyHouseObj().BuildPyHouseObj(p_root)
        self.m_xml = SetupPyHouseObj().BuildXml(p_root)
        self.m_api = houseAPI(self.m_pyhouse_obj)


class A0(unittest.TestCase):
    def setUp(self):
        pass
    def test_00_Print(self):
        print('Id: test_house')


class A1_Setup(SetupMixin, unittest.TestCase):
    """
    This section will verify the XML in the 'Modules.text.xml_data' file is correct and what the node_local
        module can read/write.
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(xml_data.XML_LONG))

    def test_01_Tags(self):
        self.assertEqual(self.m_xml.root.tag, 'PyHouse')
        self.assertEqual(self.m_xml.house_div.tag, 'HouseDivision')


class A2_Xml(SetupMixin, unittest.TestCase):
    """
    This section will verify the XML in the 'Modules.text.xml_data' file is correct and what the node_local
        module can read/write.
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(xml_data.XML_LONG))

    def test_01_House(self):
        """ Test to see if the raw XML contains the expected data.
        """
        l_xml = self.m_xml.house_div
        # print(PrettyFormatAny.form(l_xml, 'A2-01-A - House'))
        self.assertEqual(l_xml.attrib['Name'], TESTING_HOUSE_NAME)
        self.assertEqual(l_xml.attrib['Active'], TESTING_HOUSE_ACTIVE)
        self.assertEqual(l_xml.attrib['Key'], TESTING_HOUSE_KEY)
        self.assertEqual(l_xml.find('UUID').text, TESTING_HOUSE_UUID)


    def test_02_buildObjects(self):
        """ Test to be sure the compound object was built correctly - Rooms is an empty dict.
        """
        # print(PrettyFormatAny.form(self.m_pyhouse_obj.House, 'A2-2-A - House'))
        self.assertEqual(self.m_pyhouse_obj.House.Rooms, {})


class B1_Read(SetupMixin, unittest.TestCase):
    """
    This section tests the reading and writing of XML used by house.
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(xml_data.XML_LONG))

    def test_01_API(self):
        houseUtil._init_component_apis(self.m_pyhouse_obj, self)
        # print(PrettyFormatAny.form(self.m_pyhouse_obj, 'B1-1-A - XML'))
        self.assertEqual(self.m_pyhouse_obj.Uuids.All, {})

    def test_02_Base(self):
        l_obj = houseXml._read_house_base(self.m_pyhouse_obj)
        # print(PrettyFormatAny.form(l_obj, 'B1-2-A - XML'))
        self.assertEqual(l_obj.Name, TESTING_HOUSE_NAME)
        self.assertEqual(str(l_obj.Key), TESTING_HOUSE_KEY)
        self.assertEqual(str(l_obj.Active), TESTING_HOUSE_ACTIVE)
        self.assertEqual(l_obj.UUID, TESTING_HOUSE_UUID)

    def test_03_House(self):
        l_obj = houseXml.read_house_xml(self.m_pyhouse_obj)
        # print(PrettyFormatAny.form(l_obj, 'B1-03-A - XML'))
        self.assertEqual(l_obj.Name, TESTING_HOUSE_NAME)
        self.assertEqual(str(l_obj.Key), TESTING_HOUSE_KEY)
        self.assertEqual(str(l_obj.Active), TESTING_HOUSE_ACTIVE)
        self.assertEqual(l_obj.UUID, TESTING_HOUSE_UUID)
        self.assertEqual(str(l_obj.Location.Latitude), TESTING_LOCATION_LATITUDE)
        self.assertEqual(l_obj.Rooms[0].Name, TESTING_ROOM_NAME_0)

    def test_04_House(self):
        l_obj = houseXml.read_house_xml(self.m_pyhouse_obj)
        # print(PrettyFormatAny.form(l_obj, 'B1-4-A - XML'))
        self.assertEqual(l_obj.Name, TESTING_HOUSE_NAME)
        self.assertEqual(str(l_obj.Key), TESTING_HOUSE_KEY)
        self.assertEqual(str(l_obj.Active), TESTING_HOUSE_ACTIVE)
        self.assertEqual(l_obj.UUID, TESTING_HOUSE_UUID)


class C3_Write(SetupMixin, unittest.TestCase):
    """
    This section tests the reading and writing of XML used by house.
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(xml_data.XML_LONG))

    def test_01_House(self):
        l_house_obj = houseXml.read_house_xml(self.m_pyhouse_obj)
        self.m_pyhouse_obj.House = l_house_obj
        l_xml = houseXml.write_house_xml(self.m_pyhouse_obj)
        # print(PrettyFormatAny.form(l_xml, 'C3-01-A - XML'))
        self.assertEqual(l_xml.tag, 'HouseDivision')
        self.assertEqual(l_xml.attrib['Name'], TESTING_HOUSE_NAME)


class J1_JSON(SetupMixin, unittest.TestCase):
    """
    This section tests the reading and writing of XML used by house.
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(xml_data.XML_LONG))

    def test_01_Create(self):
        """ Create a JSON object for Location.5
        """
        l_house = houseXml.read_house_xml(self.m_pyhouse_obj)
        # print(PrettyFormatAny.form(l_house, 'J1-01-A - House'))
        l_json = json_tools.encode_json(l_house)
        # print('J1-01-B - JSON: {}'.format(l_json))
        l_decoded = json_tools.decode_json_unicode(l_json)
        # print(PrettyFormatAny.form(l_decoded, 'J1-01-C - Decoded'))
        self.assertEqual(l_decoded['Name'], TESTING_HOUSE_NAME)


class P1_API(SetupMixin, unittest.TestCase):
    """
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(xml_data.XML_LONG))
        self.m_api = houseAPI(self.m_pyhouse_obj)

    def test_01_Init(self):
        """ Create a JSON object for Location.5
        """
        # print(PrettyFormatAny.form(self.m_api, 'P1-01-A - API'))
        pass

    def test_02_Load(self):
        _l_xml = self.m_api.LoadXml(self.m_pyhouse_obj)
        # print(PrettyFormatAny.form(l_xml, 'P1-01-A - API'))

    def test_03_Start(self):
        pass

    def test_04_SaveXml(self):
        self.m_api.LoadXml(self.m_pyhouse_obj)
        # print(PrettyFormatAny.form(self.m_pyhouse_obj.House, 'P1-04-A - House'))
        # print(PrettyFormatAny.form(self.m_pyhouse_obj.House.FamilyData, 'P1-04-B - House'))
        l_xml = ET.Element('House')
        l_xml = self.m_api.SaveXml(l_xml)
        # print(PrettyFormatAny.form(l_xml, 'P1-04-D - API'))

# ## END DBK
