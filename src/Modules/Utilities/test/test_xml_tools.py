"""
@name:      PyHouse/src/Modules/Utilities/test/test_xml_tools.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: 2013-2016 by D. Brian Kimmel
@license:   MIT License
@note:      Created on Apr 11, 2013
@summary:   This module is for testing XML tools.

Passed 49 of 49 testa - DBK 2016-06-12

"""

# Import system type stuff
# import copy
import xml.etree.ElementTree as ET
from twisted.trial import unittest
import datetime

# Import PyMh files and modules.
from Modules.Core.data_objects import CoreLightingData, LocationData
from Modules.Utilities.xml_tools import XML, PutGetXML, XmlConfigTools, stuff_new_attrs
from Modules.Utilities import convert
from Modules.Utilities.test.xml_xml_tools import \
    TESTING_XML_BOOL_0, \
    XML_TEST, \
    TESTING_XML_INT_0, \
    TESTING_XML_IPV4_0, \
    TESTING_XML_IPV6_0, \
    TESTING_XML_TEXT_0, \
    TESTING_XML_TEXT_1, \
    TESTING_XML_FLOAT_0, \
    TESTING_XML_ROOM_X_0, \
    TESTING_XML_ROOM_Y_0, \
    TESTING_XML_ROOM_Z_0, \
    TESTING_XML_BOOL_1, \
    TESTING_XML_BOOL_2, \
    TESTING_XML_UUID_0, \
    TESTING_XML_YEAR_0, \
    TESTING_XML_MONTH_0, \
    TESTING_XML_DAY_0, \
    TESTING_XML_HOUR_0, \
    TESTING_XML_MINUTE_0, \
    TESTING_XML_SECOND_0, \
    TESTING_XML_TEXT_A0, \
    TESTING_XML_BOOL_A0, \
    TESTING_XML_FLOAT_A0, \
    TESTING_XML_INT_A0, TESTING_XML_DATE_TIME_0
from test.xml_data import XML_LONG, XML_EMPTY
from test.testing_mixin import SetupPyHouseObj
from Modules.Utilities.debug_tools import PrettyFormatAny


class SetupMixin(object):
    """
    """

    def setUp(self, p_root):
        self.m_pyhouse_obj = SetupPyHouseObj().BuildPyHouseObj(p_root)
        self.m_xml = SetupPyHouseObj().BuildXml(p_root)
        self.m_api = PutGetXML


class A1_Setup(SetupMixin, unittest.TestCase):
    """
    This tests the setup to see if everything is there.
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))
        self.m_fields = ET.fromstring(XML_TEST)

    def test_01_Setup(self):
        l_xml = self.m_fields
        # print(PrettyFormatAny.form(l_xml, 'Fields A1-1'))
        self.assertEqual(l_xml.find('Int0').text, TESTING_XML_INT_0)
        self.assertEqual(l_xml.find('IpV40').text, TESTING_XML_IPV4_0)


class A2_XML(SetupMixin, unittest.TestCase):
    """
    This texts the XML to see if it is proper.
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))
        self.m_fields = ET.fromstring(XML_TEST)

    def test_01_Setup(self):
        l_xml = self.m_fields
        # print(PrettyFormatAny.form(l_xml, 'Fields A2-1'))
        self.assertEqual(l_xml.find('Int0').text, TESTING_XML_INT_0)
        self.assertEqual(l_xml.find('IpV40').text, TESTING_XML_IPV4_0)


class B1_Element(SetupMixin, unittest.TestCase):
    """
    This series tests the PutGetXML class methods
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))
        self.m_fields = ET.fromstring(XML_TEST)

    def test_1_Text(self):
        l_elem = XML.get_element_field(self.m_fields, 'Text0')
        self.assertEqual(l_elem, TESTING_XML_TEXT_0)

    def test_2_Bool(self):
        l_elem = XML.get_element_field(self.m_fields, 'Bool0')
        self.assertEqual(l_elem, TESTING_XML_BOOL_0)

    def test_3_Int(self):
        l_elem = XML.get_element_field(self.m_fields, 'Int0')
        self.assertEqual(l_elem, TESTING_XML_INT_0)

    def test_4_Float(self):
        l_elem = XML.get_element_field(self.m_fields, 'Float0')
        self.assertEqual(l_elem, TESTING_XML_FLOAT_0)


class B2_Attribute(SetupMixin, unittest.TestCase):
    """
    This series tests the PutGetXML class methods
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))
        self.m_fields = ET.fromstring(XML_TEST)

    def test_01_GetAttribute(self):
        l_attr = XML.get_attribute_field(self.m_fields, 'BoolA0')
        self.assertEqual(l_attr, TESTING_XML_BOOL_A0)

    def test_02_GetAttribute_element(self):
        l_attr = XML.get_attribute_field(self.m_fields, 'FloatA0')
        self.assertEqual(l_attr, TESTING_XML_FLOAT_A0)

    def test_03_GetAttribute_element(self):
        l_attr = XML.get_attribute_field(self.m_fields, 'IntA0')
        self.assertEqual(l_attr, TESTING_XML_INT_A0)

    def test_04_GetAttribute_element(self):
        l_attr = XML.get_attribute_field(self.m_fields, 'TextA0')
        self.assertEqual(l_attr, TESTING_XML_TEXT_A0)

    def test_05_GetAttribute_Missing(self):
        l_attr = XML.get_attribute_field(self.m_fields, 'MissingAttribute')
        self.assertEqual(l_attr, None)


class B3_AnyField(SetupMixin, unittest.TestCase):
    """
    This series tests the PutGetXML class methods
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))
        self.m_fields = ET.fromstring(XML_TEST)

    def test_01_GetAnyField_Element(self):
        l_field = XML.get_any_field(self.m_fields, 'Text1')
        self.assertEqual(l_field, TESTING_XML_TEXT_1)

    def test_02_GetAnyField_Attribute(self):
        l_field = XML.get_any_field(self.m_fields, 'TextA0')
        self.assertEqual(l_field, TESTING_XML_TEXT_A0)

    def test_03_GetAnyField_Missing(self):
        l_field = XML.get_any_field(self.m_fields, 'NoSuchField')
        self.assertEqual(l_field, None)


class C1_Boolean(SetupMixin, unittest.TestCase):
    """
    This series tests the PutGetXML class methods
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))
        self.m_fields = ET.fromstring(XML_TEST)

    def test_01_Element(self):
        l_result = self.m_api.get_bool_from_xml(self.m_fields, 'Bool0')
        self.assertEqual(str(l_result), TESTING_XML_BOOL_0)

    def test_02_Element(self):
        l_result = self.m_api.get_bool_from_xml(self.m_fields, 'Bool1')
        self.assertEqual(str(l_result), TESTING_XML_BOOL_1)

    def test_03_Attribute(self):
        l_result = self.m_api.get_bool_from_xml(self.m_fields, 'BoolA1')
        self.assertEqual(str(l_result), TESTING_XML_BOOL_0)

    def test_04_Path(self):
        """This should find a path name field
        """
        l_result = (self.m_api.get_bool_from_xml(self.m_fields, './SubTest/BoolA1') == True)
        # print(PrettyFormatAny.form(l_result, 'Fields C1-3'))
        self.assertEqual(str(l_result), TESTING_XML_BOOL_0)

    def test_05_GetFalse(self):
        l_result = self.m_api.get_bool_from_xml(self.m_fields, 'Bool2')
        self.assertNotEqual(str(l_result), TESTING_XML_BOOL_2)

    def test_06_FalseDirect(self):
        result = PutGetXML.get_bool_from_xml(self.m_fields, 'Bool2')
        self.assertFalse(result)

    def test_07_GetInvalid(self):
        result = self.m_api.get_bool_from_xml(self.m_fields, 'BoolField3')
        self.assertFalse(result)

    def test_08_GetMissing(self):
        l_result = self.m_api.get_bool_from_xml(self.m_fields, 'BoolField999')
        self.assertFalse(l_result)

    def test_09_PutElement(self):
        l_element = ET.Element('TestBoolElement_1')
        self.m_api.put_bool_element(l_element, 'Active', True)
        self.assertEqual(bool(l_element._children[0].text), True)

    def test_10_PutAttribute(self):
        l_element = ET.Element('TestBoolAttribute_2')
        self.m_api.put_bool_attribute(l_element, 'Active', True)
        self.assertEqual(l_element.attrib['Active'], 'True')


class C2_Integer(SetupMixin, unittest.TestCase):
    """
    This series tests the PutGetXML class methods
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))
        self.m_fields = ET.fromstring(XML_TEST)

    def test_1_GetIntElement(self):
        l_result = self.m_api.get_int_from_xml(self.m_fields, 'Int0')
        self.assertEqual(l_result, int(TESTING_XML_INT_0))

    def test_2_GetIntAttribute(self):
        l_result = self.m_api.get_int_from_xml(self.m_fields, 'IntA0')
        print(PrettyFormatAny.form(l_result, 'Fields C2-2'))
        self.assertEqual(l_result, int(TESTING_XML_INT_A0))

    def test_3_PutIntElement(self):
        l_element = ET.Element('TestIntElement_1')
        # print(PrettyFormatAny.form(l_element, 'Fields C2-3'))
        self.m_api.put_int_element(l_element, 'IntNumber', -57)
        self.assertEqual(int(l_element._children[0].text), -57)

    def test_4_PutIntAttribute(self):
        l_element = ET.Element('TestIntAttribute_2')
        self.m_api.put_int_attribute(l_element, 'IntNumber', 853)
        self.assertEqual(int(l_element.attrib['IntNumber']), 853)


class C3_Text(SetupMixin, unittest.TestCase):
    """
    This series tests the PutGetXML class methods
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))
        self.m_fields = ET.fromstring(XML_TEST)

    def test_01_GetTextElement(self):
        l_text = self.m_api.get_text_from_xml(self.m_fields, 'Text0')
        self.assertEqual(l_text, TESTING_XML_TEXT_0)

    def test_02_GetTextElement(self):
        """
        we seem to not work if the field is the xml passed in.
        """
        l_text = self.m_api.get_text_from_xml(self.m_fields.find('Text0'), 'Text0')
        self.assertEqual(l_text, TESTING_XML_TEXT_0)

    def test_03_GetTextAttribute(self):
        l_text = self.m_api.get_text_from_xml(self.m_fields, 'TextA0')
        self.assertEqual(l_text, TESTING_XML_TEXT_A0)

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


class C4_Float(SetupMixin, unittest.TestCase):
    """
    This series tests the PutGetXML class methods
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))
        self.m_fields = ET.fromstring(XML_TEST)

    def test_01_GetFloatElement(self):
        result = self.m_api.get_float_from_xml(self.m_fields, 'Float0')
        self.assertAlmostEqual(result, float(TESTING_XML_FLOAT_0), places = 5)

    def test_02_GetFloatAttribute(self):
        result = self.m_api.get_float_from_xml(self.m_fields, 'FloatA0')
        self.assertAlmostEqual(result, float(TESTING_XML_FLOAT_A0), places = 5, msg = 'get_float_from_xml failed')


class D1_UUID(SetupMixin, unittest.TestCase):
    """
    This series tests the PutGetXML class methods
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))
        self.m_fields = ET.fromstring(XML_TEST)

    def test_01_GetUuidElement(self):
        """UUID elements must be returned intact
        """
        l_uuid = self.m_api.get_uuid_from_xml(self.m_fields, 'UUID0')
        self.assertEqual(l_uuid, TESTING_XML_UUID_0)


class D2_IP(SetupMixin, unittest.TestCase):
    """
    This series tests the PutGetXML class methods
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))
        self.m_fields = ET.fromstring(XML_TEST)

    def test_01_IPv4(self):
        l_ip = self.m_api.get_ip_from_xml(self.m_fields, 'IpV40')
        self.assertEqual(l_ip, convert.str_to_long(TESTING_XML_IPV4_0))

    def test_02_IPv6(self):
        l_ip = self.m_api.get_ip_from_xml(self.m_fields, 'IpV60')
        self.assertEqual(l_ip, convert.str_to_long(TESTING_XML_IPV6_0))


class D3_DateTime(SetupMixin, unittest.TestCase):
    """
    This series tests the PutGetXML class methods
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))
        self.m_fields = ET.fromstring(XML_TEST)

    def test_1_Read(self):
        l_answer = datetime.datetime(int(TESTING_XML_YEAR_0), int(TESTING_XML_MONTH_0), int(TESTING_XML_DAY_0),
                                     int(TESTING_XML_HOUR_0), int(TESTING_XML_MINUTE_0), int(TESTING_XML_SECOND_0))
        # print(PrettyFormatAny.form(l_answer, 'DateTime D3-1 A'))
        l_date = self.m_api.get_date_time_from_xml(self.m_fields, 'DateTime0')
        self.assertEqual(l_date, l_answer)

    def test_2_Write(self):
        l_date = self.m_api.get_date_time_from_xml(self.m_fields, 'DateTime0')
        l_element = ET.Element('TestDateTime')
        self.m_api.put_date_time_element(l_element, 'TestField', l_date)
        print(PrettyFormatAny.form(l_element, 'DateTime D3-2 A'))
        self.assertEqual(l_element[0].text, TESTING_XML_DATE_TIME_0)


class D4_Coords(SetupMixin, unittest.TestCase):
    """
    This series tests the PutGetXML class methods
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))
        self.m_fields = ET.fromstring(XML_TEST)
        self.m_api = PutGetXML

    def test_01_Coords(self):
        l_coords = self.m_api.get_coords_from_xml(self.m_fields, 'RoomCoords0')
        print(PrettyFormatAny.form(l_coords, 'Coords D4-1 A'))
        self.assertEqual(l_coords.X_Easting, float(TESTING_XML_ROOM_X_0))
        self.assertEqual(l_coords.Y_Northing, float(TESTING_XML_ROOM_Y_0))
        self.assertEqual(l_coords.Z_Height, float(TESTING_XML_ROOM_Z_0))


class E1_Read(SetupMixin, unittest.TestCase):
    """
    This tests the ConfigTools section
    """

    def setUp(self):
        self.m_pyhouse_obj = SetupMixin.setUp(self, ET.fromstring(XML_LONG))
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


class E2_ReadEmpty(SetupMixin, unittest.TestCase):
    """
    This tests the ConfigTools section
    """

    def setUp(self):
        self.m_pyhouse_obj = SetupMixin.setUp(self, ET.fromstring(XML_EMPTY))
        self.m_api = XmlConfigTools()

    def test_01_BaseObject(self):
        l_base_obj = CoreLightingData()
        self.m_api.read_base_object_xml(l_base_obj, self.m_xml.light)
        print(PrettyFormatAny.form(l_base_obj))
        self.assertEqual(l_base_obj.Name, 'None')
        self.assertEqual(l_base_obj.Key, 0)
        self.assertEqual(l_base_obj.Active, False)


class E3_Write(SetupMixin, unittest.TestCase):
    """
    This tests the ConfigTools section
    """

    def setUp(self):
        self.m_pyhouse_obj = SetupMixin.setUp(self, ET.fromstring(XML_LONG))

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


class Z1_NoClass(SetupMixin, unittest.TestCase):
    """
    This tests the no class routines.
    """

    def setUp(self):
        self.m_pyhouse_obj = SetupMixin.setUp(self, ET.fromstring(XML_LONG))

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
