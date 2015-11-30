"""
@name:      PyHouse/src/Modules/Utilities/test/test_xml_tools.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: 2013-2015 by D. Brian Kimmel
@license:   MIT License
@note:      Created on Apr 11, 2013
@summary:   This module is for testing XML tools.

Passed all 50 testa - DBK 2015-09-01

"""

# Import system type stuff
# import copy
import xml.etree.ElementTree as ET
from twisted.trial import unittest
import datetime

# Import PyMh files and modules.
from Modules.Utilities.xml_tools import XML, PutGetXML, XmlConfigTools, stuff_new_attrs
from Modules.Utilities import convert
from Modules.Core.data_objects import CoreLightingData, LocationData
from test import xml_data
from test.testing_mixin import SetupPyHouseObj
from Modules.Utilities.debug_tools import PrettyFormatAny
# from Modules.Utilities.debug_tools import PrettyFormatAny

XML_INT = """
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
    <IPv4>98.76.45.123</IPv4>
    <IPv6>1234:dead::beef</IPv6>
    <ExternalIPv6>1234:5678::1</ExternalIPv6>
    <DateTime>2014-10-02T12:34:56</DateTime>
    <RoomCoords1>[0.0, 1.1, 2.2]</RoomCoords1>
    <RoomCoords2>['0', '1.1', "2.2"]</RoomCoords2>
</Test>
"""

class SetupMixin(object):
    """
    """

    def setUp(self, p_root):
        self.m_pyhouse_obj = SetupPyHouseObj().BuildPyHouseObj(p_root)
        self.m_xml = SetupPyHouseObj().BuildXml(p_root)


class A1_Compound(SetupMixin, unittest.TestCase):
    """
    This series tests the complex PutGetXML class methods
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(xml_data.XML_LONG))
        self.m_fields = ET.fromstring(XML_INT)
        self.m_api = PutGetXML

    def test_01_GetIpV4(self):
        l_elem = self.m_api.get_ip_from_xml(self.m_fields, 'IPv4')
        self.assertEqual(l_elem, convert.str_to_long('98.76.45.123'))

    def test_02_GetIPv6(self):
        l_elem = self.m_api.get_ip_from_xml(self.m_fields, 'IPv6')
        self.assertEqual(l_elem, convert.str_to_long('1234:dead::beef'))

    def test_03_GetDateTime(self):
        l_elem = self.m_api.get_date_time_from_xml(self.m_fields, 'DateTime')
        self.assertEqual(l_elem, datetime.datetime(2014, 10, 2, 12, 34, 56))


class A2_GetAnyField(SetupMixin, unittest.TestCase):
    """
    """
    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(xml_data.XML_LONG))
        self.m_fields = ET.fromstring(XML_INT)
        self.m_api = PutGetXML

    def test_01_Missing(self):
        l_missing = XML.get_any_field(self.m_fields, 'NoValidName')
        self.assertIsNone(l_missing)

    def test_02_Element(self):
        l_result = XML.get_any_field(self.m_fields, 'IntField')
        self.assertEqual(l_result, '246')

    def test_03_Attribute(self):
        l_result = XML.get_any_field(self.m_fields, 'i1')
        self.assertEqual(l_result, '371')


class B01_Attribute(SetupMixin, unittest.TestCase):
    """
    This series tests the PutGetXML class methods
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(xml_data.XML_LONG))
        self.m_fields = ET.fromstring(XML_INT)
        self.m_api = PutGetXML

    def test_01_GetElement(self):
        l_elem = XML.get_element_field(self.m_fields, 'TextField1')
        self.assertEqual(l_elem, 'Test of text element')

    def test_02_GetElement_attribute(self):
        l_elem = XML.get_element_field(self.m_fields, 't1')
        self.assertEqual(l_elem, None)

    def test_03_GetElement_Missing(self):
        l_elem = XML.get_element_field(self.m_fields, 'MissingElement')
        self.assertEqual(l_elem, None)


class B02_Element(SetupMixin, unittest.TestCase):
    """
    This series tests the PutGetXML class methods
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(xml_data.XML_LONG))
        self.m_fields = ET.fromstring(XML_INT)
        self.m_api = PutGetXML

    def test_01_GetAttribute(self):
        l_attr = XML.get_attribute_field(self.m_fields, 't1')
        self.assertEqual(l_attr, 'Test of text attribute')

    def test_02_GetAttribute_element(self):
        l_attr = XML.get_attribute_field(self.m_fields, 'TextField1')
        self.assertEqual(l_attr, None)

    def test_03_GetAttribute_Missing(self):
        l_attr = XML.get_attribute_field(self.m_fields, 'MissingAttribute')
        self.assertEqual(l_attr, None)


class B03_AnyField(SetupMixin, unittest.TestCase):
    """
    This series tests the PutGetXML class methods
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(xml_data.XML_LONG))
        self.m_fields = ET.fromstring(XML_INT)
        self.m_api = PutGetXML

    def test_01_GetAnyField_Element(self):
        l_field = XML.get_any_field(self.m_fields, 'TextField1')
        self.assertEqual(l_field, 'Test of text element')

    def test_02_GetAnyField_Attribute(self):
        l_field = XML.get_any_field(self.m_fields, 't1')
        self.assertEqual(l_field, 'Test of text attribute')

    def test_03_GetAnyField_Missing(self):
        l_field = XML.get_any_field(self.m_fields, 'NoSuchField')
        self.assertEqual(l_field, None)


class B04_Boolean(SetupMixin, unittest.TestCase):
    """
    This series tests the PutGetXML class methods
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(xml_data.XML_LONG))
        self.m_fields = ET.fromstring(XML_INT)
        self.m_api = PutGetXML

    def test_01_GetElement(self):
        result = self.m_api.get_bool_from_xml(self.m_fields, 'BoolField1')
        self.assertTrue(result)

    def test_02_GetAttribute(self):
        result = self.m_api.get_bool_from_xml(self.m_fields, 'b1')
        self.assertTrue(result)

    def test_03_GetPath(self):
        """This should find a path name field
        """
        result = self.m_api.get_bool_from_xml(self.m_fields, './Part_3/b4')
        self.assertTrue(result)

    def test_04_GetFalse(self):
        result = self.m_api.get_bool_from_xml(self.m_fields, 'BoolField2')
        self.assertFalse(result)

    def test_05_FalseDirect(self):
        result = PutGetXML.get_bool_from_xml(self.m_fields, 'BoolField2')
        self.assertFalse(result)

    def test_05_GetInvalid(self):
        result = self.m_api.get_bool_from_xml(self.m_fields, 'BoolField3')
        self.assertFalse(result)

    def test_06_GetMissing(self):
        result = self.m_api.get_bool_from_xml(self.m_fields, 'BoolField999')
        self.assertFalse(result)

    def test_07_PutElement(self):
        l_element = ET.Element('TestBoolElement_1')
        self.m_api.put_bool_element(l_element, 'Active', True)
        self.assertEqual(bool(l_element._children[0].text), True)

    def test_08_PutAttribute(self):
        l_element = ET.Element('TestBoolAttribute_2')
        self.m_api.put_bool_attribute(l_element, 'Active', True)
        self.assertEqual(l_element.attrib['Active'], 'True')


class B05_Integer(SetupMixin, unittest.TestCase):
    """
    This series tests the PutGetXML class methods
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(xml_data.XML_LONG))
        self.m_fields = ET.fromstring(XML_INT)
        self.m_api = PutGetXML

    def test_01_GetIntElement(self):
        result = self.m_api.get_int_from_xml(self.m_fields, 'IntField')
        self.assertEqual(result, 246)

    def test_02_GetIntAttribute(self):
        result = self.m_api.get_int_from_xml(self.m_fields, 'i1')
        self.assertEqual(result, 371)

    def test_03_PutIntElement(self):
        l_element = ET.Element('TestIntElement_1')
        self.m_api.put_int_element(l_element, 'IntNumber', -57)
        self.assertEqual(int(l_element._children[0].text), -57)

    def test_04_PutIntAttribute(self):
        l_element = ET.Element('TestIntAttribute_2')
        self.m_api.put_int_attribute(l_element, 'IntNumber', 853)
        self.assertEqual(int(l_element.attrib['IntNumber']), 853)


class B06_Text(SetupMixin, unittest.TestCase):
    """
    This series tests the PutGetXML class methods
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(xml_data.XML_LONG))
        self.m_fields = ET.fromstring(XML_INT)
        self.m_api = PutGetXML

    def test_01_GetTextElement(self):
        l_text = self.m_api.get_text_from_xml(self.m_fields, 'TextField1')
        self.assertEqual(l_text, 'Test of text element')

    def test_02_GetTextElement(self):
        """
        we seem to not work if the field is the xml passed in.
        """
        l_text = self.m_api.get_text_from_xml(self.m_fields.find('TextField1'), 'TextField1')
        self.assertEqual(l_text, 'Test of text element')

    def test_03_GetTextAttribute(self):
        l_text = self.m_api.get_text_from_xml(self.m_fields, 't1')
        self.assertEqual(l_text, 'Test of text attribute')

    def test_04_GetTextInvalid(self):
        l_text = self.m_api.get_text_from_xml(self.m_fields, 'NoSuchField', '0223 No such field')
        self.assertEqual(l_text, '0223 No such field')

    def test_05_GetTextInvalid_NoDefault(self):
        l_text = self.m_api.get_text_from_xml(self.m_fields, 'NoSuchField')
        self.assertEqual(l_text, 'None')

    def test_06_PutTextElement(self):
        l_element = ET.Element('TestTextElement_1')
        self.m_api.put_int_element(l_element, 'Comment', 'Arbitrary Comment')
        self.assertEqual(l_element._children[0].text, 'Arbitrary Comment')

    def test_07_PutTextAttribute(self):
        l_element = ET.Element('TestTextAttribute_2')
        self.m_api.put_text_attribute(l_element, 'Name', 'Any old Name')
        self.assertEqual(l_element.attrib['Name'], 'Any old Name')


class B07_Float(SetupMixin, unittest.TestCase):
    """
    This series tests the PutGetXML class methods
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(xml_data.XML_LONG))
        self.m_fields = ET.fromstring(XML_INT)
        self.m_api = PutGetXML

    def test_01_GetFloatElement(self):
        result = self.m_api.get_float_from_xml(self.m_fields, 'FloatField')
        self.assertAlmostEqual(result, float(3.1415825435), places = 5, msg = 'get_float_from_xml failed')

    def test_02_GetFloatAttribute(self):
        result = self.m_api.get_float_from_xml(self.m_fields, 'f1')
        self.assertAlmostEqual(result, float(3.1415825435), places = 5, msg = 'get_float_from_xml failed')


class B08_UUID(SetupMixin, unittest.TestCase):
    """
    This series tests the PutGetXML class methods
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(xml_data.XML_LONG))
        self.m_fields = ET.fromstring(XML_INT)
        self.m_api = PutGetXML

    def test_01_GetUuidElement(self):
        """UUID elements must be returned intact
        """
        l_uuid = self.m_api.get_uuid_from_xml(self.m_fields, 'UUIDField')
        self.assertEqual(l_uuid, '01234567-fedc-2468-7531-0123456789ab')

    def test_02_GetUuidMissing(self):
        l_uuid = self.m_api.get_uuid_from_xml(self.m_fields, 'NoSuchField')
        self.assertEqual(l_uuid, None)


class B09_IP(SetupMixin, unittest.TestCase):
    """
    This series tests the PutGetXML class methods
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(xml_data.XML_LONG))
        self.m_fields = ET.fromstring(XML_INT)
        self.m_api = PutGetXML

    def test_01_IPv4(self):
        l_ip = self.m_api.get_ip_from_xml(self.m_fields, 'IPv4')
        self.assertEqual(l_ip, convert.str_to_long('98.76.45.123'))

    def test_02_IPv6(self):
        l_ip = self.m_api.get_ip_from_xml(self.m_fields, 'IPv6')
        self.assertEqual(l_ip, convert.str_to_long('1234:dead::beef'))


class B10_DateTime(SetupMixin, unittest.TestCase):
    """
    This series tests the PutGetXML class methods
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(xml_data.XML_LONG))
        self.m_fields = ET.fromstring(XML_INT)
        self.m_api = PutGetXML

    def test_01_DateTime(self):
        l_date = self.m_api.get_date_time_from_xml(self.m_fields, 'DateTime')
        l_dt = datetime.datetime(2014, 10, 2, 12, 34, 56)
        self.assertEqual(l_date, l_dt)


class B11_Coords(SetupMixin, unittest.TestCase):
    """
    This series tests the PutGetXML class methods
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(xml_data.XML_LONG))
        self.m_fields = ET.fromstring(XML_INT)
        self.m_api = PutGetXML

    def test_01_Coords(self):
        l_coords = self.m_api.get_coords_from_xml(self.m_fields, 'RoomCoords1')
        self.assertEqual(l_coords.X_Easting, 0.0)
        self.assertEqual(l_coords.Y_Northing, 1.1)
        self.assertEqual(l_coords.Z_Height, 2.2)

    def test_02_Coords(self):
        l_coords = self.m_api.get_coords_from_xml(self.m_fields, 'RoomCoords2')
        l_element = ET.Element('Test B11-02')
        self.m_api.put_coords_element(l_element, 'CoOrds', l_coords)
        self.assertEqual(l_element._children[0].text, '[0.0,1.1,2.2]')


class C3_Read(SetupMixin, unittest.TestCase):
    """
    This tests the ConfigTools section
    """

    def setUp(self):
        self.m_pyhouse_obj = SetupMixin.setUp(self, ET.fromstring(xml_data.XML_LONG))
        self.m_api = XmlConfigTools()

    def test_01_BaseObject(self):
        l_base_obj = CoreLightingData()
        self.m_api.read_base_object_xml(l_base_obj, self.m_xml.light)
        self.assertEqual(l_base_obj.Name, 'Insteon Light')
        self.assertEqual(l_base_obj.Key, 0)
        self.assertEqual(l_base_obj.Active, True)
        # self.assertEqual(l_base_obj.UUID, 'c15f7d76-092e-11e4-bffa-b827eb189eb4', 'Bad UUID')

    def test_02_readBaseObject(self):
        l_base_obj = CoreLightingData()
        self.m_api.read_base_object_xml(l_base_obj, self.m_xml.controller)
        self.assertEqual(l_base_obj.Name, 'Insteon Serial Controller')
        self.assertEqual(l_base_obj.Key, 0)
        self.assertEqual(l_base_obj.Active, True)


class C4_ReadEmpty(SetupMixin, unittest.TestCase):
    """
    This tests the ConfigTools section
    """

    def setUp(self):
        self.m_pyhouse_obj = SetupMixin.setUp(self, ET.fromstring(xml_data.XML_EMPTY))
        self.m_api = XmlConfigTools()

    def test_01_BaseObject(self):
        l_base_obj = CoreLightingData()
        self.m_api.read_base_object_xml(l_base_obj, self.m_xml.light)
        self.assertEqual(l_base_obj.Name, 'Missing Name')
        self.assertEqual(l_base_obj.Key, 0)
        self.assertEqual(l_base_obj.Active, False)


class C5_Write(SetupMixin, unittest.TestCase):
    """
    This tests the ConfigTools section
    """

    def setUp(self):
        self.m_pyhouse_obj = SetupMixin.setUp(self, ET.fromstring(xml_data.XML_LONG))

    def test_01_BaseObject(self):
        """Write Base Object XML w/UUID
        """
        l_base_obj = CoreLightingData()
        XmlConfigTools.read_base_object_xml(l_base_obj, self.m_xml.light)
        l_base_obj.Key = 43
        l_uuid = '12345678-fedc-1111-ffff-aaBBccDDeeFF'
        l_base_obj.UUID = l_uuid
        l_xml = XmlConfigTools.write_base_object_xml('Light', l_base_obj)
        print(PrettyFormatAny.form(l_xml, 'XML'))
        self.assertEqual(l_xml.attrib['Name'], 'Insteon Light')
        self.assertEqual(l_xml.attrib['Key'], '43')
        self.assertEqual(l_xml.find('UUID').text, l_uuid)

    def test_02_BaseObject(self):
        """Write Base Object XML w/ NO UUID
        """
        l_base_obj = CoreLightingData()
        XmlConfigTools.read_base_object_xml(l_base_obj, self.m_xml.light)
        l_base_obj.Key = 44
        l_xml = XmlConfigTools.write_base_object_xml('Light', l_base_obj, no_uuid = True)
        print(PrettyFormatAny.form(l_xml, 'XML'))
        self.assertEqual(l_xml.attrib['Name'], 'Insteon Light')
        self.assertEqual(l_xml.attrib['Key'], '44')



class D1_NoClass(SetupMixin, unittest.TestCase):
    """
    This tests the no class routines.
    """

    def setUp(self):
        self.m_pyhouse_obj = SetupMixin.setUp(self, ET.fromstring(xml_data.XML_LONG))

    def test_01_StuffAttrs(self):
        l_objA = CoreLightingData()
        l_objA.Name = 'Test 1A'
        # print(PrettyFormatAny.form(l_objA, 'Obj A'))
        l_objB = LocationData()
        l_objB.Street = 'Some road'
        # print(PrettyFormatAny.form(l_objB, 'Obj B', 120))
        #
        stuff_new_attrs(l_objA, l_objB)
        # print(PrettyFormatAny.form(l_objA, 'Result B stuffed into A', 120))
        self.assertEqual(l_objA.Street, 'Some road')

# ## END DBK
