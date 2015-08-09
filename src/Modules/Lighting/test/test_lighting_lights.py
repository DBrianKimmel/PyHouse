"""
@name:      PyHouse/src/Modules/lights/test/test_lighting_lights.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2014-2015 by D. Brian Kimmel
@note:      Created on May 23, 2014
@license:   MIT License
@summary:   This module is for testing lighting data.

Passed all 15 tests - DBK - 2015-08-02

"""

# Import system type stuff
import xml.etree.ElementTree as ET
from twisted.trial import unittest

# Import PyMh files and modules.
from Modules.Core.data_objects import LightData
from Modules.Lighting.lighting_lights import Utility, API as lightsAPI
from Modules.Core import conversions
from Modules.Families.family import API as familyAPI
from Modules.Lighting.test.xml_lights import \
        TESTING_LIGHT_DIMMABLE, \
        TESTING_LIGHTING_LIGHT_CUR_LEVEL, \
        TESTING_LIGHTING_LIGHTS_NAME_1, \
        TESTING_LIGHTING_TYPE
from Modules.Families.Insteon.test.xml_insteon import \
        TESTING_INSTEON_ADDRESS
from Modules.Core.test.xml_device import TESTING_DEVICE_COMMENT, TESTING_DEVICE_FAMILY, \
        TESTING_DEVICE_ROOM_NAME, \
        TESTING_DEVICE_UUID, \
        TESTING_DEVICE_TYPE, \
        TESTING_DEVICE_SUBTYPE, \
        TESTING_DEVICE_ROOM_X, \
        TESTING_DEVICE_ROOM_Y, \
        TESTING_DEVICE_ROOM_Z
from Modules.Web import web_utils
from test.xml_data import XML_LONG
from test.testing_mixin import SetupPyHouseObj
from Modules.Utilities.tools import PrettyPrintAny


class SetupMixin(object):
    """
    """

    def setUp(self, p_root):
        self.m_pyhouse_obj = SetupPyHouseObj().BuildPyHouseObj(p_root)
        self.m_xml = SetupPyHouseObj().BuildXml(p_root)
        self.m_family = familyAPI(self.m_pyhouse_obj).LoadFamilyTesting()
        self.m_pyhouse_obj.House.FamilyData = self.m_family
        self.m_api = lightsAPI()
        self.m_light_obj = LightData()
        self.m_version = '1.4.0'


class A1_Setup(SetupMixin, unittest.TestCase):
    """
    This section tests the reading and writing of XML used by lighting_lights.
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))

    def test_01_Objects(self):
        """ Be sure that the XML contains the right stuff.
        """
        # PrettyPrintAny(self.m_pyhouse_obj, 'PyHouse', 120)
        # PrettyPrintAny(self.m_pyhouse_obj.House, 'House', 120)
        pass

    def test_02_Family(self):
        """ Be sure that the XML contains the right stuff.
        """
        # PrettyPrintAny(self.m_pyhouse_obj.House.FamilyData, 'Families', 120)
        # PrettyPrintAny(self.m_pyhouse_obj.House.FamilyData['Insteon'], 'Insteon Family', 120)
        pass


class A2_XML(SetupMixin, unittest.TestCase):
    """
    This section tests the reading and writing of XML used by lighting_lights.
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))

    def test_01_find_xml(self):
        """ Be sure that the XML contains the right stuff.
        """
        # PrettyPrintAny(self.m_pyhouse_obj.Xml, 'PyHouse_obj.Xml', 120)
        self.assertEqual(self.m_xml.root.tag, 'PyHouse', 'Invalid XML - not a PyHouse XML config file')
        self.assertEqual(self.m_xml.house_div.tag, 'HouseDivision', 'XML - No House Division')
        self.assertEqual(self.m_xml.light_sect.tag, 'LightSection', 'XML - No Lights section')
        self.assertEqual(self.m_xml.light.tag, 'Light', 'XML - No Light')

    def test_02_lighting(self):
        l_xml = self.m_xml.light_sect
        # PrettyPrintAny(l_xml.find('Light'), 'Light-1', 120)
        # PrettyPrintAny(self.m_xml.light, 'Light-2', 120)


class R1_Read(SetupMixin, unittest.TestCase):
    """
    This section tests the reading and writing of XML used by lighting_lights.
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))
        self.m_version = '1.4.0'

    def test_01_Base(self):
        l_obj = Utility._read_base_device(self.m_xml.light, self.m_version)
        # PrettyPrintAny(l_obj, 'Base')
        self.assertEqual(l_obj.Name, TESTING_LIGHTING_LIGHTS_NAME_1)
        self.assertEqual(l_obj.Key, 0)
        self.assertEqual(l_obj.Active, True)
        self.assertEqual(l_obj.Comment, TESTING_DEVICE_COMMENT)
        self.assertEqual(l_obj.DeviceFamily, TESTING_DEVICE_FAMILY)
        self.assertEqual(l_obj.DeviceType, int(TESTING_DEVICE_TYPE))
        self.assertEqual(l_obj.DeviceSubType, int(TESTING_DEVICE_SUBTYPE))
        self.assertEqual(l_obj.LightingType, TESTING_LIGHTING_TYPE)
        self.assertEqual(l_obj.RoomName, TESTING_DEVICE_ROOM_NAME)
        self.assertEqual(l_obj.UUID, TESTING_DEVICE_UUID)
        self.assertEqual(l_obj.RoomCoords.X_Easting, float(TESTING_DEVICE_ROOM_X))
        self.assertEqual(l_obj.RoomCoords.Y_Northing, float(TESTING_DEVICE_ROOM_Y))
        self.assertEqual(l_obj.RoomCoords.Z_Height, float(TESTING_DEVICE_ROOM_Z))

    def test_02_LightData(self):
        l_obj = Utility._read_base_device(self.m_xml.light, self.m_version)
        Utility._read_light_data(l_obj, self.m_xml.light, self.m_version)
        self.assertEqual(l_obj.CurLevel, int(TESTING_LIGHTING_LIGHT_CUR_LEVEL))
        self.assertEqual(l_obj.IsDimmable, bool(TESTING_LIGHT_DIMMABLE))

    def test_03_FamilyData(self):
        l_obj = Utility._read_base_device(self.m_xml.light, self.m_version)
        Utility._read_family_data(self.m_pyhouse_obj, l_obj, self.m_xml.light, self.m_version)
        self.assertEqual(l_obj.InsteonAddress, conversions.dotted_hex2int(TESTING_INSTEON_ADDRESS))

    def test_04_OneLight(self):
        """ Read in the xml file and fill in the lights
        """
        l_obj = Utility._read_one_light_xml(self.m_pyhouse_obj, self.m_xml.light, self.m_version)
        # PrettyPrintAny(l_obj, 'ReadOneLight', 120)
        self.assertEqual(l_obj.Name, TESTING_LIGHTING_LIGHTS_NAME_1)
        self.assertEqual(l_obj.Name, 'Insteon Light')
        self.assertEqual(l_obj.Key, 0)
        self.assertEqual(l_obj.Active, True)
        self.assertEqual(l_obj.Comment, TESTING_DEVICE_COMMENT)
        self.assertEqual(l_obj.DeviceFamily, TESTING_DEVICE_FAMILY)
        self.assertEqual(l_obj.RoomName, TESTING_DEVICE_ROOM_NAME)
        self.assertEqual(l_obj.LightingType, 'Light')
        self.assertEqual(l_obj.InsteonAddress, conversions.dotted_hex2int(TESTING_INSTEON_ADDRESS))
        self.assertEqual(l_obj.RoomCoords.X_Easting, float(TESTING_DEVICE_ROOM_X))

    def test_05_AllLights(self):
        l_objs = self.m_api.read_all_lights_xml(self.m_pyhouse_obj, self.m_xml.light_sect, self.m_version)
        # PrettyPrintAny(l_objs, 'All Lights')
        self.assertEqual(len(l_objs), 2)



class W1_Write(SetupMixin, unittest.TestCase):
    """
    This section tests the reading and writing of XML used by lighting_lights.
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))
        self.m_version = '1.4.0'

    def test_01_Base(self):
        l_obj = Utility._read_one_light_xml(self.m_pyhouse_obj, self.m_xml.light, self.m_version)
        l_xml = Utility._write_base_device('Light', l_obj)
        self.assertEqual(l_xml.attrib['Name'], TESTING_LIGHTING_LIGHTS_NAME_1)
        self.assertEqual(l_xml.attrib['Key'], '0')
        self.assertEqual(l_xml.attrib['Active'], 'True')
        self.assertEqual(l_xml.find('UUID').text, TESTING_DEVICE_UUID)
        self.assertEqual(l_xml.find('Comment').text, TESTING_DEVICE_COMMENT)
        self.assertEqual(l_xml.find('DeviceFamily').text, TESTING_DEVICE_FAMILY)
        self.assertEqual(l_xml.find('RoomName').text, TESTING_DEVICE_ROOM_NAME)
        self.assertEqual(l_xml.find('UUID').text, TESTING_DEVICE_UUID)
        self.assertEqual(l_xml.find('UUID').text, TESTING_DEVICE_UUID)
        self.assertEqual(l_xml.find('UUID').text, TESTING_DEVICE_UUID)


    def test_02_LightData(self):
        l_obj = Utility._read_one_light_xml(self.m_pyhouse_obj, self.m_xml.light, self.m_version)
        l_xml = Utility._write_base_device('Light', l_obj)
        Utility._write_light_data(l_obj, l_xml)
        # PrettyPrintAny(l_xml, 'Lights XML')

    def test_03_LightFamily(self):
        l_obj = Utility._read_one_light_xml(self.m_pyhouse_obj, self.m_xml.light, self.m_version)
        l_xml = Utility._write_base_device('Light', l_obj)
        Utility._write_light_data(l_obj, l_xml)
        Utility._read_family_data(self.m_pyhouse_obj, l_obj, l_xml, self.m_version)
        # PrettyPrintAny(l_xml, 'Lights XML')

    def test_04_OneLight(self):
        """ Write out the XML file for the location section
        """
        l_obj = Utility._read_one_light_xml(self.m_pyhouse_obj, self.m_xml.light, self.m_version)
        l_xml = Utility._write_one_light_xml(self.m_pyhouse_obj, l_obj)
        # PrettyPrintAny(l_xml, 'WriteOneLight')

    def test_05_AllLights(self):
        l_objs = self.m_api.read_all_lights_xml(self.m_pyhouse_obj, self.m_xml.light_sect, self.m_version)
        # PrettyPrintAny(l_objs, 'Read all lights')
        l_xml = lightsAPI.write_all_lights_xml(self.m_pyhouse_obj)
        # PrettyPrintAny(l_xml, 'Write All Lights')



class Z1_JSON(SetupMixin, unittest.TestCase):
    """
    This section tests the reading and writing of XML used by lighting_lights.
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))
        self.m_version = '1.4.0'

    def test_01_CreateJson(self):
        """ Create a JSON object for Location.
        """
        l_obj = self.m_api.read_all_lights_xml(self.m_pyhouse_obj, self.m_xml.light_sect, self.m_version)
        # print('Light: {0:}'.format(l_obj))
        l_json = unicode(web_utils.JsonUnicode().encode_json(l_obj))
        # PrettyPrintAny(l_json, 'JSON', 120)
        # self.assertEqual(l_json[0] ['Comment'], 'Switch')

# ## END DBK
