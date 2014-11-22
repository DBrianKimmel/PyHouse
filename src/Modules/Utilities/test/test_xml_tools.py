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
import datetime

# Import PyMh files and modules.
from Modules.Utilities import xml_tools
from Modules.Utilities import convert
from Modules.Core.data_objects import BaseLightingData, ControllerData
from test import xml_data
from test.testing_mixin import SetupPyHouseObj
from Modules.Utilities.tools import PrettyPrintAny

XML = """
<Test b1='True' f1='3.14158265' i1='371' t1='Test of text attribute' >
    <BoolField1>True</BoolField1>
    <BoolField2>False</BoolField2>
    <BoolField3>Howdy</BoolField3>
    <FloatField>3.14158265</FloatField>
    <IntField>246</IntField>
    <TextField1>Test of text element</TextField1>
    <UUIDField>01234567-fedc-2468-7531-0123456789ab</UUIDField>
    <Part_3 b3='True' f3='3.14158265' i3='371' t3='Test of text'>
        <b4>True</b4>
    </Part_3>
    <IPv4>98.76.0.123</IPv4>
    <IPv6>1234:dead::beef</IPv6>
    <ExternalIPv6>1234:5678::1</ExternalIPv6>
    <DateTime>2014-10-02T12:34:56</DateTime>
</Test>
"""

class SetupMixin(object):
    """
    """

    def setUp(self, p_root):
        self.m_pyhouse_obj = SetupPyHouseObj().BuildPyHouseObj(p_root)
        self.m_xml = SetupPyHouseObj().BuildXml(p_root)


class A01_Compound(SetupMixin, unittest.TestCase):
    """
    This series tests the complex PutGetXML class methods
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(xml_data.XML_LONG))
        self.m_fields = ET.fromstring(XML)
        self.m_api = xml_tools.PutGetXML()

    def test_01_GetIpV4(self):
        l_elem = self.m_api.get_ip_from_xml(self.m_fields, 'IPv4')
        self.assertEqual(l_elem, convert.str_to_long('98.76.0.123'))
        print('Element = {}'.format(l_elem))

    def test_02_GetIPv6(self):
        l_elem = self.m_api.get_ip_from_xml(self.m_fields, 'IPv6')
        self.assertEqual(l_elem, convert.str_to_long('1234:dead::beef'))
        print('Element = {}'.format(l_elem))

    def test_03_GetDateTime(self):
        l_elem = self.m_api.get_date_time_from_xml(self.m_fields, 'DateTime')
        self.assertEqual(l_elem, datetime.datetime(2014, 10, 2, 12, 34, 56))
        print('Element = {}'.format(l_elem))



class A02_GetAnyField(SetupMixin, unittest.TestCase):
    """
    """
    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(xml_data.XML_LONG))
        self.m_fields = ET.fromstring(XML)
        self.m_api = xml_tools.PutGetXML()

    def test_01_Missing(self):
        l_missing = self.m_api._get_any_field(self.m_fields, 'NoValidName')
        print l_missing
        self.assertIsNone(l_missing)

    def test_02_Element(self):
        l_result = self.m_api._get_any_field(self.m_fields, 'IntField')
        print l_result
        self.assertEqual(l_result, '246')

    def test_03_Attribute(self):
        l_result = self.m_api._get_any_field(self.m_fields, 'i1')
        print l_result
        self.assertEqual(l_result, '371')



class C01_XML(SetupMixin, unittest.TestCase):
    """
    This series tests the PutGetXML class methods
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(xml_data.XML_LONG))
        self.m_fields = ET.fromstring(XML)
        self.m_api = xml_tools.PutGetXML()

    def test_01_GetElement(self):
        l_elem = self.m_api._get_element_field(self.m_fields, 'TextField1')
        self.assertEqual(l_elem, 'Test of text element')
        print('Element = {}'.format(l_elem))

    def test_02_GetElement_attribute(self):
        l_elem = self.m_api._get_element_field(self.m_fields, 't1')
        self.assertEqual(l_elem, None)
        print('Element = {}'.format(l_elem))

    def test_03_GetElement_Missing(self):
        l_elem = self.m_api._get_element_field(self.m_fields, 'MissingElement')
        self.assertEqual(l_elem, None)
        print('Element = {}'.format(l_elem))


    def test_11_GetAttribute(self):
        l_attr = self.m_api._get_attribute_field(self.m_fields, 't1')
        self.assertEqual(l_attr, 'Test of text attribute')
        print('Attribute = {}'.format(l_attr))

    def test_12_GetAttribute_element(self):
        l_attr = self.m_api._get_attribute_field(self.m_fields, 'TextField1')
        self.assertEqual(l_attr, None)
        print('Attribute = {0:}'.format(l_attr))

    def test_13_GetAttribute_Missing(self):
        l_attr = self.m_api._get_attribute_field(self.m_fields, 'MissingAttribute')
        self.assertEqual(l_attr, None)
        print('Attribute = {0:}'.format(l_attr))


    def test_21_GetAnyField_Element(self):
        l_field = self.m_api._get_any_field(self.m_fields, 'TextField1')
        self.assertEqual(l_field, 'Test of text element')
        print('Element = {0:}'.format(l_field))

    def test_22_GetAnyField_Attribute(self):
        l_field = self.m_api._get_any_field(self.m_fields, 't1')
        self.assertEqual(l_field, 'Test of text attribute')
        print('Element = {0:}'.format(l_field))

    def test_23_GetAnyField_Missing(self):
        l_field = self.m_api._get_any_field(self.m_fields, 'NoSuchField')
        self.assertEqual(l_field, None)
        print('Element = {0:}'.format(l_field))


    def test_31_GetBoolElement(self):
        result = self.m_api.get_bool_from_xml(self.m_fields, 'BoolField1')
        self.assertTrue(result)

    def test_32_GetBoolAttribute(self):
        result = self.m_api.get_bool_from_xml(self.m_fields, 'b1')
        self.assertTrue(result)

    def test_33_GetBoolPath(self):
        """This should find a path name field
        """
        result = self.m_api.get_bool_from_xml(self.m_fields, './Part_3/b4')
        self.assertTrue(result)

    def test_34_GetBoolFalse(self):
        result = self.m_api.get_bool_from_xml(self.m_fields, 'BoolField2')
        self.assertFalse(result)

    def test_35_GetBoolInvalid(self):
        result = self.m_api.get_bool_from_xml(self.m_fields, 'BoolField3')
        self.assertFalse(result)

    def test_36_GetBoolMissing(self):
        result = self.m_api.get_bool_from_xml(self.m_fields, 'BoolField999')
        self.assertFalse(result)

    def test_37_PutBoolElement(self):
        l_element = ET.Element('TestBoolElement_1')
        self.m_api.put_bool_element(l_element, 'Active', True)
        PrettyPrintAny(l_element, 'bool', 120)

    def test_38_PutBoolAttribute(self):
        l_element = ET.Element('TestBoolAttribute_2')
        self.m_api.put_bool_attribute(l_element, 'Active', True)
        PrettyPrintAny(l_element, 'bool', 120)


    def test_41_GetIntElement(self):
        result = self.m_api.get_int_from_xml(self.m_fields, 'IntField')
        self.assertEqual(result, 246)

    def test_42_GetIntAttribute(self):
        result = self.m_api.get_int_from_xml(self.m_fields, 'i1')
        self.assertEqual(result, 371)

    def test_43_PutIntElement(self):
        l_element = ET.Element('TestIntElement_1')
        self.m_api.put_int_element(l_element, 'IntNumber', -57)
        PrettyPrintAny(l_element, 'bool', 120)

    def test_44_PutIntAttribute(self):
        l_element = ET.Element('TestIntAttribute_2')
        self.m_api.put_int_attribute(l_element, 'IntNumber', 853)
        PrettyPrintAny(l_element, 'bool', 120)


    def test_51_GetTextElement(self):
        l_text = self.m_api.get_text_from_xml(self.m_fields, 'TextField1')
        self.assertEqual(l_text, 'Test of text element')
        print('Text = {0:}'.format(l_text))

    def test_51A_GetTextElement(self):
        """
        we seem to not work if the field is the xml passed in.
        """
        l_text = self.m_api.get_text_from_xml(self.m_fields.find('TextField1'), 'TextField1')
        self.assertEqual(l_text, 'Test of text element')
        print('Text = {0:}'.format(l_text))

    def test_52_GetTextAttribute(self):
        l_text = self.m_api.get_text_from_xml(self.m_fields, 't1')
        self.assertEqual(l_text, 'Test of text attribute')
        print('Text = {0:}'.format(l_text))

    def test_53_GetTextInvalid(self):
        l_text = self.m_api.get_text_from_xml(self.m_fields, 'NoSuchField', '0223 No such field')
        self.assertEqual(l_text, '0223 No such field')
        print('Text = {0:}'.format(l_text))

    def test_53_GetTextInvalid_NoDefault(self):
        l_text = self.m_api.get_text_from_xml(self.m_fields, 'NoSuchField')
        self.assertEqual(l_text, 'None')
        print('Text = {0:}'.format(l_text))

    def test_54_PutTextElement(self):
        l_element = ET.Element('TestTextElement_1')
        self.m_api.put_int_element(l_element, 'Comment', 'Arbitrary Comment')
        PrettyPrintAny(l_element, 'XML A', 120)

    def test_55_PutTextAttribute(self):
        l_element = ET.Element('TestTextAttribute_2')
        self.m_api.put_text_attribute(l_element, 'Name', 'Any old Name')
        PrettyPrintAny(l_element, 'XML B', 120)



    def test_61_GetFloatElement(self):
        result = self.m_api.get_float_from_xml(self.m_fields, 'FloatField')
        self.assertAlmostEqual(result, float(3.1415825435), places = 5, msg = 'get_float_from_xml failed')

    def test_62_GetFloatAttribute(self):
        result = self.m_api.get_float_from_xml(self.m_fields, 'f1')
        self.assertAlmostEqual(result, float(3.1415825435), places = 5, msg = 'get_float_from_xml failed')



    def test_71_GetUuidElement(self):
        """UUID elements must be returned intact
        """
        l_uuid = self.m_api.get_uuid_from_xml(self.m_fields, 'UUIDField')
        self.assertEqual(l_uuid, '01234567-fedc-2468-7531-0123456789ab')
        print('UUID = {0:}'.format(l_uuid))

    def test_72_GetUuidAttribute(self):
        l_uuid = self.m_api.get_uuid_from_xml(self.m_fields, 'IntField')
        # self.assertNotEqual(l_uuid, None)
        print('UUID = {0:}'.format(l_uuid))

    def test_73_GetUuidMissing(self):
        l_uuid = self.m_api.get_uuid_from_xml(self.m_fields, 'NoSuchField')
        self.assertEqual(l_uuid, None)
        print('UUID = {0:}'.format(l_uuid))



class C03_ConfigTools(SetupMixin, unittest.TestCase):
    """
    This tests the ConfigTools section
    """

    def setUp(self):
        self.m_pyhouse_obj = SetupMixin.setUp(self, ET.fromstring(xml_data.XML_LONG))
        self.m_api = xml_tools.XmlConfigTools()

    def test_01_readBaseObject(self):
        l_base_obj = BaseLightingData()
        self.m_api.read_base_object_xml(l_base_obj, self.m_xml.light)
        PrettyPrintAny(l_base_obj, 'Light')
        self.assertEqual(l_base_obj.Name, 'outside_front', 'Bad Name')
        self.assertEqual(l_base_obj.Key, 0, 'Bad Key')
        self.assertEqual(l_base_obj.Active, True, 'Bad Active')
        self.assertEqual(l_base_obj.UUID, 'c15f7d76-092e-11e4-bffa-b827eb189eb4', 'Bad UUID')

    def test_02_readBaseObject(self):
        l_base_obj = BaseLightingData()
        self.m_api.read_base_object_xml(l_base_obj, self.m_xml.controller)
        PrettyPrintAny(l_base_obj, 'Controller')
        self.assertEqual(l_base_obj.Name, 'PLM_1', 'Bad Name')
        self.assertEqual(l_base_obj.Key, 0, 'Bad Key')
        self.assertEqual(l_base_obj.Active, False, 'Bad Active')

    def test_11_writeBaseObject(self):
        l_base_obj = BaseLightingData()
        self.m_api.read_base_object_xml(l_base_obj, self.m_xml.light)
        l_xml = self.m_api.write_base_object_xml('Light', l_base_obj)
        PrettyPrintAny(l_xml, 'Base Object XML', 120)


class C05_NoClass(SetupMixin, unittest.TestCase):
    """
    This tests the no class routines.
    """

    def setUp(self):
        self.m_pyhouse_obj = SetupMixin.setUp(self, ET.fromstring(xml_data.XML_LONG))

    def test_01_StuffAttrs(self):
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
