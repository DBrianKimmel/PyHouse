"""
@name:      PyHouse/src/Modules/housing/test/test_house.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2013-2015 by D. Brian Kimmel
@license:   MIT License
@note:      Created on Apr 8, 2013
@summary:   Test handling the information for a house.


Tests all working OK - DBK 2014-05-29
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
from Modules.Housing.test.xml_housing import TESTING_HOUSE_NAME
from Modules.Housing.test.xml_location import TESTING_LOCATION_STREET


class SetupMixin(object):

    def setUp(self, p_root):
        self.m_pyhouse_obj = SetupPyHouseObj().BuildPyHouseObj(p_root)
        self.m_xml = SetupPyHouseObj().BuildXml(p_root)
        self.m_api = API(self.m_pyhouse_obj)


class C01_XML(SetupMixin, unittest.TestCase):
    """
    This section will verify the XML in the 'Modules.text.xml_data' file is correct and what the node_local module can read/write.
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(xml_data.XML_LONG))
        self.m_util = xml_tools.PutGetXML()

    def test_01_read_xml(self):
        l_pyhouse = self.m_xml.root
        self.assertEqual(l_pyhouse.tag, 'PyHouse')

    def test_02_find_houses(self):
        l_houses = self.m_xml.root.find('HouseDivision')
        self.assertEqual(l_houses.tag, 'HouseDivision')

    def test_03_PyHouse(self):
        l_xml_1 = self.m_pyhouse_obj.Xml.XmlRoot
        # PrettyPrintAny(l_xml_1)
        l_xml_2 = l_xml_1.find('ComputerDivision')
        # PrettyPrintAny(l_xml_2, 'ComputerXML')
        l_xml_2 = l_xml_1.find('HouseDivision')
        # PrettyPrintAny(l_xml_2, 'HouseXML')


class C02_Read(SetupMixin, unittest.TestCase):
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
        l_ret = houseXml._read_base(l_xml)
        # PrettyPrintAny(l_ret, 'House Base')
        self.assertEqual(l_xml.Name, TESTING_HOUSE_NAME)

    def test_06_ReadXml(self):
        """ Read in the xml file and fill in x
        """
        l_house_obj = houseXml.read_house_xml(self.m_pyhouse_obj)
        self.assertEqual(l_house_obj.Name, TESTING_HOUSE_NAME)
        self.assertEqual(l_house_obj.Location.Street, TESTING_LOCATION_STREET)



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



class C05_Utilities(SetupMixin, unittest.TestCase):

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(xml_data.XML_LONG))

    def test_01_findXml(self):
        l_xml = self.m_api._get_house_xml(self.m_pyhouse_obj)
        print('XML: {}'.format(l_xml))
        # PrettyPrintAny(l_xml, 'XML')

    def test_02_Update(self):
        # PrettyPrintAny(self.m_pyhouse_obj.House, 'PyHouse')
        l_obj = self.m_api.update_pyhouse_obj(self.m_pyhouse_obj)
        # PrettyPrintAny(l_obj.House, 'PyHouse')



class C06_Modules(SetupMixin, unittest.TestCase):
    """
    Test starting up various modules.
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(xml_data.XML_LONG))

    def test_01_Api(self):
        self.m_api._module_api(self.m_pyhouse_obj, 'Hvac')
        # PrettyPrintAny(self.m_pyhouse_obj.APIs.House, 'House APIs')
        # PrettyPrintAny(self.m_pyhouse_obj.APIs.Modules, 'House APIs Modules')

# ## END DBK
