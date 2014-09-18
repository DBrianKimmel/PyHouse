"""
@name: PyHouse/src/Modules/housing/test/test_location.py
@author: D. Brian Kimmel
@contact: D.BrianKimmel@gmail.com
@Copyright (c) 2013-2014 by D. Brian Kimmel
@license: MIT License
@note: Created on Apr 10, 2013
@summary: Test handling the rooms information for a house.


Tests all working OK - DBK 2014-05-22
"""

# Import system type stuff
import xml.etree.ElementTree as ET
from twisted.trial import unittest

# Import PyMh files and modules.
from Modules.Core.data_objects import PyHouseData, HouseObjs, LocationData
from Modules.Housing import location
from Modules.Web import web_utils
from Modules.Utilities.tools import PrettyPrintAny
from test import xml_data
from test.testing_mixin import SetupPyHouseObj
from Modules.Utilities.tools import PrettyPrintAny


class SetupMixin(object):

    def setUp(self, p_root):
        self.m_pyhouse_obj = SetupPyHouseObj().BuildPyHouseObj(p_root)
        self.m_xml = SetupPyHouseObj().BuildXml(p_root)


class Test_02_XML(SetupMixin, unittest.TestCase):

    def _pyHouses(self):
        SetupMixin.setUp(self, ET.fromstring(xml_data.XML_LONG))
        self.m_house_obj = LocationData()
        self.m_api = location.ReadWriteConfigXml()

    def setUp(self):
        self._pyHouses()

    def test_0201_find_xml(self):
        """ Be sure that the XML contains the right stuff.
        """
        self.assertEqual(self.m_xml.root.tag, 'PyHouse', 'Invalid XML - not a PyHouse XML config file')
        self.assertEqual(self.m_xml.house_div.tag, 'HouseDivision', 'XML - No Houses Division')

    def test_0202_ReadXml(self):
        """ Read in the xml file and fill in the location dict
        """
        l_location = self.m_api.read_location_xml(self.m_xml.house_div)
        self.assertEqual(l_location.City, 'Beverly Hills', 'Bad city')

    def test_0203_WriteXml(self):
        """ Write out the XML file for the location section
        """
        l_location = self.m_api.read_location_xml(self.m_xml.house_div)
        l_xml = self.m_api.write_location_xml(l_location)
        PrettyPrintAny(l_xml, 'Location')


    def test_0221_CreateJson(self):
        """ Create a JSON object for Location.
        """
        l_location = self.m_api.read_location_xml(self.m_xml.house_div)
        l_json = unicode(web_utils.JsonUnicode().encode_json(l_location))
        print('JSON: {0:}'.format(l_json))

# ## END DBK
