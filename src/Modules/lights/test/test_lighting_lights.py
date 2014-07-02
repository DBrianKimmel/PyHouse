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
from Modules.Core.data_objects import PyHouseData, LightData
from Modules.lights import lighting_lights
from Modules.families import family
from Modules.web import web_utils
from Modules.utils.tools import PrettyPrintAny
from src.test import xml_data, test_mixin


class SetupMixin(object):
    """
    """

    def setUp(self):
        test_mixin.Setup()
        self.m_pyhouse_obj = test_mixin.SetupPyHouseObj().BuildPyHouse()
        self.m_pyhouse_obj.House.OBJs.FamilyData = family.API().build_lighting_family_info()


class Test_02_XML(SetupMixin, unittest.TestCase):
    """
    This section tests the reading and writing of XML used by lighting_lights.
    """

    def setUp(self):
        self.m_root_xml = ET.fromstring(xml_data.XML_LONG)
        SetupMixin.setUp(self)

        self.m_house_div_xml = self.m_root_xml.find('HouseDivision')
        self.m_light_sect_xml = self.m_house_div_xml.find('LightSection')
        self.m_light_xml = self.m_light_sect_xml.find('Light')
        self.m_light_obj = LightData()

        self.m_api = lighting_lights.LightingLightsAPI(self.m_pyhouse_obj)

    def test_0201_find_xml(self):
        """ Be sure that the XML contains the right stuff.
        """
        self.assertEqual(self.m_root_xml.tag, 'PyHouse', 'Invalid XML - not a PyHouse XML config file')
        self.assertEqual(self.m_house_div_xml.tag, 'HouseDivision', 'XML - No House Division')
        self.assertEqual(self.m_light_sect_xml.tag, 'LightSection', 'XML - No Lights section')
        self.assertEqual(self.m_light_xml.tag, 'Light', 'XML - No Light')
        PrettyPrintAny(self.m_pyhouse_obj, 'PyHouse_obj', 120)
        PrettyPrintAny(self.m_pyhouse_obj.Xml, 'PyHouse_obj.Xml', 120)

    def test_0202_ReadOneLightXml(self):
        """ Read in the xml file and fill in the lights
        """
        l_light = self.m_api.read_one_light_xml(self.m_light_xml)
        self.assertEqual(l_light.Name, 'outside_front', 'Bad Name')
        self.assertEqual(l_light.Key, 0, 'Bad Key')
        self.assertEqual(l_light.Active, True, 'Bad Active')
        # self.assertEqual(l_light.UUID, 'a6907f21-fe3b-11e3-ad9a-082e5f8cdfd2', 'Bad UUID')
        self.assertEqual(l_light.Comment, 'SwitchLink On/Off', 'Bad comment')
        self.assertEqual(l_light.Coords, "['0', '0']", 'Bad coords')
        self.assertEqual(l_light.IsDimmable, False, 'Bad dimmable')
        self.assertEqual(l_light.ControllerFamily, 'Insteon', 'Bad Lighting family')
        self.assertEqual(l_light.RoomName, 'Foyer', 'Bad Room Name')
        self.assertEqual(l_light.LightingType, 'Light', 'Bad LightingType')
        PrettyPrintAny(l_light, 'ReadOneLight', 120)

    def test_0203_ReadAllLightsXml(self):
        l_lights = self.m_api.read_lights_xml(self.m_light_sect_xml)
        self.assertEqual(len(l_lights), 5)

    def test_0211_WriteOneLightXml(self):
        """ Write out the XML file for the location section
        """
        l_light = self.m_api.read_one_light_xml(self.m_light_xml)
        l_xml = self.m_api.write_one_light_xml(l_light)
        PrettyPrintAny(l_xml, 'WriteOneLight')

    def test_0212_WriteAllLights(self):
        l_lights_xml = self.m_api.read_lights_xml(self.m_light_sect_xml)
        l_xml = self.m_api.write_lights_xml(l_lights_xml)
        PrettyPrintAny(l_xml, 'WriteAllLights')

    def test_0281_CreateJson(self):
        """ Create a JSON object for Location.
        """
        l_light = self.m_api.read_lights_xml(self.m_light_sect_xml)
        print('Light: {0:}'.format(l_light))
        l_json = unicode(web_utils.JsonUnicode().encode_json(l_light))
        PrettyPrintAny(l_json, 'JSON', 120)
        # self.assertEqual(l_json[0] ['Comment'], 'Switch')


class Test_03_GetExternalIp(unittest.TestCase):

    def setUp(self):
        self.m_pyhouse_obj = PyHouseData()
        self.m_api = lighting_lights.LightingLightsAPI(None)

    def test_0301_createClient(self):
        # l_client = self.m_api.Start(self.m_pyhouse_obj, self.m_house_obj, self.m_house_xml)
        pass

# ## END DBK
