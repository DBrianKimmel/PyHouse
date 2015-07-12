"""
@name:      PyHouse/src/Modules/housing/test/test_location.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2013-2015 by D. Brian Kimmel
@license:   MIT License
@note:      Created on Apr 10, 2013
@summary:   Test handling the rooms information for a house.


Tests all working OK - DBK 2014-05-22
"""

# Import system type stuff
import xml.etree.ElementTree as ET
from twisted.trial import unittest

# Import PyMh files and modules.
from Modules.Core.data_objects import LocationData
from Modules.Housing import location
from Modules.Web import web_utils
from test.xml_data import XML_LONG
from test.testing_mixin import SetupPyHouseObj
from Modules.Utilities.tools import PrettyPrintAny


class SetupMixin(object):

    def setUp(self, p_root):
        self.m_pyhouse_obj = SetupPyHouseObj().BuildPyHouseObj(p_root)
        self.m_xml = SetupPyHouseObj().BuildXml(p_root)


class C01_XML(SetupMixin, unittest.TestCase):

    def _pyHouses(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))
        self.m_house_obj = LocationData()
        self.m_api = location.ReadWriteConfigXml()

    def setUp(self):
        self._pyHouses()

    def test_01_find_xml(self):
        """ Be sure that the XML contains the right stuff.
        """
        self.assertEqual(self.m_xml.root.tag, 'PyHouse', 'Invalid XML - not a PyHouse XML config file')
        self.assertEqual(self.m_xml.house_div.tag, 'HouseDivision', 'XML - No Houses Division')

    def test_02_ReadXml(self):
        """ Read in the xml file and fill in the location dict
        """
        l_location = self.m_api.read_location_xml(self.m_xml.house_div)
        PrettyPrintAny(l_location, 'Location')
        self.assertEqual(l_location.Street, '5191 N Pink Poppy Dr', 'Bad Address')
        self.assertEqual(l_location.City, 'Beverly Hills', 'Bad city')
        self.assertEqual(l_location.State, 'Florida', 'Bad state')
        self.assertEqual(l_location.ZipCode, '34465', 'Bad zip code')
        self.assertEqual(l_location.Phone, '(352) 270-8096', 'Bad phone')
        self.assertEqual(l_location.Latitude, 28.938448, 'Bad latitude')
        self.assertEqual(l_location.Longitude, -82.517208, 'Bad longitude')
        self.assertEqual(l_location.TimeZoneName, 'America/New_York', 'Bad time zone name')

    def test_03_WriteXml(self):
        """ Write out the XML file for the location section
        """
        l_location = self.m_api.read_location_xml(self.m_xml.house_div)
        l_xml = self.m_api.write_location_xml(l_location)
        PrettyPrintAny(l_xml, 'Location')


    def test_21_CreateJson(self):
        """ Create a JSON object for Location.
        """
        l_location = self.m_api.read_location_xml(self.m_xml.house_div)
        l_json = unicode(web_utils.JsonUnicode().encode_json(l_location))
        PrettyPrintAny('JSON', l_json)

# ## END DBK
