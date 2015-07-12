"""
@name:      PyHouse/src/Modules/lights/test/test_lighting_lights.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2014-2015 by D. Brian Kimmel
@note:      Created on May 23, 2014
@license:   MIT License
@summary:   This module is for testing lighting data.

"""

# Import system type stuff
import xml.etree.ElementTree as ET
from twisted.trial import unittest

# Import PyMh files and modules.
from Modules.Core.data_objects import LightData
from Modules.Lighting import lighting_lights
from Modules.Core import conversions
from Modules.Families.family import API as familyAPI
from Modules.Families.Insteon.test.xml_insteon import TESTING_INSTEON_ADDRESS
from Modules.Web import web_utils
from test.xml_data import *
from test.testing_mixin import SetupPyHouseObj
from Modules.Utilities.tools import PrettyPrintAny


class SetupMixin(object):
    """
    """

    def setUp(self, p_root):
        self.m_pyhouse_obj = SetupPyHouseObj().BuildPyHouseObj(p_root)
        self.m_xml = SetupPyHouseObj().BuildXml(p_root)
        self.m_light_obj = LightData()
        self.m_pyhouse_obj.House.RefOBJs.FamilyData = familyAPI(self.m_pyhouse_obj)._init_component_apis(self.m_pyhouse_obj)
        self.m_api = lighting_lights.LLApi(self.m_pyhouse_obj)


class A1_Setup(SetupMixin, unittest.TestCase):
    """
    This section tests the reading and writing of XML used by lighting_lights.
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))

    def test_01_Objects(self):
        """ Be sure that the XML contains the right stuff.
        """
        PrettyPrintAny(self.m_pyhouse_obj, 'PyHouse', 120)
        PrettyPrintAny(self.m_pyhouse_obj.House, 'House', 120)
        PrettyPrintAny(self.m_pyhouse_obj.House.RefOBJs, 'RefObjs', 120)

    def test_02_Family(self):
        """ Be sure that the XML contains the right stuff.
        """
        PrettyPrintAny(self.m_pyhouse_obj.House.RefOBJs.FamilyData, 'Families', 120)
        PrettyPrintAny(self.m_pyhouse_obj.House.RefOBJs.FamilyData['Insteon'], 'Insteon Family', 120)


class A2_XML(SetupMixin, unittest.TestCase):
    """
    This section tests the reading and writing of XML used by lighting_lights.
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))

    def test_01_find_xml(self):
        """ Be sure that the XML contains the right stuff.
        """
        PrettyPrintAny(self.m_pyhouse_obj.Xml, 'PyHouse_obj.Xml', 120)
        self.assertEqual(self.m_xml.root.tag, 'PyHouse', 'Invalid XML - not a PyHouse XML config file')
        self.assertEqual(self.m_xml.house_div.tag, 'HouseDivision', 'XML - No House Division')
        self.assertEqual(self.m_xml.light_sect.tag, 'LightSection', 'XML - No Lights section')
        self.assertEqual(self.m_xml.light.tag, 'Light', 'XML - No Light')

    def test_02_lighting(self):
        l_xml = self.m_xml.light_sect
        PrettyPrintAny(l_xml.find('Light'), 'Light-1', 120)
        PrettyPrintAny(self.m_xml.light, 'Light-2', 120)


class R1_Read(SetupMixin, unittest.TestCase):
    """
    This section tests the reading and writing of XML used by lighting_lights.
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))

    def test_01_LightData(self):
        l_light_obj = self.m_api._read_light_data(self.m_xml.light)
        PrettyPrintAny(l_light_obj, 'Light_Obj R1-1', 120)
        self.assertEqual(l_light_obj.Name, 'Insteon Light')
        self.assertEqual(l_light_obj.Key, 0)
        self.assertEqual(l_light_obj.Active, True)
        self.assertEqual(l_light_obj.Comment, 'SwitchLink On/Off')
        self.assertEqual(l_light_obj.DeviceFamily, 'Insteon')
        self.assertEqual(l_light_obj.CurLevel, 12)
        self.assertEqual(l_light_obj.LightingType, 'Light')
        self.assertEqual(l_light_obj.RoomName, 'Master Bath')

    def test_02_FamilyData(self):
        l_light_obj = self.m_api._read_light_data(self.m_xml.light)
        PrettyPrintAny(l_light_obj, 'Light_Obj Before', 120)
        self.m_api._read_family_data(l_light_obj, self.m_xml.light)
        PrettyPrintAny(l_light_obj, 'Light_Obj After', 120)
        self.assertEqual(l_light_obj.InsteonAddress, conversions.dotted_hex2int(TESTING_INSTEON_ADDRESS))

    def test_03_OneLight(self):
        """ Read in the xml file and fill in the lights
        """
        l_light = self.m_api._read_one_light_xml(self.m_xml.light)
        PrettyPrintAny(l_light, 'ReadOneLight', 120)
        self.assertEqual(l_light.Name, 'Insteon Light')
        self.assertEqual(l_light.Key, 0)
        self.assertEqual(l_light.Active, True)
        self.assertEqual(l_light.Comment, 'SwitchLink On/Off', 'Bad comment')
        self.assertEqual(l_light.IsDimmable, True)
        self.assertEqual(l_light.DeviceFamily, 'Insteon', 'Bad Lighting family')
        self.assertEqual(l_light.RoomName, 'Master Bath')
        self.assertEqual(l_light.LightingType, 'Light', 'Bad LightingType')
        self.assertEqual(l_light.InsteonAddress, conversions.dotted_hex2int(TESTING_INSTEON_ADDRESS))
        self.assertEqual(l_light.RoomCoords, "['0', '0', '0']", 'Bad coords')

    def test_04_AllLights(self):
        l_lights = self.m_api.read_all_lights_xml(self.m_xml.light_sect)
        PrettyPrintAny(l_lights, 'All Lights')
        self.assertEqual(len(l_lights), 2)



class W1_Write(SetupMixin, unittest.TestCase):
    """
    This section tests the reading and writing of XML used by lighting_lights.
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))

    def test_01_Base(self):
        l_light = self.m_api._read_one_light_xml(self.m_xml.light)
        l_xml = self.m_api.write_base_lighting_xml('Light', l_light)
        PrettyPrintAny(l_xml, 'Lights XML')
        PrettyPrintAny(l_xml.attrib, 'Attributes')
        PrettyPrintAny(l_xml._children, 'Children')
        self.assertEqual(l_xml.attrib['Name'], 'Insteon Light')
        self.assertEqual(l_xml.attrib['Key'], '0')
        self.assertEqual(l_xml.attrib['Active'], 'True')

    def test_02_LightData(self):
        l_light = self.m_api._read_one_light_xml(self.m_xml.light)
        l_xml = self.m_api.write_base_lighting_xml('Light', l_light)
        self.m_api._write_light_data(l_light, l_xml)
        PrettyPrintAny(l_xml, 'Lights XML')

    def test_03_LightFamily(self):
        l_light = self.m_api._read_one_light_xml(self.m_xml.light)
        l_xml = self.m_api.write_base_lighting_xml('Light', l_light)
        self.m_api._write_light_data(l_light, l_xml)
        self.m_api._add_family_data(l_light, l_xml)
        PrettyPrintAny(l_xml, 'Lights XML')

    def test_04_OneLight(self):
        """ Write out the XML file for the location section
        """
        l_light = self.m_api._read_one_light_xml(self.m_xml.light)
        l_xml = self.m_api.write_one_light_xml(l_light)
        PrettyPrintAny(l_xml, 'WriteOneLight')

    def test_05_AllLights(self):
        l_lights = self.m_api.read_all_lights_xml(self.m_xml.light_sect)
        PrettyPrintAny(l_lights, 'Read all lights')
        l_xml = self.m_api.write_all_lights_xml(l_lights)
        PrettyPrintAny(l_xml, 'Write All Lights')



class Z1_JSON(SetupMixin, unittest.TestCase):
    """
    This section tests the reading and writing of XML used by lighting_lights.
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))

    def test_01_CreateJson(self):
        """ Create a JSON object for Location.
        """
        l_light = self.m_api.read_all_lights_xml(self.m_xml.light_sect)
        print('Light: {0:}'.format(l_light))
        l_json = unicode(web_utils.JsonUnicode().encode_json(l_light))
        PrettyPrintAny(l_json, 'JSON', 120)
        # self.assertEqual(l_json[0] ['Comment'], 'Switch')

# ## END DBK
