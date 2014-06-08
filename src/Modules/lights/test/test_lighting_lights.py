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
from Modules.Core.data_objects import PyHouseData, HouseData
from Modules.lights import lighting_lights
from Modules.web import web_utils
from Modules.utils.tools import PrettyPrintAny
from src.test import xml_data

XML = xml_data.XML_LONG


class Test_02_ReadXML(unittest.TestCase):
    """ This section tests the reading and writing of XML used by node_local.
    """

    def _pyHouses(self):
        self.m_pyhouse_obj = PyHouseData()
        self.m_pyhouse_obj.HouseData = HouseData()
        self.m_pyhouse_obj.XmlRoot = self.m_root = ET.fromstring(XML)
        self.m_houses_xml = self.m_root.find('Houses')
        self.m_house_xml = self.m_houses_xml.find('House')
        self.m_lights_xml = self.m_house_xml.find('Lights')
        self.m_light_xml = self.m_lights_xml.find('Light')
        self.m_api = lighting_lights.LightingAPI()

    def setUp(self):
        self._pyHouses()

    def test_0201_find_xml(self):
        """ Be sure that the XML contains the right stuff.
        """
        self.assertEqual(self.m_root.tag, 'PyHouse', 'Invalid XML - not a PyHouse XML config file')
        self.assertEqual(self.m_houses_xml.tag, 'Houses', 'XML - No Houses section')
        self.assertEqual(self.m_house_xml.tag, 'House', 'XML - No House section')
        self.assertEqual(self.m_lights_xml.tag, 'Lights', 'XML - No Lights section')
        self.assertEqual(self.m_light_xml.tag, 'Light', 'XML - No Light section')

    def test_0202_ReadOneLightXml(self):
        """ Read in the xml file and fill in the lights
        """
        l_light = self.m_api.read_one_light_xml(self.m_light_xml)
        self.assertEqual(l_light.Name, 'Test LR Overhead', 'Bad Name')
        self.assertEqual(l_light.Key, 0, 'Bad Key')
        self.assertEqual(l_light.Active, True, 'Bad Active')
        self.assertEqual(l_light.UUID, 'ec9d9930-89c9-11e3-a1ab-082e5f8cdfd2', 'Bad UUID')
        self.assertEqual(l_light.Comment, 'SwitchLink On/Off', 'Bad comment')
        self.assertEqual(l_light.Coords, "['0', '0']", 'Bad coords')
        self.assertEqual(l_light.Dimmable, False, 'Bad dimmable')
        self.assertEqual(l_light.Family, 'Insteon', 'Bad family')
        self.assertEqual(l_light.RoomName, 'Test Living Room', 'Bad Room Name')
        self.assertEqual(l_light.Type, 'Light', 'Bad Type')

    def test_0203_ReadLightsXml(self):
        l_lights = self.m_api.read_lights_xml(self.m_house_xml)
        # print('Lights {0:}'.format(l_lights))
        self.assertEqual(len(l_lights), 2)

    def test_0211_WriteOneLightXml(self):
        """ Write out the XML file for the location section
        """
        l_light = self.m_api.read_one_light_xml(self.m_house_xml)
        l_xml = self.m_api.write_one_light_xml(l_light)
        print('XML: {0:}'.format(PrettyPrintAny(l_xml)))

    def test_0212_WriteAllLights(self):
        l_lights_xml = self.m_api.read_lights_xml(self.m_house_xml)
        l_xml = self.m_api.write_lights_xml(l_lights_xml)
        print('XML: {0:}'.format(PrettyPrintAny(l_xml)))

    def test_0221_CreateJson(self):
        """ Create a JSON object for Location.
        """
        l_light = self.m_api.read_lights_xml(self.m_house_xml)
        print('Light: {0:}'.format(l_light))
        l_json = unicode(web_utils.JsonUnicode().encode_json(l_light))
        PrettyPrintAny(l_json)
        # self.assertEqual(l_json[0] ['Comment'], 'Switch')

# ## END DBK
