"""
@name: PyHouse/src/Modules/housing/test/test_house.py
@author: D. Brian Kimmel
@contact: D.BrianKimmel@gmail.com
@Copyright (c) 2013-2014 by D. Brian Kimmel
@license: MIT License
@note: Created on Apr 8, 2013
@summary: Test handling the information for a house.


Tests all working OK - DBK 2014-05-29
"""

# Import system type stuff
import xml.etree.ElementTree as ET
from twisted.trial import unittest

# Import PyMh files and modules.
from Modules.Core.data_objects import LocationData
from Modules.Housing import house
from Modules.Web import web_utils
from Modules.Utilities import xml_tools
from test import xml_data
from test.testing_mixin import SetupPyHouseObj
from Modules.Utilities.tools import PrettyPrintAny



class SetupMixin(object):

    def setUp(self, p_root):
        self.m_pyhouse_obj = SetupPyHouseObj().BuildPyHouseObj(p_root)
        self.m_xml = SetupPyHouseObj().BuildXml(p_root)


class Test_01_XML(SetupMixin, unittest.TestCase):
    """
    This section will verify the XML in the 'Modules.text.xml_data' file is correct and what the node_local module can read/write.
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(xml_data.XML_LONG))
        self.m_util = xml_tools.PutGetXML()
        self.m_api = house.API()

    def test_01_read_xml(self):
        l_pyhouse = self.m_xml.root
        self.assertEqual(l_pyhouse.tag, 'PyHouse')

    def test_02_find_houses(self):
        l_houses = self.m_xml.root.find('HouseDivision')
        self.assertEqual(l_houses.tag, 'HouseDivision')


class Test_02_ReadXML(SetupMixin, unittest.TestCase):
    """
    This section tests the reading and writing of XML used by house.
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(xml_data.XML_LONG))
        self.m_api = house.API()

    def test_01_buildObjects(self):
        """ Test to be sure the compound object was built correctly - Rooms is an empty dict.
        """
        PrettyPrintAny(self.m_pyhouse_obj, 'PyHouse')
        self.assertEqual(self.m_pyhouse_obj.House.OBJs.Rooms, {}, 'No Rooms{}')

    def test_02_ReadXml(self):
        """ Read in the xml file and fill in x
        """
        l_house_obj = self.m_api.read_house_xml(self.m_pyhouse_obj)
        PrettyPrintAny(l_house_obj)
        self.assertEqual(l_house_obj.Name, 'Pink Poppy', 'Bad Name')
        self.assertEqual(l_house_obj.OBJs.Location.Street, '5191 N Pink Poppy Dr', 'Bad Street')

    def test_03_write_house_xml(self):
        l_house_obj = self.m_api.read_house_xml(self.m_pyhouse_obj)
        l_xml = self.m_api.write_house_xml(l_house_obj)
        PrettyPrintAny(l_xml, 'XML')

    def test_04_CreateJson(self):
        """ Create a JSON object for Location.
        """
        l_house = self.m_api.read_house_xml(self.m_pyhouse_obj)
        print('House: {0:}'.format(l_house))
        l_json = unicode(web_utils.JsonUnicode().encode_json(l_house))
        print('JSON: {0:}'.format(l_json))


class Test_03_Utilities(SetupMixin, unittest.TestCase):

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(xml_data.XML_LONG))
        self.m_api = house.API()
        self.m_house_obj = LocationData()

    def test_01_findXml(self):
        self.m_api.get_house_xml(self.m_pyhouse_obj)

    def test_02_Update(self):
        PrettyPrintAny(self.m_pyhouse_obj.House, 'PyHouse')
        l_obj = self.m_api.update_pyhouse_obj(self.m_pyhouse_obj)
        PrettyPrintAny(l_obj.House, 'PyHouse',)

# ## END DBK
