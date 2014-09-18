"""
@name: PyHouse/src/Modules/Utilities/test/test_xml_tools.py
@author: D. Brian Kimmel
@contact: D.BrianKimmel@gmail.com
@copyright: 2013-2014 by D. Brian Kimmel
@license: MIT License
@note: Created on Apr 11, 2013
@summary: This module is for testing XML tools.


Tests all working OK - DBK 2014-05-28
"""

# Import system type stuff
# import copy
import xml.etree.ElementTree as ET
from twisted.trial import unittest

# Import PyMh files and modules.
from Modules.Utilities import xml_tools
from Modules.Core.data_objects import BaseLightingData, ControllerData
from Modules.Lighting import lighting_lights
from Modules.Lighting import lighting_controllers
from test import xml_data
from test.testing_mixin import SetupPyHouseObj
from Modules.Utilities.tools import PrettyPrintAny

XML = """
<Test b1='True' f1='3.14158265' i1='371' t1='Test of text attribute' >
    <BoolField1>True</BoolField1>
    <BoolField2>False</BoolField2>
    <BoolField3>Howdy</BoolField3>
    <FloatField>3.14158265</FloatField>
    <IntField>371</IntField>
    <TextField1>Test of text element</TextField1>
    <UUIDField>01234567-fedc-2468-7531-0123456789ab</UUIDField>
    <Part_3 b3='True' f3='3.14158265' i3='371' t3='Test of text'>
        <b4>True</b4>
    </Part_3>
</Test>
"""

class SetupMixin(object):
    """
    """

    def setUp(self, p_root):
        self.m_pyhouse_obj = SetupPyHouseObj().BuildPyHouseObj(p_root)
        self.m_xml = SetupPyHouseObj().BuildXml(p_root)


class Test_02_XML(SetupMixin, unittest.TestCase):
    """
    This series tests the PutGetXML class methods
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(xml_data.XML_LONG))
        self.m_fields = ET.fromstring(XML)
        self.m_api = xml_tools.PutGetXML()

    def test_0201_GetElement(self):
        l_elem = self.m_api._get_element_field(self.m_fields, 'TextField1')
        self.assertEqual(l_elem, 'Test of text element')
        print('Element = {0:}'.format(l_elem))

    def test_0202_GetElement_attribute(self):
        l_elem = self.m_api._get_element_field(self.m_fields, 't1')
        self.assertEqual(l_elem, None)
        print('Element = {0:}'.format(l_elem))

    def test_0203_GetElement_Missing(self):
        l_elem = self.m_api._get_element_field(self.m_fields, 'MissingElement')
        self.assertEqual(l_elem, None)
        print('Element = {0:}'.format(l_elem))


    def test_0211_GetAttribute(self):
        l_attr = self.m_api._get_attribute_field(self.m_fields, 't1')
        self.assertEqual(l_attr, 'Test of text attribute')
        print('Attribute = {0:}'.format(l_attr))

    def test_0212_GetAttribute_element(self):
        l_attr = self.m_api._get_attribute_field(self.m_fields, 'TextField1')
        self.assertEqual(l_attr, None)
        print('Attribute = {0:}'.format(l_attr))

    def test_0213_GetAttribute_Missing(self):
        l_attr = self.m_api._get_attribute_field(self.m_fields, 'MissingAttribute')
        self.assertEqual(l_attr, None)
        print('Attribute = {0:}'.format(l_attr))


    def test_0221_GetAnyField_Element(self):
        l_field = self.m_api._get_any_field(self.m_fields, 'TextField1')
        self.assertEqual(l_field, 'Test of text element')
        print('Element = {0:}'.format(l_field))

    def test_0222_GetAnyField_Attribute(self):
        l_field = self.m_api._get_any_field(self.m_fields, 't1')
        self.assertEqual(l_field, 'Test of text attribute')
        print('Element = {0:}'.format(l_field))

    def test_0223_GetAnyField_Missing(self):
        l_field = self.m_api._get_any_field(self.m_fields, 'NoSuchField')
        self.assertEqual(l_field, None)
        print('Element = {0:}'.format(l_field))


    def test_0231_GetBoolElement(self):
        result = self.m_api.get_bool_from_xml(self.m_fields, 'BoolField1')
        self.assertTrue(result)

    def test_0232_GetBoolAttribute(self):
        result = self.m_api.get_bool_from_xml(self.m_fields, 'b1')
        self.assertTrue(result)

    def test_0233_GetBoolPath(self):
        """This should find a path name field
        """
        result = self.m_api.get_bool_from_xml(self.m_fields, './Part_3/b4')
        self.assertTrue(result)

    def test_0234_GetBoolFalse(self):
        result = self.m_api.get_bool_from_xml(self.m_fields, 'BoolField2')
        self.assertFalse(result)

    def test_0235_GetBoolInvalid(self):
        result = self.m_api.get_bool_from_xml(self.m_fields, 'BoolField3')
        self.assertFalse(result)

    def test_0236_GetBoolMissing(self):
        result = self.m_api.get_bool_from_xml(self.m_fields, 'BoolField999')
        self.assertFalse(result)

    def test_0237_PutBoolElement(self):
        l_element = ET.Element('TestBoolElement_1')
        self.m_api.put_bool_element(l_element, 'Active', True)
        PrettyPrintAny(l_element, 'bool', 120)

    def test_0238_PutBoolAttribute(self):
        l_element = ET.Element('TestBoolAttribute_2')
        self.m_api.put_bool_attribute(l_element, 'Active', True)
        PrettyPrintAny(l_element, 'bool', 120)


    def test_0241_GetIntElement(self):
        result = self.m_api.get_int_from_xml(self.m_fields, 'IntField')
        self.assertEqual(result, 371)

    def test_0242_GetIntAttribute(self):
        result = self.m_api.get_int_from_xml(self.m_fields, 'i1')
        self.assertEqual(result, 371)

    def test_0243_PutIntElement(self):
        l_element = ET.Element('TestIntElement_1')
        self.m_api.put_int_element(l_element, 'IntNumber', -57)
        PrettyPrintAny(l_element, 'bool', 120)

    def test_0244_PutIntAttribute(self):
        l_element = ET.Element('TestIntAttribute_2')
        self.m_api.put_int_attribute(l_element, 'IntNumber', 853)
        PrettyPrintAny(l_element, 'bool', 120)


    def test_0251_GetTextElement(self):
        l_text = self.m_api.get_text_from_xml(self.m_fields, 'TextField1')
        self.assertEqual(l_text, 'Test of text element')
        print('Text = {0:}'.format(l_text))

    def test_0252_GetTextAttribute(self):
        l_text = self.m_api.get_text_from_xml(self.m_fields, 't1')
        self.assertEqual(l_text, 'Test of text attribute')
        print('Text = {0:}'.format(l_text))

    def test_0253_GetTextInvalid(self):
        l_text = self.m_api.get_text_from_xml(self.m_fields, 'NoSuchField', '0223 No such field')
        self.assertEqual(l_text, '0223 No such field')
        print('Text = {0:}'.format(l_text))

    def test_0253_GetTextInvalid_NoDefault(self):
        l_text = self.m_api.get_text_from_xml(self.m_fields, 'NoSuchField')
        self.assertEqual(l_text, 'None')
        print('Text = {0:}'.format(l_text))

    def test_0254_PutTextElement(self):
        l_element = ET.Element('TestTextElement_1')
        self.m_api.put_int_element(l_element, 'Comment', 'Arbitrary Comment')
        PrettyPrintAny(l_element, 'XML A', 120)

    def test_0255_PutTextAttribute(self):
        l_element = ET.Element('TestTextAttribute_2')
        self.m_api.put_text_attribute(l_element, 'Name', 'Any old Name')
        PrettyPrintAny(l_element, 'XML B', 120)



    def test_0261_GetFloatElement(self):
        result = self.m_api.get_float_from_xml(self.m_fields, 'FloatField')
        self.assertAlmostEqual(result, float(3.1415825435), places = 5, msg = 'get_float_from_xml failed')

    def test_0262_GetFloatAttribute(self):
        result = self.m_api.get_float_from_xml(self.m_fields, 'f1')
        self.assertAlmostEqual(result, float(3.1415825435), places = 5, msg = 'get_float_from_xml failed')



    def test_0271_GetUuidElement(self):
        """UUID elements must be returned intact
        """
        l_uuid = self.m_api.get_uuid_from_xml(self.m_fields, 'UUIDField')
        self.assertEqual(l_uuid, '01234567-fedc-2468-7531-0123456789ab')
        print('UUID = {0:}'.format(l_uuid))

    def test_0272_GetUuidAttribute(self):
        l_uuid = self.m_api.get_uuid_from_xml(self.m_fields, 'IntField')
        # self.assertNotEqual(l_uuid, None)
        print('UUID = {0:}'.format(l_uuid))

    def test_0273_GetUuidMissing(self):
        l_uuid = self.m_api.get_uuid_from_xml(self.m_fields, 'NoSuchField')
        self.assertEqual(l_uuid, None)
        print('UUID = {0:}'.format(l_uuid))


class Test_03_ConfigTools(SetupMixin, unittest.TestCase):
    """
    This tests the ConfigTools section
    """

    def setUp(self):
        self.m_pyhouse_obj = SetupMixin.setUp(self, ET.fromstring(xml_data.XML_LONG))
        self.m_api = xml_tools.XmlConfigTools()

    def test_0301_readBaseObject(self):
        l_base_obj = BaseLightingData()
        self.m_api.read_base_object_xml(l_base_obj, self.m_xml.light)
        self.assertEqual(l_base_obj.Name, 'outside_front', 'Bad Name')
        self.assertEqual(l_base_obj.Key, 0, 'Bad Key')
        self.assertEqual(l_base_obj.Active, True, 'Bad Active')
        # self.assertEqual(l_base_obj.UUID, 'ec9d9930-89c9-11e3-a1ab-082e5f8cdfd2', 'Bad UUID')

    def test_0302_readBaseObject(self):
        l_base_obj = BaseLightingData()
        self.m_api.read_base_object_xml(l_base_obj, self.m_xml.controller)
        self.assertEqual(l_base_obj.Name, 'PLM_1', 'Bad Name')
        self.assertEqual(l_base_obj.Key, 0, 'Bad Key')
        self.assertEqual(l_base_obj.Active, False, 'Bad Active')

    def test_0311_writeBaseObject(self):
        l_base_obj = BaseLightingData()
        self.m_api.read_base_object_xml(l_base_obj, self.m_xml.light)
        l_xml = self.m_api.write_base_object_xml('Light', l_base_obj)
        PrettyPrintAny(l_xml, 'Base Object XML', 120)


class Test_05_NoClass(SetupMixin, unittest.TestCase):
    """
    This tests the no class routines.
    """

    def setUp(self):
        self.m_pyhouse_obj = SetupMixin.setUp(self, ET.fromstring(xml_data.XML_LONG))

    def test_0501_StuffAttrs(self):
        # l_objA = lighting_lights.LightingLightsAPI(self.m_pyhouse_obj).read_one_light_xml(self.m_xml.light)
        l_objA = BaseLightingData()
        PrettyPrintAny(l_objA, 'Obj A', 120)
        # l_objB = lighting_controllers.ControllersAPI(self.m_pyhouse_obj).read_one_controller_xml(self.m_xml.controller)
        l_objB = ControllerData()
        # l_objAdeep = copy.deepcopy(l_objA)
        PrettyPrintAny(l_objB, 'Obj B', 120)
        xml_tools.stuff_new_attrs(l_objA, l_objB)
        PrettyPrintAny(l_objA, 'Result B stuffed into A', 120)
        self.assertEqual(l_objA.IsDimmable, l_objB.IsDimmable)



# ## END DBK
