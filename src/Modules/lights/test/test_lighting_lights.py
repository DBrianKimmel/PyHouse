"""
@name: PyHouse/src/Modules/lights/test/test_lighting_lights.py
@author: D. Brian Kimmel
@contact: <d.briankimmel@gmail.com
@copyright: 2014 by D. Brian Kimmel
@note: Created on May 23, 2014
@license: MIT License
@summary: This module is for testing lighting data.

"""

# Import system type stuff
import xml.etree.ElementTree as ET
from twisted.trial import unittest

# Import PyMh files and modules.
from Modules.Core.data_objects import PyHouseData, HousesData, HouseData
from Modules.lights import lighting_lights
from Modules.utils import xml_tools
from Modules.web import web_utils
from Modules.utils.xml_tools import prettify
from test import xml_data

XML = xml_data.XML_LONG


class Test_02_ReadXML(unittest.TestCase):
    """ This section tests the reading and writing of XML used by node_local.
    """

    def _pyHouses(self):
        self.m_pyhouses_obj = PyHouseData()
        self.m_pyhouses_obj.HousesData[0] = HousesData()
        self.m_pyhouses_obj.HousesData[0].HouseObject = HouseData()
        self.m_pyhouses_obj.XmlRoot = self.m_root = ET.fromstring(XML)
        self.m_houses = self.m_root.find('Houses')
        self.m_house = self.m_houses.find('House')
        self.m_lights = self.m_house.find('Lights')
        self.m_light = self.m_lights.find('Light')
        self.m_api = lighting_lights.LightingAPI()

    def setUp(self):
        self._pyHouses()

    def test_0201_find_xml(self):
        """ Be sure that the XML contains the right stuff.
        """
        self.assertEqual(self.m_root.tag, 'PyHouse', 'Invalid XML - not a PyHouse XML config file')
        self.assertEqual(self.m_houses.tag, 'Houses', 'XML - No Houses section')
        self.assertEqual(self.m_house.tag, 'House', 'XML - No House section')
        self.assertEqual(self.m_lights.tag, 'Lights', 'XML - No Lights section')
        self.assertEqual(self.m_light.tag, 'Light', 'XML - No Light section')

    def test_0202_ReadXml(self):
        """ Read in the xml file and fill in the lights
        """
        l_light = self.m_api.read_light_xml(self.m_house)
        self.assertEqual(l_light.City, 'Test City 1', 'Bad city')

    def test_0203_WriteXml(self):
        """ Write out the XML file for the location section
        """
        l_light = self.m_api.read_light_xml(self.m_house)
        l_xml = self.m_api.write_location_xml(l_light)
        print('XML: {0:}'.format(prettify(l_xml)))


    def test_0221_CreateJson(self):
        """ Create a JSON object for Location.
        """
        l_light = self.m_api.read_light_xml(self.m_house)
        l_json = unicode(web_utils.JsonUnicode().encode_json(l_light))
        print('JSON: {0:}'.format(l_json))

# ## END DBK
