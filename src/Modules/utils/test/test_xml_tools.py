"""
@name: PyHouse/src/Modules/utils/test/test_xml_tools.py
@author: D. Brian Kimmel
@contact: <d.briankimmel@gmail.com
@copyright: 2013-2014 by D. Brian Kimmel
@license: MIT License
@note: Created on Apr 11, 2013
@summary: This module is for testing xml tools.


Tests all working OK - DBK 2014-05-28
"""

# Import system type stuff
# import copy
import xml.etree.ElementTree as ET
from twisted.trial import unittest

# Import PyMh files and modules.
from Modules.Core.data_objects import PyHouseData, HouseData, BaseLightingData
from Modules.utils import xml_tools
from Modules.lights import lighting_lights
from Modules.lights import lighting_controllers
from src.test import xml_data

XML1 = xml_data.XML_LONG

XML = """
<Test b1='True' f1='3.14158265' i1='371' t1='Test of text' >
    <BoolField>True</BoolField>
    <FloatField>3.14158265</FloatField>
    <IntField>371</IntField>
    <TextField>Test of text</TextField>
    <UUIDField>ec97a5c3-89c9-11e3-fedc-0123456789ab</UUIDField>
    <Part_3 b3='True' f3='3.14158265' i3='371' t3='Test of text'>
        <b4>True</b4>
    </Part_3>
</Test>
"""

class Test_02_PutGetXML(unittest.TestCase):
    """
    This series tests the PutGetXML class methods
    """

    def setUp(self):
        self.m_pyhouse_obj = PyHouseData()
        self.m_pyhouse_obj.XmlRoot = ET.fromstring(XML1)
        self.m_fields = ET.fromstring(XML)
        self.m_api = xml_tools.PutGetXML()

    def test_0201_get_bool_element(self):
        result = self.m_api.get_bool_from_xml(self.m_fields, 'BoolField')
        self.assertTrue(result)

    def test_0202_get_bool_attribute(self):
        result = self.m_api.get_bool_from_xml(self.m_fields, 'b1')
        self.assertTrue(result)

    def test_0203_get_bool_compound(self):
        """This should find a path name field
        """
        result = self.m_api.get_bool_from_xml(self.m_fields, './Part_3/b4')
        self.assertTrue(result)

    def test_0211_get_int_element(self):
        result = self.m_api.get_int_from_xml(self.m_fields, 'IntField')
        self.assertEqual(result, 371)

    def test_0212_get_int_attribute(self):
        result = self.m_api.get_int_from_xml(self.m_fields, 'i1')
        self.assertEqual(result, 371)

    def test_0221_get_text_element(self):
        result = self.m_api.get_text_from_xml(self.m_fields, 'TextField')
        self.assertEqual(result, 'Test of text')

    def test_0222_get_text_attribute(self):
        result = self.m_api.get_text_from_xml(self.m_fields, 't1')
        self.assertEqual(result, 'Test of text')

    def test_0223_get_text_default(self):
        result = self.m_api.get_text_from_xml(self.m_fields, 'xxxx', 'No such field')
        self.assertEqual(result, 'No such field')

    def test_0231_get_float_element(self):
        result = self.m_api.get_float_from_xml(self.m_fields, 'FloatField')
        self.assertAlmostEqual(result, float(3.1415825435), places = 5, msg = 'get_float_from_xml failed')

    def test_0232_get_float_attribute(self):
        result = self.m_api.get_float_from_xml(self.m_fields, 'f1')
        self.assertAlmostEqual(result, float(3.1415825435), places = 5, msg = 'get_float_from_xml failed')

    def test_0241_get_uuid_element(self):
        result = self.m_api.get_uuid_from_xml(self.m_fields, 'UUIDField')
        self.assertEqual(result, 'ec97a5c3-89c9-11e3-fedc-0123456789ab')

    def test_0242_get_uuid_attribute(self):
        result = self.m_api.get_uuid_from_xml(self.m_fields, 't1')
        self.assertEqual(result, 'Test of text')


class Test_03_ConfigTools(unittest.TestCase):
    """
    This tests the ConfigTools section
    """

    def setUp(self):
        self.m_pyhouse_obj = PyHouseData()
        self.m_pyhouse_obj.HouseData = HouseData()
        self.m_pyhouse_obj.XmlRoot = self.m_root = ET.fromstring(XML1)
        self.m_houses_xml = self.m_root.find('Houses')
        self.m_house_xml = self.m_houses_xml.find('House')  # First house
        self.m_lights_xml = self.m_house_xml.find('Lights')
        self.m_light_xml = self.m_lights_xml.find('Light')
        self.m_api = xml_tools.ConfigTools()

    def test_0301_readBaseObject(self):
        l_base_obj = BaseLightingData()
        self.m_api.read_base_object_xml(l_base_obj, self.m_light_xml)
        self.assertEqual(l_base_obj.Name, 'Test LR Overhead', 'Bad Name')
        self.assertEqual(l_base_obj.Key, 0, 'Bad Key')
        self.assertEqual(l_base_obj.Active, True, 'Bad Active')
        self.assertEqual(l_base_obj.UUID, 'ec9d9930-89c9-11e3-a1ab-082e5f8cdfd2', 'Bad UUID')


class Test_04_ConfigFile(unittest.TestCase):
    """
    This tests the ConfigFile section
    """

    def setUp(self):
        self.m_pyhouses_obj = PyHouseData()
        self.m_pyhouses_obj.XmlRoot = ET.fromstring(XML1)
        self.m_houses_xml = self.m_pyhouses_obj.XmlRoot.find('Houses')
        self.m_house_xml = self.m_houses_xml.find('House')
        self.m_rooms_xml = self.m_house_xml.find('Rooms')
        self.m_room_xml = self.m_rooms_xml.find('Room')
        self.m_api = xml_tools.ConfigTools()


class Test_05_UnClass(unittest.TestCase):
    """
    This tests the no class routines.
    """

    def setUp(self):
        self.m_pyhouses_obj = PyHouseData()
        self.m_pyhouses_obj.XmlRoot = ET.fromstring(XML1)
        self.m_houses_xml = self.m_pyhouses_obj.XmlRoot.find('Houses')
        self.m_house_xml = self.m_houses_xml.find('House')
        self.m_lights_xml = self.m_house_xml.find('Lights')
        self.m_light_xml = self.m_lights_xml.find('Light')
        self.m_controllers_xml = self.m_house_xml.find('Controllers')
        self.m_controller_xml = self.m_controllers_xml.find('Controller')

    def test_0501_StuffAttrs(self):
        l_objA = lighting_lights.LightingAPI().read_one_light_xml(self.m_light_xml)
        print('A: {0:}'.format(vars(l_objA)))
        l_objB = lighting_controllers.ControllersAPI(self.m_pyhouses_obj).read_one_controller_xml(self.m_controller_xml)
        # l_objAdeep = copy.deepcopy(l_objA)
        print('B: {0:}'.format(vars(l_objB)))
        xml_tools.stuff_new_attrs(l_objA, l_objB)
        print('C: {0:}'.format(vars(l_objA)))
        self.assertEqual(l_objA.Parity, l_objB.Parity)



# ## END DBK
