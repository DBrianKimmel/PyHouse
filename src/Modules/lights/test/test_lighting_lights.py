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
from Modules.Core import conversions
from Modules.families import family
from Modules.web import web_utils
from Modules.utils.tools import PrettyPrintAny
from test import xml_data
from test.testing_mixin import SetupPyHouseObj


class SetupMixin(object):
    """
    """

    def setUp(self, p_root):
        self.m_pyhouse_obj = SetupPyHouseObj().BuildPyHouseObj(p_root)
        self.m_xml = SetupPyHouseObj().BuildXml(p_root)


class Test_02_XML(SetupMixin, unittest.TestCase):
    """
    This section tests the reading and writing of XML used by lighting_lights.
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(xml_data.XML_LONG))
        self.m_pyhouse_obj.House.OBJs.FamilyData = family.API().build_lighting_family_info()
        self.m_light_obj = LightData()
        self.m_api = lighting_lights.LightingLightsAPI(self.m_pyhouse_obj)

    def test_0201_find_xml(self):
        """ Be sure that the XML contains the right stuff.
        """
        self.assertEqual(self.m_xml.root.tag, 'PyHouse', 'Invalid XML - not a PyHouse XML config file')
        self.assertEqual(self.m_xml.house_div.tag, 'HouseDivision', 'XML - No House Division')
        self.assertEqual(self.m_xml.light_sect.tag, 'LightSection', 'XML - No Lights section')
        self.assertEqual(self.m_xml.light.tag, 'Light', 'XML - No Light')
        PrettyPrintAny(self.m_pyhouse_obj, 'PyHouse_obj', 120)
        PrettyPrintAny(self.m_pyhouse_obj.Xml, 'PyHouse_obj.Xml', 120)

    def test_0211_ReadLightData(self):
        l_light_obj = self.m_api._read_light_data(self.m_xml.light)
        PrettyPrintAny(l_light_obj, 'Light_Obj', 120)
        self.assertEqual(l_light_obj.IsController, 'True')
        self.assertEqual(l_light_obj.CurLevel, 73)
        self.assertEqual(l_light_obj.ControllerFamily, 'Insteon')

    def test_0212_ReadFamilyData(self):
        l_light_obj = self.m_api._read_light_data(self.m_xml.light)
        l_api = self.m_api._read_family_data(l_light_obj, self.m_xml.light)
        PrettyPrintAny(l_light_obj, 'Light_Obj After', 120)
        print('Address   {0:}'.format(conversions.int2dotted_hex(l_light_obj.InsteonAddress, 3)))
        self.assertEqual(l_light_obj.InsteonAddress, conversions.dotted_hex2int('16.62.2D'))

    def test_0213_ReadOneLightXml(self):
        """ Read in the xml file and fill in the lights
        """
        l_light = self.m_api.read_one_light_xml(self.m_xml.light)
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

    def test_0214_ReadAllLightsXml(self):
        l_lights = self.m_api.read_all_lights_xml(self.m_xml.light_sect)
        self.assertEqual(len(l_lights), 5)


    def test_0221_WriteLightData(self):
        self.m_light_obj = self.m_api._read_light_data(self.m_xml.light)
        pass

    def test_0222_WriteLightFamily(self):
        self.m_api._read_family_data(self.m_light_obj, self.m_xml)
        pass

    def test_0223_WriteOneLightXml(self):
        """ Write out the XML file for the location section
        """
        l_light = self.m_api.read_one_light_xml(self.m_xml.light)
        l_xml = self.m_api.write_one_light_xml(l_light)
        PrettyPrintAny(l_xml, 'WriteOneLight')

    def test_0224_WriteAllLights(self):
        l_lights_xml = self.m_api.read_all_lights_xml(self.m_xml.light_sect)
        l_xml = self.m_api.write_all_lights_xml(l_lights_xml)
        PrettyPrintAny(l_xml, 'WriteAllLights')

    def test_0281_CreateJson(self):
        """ Create a JSON object for Location.
        """
        l_light = self.m_api.read_all_lights_xml(self.m_xml.light_sect)
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
