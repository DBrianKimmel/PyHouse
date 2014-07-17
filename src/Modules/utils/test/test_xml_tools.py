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
from Modules.utils import xml_tools
from Modules.Core.data_objects import BaseLightingData, ThermostatData
from Modules.Core import setup
from Modules.housing import house
from Modules.hvac import thermostat
from Modules.lights import lighting_lights
from Modules.lights import lighting_controllers
from test import xml_data
from Modules.utils.tools import PrettyPrintAny

XML1 = xml_data.XML_LONG

XML = """
<Test b1='True' f1='3.14158265' i1='371' t1='Test of text attribute' >
    <BoolField1>True</BoolField1>
    <BoolField2>False</BoolField2>
    <BoolField3>Howdy</BoolField3>
    <FloatField>3.14158265</FloatField>
    <IntField>371</IntField>
    <TextField1>Test of text element</TextField1>
    <UUIDField>ec97a5c3-89c9-11e3-fedc-0123456789ab</UUIDField>
    <Part_3 b3='True' f3='3.14158265' i3='371' t3='Test of text'>
        <b4>True</b4>
    </Part_3>
</Test>
"""

class SetupMixin(object):
    """
    """

    def setUp(self):
        self.m_pyhouse_obj = setup.build_pyhouse_obj(self)
        self.m_pyhouse_obj.Xml.XmlRoot = self.m_root_xml
        self.m_thermostat_obj = ThermostatData()
        self.m_api = thermostat.API()
        self.m_pyhouse_obj = house.API().update_pyhouse_obj(self.m_pyhouse_obj)
        # PrettyPrintAny(self.m_pyhouse_obj, 'SetupMixin.Setup - PyHouse_obj', 100)
        return self.m_pyhouse_obj


class Test_02_XML(SetupMixin, unittest.TestCase):
    """
    This series tests the PutGetXML class methods
    """

    def setUp(self):
        self.m_root_xml = ET.fromstring(xml_data.XML_LONG)
        self.m_pyhouse_obj = SetupMixin.setUp(self)
        house.API().update_pyhouse_obj(self.m_pyhouse_obj)
        self.m_house_div_xml = self.m_root_xml.find('HouseDivision')
        self.m_thermostat_sect_xml = self.m_house_div_xml.find('ThermostatSection')
        self.m_thermostat_xml = self.m_thermostat_sect_xml.find('Thermostat')

        self.m_pyhouse_obj.Xml.XmlRoot = ET.fromstring(XML1)
        self.m_fields = ET.fromstring(XML)
        self.m_api = xml_tools.PutGetXML()

    def test_0201_BoolElement(self):
        result = self.m_api.get_bool_from_xml(self.m_fields, 'BoolField1')
        self.assertTrue(result)

    def test_0202_BoolAttribute(self):
        result = self.m_api.get_bool_from_xml(self.m_fields, 'b1')
        self.assertTrue(result)

    def test_0203_BoolPath(self):
        """This should find a path name field
        """
        result = self.m_api.get_bool_from_xml(self.m_fields, './Part_3/b4')
        self.assertTrue(result)

    def test_0204_BoolFalse(self):
        result = self.m_api.get_bool_from_xml(self.m_fields, 'BoolField2')
        self.assertFalse(result)

    def test_0205_BoolInvalid(self):
        result = self.m_api.get_bool_from_xml(self.m_fields, 'BoolField3')
        self.assertFalse(result)

    def test_0206_BoolMissing(self):
        result = self.m_api.get_bool_from_xml(self.m_fields, 'BoolField999')
        self.assertFalse(result)



    def test_0211_IntElement(self):
        result = self.m_api.get_int_from_xml(self.m_fields, 'IntField')
        self.assertEqual(result, 371)

    def test_0212_IntAttribute(self):
        result = self.m_api.get_int_from_xml(self.m_fields, 'i1')
        self.assertEqual(result, 371)



    def test_0221_TextElement(self):
        result = self.m_api.get_text_from_xml(self.m_fields, 'TextField1')
        self.assertEqual(result, 'Test of text element')

    def test_0222_TextAttribute(self):
        result = self.m_api.get_text_from_xml(self.m_fields, 't1')
        self.assertEqual(result, 'Test of text attribute')

    def test_0223_TextInvalid(self):
        result = self.m_api.get_text_from_xml(self.m_fields, 'xxxx', '0223 No such field')
        self.assertEqual(result, '0223 No such field')



    def test_0231_FloatElement(self):
        result = self.m_api.get_float_from_xml(self.m_fields, 'FloatField')
        self.assertAlmostEqual(result, float(3.1415825435), places = 5, msg = 'get_float_from_xml failed')

    def test_0232_FloatAttribute(self):
        result = self.m_api.get_float_from_xml(self.m_fields, 'f1')
        self.assertAlmostEqual(result, float(3.1415825435), places = 5, msg = 'get_float_from_xml failed')



    def test_0241_UuidElement(self):
        result = self.m_api.get_uuid_from_xml(self.m_fields, 'UUIDField')
        self.assertEqual(result, 'ec97a5c3-89c9-11e3-fedc-0123456789ab')

    def test_0242_UuidAttribute(self):
        result = self.m_api.get_uuid_from_xml(self.m_fields, 't1')
        self.assertEqual(result, 'Test of text attribute')


class Test_03_ConfigTools(SetupMixin, unittest.TestCase):
    """
    This tests the ConfigTools section
    """

    def setUp(self):
        self.m_root_xml = ET.fromstring(xml_data.XML_LONG)
        self.m_pyhouse_obj = SetupMixin.setUp(self)
        house.API().update_pyhouse_obj(self.m_pyhouse_obj)
        self.m_house_div_xml = self.m_root_xml.find('HouseDivision')
        self.m_light_sect_xml = self.m_house_div_xml.find('LightSection')
        self.m_light_xml = self.m_light_sect_xml.find('Light')
        self.m_api = xml_tools.XmlConfigTools()

    def test_0301_readBaseObject(self):
        l_base_obj = BaseLightingData()
        self.m_api.read_base_object_xml(l_base_obj, self.m_light_xml)
        self.assertEqual(l_base_obj.Name, 'outside_front', 'Bad Name')
        self.assertEqual(l_base_obj.Key, 0, 'Bad Key')
        self.assertEqual(l_base_obj.Active, True, 'Bad Active')
        # self.assertEqual(l_base_obj.UUID, 'ec9d9930-89c9-11e3-a1ab-082e5f8cdfd2', 'Bad UUID')

    def test_0302_writeBaseObject(self):
        l_base_obj = BaseLightingData()
        self.m_api.read_base_object_xml(l_base_obj, self.m_light_xml)
        l_xml = self.m_api.write_base_object_xml('Light', l_base_obj)
        PrettyPrintAny(l_xml, 'Base Object XML', 120)


class Test_05_UnClass(SetupMixin, unittest.TestCase):
    """
    This tests the no class routines.
    """

    def setUp(self):
        self.m_root_xml = ET.fromstring(xml_data.XML_LONG)
        self.m_pyhouse_obj = SetupMixin.setUp(self)
        house.API().update_pyhouse_obj(self.m_pyhouse_obj)
        self.m_house_div_xml = self.m_root_xml.find('HouseDivision')
        self.m_thermostat_sect_xml = self.m_house_div_xml.find('ThermostatSection')
        self.m_thermostat_xml = self.m_thermostat_sect_xml.find('Thermostat')
        self.m_light_sect_xml = self.m_house_div_xml.find('LightSection')
        self.m_light_xml = self.m_light_sect_xml.find('Light')
        self.m_controller_sect_xml = self.m_house_div_xml.find('ControllerSection')
        self.m_controller_xml = self.m_controller_sect_xml.find('Controller')

    def test_0501_StuffAttrs(self):
        l_objA = lighting_lights.LightingLightsAPI(self.m_pyhouse_obj).read_one_light_xml(self.m_light_xml)
        PrettyPrintAny(l_objA, 'Obj A', 120)
        l_objB = lighting_controllers.ControllersAPI(self.m_pyhouse_obj).read_one_controller_xml(self.m_controller_xml)
        # l_objAdeep = copy.deepcopy(l_objA)
        PrettyPrintAny(l_objB, 'Obj B', 120)
        xml_tools.stuff_new_attrs(l_objA, l_objB)
        PrettyPrintAny(l_objA, 'Result B stuffed into A', 120)
        self.assertEqual(l_objA.Parity, l_objB.Parity)



# ## END DBK
